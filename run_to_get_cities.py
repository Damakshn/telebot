from lxml import html
import requests

url = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8"

page = requests.get(url)
tree = html.fromstring(page.text)

with open("cities_list.txt", "w", encoding="utf-8") as f:
    for element in tree.xpath("//tr/td[3]"):
        f.writelines(element.text_content())
