#-*- coding=utf-8 -*-
#@Time:  
#@Author: zjh
#@File: co2.py
#@Software: PyCharm
import os
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from scipy import interpolate
from pyecharts import options as opts
from pyecharts.charts import Map,Timeline


class NotNumError(Exception):
    def __init__(self,year,province,industry,type_):
        self.year = year
        self.province = province
        self.industry = industry
        self.type = type_
        self.message = "NAN in data.ErrorLocation: date:{:}, place:{:}, industry:{:}, type:{:}" \
                        .format(year,province,industry,type_)

    def interpolate_nan(self,df,place):
        # date_name = df.columns.tolist()[0]
        # value_name = df.columns.tolist()[1]
        # date = df[date_name].tolist()
        # value = df[value_name].tolist()
        df = df.dropna()
        date = df['date'].values
        value = df[f"{place},{ctsv2.type}_co2"].values
        #print(date, value)
        f = interpolate.interp1d(date, value, kind="quadratic")
        date_new = np.arange(1997, 2016)
        value_new = f(date_new)
        #print(date_new, value_new)

        df_all = pd.DataFrame({"date": date_new, f"{place},{ctsv2.type}_co2":value_new},
                          columns=['date', f"{place},{ctsv2.type}_co2"])

        return df_all


class CO2Description:
    def __init__(self):
        self.DATA_PATH = "../data/co2_demo"
        self.filelist = os.listdir(self.DATA_PATH)

    def load_total_data(self):
        co2_total_data = []
        for name_ in self.filelist:
            filename = os.path.join(self.DATA_PATH, name_)
            co2_total_data.append(pd.read_excel(filename, sheet_name=0))
        print(f"Successfully Load Total data!")
        return co2_total_data

    def load_local_data(self,province):
        co2_local_data = []
        for name_ in self.filelist:
            filename = os.path.join(self.DATA_PATH, name_)
            co2_local_data.append(pd.read_excel(filename, sheet_name=province))
        print(f"Successfully Load {province} data!")
        return co2_local_data


class CO2Visualization:
    def __init__(self):
        self.place_list  = [
              'Beijing','Tianjin','Hebei','Shanxi','InnerMongolia',
              'Liaoning','Jilin','Heilongjiang','Shanghai','Jiangsu',
              'Zhejiang','Anhui','Fujian','Jiangxi','Shandong',
              'Henan','Hubei','Hunan','Guangdong','Guangxi',
              'Hainan','Chongqing','Sichuan','Guizhou','Yunnan',
              'Shaanxi','Gansu','Qinghai','Ningxia','Xinjiang']
        self.place_list = ['Hainan','Ningxia']

