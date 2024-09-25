import tkinter as tk
from tkinter import simpledialog

def get_number():
    # 創建一個 Toplevel 彈出視窗
    popup = tk.Toplevel(root)
    popup.title("輸入一個數字")

    # 要求輸入數字的標籤
    label = tk.Label(popup, text="請輸入一個數字：")
    label.pack(pady=10)

    # 用於獲取用戶輸入的 Entry 小部件
    number_entry = tk.Entry(popup)
    number_entry.pack(pady=5)

    # 處理用戶點擊"確定"或按下 Enter 鍵的函數
    def submit():
        try:
            number = int(number_entry.get())  # 將輸入轉換為整數
            print(f"您輸入的是：{number}")
            popup.destroy()  # 提交後關閉彈出視窗
        except ValueError:
            error_label.config(text="請輸入有效的數字")

    # 提交輸入的按鈕
    submit_button = tk.Button(popup, text="確定", command=submit)
    submit_button.pack(pady=5)

    # 顯示錯誤訊息的標籤（如果輸入不是數字）
    error_label = tk.Label(popup, text="", fg="red")
    error_label.pack()

    # 綁定 Enter 鍵到 submit 函數
    number_entry.bind('<Return>', lambda event: submit())

# 主視窗
root = tk.Tk()
root.geometry("300x200")

# 觸發彈出視窗的按鈕
btn = tk.Button(root, text="獲取數字", command=get_number)
btn.pack(pady=50)

root.mainloop()
