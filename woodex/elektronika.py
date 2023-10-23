from bs4 import BeautifulSoup
import requests
import re, time, selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from multiprocessing import Pool
import mysql.connector
from mysql.connector import pooling
import re
import openpyxl
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/116.0.5845.888 Safari/537.36"
}

url = 'https://rus-elektronika.ru/ru-RU/about/exhibitor-list.aspx'



# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, "lxml")
#
# base_url = "https://rus-elektronika.ru/ru-RU/about/exhibitor-list/exhibitorview.aspx?id={}"
# elements = soup.find_all('div', class_='col-sm-3 mb-3 mb-sm-4')
#
# for element in elements:
#     if element:
#         data_item_value = element.a.get('data-item')
#         print("data-item:", data_item_value)
#         link = base_url.format(data_item_value)
#         with open('elek_links.txt', 'a', encoding='utf-8') as file:
#             file.write(link + '\n')
#
#     else:
#         print("Элемент с классом 'col-sm-3 mb-3 mb-sm-4' не найден.")


service = Service(
    executable_path="D:/PycharmProjects/freelance/woodex/chromedriver.exe"
)

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                     " Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36")

driver = webdriver.Chrome(service=service, options=options)

driver.get(url=url)

pages = driver.find_elements(By.CLASS_NAME, 'page-link')
for i in range(len(pages)):
    pages[i].click()
    time.sleep(2)
    pages = driver.find_elements(By.CLASS_NAME, 'page-link')


driver.close()
driver.quit()
