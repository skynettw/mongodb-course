import tkinter as tk
from tkinter import ttk
from woocommerce import API
from pymongo import MongoClient

conn = "mongodb://admin:mymdb$1234@localhost:27017/"
client = MongoClient(conn)
db_wp1 = client.wp1
db_wp2 = client.wp2
db = db_wp1

# 設定 WooCommerce API 連接
wcapi1 = API(
    url="http://localhost:8081",  # 本地 WooCommerce 網站 URL
    consumer_key="ck_b30416d781c7cb878e9c432d8e78c86a95a14e8f",  
    consumer_secret="cs_3bf8a4b269c915a0288de0ce18b7f312eab4df6c",  
    version="wc/v3", 
    timeout=120
)
wcapi2 = API(
    url="http://localhost:8082",  # 本地 WooCommerce 網站 URL
    consumer_key="ck_a239d97ddb8ee94467af18192a678a8dbfa7ff2a",  
    consumer_secret="cs_81cde3a32aeb48ad79eb32a76d0095d33b46ec5a",  
    version="wc/v3", 
    timeout=120
)
wcapi = wcapi1


# Create the main application window
root = tk.Tk()
root.title("遠端商品管理程式")
root.geometry("300x450")

# Title label
title_label = tk.Label(root, text="遠端商品管理程式", bg="pink", font=("Arial", 14))
title_label.pack(fill=tk.X, pady=10)

# Website dropdown menu
website_frame = tk.Frame(root)
website_frame.pack(fill=tk.X, pady=5)
website_frame.grid_columnconfigure(0, weight=1)
website_frame.grid_columnconfigure(1, weight=1)
website_frame.grid_columnconfigure(2, weight=1)

website_label = ttk.Combobox(website_frame, values=["WP1", "WP2"], width=10)
website_label.set("WP1")
website_label.grid(row=0, column=0, padx=5, pady=5)

product_list = []
product_category = []

def load_website():
    global wcapi, product_list, product_category
    selected_website = website_label.get()
    if selected_website == "WP1":
        wcapi = wcapi1
        db = db_wp1
    elif selected_website == "WP2":
        wcapi = wcapi2
        db = db_wp2

    # 取得所有商品
    product_list = wcapi.get("products").json()
    db.product.delete_many({})
    db.product.insert_many(product_list)
    
    # 取得所有商品分類
    product_category = wcapi.get("products/categories").json()
    db.category.delete_many({})
    db.category.insert_many(product_category)
    # 更新TreeView中的內容
    for i in tree.get_children():
        tree.delete(i)
    
    for i, product in enumerate(product_list):
        tags = 'even' if i % 2 == 0 else 'odd'
        tree.insert("", "end", values=(product['name'], f"${product['price']}", product['stock_quantity']), tags=(tags,))
    
    # 更新類別下拉式選單的值
    category_values = ["所有類別"] + [category['name'] for category in product_category]
    category_label['values'] = category_values
    category_label.set("所有類別")
    
    # 更新網站標題
    website_display.config(text=f"網站：{selected_website}")
def load_database():
    global wcapi, product_list, product_category, db, db_wp1, db_wp2
    selected_website = website_label.get()
    if selected_website == "WP1":
        db = db_wp1
    elif selected_website == "WP2":
        db = db_wp2

    # 取得所有商品
    product_list = db.product.find({})
    
    # 取得所有商品分類
    product_category = db.category.find({})
    # 更新TreeView中的內容
    for i in tree.get_children():
        tree.delete(i)
    
    for i, product in enumerate(product_list):
        tags = 'even' if i % 2 == 0 else 'odd'
        tree.insert("", "end", values=(product['name'], f"${product['price']}", product['stock_quantity']), tags=(tags,))
    
    # 更新類別下拉式選單的值
    category_values = ["所有類別"] + [category['name'] for category in product_category]
    category_label['values'] = category_values
    category_label.set("所有類別")
    
    # 更新網站標題
    website_display.config(text=f"網站：{selected_website}")
loadweb_button = tk.Button(website_frame, text="載入網站", width=8, command=load_website)
loadweb_button.grid(row=0, column=1, padx=5, pady=5)
load_button = tk.Button(website_frame, text="載入資料庫", width=8, command=load_database)
load_button.grid(row=0, column=2, padx=5, pady=5)

# Display current website
website_display = tk.Label(root, text="網站：WP1", bg="blueviolet", fg="white", height=2)
website_display.pack(fill=tk.X, pady=5)

# Category dropdown and filter button
category_frame = tk.Frame(root)
category_frame.pack(fill=tk.X, pady=5)

# 根據 product_category 的內容，設定下拉式選單的值
category_values = ["所有類別"] + [category['name'] for category in product_category]
category_label = ttk.Combobox(category_frame, values=category_values, width=10)
category_label.set("所有類別")
category_label.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

def filter_products():
    global db
    selected_category = category_label.get()
    filtered_products = []
    
    if selected_category == "所有類別":
        filtered_products = db.product.find({})
    else:
        filtered_products = db.product.find({"categories": {"$elemMatch": {"name": selected_category}}})
    
    # 更新TreeView中的內容
    for i in tree.get_children():
        tree.delete(i)
    
    for i, product in enumerate(filtered_products):
        tags = 'even' if i % 2 == 0 else 'odd'
        tree.insert("", "end", values=(product['name'], f"${product['price']}", product['stock_quantity']), tags=(tags,))

filter_button = tk.Button(category_frame, text="篩選", width=5, command=filter_products)
filter_button.pack(side=tk.RIGHT, padx=5)

# Keyword label, search entry, and search button
search_frame = tk.Frame(root)
search_frame.pack(fill=tk.X, pady=5)

keyword_label = tk.Label(search_frame, text="關鍵字", width=10)
keyword_label.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(search_frame, width=20)
search_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

def search_products():
    global db
    keyword = search_entry.get()
    filtered_products = []
    
    if keyword == "":
        filtered_products = db.product.find({})
    else:
        filtered_products = db.product.find({"name": {"$regex": keyword, "$options": "i"}})
    # 更新TreeView中的內容
    for i in tree.get_children():
        tree.delete(i)
    
    for i, product in enumerate(filtered_products):
        tags = 'even' if i % 2 == 0 else 'odd'
        tree.insert("", "end", values=(product['name'], f"${product['price']}", product['stock_quantity']), tags=(tags,))

search_button = tk.Button(search_frame, text="搜尋", width=5, command=search_products)
search_button.pack(side=tk.RIGHT, padx=5)

# Create the table for product data
columns = ("品名", "售價", "庫存")

tree = ttk.Treeview(root, columns=columns, show="headings", height=5)
tree.heading("品名", text="品名")
tree.heading("售價", text="售價")
tree.heading("庫存", text="庫存")

tree.column("品名", width=100)
tree.column("售價", width=50)
tree.column("庫存", width=50)

# Add alternating row colors
tree.tag_configure('odd', background='#F8E0E0')  # Light pink
tree.tag_configure('even', background='#E0F0FF')  # Light blue

tree.pack(pady=10, fill=tk.X, expand=True)

# Buttons for additional actions
button_frame = tk.Frame(root)
button_frame.pack(pady=5, fill=tk.X)

discount_button = tk.Button(button_frame, text="折扣", width=8)
discount_button.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

delete_button = tk.Button(button_frame, text="刪除", width=8)
delete_button.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

update_button = tk.Button(button_frame, text="更新", width=8)
update_button.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

# Start the main event loop
root.mainloop()