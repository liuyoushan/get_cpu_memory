import matplotlib.pyplot as plt  # 图片生成
import get_cpu_memory_Threads


class creat_plt:
    # def __init__(self):
    #     self.fig = plt.figure()

    # 创建图
    def plt(self):
        '''

        :return: 返回figure生成的图片
        '''


        count_cpu = get_cpu_memory_Threads.count_cpu
        count_memory = get_cpu_memory_Threads.count_memory
        count_memoryRSS = get_cpu_memory_Threads.count_memoryRSS
        if count_cpu and count_memory and count_memoryRSS:
            try:
                # # 清图释放内存，如果不释放会重复创建并且保存到程序内存里面，导致内存泄漏。
                # plt.clf()
                # plt.cla()
                # plt.close("all")
                fig = plt.figure()
                # self.fig = plt.figure()
                # fig = plt.figure(dpi=50,figsize=(30,8)) # 设置图片大小
                # 第一张图片
                plt.subplot(211, facecolor='#FFDAB9')  # 设置图片面板底色
                plt.subplots_adjust(wspace=0, hspace=0.4)  # 调整2张图间距
                plt.title('Cpu(%) Mem(%)')
                plt.ylabel(' Data value ')
                plt.plot(count_cpu, color='red', label='Cpu%', linewidth=1.5, linestyle='-')
                plt.legend()  # 加这个才能显示label
                plt.plot(count_memory, color='blue', label='Mem%', linewidth=1.5, linestyle='-')
                plt.legend()
                # 第二张图片
                plt.subplot(212, facecolor='#FFDAB9')
                plt.title('Mem_rss(GB)')
                plt.xlabel(' Running time ')
                plt.ylabel(' Data value ')
                plt.plot(count_memoryRSS, color='red', label='Rss(GB)', linewidth=2.0, linestyle='--')
                plt.legend()
                # plt.savefig('资源监控趋势图.png') # 当前目录下生成图片
                # plt.show()  # 打开一个窗口显示图片
                return fig
            except Exception as e:
                print(e)
                # tkinter.messagebox.showinfo("提示", '图片生成失败，error：{}'.format(e))
                return False
        else:
            return False



    # # 计算所有线程的数据，线程数据相加一起等于程序总占用(制作图片用的)
    # def plt_count(self, resources_number):
    #     # 获取到数据量的总条数
    #     number = [len(v) for k, v in resources_number.items()]
    #     # 所有线程的占用率加在一起，等于程序总占用，每次
    #     _list = []
    #     for i in range(number[0]):
    #         _count = 0
    #         for k, v in resources_number.items():
    #             # print(v[i])
    #             _count += float(v[i])
    #         _list.append(_count)
    #     # print(_list)
    #     # print('---------------------------------------')
    #     return _list
