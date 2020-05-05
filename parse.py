import requests
from bs4 import BeautifulSoup
import csv
import colorama

print(colorama.Fore.LIGHTBLUE_EX + '[x] Парсинг новостей - успешно!')

URL = 'https://www.samgups.ru'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/81.0.4044.129 Safari/537.36 OPR/68.0.3618.63',
    'accept': '*/*'}
HOST = 'https://www.samgups.ru'
FILE = 'src/news.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_news = soup.find_all('div', class_='news-item row')

    newsDict = []  # пустой словарь
    for news in all_news:
        newsDict.append({
            'title': '❗' + news.find('b').get_text(strip=True),
            'anons': '\n' + news.find('div', class_='news-anons').get_text(strip=True),
            'date': '📅' + news.find('span', class_='news-date-time').get_text(strip=True),
            'link': '🌐' + HOST + news.find('a').get('href')
        })
    return newsDict


def news_to_csv(newsDict, path):
    with open(path, 'w', newline='', encoding='utf8') as file:
        writer = csv.writer(file)
        for news in newsDict:
            writer.writerow([news['title'] + '\n' + news['anons'] + '\n' + news['date'] + '\n' + news['link']])


def parse_news():
    html = get_html(URL)
    if html.status_code == 200:
        newsDict = []
        get_content(html.text)
        newsDict.extend(get_content(html.text))
        news_to_csv(newsDict, FILE)
        print('Парсинг новостей - успешно!')
    else:
        return 'Ошибка парсинга!'


def view_all_news():
    newsList = []
    with open('src/news.csv', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            newsList.append(row)
        return newsList


def view_last_news():
    newsList = []
    with open('src/news.csv', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            newsList.append(row)
        last_newsString = ''.join(newsList[1])
        return last_newsString
