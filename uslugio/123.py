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


all_urls = []

with open('cat_links_1.txt', 'r') as file:
    for line in file:
        cleaned_line = line.strip()
        all_urls.append(cleaned_line)


def get_data(url):
    profile_id = '175493556'
    req_url = f'http://localhost:3001/v1.0/browser_profiles/' + profile_id + '/start?automation=1'
    response = requests.get(req_url)
    print(response)
    response_json = response.json()
    print(response_json)
    port = str(response_json['automation']['port'])
    chrome_driver_path = Service('D:/PycharmProjects/freelance/uslugio/chromedriver-windows-x64.exe')
    options = webdriver.ChromeOptions()
    options.debugger_address = '127.0.0.1:' + port
    driver = webdriver.Chrome(service=chrome_driver_path, options=options)

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

                try:
                    connection = mysql.connector.connect(**db_config)
                    cursor = connection.cursor()
                    sql_insert_query = ("INSERT INTO data (name, description, price, phone_num) "
                                        "VALUES (%s, %s, %s, %s)")
                    values = (t_name, des_text, price, phone_num)
                    cursor.execute(sql_insert_query, values)
                    connection.commit()
                    print("Данные успешно добавлены в базу данных!")

                except mysql.connector.Error as error:
                    print("Ошибка при работе с базой данных: {}".format(error))

                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()
                        print("Соединение с базой данных закрыто.")

    except Exception as ex:
        print(ex)

    driver.close()
    driver.quit()


if __name__ == '__main__':
    p = Pool(1)
    p.map(get_data, all_urls)