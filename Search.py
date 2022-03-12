from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains

#
#    Get Response.
#
def getRes(url, headers):
    res = requests.get(url, headers = headers)
    time.sleep(1)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
        
    return res


keyword = "귀여운동전지갑"

for val in range(0, 50):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.w3c = True
    driver = webdriver.Chrome(options=options)

    # search url
    url = 'https://naver.com'

    driver.get(url) # Open Url.
    driver.maximize_window() # maximize window.
    action= ActionChains(driver)

    driver.get(f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={keyword}")

    time.sleep(1)

    # Click using xpath.
    tmp = driver.find_element_by_xpath('//*[@id="main_pack"]/section[1]/div[1]/div[3]/div[1]/div[1]/ul/li[3]/div/div/a').click()

    # Close chrome.
    driver.close()

    time.sleep(5)