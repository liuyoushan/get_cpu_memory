# -*- coding:utf-8 -*-
import psutil
import time
import datetime

'''
脚本简介：
        根据包名找到指定包的所有线程，打印出所有线程的cpu使用率，并计算平均数。
        将cpu数据输出到指定文件。
        使用前先修改包名配置，以及运行时长
'''
#######################################################################################
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓配置部分↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
#######################################################################################
# 进程包名
PACKAGE_NAME = "firefox.exe"
# 运行时长，单位分钟，输入数字如(“1”等于1分钟,“0.1”等于60*0.1分钟）
RUN_TIME = 0.1
# 日志写入路径
PATH = 'D:\logs\get_cpu_memory.txt'

# 定义一个进程列表
process_lst = []
# 存储进程pid和对应的cpu百分比
dicts_cpu = {}
dicts_memory = {}


# 获取进程名为Python的进程对象列表,并添加到指定列表
def getProcess(pName):
    # 获取当前系统所有进程id列表
    all_pid = psutil.pids()

    # 遍历所有进程，名称匹配的加入process_lst
    for pid in all_pid:
        p = psutil.Process(pid)
        if p.name() == pName:
            process_lst.append(p)
            # 匹配的pid加入dicts字典，用来计算平均数
            dicts_cpu[p.pid] = []
            dicts_memory[p.pid] = []

    # 未找到进程则抛异常
    if not process_lst:
        raise Exception("Package name({}) not found, please confirm whether the program has started".
                        format(PACKAGE_NAME))
    return process_lst

if __name__ == '__main__':
    e=getProcess(PACKAGE_NAME)
    for i in range(len(process_lst)):
      print('{p2}的内存使用：{p1:.4f} GB'.format(p1=process_lst[i].memory_info().rss / 1024 / 1024 / 1024, p2=process_lst[i].pid))



