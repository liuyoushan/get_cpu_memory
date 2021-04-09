import psutil
import time
import datetime

'''
脚本简介：
        根据包名找到对应包的所有线程，打印出所有线程的cpu使用率，并计算平均数。
        将cpu数据输出到指定文件。
        使用前先修改包名配置，以及运行时长
'''

# 进程名称
NAME = "chrome.exe"
# 日志写入路径
PATH = 'D:\logs\get_cpu_memory.txt'
# 运行时长，单位分钟，输入数字如(“1”等于1分钟,“0.1”等于60*0.1分钟）
NUMBER = 0.1

# 定义一个进程列表
process_lst = []
# 存储进程pid和对应的cpu百分比
dicts = {}


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
            dicts[p.pid] = []
    # 未找到进程则抛异常
    if not process_lst:
        raise Exception('The package name was not found in the system process. '
                        'Please verify that the program is started')
    return process_lst


def get_cpu(run_time):
    for i in process_lst:
        dicts[i.pid] = []
    # 运行时间
    start_time = datetime.datetime.now()
    end_times = (datetime.datetime.now() + datetime.timedelta(minutes=run_time)).strftime('%H:%M:%S')
    with open(PATH, 'w'):  # 清空文件
        pass
    while True:
        # # 获取内存利用率：
        # for process_instance in process_lst:
        #     print(process_instance.memory_percent())
        # ------------------------------------
        # 获取cpu利用率：
        for process_instance in process_lst:
            process_instance.cpu_percent(None)
        # 间隔时间
        time.sleep(2)
        # 再次获取cpu利用率：因为cpu是要第一次和第二次获取时，中间时间的cpu使用率，不然都是获取的0
        for process_instance in process_lst:
            cpu = process_instance.cpu_percent()
            localtime = time.strftime('%H:%M:%S', time.localtime(time.time()))

            # cpu添加到dicts字典中，按pid进行存储
            dicts[process_instance.pid].append(cpu)

            cpu_data = 'Time:{p1}, PID:{p2}, Name:{p3}, CPU:{p4}%'.format \
                (p1=localtime, p2=process_instance.pid, p3=NAME, p4=cpu)
            print(cpu_data)
            with open(PATH, 'a+') as f:  # 写入文件
                f.write(str(cpu_data) + '\n')

        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        # print('当前时间：{}  运行结束时间：{}'.format(current_time, end_times))
        # 如果时间到了则退出，并计算平均数
        if current_time == end_times:
            end_info = 'StartTime：{}, CurrentTime：{}, EndTime：{}'. \
                format(start_time.strftime('%H:%M:%S'), current_time, end_times)
            title = ' ' * len(dicts) + 'PID' + ' ' * len(dicts) + 'CPU平均值(总进程数)'
            cpu_count_avg = '-'*80 + '\n' + end_info + '\n' + title + '\n'
            # 计算cpu平均数

            for i in dicts:
                counts = (dicts[i][0] + dicts[i][-1]) / len(dicts[i])
                e = ('{p1}{p2}{p3}{p4:.1f}%({p5})'.format
                     (p1=' '*len(dicts), p2=i, p3=' '*(len(dicts)-len(str(i))+3), p4=counts, p5=len(dicts[i])))
                cpu_count_avg += e + '\n'
            print(cpu_count_avg)
            with open(PATH, 'a+') as f:  # 写入文件
                f.write(cpu_count_avg)
            break


if __name__ == '__main__':
    getProcess(NAME)
    get_cpu(NUMBER)
