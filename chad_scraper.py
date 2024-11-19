import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import random
import csv


def check_page_availability(url):
    try:
        response = urlopen(url)
        print("Страница доступна:", url)
    except HTTPError as e:
        print(f"HTTP ошибка: {e.code} {e.reason}")
    except URLError as e:
        print(f"Ошибка подключения: {e.reason}")


def check_ssl_certificate(url):
    try:
        requests.get(url)
        print(f"Сайт {url} использует SSL сертификат")
    except requests.exceptions.SSLError:
        print(f"Сайт {url} не использует SSL сертификат")


def get_site_info(url):
    response = requests.get(url)

    print(f"{'Status Code':<12}: {response.status_code}")
    print(f"{'Headers':<12}: {response.headers}")
    print(f"{'Url':<12}: {response.url}")
    print(f"{'History':<12}: {response.history}")
    print(f"{'Encoding':<12}: {response.encoding}")
    print(f"{'Reason':<12}: {response.reason}")
    print(f"{'Cookies':<12}: {response.cookies}")
    print(f"{'Elapsed':<12}: {response.elapsed}")
    print(f"{'Request':<12}: {response.request}")
    print(f"{'Content':<12}: {response.content[:200]}")


def get_robots_txt(url):
    response = requests.get(url)
    print(f"Содержимое robots.txt с сайта {url}:\n", response.text[:1000])


def get_h1_tag(url):
    try:
        response = urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        h1 = soup.find('h1')
        print("Заголовок h1:", h1.text if h1 else "Не найден")
    except Exception as e:
        print(f"Ошибка при извлечении h1: {e}")


def get_all_headers(url):
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    print(f"Заголовки со страницы {url}:")
    for header in headers:
        print(header.name, ":", header.text.strip())


def get_all_links(url):
    response = requests.get(url)

    if response.status_code != 200:
        print("Ошибка при запросе страницы.")
        return

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    links = soup.find_all('a', href=True)
    for link in links:
        href = link['href']
        if href.startswith('http') or href.startswith('#'):
            print(href)
        elif href.startswith('/'):
            print(f"https://en.wikipedia.org{href}")


def count_csv_lines(url):
    response = requests.get(url)
    lines = response.text.strip().split('\n')
    print(f"Количество строк в CSV ({url}):", len(lines))


def scrape_imdb_top():
    url = "https://www.imdb.com/chart/top"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        titles = [x.text for x in soup.find_all("h3", class_="ipc-title__text")]
        titles = titles[1:-1]

        movies = []
        for i in range(len(titles)):
            movies.append({
                'title': titles[i]
            })

        random_movies = random.sample(movies, 10)

        for movie in random_movies:
            print("--------------------------------------------")
            print(f"{movie['title']}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке данных: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def main():
    print("Task 1")
    check_page_availability("http://example.com")

    print("Task 2")
    check_ssl_certificate("https://example.com")

    print("Task 3")
    get_site_info("https://python.org")

    print("Task 4")
    get_robots_txt("https://en.wikipedia.org/robots.txt")

    print("Task 5")
    get_h1_tag("http://www.example.com")

    print("Task 6")
    get_all_headers("https://en.wikipedia.org/wiki/Main_Page")

    print("Task 7")
    get_all_links("https://en.wikipedia.org/wiki/Python")

    print("Task 8")
    count_csv_lines("http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_month.csv")

    print("Task 9")
    scrape_imdb_top()


if __name__ == "__main__":
    main()
