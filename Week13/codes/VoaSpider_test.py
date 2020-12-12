#-*- coding=utf-8 -*-
# @Time:
# @Author: zjh
# @File: VoaSpider.py
# @Software: PyCharm

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


def askurl(url):
    """
    get the content of a web page by its url
    :param url: the specific url name
    :return: the html content of the url
    """
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    }
    # 用封装好的request对象去访问,伪装
    req = urllib.request.Request(url=url,headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(req)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as ue:
        if hasattr(ue,"code"):
            print(ue.code)
        if hasattr(ue,"reason"):
            print(ue.reason)
    return html


def get_link(baseurl,findlink):
    """
    get the link data on the web page at one time
    :param baseurl: "https://www.51voa.com"
    :findLink: an mode of re.complie used for finding href
    :return: linklist contains links in 35 pages which are linked to mp3 data
    """
    linklist = []
    for i in range(2):
        print(f"collect page{i+1}")
        url = baseurl + f'/VOA_Standard_{i+1}.html'
        html = askurl(url)
        #print(html)

        soup = BeautifulSoup(html, "html.parser")

        links = []   # save the links in one pages
        for item in soup.find_all("a",target="_blank"):  # 查找符合要求的字符串,行程列表
            item = str(item)
            # 匹配数据连接
            link = baseurl + re.findall(findlink, item)[0]   # re库用来通过
            links.append(link)
        linklist.append(links)
    return linklist


def get_data(url,findmp3,replace_tag):
    """

    :param url: the url of the mp3
    :param findmp3: an mode of re.complie used for searching mp3 href
    :param replace_tag:
    :return:
    """
    data_list = []  # save the return data
    html_data = askurl(url)
    soup = BeautifulSoup(html_data, "html.parser")

    title = soup.find_all("h1")[0]
    title = re.sub(replace_tag,'',str(title))
    title = re.sub('[\/*:?"<>|]','',title)
    data_list.append(title)

    mp3_item = soup.find_all("a",id="mp3")[0]
    mp3_item = str(mp3_item)   # bs4 tag -> str
    music_url = re.findall(findmp3,mp3_item)[0]
    data_list.append(music_url)

    text_item = soup.find_all("p")
    for i in range(len(text_item)):
        text_item[i] = str(text_item[i])
        text_item[i] = re.sub(replace_tag,'',text_item[i])
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
    #print(f"filename={filename}\ndir={dir}")
    if not os.path.exists(dir):
        os.makedirs(dir)
    # 放到else里会少一次
    with open(file=filename, mode="wb") as f:
        f.write(content)


def download_music(music_name, music_url,package_num):
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


def save_data(datalist,savepath):
    """
    save (name,url of mp3,text) to an excel sheet
    :param datalist: a 2d list with the imformation above
    :param savepath: the path where the data will be saved
    :return: an excel data
    """
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("VOA",cell_overwrite_ok=True)
    col = ("name","url","text")
    for i in range(3):
        sheet.write(0,i,col[i])  #列名
    for i in range(len(datalist)):
        data = datalist[i]
        for j in range(0,3):
            sheet.write(i+1,j,data[j])
    book.save(savepath)

def work(page,page_num,find_mp3,replace_tag):
    """
    the working function for multi-thread
    :param page: an url list in a page
    :param page_num: the index of the page, which can help create the folder
    :param find_mp3: an mode of re.complie used for searching mp3 href
    :param replace_tag: strip the html tag
    :return:
    """
    datas = []
    bar = tqdm(page)
    for url in bar:
    # for url in page:
        bar.set_description(f"Batch {page_num}")
        data = get_data(url, find_mp3, replace_tag)
        title, music_url, text = data[0], data[1], data[2]
        download_music(title, music_url, page_num)
        datas.append(data)
    return datas

if __name__ == '__main__':
    baseurl = "https://www.51voa.com"
    find_link = re.compile(r'<a href="(.*?)" target="_blank">')  # 创建正则表达式的对象,表示规则(字符串的模式)
    find_mp3 = re.compile(r'<a href="(.*?)" id="mp3">')
    replace_tag = r'</?\w+[^>]*>'

    link_list = get_link(baseurl, find_link)

    data_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(work,link_list[page_num],page_num+1,find_mp3,replace_tag):
                   page_num+1 for page_num in range(len(link_list))}
        for future in concurrent.futures.as_completed(futures):
            now_page = futures[future]
            datas = future.result()
            data_list.extend(datas)
            # print(now_page," finished!")
    print(data_list)
    save_data(data_list, "../results/voa.xls")


    # for i in range(len(link_list)):
    #     page = link_list[i]
    #     datas = work(page,i+1,find_mp3,replace_tag)
    #     data_list.extend(datas)
    #
    # print(sys.getsizeof(data_list))
    # print(data_list)
    # save_data(data_list, "../results/voa.xls")

