import tkinter as tk
from tkinter import filedialog

# Create the main window
root = tk.Tk()
root.title("File Open UI Example")

# Function to open the file dialog
def open_file():
    file_path = filedialog.askopenfilename(
        title="Open a file",
        filetypes=[("商品資料檔案", "*.csv")]
    )
    if file_path:
        print(f"File selected: {file_path}")

# Create a button that triggers the file open dialog
open_button = tk.Button(root, text="Open File", command=open_file)
open_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
