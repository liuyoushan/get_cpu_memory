import time
import threading
import queue

import tkinter as tk
import tkinter.messagebox  # 弹出对话框
from tkinter import *
from tkinter import ttk

import matplotlib.pyplot as plt  # 图片生成
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import get_cpu_memory_Threads


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
                # 在最后一行插入内容
                self.text.insert(END, content)
                # 获取日志控件光标当前的X、Y所在位置
                current_row = self.text.index(INSERT)
                # 切割字符串，获取Y行数
                current_row = current_row.split('.')
                current_row = int(current_row[0])
                # 获取日志控件的总行数
                end_row = self.text.index('end')
                # 判断当前行>(总行数-35)=在倒数第35行以上时，就执行保持焦点在行尾
                if current_row > float(end_row) - 35:
                    # 移动光标到最底部
                    self.text.mark_set('insert', END)
                    # 保持焦点在行尾
                    self.text.see(END)

                # 判断滚动条位置这个方法，由于获取的滚动条参数不准确，故实现效果较差。弃用
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
        # _tips.place(x=10, y=560)
        _tips.place(relx=0.01, rely=0.96)

        # 开始运行按钮
        self.btn_start = Button(self.root, text="开始", takefocus=0, command=self.show,
                                bg='green', width=8, height=0, font=('Helvetica', '10'))
        self.btn_start.place(x=550, y=10)

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

        # 生成趋势图
        # self.btn4 = Button(self.root, text="生成趋势图", takefocus=0, command=test_add.add,
        #                   width=8, height=0, font=('Helvetica', '10'))
        self.btn4 = Button(self.root, text="查看趋势图", takefocus=0, command=self.plt_if,
                           width=8, height=0, font=('Helvetica', '10'))
        self.btn4.place(x=830, y=10)

        # 设置滚动条
        self.scrollBar = ttk.Scrollbar(self.root)
        self.scrollBar.pack(side="right", fill="y")

        # Text（文本）组件用于显示和处理多行文本
        self.text = tk.Text(self.root, height=80, width=135, bd=1, relief="solid", bg='PaleGreen',
                            yscrollcommand=self.scrollBar.set)
        logPrint = ('⬇' * 40) + '日志打印' + ('⬇' * 40)
        self.text.insert("insert", 'Tips：\n'
                                   '     1、填写包名后运行，如：firefox.exe\n'
                                   '     2、点击【结束运行】自动计算平均值\n'
                                   '     3、日志保存路径：运行程序同级目录下\n\n'
                         + '\n' + logPrint + '\n')

        self.text.pack(side="left", fill="y", padx=10, pady=42)

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
        # 判断按钮状态,避免重复运行
        # ⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆初始化⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆
        # 将在输入框控件（E1）获取的包名赋值给PACKAGE_NAME变量（执行的包名）
        get_cpu_memory_Threads.PACKAGE_NAME = str(self.E1.get())
        # 点击运行重置旗标判断的属性为True（用来判断是否结束运行的属性）
        get_cpu_memory_Threads.if_code = True
        # 每次点击运行要先清空process_lst列表
        get_cpu_memory_Threads.process_lst = []
        # 清空存储进程pid和对应的数据
        get_cpu_memory_Threads.dicts_cpu = {}
        get_cpu_memory_Threads.dicts_memory = {}
        get_cpu_memory_Threads.dicts_memory_rss = {}
        # 首次点击运行时清空log文件
        with open(get_cpu_memory_Threads.PATH, 'w'):
            print('log文件已清空')
        # ⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆初始化⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆

        # 调用getProcess根据包名获取进程列表
        get_cpu_memory_Threads.getProcess()
        if get_cpu_memory_Threads.process_lst:
            # 创建一个线程运行
            t = threading.Thread(target=self.__show, args=())
            t.start()
            # 设置为不可点击
            self.btn_start['state'] = DISABLED
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
            # 设置为False，get_cpu等判断为False则会自动停止
            get_cpu_memory_Threads.if_code = False
            # 按钮状态恢复可以点击
            self.btn4['state'] = NORMAL
            self.btn_start['state'] = NORMAL

    def plt_if(self):
        plts = self.plt()
        if plts is not False:
            # 创建画布
            self.canvs = FigureCanvasTkAgg(plts, self.root)
            self.canvs.draw()
            print('成功创建画布')
            # 显示画布
            self.canvs.get_tk_widget().place(relx=0.56, rely=0.07)

            # 按钮设置为不可点击
            self.btn4['state'] = DISABLED
            # 修改画布的图片
            self.update_canvas()
        else:
            tkinter.messagebox.showinfo("提示", '图片生成失败!!\n请先运行程序')

    # 修改画布的图片
    def update_canvas(self):
        self.canvs.figure = self.plt()
        self.canvs.draw()
        # self.canvs.get_tk_widget().place(relx=0, rely=0.07)
        if self.btn4['state'] == 'disabled':
            self.root.after(1000, self.update_canvas)

    # 创建图
    def plt(self):
        # 清图释放内存，如果不释放会重复创建并且保存到程序内存里面，导致内存泄漏。
        plt.clf()
        plt.cla()
        plt.close("all")

        cpu = get_cpu_memory_Threads.dicts_cpu
        memory = get_cpu_memory_Threads.dicts_memory
        memory_rss = get_cpu_memory_Threads.dicts_memory_rss
        if cpu and memory and memory_rss:
            list_cpu = self.plt_count(cpu)
            list_memory = self.plt_count(memory)
            list_rss = self.plt_count(memory_rss)
            try:
                fig = plt.figure()
                # fig = plt.figure(dpi=50,figsize=(30,8)) # 设置图片大小
                # 第一张图片
                plt.subplot(211, facecolor='#FFDAB9')  # 设置图片面板底色
                plt.subplots_adjust(wspace=0, hspace=0.4)  # 调整2张图间距
                plt.title('Cpu(%) Mem(%)')
                plt.ylabel(' Data value ')
                plt.plot(list_cpu, color='red', label='Cpu%', linewidth=1.5, linestyle='-')
                plt.legend()  # 加这个才能显示label
                plt.plot(list_memory, color='blue', label='Mem%', linewidth=1.5, linestyle='-')
                plt.legend()
                # 第二张图片
                plt.subplot(212, facecolor='#FFDAB9')
                plt.title('Mem_rss(GB)')
                plt.xlabel(' Running time ')
                plt.ylabel(' Data value ')
                plt.plot(list_rss, color='red', label='Rss(GB)', linewidth=2.0, linestyle='--')
                plt.legend()
                # plt.savefig('资源监控趋势图.png') # 当前目录下生成图片
                # plt.show()  # 在编译器里面生成
                return fig
            except Exception as e:
                print(e)
                # tkinter.messagebox.showinfo("提示", '图片生成失败，error：{}'.format(e))
                return False
        else:
            return False

    # 计算所有线程的数据，线程数据相加一起等于程序总占用(制作图片用的)
    def plt_count(self, resources_number):
        # 获取到数据量的总条数
        number = [len(v) for k, v in resources_number.items()]
        # 所有线程的占用率加在一起，等于程序总占用，每次
        _list = []
        for i in range(number[0]):
            _count = 0
            for k, v in resources_number.items():
                # print(v[i])
                _count += float(v[i])
            _list.append(_count)
        # print(_list)
        return _list


if __name__ == "__main__":
    root = tk.Tk()
    myGUI = GUI(root)
