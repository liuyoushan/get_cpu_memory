from pyecharts import Line
import datetime
current_time = datetime.datetime.now().strftime('%H:%M:%S')

# //设置行名
columns = ["00:00", "", '00:01', '', "00:02", '', "00:03", '', "00:04", '', "00:05", current_time]
# //设置数据
data1 = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
data2 = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]

line = Line("折线图","一年的降水量与蒸发量")
# //is_label_show是设置上方数据是否显示
line.add("CPU占用率", columns, data1, is_label_show=True)
line.render()