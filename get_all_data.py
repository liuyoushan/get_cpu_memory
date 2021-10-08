import psutil, time

_timer = getattr(time, 'monotonic', time.time)
num_cpus = psutil.cpu_count() or 1
def timer():
    return _timer() * num_cpus


pid_cpuinfo = {}


def GetProcessCPU_Pre(id):
    p = psutil.Process(id)
    pt = p.cpu_times()
    st1, pt1_0, pt1_1 = timer(), pt.user, pt.system  # new
    st0, pt0_0, pt0_1 = pid_cpuinfo.get(id, (0, 0, 0))  # old

    delta_proc = (pt1_0 - pt0_0) + (pt1_1 - pt0_1)
    delta_time = st1 - st0
    try:
        cpus_percent = ((delta_proc / delta_time) * 100)
    except:
        cpus_percent = 0.0

    pid_cpuinfo[id] = [st1, pt1_0, pt1_1]
    return "{:.2f}".format(cpus_percent)


def GetProcessMEMORY(process_instance):
    memorys = process_instance.memory_percent()
    return "{:.2f}".format(memorys)


def GetProcessMEMORY_RSS(process_instance):
    memory_rss = process_instance.memory_info().rss / 1024 / 1024 / 1024
    return "{:.3f}".format(memory_rss)

def GetProcessDISK(process_instance):
    disk=process_instance.io_counters()
    print(disk)

    d = psutil.net_io_counters()
    ins = d.bytes_recv
    insb = d.bytes_sent
    print(ins,insb)
    return disk