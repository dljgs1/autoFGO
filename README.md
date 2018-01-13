# autoFGO
自动抽池子，基于adb。
adb工具已经在目录下，无需安装

使用说明：
- 1 搭建python3环境，需要的库有opencv，numpy，scipy，PIL等
- 2 连接手机，开启USB调试模式
- 3 运行getpic.py 进入图像搜集，对关键图像区域进行查找，按w调整方框大小，按s存储位置，按p存储图像
- 4 运行action.py 进入脚本运行。

注意：不同的手机屏幕其坐标点可能不同，需要自己调整，坐标点均在save.txt中。

