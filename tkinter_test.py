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
        # 将initGUI方法放到初始化方法里面，调用类的时候默认执行
        self.initGUI(root)

    # 在show_msg方法里，从Queue取出元素，输出到Text
    def show_msg(self):
        '''
        1、队列不为空则执行循环
        2、去get队列里面的内容并输出到日志文本框
        :return:
        '''
        while not self.msg_queue.empty():
            content = self.msg_queue.get()
            if content != None:
                self.text.insert("insert", content)
                # 保持焦点在行尾
                self.text.see("end")
            else:
                # print('self.msg_queue.get 为空')
                break

        # after方法再次调用show_msg
        self.root.after(100, self.show_msg)

    def initGUI(self, root):
        '''
        1、tkinter主页面布局
        2、按钮、输入框、日志文本框等所有控件
        3、ps：定时任务：after，定时(100毫秒)调用show_msg方法，相当于监控吧
        :param root:将调用的库tk.Tk()，变量给root了
        '''
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
        self.text = tk.Text(self.root, height=50, bd=1, relief="solid", bg='PaleGreen',
                            yscrollcommand=self.scrollBar.set)
        logPrint = ('⬇' * 40) + '日志打印' + ('⬇' * 40)
        self.text.insert("insert", 'Tips：\n'
                                   '     1、请先填写包名，如：chrome.exe\n'
                                   '     2、点击【结束运行】可获取平均值\n\n'
                                   '工具作用：\n'
                                   '     1、获取指定程序每秒占用cpu的百分比\n'
                         + '\n' + logPrint + '\n')

        # 清空text控件内容
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
        '''
        1、调用get_cpu方法并传入当前时间
        2、写个死循环去获取cpu数据
        3、判断有cpu数据将添加到msg_queue队列，无数据为None时，则计算平均数。并退出循环
        '''
        Time = get_cpu_memory_Threads.times()
        while True:
            d = get_cpu_memory_Threads.get_cpu(Time)
            # 判断get_cpu已停止则计算平均数
            if d != None:
                self.msg_queue.put(d)
            else:
                avg_count = get_cpu_memory_Threads.if_exit()
                self.msg_queue.put(avg_count)
                print(avg_count)
                break

    def show(self):
        '''
        点击运行按钮后调用此方法
        1、点击运行时重置一些配置数据
        2、调用getProcess根据包名获取进程列表
        3、判断getProcess，找到线程则开启一个线程来运行，未找到则抛异常
        '''
        # 将在输入框控件（E1）获取的包名赋值给PACKAGE_NAME变量（执行的包名）
        get_cpu_memory_Threads.PACKAGE_NAME = str(self.E1.get())
        # 点击运行重置旗标判断的属性为True（用来判断是否结束运行的属性）
        get_cpu_memory_Threads.if_code = True
        # 每次点击运行要先清空process_lst列表
        get_cpu_memory_Threads.process_lst = []
        # 调用getProcess根据包名获取进程列表
        getprocess = get_cpu_memory_Threads.getProcess()

        if getprocess:
            # 创建一个线程运行
            T = threading.Thread(target=self.__show, args=())
            T.start()
        else:
            Error = 'ERROR:Package name({}) not found, please confirm whether the program has started' \
                .format(get_cpu_memory_Threads.PACKAGE_NAME)
            self.text.insert("insert", '\n' + Error + '\n')

    def end_threads(self):
        '''
        点击结束运行将code设置为False
        :return:
        '''
        get_cpu_memory_Threads.if_code = False


if __name__ == "__main__":
    root = tk.Tk()
    myGUI = GUI(root)
