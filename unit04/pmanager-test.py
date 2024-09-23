import tkinter as tk
from tkinter import ttk
from woocommerce import API

# 設定 WooCommerce API 連接
wcapi1 = API(
    url="http://localhost:8081", 
    consumer_key="ck_53c93a2b250a345d0d56ef348c0c16d811546096",  
    consumer_secret="cs_41803c47be4fae4e8735d89dc5adbad3560d86eb",  
    version="wc/v3", 
    timeout=120
)
wcapi2 = API(
    url="http://localhost:8082", 
    consumer_key="ck_1c143868befe40b77d9bb13a4e14b884d728ea1e",  
    consumer_secret="cs_0cc138eb94895a9984ad9a0cf86912a5706e8e83",  
    version="wc/v3", 
    timeout=120
)
wcapi = wcapi2

# 創建主應用程式視窗
root = tk.Tk()
root.title("遠端商品管理程式")
root.geometry("300x450")

# 標題標籤
title_label = tk.Label(root, text="遠端商品管理程式", bg="pink", font=("Arial", 14))
title_label.pack(fill=tk.X, pady=10)

# 網站下拉選單
website_frame = tk.Frame(root)
website_frame.pack(fill=tk.X, pady=5)

website_label = ttk.Combobox(website_frame, values=["WP1", "WP2"], width=10)
website_label.set("WP1")
website_label.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

product_list = list()
product_category = list()

def load_website():
    global wcapi, product_list, product_category
    selected_website = website_label.get()
    if selected_website == "WP1":
        wcapi = wcapi1
    elif selected_website == "WP2":
        wcapi = wcapi2
    # 擷取所有商品
    response = wcapi.get("products", params={"per_page": 100})
    if response.status_code == 200:
        product_list = response.json()
    else:
        product_list = []
        print(f"無法獲取商品列表：{response.status_code}")
    # 擷取所有商品類別
    response = wcapi.get("products/categories", params={"per_page": 100})
    if response.status_code == 200:
        product_category = response.json()
    else:
        product_category = []
        print(f"無法獲取商品類別：{response.status_code}")
    update_category_dropdown()
    update_treeview()
    website_display.config(text=f"網站：{selected_website}")

load_button = tk.Button(website_frame, text="載入", width=5, command=load_website)
load_button.pack(side=tk.RIGHT, padx=5)

# 顯示當前網站
website_display = tk.Label(root, text="網站：WP1", bg="blueviolet", fg="white", height=2)
website_display.pack(fill=tk.X, pady=5)

# 類別下拉選單和篩選按鈕
category_frame = tk.Frame(root)
category_frame.pack(fill=tk.X, pady=5)

def update_category_dropdown():
    category_values = ["所有類別"]
    for category in product_category:
        if isinstance(category, dict) and "name" in category:
            category_values.append(category["name"])
    category_label["values"] = category_values

category_label = ttk.Combobox(category_frame, width=10)
category_label.set("類別")
category_label.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

def filter_products():
    selected_category = category_label.get()
    if selected_category == "所有類別":
        filtered_products = product_list
    else:
        filtered_products = [product for product in product_list if any(cat['name'] == selected_category for cat in product.get('categories', []))]
    update_treeview(filtered_products)

filter_button = tk.Button(category_frame, text="篩選", width=5, command=filter_products)
filter_button.pack(side=tk.RIGHT, padx=5)

# 關鍵字標籤、搜尋輸入框和搜尋按鈕
search_frame = tk.Frame(root)
search_frame.pack(fill=tk.X, pady=5)

keyword_label = tk.Label(search_frame, text="關鍵字", width=10)
keyword_label.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(search_frame, width=20)
search_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

search_button = tk.Button(search_frame, text="搜尋", width=5)
search_button.pack(side=tk.RIGHT, padx=5)

# 創建商品資料表格
columns = ("品名", "售價", "庫存")

tree = ttk.Treeview(root, columns=columns, show="headings", height=5)
tree.heading("品名", text="品名")
tree.heading("售價", text="售價")
tree.heading("庫存", text="庫存")

tree.column("品名", width=100)
tree.column("售價", width=50)
tree.column("庫存", width=50)

# 添加交替行顏色
tree.tag_configure('odd', background='#F8E0E0')  # 淺粉色
tree.tag_configure('even', background='#E0F0FF')  # 淺藍色

def update_treeview(products=None):
    if products is None:
        products = product_list
    # 清除現有的資料
    for item in tree.get_children():
        tree.delete(item)
    
    # 插入新的資料
    for i, product in enumerate(products):
        if isinstance(product, dict):
            name = product.get('name', '')
            price = product.get('price', '0')
            stock = product.get('stock_quantity', '0')
        else:
            name = str(product)
            price = '0'
            stock = '0'
        tag = 'even' if i % 2 == 0 else 'odd'
        tree.insert("", "end", values=(name, f"${price}", stock), tags=(tag,))

tree.pack(pady=10, fill=tk.X, expand=True)

# 額外操作按鈕
button_frame = tk.Frame(root)
button_frame.pack(pady=5, fill=tk.X)

discount_button = tk.Button(button_frame, text="折扣", width=8)
discount_button.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

delete_button = tk.Button(button_frame, text="刪除", width=8)
delete_button.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

update_button = tk.Button(button_frame, text="更新", width=8)
update_button.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

# 啟動主事件循環
root.mainloop()
