from selenium import webdriver
from bs4 import BeautifulSoup
import time


if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get("http://www.theskinfood.com/goods/goodsList.do?catCd=4000000000&flag=4000000001&gubun=B")
    elem = driver.find_element_by_id("moreA")

    allnum = int(driver.find_element_by_id("resultCount").text)
    num = 0
    while allnum > num:
        elem.click()
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        #allnum = soup.find('span', {'id': 'resultCount'})
        num = len(soup.findAll('li', {'class': 'best'}))
    #elem.click()

    """언니는 아래처럼 하면 되던대 나는 무슨 이유인지 되지 않아서 직접 더보기 클릭하는 것으로 진행함
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    driver.execute_script("selectGoodsList('','',10);")
    """
