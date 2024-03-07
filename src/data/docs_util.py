import requests
from bs4 import BeautifulSoup
import pandas as pd


class Scrappy:
    def __init__(self, base_path:str, main_page:str):
        self.base_path = base_path
        self.main_page = main_page
        print(f'--Doing request to {base_path}--')
        self.request = requests.get(self.main_page)
        self.soup = BeautifulSoup(self.request.text, 'html.parser')
        print(f'--Request status {self.request}--')
        
    def __get_all_links(self, soup: BeautifulSoup):
        list_items = soup.find_all('li', class_='nav-item')
        ref = []
        for item in list_items:
            anchor = item.find('a', class_='nav-link')
            if anchor:
                ref.append(anchor['href'])
        return ref
    
    def __get_only_html(self, links: list):
        only_html = list(filter(lambda text: text.endswith('.html'), links))
        only_html.pop(0)
        return only_html

    def get_soups_from_base_path(self):
        links = self.__get_all_links(self.soup)
        htmls = self.__get_only_html(links)

        reqs = []
        soups = []
        for link in htmls:
            full_path = self.base_path + link
            req = requests.get(full_path)
            reqs.append(req)
            soups.append(BeautifulSoup(req.text, 'html.parser'))
            print(f'--Doing request to {full_path}-- \n --Request status {self.request}--')

                
        return soups 

    def __get_content_as_plain_text(self, soup: BeautifulSoup):
        paragraphs = soup.find_all('p')
        content = '\n'.join([p.get_text() for p in paragraphs])
        return soup.title.string, soup.title.string + ' ' + content

    def get_content_as_dataframe(self, soups) -> pd.DataFrame:
        contents = [self.__get_content_as_plain_text(s) for s in soups]    
        data = {}
        titles = [c[0] for c in contents]
        content = [c[1] for c in contents]
        data['title'] = titles
        data['content'] = content
        return pd.DataFrame(data)