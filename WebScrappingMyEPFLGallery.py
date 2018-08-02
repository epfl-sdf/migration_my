import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import datetime
import re

def script(filename, from_, to):
    df_urls = pd.read_csv(input_)
    df_urls = df_urls.iloc[from_:to]
    df_urls = df_urls.rename(index=str, columns={'Sites': 'URL'})
    result = myEpflGalleryBox_documents(list(df_urls['URL']))
    write_result(filename, result)

def links_in_page(domain_url, page_url):
    # valid url links in the page
    links = []
    # initial empty error message
    error_message = None
    
    # We want the url to have the format http://www.example.com/
    # and not http://www.example.com => to end with a forward slash
    forward_slash = '/'
    if(domain_url[-1:] != forward_slash):
        domain_url += forward_slash
    try:
        # Http response for the requested url
        resp = requests.get(page_url)
        # Initialize parser for the requested url
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        if(resp.ok):
            # Pattern to match strings starting
            # with a single forward slash '/...', a hastag '#...', 'http://' or 'https://'
            pattern = '^(/[^/].|#|'+ domain_url + '.+)'
            # pattern = '^(/[^/].|'+ domain_url+ '.+)'
            # associated regex object
            regObj = re.compile(pattern)
            # Find valid url links in the page_url
            for elem in soup.find_all(href=True):
                tag = 'href'
                link = elem[tag]
                # matching string
                result = regObj.match(link)
                # If link matches '#' pattern
                hashtag = '#'
                # If link matches domain url pattern
                prefix = domain_url
                # If link matches '/' pattern
                forward_slash = '/'
                if (result is not None) and (result.group() == hashtag):
                    # construct full url
                    full_url = domain_url + result.string
                    # add url to the list
                    links.append(full_url)
                elif (result is not None) and (prefix in result.group()):
                    # add url to the list
                    links.append(result.string)
                elif (result is not None) and (result.group()[0] == forward_slash):
                    # conctruct full url
                    full_url = domain_url[:-1] + result.string
                    # add url to the list
                    links.append(full_url)
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
        error_message = 'There was an ambiguous exception that occurred while handling your request.'
    return set(links), error_message

# function that recursively explores a domain and find all pages in the domain
def explore_domain(domain_url, page_url, visited, depth, max_depth=10):
    # Construct list of full path urls within the page
    links, error_message = links_in_page(domain_url, page_url)
    
    # update list of visited url
    if(domain_url == page_url and depth == 0):
        visited.append(domain_url)
    for url in links:
        # Check whether the url has never been visited
        if not any(url == v for v in visited):
            # If true add the new url reference to the list of visited pages
            visited.append(url)
    
    index = visited.index(page_url)
    # Stopping condition
    if(depth == max_depth):
        return visited
    # Stopping condition (No more new url page to explore)
    elif(index == len(visited)-1):
        return visited
    else:
        return explore_domain(domain_url, visited[index + 1], visited, depth + 1)

def myEpflGalleryBox_documents(domain_urls):
    prefix_1 = 'https://documents.epfl.ch/'
    prefix_2 = 'http://documents.epfl.ch/'
    
    # Assumption : Documents we are looking for are all children of the class 'myEpflGalleryBox'
    class_ = 'myEpflGalleryBox'
    # final dataframe to store the result
    df_res = pd.DataFrame()
    # Get all documents inside myEpflGalleyBox from the domain_urls
    for domain_url in domain_urls:
        print('domain url --> ', domain_url)
        page_url = domain_url
        visited = []
        depth = 0
        for page_url in explore_domain(domain_url, page_url, visited, depth):
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
                if(resp.ok):
                    # Get all galleries in the page
                    galleries = soup.find_all(class_=class_)
                    for box in galleries:
                        # external links
                        ext_links = box.find_all(href=True)
                        for elem in ext_links:
                            link = elem['href']
                            if prefix_1 in link or prefix_2 in link:
                                documents.append(link)
                                try:
                                    # Http response for the requested document
                                    resp = requests.get(page_url)
                                    # helper
                                    byte_to_kilobyte = 10**(-3)
                                    # Get the size of the document
                                    sizes.append(int(resp.headers['Content-Length']) * byte_to_kilobyte)
                                except requests.exceptions.RequestException as e:
                                    sizes.append(float('NaN'))
                        

                    # Update DataFrame of result
                    d = {'domain': [domain_url]*len(documents), 'page': [page_url]*len(documents), 'document': documents, 'size [KB]': sizes}
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
                error_message = 'There was an ambiguous exception that occurred while handling your request.'
    # Remove duplicates from dataframe of documents
    return df_res.set_index('domain').drop_duplicates(subset=['page', 'document'])[['page', 'document', 'size [KB]']]         


def write_result(input_filename, result):
    basename_index = 0
    extension_index = 1
    # input filename
    base = os.path.splitext(input_filename)[basename_index]
    # input file extension
    extension = os.path.splitext(input_filename)[extension_index]
    # Date the result as been produced (Specific format)
    date = datetime.datetime.now().strftime('%y%m%d.%H%M')
    # part of the output filename
    out = 'out'
    dot = '.'
    # output filename
    output_filename = base + dot + out + dot + date + extension
    # Write result to output file
    result.reset_index().to_csv(output_filename, index=False)



if(__name__ == '__main__'):
    input_filename = 'urls_myEpflGallery.csv'
    from_ = 0
    to = 10
    script(input_filename, from_, to)
