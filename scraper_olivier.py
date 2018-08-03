import datetime
import os
import re
import time
from bs4 import BeautifulSoup

import pandas as pd
import requests

bad_extensions = ['css', 'js', 'ico', 'png', 'jpg', 'pdf']
prefix = '//documents.epfl.ch/'


def links_in_page(domain_url, page_url):
    links = set()
    error_message = None
    df_temp = pd.DataFrame()
    if page_url[-1:] != '/':
        page_url += '/'
    if domain_url[-1:] != '/':
        domain_url += '/'
    response = None
    try:
        response = requests.get(page_url)
        if not response.ok:
            print("Error with page", page_url,"status",response.status_code)
            return None, None, None, response.status_code
        soup = BeautifulSoup(response.text, 'html.parser')
        df_temp = parse_gallery(soup, domain_url, page_url)
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
            if not result:
                continue
            if prefix in result.group():
                # add url to the list
                links.add(result.string)
            elif result.group()[0] == forward_slash:
                # construct full url
                if domain_url[-1] == '/':
                    full_url = domain_url[:-1] + result.string
                else:
                    full_url = domain_url + result.string
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
    return links, error_message, df_temp, response.status_code


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
    return good_links


def explore_domain(domain):
    to_visit_in_domain = set()
    visited_in_domain = set()

    to_visit_in_domain.add(domain)
    df_domain = pd.DataFrame()
    depth = 1
    while to_visit_in_domain:
        start_depth_time = time.time()
        for page in to_visit_in_domain.copy():
            to_visit_in_domain.remove(page)
            if page not in visited_in_domain:
                visited_in_domain.add(page)
                links, error_message, df_temp, stat_code = links_in_page(domain, page)
                if not stat_code:
                    continue
                if not links and not df_temp and stat_code != 200:
                    d = {
                        'domain': [domain],
                        'page': [page],
                        'status_code': [stat_code]
                    }
                    df_temp = pd.DataFrame(data=d)
                df_domain = pd.concat([df_domain, df_temp], axis=0)
                if error_message:
                    print("Page", page, "yielded an error:", error_message)
                links = clean_links(links)
                to_visit_in_domain = to_visit_in_domain.union(links)
        print("Domain {}, depth {}, found {} subpages in {}s".format(
            domain, depth, len(to_visit_in_domain), time.time()-start_depth_time))
        depth += 1
    return df_domain


def parse_gallery(soup, domain, subpage):
    # Assumption : Documents we are looking for are all children of the class 'myEpflGalleryBox'
    class_ = 'myEpflGalleryBox'

    # Initialize empty list of all documents inside a myEpflGalleryBox
    documents = []

    # Initialize empty list of all document sizes inside a myEpflGalleryBox
    sizes = []
    byte_to_kilobyte = 10**(-3)
    # Get all galleries in the page
    galleries = soup.find_all(class_=class_)
    for box in galleries:
        # external links
        ext_links = box.find_all(href=True)
        for elem in ext_links:
            link = elem['href']
            if prefix not in link:
                continue
            documents.append(link)
            try:
                # Http response for the requested document
                resp = requests.get(link)
                # helper
                # Get the size of the document
                sizes.append(
                    int(resp.headers['Content-Length']) * byte_to_kilobyte)
            except requests.exceptions.RequestException as e:
                sizes.append(float('NaN'))

    # Update DataFrame of result
    d = {
        'domain': [domain]*len(documents),
        'page': [subpage]*len(documents),
        'document': documents,
        'size [KB]': sizes,
        'status_code': float('NaN')
    }
    return pd.DataFrame(data=d)


def myEpflGalleryBox_documents(page_urls):

    # final dataframe to store the result
    df_res = pd.DataFrame()
    # Get all documents inside myEpflGalleyBox from the domain_urls
    for domain in page_urls:
        print('domain url --> ', domain,"at",datetime.datetime.now())
        df_temp = recover(domain)
        if df_temp.empty:
            df_temp = explore_domain(domain)
            save_temp(domain, df_temp)
        else:
            print("Recovered", domain, "from a previous run")
        df_res = pd.concat([df_res, df_temp], axis=0)
        # Remove duplicates from dataframe of documents
    return df_res.set_index('domain').drop_duplicates(subset=['page', 'document'])[['page', 'document', 'size [KB]', 'status_code']]


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


def save_temp(domain, dataframe):
    base_filename = "tmp_res/temporary"
    domain_name = name_extractor(domain)
    filename = base_filename + "_" + domain_name + ".csv"
    result = dataframe.set_index('domain').drop_duplicates(
        subset=['page', 'document'])[['page', 'document', 'size [KB]', 'status_code']]
    result.reset_index().to_csv(filename, index=False)


def recover(domain):
    base_filename = "tmp_res/temporary"
    domain_name = name_extractor(domain)
    filename = base_filename + "_" + domain_name + ".csv"
    try:
        df_recovered = pd.read_csv(filename)
        return df_recovered
    except FileNotFoundError:
        return pd.DataFrame()


def name_extractor(url):
    return re.sub(r"http.?://([^/.]*)\.epfl\.ch$", r"\1", url)


if __name__ == "__main__":
    print("Starting at",datetime.datetime.now())
    input_filename = 'urls_myEpflGallery.csv'
    output_filename = "output_olivier.csv"
    df_urls = pd.read_csv(input_filename)
    df_urls = df_urls.rename(index=str, columns={'Sites': 'URL'})
    result = myEpflGalleryBox_documents(list(df_urls['URL']))
    write_result(output_filename, result)
    print("Ending at",datetime.date.now())
