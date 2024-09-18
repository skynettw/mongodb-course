import tkinter as tk
from tkinter import ttk

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

website_label = ttk.Combobox(website_frame, values=["WP1", "WP2", "WP3"], width=10)
website_label.set("WP1")
website_label.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

load_button = tk.Button(website_frame, text="載入", width=5)
load_button.pack(side=tk.RIGHT, padx=5)

# Display current website
website_display = tk.Label(root, text="網站：WP1", bg="blueviolet", fg="white", height=2)
website_display.pack(fill=tk.X, pady=5)

# Category dropdown and filter button
category_frame = tk.Frame(root)
category_frame.pack(fill=tk.X, pady=5)

category_label = ttk.Combobox(category_frame, values=["所有類別", "類別1", "類別2"], width=10)
category_label.set("類別")
category_label.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

filter_button = tk.Button(category_frame, text="篩選", width=5)
filter_button.pack(side=tk.RIGHT, padx=5)

# Keyword label, search entry, and search button
search_frame = tk.Frame(root)
search_frame.pack(fill=tk.X, pady=5)

keyword_label = tk.Label(search_frame, text="關鍵字", width=10)
keyword_label.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(search_frame, width=20)
search_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

search_button = tk.Button(search_frame, text="搜尋", width=5)
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

# Example data insertion
for i in range(6):
    if i % 2 == 0:
        tree.insert("", "end", values=(f"商品{i+1}", f"${i*100}", f"{i*10}"), tags=('even',))
    else:
        tree.insert("", "end", values=(f"商品{i+1}", f"${i*100}", f"{i*10}"), tags=('odd',))

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
