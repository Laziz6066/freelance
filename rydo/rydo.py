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


# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
#                   "(KHTML, like Gecko) Chrome/116.0.5845.888 Safari/537.36"
# }
#
# url = 'https://rydo.ru/moskva/uslugi/'
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, "lxml")
# links = soup.find('div', class_='nss-main-locations').find_all('a')
#
# links_list = ['https://rydo.ru' + link['href'] for link in links]
#
# for i in links_list:
#     response = requests.get(url=i, headers=headers)
#     soup = BeautifulSoup(response.text, "lxml")
#
#     if soup.find('div', class_='nss-main-locations'):
#         links_s = soup.find('div', class_='nss-main-locations').find_all('a')
#
#         for link in links_s:
#             print("https://rydo.ru" + link['href'])
#             s = "https://rydo.ru" + link['href']
#             with open('rydo_links_s.txt', 'a', encoding='utf-8') as file:
#                 file.write(s + '\n')
#     else:
#         print(f'Класс "nss-main-locations" не найден на странице: {i}')
#         with open('rydo_links_s.txt', 'a', encoding='utf-8') as file:
#             file.write(i + '\n')


links = []
with open('rydo_links_s.txt', 'r', encoding='utf-8') as file:
    for i in file:
        links.append(i.strip())

#
# for link in links:
#     print('*' * 20, link, '*' * 20)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "52949235",
    "database": "rydo"
}



def get_data(link):
    service = Service(
        executable_path="D:/PycharmProjects/freelance/rydo/chromedriver.exe"
    )

    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                         " Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.headless = True
    driver = webdriver.Chrome(service=service, options=options)
    print('*' * 20, link, '*' * 20)
    try:
        driver.get(url=link)
        elements = driver.find_elements(By.CLASS_NAME, 'nss-item-title')
        elements_links = [element.find_element(By.TAG_NAME, 'a').get_attribute('href') for element in elements]
        time.sleep(2)
        for i in elements_links[:5]:
            driver.get(url=i)
            time.sleep(2)
            try:
                title = driver.find_element(By.CSS_SELECTOR, '.nss-conteiner h1')
                ser_title = title.text
            except NoSuchElementException:
                ser_title = 'Без названия'
            try:
                price = driver.find_element(By.CLASS_NAME, 'nss-detail-price')
                ser_price = price.text
            except NoSuchElementException:
                ser_price = 'Цена не указана'
            try:
                phone = driver.find_element(By.ID, 'get_phone_contact')
                phone.click()
                time.sleep(2)
                num = driver.find_element(By.CLASS_NAME, 'nss-detail-phone-bx')
                time.sleep(2)
                ser_num = num.text
            except NoSuchElementException:
                ser_num = 'Нет номера'

            try:
                description = driver.find_element(By.CLASS_NAME, 'nss-detail-info')
                ser_description = description.text
            except NoSuchElementException:
                ser_description = 'Нет описания'

            try:
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()
                sql_insert_query = ("INSERT INTO rydoru (title, url, price, phone_number, description) "
                                    "VALUES (%s, %s, %s, %s, %s)")
                values = (ser_title, i, ser_price, ser_num, ser_description)
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

            print(ser_title)
            print(ser_price)
            print(ser_num)
            print(ser_description)

    except Exception as ex:
        print(ex)


    driver.close()
    driver.quit()


if __name__ == '__main__':
    p = Pool(3)
    p.map(get_data, links)