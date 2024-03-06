import requests
from bs4 import BeautifulSoup
import pandas as pd


class Scrappy:
    def __init__(self, base_path:str):
        self.base_path = base_path
        
    def __get_all_links(self, soup: BeautifulSoup):
        links = soup.find_all("link")
        links_a = soup.find_all("a")
        links = links + links_a
        ref = []
        for link in links:
            ref.append(link.get('href'))
        return ref
    
    def __get_only_html(self, links: list):
        only_html = list(filter(lambda text: text.endswith('.html'), links))
        only_html.pop(0)
        return only_html

    def get_soups_from_base_path(self):
        request = requests.get(self.base_path)
        soup = BeautifulSoup(request.text, 'html.parser')
        links = self.__get_all_links(soup)
        htmls = self.__get_only_html(links)

        reqs = []
        soups = []
        for link in htmls:
            full_path = self.base_url + link
            req = requests.get(full_path)
            reqs.append(req)
            soups.append(BeautifulSoup(req.text, 'html.parser'))
                
        return soups 

    def get_content_as_plain_text(self, soup: BeautifulSoup):
        paragraphs = soup.find_all('p')
        content = '\n'.join([p.get_text() for p in paragraphs])
        return soup.title.string, soup.title.string + content

    def get_content_as_dataframe(self, soups):
        contents = [self.get_content_as_plain_text(s) for s in soups]    
        id_cloud_docs = {}
        titles = [c[0] for c in contents]
        content = [c[1] for c in contents]
        id_cloud_docs['title'] = titles
        id_cloud_docs['content'] = content
        return pd.DataFrame(id_cloud_docs)