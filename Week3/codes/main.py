#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: main.py
#@Software: PyCharm


import numpy as np
import pandas as pd
import jieba
import re
import matplotlib.pyplot as plt
import math
import folium
from sklearn.cluster import KMeans
from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 100)


def tokenize(text_string):
    '''
    strip the url and split the text

    :param text_string: A string with url
    :return: A split_list
    '''
    results = re.compile(r'http://[a-zA-Z0-9.?/&=:]*', re.S)
    text_string = results.sub("", text_string)
    token_list = jieba.lcut(text_string)
    return token_list

def load_dict():
    '''
    load the dictionary of the emotion_word

    :return:5 dictionary saving angry;disgust;fear;joy;sadness
    '''
    with open("../data/emotion_lexicon/anger.txt",encoding="UTF-8") as d1:
        d1 = d1.read().splitlines()   #is a way to read the word without '\n'
    with open("../data/emotion_lexicon/disgust.txt",encoding="UTF-8") as d2:
        d2 = d2.read().splitlines()
    with open("../data/emotion_lexicon/fear.txt",encoding="UTF-8") as d3:
        d3 = d3.read().splitlines()
    with open("../data/emotion_lexicon/joy.txt",encoding="UTF-8") as d4:
        d4 = d4.read().splitlines()
    with open("../data/emotion_lexicon/sadness.txt",encoding="UTF-8") as d5:
        d5 = d5.read().splitlines()
    return d1,d2,d3,d4,d5

def emo_num(df):
    '''
    classify the emotion based on the dict and the split_text in df

    :param df: A dataframe including text,place,time
    :return: A dataframe with new attributes [emotion tag]
    '''
    d1, d2, d3, d4, d5 = load_dict()
    df['angry']=0;df['disgust']=0;df['fear']=0;
    df['joy']=0;df['sadness']=0
    #df['tag'] = []
    for index,row in df.iterrows():
        # print(row)
        #print(getattr(row, 'Text'))  # get the element by the column
        tempCnt = [0,0,0,0,0]
        for word in getattr(row,'Text'):
            if word in d1:tempCnt[0] += 1
            elif word in d2:tempCnt[1] += 1
            elif word in d3:tempCnt[2] += 1
            elif word in d4:tempCnt[3] += 1
            elif word in d5:tempCnt[4] += 1

        # 0:Text 1:Long 2:Lati 3:Time
        # 4:angry 5:disgust 6:fear 7:joy 8:sadness
        df.iloc[index, 4] = tempCnt[0]
        df.iloc[index, 5] = tempCnt[1]
        df.iloc[index, 6] = tempCnt[2]
        df.iloc[index, 7] = tempCnt[3]
        df.iloc[index, 8] = tempCnt[4]

    return df

def load_func(df):
    '''
    load the emo_classify function

    :param df: A dataframe with count of each emotion
    :return: emo_classify function
    '''
    df['pangry']=0;df['pdisgust']=0;df['pfear']=0;
    df['pjoy']=0;df['psadness']=0;df['tag']=''
    def emo_classify(pattern):
        '''
        classify the emotions and label it with tag

        :param pattern:choose the way of tools: mixed ot unique
        :return: A dataframe with full information
        '''
        nonlocal df
        for index, row in df.iterrows():
            tempCnt = list(row[['angry', 'disgust','fear','joy','sadness']])
            # print(tempCnt)
            if pattern == 'mixed':
                percent = lambda tempCnt: [tempCnt[i]/sum(tempCnt) if sum(tempCnt)>0
                                           else 0 for i in range(5)]
                pct_list = percent(tempCnt)
                # 9:pangry 10:pdisgust 11:pfear 12:pjoy 13:psadness
                df.iloc[index, 9] = pct_list[0]
                df.iloc[index, 10] = pct_list[1]
                df.iloc[index, 11] = pct_list[2]
                df.iloc[index, 12] = pct_list[3]
                df.iloc[index, 13] = pct_list[4]
            elif pattern == 'unique':
                # 14:tag
                emo_list = ['angry', 'disgust','fear','joy','sadness','others','mixed']
                tempM = max(tempCnt)
                if tempM == 0 : Id=5
                elif tempCnt.count(tempM) >= 2: Id=6
                else : Id = tempCnt.index(tempM)
                df.iloc[index,14] = emo_list[Id]
        return df
    return emo_classify

