import requests
from bs4 import BeautifulSoup

"""
爬取豆瓣电影top250
"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/122.0.0.0 Safari/537.36'
}


def movie_top250(file="movie_top250.txt"):
    for start in range(0, 250, 25):
        # url = f"https://movie.douban.com/top250?start={start}&filter="
        # response = requests.get(url, headers=headers)
        url = f"https://movie.douban.com/top250"
        params = {
            "start": start
        }
        response = requests.get(url, params=params, headers=headers)
        html = response.text
        # print(html)
        # 解析html
        soup = BeautifulSoup(html, 'html.parser')
        all_titles = soup.findAll('span', attrs={'class': 'title'})
        with open(file, 'a', encoding='utf-8') as f:
            for title in all_titles:
                title_str = title.string.strip()
                if "/" not in title_str:
                    print(title_str)
                    f.write(title_str + "\n")


movie_top250()
