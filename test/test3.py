import requests
import time
import pandas as pd
from pandas import DataFrame
from bs4 import BeautifulSoup

# 이니스프리
# pageNo로 페이지 넘
def trade_spider(max_pages):
    check = 1
    url = 'http://www.innisfree.co.kr/Product.do'
    source_code = requests.get(url, allow_redirects=False)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,'html.parser')

    typelist = []
    namelist = []
    imglist = []
    urllist = []

    for large in soup.findAll('ul', {'class': 'lnbList'}):

        for link in large.findAll('a', {'class': 'color'}):
            if check > 1: #전체 제외
                category = 'http://www.innisfree.co.kr' + link.get('href')
                category_name = link.text
                print('카테고리 주소 : ' + category)
                print('카테고리 명 : ' + category_name)

                page = 1
                pagenum = 1

                while page <= pagenum:
                    time.sleep(1)
                    category_url = category + '&pageNo=' + str(page)
                    print('카테고리 페이지 주소 : ' + category_url)
                    sc = requests.get(category_url, allow_redirects=False)
                    soup2 = BeautifulSoup(sc.text,'html.parser')
                    pagenum = len(soup2.findAll('span',{'class':'num'})) + 1
                    page+=1

                    for product in soup2.find('div',{'class':'listBox1'}).findAll('p', {'class': 'img'}):
                        href = 'http://www.innisfree.co.kr' + product.find('a').get('href')
                        imgurl = product.find('img').get('src')
                        p_name = product.find('img').get('alt')
                        typelist.append(category_name)
                        namelist.append(p_name)
                        imglist.append(imgurl)
                        urllist.append(href)
            check += 1
    result = {'category':typelist,
              'product_name':namelist,
              'img':imglist,
              'url':urllist}
    df = pd.DataFrame(result)

    df.to_csv('/Users/mijeong/builds/innisfree.csv', sep=',', na_rep='NaN')

trade_spider(1)