def save_df(df,name="default_name"):
    '''
    save the dataframe

    :param df: a dataframe
    :return: a xlsx in "../data"
    '''
    writer = pd.ExcelWriter('../data/{:}.xlsx'.format(name))  # 写入Excel文件
    df.to_excel(writer, 'page_1')              # ‘page_1’是写入excel的sheet名
    writer.save()
    writer.close()
    print("DataFrame Already Saved!")

def time(df):
    '''
    analyize the text~time

    :param df:a dataframe
    :return:2d list Percent with Counts of emotion split by hours
    '''
    df_tag_time = df[['Time','angry', 'disgust','fear','joy','sadness',
                      'tag']].sort_values("Time",inplace=False)
                    #inplace=False表示不修改df,仅返回
    #print(df_tag_time)
    time_interval = ['08 {:}:00:00'.format(str(i).zfill(2)) for i in range(24)]
    time_interval.append('09 00:00:00')
    Counts = [[0 for i in range(5)] for i in range(len(time_interval))]
    Freqs = [[0 for i in range(5)] for i in range(len(time_interval))]
    #print(time_interval)

    for index,row in df_tag_time.iterrows():
        temp_time = row['Time'][-11:]   #string of time,which can be compared directly
        temp_emo = list(row[['angry', 'disgust','fear','joy','sadness']])

        for i in range(len(time_interval)-1):
            if time_interval[i] <= temp_time < time_interval[i+1]:
                for j in range(5):
                    Counts[i][j] += temp_emo[j]
        if temp_time >= time_interval[len(time_interval)-1]:
            for j in range(5):
                Counts[len(time_interval)-1][j] += temp_emo[j]

    percent = lambda tempCnt: [round(tempCnt[i] / sum(tempCnt),4) if sum(tempCnt) > 0
                               else 0 for i in range(5)]
    for i in range(len(Counts)):
        Freqs[i] = percent(Counts[i])
    return Counts,Freqs

def build_stack(Counts_trans):
    '''
    calculate the bottom of each layer of the stack

    :param Freqs: transposed,5x25
    :return:A 2d list, used by layer2-4
    '''
    d=np.zeros((5,25))
    for i in range(len(Counts_trans)):
        for j in range(len(Counts_trans[0])):
            if i != 0:
                d[i][j] = d[i-1][j] + Counts_trans[i-1][j]
        print("i=",i,d)
    return d

def time_plot(Counts):
    '''
    plot the result of text~time

    :param Counts: 2d list Frequency of emotion split by hours
    :return:
    '''
    Counts_trans = [[row[i] for row in Counts] for i in range(5)]
    print(Counts_trans)
    #set the plot
    fig = plt.figure(figsize=(12, 5))

    #set the title
    plt.title('Five Emotions on Weibo During a Day')

    #set the axis-x
    N = 25
    ind = np.arange(N)
    x_tpl = ['08d-{:}h'.format(str(i).zfill(2)) for i in range(N)]
    x_tpl=tuple(x_tpl)
    plt.xticks(ind, x_tpl,rotation=30)

    #set the axis-y
    plt.yticks(np.arange(0, 1, 0.1))  # 0到81 间隔20
    plt.ylabel('percentage')

    #build the stack
    d=build_stack(Counts_trans)

    #plot
    width = 0.35
    p1 = plt.bar(ind, Counts_trans[0], width, color='red')
    p2 = plt.bar(ind, Counts_trans[1], width, bottom=d[1] , color='orange')
    p3 = plt.bar(ind, Counts_trans[2], width, bottom=d[2],color = 'green')
    p4 = plt.bar(ind, Counts_trans[3], width, bottom=d[3],color = 'blue')
    p5 = plt.bar(ind, Counts_trans[4], width, bottom=d[4],color = 'purple')
    #legend
    plt.legend((p1[0], p2[0],p3[0],p4[0],p5[0]), \
               ('Angry', 'Disgust','Fear','Joy','Sadness'), loc=3)
    # loc=3 表示lower left 也就是底部最左
    plt.show()


