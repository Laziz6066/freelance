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


# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                   "Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36"
# }


# url = "https://uslugio.com/moskva"
# req = requests.get(url=url, headers=headers)
# soup = BeautifulSoup(req.text, 'lxml')
# all_services = soup.find_all('div', class_='col-sm-4')
#
# with open('links.txt', 'w') as file:
#     for div in all_services:
#         links = div.find_all('a', href=True)
#         for link in links:
#             file.write("https://uslugio.com/" + link['href'] + '\n')

# with (open('links.txt', 'r') as file):
#     for i in file:
#
#         req = requests.get(url=i, headers=headers)
#         soup = BeautifulSoup(req.text, 'lxml')
#         category = soup.find('div', class_="main-top").find('h1').text
#         cat_name = translit(category, 'ru', reversed=True
#                             ).replace(' ', '_').replace(',', '_').replace("'", '_')
#
#         cat_list = soup.find_all('div', class_="col-sm-4")
#
#         with open('cat_links.txt', 'a') as file:
#             for div in cat_list:
#                 links = div.find_all('a', href=True)
#                 for link in links:
#                     file.write("https://uslugio.com/" + link['href'] + '\n')


# def check_last_two_digits(url):
#     pattern = r'/(\d{1,2})$'
#     match = re.search(pattern, url)
#     if match:
#         return True
#     else:
#         return False
#
#
# with open('cat_links.txt', 'r') as file:
#     for i in file:
#         result = check_last_two_digits(i)
#         if result:
#             req = requests.get(url=i, headers=headers)
#             soup = BeautifulSoup(req.text, 'lxml')
#             category = soup.find('div', class_="main-top").find('h1').text
#             cat_name = translit(category, 'ru', reversed=True
#                                 ).replace(' ', '_').replace(',', '_').replace("'", '_')
#
#             cat_list = soup.find_all('div', class_="col-sm-4")
#             with open('cat_links_1.txt', 'a') as file:
#                 for div in cat_list:
#                     links = div.find_all('a', href=True)
#                     for link in links:
#                         file.write("https://uslugio.com/" + link['href'] + '\n')
#         else:
#             with open('cat_links_1.txt', 'a') as file:
#                 for div in cat_list:
#                     links = div.find_all('a', href=True)
#                     for link in links:
#                         file.write("https://uslugio.com/" + link['href'] + '\n')

# *********************************************************************************************************************

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "52949235",
    "database": "uslugio"
}
all_urls = []

with open('cat_links_1.txt', 'r') as file:
    for line in file:
        cleaned_line = line.strip()
        all_urls.append(cleaned_line)


def get_data(url):
    PROXY = "keQnat:PUG9VUw9SEP8@dq.mobileproxy.space:62027"
    service = Service(
        executable_path="D:/PycharmProjects/freelance/uslugio/chromedriver.exe"
    )

    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                         " Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36")
    options.add_argument(f'--proxy-server={PROXY}')
    driver = webdriver.Chrome(service=service, options=options)

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


if __name__ == '__main__':
    p = Pool(1)
    p.map(get_data, all_urls)

