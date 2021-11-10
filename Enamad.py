import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

try:
    df = pd.read_excel('final.xlsx')
except FileNotFoundError:
    df = None


def get_sites(html_input):
    soup = BeautifulSoup(html_input.content, 'html.parser')
    sites = soup.find_all("div", attrs={"class": "row", "style": ["background-color: #ffffff",
                                                                  "background-color: #efefef"]})
    lst = []
    dic = {}
    for site in sites:
        text = site.text.replace("\n", " ").split("\n")
        stars = len(site.find_all('img'))
        text.append(stars)
        lst.append(text)
    for row in lst:
        text = re.findall(r'([-آ()0-9ا-ی/A-Za-z.]+)', str(row))
        cities = ['خراسان', 'آذربایجان', 'چهارمحال', 'سیستان', 'کهگیلویه']
        index = str(text[0])
        url = str(text[1])
        star_count = int(text[-1])
        city = str(text[-3])
        exp_date = str(text[-2])
        if str(text[-5]) not in cities and star_count != 0:
            title = ' '.join(text[2:-4])
            state = str(text[-4])
        elif star_count == 0 and str(text[-6]) in cities:
            title = ' '.join(text[2:-6])
            state = ' '.join(text[-6:-4])
            city = str(text[-4])
        elif star_count == 0 and str(text[-6]) not in cities:
            title = ' '.join(text[2:-5])
            state = str(text[-5])
            city = str(text[-4])
        else:
            title = ' '.join(text[2:-5])
            state = ' '.join(text[-5:-3])

        if df is not None:
            if (df['آدرس دامنه'] == url).any():
                print(url)
        dic[index] = {'آدرس دامنه': url, 'عنوان کسب و کار': title, 'استان': state,
                      'شهر': city, 'تعداد ستاره': star_count, 'تاریخ انقضا': exp_date}

    return dic


first_page_get = requests.get("https://enamad.ir/DomainListForMIMT")
first_page = get_sites(first_page_get)
last_page = BeautifulSoup(first_page_get.content, 'html.parser').find('li', attrs={'class': 'PagedList-skipToLast'}).a. \
    get('href')
print("1 done")

for page in range(2, int(last_page[-4:]) + 1):
    page_addr = requests.get(f"https://enamad.ir/DomainListForMIMT/Index/{page}")
    pages = get_sites(page_addr)
    first_page.update(pages)
    print(f"{page} added")

if df is None:
    df = pd.DataFrame.from_dict(first_page, orient='index')
    df.index.name = '#'
    df.to_excel('final.xlsx')
else:
    print('new rows successfully added!')
