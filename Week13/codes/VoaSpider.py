# -*- coding=utf-8 -*-
# @Time:
# @Author: zjh
# @File: VoaSpider.py
# @Software: PyCharm

import os
import re
import sys
import time
import json
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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    }
    # 用封装好的request对象去访问,伪装
    req = urllib.request.Request(url=url, headers=headers)
    html = ""
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    # try:
    #     response = urllib.request.urlopen(req)
    #     html = response.read().decode("utf-8")
    # except urllib.error.URLError as ue:
    #     if hasattr(ue, "code"):
    #         print(ue.code)
    #     if hasattr(ue, "reason"):
    #         print(ue.reason)

    return html


def get_link(page_num,baseurl, findlink, page_start_ind=0):
    """
    get the link data on the web page at one time
    :param baseurl: "https://www.51voa.com"
    :findLink: an mode of re.complie used for finding href
    :param page_start_ind: the first page need to craw
    :return: linklist contains links in 35 pages which are linked to mp3 data
    """
    linklist = []
    # page_start = page_start - 1 # change num2ind
    for i in range(page_start_ind,page_start_ind+page_num):
        print(f"collect page{i + 1}")
        url = baseurl + f'/VOA_Standard_{i + 1}.html'
        html = askurl(url)
        # print(html)

        soup = BeautifulSoup(html, "html.parser")

        links = []  # save the links in one pages
        for item in soup.find_all("a", target="_blank"):  # 查找符合要求的字符串,行程列表
            item = str(item)
            # 匹配数据连接
            link = baseurl + re.findall(findlink, item)[0]  # re库用来通过
            links.append(link)
        linklist.append(links)
    return linklist


def get_data(url, findmp3, replace_tag):
    """
	get the one music data on the web page by url at one time
    :param url: the url of the mp3
    :param findmp3: a mode of re.complie used for searching mp3 href
    :param replace_tag: a mode of re.compile used for striping the html tag
    :return: a datalist consist of music_name,music_url,music_text
    """
    data_list = []  # save the return data
    html_data = askurl(url)
    soup = BeautifulSoup(html_data, "html.parser")

    title = soup.find_all("h1")[0]
    title = re.sub(replace_tag, '', str(title))
    title = re.sub('[\/*:?"<>|]', '', title)
    data_list.append(title)

    mp3_item = soup.find_all("a", id="mp3")[0]
    mp3_item = str(mp3_item)  # bs4 tag -> str
    music_url = re.findall(findmp3, mp3_item)[0]
    data_list.append(music_url)

    text_item = soup.find_all("p")
    for i in range(len(text_item)):
        text_item[i] = str(text_item[i])
        text_item[i] = re.sub(replace_tag, '', text_item[i])
    text = '\n'.join(text_item)
    data_list.append(text)

    return data_list


def save_file(filename, content):
    """
	save the content 
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
    :return: the size of the content
    """

    response = urllib.request.urlopen(music_url)
    content = response.read()

    save_file(rf'../voa_mp3/{package_num}/' + music_name + '.mp3', content)
    return sys.getsizeof(content)/(1024*1024)

def save_data(datalist, savepath):
    """
    save (name,url of mp3,text) to an excel sheet
    :param datalist: a 2d list with the imformation above
    :param savepath: the path where the data will be saved
    :return: an excel data
    """
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("VOA", cell_overwrite_ok=True)
    col = ("name", "url","size(MB)","text")
    for i in range(4):
        sheet.write(0, i, col[i])  # 列名
    for i in range(len(datalist)):
        data = datalist[i]
        for j in range(0, 4):
            sheet.write(i + 1, j, data[j])
    book.save(savepath)


def craw(link_list,data_list,start_ind=0):
    """
    the working function for the work thread
    :param link_list: the link_list get by the get_link data
    :param data_list: the content to save the data parse from the mp3url, share with different thread,
    				  each thread extend its own data into it
    :param start_ind: remark where to start, work only if there is a breakpoint
    :return:
    """
    find_mp3 = re.compile(r'<a href="(.*?)" id="mp3">')
    replace_tag = r'</?\w+[^>]*>'


    while True:
        link_ind = q.get()
        if link_ind is None:
            break

        datas = []
        page_num = start_ind + link_ind + 1
        page = link_list[link_ind]

        # bar = tqdm(page)
        # without try-except
        # for url in bar:
        #     # for url in page:
        #         bar.set_description(f"Batch {page_num}")
        #         data = get_data(url, find_mp3, replace_tag)
        #         title, music_url, text = data[0], data[1], data[2]
        #         download_music(title, music_url, page_num)
        #         datas.append(data)


        for url in page:
            # for url in page:
            try:
                # bar.set_description(f"Batch {page_num}")
                data = get_data(url, find_mp3, replace_tag)
                title, music_url, text = data[0], data[1], data[2]
                size = download_music(title, music_url, page_num)
                data.insert(2,size)
                datas.append(data)
                qs.put(size)
            except urllib.error.HTTPError as ueh:
                # print("HTTP")
                info = {"id": page_num, "error": "HTTPError"}
                if hasattr(ueh, "code"):
                    print(ueh.code)
                if hasattr(ueh, "reason"):
                    print(ueh.reason)
                qe.put(info)
                break
            except urllib.error.URLError as ueu:
                # print("URL")
                info = {"id":page_num,"error":"URLError"}
                if hasattr(ueu, "code"):
                    print(ueu.code)
                if hasattr(ueu, "reason"):
                    print(ueu.reason)
                qe.put(info)

                break

        # return datas
        data_list.extend(datas)
        q.task_done()
        qe.put(1)  # use 1 to mark the thread has done its work
        print(f"close : {page_num} !" )


