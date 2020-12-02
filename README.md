# 2020_Python_Homework
现代程序设计技术作业

### Week2：文本分析任务

运行main.py函数即可，

在通过修改路径可以选择导入的文本，同时需要指定语言

在run函数中可以指定是否需要绘制云图、柱状图等系列分析操作；

也可以直接通过读取`Distance<...>.xlsx`文件来导入`DisM`，从而进行重心句子的寻找及聚类操作



### Week3：微博情感分析

运行code文件夹下main.py函数即可

为了提升速度，在关键时候将运行结果保留

`df_emo_tag = pd.read_excel("../data/emo_tag_data.xlsx", header=0)`可代替其上情感分析任务

`df_emo_plc_tag = pd.read_excel("../data/plc_emo_tag_data.xlsx", header=0)`可直接用于空间动态可视化

以下函数根据需求可以选择是否进行可视化展示

| 函数                          | 可视化结果                 |
| ----------------------------- | -------------------------- |
| time_plot(Freqs)              | 情感-时间分布柱状图        |
| place_plot_1(df_emo_tag)      | 情感-空间分布散点图        |
| place_plot_2(df_emo_tag)      | 特定时间内北京地图情感分布 |
| place_plot_3(df_emo_plc_tag)  | 聚类结果展示               |
| dynamic_place(df_emo_plc_tag) | timeline动态可视化         |

### Week5：演艺圈网络分析





### Week6：通信簿类

+ **类**提供两种英文查找方式：`search` 及 `hash_sort` ;一种中文查找方式`chinese_sort` 

  在主函数中可以通过`search_all`将所有的元素全部搜索一遍，从而计算搜索时间，给出搜索效率

+ `random_tel` 和 `random_mail` 是为了保证随机过后的数据尽可能拟合真实情况（且都保持11位从而便于比较）



### Week7：图片过滤操作

运行`ImageShop.py`

+ 首先创建一个测试类，例如`T = TestImageShop("jpg","../images/batch4")`，可以指定参数分别为图片的格式和图片`batch`的路径
+ 指定展示参数及相关过滤操作，如`T.test(3,3,9,("Contour",None),("Blur",None),("Sharpen",None),("ShapeAdj",(600,450)))`，前三个数字分别代表：展示结构为行3张，列3张，最多显示9章；随后可以指定需要进行的过滤操作。其中改变大小需要指定参数，其余不用。



### Week8：CO2排放数据分析

运行`CO2.py`

+ 在代码中解除相关内容的注释可以进行相应的操作，操作介绍在每段注释的头部



### Week9：关系显示装饰器

+ 相关文件信息

` RelationNetwork.py`：用于实现文本关系可视化的类，提供`lazy_vis`外函数构建闭包，实现一次导入，多次利用的功能，实例化的函数由`vis`定义

`main.py`

+ 装饰器的使用

  **进度条**：引入tqdm包，直接运行`main.py`

  **时间管理**：在`main.py`中打开`@profile`装饰器，同时关闭`RelationNetwork.py`中的内存管理装饰器`@profile`，在命令行中运行` kernprof -l -v main.py`

  **内存管理**：关闭`main.py`中的`@profile`装饰器，同时打开`RelationNetwork.py`中的内存管理装饰器`@profile`，直接运行`main.py`

  **声音装饰器**：`@sound`装饰器，直接运行`main.py`

  检查装饰器：`@check_file`，直接运行`main.py`



### Week10：



### Week11：

remote: error: GH001: Large files detected. You may want to try Git Large File Storage - https://git-lfs.github.com.
remote: error: Trace: 2527381d7933e120c521d62f21eaa4439684613abf692fe6e357c8d2480022e7
remote: error: See http://git.io/iEPt8g for more information.
remote: error: File Week11/report/Week11 适配器模式.assets/snow.gif is 140.76 MB; this exceeds GitHub's file size limit of 100.00 MB
remote: error: File Week11/report/Week11 适配器模式.assets/test_mini.gif is 145.65 MB; this exceeds GitHub's file size limit of 100.00 MB
To https://github.com/zhuangjiaheng/2020_Python_Homework.git
 ! [remote rejected] master -> master (pre-receive hook declined)
error: failed to push some refs to 'https://github.com/zhuangjiaheng/2020_Python_Homework.git'

两个gif文件几个比较大的文件上传失败

解决方案：创建.gitignore文件，把文件放进去