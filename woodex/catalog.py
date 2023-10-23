from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import re
import openpyxl


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/116.0.5845.888 Safari/537.36"
}

# url = 'https://catalogue.ite-expo.ru/ru-RU/exhibitorlist.aspx?project_id=511'
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, "lxml")
#
# links = soup.find_all('a', class_='link')
#
#
service = Service(
    executable_path="D:/PycharmProjects/freelance/woodex/chromedriver.exe"
)

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                     " Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36")

driver = webdriver.Chrome(service=service, options=options)
# driver.get(url=url)
#
# time.sleep(2)
# a = "//a[@class='link' and text()='{}']"
# links_list = []
# for i in range(2, 10):
#     html = driver.page_source
#     soup = BeautifulSoup(html, 'lxml')
#     link_popup = soup.find_all('a', class_='popUp')
#     for j in link_popup:
#         link = j['href']
#         j_link = "https://catalogue.ite-expo.ru" + link
#         with open('cat_links.txt', 'a', encoding='utf-8') as file:
#             file.write(j_link + '\n')
#
#     try:
#         link = a.format(i)
#         link_element = driver.find_element(By.XPATH, str(link))
#         link_element.click()
#         time.sleep(2)
#
#     except NoSuchElementException:
#         link_element = ''
#
# driver.close()
# driver.quit()

workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.append(["Наименование", "Номер телефона", "Email"])
with open('cat_links.txt', 'r') as file:
    for i in file:
        print(i)
        url = i.strip()
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        participant = soup.find('div', class_='scorecard').find('h2')

        phone_elements = soup.find_all('p', text=lambda text: text and re.search(r'\+\d', text) is not None)

        if phone_elements:
            for phone_element in phone_elements:
                phone_number = phone_element.get_text(strip=True)
        else:
            phone_number = "Номер телефона не найден."

        driver.get(url=url)
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        email_element = soup.find('a', {'href': re.compile(r'^mailto:')})
        if email_element:
            email = email_element.text

        else:
            email = "Нет Email."

        sheet.append([participant.text, phone_number, email])

        print(participant.text, '\n', phone_number, '\n', email)


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

workbook.save("data_cat.xlsx")