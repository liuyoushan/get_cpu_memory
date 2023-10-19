
简介：获取PC端进程cpu、内存，并计算平均值
------------------------
示例：
![图片](https://user-images.githubusercontent.com/74752752/136493071-c76b102f-e5a8-40fc-adfa-76080312ca65.png)



实现逻辑：



![10453545-f55ed0a177988c76](https://user-images.githubusercontent.com/74752752/128282191-d8d5e930-6284-4ef9-818d-6ca0dea32dbe.png)



















简书地址：https://www.jianshu.com/p/feb479089d82


获取某一进程的CPU使用率的计算方法，轮子传送门：
https://blog.csdn.net/Hubz131/article/details/94414013?utm_medium=distribute.pc_relevant_download.none-task-blog-2~default~BlogCommendFromBaidu~default-3.nonecase&depth_1-utm_source=distribute.pc_relevant_download.none-task-blog-2~default~BlogCommendFromBaidu~default-3.nonecas

其他问题记录：
1、需要安装numpy，注意需要和python版本对应的包。否则运行报错（ from matplotlib._path import (ImportError: DLL load failed: 找不到指定的模块。）
    下载连接：https://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
2、注意matplotlib 和numpy版本需要对应，不然报错（RuntimeError: implement_array_function method already has a docstring）
我安装的是，numpy=1.17.0 , matplotlib==3.0.3 , python3.7.0

打包参考：https://www.jianshu.com/p/ae85d2ed7a6e
如果打包报错，可能需要手动导入 hiddenimports=['numpy.random.common', 'numpy.random.bounded_integers', 'numpy.random.entropy'],
再次打包试试：pyinstaller **.spec