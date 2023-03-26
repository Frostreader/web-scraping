import requests
from bs4 import BeautifulSoup as bs
from fake_user_agent import user_agent as ua
import json
import lxml


url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
headers = {'User-Agent': ua()}

page = requests.get(url=url, headers=headers)
soup = bs(page.text, 'lxml')

result = []

for vacancy in soup.find_all(class_='vacancy-serp-content'):
  # ссылка
  link_tag = vacancy.find_all(class_='serp-item__title')
  for x in link_tag:
    link = x['href']
    vacancy_desc = requests.get(url=link, headers=headers)
    desc_soup = bs(vacancy_desc.content, 'lxml')
    desc = desc_soup.find('div', class_='vacancy-description').text.lower().strip()


    if 'django' in desc and 'flask' in desc:
      # наименование компании
      companies_tag = vacancy.find_all(class_='vacancy-serp-item__meta-info-company')
      for x in companies_tag:
        company = x.text

      # ЗП
      salary_tag = vacancy.find_all('span', class_="bloko-header-section-3")
      for x in salary_tag:
        salary = x.text

      # город
      cities_tag = vacancy.select('.bloko-text[data-qa=vacancy-serp__vacancy-address]')
      for x in cities_tag:
        city = x.text

      # название вакансии
      vacancy_title_tag = soup.find_all(class_='serp-item__title')
      for x in vacancy_title_tag:
        vacancy_title = x.text

      result.append({
        'link': link,
        'salary': salary.replace('\u202f', ' '),
        'name': vacancy_title,
        'company': company,
        'city': city
      })

print(result)

with open('result.json', 'w', encoding='utf-8') as f:
  json.dump(result, f, ensure_ascii=False, indent=4)

