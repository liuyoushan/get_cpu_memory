# -*- coding:utf-8 -*-
import psutil
import time
import datetime
import os
import sys

import get_all_data

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
PATH = os.path.join(PATH, 'log_getCM.txt')
# PATH = os.path.join(os.path.dirname(__file__), 'logs.txt')
# 定义一个进程列表
process_lst = []
# 存储进程pid和对应的数据
dicts_cpu = {}
dicts_memory = {}
dicts_memory_rss = {}
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
            dicts_memory[p.pid] = []
            dicts_memory_rss[p.pid] = []

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
            # 判断如果if_code等于False则退出循环
            if if_code is False:
                f.write(get_avg())
                break
            info_lose = ''

            # 获取cpu内存利用率
            for process_instance in process_lst:
                localtime = time.strftime('%H:%M:%S', time.localtime(time.time()))
                try:
                    # 获取cpu，计算cpu占用率
                    cpu = get_all_data.GetProcessCPU_Pre(process_instance.pid)
                    # 获取内存利用率
                    memorys = get_all_data.GetProcessMEMORY(process_instance)
                    # 获取rss内存消耗
                    memory_rss = get_all_data.GetProcessMEMORY_RSS(process_instance)

                    # 内存利用率添加到dicts字典中，按pid进行存储
                    dicts_memory[process_instance.pid].append(memorys)
                    # 内存rss数据添加到字典中，按pid进行存储
                    dicts_memory_rss[process_instance.pid].append(memory_rss)
                    # cpu数据添加到dicts字典中，按pid进行存储
                    dicts_cpu[process_instance.pid].append(cpu)

                    # 整合显示数据
                    cpu_data = 'INFO:Time:{p1}, PID:{p2}, Name:{p3}, CPU:{p4}%, Memory/rss:{p5}%/{p6}GB, disk:{p7}, network:{p8}' \
                        .format(p1=localtime, p2=process_instance.pid, p3=PACKAGE_NAME, p4=cpu, p5=memorys,
                                p6=memory_rss, p7='', p8='')
                    info_lose += cpu_data + '\n'

                except psutil.NoSuchProcess as e:
                    info_lose += 'WARNING:线程丢失 {}\n'.format(e)
                    process_lst.remove(process_instance)
                    info_lose += '删除线程：{}\n'.format(process_instance)

            time.sleep(1)  # 1秒获取一次数据
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            info_lose += str('开始时间：{p2}    当前时间：{p1}  '.format(p1=current_time, p2=times_data)) + '\n'
            # print(info_lose)
            f.write(info_lose)

            # 如果所有进程都丢失了，则退出循环
            if not process_lst:
                info_lose += '所有进程都丢失，无法获取cpu。结束运行！！！！！！！！！！'
                f.write(info_lose)
                break

            return info_lose


def count_avg(number):
    '''
    计算cpu平均数
    1、for获取字典的key，定义一个counts变量用来计算总数（每次循环前将counts重置为0）
    2、第二个for获取指定key的value列表的所有参数，并相加->再除以参数个数->得出平均数
    3、将平均数添加到info_lose变量
    4、执行完成后进行return
    :param texts:预置字符串字段，用来输出提示信息的，如需要可进行调用
    :return:返回所有线程平均值
    '''
    counts = []  # 计算出来的平均值
    thread = []  # 对应的线程
    data_count = 0  # 数据总数

    for k, v in number.items():
        n = 0
        for i in range(len(v)):
            n += float(v[i])
        n = n / len(v)
        counts.append(n)
        thread.append(k)
        if data_count == 0:
            data_count += len(number[k])

    return counts, thread, data_count


def get_avg():
    '''
    数据整合
    :return: 返回整理好的平均值
    '''
    avg_cpu = count_avg(dicts_cpu)
    avg_memory = count_avg(dicts_memory)
    avg_memory_rss = count_avg(dicts_memory_rss)

    info_lose = '运行结束！！！' + '\n'
    info_lose += ('-' * 40) + ' E N D ' + ('-' * 40) + '\n'
    info_lose += '各线程平均值：' + '\n'
    info_lose += ' ' * 5 + 'PID' + ' ' * 5 + 'CPU(计算数)' + ' ' * 5 + 'Memory利用率/RSS消耗(计算数)' \
                 + ' ' * 5 + 'disk' + ' ' * 5 + 'network' + '\n'
    for i in range(len(avg_cpu[0])):
        space = ' ' * (13 - len(str(avg_cpu[1][i])))
        info_lose += ('{p1}{p2}{p3}{p4:.2f}%({p5}){p8}{p6:.2f}% / {p7:.4f}GB({p9})\n'.format
                      (p1=' ' * 4, p2=avg_cpu[1][i], p3=space, p4=avg_cpu[0][i], p5=avg_cpu[2],
                       p6=avg_memory[0][i], p7=avg_memory_rss[0][i], p8=' ' * 10,
                       p9=avg_memory[2]))

    # 所有线程的平均数相加，计算出这个程序占用的资源
    cpu, memory, rss = 0, 0, 0
    for c, m, r in zip(avg_cpu[0], avg_memory[0], avg_memory_rss[0]):
        cpu += c
        memory += m
        rss += r
    info_lose += '程序总占用平均值：' + '\n'
    info_lose += '             CPU:{:.2f}%     Memory:{:.2f}%     RSS:{:.4f}GB'.format(cpu, memory, rss)

    return info_lose
