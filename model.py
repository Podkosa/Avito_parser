from bs4 import BeautifulSoup
import requests
from sqlalchemy import Column, Integer, Float, String, Text, JSON
from database import Base

class AvitoItem(Base):
    __tablename__ = 'avito_items'
    
    id = Column(Integer, primary_key=True)
    avito_id = Column(Integer)
    name = Column(String)
    owner = Column(String)
    desciption = Column(Text)
    params = Column(JSON)
    price_rub = Column(Float)
    price_eur = Column(Float)


    def __init__(self, url: str): 
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.avito_id = int(soup.find('span', attrs={"data-marker": "item-view/item-id"}).text.strip('№ '))
        self.name = soup.find('span', 'title-info-title-text').text
        self.owner = soup.find('div', 'seller-info-name js-seller-info-name').text.strip()
        self.desciption = soup.find('div', 'item-description-text').text.strip()
        self.params = self._parse_params(soup)
        self.price_rub = float(soup.find('span', 'js-item-price').text.replace('\xa0', ''))
        self.price_eur = self._price_to_eur()
    
    def _parse_params(self, soup):
        _list_params = list(soup.find('ul', 'item-params-list').stripped_strings)
        params = {_list_params[i].replace(':', ''):_list_params[i+1].replace('\xa0', ' ') for i in range(0, len(_list_params), 2)}
        return params

    def _price_to_eur(self):
        url_cb = 'https://www.cbr.ru/scripts/XML_daily.asp'
        response_cb = requests.get(url_cb)
        soup_cb = BeautifulSoup(response_cb.text, 'xml')
        euro_value = float((soup_cb.find('Valute', ID="R01239").find('Value').text.replace(',', '.')))
        price_eur = round((self.price_rub / euro_value), 2)
        return price_eur
    
    def __repr__(self):
        return self.name