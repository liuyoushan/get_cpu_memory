import tkinter as tk
from tkinter import *
from tkinter import ttk
import get_cpu_memory_Threads
import threading
import queue


class GUI():
    def __init__(self, root):
        # new 一个Quue用于保存输出内容
        self.msg_queue = queue.Queue()
        self.initGUI(root)

    # 在show_msg方法里，从Queue取出元素，输出到Text
    def show_msg(self):
        while not self.msg_queue.empty():
            content = self.msg_queue.get()
            if content == None:
                # print('self.msg_queue.get 为空')
                break
            self.text.insert("insert", content)
            # 保持焦点在行尾
            self.text.see("end")
        # after方法再次调用show_msg
        self.root.after(100, self.show_msg)

    def initGUI(self, root):
        self.root = root
        self.root.title("获取cpu占用率工具")
        self.root.geometry("800x600")
        self.root.resizable = False

        w = tk.Label(self.root, text="包名：")
        w.pack(side=TOP)

        self.E1 = Entry(self.root, bd=5, bg='white')
        self.E1.pack(side=TOP)

        # 运行按钮
        self.btn = ttk.Button(self.root, text="运行", takefocus=0, command=self.show)
        self.btn.pack(side=TOP)

        # 结束运行按钮
        self.btn = ttk.Button(self.root, text="结束运行", takefocus=0, command=self.end_threads)
        self.btn.pack(side=TOP)

        # 设置滚动条
        self.scrollBar = ttk.Scrollbar(self.root)
        self.scrollBar.pack(side="right", fill="y")

        # Text（文本）组件用于显示和处理多行文本
        self.text = tk.Text(self.root, height=50, bd=1, relief="solid",
                            yscrollcommand=self.scrollBar.set)
        logPrint = ('⬇'*40)+'日志打印'+('⬇'*40)
        self.text.insert("insert", 'Tips：\n1、请先填写包名，如：chrome.exe\n2、点击【结束运行】可获取平均值！！\n'+'\n'+logPrint+'\n')

        def deletes():
            self.text.delete(0.0, tk.END)

        # 清空按钮
        self.btn = ttk.Button(self.root, text="清空", takefocus=0, command=deletes)
        self.btn.pack(side=TOP)

        self.text.pack(side="top", fill="both", padx=10, pady=10)
        # # 垂直滚动条绑定text
        self.scrollBar.config(command=self.text.yview)

        # 启动after方法
        # 定时任务，规定时间内持续执行
        self.root.after(100, self.show_msg)

        # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示
        root.mainloop()

    def __show(self):
        while True:
            d = get_cpu_memory_Threads.get_cpu()
            self.msg_queue.put(d)
            # 判断停止后则输出平均数
            if get_cpu_memory_Threads.if_code == False:
                avg_count = get_cpu_memory_Threads.if_exit()
                self.msg_queue.put(avg_count)
                print(avg_count)
            if not d:
                # print('为空')
                break

    def show(self):
        # 修改get_cpu_memory_Threads文件的packname属性（执行的包名）
        get_cpu_memory_Threads.PACKAGE_NAME = str(self.E1.get())
        # 点击运行重置旗标判断的属性为True
        get_cpu_memory_Threads.if_code = True
        # 先清空process_lst列表
        get_cpu_memory_Threads.process_lst = []
        # 调用getProcess获取进程列表
        getprocess = get_cpu_memory_Threads.getProcess()

        if getprocess == False:
            Error = 'ERROR:Package name({}) not found, please confirm whether the program has started'.format(
                get_cpu_memory_Threads.PACKAGE_NAME)
            self.text.insert("insert", '\n' + Error + '\n')
        else:
            # 创建一个线程运行
            T = threading.Thread(target=self.__show, args=())
            T.start()

    def end_threads(self):
        # 点击结束运行将code设置为False
        get_cpu_memory_Threads.if_code = False


if __name__ == "__main__":
    root = tk.Tk()
    myGUI = GUI(root)
