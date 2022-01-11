from bs4 import BeautifulSoup
import requests
import datetime
import json

categoryId = "2083"
get_pages = BeautifulSoup(requests.get(
    f"https://rabota.ykt.ru/jobs?categoriesIds={categoryId}").text, "html.parser")
pages = int(get_pages.find_all(class_='yui-pagination_page')
            [-2].find('a').get_text())

result = list()
for page in range(1, pages + 1):
    url = f"https://rabota.ykt.ru/jobs?categoriesIds={categoryId}&page={page}"
    get_html = BeautifulSoup(requests.get(url).text, "html.parser")

    vacancies = get_html.find_all(class_='r-vacancy_list_item')
    for v in vacancies:
        title = v.find(class_='r-vacancy_title').get_text()
        link = "https://rabota.ykt.ru" + \
            v.find(class_='r-vacancy_title_link').attrs['href']
        id = link.split('id=')[1]
        company = v.find(class_='r-vacancy_company').find("a").get_text()
        phone = v.find(class_='r-vacancy_contacts_phone').get_text().replace('\n', '').replace('\xa0', '') if v.find(
            class_='r-vacancy_contacts_phone') else "Телефон не указан"
        email = v.find(class_='r-vacancy_contacts_email').find("a").get_text(
        ) if v.find(class_='r-vacancy_contacts_email') else "Email не указан"
        salary = v.find(class_='r-vacancy_salary').get_text().replace('\n', '')
        createdate = "Дата не найдена"
        date_div = v.find(class_='r-vacancy_createdate')
        if date_div:
            createdate = date_div.get_text()
        if date_div and "Сегодня" in date_div.get_text():
            createdate = datetime.datetime.now().strftime("%d.%m.%Y")

        classes = v.find('div')["class"]
        if "r-vacancy--vip" in classes:
            type = "VIP вакансия"
        elif "r-vacancy--paid" in classes:
            type = "Платная вакансия"
        else:
            type = "Бесплатная вакансия"

        box = v.find(class_='r-vacancy_box').find_all('dd')
        try:
            education = box[0].get_text()
        except IndexError:
            education = "Требуемое образование не указано"
        try:
            experience = box[1].get_text()
        except IndexError:
            experience = "Требуемый опыт не указан"
        try:
            schedule = box[2].get_text()
        except IndexError:
            schedule = "График не указан"

        full_titles = v.find_all(class_='r-vacancy_body_full_title')
        try:
            description = full_titles[0].find_previous_sibling().get_text()
        except IndexError:
            description = "Описание вакансии не добавлено"
        try:
            responsibilities = full_titles[0].find_next_sibling().get_text(
                separator='\n', strip=True)
        except IndexError:
            responsibilities = "Обязанности вакансии не добавлено"
        try:
            requirements = full_titles[1].find_next_sibling(
            ).get_text(separator='\n', strip=True)
        except IndexError:
            requirements = "Требования вакансии не добавлено"
        try:
            conditions = full_titles[2].find_next_sibling(
            ).get_text(separator='\n', strip=True)
        except IndexError:
            conditions = "Условия работы не добавлено"

        result.append({"id": id, "type": type, "title": title, "company": company, "phone": phone, "email": email, "salary": salary,
                       "createdate": createdate, "link": link, "education": education, "schedule": schedule, "description": description, "responsibilities": responsibilities, "requirements": requirements, "conditions": conditions})

with open("result.json", "w", encoding='utf8') as f:
    json.dump(result, f, ensure_ascii=False)