class Co2TimeSeriesVis(CO2Visualization):
    def __init__(self,industry,type_):
        super(Co2TimeSeriesVis, self).__init__()
        self.industry = industry
        self.type = type_
        # 时空数据跟随场景变化--for

    def time_series_plot(self,df,place):
        # Get data
        date_name = df.columns.tolist()[0]
        value_name = df.columns.tolist()[1]
        date = df[date_name].tolist()
        value = df[value_name].tolist()

        if np.isnan(sum(value)):
            #np.where(np.isnan(value))[0] --array([2], dtype=int64)
            #print(np.where(np.isnan(value))[0])
            raise NotNumError([date[i] for i in np.where(np.isnan(value))[0]],
                              place,self.industry,self.type)

        else:
            # Draw Plot
            plt.figure(figsize=(16, 10), dpi=80)
            plt.plot(date, value,'o-',color='tab:blue',label=self.industry)

            # Decoration
            xtick_labels = df[date_name].tolist()
            plt.xticks(ticks=xtick_labels, labels=xtick_labels, rotation=0, fontsize=12, horizontalalignment='center',
                       alpha=.7)
            plt.yticks(fontsize=12, alpha=.7)
            plt.title(f"{value_name} (1997 - 2015)", fontsize=22)
            for a, b in zip(date, value):
                plt.text(a, b+0.5, round(b,2), ha='center', va='bottom', fontsize=10)
            plt.grid(axis='both', alpha=.3)

            # peak and through location
            data = df[value_name].values
            doublediff = np.diff(np.sign(np.diff(data)))
            peak_locations = np.where(doublediff == -2)[0] + 1
            doublediff2 = np.diff(np.sign(np.diff(-1 * data)))
            trough_locations = np.where(doublediff2 == -2)[0] + 1

            plt.scatter(df[date_name][peak_locations], df[value_name][peak_locations], marker=mpl.markers.CARETUPBASE,
                        color='tab:green', s=100, label='Peaks')
            plt.scatter(df[date_name][trough_locations], df[value_name][trough_locations], marker=mpl.markers.CARETDOWNBASE,
                        color='tab:red', s=100, label='Troughs')

            # for t, p in zip(trough_locations[1::5], peak_locations[::3]):
            #     plt.text(df[date_name][p], df[value_name][p] + 15, df[date_name][p], horizontalalignment='center', color='darkgreen')
            #     plt.text(df[date_name][t], df[value_name][t] - 35, df[date_name][t], horizontalalignment='center', color='darkred')

            # Remove borders
            plt.gca().spines["top"].set_alpha(0.0)
            plt.gca().spines["bottom"].set_alpha(0.3)
            plt.gca().spines["right"].set_alpha(0.0)
            plt.gca().spines["left"].set_alpha(0.3)
            plt.legend()
            plt.show()

            # if self.industry == "Sum-CO2":
            #     plt.savefig(f"../images/time_series_plot/sum_co2")
            # else:
            #     #plt.savefig(f"../images/time_sereis_plot/{self.industry}_{self.type}_co2/{place}")
            #     plt.savefig(place)

    def time_series_stack(self,df):
        # Decide Colors
        #mycolors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:brown', 'tab:grey', 'tab:pink', 'tab:olive']

        # Draw Plot and Annotate
        fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
        columns = df.columns[1:]
        date_name = df.columns[0]
        # Prepare data
        x = df[date_name].values.tolist()
        y0 = df[columns[0]].values.tolist()
        y1 = df[columns[1]].values.tolist()
        y2 = df[columns[2]].values.tolist()
        y3 = df[columns[3]].values.tolist()
        y4 = df[columns[4]].values.tolist()
        y5 = df[columns[5]].values.tolist()
        y6 = df[columns[6]].values.tolist()
        y7 = df[columns[7]].values.tolist()
        y8 = df[columns[8]].values.tolist()
        y9 = df[columns[9]].values.tolist()
        y10 = df[columns[10]].values.tolist()
        y11 = df[columns[11]].values.tolist()
        y12 = df[columns[12]].values.tolist()
        y13 = df[columns[13]].values.tolist()
        y14 = df[columns[14]].values.tolist()
        y15 = df[columns[15]].values.tolist()
        y16 = df[columns[16]].values.tolist()
        y17 = df[columns[17]].values.tolist()
        y = np.vstack([y0,y1,y2,y3,y4,y5,y6,y7,y8,
                       y9,y10,y11,y12,y13,y14,y15,y16,y17])

        # Plot for each column
        labs = columns.values.tolist()
        ax = plt.gca()
        ax.stackplot(x, y, labels=labs, alpha=0.8)

        # Decorations
        ax.set_title('Different Type Co2 Time Series(1997-2015)', fontsize=18)
        ax.set(ylim=[0, 10000])
        ax.legend(fontsize=10, ncol=3,loc="upper left")
        plt.xticks(x[::1], fontsize=10, horizontalalignment='center')
        #plt.yticks(np.arange(10000, 100000, 20000), fontsize=10)
        plt.xlim(x[0], x[-1])

        # Lighten borders
        plt.gca().spines["top"].set_alpha(0)
        plt.gca().spines["bottom"].set_alpha(.3)
        plt.gca().spines["right"].set_alpha(0)
        plt.gca().spines["left"].set_alpha(.3)

        plt.show()


