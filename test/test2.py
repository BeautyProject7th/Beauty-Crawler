import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver

def trade_spider(max_pages):
    page = 1
    url = 'http://www.innisfree.co.kr/Product.do'
    source_code = requests.get(url, allow_redirects=False)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,'html.parser')
    for large in soup.findAll('ul', {'class': 'lnbList'}):
        for link in large.findAll('a', {'class': 'color'}):
            if page > 1: #전체 제외
                category = 'http://www.innisfree.co.kr' + link.get('href')
                print('카테고리 주소 : ' + category)
                print('카테고리 명 : ' + link.text)
                print('-----')
                time.sleep(1)
                sc = requests.get(category, allow_redirects=False)
                soup2 = BeautifulSoup(sc.text,'html.parser')
                for product in soup2.findAll('p', {'class': 'pdtName'}):
                    href = 'http://www.innisfree.co.kr' + product.find('a').get('href')
                    print('제품 명 : '+product.text)
                    print('제품 url : '+href)
                #driver.execute_script("nextPage(1);")
            page += 1

trade_spider(1)
