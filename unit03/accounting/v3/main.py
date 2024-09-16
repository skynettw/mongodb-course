import tkinter as tk
from tkinter import messagebox, font, ttk
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from tkcalendar import DateEntry
from datetime import datetime
import calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.font_manager import FontProperties
import matplotlib
matplotlib.use('TkAgg')

class AccountingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("個人記帳程式")
        self.master.geometry("800x500")
        self.master.configure(bg="white")

        self.conn = "mongodb://admin:mymdb$1234@localhost:27017"
        self.client = None
        self.db = None

        self.current_user = None  # 添加此行來存儲當前用戶

        self.setup_database()
        self.create_login_screen()

        # 設置中文字體
        self.chinese_font = FontProperties(fname=r"C:\Windows\Fonts\msjh.ttc", size=10)

        self.fig = None
        self.ax = None
        self.canvas = None

        # 綁定窗口關閉事件
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_database(self):
        try:
            self.client = MongoClient(self.conn)
            self.client.admin.command('ismaster')
            self.db = self.client['unit03db']
            print("成功連接到MongoDB")
        except ConnectionFailure:
            print("無法連接到MongoDB")
            messagebox.showerror("錯誤", "無法連接到資料庫")

    def create_login_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        title_frame = tk.Frame(self.master, bg="blue", height=50)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="個人記帳程式", font=("微軟正黑體", 20, "bold"), bg="blue", fg="white")
        title_label.pack(expand=True)

        login_frame = tk.Frame(self.master, bg="white")
        login_frame.pack(expand=True)

        tk.Label(login_frame, text="使用者名稱：", bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(login_frame, text="密碼：", bg="white").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        login_button = tk.Button(login_frame, text="登入", command=self.login)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.db.user.find_one({"username": username, "password": password})
        if user:
            self.current_user = username  # 設置當前用戶
            self.create_main_screen()
        else:
            messagebox.showerror("錯誤", "使用者名稱或密碼錯誤")

    def create_main_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        title_frame = tk.Frame(self.master, bg="blue", height=50)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="個人記帳程式", font=("微軟正黑體", 20, "bold"), bg="blue", fg="white")
        title_label.pack(expand=True)

        button_frame = tk.Frame(self.master, bg="white")
        button_frame.pack(expand=True)

        button_font = font.Font(family="微軟正黑體", size=12, weight="bold")

        buttons = [
            ("新增收入", self.add_income),
            ("新增支出", self.add_expense),
            ("瀏覽收支", self.view_transactions),
            ("用戶資訊", self.user_info),
            ("登出", self.logout)
        ]

        for text, command in buttons:
            button = tk.Button(button_frame, text=text, command=command, font=button_font, width=20)
            button.pack(pady=10)

    def add_income(self):
        self.create_income_form()

    def create_income_form(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        title_frame = tk.Frame(self.master, bg="blue", height=50)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="新增收入", font=("微軟正黑體", 20, "bold"), bg="blue", fg="white")
        title_label.pack(expand=True)

        form_frame = tk.Frame(self.master, bg="white")
        form_frame.pack(expand=True, padx=20, pady=20)

        tk.Label(form_frame, text="日期：", bg="white").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.date_entry = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="摘要：", bg="white").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.summary_entry = tk.Entry(form_frame)
        self.summary_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="金額：", bg="white").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.amount_entry = tk.Entry(form_frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="備註：", bg="white").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.memo_entry = tk.Entry(form_frame)
        self.memo_entry.grid(row=3, column=1, padx=5, pady=5)

        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="新增", command=self.add_transaction).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="新增並返回", command=self.add_and_return).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="清除", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="直接返回", command=self.create_main_screen).pack(side=tk.LEFT, padx=5)

    def add_transaction(self, return_to_main=False):
        date = self.date_entry.get_date()
        summary = self.summary_entry.get()
        amount = self.amount_entry.get()
        memo = self.memo_entry.get()

        if not all([date, summary, amount]):
            messagebox.showerror("錯誤", "請填寫所有必填欄位（日期、摘要、金額）")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("錯誤", "金額必須是數字")
            return

        # 將 date 轉換為 datetime 對象
        date_time = datetime.combine(date, datetime.min.time())

        transaction = {
            "user": self.current_user,
            "date": date_time,  # 使用轉換後的 datetime 對象
            "amount": amount,
            "category": "income",
            "memo": memo
        }

        self.db.transaction.insert_one(transaction)
        messagebox.showinfo("成功", "收入已新增")

        if return_to_main:
            self.create_main_screen()
        else:
            self.clear_form()

    def add_and_return(self):
        self.add_transaction(return_to_main=True)

    def clear_form(self):
        self.date_entry.set_date(datetime.now())
        self.summary_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.memo_entry.delete(0, tk.END)

    def add_expense(self):
        self.create_expense_form()

    def create_expense_form(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        title_frame = tk.Frame(self.master, bg="blue", height=50)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="新增支出", font=("微軟正黑體", 20, "bold"), bg="blue", fg="white")
        title_label.pack(expand=True)

        form_frame = tk.Frame(self.master, bg="white")
        form_frame.pack(expand=True, padx=20, pady=20)

        tk.Label(form_frame, text="日期：", bg="white").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.date_entry = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="摘要：", bg="white").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.summary_entry = tk.Entry(form_frame)
        self.summary_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="金額：", bg="white").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.amount_entry = tk.Entry(form_frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="備註：", bg="white").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.memo_entry = tk.Entry(form_frame)
        self.memo_entry.grid(row=3, column=1, padx=5, pady=5)

        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="新增", command=lambda: self.add_transaction("expense")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="新增並返回", command=lambda: self.add_and_return("expense")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="清除", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="直接返回", command=self.create_main_screen).pack(side=tk.LEFT, padx=5)

    def add_transaction(self, category, return_to_main=False):
        date = self.date_entry.get_date()
        summary = self.summary_entry.get()
        amount = self.amount_entry.get()
        memo = self.memo_entry.get()

        if not all([date, summary, amount]):
            messagebox.showerror("錯誤", "請填寫所有必填欄位（日期、摘要、金額）")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("錯誤", "金額必須是數字")
            return

        # 將 date 轉換為 datetime 對象
        date_time = datetime.combine(date, datetime.min.time())

        transaction = {
            "user": self.current_user,
            "date": date_time,  # 使用轉換後的 datetime 對象
            "amount": amount,
            "category": category,
            "memo": memo
        }

        self.db.transaction.insert_one(transaction)
        messagebox.showinfo("成功", f"{'收入' if category == 'income' else '支出'}已新增")

        if return_to_main:
            self.create_main_screen()
        else:
            self.clear_form()

    def add_and_return(self, category):
        self.add_transaction(category, return_to_main=True)

    def view_transactions(self):
        self.create_view_transactions_screen()

    def create_view_transactions_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        title_frame = tk.Frame(self.master, bg="blue", height=50)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="瀏覽收支", font=("微軟正黑體", 20, "bold"), bg="blue", fg="white")
        title_label.pack(expand=True)

        filter_frame = tk.Frame(self.master, bg="white")
        filter_frame.pack(fill=tk.X, padx=20, pady=10)

        # 年份選擇
        tk.Label(filter_frame, text="年份：", bg="white").pack(side=tk.LEFT)
        self.year_var = tk.StringVar(value=str(datetime.now().year))
        year_menu = ttk.Combobox(filter_frame, textvariable=self.year_var, values=[str(year) for year in range(2020, datetime.now().year + 1)])
        year_menu.pack(side=tk.LEFT, padx=(0, 10))

        # 月份選擇
        tk.Label(filter_frame, text="月份：", bg="white").pack(side=tk.LEFT)
        self.month_var = tk.StringVar(value=str(datetime.now().month))
        month_menu = ttk.Combobox(filter_frame, textvariable=self.month_var, values=[str(month) for month in range(1, 13)])
        month_menu.pack(side=tk.LEFT, padx=(0, 10))

        # 類型選擇
        tk.Label(filter_frame, text="類型：", bg="white").pack(side=tk.LEFT)
        self.type_var = tk.StringVar(value="全部")
        type_menu = ttk.Combobox(filter_frame, textvariable=self.type_var, values=["全部", "收入", "支出"])
        type_menu.pack(side=tk.LEFT, padx=(0, 10))

        # 篩選按鈕
        filter_button = tk.Button(filter_frame, text="篩選", command=self.filter_transactions)
        filter_button.pack(side=tk.LEFT)

        # 結餘總計標籤
        self.balance_label = tk.Label(self.master, text="", font=("微軟正黑體", 14, "bold"), bg="white")
        self.balance_label.pack(pady=10)

        # 創建一個框架來容納交易列表和滾動條
        list_frame = tk.Frame(self.master)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 創建滾動條
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 創建交易列表
        self.transaction_list = ttk.Treeview(list_frame, yscrollcommand=scrollbar.set, columns=("日期", "摘要", "金額"), show="headings")
        self.transaction_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 設置列標題
        self.transaction_list.heading("日期", text="日期")
        self.transaction_list.heading("摘要", text="摘要")
        self.transaction_list.heading("金額", text="金額")

        # 設置列寬
        self.transaction_list.column("日期", width=100)
        self.transaction_list.column("摘要", width=300)
        self.transaction_list.column("金額", width=100)

        # 配置滾動條
        scrollbar.config(command=self.transaction_list.yview)

        # 綁定點擊事件
        self.transaction_list.bind('<ButtonRelease-1>', self.on_transaction_click)

        # 顯示初始數據
        self.filter_transactions()

        # 返回按鈕
        return_button = tk.Button(self.master, text="返回主畫面", command=self.create_main_screen, font=("微軟正黑體", 12))
        return_button.pack(pady=10)

    def filter_transactions(self):
        year = int(self.year_var.get())
        month = int(self.month_var.get())
        transaction_type = self.type_var.get()

        # 清空列表
        for item in self.transaction_list.get_children():
            self.transaction_list.delete(item)

        # 設置日期範圍
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)

        # 構建查詢條件
        query = {
            "user": self.current_user,
            "date": {"$gte": start_date, "$lte": end_date}
        }
        if transaction_type != "全部":
            query["category"] = "income" if transaction_type == "收入" else "expense"

        # 查詢交易記錄
        transactions = self.db.transaction.find(query).sort("date", 1)

        # 計算總金額
        total_amount = 0

        # 顯示交易記錄
        for transaction in transactions:
            amount = transaction["amount"]
            if transaction["category"] == "expense":
                amount = -amount
            total_amount += amount

            date_str = transaction["date"].strftime("%Y-%m-%d")
            amount_str = f"{amount:,.2f}"
            summary = transaction["memo"]

            # 設置顏色
            tag = "income" if amount >= 0 else "expense"

            # 插入到列表中
            self.transaction_list.insert("", "end", values=(date_str, summary, amount_str), tags=(tag,))

        # 設置標籤顏色
        self.transaction_list.tag_configure("income", foreground="green")
        self.transaction_list.tag_configure("expense", foreground="red")

        # 更新結餘總計標籤
        total_color = "green" if total_amount >= 0 else "red"
        self.balance_label.config(text=f"結餘總計: {total_amount:,.2f}", fg=total_color)

    def on_transaction_click(self, event):
        # 獲取點擊的項目
        item = self.transaction_list.selection()[0]
        values = self.transaction_list.item(item, "values")
        if values:
            if messagebox.askyesno("刪除確認", f"是否要刪除此記錄？\n{' | '.join(values)}"):
                # 從資料庫中刪除記錄
                date_str, summary, amount_str = values
                date = datetime.strptime(date_str, "%Y-%m-%d")
                amount = float(amount_str.replace(",", ""))
                
                query = {
                    "user": self.current_user,
                    "date": date,
                    "memo": summary,
                    "amount": abs(amount)
                }
                self.db.transaction.delete_one(query)
                
                # 重新加載交易記錄
                self.filter_transactions()

    def user_info(self):
        self.create_user_info_screen()

    def create_user_info_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        # 顯示用戶名稱
        username_label = tk.Label(self.master, text=self.current_user, font=("微軟正黑體", 24, "bold"), bg="white")
        username_label.pack(pady=10)

        # 標題
        title_frame = tk.Frame(self.master, bg="blue", height=50)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="用戶資訊", font=("微軟正黑體", 20, "bold"), bg="blue", fg="white")
        title_label.pack(expand=True)

        # 返回主畫面按鈕
        return_button = tk.Button(self.master, text="返回主畫面", command=self.create_main_screen, font=("微軟正黑體", 12))
        return_button.pack(pady=10)

        # 年份選擇
        current_year = datetime.now().year
        years = [str(year) for year in range(current_year, current_year-5, -1)]
        self.year_var = tk.StringVar(value=str(current_year))
        year_menu = ttk.Combobox(self.master, textvariable=self.year_var, values=years)
        year_menu.pack(pady=10)
        year_menu.bind("<<ComboboxSelected>>", self.update_user_info)

        # 創建左右區塊
        info_frame = tk.Frame(self.master)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 左側區塊
        left_frame = tk.Frame(info_frame, width=200)  # 設置固定寬度
        left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        left_frame.pack_propagate(False)  # 防止 frame 自動調整大小

        # 右側區塊
        right_frame = tk.Frame(info_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.balance_list = ttk.Treeview(left_frame, columns=("月份", "結餘"), show="headings")
        self.balance_list.heading("月份", text="月份")
        self.balance_list.heading("結餘", text="結餘")
        self.balance_list.pack(fill=tk.BOTH, expand=True)

        # 調整列寬
        self.balance_list.column("月份", width=70)
        self.balance_list.column("結餘", width=130)

        if self.fig:
            plt.close(self.fig)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))  # 增加圖表寬度
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update_user_info()

    def update_user_info(self, event=None):
        selected_year = int(self.year_var.get())
        monthly_balances = self.get_monthly_balances(selected_year)

        # 更新左側列表
        for item in self.balance_list.get_children():
            self.balance_list.delete(item)

        for month, balance in monthly_balances.items():
            self.balance_list.insert("", "end", values=(f"{month}月", f"{balance:.2f}"))

        # 更新右側圖表
        self.ax.clear()
        months = list(monthly_balances.keys())
        balances = list(monthly_balances.values())

        colors = ['green' if b >= 0 else 'red' for b in balances]
        self.ax.bar(months, balances, color=colors)
        self.ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        self.ax.set_title(f"{selected_year}年月度結餘", fontproperties=self.chinese_font)
        self.ax.set_xlabel("月份", fontproperties=self.chinese_font)
        self.ax.set_ylabel("結餘", fontproperties=self.chinese_font)

        # 設置 x 軸刻度標籤
        self.ax.set_xticks(months)
        self.ax.set_xticklabels([f"{m}月" for m in months], fontproperties=self.chinese_font)

        self.canvas.draw()

    def get_monthly_balances(self, year):
        monthly_balances = {month: 0 for month in range(1, 13)}

        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31, 23, 59, 59)

        transactions = self.db.transaction.find({
            "user": self.current_user,
            "date": {"$gte": start_date, "$lte": end_date}
        })

        for transaction in transactions:
            month = transaction["date"].month
            amount = transaction["amount"]
            if transaction["category"] == "expense":
                amount = -amount
            monthly_balances[month] += amount

        return monthly_balances

    def logout(self):
        self.current_user = None  # 清除當前用戶
        self.create_login_screen()

    def on_closing(self):
        if self.fig:
            plt.close(self.fig)
        self.master.quit()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AccountingApp(root)
    root.mainloop()