from bs4 import BeautifulSoup
import requests

url = "https://rabota.ykt.ru/jobs?categoriesIds=2083&page=1"
result = BeautifulSoup(requests.get(url).text, "html.parser")

vacancies = result.find_all(class_='r-vacancy_list_item')
for each in vacancies:
    print(each.find(class_='r-vacancy_title').get_text())