class CO2ProportionVis(CO2Visualization):
    def set_year(self,year):
        self.year = year

    def set_place(self,place):
        self.place = place

    def set_industry(self,industry):
        self.industry = industry

    def set_type(self,type_):
        self.type = type_

    # draw line
    def calculate_pro(self,df_,place):
        columns = df_.columns
        before = df_[columns[0]];before_sum = sum(before)
        after = df_[columns[1]];after_sum = sum(after)
        print("before_sum",before_sum,"after_sum",after_sum)
        if before_sum == 0 :
            print(f"Error in {columns[0]}")
            raise ZeroDivisionError
        if after_sum == 0:
            print(f"Error in {columns[1]}")
            raise  ZeroDivisionError

        if np.isnan(before_sum):
            raise NotNumError(columns[0],place,self.industry,self.type)
        if np.isnan(after_sum):
            raise NotNumError(columns[1],place,self.industry,self.type)


        before = [i/before_sum for i in before]
        after = [i/after_sum for i in after]
        df = pd.DataFrame({f"{columns[0]}":before,f"{columns[1]}":after,
                          f"{columns[2]}":df_[columns[2]].values.tolist()},
                          columns = columns)
        return df

    def newline(self,p1, p2,color='black'):
        ax = plt.gca()
        l = mlines.Line2D([p1[0], p2[0]], [p1[1], p2[1]], color='red' if p1[1] - p2[1] > 0 else 'green', marker='o',
                          markersize=6)
        ax.add_line(l)
        return l

    def slopt_plot(self,df_,place,title):
        df = self.calculate_pro(df_,place)
        print(df)
        columns = df.columns
        b_data = columns[0]
        a_data = columns[1]
        name = columns[2]
        y_max_lim = max(max(df[b_data]),max(df[a_data]))

        fig, ax = plt.subplots(1, 1, figsize=(14, 14), dpi=80)

        # Vertical Lines
        ax.vlines(x=1, ymin=0, ymax=y_max_lim, color='black', alpha=0.7, linewidth=1, linestyles='dotted')
        ax.vlines(x=3, ymin=0, ymax=y_max_lim, color='black', alpha=0.7, linewidth=1, linestyles='dotted')

        # Points
        ax.scatter(y=df[b_data], x=np.repeat(1, df.shape[0]), s=10, color='black', alpha=0.7)
        ax.scatter(y=df[a_data], x=np.repeat(3, df.shape[0]), s=10, color='black', alpha=0.7)

        # Line Segmentsand Annotation
        for p1, p2, loc in zip(df[b_data], df[a_data], df[name]):
            self.newline([1, p1], [3, p2])
            ax.text(1 - 0.05, p1, loc + ', ' + str(round(p1,4)), horizontalalignment='right', verticalalignment='center',
                    fontdict={'size': 10})
            ax.text(3 + 0.05, p2, loc + ', ' + str(round(p2,4)), horizontalalignment='left', verticalalignment='center',
                    fontdict={'size': 10})

        # 'Before' and 'After' Annotations
        ax.text(1 - 0.05, 13000, 'BEFORE', horizontalalignment='right', verticalalignment='center',
                fontdict={'size': 18, 'weight': 700})
        ax.text(3 + 0.05, 13000, 'AFTER', horizontalalignment='left', verticalalignment='center',
                fontdict={'size': 18, 'weight': 700})

        # Decoration
        ax.set_title(title, fontdict={'size': 22})
        ax.set(xlim=(0, 4), ylim=(0, y_max_lim), ylabel='total co2 from each province')
        ax.set_xticks([1, 3])
        ax.set_xticklabels([b_data, a_data])
        #plt.yticks(np.arange(500, 13000, 2000), fontsize=12)

        # Lighten borders
        plt.gca().spines["top"].set_alpha(.0)
        plt.gca().spines["bottom"].set_alpha(.0)
        plt.gca().spines["right"].set_alpha(.0)
        plt.gca().spines["left"].set_alpha(.0)
        plt.show()
        plt.savefig(place)


