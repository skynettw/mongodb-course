import requests, time, pymongo
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
# 設定PTT八卦版網址
url = "https://www.ptt.cc/bbs/Gossiping"
# 設定瀏覽器標頭
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
}
# 設定PTT八卦版cookies
cookies = {
    "over18":"1"
}
conn = "mongodb://admin:mymdb$1234@localhost:27017"
client = MongoClient(conn)
db = client.unit05db
db.gossiping.create_index([('title', pymongo.ASCENDING)], unique=True)
page = 1
while page <= 5:
    html = requests.get(url, headers=headers, cookies=cookies, verify=False).text
    soup = BeautifulSoup(html)
    items = soup.find_all("div", class_="r-ent")
    for item in items:
        data = dict()
        try:
            data['title'] = item.find("div", class_="title").a.text
            data['date']=item.find("div", class_="date").text
            data['author']=item.find("div", class_="author").text
            db.gossiping.insert_one(data)
        except DuplicateKeyError:
            print("資料已存在")
            pass
        except:
            pass
    nextpage_url = soup.find("a", string="‹ 上頁")['href']
    if nextpage_url == None:
        break
    url = "https://www.ptt.cc" + nextpage_url
    page += 1
    time.sleep(3)