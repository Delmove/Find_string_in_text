import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def search_string_in_files(folder_path, file_extension, search_string):
    results = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(file_extension):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    for line_number, line in enumerate(file, 1):
                        if search_string in line:
                            results.append((file_path, line_number, line.strip()))
    return results

def on_search_button_click():
    folder_path = entry_path.get() or r"D:\公司系统\Daily reports"
    file_extension = entry_extension.get() or ".txt"
    search_string = entry_search.get()

    search_results = search_string_in_files(folder_path, file_extension, search_string)

    if search_results:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "包含字符串的文件和行：\n")
        for result in search_results:
            result_text.insert(tk.END, f"文件：{result[0]}，行数：{result[1]}，内容：{result[2]}\n")
        result_text.config(state=tk.DISABLED)
    else:
        messagebox.showinfo("查询结果", "未在文件中找到指定字符串。")

# 创建主窗口
root = tk.Tk()
root.title("文本查询工具")

# 设置窗口不可调整大小
root.resizable(False, False)

# 创建并布局组件
style = ttk.Style()

# 设置按钮的外观
style.configure("TButton", padding=5, relief="flat", background="#ccc", borderwidth=0)
style.map("TButton", background=[("active", "#ddd")])

# 设置输入框的外观
style.configure("TEntry", padding=5, relief="flat")

label_path = ttk.Label(root, text="文件夹路径：")
label_path.grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_path = ttk.Entry(root, style="TEntry")
entry_path.grid(row=0, column=1, columnspan=2, sticky="we", padx=5, pady=5)

label_extension = ttk.Label(root, text="文件后缀：")
label_extension.grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_extension = ttk.Entry(root, style="TEntry")
entry_extension.grid(row=1, column=1, columnspan=2, sticky="we", padx=5, pady=5)

label_search = ttk.Label(root, text="查询字符串：")
label_search.grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_search = ttk.Entry(root, style="TEntry")
entry_search.grid(row=2, column=1, columnspan=2, sticky="we", padx=5, pady=5)

search_button = ttk.Button(root, text="开始查询", command=on_search_button_click, style="TButton")
search_button.grid(row=3, column=0, columnspan=3, pady=10)

result_text = tk.Text(root, height=10, width=50, state=tk.DISABLED)
result_text.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

# 启动主循环
root.mainloop()
