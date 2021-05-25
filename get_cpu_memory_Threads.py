# -*- coding:utf-8 -*-
import psutil
import time
import datetime
import os
import sys

'''
脚本简介：根据包名找到指定包的所有线程，打印出所有线程每秒cpu使用率，并计算平均数。

获取cpu逻辑：
psutil官方文档介绍：
When interval is 0.0 or None compares process times to system CPU 
times elapsed since last call, returning 
immediately. That means the first time this is called it will return a 
meaningless 0.0 value which you are supposed to ignore.

备注：所以可以对每个process object调用两回cpu_percent, 都用interval=None做参数. 
第一次相当于启动"秒表", 第二次相当于读取"秒表", 所有的调用都是即时返回的, 所以所得到的结果几乎是对同一时间断统计得到的.

'''
#######################################################################################
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓配置部分↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
#######################################################################################
# 进程包名
PACKAGE_NAME = ''
# 日志写入路径
PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
PATH = os.path.join(PATH, 'log_getCpu.txt')
# PATH = os.path.join(os.path.dirname(__file__), 'logs.txt')
# 定义一个进程列表
process_lst = []
# 存储进程pid和对应的cpu百分比
dicts_cpu = {}
dicts_memory = {}
# 旗标判断，用来判断是否退出运行
if_code = True


# 获取进程名为Python的进程对象列表,并添加到指定列表
def getProcess():
    '''
    根据包名找到该包名下的所有线程，并添加到列表
    :return: 进程列表process_lst
    '''
    # 获取当前系统所有进程id列表
    all_pid = psutil.pids()

    # 遍历所有进程，名称匹配的加入process_lst
    for pid in all_pid:
        p = psutil.Process(pid)
        if p.name() == PACKAGE_NAME:
            process_lst.append(p)
            # 匹配的pid加入dicts字典，用来计算平均数
            dicts_cpu[p.pid] = []

    # 未找到进程则返回False
    if not process_lst:
        return False
    return process_lst


def times():
    '''
    获取一个当前时间，作为开始启动的时间
    :return: startRun时间
    '''
    # 运行时间
    start_time = datetime.datetime.now().strftime('%H:%M:%S')
    return start_time


def get_cpu(times_data):
    '''
    获取cpu方法
    1、分2次获取cpu得出间隔时间内的cpu占用率
    2、间隔时间2秒，得出的cpu除以2，等于得出每秒占用率
    3、判断为False退出循环，判断线程丢失退出循环
    :param times_data:开始执行的时间
    :return:每次获取的cpu占用率进行return
    '''
    with open(PATH, 'a+') as f:  # 写入文件
        while True:
            info_lose = ''
            # 获取cpu利用率：
            for process_instance in process_lst:
                try:
                    process_instance.cpu_percent(interval=None)
                except psutil.NoSuchProcess as e:
                    info_lose += 'WARNING:{}\n'.format(e)  # 如果没有获取到打印警告
            # 间隔时间
            time.sleep(2)

            # 再次获取cpu利用率：因为cpu是要第一次和第二次获取时，中间时间的cpu使用率，不然都是获取的0
            for process_instance in process_lst:
                localtime = time.strftime('%H:%M:%S', time.localtime(time.time()))
                # 如果进程丢失没有获取到cpu，则抛出警告提示
                try:
                    cpu = process_instance.cpu_percent(interval=None)
                    # 获取的cpu除以间隔时间
                    cpu = cpu / 2

                    # cpu数据添加到dicts字典中，按pid进行存储
                    dicts_cpu[process_instance.pid].append(cpu)
                    cpu_data = 'INFO:Time:{p1}, PID:{p2}, Name:{p3}, CPU:{p4}%'. \
                        format(p1=localtime, p2=process_instance.pid, p3=PACKAGE_NAME, p4=cpu)
                    info_lose += cpu_data + '\n'
                except psutil.NoSuchProcess as e:
                    info_lose += 'WARNING:线程丢失 {}\n'.format(e)
                    process_lst.remove(process_instance)
                    info_lose += '删除线程：{}\n'.format(process_instance)

            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            time_info = '开始时间：{p2}    当前时间：{p1}  '.format(p1=current_time, p2=times_data)
            info_lose += str(time_info) + '\n'
            print(info_lose)
            f.write(info_lose)

            # 如果所有进程都丢失了，则退出循环
            if not process_lst:
                info_lose += '所有进程都丢失，无法获取cpu。结束运行！！！！！！！！！！'
                f.write(info_lose)
                break

            # 判断如果if_code等于False则退出循环
            if if_code is False:
                avg = if_exit()
                f.write(avg)
                break

            return info_lose


# 计算平均数
def if_exit(texts=''):
    '''
    计算cpu平均数
    1、for获取字典的key，定义一个counts变量用来计算总数（每次循环前将counts重置为0）
    2、第二个for获取指定key的value列表的所有参数，并相加->再除以参数个数->得出平均数
    3、将平均数添加到info_lose变量
    4、执行完成后进行return
    :param texts:预置字符串字段，用来输出提示信息的，如需要可进行调用
    :return:返回所有线程平均值
    '''
    info_lose = ''
    info_lose += texts + '\n'
    title = ' ' * len(dicts_cpu) + 'PID' + ' ' * len(dicts_cpu) + 'CPU平均值(数据总数)'
    info_lose += '-' * 80 + '\n' + '\n' + title + '\n'

    for k, v in dicts_cpu.items():
        counts = 0
        for i in range(len(v)):
            counts += v[i]
        counts = counts / len(v)
        text = ('{p1}{p2}{p3}{p4:.1f}%({p5})'.format
                (p1=' ' * len(dicts_cpu), p2=k, p3=' ' * (len(dicts_cpu) - len(str(k)) + 6),
                 p4=counts, p5=len(dicts_cpu[k])))
        info_lose += text + '\n'

    return info_lose
