from bs4 import BeautifulSoup, Comment
import requests

url = "https://rabota.ykt.ru/jobs?categoriesIds=2083&page=1"
get_html = BeautifulSoup(requests.get(url).text, "html.parser")

result = list()
vacancies = get_html.find_all(class_='r-vacancy_list_item')
for v in vacancies:
    title = v.find(class_='r-vacancy_title').get_text()
    link = "https://rabota.ykt.ru" + \
        v.find(class_='r-vacancy_title_link').attrs['href']
    id = link.split('id=')[1]
    company = v.find(class_='r-vacancy_company').find("a").get_text()
    phone = v.find(class_='r-vacancy_contacts_phone').get_text().replace('\n', '').replace('\xa0', '') if v.find(
        class_='r-vacancy_contacts_phone') else "Телефон не указан"
    email = v.find(class_='r-vacancy_contacts_email').find("a").get_text()
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
    result.append({"id": id, "title": title, "company": company, "phone": phone, "email": email, "salary": salary,
                   "createdate": createdate, "link": link, "education": education, "schedule": schedule, "description": description, "responsibilities": responsibilities, "requirements": requirements, "conditions": conditions})

print(result[0])
