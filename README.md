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