from bs4 import BeautifulSoup, Comment
import requests

url = "https://rabota.ykt.ru/jobs?categoriesIds=2083&page=1"
get_html = BeautifulSoup(requests.get(url).text, "html.parser")

result = list()
vacancies = get_html.find_all(class_='r-vacancy_list_item')
for index, v in enumerate(vacancies, start=1):
    title = v.find(class_='r-vacancy_title').get_text()
    company = v.find(class_='r-vacancy_company').find("a").get_text()
    salary = v.find(class_='r-vacancy_salary').get_text().replace('\n', '')
    createdate = v.find(class_='r-vacancy_createdate').get_text()

    box = v.find(class_='r-vacancy_box').find_all('dd')
    education = box[0].get_text()
    experience = box[1].get_text()
    schedule = box[2].get_text()

    full_titles = v.find_all(class_='r-vacancy_body_full_title')
    description = full_titles[0].find_previous_sibling().get_text()
    responsibilities = full_titles[0].find_next_sibling(
    ).get_text().replace('\n', '')
    requirements = full_titles[1].find_next_sibling(
    ).get_text().replace('\n', '')
    conditions = full_titles[2].find_next_sibling(
    ).get_text().replace('\n', '')
    result.append({"id": index, "title": title, "company": company, "salary": salary,
                   "createdate": createdate, "education": education, "schedule": schedule, "description": description, "responsibilities": responsibilities, "requirements": requirements, "conditions": conditions})

print(list(result))