# class CO2CorelationVis(CO2Visualization):
#     def set_year(self,year):
#         self.year = year
#
#     def set_place(self,place):
#         self.place = place
#
#     def set_industry(self,industry):
#         self.industry = industry
#
#     def set_type(self,type_):
#         self.type = type_


class CO2MapVis(CO2Visualization):
    def set_year(self,year):
        self.year = year

    def set_place(self,place):
        self.place = place

    def set_industry(self,industry):
        self.industry = industry

    def set_type(self,type_):
        self.type = type_

    def china_province_plot(self,data):
        c = (
            Map()
                .add("CO2排放总量", [list(z) for z in zip(self.place, data)], "china")
                .set_global_opts(title_opts=opts.TitleOpts(title="各省CO2排放总量"),
                                 visualmap_opts=opts.VisualMapOpts(max_=600))
        )
        c.render(f"{self.year}.html")
        print(f"Map on {self.year},{self.industry},{self.type} Finished!")


    def dynamic_province_plot(self):
        tl = Timeline()
        for i_year in self.year:
            data = co2_total_data[i_year-1997]
            data = data["Total"].values.tolist()[:30]
            c = (
                Map()
                    .add("CO2排放总量", [list(z) for z in zip(self.place, data)], "china")
                    .set_global_opts(title_opts=opts.TitleOpts(title="各省CO2排放总量"),
                                     visualmap_opts=opts.VisualMapOpts(max_=500))
            )
            tl.add(c,"{}".format(i_year))
        tl.render("dynamic_map.html")
        print(f"Map on {self.industry},{self.type} Finished!")

#####################################################
cd = CO2Description()
co2_total_data = cd.load_total_data()


'''全国CO2总排放'''
# sum_co2 = np.array([])
# for data in co2_total_data:
#     date = np.arange(1997,2016)
#     #print(data.loc[["Sum-CO2"],"Total"])
#     sum_co2 = np.append(sum_co2,data.loc[["Sum-CO2"],"Total"])
# df = pd.DataFrame({"date":date,"sum_co2":sum_co2},columns =['date','sum_co2'])
#
# ctsv1 = Co2TimeSeriesVis("Sum-CO2","Total")
# ctsv1.time_series_plot(df,"china")


'''各地区CO2总排放'''
# ctsv2 = Co2TimeSeriesVis("Total Consumption","Total")
# for place in ctsv2.place_list:
#     co2_local_data = cd.load_local_data(place)
#     #location: date + value(place; industry; tpye_)
#     local_sum_co2 = np.array([])
#     for data in co2_local_data:
#         date = np.arange(1997,2016)
#         #print(data.loc[["Total Consumption"],"Total"])
#         local_sum_co2 = np.append(local_sum_co2,data.loc[["Total Consumption"],"Total"])
#     df = pd.DataFrame({"date":date,f"{place},{ctsv2.type}_co2":local_sum_co2},
#                       columns =['date',f"{place},{ctsv2.type}_co2"])
#     try:
#         ctsv2.time_series_plot(df,place)
#     except NotNumError as nne:
#         message = nne.message
#         print(message)
#         df_all = nne.interpolate_nan(df,place)
#         ctsv2.time_series_plot(df_all, place)
#         print(f"{place} Finished")
#     else:
#         print(f"{place} Finished")




