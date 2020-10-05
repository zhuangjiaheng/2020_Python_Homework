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

