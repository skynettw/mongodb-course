url_pattern = "https://www.nkust.edu.tw/p/403-1000-1363-{}.php?Lang=zh-tw"
import requests, time, json
from pymongo import MongoClient
import pymongo
from bs4 import BeautifulSoup
conn = "mongodb://admin:mymdb$1234@localhost:27017"
client = MongoClient(conn)
db = client.unit05db
db.nkustnews.create_index([('title', pymongo.ASCENDING)], unique=True)
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
}
data = list()
page = 1
while True:
    if page>5: break
    print("Fetching page:", page)
    url = url_pattern.format(page)
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    titles = soup.find_all("div", class_="mtitle")
    for title in titles:
        item = dict()
        item["title"] = title.a.text.strip()
        item["date"] = title.i.text.strip()
        item["url"] = title.a["href"]
        try:
            db.nkustnews.insert_one(item)
        except:
            print("資料已存在")
            pass
        data.append(item)
    has_next_page = soup.find("li", class_="pg-next")
    if has_next_page:
        page = page + 1
    else:
        break
    time.sleep(5)
print(len(data))
print("Done")