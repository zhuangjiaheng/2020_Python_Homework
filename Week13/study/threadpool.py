#-*- coding=utf-8 -*-
#@Time:
#@Author: zjh
#@File: VosSpiderClass.py
#@Software: PyCharm

import os
import re
import sys
import urllib.request
import queue
from tqdm import tqdm
from bs4 import BeautifulSoup
import xlwt
from threading import Thread
import concurrent.futures

class Craw:
    @staticmethod
    def askurl(url):
        """
        get the content of a web page by its url
        :param url: the specific url name
        :return: the html content of the url
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
        }
        # 用封装好的request对象去访问,伪装
        req = urllib.request.Request(url=url, headers=headers)
        html = ""
        try:
            response = urllib.request.urlopen(req)
            html = response.read().decode("utf-8")
        except urllib.error.URLError as ue:
            if hasattr(ue, "code"):
                print(ue.code)
            if hasattr(ue, "reason"):
                print(ue.reason)
        return html



class LinkCraw(Craw):
    def __init__(self,base_url):
        super(LinkCraw, self).__init__()
        self.base_url = base_url
        self.find_link = re.compile(r'<a href="(.*?)" target="_blank">')  # 创建正则表达式的对象,表示规则(字符串的模式)

    def get_link(self,page_num):
        """
        get the link data on the web page at one time
        :param baseurl: "https://www.51voa.com"
        :findLink: an mode of re.complie used for finding href
        :return: linklist contains links in 35 pages which are linked to mp3 data
        """
        linklist = []
        for i in range(page_num):
            print(f"collect page{i + 1}")
            url = self.base_url + f'/VOA_Standard_{i + 1}.html'
            html = self.askurl(url)
            # print(html)

            soup = BeautifulSoup(html, "html.parser")
            links = []  # save the links in one pages
            for item in soup.find_all("a", target="_blank"):  # 查找符合要求的字符串,行程列表
                item = str(item)
                # 匹配数据连接
                link = self.base_url + re.findall(self.findlink, item)[0]  # re库用来通过
                links.append(link)
            linklist.append(links)
        return linklist


class DataCraw(Craw,Thread):
    def __init__(self):
        super(DataCraw, self).__init__()
        self.find_mp3 = re.compile(r'<a href="(.*?)" id="mp3">')
        self.replace_tag = r'</?\w+[^>]*>'


    def get_data(self,url):
        """

        :param url: the url of the mp3
        :param findmp3: an mode of re.complie used for searching mp3 href
        :param replace_tag:
        :return:
        """
        data_list = []  # save the return data
        html_data = self.askurl(url)
        soup = BeautifulSoup(html_data, "html.parser")

        title = soup.find_all("h1")[0]
        title = re.sub(self.replace_tag, '', str(title))
        title = re.sub('[\/*:?"<>|]', '', title)
        data_list.append(title)

        mp3_item = soup.find_all("a", id="mp3")[0]
        mp3_item = str(mp3_item)  # bs4 tag -> str
        music_url = re.findall(self.find_mp3, mp3_item)[0]
        data_list.append(music_url)

        text_item = soup.find_all("p")
        for i in range(len(text_item)):
            text_item[i] = str(text_item[i])
            text_item[i] = re.sub(self.replace_tag, '', text_item[i])
        text = '\n'.join(text_item)
        data_list.append(text)

        return data_list

    def save_file(filename, content):
        """

        :param filename: the name saved on the disk
        :param content: the content of the music
        :return:
        """
        dir = os.path.dirname(filename)
        # print(f"filename={filename}\ndir={dir}")
        if not os.path.exists(dir):
            os.makedirs(dir)
        # 放到else里会少一次
        with open(file=filename, mode="wb") as f:
            f.write(content)

    def download_music(music_name, music_url, package_num):
        """
        download the music
        :param music_name: the name saved on the disk
        :param music_url: the download url of the music
        :param package_num: the number of package the file will be put
        :return:
        """

        response = urllib.request.urlopen(music_url)
        content = response.read()

        save_file(rf'../mp3/{package_num}/' + music_name + '.mp3', content)




def save_file(filename, content):
    """

    :param filename: the name saved on the disk
    :param content: the content of the music
    :return:
    """
    dir = os.path.dirname(filename)
    # print(f"filename={filename}\ndir={dir}")
    if not os.path.exists(dir):
        os.makedirs(dir)
    # 放到else里会少一次
    with open(file=filename, mode="wb") as f:
        f.write(content)


def download_music(music_name, music_url, package_num):
    """
    download the music
    :param music_name: the name saved on the disk
    :param music_url: the download url of the music
    :param package_num: the number of package the file will be put
    :return:
    """

    response = urllib.request.urlopen(music_url)
    content = response.read()

    save_file(rf'../mp3/{package_num}/' + music_name + '.mp3', content)


def save_data(datalist, savepath):
    """
    save (name,url of mp3,text) to an excel sheet
    :param datalist: a 2d list with the imformation above
    :param savepath: the path where the data will be saved
    :return: an excel data
    """
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("VOA", cell_overwrite_ok=True)
    col = ("name", "url", "text")
    for i in range(3):
        sheet.write(0, i, col[i])  # 列名
    for i in range(len(datalist)):
        data = datalist[i]
        for j in range(0, 3):
            sheet.write(i + 1, j, data[j])
    book.save(savepath)


def craw(link_list,data_list):
    """
    the working function for multi-thread
    :param page: an url list in a page
    :param page_num: the index of the page, which can help create the folder
    :param find_mp3: an mode of re.complie used for searching mp3 href
    :param replace_tag: strip the html tag
    :return:
    """
    find_mp3 = re.compile(r'<a href="(.*?)" id="mp3">')
    replace_tag = r'</?\w+[^>]*>'

    while True:
        link_ind = q.get()
        if link_ind is None:
            break
        datas = []
        page_num = link_ind + 1
        page = link_list[link_ind]
        bar = tqdm(page)
        for url in bar:
            # for url in page:
            bar.set_description(f"Batch {page_num}")
            data = get_data(url, find_mp3, replace_tag)
            title, music_url, text = data[0], data[1], data[2]
            download_music(title, music_url, page_num)
            datas.append(data)
        # return datas
        data_list.extend(datas)
        q.task_done()


def monitor():
    pass


if __name__ == '__main__':
    base_url = "https://www.51voa.com"
    page_num = 35
    l = LinkCraw(base_url)
    link_list = l.get_link(page_num)


    data_list = []
    q = queue.Queue()
    craw_threads = []
    num_craw_threads = 15
    num_save_threads = 3

    for link_ind in range(len(link_list)):
        q.put(link_ind)
    q.join()
    for i in range(num_craw_threads):
        t = Thread(target=craw,args=(link_list,data_list))
        craw_threads.append(t)
        t.start()

    for i in range(num_craw_threads):
        q.put(None)
    for t in num_craw_threads:
        t.join()


    save_data(data_list, "../results/voa1.xls")





