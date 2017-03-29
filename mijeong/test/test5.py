import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver

#driver = webdriver.PhantomJS(executable_path='/Users/mijeong/builds/phantomjs')
driver = webdriver.Firefox()
driver.get('http://www.theskinfood.com/goods/goodsList.do?catCd=4000000000&flag=4000000001&gubun=B')
driver.execute_script("selectGoodsList('','',10);")
html = driver.page_source
soup = BeautifulSoup(html,"html.parser")


#driver.execute_script("selectCategory(\'\',\'\',10);")
#driver.find_elements_by_id('moreA')[0].click()
#driver.find_elements_by_id('moreA')[0].style.display='none'
time.sleep(3)
#prodList = soup.findAll('li',{'class':'best'})
#print(len(prodList))

