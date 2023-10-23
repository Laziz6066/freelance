from bs4 import BeautifulSoup
import requests
from multiprocessing import Pool
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/116.0.5845.888 Safari/537.36"
}

url = 'https://1000.menu/catalog/pirogi'
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")
recipes = soup.find_all('div', class_='cn-item')

links = []

for recipe in recipes:
    if recipe.find('div', class_='photo'):
        element = recipe.find('div', class_='photo')
        link = element.find('a')['href']
        url_d = "https://1000.menu" + link
        links.append(url_d)

result_list = []
id = 1
for detail in links[:10]:
    response = requests.get(url=detail, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    name = soup.find('div', class_='main-photo imgr links-no-style').find('a').get('title')

    photo = soup.find('div', class_='main-photo imgr links-no-style').find('a').get('href')

    ingredients_div = soup.find('div', {'id': 'ingredients'})
    ingredients_list = ingredients_div.find_all('div', {'class': 'ingredient'})

    formatted_ingredients = []

    for ingredient in ingredients_list:
        ing_name = ingredient.find('a', {'class': 'name'}).text.strip()
        quantity_span = ingredient.find('span', {'class': 'squant value'})
        quantity = quantity_span.text.strip() if quantity_span else ''
        unit_select = ingredient.find('select', {'class': 'recalc_s_num'})
        unit_option = unit_select.find('option', {'selected': True}) if unit_select else None

        unit = unit_option.text.strip() if unit_option else ''
        formatted_ingredient = f"{ing_name}: {quantity} {unit}"
        formatted_ingredients.append(formatted_ingredient)

    formatted_text = "\n".join(formatted_ingredients)

    proteins_percentage = soup.find(id='nutr_ratio_p').text
    proteins_grams = soup.find(id='nutr_p').text
    fats_percentage = soup.find(id='nutr_ratio_f').text
    fats_grams = soup.find(id='nutr_f').text
    carbs_percentage = soup.find(id='nutr_ratio_c').text
    carbs_grams = soup.find(id='nutr_c').text
    calories = soup.find(id='nutr_kcal').text

    instructions_list = soup.find('ol', class_='instructions').find_all('li')

    instructions_text = []
    photo_links = []
    iiin = 0
    for instruction in instructions_list:
        iiin += 1
        step_text_element = instruction.find('p', class_='instruction')
        if step_text_element:
            step_text = step_text_element.text.strip()
            instructions_text.append({f'Шаг {iiin}': step_text})

        photo_link_element = instruction.find('a', class_='step-img')
        if photo_link_element and 'href' in photo_link_element.attrs:
            photo_link = photo_link_element['href']

        photo_links.append({f'Шаг {iiin}': photo_link})

    for index, step_text in enumerate(instructions_text):
        print(f"Шаг {index + 1}: {step_text}")
        print(f"Ссылка на фото: {photo_links[index]}")
        print("\n")

    result_list.append(
        {
            'id': id,
            'name': name,
            'photo': photo,
            'ingredients': formatted_ingredients,
            'ccal': [f"Белки {proteins_percentage}% - {proteins_grams} г", f"Жиры {fats_percentage}% - {fats_grams} г",
                     f"Углеводы {carbs_percentage}% - {carbs_grams} г", f"{calories} ккал"],
            'description': instructions_text,
            'description_photo': photo_links

        }
    )
    id += 1

with open('result_list.json', 'a', encoding='utf-8') as file:
    json.dump(result_list, file, indent=4, ensure_ascii=False)