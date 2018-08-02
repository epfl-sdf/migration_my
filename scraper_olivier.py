import datetime
import os
import re
import time
from bs4 import BeautifulSoup

import pandas as pd
import requests

ALL_PAGES = set()
VISITED = set()
bad_extensions = ['css', 'js', 'ico', 'png', 'jpg', 'pdf']
good_extensions = ['html', 'php', 'ejs']


def links_in_page(domain_url, page_url):
    links = set()
    error_message = None
    if page_url[-1:] != '/':
        page_url += '/'
    try:
        response = requests.get(page_url)
        if not response.ok:
            try:
                ALL_PAGES.remove(page_url)
            except KeyError:
                pass
            return None, None
        soup = BeautifulSoup(response.text, 'html.parser')
        regObj = re.compile('^(/[^/].+|' + domain_url + '.+)')
        for elem in soup.find_all(href=True):
            tag = 'href'
            link = elem[tag]
            # matching string
            result = regObj.match(link)
            # If link matches domain url pattern
            prefix = domain_url
            # If link matches '/' pattern
            forward_slash = '/'
            if (result is not None) and (prefix in result.group()):
                # add url to the list
                links.add(result.string)
            elif (result is not None) and (result.group()[0] == forward_slash):
                # construct full url
                full_url = domain_url[:-1] + result.string
                # add url to the list
                links.add(full_url)
    except requests.exceptions.InvalidURL:
        error_message = 'The URL provided was somehow invalid.'
    except requests.exceptions.URLRequired:
        error_message = 'A valid URL is required to make a request.'
    except requests.exceptions.HTTPError:
        error_message = 'An HTTP error occurred.'
    except requests.exceptions.Timeout:
        error_message = 'The request timed out'
    except requests.exceptions.ConnectionError:
        error_message = 'A Connection error occurred.'
    except requests.exceptions.RequestException as e:
        error_message = 'There was an ambiguous exception that' +\
            'occurred while handling your request : ' + str(e)
    return links, error_message


def clean_links(links_list):
    if not links_list:
        return []
    extension_pattern = re.compile("([^.]*)$")
    global good_extensions
    global bad_extensions
    global ALL_PAGES
    good_links = []
    for link in links_list:
        match = extension_pattern.search(link)
        if match:
            ext = match.group().lower()
            if ext not in bad_extensions and ';jsessionid=' not in link:
                good_links.append(link)
            # if ext in good_extensions:
            #     good_links += link
            # elif ext not in bad_extensions:
            #     is_good = input(ext + " good ? :")
            #     if is_good in 'yYoO':
            #         good_extensions += ext
            #         good_links += link
            #     else:
            #         bad_extensions += ext
    return good_links


def explore_domain(page_url):
    domain_to_visit = set()
    domain_visited = set()

    domain_url = domain_extractor(page_url)
    domain_to_visit.add(page_url)

    global ALL_PAGES
    global VISITED
    depth = 1
    while len(domain_to_visit) > 0:
        start_depth_time = time.time()
        for page in domain_to_visit.copy():
            if page not in VISITED:
                domain_to_visit.remove(page)
                VISITED.add(page)

                links, error_message = links_in_page(domain_url, page)
                if error_message:
                    print("Page", page, "yielded an error:", error_message)
                links = clean_links(links)
                domain_to_visit = domain_to_visit.union(links)
                ALL_PAGES = ALL_PAGES.union(links)
            else:
                domain_to_visit.remove(page)
        print("Ending depth", depth)
        print("Page {}, depth {}, found {} subpages in {}s".format(
            page_url, depth, len(domain_to_visit), time.time()-start_depth_time))
        depth += 1


def myEpflGalleryBox_documents(page_urls):
    prefix = '//documents.epfl.ch/'

    # Assumptilinkson : Documents we are looking for are all children of the class 'myEpflGalleryBox'
    class_ = 'myEpflGalleryBox'
    # final dataframe to store the result
    df_res = pd.DataFrame()
    # Get all documents inside myEpflGalleyBox from the domain_urls
    for page_url in page_urls:
        domain_url = domain_extractor(page_url)
        print('page url -->', page_url, ', domain url --> ', domain_url)
        explore_domain(page_url)

    for page_url in ALL_PAGES:
        error_message = None
        try:
            # Http response for the requested url
            resp = requests.get(page_url)
            # Initialize parser for the requested url
            soup = BeautifulSoup(resp.text, 'html.parser')

            # Initialize empty list of all documents inside a myEpflGalleryBox
            documents = []
            # Initialize empty list of all document sizes inside a myEpflGalleryBox
            sizes = []
            if resp.ok:
                # Get all galleries in the page
                galleries = soup.find_all(class_=class_)
                for box in galleries:
                    # external links
                    ext_links = box.find_all(href=True)
                    for elem in ext_links:
                        link = elem['href']
                        if prefix in link:
                            documents.append(link)
                            try:
                                # Http response for the requested document
                                resp = requests.get(page_url)
                                # helper
                                byte_to_kilobyte = 10**(-3)
                                # Get the size of the document
                                sizes.append(
                                    int(resp.headers['Content-Length']) * byte_to_kilobyte)
                            except requests.exceptions.RequestException as e:
                                sizes.append(float('NaN'))

                # Update DataFrame of result
                d = {'domain': [domain_url]*len(documents), 'page': [page_url]*len(
                    documents), 'document': documents, 'size [KB]': sizes}
                temp = pd.DataFrame(data=d)
                df_res = pd.concat([df_res, temp], axis=0)
            else:
                error_message = resp.status_code
        except requests.exceptions.InvalidURL as e:
            error_message = 'The URL provided was somehow invalid.'
        except requests.exceptions.URLRequired as e:
            error_message = 'A valid URL is required to make a request.'
        except requests.exceptions.HTTPError as e:
            error_message = 'An HTTP error occurred.'
        except requests.exceptions.Timeout as e:
            error_message = 'The request timed out'
        except requests.exceptions.ConnectionError as e:
            error_message = 'A Connection error occurred.'
        except requests.exceptions.RequestException as e:
            error_message = 'There was an ambiguous exception that occurred while handling your request: ' + \
                str(e)
    # Remove duplicates from dataframe of documents
    return df_res.set_index('domain').drop_duplicates(subset=['page', 'document'])[['page', 'document', 'size [KB]']]


def write_result(base_output_filename, result):
    basename_index = 0
    extension_index = 1
    # input filename
    base = os.path.splitext(base_output_filename)[basename_index]
    # input file extension
    extension = os.path.splitext(base_output_filename)[extension_index]
    # Date the result as been produced (Specific format)
    date = datetime.datetime.now().strftime('%y%m%d.%H%M')
    # part of the output filename
    out = 'out'
    dot = '.'
    # output filename
    final = base + dot + out + dot + date + extension
    # Write result to output file
    result.reset_index().to_csv(final, index=False)


def domain_extractor(url):
    splitted = url.split('/')
    return splitted[0] + '//' + splitted[2] + '/'


if __name__ == "__main__":
    input_filename = 'original_urls.csv'
    output_filename = "output_olivier.csv"
    df_urls = pd.read_csv(input_filename)
    df_urls = df_urls.rename(index=str, columns={'Sites': 'URL'})
    result = myEpflGalleryBox_documents(list(df_urls['URL']))
    write_result(output_filename, result)
