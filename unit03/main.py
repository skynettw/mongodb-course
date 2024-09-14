import tkinter as tk
from tkinter import messagebox, ttk
from pymongo import MongoClient
from tkcalendar import DateEntry
from datetime import datetime
import calendar
from bson.objectid import ObjectId
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm

# 在文件開頭添加以下代碼來設置中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 連接到 MongoDB
conn = "mongodb://admin:mymdb$1234@localhost:27017"
client = MongoClient(conn)
db = client["unit03db"]
users = db["user"]

# 新增全局變量來儲存當前登入的用戶名
current_user = None

def login():
    global current_user
    username = username_entry.get()
    password = password_entry.get()
    
    user = users.find_one({"username": username, "password": password})
    if user:
        current_user = username  # 記錄當前登入的用戶名
        show_main_menu()
    else:
        messagebox.showerror("登入失敗", "帳號或密碼錯誤")

def show_main_menu():
    # 清除所有現有框架
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame) and widget != title_frame:
            widget.destroy()
    
    # 創建主選單框架
    main_menu_frame = tk.Frame(root, bg="white")
    main_menu_frame.pack(expand=True, fill="both")
    
    buttons = [
        ("新增收入", add_income),
        ("新增支出", add_expense),
        ("瀏覽收支", browse_transactions),
        ("用戶資訊", show_user_info),
        ("登出", logout)
    ]
    
    for i, item in enumerate(buttons):
        if isinstance(item, tuple):
            text, command = item
            button = tk.Button(main_menu_frame, text=text, font=("微軟正黑體", 12, "bold"), width=20, command=command)
        else:
            button = tk.Button(main_menu_frame, text=item, font=("微軟正黑體", 12, "bold"), width=20)
        button.pack(pady=10)

