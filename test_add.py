# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#
# import get_cpu_memory_Threads
#
# def add():
#     print('生成图片')
#     x_data = ['2011', '2012', '2013', '2014', '2015', '2016', '2017']
#     # cpu = [58000, 60200, 63000, 71000, 84000, 90500, 107000]
#     # memory = [52000, 54200, 51500, 58300, 56800, 59500, 62700]
#     #
#     # plt.plot(x_data, cpu, color='red', linewidth=2.0, linestyle='--')
#     # plt.plot(x_data, memory, color='blue', linewidth=3.0, linestyle='-.')
#     # plt.show()
#
#     print(get_cpu_memory_Threads.dicts_cpu)
#
#     number = [len(v) for k,v in get_cpu_memory_Threads.dicts_cpu.items()]
#     number = number[0]
#     # 所有线程的占用率加在一起，等于程序总占用，每次
#     list_cpu = []
#     for i in range(number):
#         cpu = 0
#         for k,v in get_cpu_memory_Threads.dicts_cpu.items():
#             # print(v[i])
#             cpu+=float(v[i])
#         list_cpu.append(cpu)
#     print(list_cpu)
#
#
#
#     plt.plot(list_cpu, color='red', linewidth=2.0, linestyle='--')
#     plt.show()
#
