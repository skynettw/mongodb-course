import tkinter as tk
import requests
from bs4 import BeautifulSoup
from tkinter import ttk
from pymongo import MongoClient

conn = 'mongodb://admin:mymdb$1234@localhost:27017'
client = MongoClient(conn)
db = client['unit0204']
collection = db.carInfo


# 建立主視窗
root = tk.Tk()
root.title("商品管理程式")
root.geometry("800x500")

# 標題標籤
title_label = tk.Label(root, text="商品管理程式", bg="blue", fg="white", font=("微軟正黑體", 16))
title_label.pack(fill=tk.X)

# "取得最新資料" 按鈕
def fetch():
    data = list()
    url = "https://sscars.com.tw/car/page/1/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    selector = "div.product-small.box"
    cars = soup.select(selector)
    count = 0
    for car in cars:
        item = dict()
        item['name'] = car.text.strip().split("\n")[0]
        item['price'] = car.text.strip().split("\n")[1]
        item['description'] = car.text.strip().split("\n")[3]
        data.append(item)
    for item in data:
        if collection.find_one({"name": item["name"]}) is None:
            count = count + 1
            collection.insert_one(item)
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, f"共加入 {count} 筆新資料。\n")    

btn_fetch_data = tk.Button(root, text="取得最新資料", font=("微軟正黑體", 12), command=fetch)
btn_fetch_data.place(x=50, y=60, width=100, height=30)

# 搜尋輸入框
entry_search = tk.Entry(root, font=("微軟正黑體", 12))
entry_search.place(x=50, y=100, width=150, height=30)

def search():
    # 取得搜尋關鍵字
    keyword = entry_search.get()
    # 從 MongoDB 查詢資料
    query = {"name": {"$regex": keyword}}
    count = collection.count_documents(query)
    results = collection.find(query)
    # 清空顯示區域
    text_area.delete("1.0", tk.END)
    # 顯示查詢結果
    if count > 0:
        text_area.insert(tk.END, f"找到 {count} 筆資料\n")
        for result in results:
            text_area.insert(tk.END, f"【{result['price']}】{result['name']}\n")    
    else:
        text_area.insert(tk.END, "沒有找到任何結果")
        
# 搜尋按鈕
btn_search = tk.Button(root, text="搜尋", font=("微軟正黑體", 12), command=search)
btn_search.place(x=210, y=100, width=50, height=30)

# 顯示區域 (使用 Text 控件以便顯示多行文字)
text_area = tk.Text(root, font=("Arial", 12))
text_area.place(x=20, y=150, width=760, height=270)

# 捲軸
scrollbar = tk.Scrollbar(root, orient="vertical", command=text_area.yview)
scrollbar.place(x=780, y=150, height=270)

# 連接捲軸與顯示區域
text_area.config(yscrollcommand=scrollbar.set)

# 結束按鈕
btn_exit = tk.Button(root, text="結束", font=("Arial", 12), command=root.quit)
btn_exit.place(x=50, y=430, width=60, height=30)



# 啟動主事件循環
root.mainloop()