def add_income():
    # 清除所有現有框架
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame) and widget != title_frame:
            widget.destroy()
    
    # 創建新增收入框架
    income_frame = tk.Frame(root, bg="white")
    income_frame.pack(expand=True, fill="both")
    
    # 創建內部框架以實現置中效果
    inner_frame = tk.Frame(income_frame, bg="white")
    inner_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    # 日期
    tk.Label(inner_frame, text="日期:", bg="white", font=("微軟正黑體", 14)).grid(row=0, column=0, sticky="e", pady=10)
    date_entry = DateEntry(inner_frame, width=12, background='darkblue', foreground='white', borderwidth=2, font=("微軟正黑體", 14))
    date_entry.grid(row=0, column=1, pady=10, padx=10)
    
    # 摘要
    tk.Label(inner_frame, text="摘要:", bg="white", font=("微軟正黑體", 14)).grid(row=1, column=0, sticky="e", pady=10)
    summary_entry = tk.Entry(inner_frame, font=("微軟正黑體", 14))
    summary_entry.grid(row=1, column=1, pady=10, padx=10)
    
    # 金額
    tk.Label(inner_frame, text="金額:", bg="white", font=("微軟正黑體", 14)).grid(row=2, column=0, sticky="e", pady=10)
    amount_entry = tk.Entry(inner_frame, font=("微軟正黑體", 14))
    amount_entry.grid(row=2, column=1, pady=10, padx=10)
    
    # 備註
    tk.Label(inner_frame, text="備註:", bg="white", font=("微軟正黑體", 14)).grid(row=3, column=0, sticky="e", pady=10)
    memo_entry = tk.Entry(inner_frame, font=("微軟正黑體", 14))
    memo_entry.grid(row=3, column=1, pady=10, padx=10)
    
    def clear_entries():
        date_entry.set_date(datetime.now())
        summary_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        memo_entry.delete(0, tk.END)
    
    def add_to_database(and_return=False):
        global current_user
        date = date_entry.get_date()
        summary = summary_entry.get()
        amount = amount_entry.get()
        memo = memo_entry.get()
        
        if not (date and summary and amount):
            messagebox.showerror("錯誤", "請填寫所有必要欄位（日期、摘要、金額）")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("錯誤", "金額必須是數字")
            return
        
        # 將 date 轉換為 datetime 對象
        date_time = datetime.combine(date, datetime.min.time())
        
        # 新增到資料庫
        transaction = {
            "user": current_user,  # 使用全局變量中儲存的用戶名
            "date": date_time,  # 使用轉換後的 datetime 對象
            "amount": amount,
            "category": "income",
            "summary": summary,  # 添加摘要欄位
            "memo": memo
        }
        db.transaction.insert_one(transaction)
        
        messagebox.showinfo("成功", "收入已新增")
        
        if and_return:
            show_main_menu()
        else:
            clear_entries()
    
    # 按鈕
    button_frame = tk.Frame(inner_frame, bg="white")
    button_frame.grid(row=4, column=0, columnspan=2, pady=20)
    
    tk.Button(button_frame, text="新增", command=lambda: add_to_database(False), font=("微軟正黑體", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="新增並返回", command=lambda: add_to_database(True), font=("微軟正黑體", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="清除", command=clear_entries, font=("微軟正黑體", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="直接返回", command=show_main_menu, font=("微軟正黑體", 12)).pack(side=tk.LEFT, padx=5)

def add_expense():
    # 清除所有現有框架
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame) and widget != title_frame:
            widget.destroy()
    
    # 創建新增支出框架
    expense_frame = tk.Frame(root, bg="white")
    expense_frame.pack(expand=True, fill="both")
    
    # 創建內部框架以實現置中效果
    inner_frame = tk.Frame(expense_frame, bg="white")
    inner_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    # 日期
    tk.Label(inner_frame, text="日期:", bg="white", font=("微軟正黑體", 14)).grid(row=0, column=0, sticky="e", pady=10)
    date_entry = DateEntry(inner_frame, width=12, background='darkblue', foreground='white', borderwidth=2, font=("微軟正黑體", 14))
    date_entry.grid(row=0, column=1, pady=10, padx=10)
    
    # 摘要
    tk.Label(inner_frame, text="摘要:", bg="white", font=("微軟正黑體", 14)).grid(row=1, column=0, sticky="e", pady=10)
    summary_entry = tk.Entry(inner_frame, font=("微軟正黑體", 14))
    summary_entry.grid(row=1, column=1, pady=10, padx=10)
    
    # 金額
    tk.Label(inner_frame, text="金額:", bg="white", font=("微軟正黑體", 14)).grid(row=2, column=0, sticky="e", pady=10)
    amount_entry = tk.Entry(inner_frame, font=("微軟正黑體", 14))
    amount_entry.grid(row=2, column=1, pady=10, padx=10)
    
    # 備註
    tk.Label(inner_frame, text="備註:", bg="white", font=("微軟正黑體", 14)).grid(row=3, column=0, sticky="e", pady=10)
    memo_entry = tk.Entry(inner_frame, font=("微軟正黑體", 14))
    memo_entry.grid(row=3, column=1, pady=10, padx=10)
    
    def clear_entries():
        date_entry.set_date(datetime.now())
        summary_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        memo_entry.delete(0, tk.END)
    
    def add_to_database(and_return=False):
        global current_user
        date = date_entry.get_date()
        summary = summary_entry.get()
        amount = amount_entry.get()
        memo = memo_entry.get()
        
        if not (date and summary and amount):
            messagebox.showerror("錯誤", "請填寫所有必要欄位（日期、摘要、金額）")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("錯誤", "金額必須是數字")
            return
        
        # 將 date 轉換為 datetime 對象
        date_time = datetime.combine(date, datetime.min.time())
        
        # 新增到資料庫
        transaction = {
            "user": current_user,
            "date": date_time,
            "amount": amount,
            "category": "expense",
            "summary": summary,  # 添加摘要欄位
            "memo": memo
        }
        db.transaction.insert_one(transaction)
        
        messagebox.showinfo("成功", "支出已新增")
        
        if and_return:
            show_main_menu()
        else:
            clear_entries()
    
    # 按鈕
    button_frame = tk.Frame(inner_frame, bg="white")
    button_frame.grid(row=4, column=0, columnspan=2, pady=20)
    
    tk.Button(button_frame, text="新增", command=lambda: add_to_database(False), font=("微軟正黑體", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="新增並返回", command=lambda: add_to_database(True), font=("微軟正黑體", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="清除", command=clear_entries, font=("微軟正黑體", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="直接返回", command=show_main_menu, font=("微軟正黑體", 12)).pack(side=tk.LEFT, padx=5)

def browse_transactions():
    # 清除所有現有框架
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame) and widget != title_frame:
            widget.destroy()
    
    # 創建瀏覽收支框架
    browse_frame = tk.Frame(root, bg="white")
    browse_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # 年份選擇
    tk.Label(browse_frame, text="年份:", bg="white").grid(row=0, column=0, sticky="e", pady=5)
    year_var = tk.StringVar(value=str(datetime.now().year))
    year_menu = ttk.Combobox(browse_frame, textvariable=year_var, values=[str(year) for year in range(2020, datetime.now().year + 1)])
    year_menu.grid(row=0, column=1, pady=5)
    
    # 月份選擇
    tk.Label(browse_frame, text="月份:", bg="white").grid(row=0, column=2, sticky="e", pady=5)
    month_var = tk.StringVar(value=str(datetime.now().month))
    month_menu = ttk.Combobox(browse_frame, textvariable=month_var, values=[str(month) for month in range(1, 13)])
    month_menu.grid(row=0, column=3, pady=5)
    
    # 類型選擇
    tk.Label(browse_frame, text="類型:", bg="white").grid(row=1, column=0, sticky="e", pady=5)
    type_var = tk.StringVar(value="全部")
    type_menu = ttk.Combobox(browse_frame, textvariable=type_var, values=["全部", "收入", "支出"])
    type_menu.grid(row=1, column=1, pady=5)
    
    # 創建顯示區域
    display_frame = tk.Frame(browse_frame, bg="white")
    display_frame.grid(row=2, column=0, columnspan=4, pady=10)
    
    # 合計金額標籤
    total_label = tk.Label(display_frame, text="合計: 0", font=("微軟正黑體", 16, "bold"), bg="white")
    total_label.pack()
    
import tkinter as tk
from tkinter import messagebox, ttk
from pymongo import MongoClient
from tkcalendar import DateEntry
from datetime import datetime
import calendar
from bson.objectid import ObjectId
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm

# 在文件開頭添加以下代碼來設置中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 連接到 MongoDB
conn = "mongodb://admin:mymdb$1234@localhost:27017"
client = MongoClient(conn)
db = client["unit03db"]
users = db["user"]

# 新增全局變量來儲存當前登入的用戶名
current_user = None

def login():
    global current_user
    username = username_entry.get()
    password = password_entry.get()
    
    user = users.find_one({"username": username, "password": password})
    if user:
        current_user = username  # 記錄當前登入的用戶名
        show_main_menu()
    else:
        messagebox.showerror("登入失敗", "帳號或密碼錯誤")

def show_main_menu():
    # 清除所有現有框架
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame) and widget != title_frame:
            widget.destroy()
    
    # 創建主選單框架
    main_menu_frame = tk.Frame(root, bg="white")
    main_menu_frame.pack(expand=True, fill="both")
    
    buttons = [
        ("新增收入", add_income),
        ("新增支出", add_expense),
        ("瀏覽收支", browse_transactions),
        ("用戶資訊", show_user_info),
        ("登出", logout)
    ]
    
    for i, item in enumerate(buttons):
        if isinstance(item, tuple):
            text, command = item
            button = tk.Button(main_menu_frame, text=text, font=("微軟正黑體", 12, "bold"), width=20, command=command)
        else:
            button = tk.Button(main_menu_frame, text=item, font=("微軟正黑體", 12, "bold"), width=20)
        button.pack(pady=10)

def add_income():
    # 清除所有現有框架
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame) and widget != title_frame:
            widget.destroy()
    
    # 創建新增收入框架
    income_frame = tk.Frame(root, bg="white")
    income_frame.pack(expand=True, fill="both")
    
    # 創建內部框架以實現置中效果
    inner_frame = tk.Frame(income_frame, bg="white")
    inner_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    # 日期
    tk.Label(inner_frame, text="日期:", bg="white", font=("微軟正黑體", 14)).grid(row=0, column=0, sticky="e", pady=10)
    date_entry = DateEntry(inner_frame, width=12, background='darkblue', foreground='white', borderwidth=2, font=("微軟正黑體", 14))
    date_entry.grid(row=0, column=1, pady=10, padx=10)
    
    # 摘要
    tk.Label(inner_frame, text="摘要:", bg="white", font=("微軟正黑體", 14)).grid(row=1, column=0, sticky="e", pady=10)
    summary_entry = tk.Entry(inner_frame, font=("微軟正黑體", 14))
    summary_entry.grid(row=1, column=1, pady=10, padx=10)
    
    # 金額
    tk.Label(inner_frame, text="金額:", bg="white", font=("微軟正黑體", 14)).grid(row=2, column=0, sticky="e", pady=10)
    amount_entry = tk.Entry(inner_frame, font=("微軟正黑體", 14))
    amount_entry.grid(row=2, column=1, pady=10, padx=10)
    
    # 備註
    tk.Label(inner_frame, text="備註:", bg="white", font=("微軟正黑體", 14)).grid(row=3, column=0, sticky="e", pady=10)
    memo_entry = tk.Entry(inner_frame, font=("微軟正黑體", 14))
    memo_entry.grid(row=3, column=1, pady=10, padx=10)
    
    def clear_entries():
        date_entry.set_date(datetime.now())
        summary_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        memo_entry.delete(0, tk.END)
    
    def add_to_database(and_return=False):
        global current_user
        date = date_entry.get_date()
        summary = summary_entry.get()
        amount = amount_entry.get()
        memo = memo_entry.get()
        
        if not (date and summary and amount):
            messagebox.showerror("錯誤", "請填寫所有必要欄位（日期、摘要、金額）")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("錯誤", "金額必須是數字")
            return
        
        # 將 date 轉換為 datetime 對象
        date_time = datetime.combine(date, datetime.min.time())
        
        # 新增到資料庫
        transaction = {
            "user": current_user,  # 使用全局變量中儲存的用戶名
            "date": date_time,  # 使用轉換後的 datetime 對象
            "amount": amount,
            "category": "income",
            "summary": summary,  # 添加摘要欄位
            "memo": memo
        }
        db.transaction.insert_one(transaction)
        
        messagebox.showinfo("成功", "收入已新增")
        
        if and_return:
            show_main_menu()
        else:
            clear_entries()
    
    # 按鈕
    button_frame = tk.Frame(inner_frame, bg="white")
    button_frame.grid(row=4, column=0, columnspan=2, pady=20)
    
    tk.Button(button_frame, text="新增", command=lambda: add_to_database(False), font=("微軟正黑體", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="新增並返回", command=lambda: add_to_database(True), font=("微軟正黑體", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="清除", command=clear_entries, font=("微軟正黑體", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="直接返回", command=show_main_menu, font=("微軟正黑體", 12)).pack(side=tk.LEFT, padx=5)

def add_expense():
    # 清除所有現有框架
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame) and widget != title_frame:
            widget.destroy()
    
    # 創建新增支出框架
    expense_frame = tk.Frame(root, bg="white")
    expense_frame.pack(expand=True, fill="both")
    
    # 創建內部框架以實現置中效果
    inner_frame = tk.Frame(expense_frame, bg="white")
    inner_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    # 日期
    tk.Label(inner_frame, text="日期:", bg="white", font=("微軟正黑體", 14)).grid(row=0, column=0, sticky="e", pady=10)
    date_entry = DateEntry(inner_frame, width=12, background='darkblue', foreground='white', borderwidth=2, font=("微軟正黑體", 14))
    date_entry.grid(row=0, column=1, pady=10, padx=10)
    
    # 摘要
    tk.Label(inner_frame, text="摘要:", bg="white", font=("微軟正黑體", 14)).grid(row=1, column=0, sticky="e", pady=10)
    summary_entry = tk.Entry(inner_frame, font=("微軟正黑體", 14))
    summary_entry.grid(row=1, column=1, pady=10, padx=10)
    
    # 金額
    tk.Label(inner_frame, text="金額:", bg="white", font=("微軟正黑體", 14)).grid(row=2, column=0, sticky="e", pady=10)
    amount_entry = tk.Entry(inner_frame, font=("微軟正黑體", 14))
    amount_entry.grid(row=2, column=1, pady=10, padx=10)
    
    # 備註
    tk.Label(inner_frame, text="備註:", bg="white", font=("微軟正黑體", 14)).grid(row=3, column=0, sticky="e", pady=10)
    memo_entry = tk.Entry(inner_frame, font=("微軟正黑體", 14))
    memo_entry.grid(row=3, column=1, pady=10, padx=10)
    
    def clear_entries():
        date_entry.set_date(datetime.now())
        summary_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        memo_entry.delete(0, tk.END)
    
    def add_to_database(and_return=False):
        global current_user
        date = date_entry.get_date()
        summary = summary_entry.get()
        amount = amount_entry.get()
        memo = memo_entry.get()
        
        if not (date and summary and amount):
            messagebox.showerror("錯誤", "請填寫所有必要欄位（日期、摘要、金額）")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("錯誤", "金額必須是數字")
            return
        
        # 將 date 轉換為 datetime 對象
        date_time = datetime.combine(date, datetime.min.time())
        
        # 新增到資料庫
        transaction = {
            "user": current_user,
            "date": date_time,
            "amount": amount,
            "category": "expense",
            "summary": summary,  # 添加摘要欄位
            "memo": memo
        }
        db.transaction.insert_one(transaction)
        
        messagebox.showinfo("成功", "支出已新增")
        
        if and_return:
            show_main_menu()
        else:
            clear_entries()
    
    # 按鈕
    button_frame = tk.Frame(inner_frame, bg="white")
    button_frame.grid(row=4, column=0, columnspan=2, pady=20)
    
    tk.Button(button_frame, text="新增", command=lambda: add_to_database(False), font=("微軟正黑體", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="新增並返回", command=lambda: add_to_database(True), font=("微軟正黑體", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="清除", command=clear_entries, font=("微軟正黑體", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="直接返回", command=show_main_menu, font=("微軟正黑體", 12)).pack(side=tk.LEFT, padx=5)

def browse_transactions():
    # 清除所有現有框架
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame) and widget != title_frame:
            widget.destroy()
    
    # 創建瀏覽收支框架
    browse_frame = tk.Frame(root, bg="white")
    browse_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # 年份選擇
    tk.Label(browse_frame, text="年份:", bg="white").grid(row=0, column=0, sticky="e", pady=5)
    year_var = tk.StringVar(value=str(datetime.now().year))
    year_menu = ttk.Combobox(browse_frame, textvariable=year_var, values=[str(year) for year in range(2020, datetime.now().year + 1)])
    year_menu.grid(row=0, column=1, pady=5)
    
    # 月份選擇
    tk.Label(browse_frame, text="月份:", bg="white").grid(row=0, column=2, sticky="e", pady=5)
    month_var = tk.StringVar(value=str(datetime.now().month))
    month_menu = ttk.Combobox(browse_frame, textvariable=month_var, values=[str(month) for month in range(1, 13)])
    month_menu.grid(row=0, column=3, pady=5)
    
    # 類型選擇
    tk.Label(browse_frame, text="類型:", bg="white").grid(row=1, column=0, sticky="e", pady=5)
    type_var = tk.StringVar(value="全部")
    type_menu = ttk.Combobox(browse_frame, textvariable=type_var, values=["全部", "收入", "支出"])
    type_menu.grid(row=1, column=1, pady=5)
    
    # 創建顯示區域
    display_frame = tk.Frame(browse_frame, bg="white")
    display_frame.grid(row=2, column=0, columnspan=4, pady=10)
    
    # 合計金額標籤
    total_label = tk.Label(display_frame, text="合計: 0", font=("微軟正黑體", 16, "bold"), bg="white")
    total_label.pack()
    
    # 創建列表顯示和捲軸
    tree_frame = tk.Frame(display_frame)
    tree_frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(tree_frame, columns=("date", "summary", "amount", "memo"), show="headings")
    tree.heading("date", text="日期")
    tree.heading("summary", text="摘要")
    tree.heading("amount", text="金額")
    tree.heading("memo", text="備註")
    tree.column("date", width=100)
    tree.column("summary", width=200)
    tree.column("amount", width=100)
    tree.column("memo", width=300)

    # 添加垂直捲軸
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

    def on_item_click(event):
        item = tree.selection()[0]
        transaction_id = tree.item(item, "values")[-1]  # 獲取存儲的 _id 字符串
        if messagebox.askyesno("刪除確認", "您確定要刪除這筆記錄嗎？"):
            # 將字符串轉換為 ObjectId
            object_id = ObjectId(transaction_id)
            result = db.transaction.delete_one({"_id": object_id})
            if result.deleted_count > 0:
                messagebox.showinfo("成功", "記錄已刪除")
                update_display()
            else:
                messagebox.showerror("錯誤", "刪除失敗,請稍後再試")

    tree.bind("<ButtonRelease-1>", on_item_click)

    def update_display():
        # 清除現有項目
        for item in tree.get_children():
            tree.delete(item)

        # 獲取選擇的年月和類型
        year = int(year_var.get())
        month = int(month_var.get())
        type_filter = type_var.get()
        
        # 構建查詢條件
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
        query = {
            "user": current_user,
            "date": {"$gte": start_date, "$lte": end_date}
        }
        if type_filter != "全部":
            query["category"] = "income" if type_filter == "收入" else "expense"
        
        # 查詢資料庫
        transactions = db.transaction.find(query).sort("date", 1)
        
        # 顯示交易記錄
        total = 0
        for trans in transactions:
            date_str = trans["date"].strftime("%Y-%m-%d")
            amount = trans["amount"] if trans["category"] == "income" else -trans["amount"]
            total += amount
            summary = trans.get("summary", "無摘要")
            memo = trans.get("memo", "")
            
            # 插入記錄，包括 _id 作為最後一個值
            item = tree.insert("", "end", values=(date_str, summary, f"{amount:.2f}", memo, str(trans["_id"])))
            tree.tag_configure("income", foreground="green")
            tree.tag_configure("expense", foreground="red")
            tree.item(item, tags=(trans["category"],))

        # 更新合計金額
        total_label.config(text=f"合計: {total:.2f}", fg="green" if total >= 0 else "red")
    
    # 綁定更新函數到選單
    year_menu.bind("<<ComboboxSelected>>", lambda e: update_display())
    month_menu.bind("<<ComboboxSelected>>", lambda e: update_display())
    type_menu.bind("<<ComboboxSelected>>", lambda e: update_display())
    
    # 返回按鈕
    tk.Button(browse_frame, text="返回主選單", command=show_main_menu).grid(row=3, column=0, columnspan=4, pady=10)
    
    # 初始顯示
    update_display()

def show_user_info():
    # 清除所有現有框架
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame) and widget != title_frame:
            widget.destroy()
    
    # 創建用戶資訊框架
    user_info_frame = tk.Frame(root, bg="white")
    user_info_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # 顯示用戶名稱
    tk.Label(user_info_frame, text=f"用戶名稱: {current_user}", font=("微軟正黑體", 16, "bold"), bg="white").pack(pady=5)
    # 返回按鈕
    tk.Button(user_info_frame, text="返回主選單", command=show_main_menu, font=("微軟正黑體", 12)).pack(pady=5)
    # 創建左右框架
    left_frame = tk.Frame(user_info_frame, bg="white")
    left_frame.pack(side="left", expand=True, fill="both")
    right_frame = tk.Frame(user_info_frame, bg="white")
    right_frame.pack(side="right", expand=True, fill="both")

    # 創建列表顯示和捲軸
    tree_frame = tk.Frame(left_frame)
    tree_frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(tree_frame, columns=("month", "income", "expense", "balance"), show="headings", height=10)  # 設置高度為10行
    tree.heading("month", text="月份")
    tree.heading("income", text="收入")
    tree.heading("expense", text="支出")
    tree.heading("balance", text="結餘")
    tree.column("month", width=50)
    tree.column("income", width=100)
    tree.column("expense", width=100)
    tree.column("balance", width=100)

    # 添加垂直捲軸
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

    # 獲取本年度每個月份的收支總計
    current_year = datetime.now().year
    monthly_data = []
    for month in range(1, 13):
        start_date = datetime(current_year, month, 1)
        end_date = datetime(current_year, month, calendar.monthrange(current_year, month)[1], 23, 59, 59)
        
        pipeline = [
            {
                "$match": {
                    "user": current_user,
                    "date": {"$gte": start_date, "$lte": end_date}
                }
            },
            {
                "$group": {
                    "_id": "$category",
                    "total": {"$sum": "$amount"}
                }
            }
        ]
        
        result = list(db.transaction.aggregate(pipeline))
        
        income = next((item["total"] for item in result if item["_id"] == "income"), 0)
        expense = next((item["total"] for item in result if item["_id"] == "expense"), 0)
        balance = income - expense
        
        tree.insert("", "end", values=(f"{month}月", f"{income:.2f}", f"{expense:.2f}", f"{balance:.2f}"))
        monthly_data.append(balance)

    # 創建直條圖
    fig, ax = plt.subplots(figsize=(5, 3))  # 減小圖表大小
    months = range(1, 13)
    colors = ['green' if x >= 0 else 'red' for x in monthly_data]
    ax.bar(months, monthly_data, color=colors)
    ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax.set_xlabel('月份')
    ax.set_ylabel('結餘')
    ax.set_title(f'{current_year}年度月收支結餘')
    ax.set_xticks(months)
    ax.set_xticklabels(months)
    plt.tight_layout()  # 自動調整佈局

    # 將直條圖嵌入到 Tkinter 視窗中
    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(pady=10, expand=True, fill="both")

    

def logout():
    global current_user
    current_user = None  # 清除當前用戶
    # 清除主選單框架
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame) and widget != title_frame:
            widget.destroy()
    
    # 重新創建並顯示登入框架
    create_login_frame()

def create_login_frame():
    global login_frame, username_entry, password_entry
    login_frame = tk.Frame(root, bg="white")
    login_frame.pack(expand=True)

    username_label = tk.Label(login_frame, text="帳號:", bg="white")
    username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    username_entry = tk.Entry(login_frame)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    password_label = tk.Label(login_frame, text="密碼:", bg="white")
    password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

    password_entry = tk.Entry(login_frame, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    login_button = tk.Button(login_frame, text="登入", command=login)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

# 創建主視窗
root = tk.Tk()
root.title("個人記帳程式")
root.geometry("800x600")
root.configure(bg="white")

# 創建標題
title_frame = tk.Frame(root, bg="blue", width=800)
title_frame.pack(fill="x")

title_label = tk.Label(title_frame, text="個人記帳程式", font=("Arial", 24), bg="blue", fg="white")
title_label.pack(pady=10)

# 初始創建登入框架
create_login_frame()

# 在主程式中添加以下行來確保可以使用 DateEntry
root.option_add('*TCombobox*Listbox.font', ('微軟正黑體', 12))

root.mainloop()