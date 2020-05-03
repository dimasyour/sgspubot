import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://www.samgups.ru'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/81.0.4044.129 Safari/537.36 OPR/68.0.3618.63',
    'accept': '*/*'}
HOST = 'https://www.samgups.ru'
FILE = 'news.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_news = soup.find_all('div', class_='news-item row')

    newsDict = []  # пустой словарь
    for news in all_news:
        newsDict.append({
            'title': news.find('b').get_text(strip=True),
            'anons': news.find('div', class_='news-anons').get_text(strip=True),
            'date': news.find('span', class_='news-date-time').get_text(strip=True),
            'link': HOST + news.find('a').get('href')
        })
    return newsDict


def news_to_csv(newsDict, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Заголовок', 'Анонс', 'Дата публикации', 'Ссылка'])
        for news in newsDict:
            writer.writerow([news['title'], news['anons'], news['date'], news['link']])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        newsDict = []
        get_content(html.text)
        newsDict.extend(get_content(html.text))
        news_to_csv(newsDict, FILE)
    else:
        return 'error'