def place_plot_1(df):
    '''
    Plot the Map Based on the frequency of each text

    :param df: The full information dataframe
    :return:Abstract Plot reflecting emotion
    '''
    df_place_tag = df[['Longtitude','Latitude','pangry', 'pdisgust','pfear','pjoy','psadness']]
    Long = df_place_tag['Longtitude'].tolist()
    Lati = df_place_tag['Latitude'].tolist()
    #print(Long,Lati)   #flo
    #set the title
    plt.title('Emotion Distribution Based on Frequency')
    #set the axis-X
    # plt.xticks(np.linspace(116.11,116.68,11))
    plt.xlabel('Longtitude(°E)')
    #set the axis-Y
    # plt.yticks(np.arange(39.71, 39.86, 0.015))
    plt.ylabel('Latitude(°N)')
    #plot
    color_dict = {2:"Red",3:"Orange",4:"Green",5:"Blue",6:"Purple"}
    shape_dict = {2:"*",3:"^",4:"s",5:".",6:"o"}  #五角星;上三角;正方;圆;圈
    label_dict = {2:"Angry",3:"Disgust",4:"Fear",5:"Joy",6:"Sadness"}
    has_label = [0,0,0,0,0]   #用来协助legend的绘制 [2,7]->[0,5] has_label[i-2]
    for index,row in df_place_tag.iterrows():
        row_data = list(row)
        # 0:Longtitude 1:Latitude 2:angry 3:disgust
        # 4:fear 5:joy 6:sadness
        for i in range(2,7):
            if row_data[i]!=0:
                plt.scatter(Long[index],Lati[index],marker=shape_dict[i],
                            s=20*row_data[i],alpha=0.5*row_data[i],c=color_dict[i],
                            cmap=color_dict[i]+'s')
                if row_data[i] == 1 and has_label[i-2] == 0:   #for the legend
                    plt.scatter(Long[index], Lati[index], marker=shape_dict[i],
                                s=15, alpha=0.5,c=color_dict[i],
                                cmap=color_dict[i] + 's', label=label_dict[i])
                    has_label[i-2]=1
    #legend
    plt.legend(loc=4)
    #grid
    plt.grid()
    plt.show()

def transformalt(*vartuple):
    '''
    a function for calculatin the latitude

    :param vartuple:
    :return:
    '''
    long, lati = vartuple
    r = -100 + 2.0*long + 3.0 *lati + 0.2 * lati * lati + 0.1 * long * lati + 0.2 * math.sqrt(math.fabs(long))
    r += (20.0 * math.sin(6.0 * long * math.pi) + 20.0 * math.sin(2.0 * long * math.pi)) * 2.0 / 3.0
    r += (20.0 * math.sin(lati * math.pi) + 40.0 * math.sin(lati / 3.0 * math.pi)) * 2.0 / 3.0
    r += (160.0 * math.sin(lati / 12.0 * math.pi) + 320 * math.sin(lati * math.pi / 30.0)) * 2.0 / 3.0
    return r

def transformlng(*vartuple):
    '''
    a function for calculatin the longtitude

    :param vartuple:
    :return:
    '''
    long, lati = vartuple
    r = 300.0 + long + 2.0 * lati + 0.1 * long * long + 0.1 * long * lati + 0.1 * math.sqrt(math.fabs(long))
    r += (20.0 * math.sin(6.0 * long * math.pi) + 20.0 * math.sin(2.0 * long * math.pi)) * 2.0 / 3.0
    r += (20.0 * math.sin(long * math.pi) + 40.0 * math.sin(long / 3.0 * math.pi)) * 2.0 / 3.0
    r += (150.0 * math.sin(long / 12.0 * math.pi) + 300.0 * math.sin(long / 30.0 * math.pi)) * 2.0 / 3.0
    return r

def judge_china(*vartuple):
    '''
    judge whether the tuple of (long,lati) is located in China

    :param vartuple:parameters
    :return: False refers to Located, while True refers to not located
    '''
    long, lati = vartuple
    if long<70 or long>140:
        return True
    if lati<0 or lati>55:
        return True
    return False

def place_trans(*vartuple):
    '''
    trans the long and lati from gcj02 to wgs84

    :param vartuple: long and lati (gcj02)
    :return: long and lati (wgs84)
    '''
    la = 6378245.0                #长半轴
    ob = 0.00669342162296594323   #离心率
    long, lati = vartuple
    if judge_china(long,lati):
        return [long,lati]
    tlat = transformalt(long - 105.0 ,lati - 35.0)
    tlng = transformalt(long - 105.0 ,lati - 35.0)
    rlat = lati / 180.0 * math.pi
    m = math.sin(rlat)
    m = 1 - ob * m * m
    sm = math.sqrt(m)
    tlat = (tlat * 180.0) / ((la * (1-ob)) / (m*sm) * math.pi)
    tlng = (tlng * 180.0) / (la / sm * math.cos(rlat) * math.pi)
    lat_wgs84 = 2 * lati - (lati + tlat)
    lon_wgs84 = 2 * long - (long + tlng)
    return lon_wgs84,lat_wgs84

