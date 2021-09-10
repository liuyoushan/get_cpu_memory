import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
import get_cpu_memory_Threads
import threading
import queue
import tkinter.messagebox  # 弹出对话框


class GUI():
    def __init__(self, root):
        # 初始化一个属性值
        self.numb = 0
        # new 一个Quue用于保存输出内容
        self.msg_queue = queue.Queue()
        # 将initGUI方法放到初始化方法里面，调用类的时候默认执行
        self.initGUI(root)

    # 在show_msg方法里，从Queue取出元素，输出到Text
    def show_msg(self):
        '''
        1、队列不为None则执行循环
        2、去get队列里面的内容并输出到日志文本框
        :return:
        '''
        while not self.msg_queue.empty():
            content = self.msg_queue.get()
            if content is not None:

                self.text.insert(END, content)
                # 在倒数第30行以上时，就执行保持焦点在行尾
                current_row = self.text.index(INSERT)
                current_row = current_row.split('.')
                current_row = int(current_row[0])
                end_row = self.text.index('end')
                if current_row > float(end_row) - 40:
                    # 移动光标到最底部
                    self.text.mark_set('insert', END)
                    # 保持焦点在行尾
                    self.text.see(END)

                # # 获取滚动条的Y轴位置（范围0.0~1.0），如果大于0.98就保持焦点在行尾
                # scrollBar_Y = self.scrollBar.get()
                # if scrollBar_Y[0] > 0.98:
                #     # print('在最底部：{}'.format(scrollBar_Y[0]))
                #     # # 保持焦点在行尾
                #     self.text.see(END)
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
        self.root.title("PC端程序监控")
        self.root.geometry("1000x600")
        self.root.resizable = False

        w = tk.Label(self.root, text="程序包名：")
        w.place(x=10, y=10)

        # 输入框设置默认值
        addr = tkinter.StringVar()
        addr.set('firefox.exe')
        self.E1 = Entry(self.root, bd=2, bg='white', textvariable=addr)
        self.E1.place(x=70, y=10)

        _tips = tk.Label(self.root, text="PS：鼠标焦点切换到底部可以自动滚动")
        _tips.place(x=10, y=560)

        # 运行按钮
        self.btn = Button(self.root, text="开始", takefocus=0, command=self.show,
                          bg='green', width=8, height=0, font=('Helvetica', '10'))
        self.btn.place(x=550, y=10)

        # 结束运行按钮
        self.btn = Button(self.root, text="结束", takefocus=0, command=self.end_threads,
                          bg='red', width=8, height=0, font=('Helvetica', '10'))
        self.btn.place(x=640, y=10)

        # 清空text控件内容
        def deletes():
            self.text.delete(0.0, tk.END)

        # 清空按钮
        self.btn = Button(self.root, text="清空内容", takefocus=0, command=deletes,
                          width=8, height=0, font=('Helvetica', '10'))
        self.btn.place(x=730, y=10)

        # 设置滚动条
        self.scrollBar = ttk.Scrollbar(self.root)
        self.scrollBar.pack(side="right", fill="y")

        # Text（文本）组件用于显示和处理多行文本
        self.text = tk.Text(self.root, height=50, width=110, bd=1, relief="solid", bg='PaleGreen',
                            yscrollcommand=self.scrollBar.set)
        logPrint = ('⬇' * 40) + '日志打印' + ('⬇' * 40)
        self.text.insert("insert", 'Tips：\n'
                                   '     1、填写包名后运行，如：firefox.exe\n'
                                   '     2、点击【结束运行】自动计算平均值\n'
                                   '     3、日志保存路径：运行程序同级目录下\n\n'
                         + '\n' + logPrint + '\n')

        self.text.pack(side="top", fill="both", padx=10, pady=50)
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
        2、写个死循环去获取cpu等数据
        3、判断有数据将添加到msg_queue队列，无数据为None时，则计算平均数。并退出循环
        '''
        time_data = get_cpu_memory_Threads.times()
        while True:
            d = get_cpu_memory_Threads.get_cpu(time_data)
            # 判断get_cpu，如已停止则计算平均数
            if d is not None:
                # 将数据写入队列
                self.msg_queue.put(d)
            else:
                time.sleep(1)
                avg = get_cpu_memory_Threads.get_avg()
                print(avg)
                self.msg_queue.put(avg)
                break

    # 初始化数据
    def show(self):
        '''
        点击运行按钮后调用此方法
        1、点击运行时初始化一些配置数据
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
        get_cpu_memory_Threads.getProcess()

        # 首次点击运行时清空log文件
        if self.numb < 1:
            with open(get_cpu_memory_Threads.PATH, 'w'):
                print('log文件已清空')
            self.numb += 1

        if get_cpu_memory_Threads.process_lst:
            # 创建一个线程运行
            t = threading.Thread(target=self.__show, args=())
            t.start()
        else:
            error = 'ERROR:Package name({}) not found, please confirm whether the program has started' \
                .format(get_cpu_memory_Threads.PACKAGE_NAME)
            self.text.insert("insert", '\n' + error + '\n')

    def end_threads(self):
        '''
        点击结束运行将code设置为False
        :return:
        '''
        # 确认框
        a = tkinter.messagebox.askokcancel('提示', '要执行此操作吗？')
        if a:
            get_cpu_memory_Threads.if_code = False


if __name__ == "__main__":
    root = tk.Tk()
    myGUI = GUI(root)
