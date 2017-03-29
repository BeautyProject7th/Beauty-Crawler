import requests
import time
from bs4 import BeautifulSoup

def trade_spider():
    page = 1
    url = 'http://www.theskinfood.com/shopMain/shopMain.do'
    source_code = requests.get(url, allow_redirects=False)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,'html.parser')

    typelist = []
    namelist = []
    imglist = []
    urllist = []
    pricelist = []

    for large in soup.findAll('div', {'class': 'depth-wrap pd-left10 no-bd-left'}):
        for category in large.findAll('a'):
            category_url = 'http://www.theskinfood.com' + category.get('href')
            category_name = category.text
            print('카테고리 명 : ' + category_name)
            time.sleep(1)
            sc = requests.get(category_url, allow_redirects=False)
            soup2 = BeautifulSoup(sc.text, 'html.parser')
            productlist = soup2.find('div',{'class':'productList more-wrap'})
            print(productlist)
            for product in productlist.findAll('li'):
                print(product)
                name = product.find('span',{'class':'name'})
                print('제품 명 : '+name)

trade_spider()