def place_subdf(df):
    '''
    replace the long and lati in df, in order to plot by folium

    :param df: dataframe with long and lati(gcj02)
    :return: dataframe(place & tag only) with long and lati(wgs84)
    '''
    df_place_tag = df[['Longtitude','Latitude','Time','tag']]
    # df_place_tag['Lon_wgs84'] = 0
    # df_place_tag['Lat_wgs84'] = 0
    Long = df_place_tag['Longtitude'].tolist()
    Lati = df_place_tag['Latitude'].tolist()
    Places = zip(Long,Lati)
    Lon_wgs84=[];Lat_wgs84=[]
    for item in Places:
        lon_wgs84,lat_wgs84 = place_trans(*list(item))
        Lon_wgs84.append(lon_wgs84)
        Lat_wgs84.append(lat_wgs84)
    #print("Long:",Long,"Lon_wgs84",Lon_wgs84)
    #print("Lati:",Lati,"Lat_wgs84",Lat_wgs84)
    temp_df = pd.DataFrame(list(zip(Lon_wgs84,Lat_wgs84)),
                           columns=["Lon_wgs84","Lat_wgs84"])
    #print(temp_df)
    df_place_tag = pd.concat([df_place_tag, temp_df], axis=1)
    return df_place_tag

def place_plot_2(df,*vartuple):
    '''
    plot the emotion distribution given a certain time

    :param df: dataframe with (time,place,tag)
    :param vartuple: time period
    :return: a html file at the certain time
    '''
    t_start,t_end = vartuple
    t_start = "08 {:}:00:00".format(t_start.zfill(2))
    t_end = "08 {:}:00:00".format(t_end.zfill(2))

    color_dict = {"angry":"red","disgust":"orange","fear":"green",
                  "joy":"blue","sadness":"purple","mixed":"black"}
    Map = folium.Map(location=[39.791999,  116.359925],
                     zoom_start=12,
                     attr='default'
                     )
    # i=0
    print(t_start, t_end)
    for row in df.itertuples():
        # i += 1
        #print(getattr(row,'Time')[-11:])
        if t_start <= getattr(row,'Time')[-11:] < t_end  \
        and getattr(row,'tag') != 'others':
            location = [getattr(row,'Lat_wgs84'),getattr(row,'Lon_wgs84')]
            folium.Marker(location,
                          popup=folium.Popup(getattr(row,'tag'), max_width=1000),
                          tooltip='click here',
                          icon = folium.Icon(color= color_dict[getattr(row,'tag')])
                          ).add_to(Map)
            # if i > 10: break
    Map.save('../image/place_{:}.html'.format(vartuple))


def cluster(df,k=5):
    '''
    cluster the place with longtitude and latitude

    :param df: dataframe with (index,place,time,tag,place_wgs84)
    :return: dataframe with (index,place,time,tag,place_wgs84,place_class)
    '''
    data = df[['Longtitude','Latitude']]
    print(data)

    # 假如我要构造一个聚类数为3的聚类器
    estimator = KMeans(n_clusters=k)  # 构造聚类器
    estimator.fit(data)  # 聚类
    label_pred = estimator.labels_  # 获取聚类标签
    inertia = estimator.inertia_  # 获取聚类准则的总和
    #print(label_pred, inertia)
    df_plc_tag = pd.DataFrame(label_pred,columns=['Class'])
    df_emo_plc_tag = pd.concat([df , df_plc_tag], axis=1)
    return df_emo_plc_tag


def place_plot_3(df):
    '''
    Show the cluser result

    :param df: A dataframe with (index,place,time,tag,place_wgs84,place_class)
    :return: a scatter plot painted by the place_class
    '''
    Long = df['Longtitude'].tolist()
    Lati = df['Latitude'].tolist()
    # print(Long,Lati)   #flo
    # set the title
    plt.title('Classification Based on Place')
    # set the axis-X
    # plt.xticks(np.linspace(116.11,116.68,11))
    plt.xlabel('Longtitude(°E)')
    # set the axis-Y
    # plt.yticks(np.arange(39.71, 39.86, 0.015))
    plt.ylabel('Latitude(°N)')
    # plot
    color_dict = {0: "Red", 1: "Orange", 2: "Green", 3: "Blue", 4: "Purple"}
    #Color is based on Place in this Fuction
    for index, row in df.iterrows():
        row_data = list(row)
        # 0:Longtitude   1:Latitude  2:Time  3:tag
        # 4:Lon_wgs84    5:Lat_wgs84 6:Class
        plt.scatter(Long[index],Lati[index],c=color_dict[df['Class'][index]])
    # grid
    plt.grid()
    plt.show()



