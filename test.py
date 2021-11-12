import tkinter as tk
from tkinter import *


class DialogueCreation(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.xbar = tk.Scrollbar(parent, orient=HORIZONTAL)
        self.xbar.pack(side=BOTTOM, fill=X)

        self.ybar = tk.Scrollbar(parent)
        self.ybar.pack(side=RIGHT, fill=Y)



        self.item_canvas = tk.Canvas(parent, width=5000, height=5000, xscrollcommand=self.xbar.set, yscrollcommand=self.ybar.set)
        self.item_canvas.pack(side=LEFT, expand=FALSE, fill=None)
        self.item_canvas.configure(background='black')
        w = tk.Label(self.item_canvas, text="程序包名：")
        w.place(x=20, y=10)

if __name__ == '__main__':
    root = tk.Tk()
    DialogueCreation(root)
    root.title("Editor")
    root.mainloop()

# 设置日志框Y轴滚动条
self.scrollBar = ttk.Scrollbar(root)
self.scrollBar.pack(side=LEFT, fill="y")
# Text（文本）组件用于显示和处理多行文本
self.text = tk.Text(root, height=80, width=135, bd=1, relief="solid", bg='#5f9ea0',
                    yscrollcommand=self.scrollBar.set, maxundo=1)
self.text.pack(side="left", fill="y", padx=10, pady=42)
# 垂直滚动条绑定text
self.scrollBar.config(command=self.text.yview)