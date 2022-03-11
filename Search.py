from bs4 import BeautifulSoup
from selenium import webdriver
import time

query_txt = input('귀여운동전지갑')

# step1. Exeute web browser using chrome driver.
path = 'py_temp/chromdriver_win32/chromedriver.exe'
driver = webdriver.chrome(path)

# step2. Find search bar and input keyword.
driver.get('https://m.naver.com')
time.sleep(2) # wait 2 second until opening chrome.

element = driver.find_element_by_id('query)

element.send_keys(query_txt)

# step3. Click search button.
driver.find_element_by_id("search_btn").click()

