import time
import threading
import queue

import tkinter as tk
import tkinter.messagebox  # 弹出对话框
from tkinter import *
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import get_cpu_memory_Threads
import _plt


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

            # 为了实现强制杀死进程的代码
            # if self.root.state() == 'normal' and get_cpu_memory_Threads.ck_==False:
            #     get_cpu_memory_Threads.ck_ = True

            if content is not None:
                self.tag_name = "color-"  # 您需要为每种颜色使用唯一的标记名
                self.text.tag_config(self.tag_name, foreground='white')  # 标记的颜色字体设置成白色
                # 在最后一行插入内容
                self.text.insert(END, content, self.tag_name)

                # 获取日志控件光标当前的X、Y所在位置
                current_row = self.text.index(INSERT)
                # 切割字符串，获取Y行数
                current_row = current_row.split('.')
                current_row = int(current_row[0])
                # 获取日志控件的总行数
                end_row = self.text.index('end')
                # 判断当前行>(总行数-35)=即在倒数第35行以上时，就执行保持焦点在行尾
                if current_row > (float(end_row) - 35):
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
                print('队列为空，停止打印')
                break

        # 再次调用show_msg
        self.root.after(100, self.show_msg)

    def initGUI(self, root):
        '''
        1、tkinter主页面布局
        2、按钮、输入框、日志文本框等所有控件
        3、ps：定时任务：定时(100毫秒)调用show_msg方法，相当于监控吧
        :param root:将调用的库tk.Tk()，变量给root了
        '''
        self.root = root
        root.title("PC端程序监控")
        root.geometry("1000x600")
        root.resizable = False  # 是否可调整大小

        f = tk.Menu(root)
        root['menu'] = f
        f2 = tkinter.Menu(f)
        f2.add_command(label='空的别看了')
        f.add_cascade(label='主页面', menu=root)  # 创建顶级菜单栏，并关联子菜单
        f.add_cascade(label='编辑', menu=f2)
        f.add_cascade(label='关于')

        w = tk.Label(root, text="程序包名：")
        w.place(x=20, y=10)

        # 输入框设置默认值
        addr = tkinter.StringVar()
        addr.set('firefox.exe')
        self.E1 = Entry(root, bd=2, bg='white', textvariable=addr)
        self.E1.place(x=80, y=10)

        _tips = tk.Label(root, text="PS：鼠标焦点切换到底部可以自动滚动")
        # _tips.place(x=10, y=560)
        _tips.place(relx=0.03, rely=0.96)

        def _tips():
            tips = '功能简介：\n1、监控程序资源利用率\n2、运行结束自动计算平均值\n' \
                   '3、查看曲线图\n4、logPATH：工具同级目录下'
            tkinter.messagebox.showinfo("提示", tips)

        self.tips = Button(root, text=' ? ', command=_tips,
                           bg='white', width=0, height=0, font=('Helvetica', '8'))
        self.tips.place(x=226, y=10)

        # 开始运行按钮
        self.btn_start = Button(root, text="开始运行", takefocus=0, command=self.show,
                                bg='blue', fg='white', width=8, height=0, font=('Helvetica', '10'))
        self.btn_start.place(x=260, y=10)

        # 结束运行按钮
        self.btn = Button(root, text="结束运行", takefocus=0, command=self.end_threads,
                          bg='#FFB6C1', fg='white', width=8, height=0, font=('Helvetica', '10'))
        self.btn.place(x=790, y=10)

        # 清空text控件内容
        def deletes():
            # self.text.edit_undo()
            self.text.delete('1.0', tk.END)

        # 清空按钮
        self.btn = Button(root, text="清空日志框", takefocus=0, command=deletes,
                          bg='#FFB6C1', fg='white', width=8, height=0, font=('Helvetica', '10'))
        self.btn.place(x=880, y=10)

        # 生成趋势图
        self.btn4 = Button(root, text="查看趋势图", takefocus=0, command=self.plt_if,
                           bg='blue', fg='white', width=8, height=0, font=('Helvetica', '10'))
        self.btn4.place(x=350, y=10)

        # 设置日志框Y轴滚动条
        self.scrollBar = ttk.Scrollbar(root)
        self.scrollBar.pack(side=LEFT, fill="y")
        # Text（文本）组件用于显示和处理多行文本
        self.text = tk.Text(root, height=80, width=135, bd=1, relief="solid", bg='#5f9ea0',
                            yscrollcommand=self.scrollBar.set, maxundo=1)
        self.text.pack(side="left", fill="y", padx=10, pady=42)
        # 垂直滚动条绑定text
        self.scrollBar.config(command=self.text.yview)

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

    # 点击开始运行按钮触发此函数，初始化数据
    def show(self):
        # 调用队列方法
        self.show_msg()
        '''
        点击运行按钮后调用此方法
        1、点击运行时初始化一些配置数据
        2、调用getProcess根据包名获取进程列表
        3、判断getProcess，线程存在则开启一个线程来运行，未找到则抛异常
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
        # 程序总占用数据清空
        get_cpu_memory_Threads.count_cpu = []
        get_cpu_memory_Threads.count_memory = []
        get_cpu_memory_Threads.count_memoryRSS = []
        # 首次点击运行时清空log文件
        with open(get_cpu_memory_Threads.PATH, 'w'):
            print('log文件已清空')
        # ⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆初始化⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆⬆

        # 调用getProcess根据包名获取进程列表
        get_cpu_memory_Threads.getProcess()
        if get_cpu_memory_Threads.process_lst:
            # 创建一个线程运行
            t = threading.Thread(target=self.__show, args=())
            # 设置线程为守护线程，防止退出主线程时，子线程仍在运行
            t.setDaemon(True)
            t.start()
            # 设置为不可点击
            self.btn_start['state'] = DISABLED
        else:
            error = 'ERROR:Package name({}) not found, please confirm whether the program has started' \
                .format(get_cpu_memory_Threads.PACKAGE_NAME)
            tkinter.messagebox.showinfo("提示", error)

    def end_threads(self):
        '''
        结束运行后状态变更
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

    # 创建画布显示趋势图
    def plt_if(self):
        try:
            self.top.destroy()
            print('删除旧子窗口')
        except:
            pass
        plts = _plt.creat_plt().plt()
        if plts is not False:
            # 创建一个子窗口
            self.top = Toplevel()
            self.top.title('趋势图')
            self.top.geometry("800x500")
            # 子窗口创建画布
            self.canvs = FigureCanvasTkAgg(plts, self.top)
            self.canvs.draw()
            print('成功创建画布')
            # 显示画布
            # self.canvs.get_tk_widget().place(relx=0.56, rely=0.07)
            self.canvs.get_tk_widget().pack(side=LEFT)
            # 按钮设置为不可点击
            self.btn4['state'] = DISABLED
            # # 修改画布的图片
            self.update_canvas()
        else:
            tkinter.messagebox.showinfo("提示", '画布创建失败!!\n需先开始运行')

    '''这里就牛b了，解决了一个plt报错问题。
    error日志：（invalid command name "1671000502536show_msg"     while executing "1671000502536show_msg"     ("after" script)）
    问题原因：当直接关闭主页面窗口后，进程无法停止。
    问题分析：当我把plt图片清除后，发现未复现此问题。
            分析可能因为plt里面还存在生成的图片，但控件载体已销毁无法显示，则弹出报错，进程无法停止，
            导致程序窗口也无法关闭。
    解决方案：调用完plt图片并显示到画布后，直接去清除掉plt的图片，这样即可以解决报错问题，还能释放内存。
    解决的问题：
    主要解决了2个问题
    1、清图释放内存，如果不释放会重复创建并且保存到程序内存里面，导致内存泄漏
    2、解决plt图片报错问题无法关闭进程问题
    '''

    # 修改画布的图片
    def update_canvas(self):
        try:
            plts = _plt.creat_plt().plt()
            self.canvs.figure = plts  # 修改画布的图片
            self.canvs.draw()
            # 清图，就是上面备注里面说的东西
            _plt.plt.clf()
            _plt.plt.cla()
            _plt.plt.close("all")
        except Exception as e:
            # print('曲线图生成失败！！ERROR:{}'.format(e))
            tkinter.messagebox.showinfo("提示", '曲线图生成失败！！ERROR:{}'.format(e))
        # self.canvs.get_tk_widget().place(relx=0, rely=0.07)
        # 判断趋势图按钮的状态是否为“disabled”，and判断窗口是否存在。
        if self.btn4['state'] == 'disabled' and self.top.winfo_exists():
            # 存在，after循环运行此方法更新图片
            self.root.after(1500, self.update_canvas)
        else:
            # 不存在，修改"查看趋势图"按钮状态为”可点击“状态
            self.btn4['state'] = NORMAL


if __name__ == "__main__":
    root = tk.Tk()
    myGUI = GUI(root)