'''全国各种CO2类型变化图'''
# co2_list = [];i=0
# for data in co2_total_data:
#     date = np.arange(1997,2016)
#     per_value = data.loc[["Sum-CO2"],data.columns[1:]].values.tolist()[0]
#     per_value.insert(0,date[i])
#     co2_list.append(per_value)
#     i += 1
# columns_name = ['date']
# columns_name.extend(data.columns[1:])
# print(columns_name)
# df = pd.DataFrame(co2_list,columns=columns_name)
# ctsv3 = Co2TimeSeriesVis("Sum-CO2","all_type")
# ctsv3.time_series_stack(df)


'''1997-2015省排放量变化'''
# cpv1 = CO2ProportionVis()
# # co2_total_data[0] -- dataframe
# # df.loc[,] -- ans of search dataframe
# # .values -- list:[num]
# # before_total = co2_total_data[0].loc[["Sum-CO2"],"Total"].values[0]
# # after_total = co2_total_data[-1].loc[["Sum-CO2"],"Total"].values[0]
# #
# # co2_before = [n/before_total for n in co2_total_data[0]['Total'][:30]]
# # co2_after = [n/after_total for n in co2_total_data[-1]['Total'][:30]]
# co2_before = co2_total_data[0]['Total'][:30]
# co2_after = co2_total_data[-1]['Total'][:30]
# place = cpv1.place_list
# df = pd.DataFrame({"1997":co2_before,"2015":co2_after,"place":place},
#                   columns=["1997","2015","place"])
#
# try:
#     cpv1.slopt_plot(df,title = "comparing co2_proportion between 1997 and 2015")
# except ZeroDivisionError:
#     pass

'''1997-2015全国CO2类型变化'''
# cpv2 = CO2ProportionVis()
# before = co2_total_data[0].loc[["Sum-CO2"]].values[0] #select the list
# after = co2_total_data[-1].loc[["Sum-CO2"]].values[0]
# print(before,after)
# co2_type = co2_total_data[0].columns[1:]
# df = pd.DataFrame({"1997":before[1:],"2015":after[1:],
#                    "co2_type":co2_type})
# print(df)
# cpv2.slopt_plot(df,place="china",title ="co2_type_proportion between 1997 and 2015")


'''1997-2015各地区CO2类型变化'''
# cpv3 = CO2ProportionVis()
# cpv3.set_industry('Total Consumption')
# co2_before_data = co2_total_data[0]
# co2_after_data = co2_total_data[-1]
# for place in cpv3.place_list:
#     before = co2_total_data[0].loc[[place]].values[0] #select the list
#     after = co2_total_data[-1].loc[[place]].values[0]
#     print(before,after)
#     co2_type = co2_total_data[0].columns[1:]
#     df = pd.DataFrame({"1997":before[1:],"2015":after[1:],
#                         "co2_type":co2_type})
#     cpv3.slopt_plot(df,place,title =f"{place} co2 type between 1997 and 2015")

'''2015年各省CO2排放量'''
# cmv1 = CO2MapVis()
# plot_year = 2015
# cmv1.set_year(plot_year)
# cmv1.set_place(
# ['北京','天津','河北','山西','内蒙古','辽宁','吉林','黑龙江','上海','江苏',
# '浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','广西',
# '海南','重庆','四川','贵州','云南','陕西','甘肃','青海','宁夏','新疆']
# )
# data = co2_total_data[plot_year-1997]
# data = data["Total"].values.tolist()[:30]
# cmv1.set_industry("Total Consumption")
# cmv1.set_type("Total")
# cmv1.china_province_plot(data)


'''1997-2015年各省CO2排放量'''
# cmv2 = CO2MapVis()
# cmv2.set_year(list(range(1997,2016)))
# cmv2.set_place(
# ['北京','天津','河北','山西','内蒙古','辽宁','吉林','黑龙江','上海','江苏',
# '浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','广西',
# '海南','重庆','四川','贵州','云南','陕西','甘肃','青海','宁夏','新疆']
# )
# cmv2.set_industry("Total Consumption")
# cmv2.set_type("Total")
# cmv2.dynamic_province_plot()

