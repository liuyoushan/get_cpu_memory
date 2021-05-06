# -*- coding:utf-8 -*-
import psutil
import time
import datetime


'''
脚本简介：
        根据包名找到指定包的所有线程，打印出所有线程的cpu使用率，并计算平均数。
'''
#######################################################################################
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓配置部分↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
#######################################################################################
# 进程包名
PACKAGE_NAME = ''
# 日志写入路径
PATH = 'D:\logs\get_cpu_memory.txt'

# 定义一个进程列表
process_lst = []
# 存储进程pid和对应的cpu百分比
dicts_cpu = {}
dicts_memory = {}
# 旗标判断，用来判断是否退出运行
if_code = True


# 获取进程名为Python的进程对象列表,并添加到指定列表
def getProcess():
    # 获取当前系统所有进程id列表
    all_pid = psutil.pids()

    # 遍历所有进程，名称匹配的加入process_lst
    for pid in all_pid:
        p = psutil.Process(pid)
        if p.name() == PACKAGE_NAME:
            process_lst.append(p)
            # 匹配的pid加入dicts字典，用来计算平均数
            dicts_cpu[p.pid] = []

    # 未找到进程则抛异常
    if not process_lst:
        return False
    return process_lst

def times():
    # 运行时间
    start_time = datetime.datetime.now().strftime('%H:%M:%S')
    return start_time

def get_cpu(timess):
    # for i in process_lst:
    #     dicts_cpu[i.pid] = []

    with open(PATH, 'w'):  # 清空文件
        pass

    with open(PATH, 'a+') as f:  # 写入文件
        while True:
            info_lose = ''
            # 获取cpu利用率：
            for process_instance in process_lst:
                try:
                    process_instance.cpu_percent(None)
                except psutil.NoSuchProcess as e:
                    info_lose += 'WARNING:{}\n'.format(e)  # 如果没有获取到打印警告
            # 间隔时间
            time.sleep(2)

            # 再次获取cpu利用率：因为cpu是要第一次和第二次获取时，中间时间的cpu使用率，不然都是获取的0
            for process_instance in process_lst:
                try:
                    cpu = process_instance.cpu_percent()
                    cpus = cpu / 2
                except psutil.NoSuchProcess as e:
                    cpus = None
                    info_lose += 'WARNING:{}\n'.format(e)
                    # print(info_lose)

                localtime = time.strftime('%H:%M:%S', time.localtime(time.time()))

                if cpus != None:
                    # cpu数据添加到dicts字典中，按pid进行存储
                    dicts_cpu[process_instance.pid].append(cpus)

                    cpu_data = 'INFO:Time:{p1}, PID:{p2}, Name:{p3}, CPU:{p4}%'. \
                        format(p1=localtime, p2=process_instance.pid, p3=PACKAGE_NAME, p4=cpus)
                    info_lose += cpu_data + '\n'
            print(info_lose)

            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            timess = '开始时间：{p2}    当前时间：{p1}  '.format(p1=current_time, p2=timess)
            info_lose += str(timess) + '\n'

            if if_code == False:
                avg_count = if_exit()
                info_lose += str(avg_count)
                break
            return info_lose

# 计算平均数
def if_exit():
    info_lose = ''
    title = ' ' * len(dicts_cpu) + 'PID' + ' ' * len(dicts_cpu) + 'CPU平均值(数据总数)'
    info_lose += '-' * 80 + '\n'  + '\n' + title + '\n'
    '''
    计算cpu平均数
    1、for获取字典的key
    2、第二个for获取对应value列表的所有参数，并相加->再除以参数个数->得出平均数
    3、每次循环后counts都重置为0
    '''
    for i in dicts_cpu:
        counts = 0
        for j in range(len(dicts_cpu[i])):
            counts = dicts_cpu[i][j] + counts
        counts = counts / len(dicts_cpu[i])
        text = ('{p1}{p2}{p3}{p4:.1f}%({p5})'.format
             (p1=' ' * len(dicts_cpu), p2=i, p3=' ' * (len(dicts_cpu)+3 - len(str(i)) + 3), p4=counts,
              p5=len(dicts_cpu[i])))
        info_lose += text + '\n'
    return info_lose



