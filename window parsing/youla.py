from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from seleniumwire import webdriver
from time import sleep


service = Service(
    executable_path="D:/PycharmProjects/freelance/window parsing/chromedriver.exe"
)

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                     " Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36")
# options.headless = True
driver = webdriver.Chrome(service=service, options=options)

with open("links.txt", 'r') as file:
    for line in file:
        print(line.strip() + '?q=%D0%BE%D0%BA%D0%BD%D0%B0%20%D0%B1%2F%D1%83')
        url = line.strip() + '?q=%D0%BE%D0%BA%D0%BD%D0%B0%20%D0%B1%2F%D1%83'
        driver.get(url=url)
        page_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            sleep(3)
            new_page_height = driver.execute_script("return document.body.scrollHeight")
            if new_page_height == page_height:
                break
            page_height = new_page_height


