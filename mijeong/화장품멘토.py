from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

brandlist = []
namelist = []
pricelist = []
imglist = []
bdnolist = []

if __name__ == "__main__":
    driver = webdriver.Firefox()
    webpage = "http://www.allofcosmetics.com/main/product_list"
    driver.get(webpage)
    mainpage = BeautifulSoup(driver.page_source, "html.parser")
    loginbtns = mainpage.findAll('p',{'class':'pop_btn'})
    loginurl = loginbtns[0].find('a').get('href')
    driver.get(loginurl)
    #login 화면
    login = driver.find_element_by_id("id")
    login.send_keys("lmjing")
    login = driver.find_element_by_id("pw")
    login.send_keys("dltjtel4905")
    login.submit()
    time.sleep(3)
    #검색화면으로 이동
    searchpage = "http://www.allofcosmetics.com/main/product_list"
    driver.get(searchpage)
    time.sleep(1)
    #브랜드 명 검색하기
    search = driver.find_element_by_class_name("input_search")
    search.send_keys("미샤")
    search = driver.find_element_by_class_name("btn_blue_normal2")
    search.click()
    time.sleep(1)
    #검색된 화장품 개수
    #일단 분류안하고 사진,브랜드 명,제품 명만 긁어 올 예정
    searchpage = driver.page_source
    soup = BeautifulSoup(searchpage, "html.parser")
    for product in soup.findAll('div',{'class':'list_txt'}):
        brandlist.append(product.find('p',{'class':'list_h1'}).text)
        namelist.append(product.find('a').text)
        pricelist.append(product.find('p',{'class':'price'}).text)

    for img in soup.findAll('div',{'class':'list_thumb'}):
        imglist.append(img.find('a').get('href'))

    for bdno in soup.findAll('div',{'class':'list_bdno'}):
        bdnolist.append(bdno.text)
    # 다음 페이지로 이동
    time.sleep(1)
    pagebtn = driver.find_element_by_class_name("page_btn")
    pagebtn.click()

    result = {'brand': brandlist,
              'product_name': namelist,
              'price': pricelist,
              'img': imglist,
              'bdno': bdnolist}
    df = pd.DataFrame(result)
    print(df)
