from bs4 import BeautifulSoup
import requests

url = "https://rabota.ykt.ru/jobs?categoriesIds=2083&page=1"
result = BeautifulSoup(requests.get(url).text, "html.parser")

vacancies = result.find_all(class_='r-vacancy_list_item')
for v in vacancies:
    title = v.find(class_='r-vacancy_title').get_text()
    company = v.find(class_='r-vacancy_company').find("a").get_text()
    salary = v.find(class_='r-vacancy_salary').get_text()
    createdate = v.find(class_='r-vacancy_createdate').get_text()
    box = v.find(class_='r-vacancy_box').find_all('dd')
    education = box[0].get_text()
    experience = box[1].get_text()
    schedule = box[2].get_text()
