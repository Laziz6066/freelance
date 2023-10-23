from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/116.0.5845.888 Safari/537.36"
}

url = "https://youla.ru/cities"
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")
cities = soup.find_all('div', class_="cities_list")

links = []
for c in cities:
    city_items = c.find_all('li', class_='cities_list__item')
    for item in city_items:
        # Check if an anchor tag exists within the list item
        anchor = item.find('a')
        if anchor:
            link = anchor['href']
            links.append(link)

print(links)

with open('links.txt', 'w') as file:
    # Loop through the links and write each link to the file
    for link in links:
        file.write(link + '\n')

print("Links have been written to links.txt file.")