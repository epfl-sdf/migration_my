import requests
from bs4 import BeautifulSoup
import lxml.html as lh
import pandas as pd


def get_documents(path_urls):
    df_urls = pd.read_csv(path_urls)
    df_urls = df_urls['URL']

    # prefixes for all document links we are looking for
    prefix_1 = 'https://documents.epfl.ch/'
    prefix_2 = 'http://documents.epfl.ch/'
    # Dataframe with all documents associated
    # the url we found inside.
    df_documents = pd.DataFrame()
    # Pages with a ConnectionErrors
    error_pages = []
    for url in df_urls:
        try:
            # Http response for the requested url
            resp = requests.get(url)
            # Initialize parser for the requested url
            soup = BeautifulSoup(resp.text, 'html.parser')

            # Initialize empty list of all document links
            # we find in the html page
            documents = []
            # Get all tags in the html
            all_tags = set([tag.name for tag in soup.find_all()])
            # Search for the documents
            for tag in all_tags:
                for elem in soup.find_all(tag, href=True):
                    link = elem['href']
                    if prefix_1 in link or prefix_2 in link:
                        documents.append(link)

            # Dictionnary to construct dataFrame
            d = {'URL': [url]*len(documents), 'Documents': documents}
            temp = pd.DataFrame(data=d)
            df_documents = pd.concat([df_documents, temp], axis=0)
        except requests.exceptions.RequestException as e:
            error_pages.append(url)

if __name__ == '__main__':
    path_urls = 'urls_document.csv'
    get_documents(path_urls)
