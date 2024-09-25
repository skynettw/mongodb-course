import tkinter as tk
from tkinter import ttk

def delete_selected_items():
    # 獲取所有選中的項目
    selected_items = tree.selection()
    
    if selected_items:
        # 刪除所有選中的項目
        for item in selected_items:
            tree.delete(item)

# 主視窗
root = tk.Tk()
root.title("多選刪除示例")

# 創建 Treeview
tree = ttk.Treeview(root, columns=("姓名", "年齡"), show='headings', selectmode='extended')
tree.heading("姓名", text="姓名")
tree.heading("年齡", text="年齡")

# 插入一些數據到 Treeview
tree.insert("", tk.END, values=("愛麗絲", 30))
tree.insert("", tk.END, values=("鮑伯", 25))
tree.insert("", tk.END, values=("查理", 35))

tree.pack(pady=20)

# 刪除選中項目的按鈕
btn_delete = tk.Button(root, text="刪除選中項目", command=delete_selected_items)
btn_delete.pack(pady=10)

root.mainloop()
