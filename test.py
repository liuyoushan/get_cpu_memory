# # -*- coding:utf-8 -*-
# import psutil
# import time
# import datetime
# import os
# import sys
#
# import get_all_data
#
#
# # 进程包名
# PACKAGE_NAME = 'firefox.exe'
#
# # 定义一个进程列表
# process_lst = []
# # 存储进程pid和对应的数据
# dicts_cpu = {}
# dicts_memory = {}
# dicts_memory_rss = {}
#
#
#
# # 获取进程名为Python的进程对象列表,并添加到指定列表
# def getProcess():
#     '''
#     根据包名找到该包名下的所有线程，并添加到列表
#     :return: 进程列表process_lst
#     '''
#     # 获取当前系统所有进程id列表
#     all_pid = psutil.pids()
#
#     # 遍历所有进程，名称匹配的加入process_lst
#     for pid in all_pid:
#         p = psutil.Process(pid)
#         if p.name() == PACKAGE_NAME:
#             process_lst.append(p)
#             # 匹配的pid加入dicts字典，用来计算平均数
#             dicts_cpu[p.pid] = []
#             dicts_memory[p.pid] = []
#             dicts_memory_rss[p.pid] = []
#
#     # 未找到进程则返回False
#     if not process_lst:
#         return False
#     return process_lst
#
#
#
#
#
# def get_cpu():
#     '''
#     获取cpu方法
#     1、分2次获取cpu得出间隔时间内的cpu占用率
#     2、间隔时间2秒，得出的cpu除以2，等于得出每秒占用率
#     3、判断为False退出循环，判断线程丢失退出循环
#     :param times_data:开始执行的时间
#     :return:每次获取的cpu占用率进行return
#     '''
#     numb = 0
#     while True:
#         info_lose = ''
#         # # 获取cpu利用率：
#         # for process_instance in process_lst:
#         #     try:
#         #         process_instance.cpu_percent(None)
#         #     except psutil.NoSuchProcess as e:
#         #         info_lose = 'WARNING:{}\n'.format(e)
#         # # 间隔时间
#         # time.sleep(1)
#
#         # 再次获取cpu利用率：因为cpu是要第一次和第二次获取时，中间时间的cpu使用率，不然都是获取的0
#         # 获取cpu内存利用率
#         aaa=[]
#         aaa.append(process_lst[6])
#         print(aaa)
#         for q in aaa:
#             aa = q.cpu_percent(interval=None)
#         time.sleep(1)
#         for q in aaa:
#             aa = q.cpu_percent(interval=None)
#             print(q.pid,aa)
#
#         # for process_instance in process_lst:
#         #
#         #     # 获取cpu，计算cpu占用率
#         #     cpu = process_instance.cpu_percent(interval=1)
#         #     # print(cpu)
#         #     # 获取内存利用率
#         #     memorys = get_all_data.GetProcessMEMORY(process_instance)
#         #     # 获取rss内存消耗
#         #     memory_rss = get_all_data.GetProcessMEMORY_RSS(process_instance)
#         #
#         #     # 内存利用率添加到dicts字典中，按pid进行存储
#         #     dicts_memory[process_instance.pid].append(memorys)
#         #     # 内存rss数据添加到字典中，按pid进行存储
#         #     dicts_memory_rss[process_instance.pid].append(memory_rss)
#         #     # cpu数据添加到dicts字典中，按pid进行存储
#         #     dicts_cpu[process_instance.pid].append(cpu)
#         #
#         #
#         #     localtime = time.strftime('%H:%M:%S', time.localtime(time.time()))
#         #     # 整合显示数据
#         #     cpu_data = 'INFO:Time:{p1}, PID:{p2}, Name:{p3}, CPU:{p4}%, Memory/rss:{p5}%/{p6}GB, disk:{p7}, network:{p8}' \
#         #         .format(p1=localtime, p2=process_instance.pid, p3=PACKAGE_NAME, p4=cpu, p5=memorys,
#         #                 p6=memory_rss, p7='', p8='')
#         #     info_lose += cpu_data + '\n'
#         #     # print(cpu_data)
#         # print('-'*50)
#
# print('start')
# getProcess()
# # print(process_lst)
# get_cpu()
