import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
import time, requests
from bs4 import BeautifulSoup

# MongoDB 連線設置
def connect_to_mongo():
    try:
        # 修改此處為您的 MongoDB 連線 URI
        conn = "mongodb://admin:mymdb$1234@localhost:27017"
        client = MongoClient(conn)
        db = client["unit0204"]
        collection = db["carInfo"]
        # messagebox.showinfo("連線成功", "已成功連線到 MongoDB")
        return collection
    except Exception as e:
        messagebox.showerror("連線失敗", f"連線到 MongoDB 失敗: {e}")
        return None

def fetch(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    selector = "div.box-text.box-text-products"
    cars = soup.select(selector)
    data = list()
    for car in cars:
        try:
            item = dict()
            item['name'] = car.p.text
            item['price'] = car.select("span", class_="price")[0].text
            item['desc'] = car.h4.text
            data.append(item)
        except:
            pass
    return data

# 從 MongoDB 取得資料
def fetch_data():
    url_pattern = "https://sscars.com.tw/car/page/{}/"
    data = list()
    for page in range(1, 7):
        data = data + fetch(url_pattern.format(page))
        time.sleep(3)
    text_area.delete(1.0, tk.END)  # 清空文字區域
    text_area.insert(tk.END, f"共抓取 {len(data)} 筆資料\n")
    conn = "mongodb://admin:mymdb$1234@localhost:27017"
    client = MongoClient(conn)
    db = client["unit0204"]
    db.drop_collection("carInfo")
    db.create_collection("carInfo")
    collection = db["carInfo"]
    collection.insert_many(data)

# 搜尋 MongoDB 資料
def search_data():
    search_term = search_entry.get()
    collection = connect_to_mongo()
    if collection is not None:
        query = {"name": {"$regex": search_term}}
        count = collection.count_documents(query)
        result = collection.find(query)  # 修改 "欄位名稱" 為您的 MongoDB 欄位
        if count > 0:
            text_area.delete(1.0, tk.END)  # 清空文字區域
            text_area.insert(tk.END, f"找到 {count} 筆資料\n")
            for item in result:
                text_area.insert(tk.END, f"#【{item["name"]}】, {item['price']}, {item['desc']}\n")  # 將結果顯示在文字區域
            # messagebox.showinfo("搜尋結果", f"找到: {count} 筆資料")
        else:
            messagebox.showinfo("搜尋結果", "沒有找到資料")

# 結束應用程式
def quit_app():
    root.quit()

# 建立 Tkinter 視窗
root = tk.Tk()
root.title("商品管理程式")
root.geometry("800x400")

# 新增視窗元件
title_label = tk.Label(root, text="商品管理程式", bg="blue", fg="white", font=("Arial", 16))
title_label.pack(fill=tk.X)

fetch_button = tk.Button(root, text="取得最新資料", command=fetch_data)
fetch_button.pack(pady=10)

search_entry = tk.Entry(root)
search_entry.pack(pady=5)

search_button = tk.Button(root, text="搜尋", command=search_data)
search_button.pack(pady=5)

# 建立文字區域及垂直捲軸
text_frame = tk.Frame(root)
text_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# 建立捲軸
scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# 建立文字區域
text_area = tk.Text(text_frame, wrap="none", yscrollcommand=scrollbar.set, width=40, height=10)
text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 配置捲軸與文字區域的同步滾動
scrollbar.config(command=text_area.yview)

# 結束按鈕
quit_button = tk.Button(root, text="結束", command=quit_app)
quit_button.pack(side=tk.BOTTOM, pady=10)

# 啟動 Tkinter 主迴圈
root.mainloop()
