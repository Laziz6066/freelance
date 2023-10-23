from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import requests, json
import openpyxl

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/116.0.5845.888 Safari/537.36"
}

url = 'https://rus-elektronika.ru/ru-RU/about/exhibitor-list.aspx'


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
    time.sleep(2)
    html = driver.page_source

    soup = BeautifulSoup(html, "lxml")

    base_url = "https://rus-elektronika.ru/ru-RU/about/exhibitor-list/exhibitorview.aspx?id={}"
    elements = soup.find_all('div', class_='col-sm-3 mb-3 mb-sm-4')

    for element in elements:
        if element:
            data_item_value = element.a.get('data-item')
            print("data-item:", data_item_value)
            link = base_url.format(data_item_value)
            with open('elek_links.txt', 'a', encoding='utf-8') as file:
                file.write(link + '\n')

        else:
            print("Элемент с классом 'col-sm-3 mb-3 mb-sm-4' не найден.")
        time.sleep(2)

driver.close()
driver.quit()
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.append(["Наименование", "Номер телефона", "Email"])

with open('elek_links.txt', 'r') as file:
    for i in file:
        print(i.strip())

        response = requests.get(i.strip())

        soup = BeautifulSoup(response.text, "lxml")
        script_tag = soup.find("body")
        data = script_tag.text
        data_2 = json.loads(data)
        name = data_2[0]["Name"]

        if len(data_2[0]['PhoneOne']) > 5: phone_1 = data_2[0]['PhoneOne']
        else: phone_1 = 'Номер не указан'
        if len(data_2[0]['PhoneTwo']) > 5: phone_2 = data_2[0]['PhoneTwo']
        else: phone_2 = 'Второй номер не указан'
        if len(data_2[0]['Email']) > 2: email_1 = data_2[0]['Email']
        else: email_1 = 'Email не указан'

        print(name)
        print(phone_1)
        print(phone_2)
        print(email_1)

        phone_numbers = f"{phone_1}; {phone_2}" if phone_1 != 'Номер не указан' and phone_2 != 'Второй номер не указан' else phone_1
        sheet.append([name, phone_numbers, email_1])


for column in sheet.columns:
    max_length = 0
    column = [cell for cell in column]
    for cell in column:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(cell.value)
        except:
            pass
    adjusted_width = (max_length + 2)
    sheet.column_dimensions[column[0].column_letter].width = adjusted_width

workbook.save("data_elek.xlsx")