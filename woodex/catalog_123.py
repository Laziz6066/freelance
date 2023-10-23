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
#
#
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/116.0.5845.888 Safari/537.36"
}
#
#
# with open('cat_links.txt', 'r') as file:
#     for index, i in enumerate(file):
#
#         if index >= 5:
#             break
#         response = requests.get(url=i.strip(), headers=headers)
#         soup = BeautifulSoup(response.text, "lxml")
#         participant = soup.find('div', class_='scorecard').find('h2')
#
#         phone_elements = soup.find_all('p', text=lambda text: text and re.search(r'\+\d', text) is not None)
#
#         if phone_elements:
#             for phone_element in phone_elements:
#                 phone_number = phone_element.get_text(strip=True)
#         else:
#             phone_number = "Номер телефона не найден."
#
#         email_element = soup.find('a', {'href': re.compile(r'^mailto:')})
#         if email_element:
#             email = email_element.get('href').split(':')[1]
#
#         else:
#             email = "Нет Email."
#
#         print(participant.text)
#         print(email)


service = Service(
    executable_path="D:/PycharmProjects/freelance/woodex/chromedriver.exe"
)

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                     " Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36")

driver = webdriver.Chrome(service=service, options=options)

url = "https://catalogue.ite-expo.ru/ru-RU/specialpages/exhibitor_view.aspx?project_id=511&exhibitor_id=81260&itemid=122955"
driver.get(url=url)
time.sleep(1)
html = driver.page_source


soup = BeautifulSoup(html, "lxml")
email_element = soup.find('a', {'href': re.compile(r'^mailto:')})
print(email_element.text)
if email_element:
    email = email_element.get('href').split(':')[1]

else:
    email = "Нет Email."