def show_status(check_id,total_page_num,cnt_to_stop,break_page,start,temp_size):
    """
    :param check_id: the key of the information
    :param total_page_num: the page number need to be processed
    :param cnt_to_stop: the number of page already processed
    :param break_page: the number of page which didn't download successfully due to the urlerror etc
    :param start: the start time of the monitor
    :param temp_size: the total size of the file which has been download
    :return:
    """
    print(f"\n=========Check {check_id} Report========")
    print(f"\t total_page: {total_page_num}")
    print(f"\t finished_page: {cnt_to_stop}")
    remain_page = total_page_num - cnt_to_stop
    print(f"\t remain_page: {remain_page}")
    print("\t memory_used: {:.2f} MB".format(temp_size))
    page_size = 3.45*1024/34
    remain_size = max(0,page_size * (total_page_num - break_page) - temp_size)
    print("\t memory_need: {:.2f} MB".format(remain_size))
    period = time.time() - start
    print("\t run_time: {:.2f} s".format(period))
    try:
        print("\t predict_time: {:.2f} s".format(period / temp_size * remain_size))
    except ZeroDivisionError:
        print("\t predict_time: 99999 s")   # if the net is too slow to load ,the temp_size will be zero

def monitor(total_page_num):
    """
    monitor the craw thread, it will be closed until the information sent
    by the threads is equal to the page_num, and print a success information
    :param page_num: the number of page needs to be processed this time
    :return:
    """
    start = time.time()
    check_id = 0
    break_page = 0
    cnt_to_stop = 0
    temp_size = 0
    json_file = "./breakpoint.json"
    with open(json_file, "w") as f:
        json.dump(dict(), f)
    with open(json_file, "r") as f:
        info_dict = json.load(f)
    # key = 1
    while True:
        check_id += 1
        time.sleep(0.5)
        if not qe.empty():
            info = qe.get()
            if info != 1:  # find error
                key = time.strftime("%Y-%m-%d %H:%M:%S",
                                    time.localtime())


                info_dict[f"{key}"] = info
                with open(json_file, "w") as f:
                    json.dump(info_dict,f)
                break_page += 1
                # key += 1
            else: # successfully
                cnt_to_stop += 1
                if cnt_to_stop == total_page_num:
                    print("successfully download the data!")
                    break
        if not qs.empty():
            temp_size += qs.get()
        if check_id % 10 == 0:
            # print(break_page)
            show_status(check_id,total_page_num,cnt_to_stop,break_page,start,temp_size)
    qe.task_done()
    with open(json_file, 'w') as f:
        json.dump(info_dict, f)
    print(break_page)
    show_status(check_id,total_page_num,cnt_to_stop,break_page,start,temp_size)
    print("close: monitor ! ")





if __name__ == '__main__':
	# CONFIG
    # setting number of pages and number of threads
    page_num = 35
    num_craw_threads = 7
    # setting the breakpoint information via breakpoint.json
    # breakpoint = 1
    start_from_break_point = 0
    if start_from_break_point == 1:
        with open("./breakpoint.json","r") as f:
            j = json.load(f)
            breakpoint = j["2020-12-06 21:30:47"]["id"]

    # GET LINKLIST
    # get the information (a link list) of main page
    baseurl = "https://www.51voa.com"
    find_link = re.compile(r'<a href="(.*?)" target="_blank">')  # create a object of regular expression to show the rules of matching
    link_list = get_link(page_num,baseurl, find_link,
                         page_start_ind = breakpoint - 1)  # if start index is 8, then will fisrt collect 9

    # GET DATA
    # Spider with multi-threads, plus a monitor thread to examing the working status 
    q = queue.Queue()   # send the raw id
    qe = queue.Queue()  # send the error to monitor
    qs = queue.Queue()  # send the file size to monitor

    data_list = []      # prepare for all work threads to write
    craw_threads = []   # the list of work threads

    # put all the resoureses to the q, which can be get by the threads competedly
    for link_ind in range(len(link_list)):   
        q.put(link_ind)
    # define the threads
    for i in range(num_craw_threads):
        t = Thread(target=craw,args=(link_list,data_list),
                   kwargs=({"start_ind":breakpoint-1}))
        craw_threads.append(t)
        t.start()
    # start the monitor threads
    tm = Thread(target=monitor,args=(page_num,))
    tm.start()

    # q.join()
    # qe.join()

    # use None to show the threads is over which can help stop the while Ture in the craw threads
    for i in range(num_craw_threads):
        q.put(None)
    for t in craw_threads:
        t.join()
    # tm.join()

    print(sys.getsizeof(data_list))
    try:
        save_data(data_list, "../results/voa.xls")
    except PermissionError:
        save_data(data_list, "../results/voa(1).xls")