def dynamic_place(df):
    '''
    Plot some place by the time, add a timeline to decorate them

    :param df: dataframe with (index,place,time,tag,place_wgs84,place_class)
    :return:A timeline plot
    '''
    cluster_name = ["丰台","通州","房山","大兴西","大兴东"]
    emo_dict = {"angry":0, "disgust":1, "fear":2,
                "joy":3, "sadness":4, "mixed":5}
    df = df[['Time','tag','Class']]
    #print(df)
    time_interval = ['{:}:00:00'.format(str(i).zfill(2)) for i in range(0,24,2)]
    #初始化字典
    d = {}
    for i in range(len(time_interval)):
        Counts = np.zeros((5,6))
        #Counts = [[0 for j in range(6)] for j in range(len(cluster_name))]
        d[time_interval[i]] = Counts
    #print(d)
    #计算一天中不同地域不同情绪的分布情况
    for index,row in df.iterrows():
        temp_time = row['Time'][-8:]
        #print(temp_time)
        if getattr(row,"tag") != "others":
            for i in range(len(time_interval)-1):
                if time_interval[i] <= temp_time < time_interval[i + 1]:
                    print(getattr(row,"Class"),getattr(row,"tag"))
                    d[time_interval[i]][getattr(row,"Class")][emo_dict[getattr(row,"tag")]] += 1
            if temp_time >= time_interval[len(time_interval) - 1]:
                d[time_interval[-1]][getattr(row, "Class")][emo_dict[getattr(row, "tag")]] += 1
    # print(d['00:00:00'])
    # print(d['00:00:00'][:,0])

    x = cluster_name
    tl = Timeline()
    for i in time_interval:
        Y = d[i]
        #print(Y)
        bar = (
            Bar()
                .add_xaxis(x)
                .add_yaxis("angry", list(Y[:,0]))
                .add_yaxis("disgust", list(Y[:,1]))
                .add_yaxis("fear", list(Y[:, 2]))
                .add_yaxis("joy", list(Y[:, 3]))
                .add_yaxis("sadness", list(Y[:, 4]))
                .add_yaxis("mixed", list(Y[:, 5]))
                .set_global_opts(title_opts=opts.TitleOpts("{}情绪空间分布".format(i)))
        )
        tl.add(bar, "{}".format(i))
    tl.render("../image/timeline_bar.html")
    print("Picture Saved!")


def main():
    #构建自定义字典
    jieba.load_userdict("../data/emotion_lexicon/anger.txt")
    jieba.load_userdict("../data/emotion_lexicon/disgust.txt")
    jieba.load_userdict("../data/emotion_lexicon/fear.txt")
    jieba.load_userdict("../data/emotion_lexicon/joy.txt")
    jieba.load_userdict("../data/emotion_lexicon/sadness.txt")

    #文本处理
    with open("../data/weibo.txt",encoding="UTF-8") as f:
        text = f.readlines()
        for i in range(len(text)):
            text[i]=text[i].split("\t")
            text[i][0] = tokenize(text[i][0])   #Process the Text
            text[i][-1] = text[i][-1][:-12]     #strip the time

    df = pd.DataFrame(text,columns=['Text','Longtitude','Latitude','Time'])
    df = emo_num(df)
    emo_classify = load_func(df)
    emo_classify('mixed')
    df_emo_tag = emo_classify('unique')
    #save_df(df_emo_tag,"emo_tag_data")

    #时间分析
    df_emo_tag = pd.read_excel("../data/emo_tag_data.xlsx", header=0)
    Counts,Freqs = time(df_emo_tag)
    time_plot(Freqs)

    #空间分析
    print(df_emo_tag.describe())
    #place_plot_1(df_emo_tag)

    df_emo_tag = place_subdf(df_emo_tag)

    # print(df_emo_tag.describe())
    # for i in range(0,24,2):
    #     place_plot_2(df_emo_tag,str(i),str(i+2))

    #动态可视化
    df_emo_plc_tag = cluster(df_emo_tag,5)
    #save_df(df_emo_plc_tag,"plc_emo_tag_data")

    df_emo_plc_tag = pd.read_excel("../data/plc_emo_tag_data.xlsx", header=0)

    #place_plot_3(df_emo_plc_tag)
    #dynamic_place(df_emo_plc_tag)


if __name__=='__main__':main()
