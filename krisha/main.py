from bs4 import BeautifulSoup
import requests


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36"
}

url = "https://krisha.kz/prodazha/kvartiry/?page=1"


response = requests.get(url=url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")
sellers = soup.find_all('div', class_="a-card a-storage-live ddl_product ddl_product_link not-colored is-visible")
for i in sellers:
    print(i)
