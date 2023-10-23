from bs4 import BeautifulSoup
import requests
from transliterate import translit
import re, time, selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import sqlite3, random
from selenium.common.exceptions import NoSuchElementException
import mysql.connector
from random import randint
from multiprocessing import Pool
from selenium.webdriver.chrome.options import Options


PROXY = "keQnat:PUG9VUw9SEP8@88.155.24.245:16894"

service = Service(
    executable_path="D:/PycharmProjects/freelance/uslugio/chromedriver.exe"
)

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                     " Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36")

driver = webdriver.Chrome(service=service, options=options)
url = ''
try:
    driver.get(url=url)
    titles = driver.find_elements(By.CLASS_NAME, 'title.showone')
    time.sleep(2)
    for i in range(5):
        if len(titles) > 1:
            title = titles[i]
            title.click()
            time.sleep(2)

            try:
                name = driver.find_element(By.CLASS_NAME, 'modal-title')
                t_name = name.text
            except NoSuchElementException:
                t_name = None

            try:
                description = driver.find_element(By.ID, 'html_showone')
                des_text = description.get_attribute('innerHTML').split('<br>')[0].strip().replace('\n', '')
            except NoSuchElementException:
                des_text = None

            try:
                div_price_element = driver.find_element(By.CLASS_NAME, "div-price")
                html_code = div_price_element.get_attribute('outerHTML')
                soup = BeautifulSoup(html_code, 'html.parser')
                for thead_row in soup.select('thead tr'):
                    thead_row.decompose()
                tex = soup.get_text(strip=True)
                price = tex.replace("₽", "₽, ")
            except NoSuchElementException:
                price = None

            try:
                cl = driver.find_element(By.CLASS_NAME, 'showphone1.btn.btn-success.btn-lg.btn-block.showphone')
                cl.click()
                time.sleep(2)
                phone_num = cl.text
                time.sleep(2)
                clo = driver.find_element(By.CLASS_NAME, 'btn.btn-secondary')
                clo.click()
                time.sleep(2)
            except NoSuchElementException:
                phone_num = None

except Exception as ex:
    print(ex)

driver.close()
driver.quit()


