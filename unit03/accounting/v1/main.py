import tkinter as tk
from tkinter import messagebox, font
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class AccountingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("個人記帳程式")
        self.master.geometry("800x500")
        self.master.configure(bg="white")

        self.conn = "mongodb://admin:mymdb$1234@localhost:27017"
        self.client = None
        self.db = None

        self.setup_database()
        self.create_login_screen()

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
        messagebox.showinfo("功能", "新增收入")

    def add_expense(self):
        messagebox.showinfo("功能", "新增支出")

    def view_transactions(self):
        messagebox.showinfo("功能", "瀏覽收支")

    def user_info(self):
        messagebox.showinfo("功能", "用戶資訊")

    def logout(self):
        self.create_login_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = AccountingApp(root)
    root.mainloop()