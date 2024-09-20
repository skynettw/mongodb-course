import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("遠端商品管理程式")
root.geometry("300x500")

# Set the background color of the main window
root.configure(bg="#fddddd")

# Title label
title_label = tk.Label(root, text="遠端商品管理程式", font=("Arial", 14), bg="#f58a8a", fg="white", width=25)
title_label.grid(row=0, column=0, columnspan=3, pady=10)

# 網站下拉式選單標籤
website_label = tk.Label(root, text="網站：", bg="#fddddd")
website_label.grid(row=1, column=0, sticky="e")

# 網站下拉式選單
website_combo = ttk.Combobox(root, values=["WP1", "WP2"], width=10)
website_combo.current(0)
website_combo.grid(row=1, column=1)

# 載入按鈕
load_button = tk.Button(root, text="載入")
load_button.grid(row=1, column=2, padx=5)

# 新增：網站狀態標籤（修改外觀）
website_status_label = tk.Label(root, text="已選擇網站：WP1", font=("Arial", 12), bg="#4a86e8", fg="white", width=25)
website_status_label.grid(row=2, column=0, columnspan=3, pady=5)

# 更新網站狀態標籤的函數
def update_website_status(event):
    selected_website = website_combo.get()
    website_status_label.config(text=f"已選擇網站：{selected_website}")

# 綁定下拉式選單的選擇事件
website_combo.bind("<<ComboboxSelected>>", update_website_status)

# Category label
category_label = tk.Label(root, text="類別", bg="#fddddd")
category_label.grid(row=3, column=0, sticky="e", pady=5)

# Category dropdown menu
category_combo = ttk.Combobox(root, values=["所有", "類別1", "類別2"], width=10)
category_combo.grid(row=3, column=1)

# Filter button
filter_button = tk.Button(root, text="篩選")
filter_button.grid(row=3, column=2, padx=5)

# Keyword label
keyword_label = tk.Label(root, text="關鍵字", bg="#fddddd")
keyword_label.grid(row=4, column=0, sticky="e", pady=5)

# Keyword entry field
keyword_entry = tk.Entry(root, width=15)
keyword_entry.grid(row=4, column=1)

# Search button
search_button = tk.Button(root, text="搜尋")
search_button.grid(row=4, column=2, padx=5)

# Table for displaying items (Treeview)
columns = ("name", "price", "stock")
tree = ttk.Treeview(root, columns=columns, show="headings", height=8)
tree.heading("name", text="品名")
tree.heading("price", text="售價")
tree.heading("stock", text="庫存")

tree.column("name", width=100)
tree.column("price", width=50)
tree.column("stock", width=50)

tree.grid(row=5, column=0, columnspan=3, pady=10)

# Alternate row colors
tree.tag_configure("evenrow", background="#f0f8ff")
tree.tag_configure("oddrow", background="#fddddd")

# Add some dummy data
data = [
    ("商品1", 100, 50),
    ("商品2", 200, 30),
    ("商品3", 150, 20),
    ("商品4", 300, 15),
    ("商品5", 400, 10),
    ("商品6", 250, 25),
    ("商品7", 180, 40),
    ("商品8", 350, 12),
    ("商品9", 120, 60),
    ("商品10", 280, 18),
]

# Insert data into the treeview
for i, item in enumerate(data):
    tag = "evenrow" if i % 2 == 0 else "oddrow"
    tree.insert("", "end", values=item, tags=(tag,))

# Bottom buttons (fold, delete, update)
fold_button = tk.Button(root, text="折扣")
fold_button.grid(row=6, column=0, pady=5)

delete_button = tk.Button(root, text="刪除")
delete_button.grid(row=6, column=1, pady=5)

update_button = tk.Button(root, text="更新")
update_button.grid(row=6, column=2, pady=5)

# Run the application
root.mainloop()
