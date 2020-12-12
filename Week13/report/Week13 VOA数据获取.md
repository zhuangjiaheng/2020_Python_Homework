## Week13 VOA数据获取

### 13.1 作业内容

利用Python的多线程实现简单的网络爬虫。以51VOA美国之音网站为例，要求实现爬虫，获取其中mp3音频以及对应的文本并进行存储。具体要求如下：

1. 通过音频列表链接：https://www.51voa.com/VOA_Standard_1.html (其中"1"可被替换为其他数字，对应翻页操作), 要求从中获取要爬取的数据页面链接。

2. 根据获取的数据页面链接列表，基于多线程实现数据下载与存储。要求获取页面中的.mp3音频文件以及对应的文本信息（其中mp3链接可在数据页面中直接找到）。

3. 爬取规模自定义，建议多运行几天，采集的数据或许下学期可以用于别的课程作为训练数据集。

4. （附加）：爬虫程序往往需要稳定运行较长的时间，因此如果你的程序突然中断或异常（比如网络或被封），如何能够快速从断点重启？

5. （附加）：爬虫程序往往需要比较友好的状态输出，因此可否专门有一个线程动态地进行输出更新，来显示当前的状态，比如程序连续运行的时长，要完成的总页面数，其中有多少已被爬取，已收集的文件占用了多少空间，大概还需要多少时间才能完成，预计需要耗费多少硬盘空间等。

提示：

1. 数据页面以及mp3文件链接可以通过观察原html网页的形式，利用beautifulsoup对页面进行解析，提取相关标签获得

2. 存储时如果使用文件系统，同一目录下的文件数避免过多，要自动构建子文件夹来进行切割。



### 13.2 爬虫实现

```python
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
```



#### 13.2.1 爬虫线程

函数介绍，指定相应的匹配模式

```python
def craw(link_list,data_list,start_ind=0):
    """
    the working function for the work thread
    :param link_list: the link_list get by the get_link data
    :param data_list: the content to save the data parse from the mp3url, share with 		 different thread,each thread extend its own data into it
    :param start_ind: remark where to start, work only if there is a breakpoint
    :return:
    """
    find_mp3 = re.compile(r'<a href="(.*?)" id="mp3">')
    replace_tag = r'</?\w+[^>]*>'
```

循环从q中获取数据（因为每次输入的链接并不一定按顺序，q需要爬取链接的下标，从0到总长度-1），通过`page_num = start_ind + link_ind + 1`转换成页面的代号，在主页面获取的`link_list`索引得到该页面下的35个数据的`url`

q：send the link id

```python
    while True:
        link_ind = q.get()
        if link_ind is None:
            break

        datas = []
        page_num = start_ind + link_ind + 1
        page = link_list[link_ind]
```

循环遍历数据页面中的每一个`url`，利用`get_data`和其中的`ask_url`访问链接，并解析网页获取其标题，音乐下载链接，文档，大小信息，存放到`datas`中，随后`extend`到所有存放数据的`data_list`的大列表中

对数据的操作需要进行异常处理，如果出现URL异常需要记录信息（如代号和原因），通过`qe`队列给`monitor`线程发送信息，以供`monitor`处理，关于`monitor`监控线程详见13.3

```python
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
```
在一个页面处理完成后，需要通过`q.task_done`来告诉队列这个页面的数据已经处理完成，通过`qe.put(1)`告诉`monitor`该线程已经处理完毕

```python
# return datas
data_list.extend(datas)
q.task_done()
qe.put(1)  # use 1 to mark the thread has done its work
print(f"close : {page_num} !" )
```


#### 13.2.2 请求网络

```python
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
```

tips：

1. 需要通过headers来伪装

![image-20201211154850511](Week13 VOA数据获取.assets/image-20201211154850511.png)

2. 将异常处理放到外面，方便进行断点的恢复

#### 13.2.3 解析主页面

```python
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
        for item in soup.find_all("a", target="_blank"):  
            # find the string with [target = "_blank"]return a list
            item = str(item)  # change the bs4 to string
            # find the link we need to download
            link = baseurl + re.findall(findlink, item)[0]  
            links.append(link)
        linklist.append(links)
    return linklist
```

#### 13.2.4 解析数据页面

```python
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
```

根据一个特定的url，解析出相关的数据，返回到data_list中。其中findmp3和replace_tag为指定的两个正则表达式的模式，分别用于找到mp3下载链接、找到html标签来替换

#### 13.2.5 存储相关

```python
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

    save_file(rf'../mp3/{package_num}/' + music_name + '.mp3', content)
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
```

`save_file`用于写文件，`download_music`调用`save_file`可以存储音乐，而`save_data`用于写下载的数据表

### 13.3 监控线程实现

显示当前状态，包括检查的唯一索引`check_id`，总页面数`total_page_num`，已经收到的页面数`cnt_to_stop`，因为网络异常下载失败的页数`break_page`，monitor线程启动时间`start`，当前已采集的数据大小`temp_size`

并可以据此推测还需要运行的时间`period`，还剩下的数据大小`remain_size`

计算`remain_size`时进行了异常处理，是为了防止网速太慢使得到了汇报时间还没有下载成功一个音频

```python
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
```

每0.5秒进行一次监控，已达到实时监控，每10s汇报一次当前状态

每当一个线程完成任务，则发送1给`monitor`线程，`monitor`对其累加，当达到`total_page_num`时关闭

利用`qs`来和爬虫线程进行通信，将每个文件的大小传给`monitor`线程

关闭前最后显示一次状态

```python
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
    # prevent local variable use before define
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
    # print(break_page)
    show_status(check_id,total_page_num,cnt_to_stop,break_page,start,temp_size)
    print("close: monitor ! ")
```

### 13.4 多线程实现

先定义一些参数，（若`start_from_break_point=0`，则从头下载，若`start_from_break_point=1`，则根据`breakpoint.json`中的断点信息进行恢复）然后通过13.2.3得到`link_list`，对`link_list`进行多线程爬虫

`q,qe,qs`分别用于线程间通信，从而实现线程之间竞争获取资源和系列操作

```python
if __name__ == '__main__':
	# CONFIG
    
    # setting number of pages and number of threads
    page_num = 2
    num_craw_threads = 2
    # setting the breakpoint information via breakpoint.json
    breakpoint = 1
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
                         page_start_ind = breakpoint - 1)  
    # if start index is 8, then will fisrt collect 9

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
```



![image-20201206232343452](Week13 VOA数据获取.assets/image-20201206232343452.png)

![image-20201206233353959](Week13 VOA数据获取.assets/image-20201206233353959.png)



### 13.4 一些表达

+ 多个线程轮流对一个数据结构进行操作

```python
if __name__ == '__main__':
    q = queue.Queue()   # send the raw id

    data_list = []      # prepare for all work threads to write
    craw_threads = []   # the list of work threads

    for link_ind in range(len(link_list)):   
        q.put(link_ind) 
    # craw函数中需要while True和q.get，并向每一个线程传输None，在craw中合理设置break来退出
    # define the threads
    for i in range(num_craw_threads):
        t = Thread(target=craw,args=(link_list,data_list),
                   kwargs=({"start_ind":breakpoint-1}))
        craw_threads.append(t)
        t.start()
```

+ 爬取网页及异常处理

```python
req = urllib.request.Request(url=url, headers=headers)
    html = ""
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    try:
        response = urllib.request.urlopen(req)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as ue:
        if hasattr(ue, "code"):
            print(ue.code)
        if hasattr(ue, "reason"):
            print(ue.reason)
```





> D:\Downloads\Anaconda\anaconda\python.exe "E:/大三上2020秋/1 现代程序设计技术/Homework/Week13/codes/VoaSpider.py"
> collect page1
> collect page2
> collect page3
> collect page4
> collect page5
> collect page6
> collect page7
> collect page8
> collect page9
> collect page10
> collect page11
> collect page12
> collect page13
> collect page14
> collect page15
> collect page16
> collect page17
> collect page18
> collect page19
> collect page20
> collect page21
> collect page22
> collect page23
> collect page24
> collect page25
> collect page26
> collect page27
> collect page28
> collect page29
> collect page30
> collect page31
> collect page32
> collect page33
> collect page34
> collect page35
>
> =========Check 10 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 14.52 MB
> 	 memory_need: 3622.19 MB
> 	 run_time: 5.25 s
> 	 predict_time: 1309.46 s
>
> =========Check 20 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 32.92 MB
> 	 memory_need: 3603.79 MB
> 	 run_time: 10.37 s
> 	 predict_time: 1135.17 s
>
> =========Check 30 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 55.98 MB
> 	 memory_need: 3580.73 MB
> 	 run_time: 15.60 s
> 	 predict_time: 998.13 s
>
> =========Check 40 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 81.53 MB
> 	 memory_need: 3555.17 MB
> 	 run_time: 21.11 s
> 	 predict_time: 920.28 s
>
> =========Check 50 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 102.53 MB
> 	 memory_need: 3534.18 MB
> 	 run_time: 26.36 s
> 	 predict_time: 908.79 s
>
> =========Check 60 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 126.68 MB
> 	 memory_need: 3510.02 MB
> 	 run_time: 31.70 s
> 	 predict_time: 878.24 s
>
> =========Check 70 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 146.51 MB
> 	 memory_need: 3490.19 MB
> 	 run_time: 36.98 s
> 	 predict_time: 880.90 s
>
> =========Check 80 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 172.87 MB
> 	 memory_need: 3463.83 MB
> 	 run_time: 42.35 s
> 	 predict_time: 848.64 s
>
> =========Check 90 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 191.50 MB
> 	 memory_need: 3445.21 MB
> 	 run_time: 47.69 s
> 	 predict_time: 857.91 s
>
> =========Check 100 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 211.83 MB
> 	 memory_need: 3424.88 MB
> 	 run_time: 52.96 s
> 	 predict_time: 856.21 s
>
> =========Check 110 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 236.42 MB
> 	 memory_need: 3400.29 MB
> 	 run_time: 58.25 s
> 	 predict_time: 837.76 s
>
> =========Check 120 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 257.52 MB
> 	 memory_need: 3379.18 MB
> 	 run_time: 63.70 s
> 	 predict_time: 835.84 s
>
> =========Check 130 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 278.50 MB
> 	 memory_need: 3358.20 MB
> 	 run_time: 69.00 s
> 	 predict_time: 832.02 s
>
> =========Check 140 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 301.05 MB
> 	 memory_need: 3335.66 MB
> 	 run_time: 74.27 s
> 	 predict_time: 822.87 s
>
> =========Check 150 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 322.99 MB
> 	 memory_need: 3313.71 MB
> 	 run_time: 79.31 s
> 	 predict_time: 813.69 s
>
> =========Check 160 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 343.03 MB
> 	 memory_need: 3293.67 MB
> 	 run_time: 84.51 s
> 	 predict_time: 811.43 s
>
> =========Check 170 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 367.21 MB
> 	 memory_need: 3269.50 MB
> 	 run_time: 89.53 s
> 	 predict_time: 797.11 s
>
> =========Check 180 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 391.51 MB
> 	 memory_need: 3245.19 MB
> 	 run_time: 94.62 s
> 	 predict_time: 784.28 s
>
> =========Check 190 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 413.92 MB
> 	 memory_need: 3222.78 MB
> 	 run_time: 99.65 s
> 	 predict_time: 775.86 s
>
> =========Check 200 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 435.40 MB
> 	 memory_need: 3201.31 MB
> 	 run_time: 104.66 s
> 	 predict_time: 769.52 s
>
> =========Check 210 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 457.84 MB
> 	 memory_need: 3178.87 MB
> 	 run_time: 109.70 s
> 	 predict_time: 761.70 s
>
> =========Check 220 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 481.72 MB
> 	 memory_need: 3154.98 MB
> 	 run_time: 114.77 s
> 	 predict_time: 751.66 s
>
> =========Check 230 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 505.90 MB
> 	 memory_need: 3130.81 MB
> 	 run_time: 119.82 s
> 	 predict_time: 741.52 s
>
> =========Check 240 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 528.81 MB
> 	 memory_need: 3107.89 MB
> 	 run_time: 124.83 s
> 	 predict_time: 733.63 s
>
> =========Check 250 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 551.05 MB
> 	 memory_need: 3085.66 MB
> 	 run_time: 129.83 s
> 	 predict_time: 727.03 s
>
> =========Check 260 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 574.17 MB
> 	 memory_need: 3062.54 MB
> 	 run_time: 134.84 s
> 	 predict_time: 719.23 s
>
> =========Check 270 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 597.66 MB
> 	 memory_need: 3039.04 MB
> 	 run_time: 139.87 s
> 	 predict_time: 711.21 s
>
> =========Check 280 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 623.11 MB
> 	 memory_need: 3013.60 MB
> 	 run_time: 145.06 s
> 	 predict_time: 701.59 s
>
> =========Check 290 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 646.93 MB
> 	 memory_need: 2989.77 MB
> 	 run_time: 150.38 s
> 	 predict_time: 694.97 s
>
> =========Check 300 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 668.96 MB
> 	 memory_need: 2967.75 MB
> 	 run_time: 155.98 s
> 	 predict_time: 692.00 s
>
> =========Check 310 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 690.21 MB
> 	 memory_need: 2946.49 MB
> 	 run_time: 161.09 s
> 	 predict_time: 687.68 s
>
> =========Check 320 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 711.45 MB
> 	 memory_need: 2925.26 MB
> 	 run_time: 166.20 s
> 	 predict_time: 683.38 s
>
> =========Check 330 Report========
> 	 total_page: 35
> 	 finished_page: 0
> 	 remain_page: 35
> 	 memory_used: 732.75 MB
> 	 memory_need: 2903.96 MB
> 	 run_time: 171.29 s
> 	 predict_time: 678.86 s
> close : 1 !
>
> =========Check 340 Report========
> 	 total_page: 35
> 	 finished_page: 1
> 	 remain_page: 34
> 	 memory_used: 742.53 MB
> 	 memory_need: 2894.18 MB
> 	 run_time: 176.38 s
> 	 predict_time: 687.48 s
>
> =========Check 350 Report========
> 	 total_page: 35
> 	 finished_page: 1
> 	 remain_page: 34
> 	 memory_used: 758.64 MB
> 	 memory_need: 2878.06 MB
> 	 run_time: 181.50 s
> 	 predict_time: 688.57 s
>
> =========Check 360 Report========
> 	 total_page: 35
> 	 finished_page: 1
> 	 remain_page: 34
> 	 memory_used: 765.38 MB
> 	 memory_need: 2871.32 MB
> 	 run_time: 186.65 s
> 	 predict_time: 700.23 s
>
> =========Check 370 Report========
> 	 total_page: 35
> 	 finished_page: 1
> 	 remain_page: 34
> 	 memory_used: 769.28 MB
> 	 memory_need: 2867.43 MB
> 	 run_time: 191.76 s
> 	 predict_time: 714.78 s
> close : 3 !
>
> =========Check 380 Report========
> 	 total_page: 35
> 	 finished_page: 2
> 	 remain_page: 33
> 	 memory_used: 775.88 MB
> 	 memory_need: 2860.83 MB
> 	 run_time: 196.98 s
> 	 predict_time: 726.31 s
> close : 5 !
>
> =========Check 390 Report========
> 	 total_page: 35
> 	 finished_page: 3
> 	 remain_page: 32
> 	 memory_used: 791.87 MB
> 	 memory_need: 2844.84 MB
> 	 run_time: 202.13 s
> 	 predict_time: 726.16 s
> close : 6 !
> close : 7 !
> close : 4 !
> close : 2 !
>
> =========Check 400 Report========
> 	 total_page: 35
> 	 finished_page: 7
> 	 remain_page: 28
> 	 memory_used: 816.82 MB
> 	 memory_need: 2819.89 MB
> 	 run_time: 207.61 s
> 	 predict_time: 716.73 s
>
> =========Check 410 Report========
> 	 total_page: 35
> 	 finished_page: 7
> 	 remain_page: 28
> 	 memory_used: 840.20 MB
> 	 memory_need: 2796.51 MB
> 	 run_time: 212.89 s
> 	 predict_time: 708.57 s
>
> =========Check 420 Report========
> 	 total_page: 35
> 	 finished_page: 7
> 	 remain_page: 28
> 	 memory_used: 866.27 MB
> 	 memory_need: 2770.43 MB
> 	 run_time: 218.39 s
> 	 predict_time: 698.44 s
>
> =========Check 430 Report========
> 	 total_page: 35
> 	 finished_page: 7
> 	 remain_page: 28
> 	 memory_used: 888.35 MB
> 	 memory_need: 2748.35 MB
> 	 run_time: 223.84 s
> 	 predict_time: 692.51 s
> 404
> Not Found
> close : 10 !
>
> =========Check 440 Report========
> 	 total_page: 35
> 	 finished_page: 8
> 	 remain_page: 27
> 	 memory_used: 909.95 MB
> 	 memory_need: 2622.85 MB
> 	 run_time: 229.49 s
> 	 predict_time: 661.48 s
>
> =========Check 450 Report========
> 	 total_page: 35
> 	 finished_page: 8
> 	 remain_page: 27
> 	 memory_used: 931.97 MB
> 	 memory_need: 2600.83 MB
> 	 run_time: 234.98 s
> 	 predict_time: 655.75 s
>
> =========Check 460 Report========
> 	 total_page: 35
> 	 finished_page: 8
> 	 remain_page: 27
> 	 memory_used: 961.38 MB
> 	 memory_need: 2571.42 MB
> 	 run_time: 240.33 s
> 	 predict_time: 642.81 s
>
> =========Check 470 Report========
> 	 total_page: 35
> 	 finished_page: 8
> 	 remain_page: 27
> 	 memory_used: 983.77 MB
> 	 memory_need: 2549.03 MB
> 	 run_time: 245.85 s
> 	 predict_time: 637.00 s
>
> =========Check 480 Report========
> 	 total_page: 35
> 	 finished_page: 8
> 	 remain_page: 27
> 	 memory_used: 1007.86 MB
> 	 memory_need: 2524.94 MB
> 	 run_time: 251.51 s
> 	 predict_time: 630.10 s
>
> =========Check 490 Report========
> 	 total_page: 35
> 	 finished_page: 8
> 	 remain_page: 27
> 	 memory_used: 1030.47 MB
> 	 memory_need: 2502.33 MB
> 	 run_time: 256.85 s
> 	 predict_time: 623.72 s
>
> =========Check 500 Report========
> 	 total_page: 35
> 	 finished_page: 8
> 	 remain_page: 27
> 	 memory_used: 1054.12 MB
> 	 memory_need: 2478.68 MB
> 	 run_time: 262.27 s
> 	 predict_time: 616.71 s
>
> =========Check 510 Report========
> 	 total_page: 35
> 	 finished_page: 8
> 	 remain_page: 27
> 	 memory_used: 1079.96 MB
> 	 memory_need: 2452.84 MB
> 	 run_time: 267.61 s
> 	 predict_time: 607.80 s
>
> =========Check 520 Report========
> 	 total_page: 35
> 	 finished_page: 8
> 	 remain_page: 27
> 	 memory_used: 1108.16 MB
> 	 memory_need: 2424.64 MB
> 	 run_time: 273.01 s
> 	 predict_time: 597.34 s
>
> =========Check 530 Report========
> 	 total_page: 35
> 	 finished_page: 8
> 	 remain_page: 27
> 	 memory_used: 1131.85 MB
> 	 memory_need: 2400.95 MB
> 	 run_time: 278.51 s
> 	 predict_time: 590.80 s
>
> =========Check 540 Report========
> 	 total_page: 35
> 	 finished_page: 8
> 	 remain_page: 27
> 	 memory_used: 1159.43 MB
> 	 memory_need: 2373.37 MB
> 	 run_time: 283.65 s
> 	 predict_time: 580.63 s
>
> =========Check 550 Report========
> 	 total_page: 35
> 	 finished_page: 8
> 	 remain_page: 27
> 	 memory_used: 1183.77 MB
> 	 memory_need: 2349.03 MB
> 	 run_time: 288.99 s
> 	 predict_time: 573.46 s
>
> =========Check 560 Report========
> 	 total_page: 35
> 	 finished_page: 8
> 	 remain_page: 27
> 	 memory_used: 1212.41 MB
> 	 memory_need: 2320.39 MB
> 	 run_time: 294.15 s
> 	 predict_time: 562.97 s
> close : 8 !
>
> =========Check 570 Report========
> 	 total_page: 35
> 	 finished_page: 9
> 	 remain_page: 26
> 	 memory_used: 1235.64 MB
> 	 memory_need: 2297.16 MB
> 	 run_time: 299.57 s
> 	 predict_time: 556.93 s
>
> =========Check 580 Report========
> 	 total_page: 35
> 	 finished_page: 9
> 	 remain_page: 26
> 	 memory_used: 1259.46 MB
> 	 memory_need: 2273.34 MB
> 	 run_time: 304.71 s
> 	 predict_time: 550.00 s
> close : 11 !
> close : 9 !
>
> =========Check 590 Report========
> 	 total_page: 35
> 	 finished_page: 11
> 	 remain_page: 24
> 	 memory_used: 1281.67 MB
> 	 memory_need: 2251.13 MB
> 	 run_time: 309.92 s
> 	 predict_time: 544.34 s
> close : 12 !
> close : 14 !
> close : 13 !
>
> =========Check 600 Report========
> 	 total_page: 35
> 	 finished_page: 14
> 	 remain_page: 21
> 	 memory_used: 1303.17 MB
> 	 memory_need: 2229.63 MB
> 	 run_time: 315.30 s
> 	 predict_time: 539.46 s
>
> =========Check 610 Report========
> 	 total_page: 35
> 	 finished_page: 14
> 	 remain_page: 21
> 	 memory_used: 1328.15 MB
> 	 memory_need: 2204.65 MB
> 	 run_time: 320.53 s
> 	 predict_time: 532.05 s
>
> =========Check 620 Report========
> 	 total_page: 35
> 	 finished_page: 14
> 	 remain_page: 21
> 	 memory_used: 1352.32 MB
> 	 memory_need: 2180.48 MB
> 	 run_time: 325.85 s
> 	 predict_time: 525.41 s
>
> =========Check 630 Report========
> 	 total_page: 35
> 	 finished_page: 14
> 	 remain_page: 21
> 	 memory_used: 1377.12 MB
> 	 memory_need: 2155.68 MB
> 	 run_time: 331.10 s
> 	 predict_time: 518.29 s
>
> =========Check 640 Report========
> 	 total_page: 35
> 	 finished_page: 14
> 	 remain_page: 21
> 	 memory_used: 1402.96 MB
> 	 memory_need: 2129.84 MB
> 	 run_time: 336.24 s
> 	 predict_time: 510.45 s
> close : 15 !
>
> =========Check 650 Report========
> 	 total_page: 35
> 	 finished_page: 15
> 	 remain_page: 20
> 	 memory_used: 1423.94 MB
> 	 memory_need: 2108.86 MB
> 	 run_time: 341.81 s
> 	 predict_time: 506.23 s
>
> =========Check 660 Report========
> 	 total_page: 35
> 	 finished_page: 15
> 	 remain_page: 20
> 	 memory_used: 1449.94 MB
> 	 memory_need: 2082.86 MB
> 	 run_time: 347.06 s
> 	 predict_time: 498.56 s
>
> =========Check 670 Report========
> 	 total_page: 35
> 	 finished_page: 15
> 	 remain_page: 20
> 	 memory_used: 1475.90 MB
> 	 memory_need: 2056.90 MB
> 	 run_time: 352.22 s
> 	 predict_time: 490.87 s
>
> =========Check 680 Report========
> 	 total_page: 35
> 	 finished_page: 15
> 	 remain_page: 20
> 	 memory_used: 1499.31 MB
> 	 memory_need: 2033.49 MB
> 	 run_time: 358.05 s
> 	 predict_time: 485.61 s
>
> =========Check 690 Report========
> 	 total_page: 35
> 	 finished_page: 15
> 	 remain_page: 20
> 	 memory_used: 1522.60 MB
> 	 memory_need: 2010.20 MB
> 	 run_time: 363.46 s
> 	 predict_time: 479.86 s
>
> =========Check 700 Report========
> 	 total_page: 35
> 	 finished_page: 15
> 	 remain_page: 20
> 	 memory_used: 1545.30 MB
> 	 memory_need: 1987.50 MB
> 	 run_time: 368.99 s
> 	 predict_time: 474.57 s
>
> =========Check 710 Report========
> 	 total_page: 35
> 	 finished_page: 15
> 	 remain_page: 20
> 	 memory_used: 1567.44 MB
> 	 memory_need: 1965.36 MB
> 	 run_time: 374.49 s
> 	 predict_time: 469.56 s
>
> =========Check 720 Report========
> 	 total_page: 35
> 	 finished_page: 15
> 	 remain_page: 20
> 	 memory_used: 1594.16 MB
> 	 memory_need: 1938.64 MB
> 	 run_time: 380.08 s
> 	 predict_time: 462.20 s
>
> =========Check 730 Report========
> 	 total_page: 35
> 	 finished_page: 15
> 	 remain_page: 20
> 	 memory_used: 1620.04 MB
> 	 memory_need: 1912.76 MB
> 	 run_time: 385.39 s
> 	 predict_time: 455.02 s
>
> =========Check 740 Report========
> 	 total_page: 35
> 	 finished_page: 15
> 	 remain_page: 20
> 	 memory_used: 1644.05 MB
> 	 memory_need: 1888.75 MB
> 	 run_time: 390.68 s
> 	 predict_time: 448.83 s
>
> =========Check 750 Report========
> 	 total_page: 35
> 	 finished_page: 15
> 	 remain_page: 20
> 	 memory_used: 1668.55 MB
> 	 memory_need: 1864.25 MB
> 	 run_time: 395.93 s
> 	 predict_time: 442.37 s
>
> =========Check 760 Report========
> 	 total_page: 35
> 	 finished_page: 15
> 	 remain_page: 20
> 	 memory_used: 1693.98 MB
> 	 memory_need: 1838.82 MB
> 	 run_time: 401.32 s
> 	 predict_time: 435.63 s
>
> =========Check 770 Report========
> 	 total_page: 35
> 	 finished_page: 15
> 	 remain_page: 20
> 	 memory_used: 1724.15 MB
> 	 memory_need: 1808.65 MB
> 	 run_time: 406.78 s
> 	 predict_time: 426.71 s
> close : 16 !
>
> =========Check 780 Report========
> 	 total_page: 35
> 	 finished_page: 16
> 	 remain_page: 19
> 	 memory_used: 1744.33 MB
> 	 memory_need: 1788.47 MB
> 	 run_time: 412.14 s
> 	 predict_time: 422.57 s
> close : 21 !
>
> =========Check 790 Report========
> 	 total_page: 35
> 	 finished_page: 17
> 	 remain_page: 18
> 	 memory_used: 1762.83 MB
> 	 memory_need: 1769.97 MB
> 	 run_time: 417.74 s
> 	 predict_time: 419.43 s
> close : 18 !
> close : 17 !
> close : 20 !
>
> =========Check 800 Report========
> 	 total_page: 35
> 	 finished_page: 20
> 	 remain_page: 15
> 	 memory_used: 1784.37 MB
> 	 memory_need: 1748.43 MB
> 	 run_time: 423.69 s
> 	 predict_time: 415.16 s
> close : 19 !
>
> =========Check 810 Report========
> 	 total_page: 35
> 	 finished_page: 21
> 	 remain_page: 14
> 	 memory_used: 1808.45 MB
> 	 memory_need: 1724.35 MB
> 	 run_time: 429.32 s
> 	 predict_time: 409.36 s
>
> =========Check 820 Report========
> 	 total_page: 35
> 	 finished_page: 21
> 	 remain_page: 14
> 	 memory_used: 1836.19 MB
> 	 memory_need: 1696.61 MB
> 	 run_time: 434.69 s
> 	 predict_time: 401.64 s
>
> =========Check 830 Report========
> 	 total_page: 35
> 	 finished_page: 21
> 	 remain_page: 14
> 	 memory_used: 1854.81 MB
> 	 memory_need: 1677.99 MB
> 	 run_time: 440.02 s
> 	 predict_time: 398.07 s
> close : 22 !
>
> =========Check 840 Report========
> 	 total_page: 35
> 	 finished_page: 22
> 	 remain_page: 13
> 	 memory_used: 1873.86 MB
> 	 memory_need: 1658.94 MB
> 	 run_time: 445.73 s
> 	 predict_time: 394.61 s
>
> =========Check 850 Report========
> 	 total_page: 35
> 	 finished_page: 22
> 	 remain_page: 13
> 	 memory_used: 1890.83 MB
> 	 memory_need: 1641.97 MB
> 	 run_time: 451.00 s
> 	 predict_time: 391.64 s
>
> =========Check 860 Report========
> 	 total_page: 35
> 	 finished_page: 22
> 	 remain_page: 13
> 	 memory_used: 1910.43 MB
> 	 memory_need: 1622.37 MB
> 	 run_time: 456.52 s
> 	 predict_time: 387.68 s
>
> =========Check 870 Report========
> 	 total_page: 35
> 	 finished_page: 22
> 	 remain_page: 13
> 	 memory_used: 1935.15 MB
> 	 memory_need: 1597.65 MB
> 	 run_time: 461.92 s
> 	 predict_time: 381.36 s
>
> =========Check 880 Report========
> 	 total_page: 35
> 	 finished_page: 22
> 	 remain_page: 13
> 	 memory_used: 1955.31 MB
> 	 memory_need: 1577.49 MB
> 	 run_time: 467.45 s
> 	 predict_time: 377.13 s
>
> =========Check 890 Report========
> 	 total_page: 35
> 	 finished_page: 22
> 	 remain_page: 13
> 	 memory_used: 1975.06 MB
> 	 memory_need: 1557.74 MB
> 	 run_time: 472.91 s
> 	 predict_time: 372.99 s
>
> =========Check 900 Report========
> 	 total_page: 35
> 	 finished_page: 22
> 	 remain_page: 13
> 	 memory_used: 1992.05 MB
> 	 memory_need: 1540.75 MB
> 	 run_time: 478.24 s
> 	 predict_time: 369.90 s
>
> =========Check 910 Report========
> 	 total_page: 35
> 	 finished_page: 22
> 	 remain_page: 13
> 	 memory_used: 2015.70 MB
> 	 memory_need: 1517.10 MB
> 	 run_time: 483.44 s
> 	 predict_time: 363.86 s
>
> =========Check 920 Report========
> 	 total_page: 35
> 	 finished_page: 22
> 	 remain_page: 13
> 	 memory_used: 2037.73 MB
> 	 memory_need: 1495.07 MB
> 	 run_time: 488.67 s
> 	 predict_time: 358.54 s
>
> =========Check 930 Report========
> 	 total_page: 35
> 	 finished_page: 22
> 	 remain_page: 13
> 	 memory_used: 2055.66 MB
> 	 memory_need: 1477.14 MB
> 	 run_time: 494.20 s
> 	 predict_time: 355.12 s
>
> =========Check 940 Report========
> 	 total_page: 35
> 	 finished_page: 22
> 	 remain_page: 13
> 	 memory_used: 2078.59 MB
> 	 memory_need: 1454.21 MB
> 	 run_time: 499.45 s
> 	 predict_time: 349.42 s
>
> =========Check 950 Report========
> 	 total_page: 35
> 	 finished_page: 22
> 	 remain_page: 13
> 	 memory_used: 2102.93 MB
> 	 memory_need: 1429.87 MB
> 	 run_time: 504.80 s
> 	 predict_time: 343.24 s
> close : 25 !
>
> =========Check 960 Report========
> 	 total_page: 35
> 	 finished_page: 23
> 	 remain_page: 12
> 	 memory_used: 2123.08 MB
> 	 memory_need: 1409.72 MB
> 	 run_time: 510.32 s
> 	 predict_time: 338.85 s
> close : 23 !
> close : 26 !
> close : 24 !
>
> =========Check 970 Report========
> 	 total_page: 35
> 	 finished_page: 26
> 	 remain_page: 9
> 	 memory_used: 2143.54 MB
> 	 memory_need: 1389.26 MB
> 	 run_time: 515.64 s
> 	 predict_time: 334.20 s
>
> =========Check 980 Report========
> 	 total_page: 35
> 	 finished_page: 26
> 	 remain_page: 9
> 	 memory_used: 2165.29 MB
> 	 memory_need: 1367.51 MB
> 	 run_time: 521.41 s
> 	 predict_time: 329.30 s
>
> =========Check 990 Report========
> 	 total_page: 35
> 	 finished_page: 26
> 	 remain_page: 9
> 	 memory_used: 2187.15 MB
> 	 memory_need: 1345.65 MB
> 	 run_time: 526.64 s
> 	 predict_time: 324.01 s
> close : 27 !
>
> =========Check 1000 Report========
> 	 total_page: 35
> 	 finished_page: 27
> 	 remain_page: 8
> 	 memory_used: 2212.59 MB
> 	 memory_need: 1320.21 MB
> 	 run_time: 531.86 s
> 	 predict_time: 317.35 s
>
> =========Check 1010 Report========
> 	 total_page: 35
> 	 finished_page: 27
> 	 remain_page: 8
> 	 memory_used: 2237.63 MB
> 	 memory_need: 1295.17 MB
> 	 run_time: 537.02 s
> 	 predict_time: 310.83 s
>
> =========Check 1020 Report========
> 	 total_page: 35
> 	 finished_page: 27
> 	 remain_page: 8
> 	 memory_used: 2259.40 MB
> 	 memory_need: 1273.40 MB
> 	 run_time: 542.14 s
> 	 predict_time: 305.55 s
>
> =========Check 1030 Report========
> 	 total_page: 35
> 	 finished_page: 27
> 	 remain_page: 8
> 	 memory_used: 2277.28 MB
> 	 memory_need: 1255.52 MB
> 	 run_time: 547.29 s
> 	 predict_time: 301.73 s
> close : 28 !
>
> =========Check 1040 Report========
> 	 total_page: 35
> 	 finished_page: 28
> 	 remain_page: 7
> 	 memory_used: 2296.02 MB
> 	 memory_need: 1236.78 MB
> 	 run_time: 552.68 s
> 	 predict_time: 297.71 s
>
> =========Check 1050 Report========
> 	 total_page: 35
> 	 finished_page: 28
> 	 remain_page: 7
> 	 memory_used: 2318.86 MB
> 	 memory_need: 1213.94 MB
> 	 run_time: 557.93 s
> 	 predict_time: 292.08 s
> close : 29 !
>
> =========Check 1060 Report========
> 	 total_page: 35
> 	 finished_page: 29
> 	 remain_page: 6
> 	 memory_used: 2337.15 MB
> 	 memory_need: 1195.65 MB
> 	 run_time: 563.29 s
> 	 predict_time: 288.17 s
>
> =========Check 1070 Report========
> 	 total_page: 35
> 	 finished_page: 29
> 	 remain_page: 6
> 	 memory_used: 2358.24 MB
> 	 memory_need: 1174.56 MB
> 	 run_time: 568.67 s
> 	 predict_time: 283.24 s
>
> =========Check 1080 Report========
> 	 total_page: 35
> 	 finished_page: 29
> 	 remain_page: 6
> 	 memory_used: 2384.74 MB
> 	 memory_need: 1148.06 MB
> 	 run_time: 574.12 s
> 	 predict_time: 276.39 s
>
> =========Check 1090 Report========
> 	 total_page: 35
> 	 finished_page: 29
> 	 remain_page: 6
> 	 memory_used: 2406.19 MB
> 	 memory_need: 1126.61 MB
> 	 run_time: 579.40 s
> 	 predict_time: 271.28 s
>
> =========Check 1100 Report========
> 	 total_page: 35
> 	 finished_page: 29
> 	 remain_page: 6
> 	 memory_used: 2423.10 MB
> 	 memory_need: 1109.70 MB
> 	 run_time: 584.84 s
> 	 predict_time: 267.84 s
>
> =========Check 1110 Report========
> 	 total_page: 35
> 	 finished_page: 29
> 	 remain_page: 6
> 	 memory_used: 2436.88 MB
> 	 memory_need: 1095.92 MB
> 	 run_time: 590.08 s
> 	 predict_time: 265.37 s
>
> =========Check 1120 Report========
> 	 total_page: 35
> 	 finished_page: 29
> 	 remain_page: 6
> 	 memory_used: 2452.86 MB
> 	 memory_need: 1079.94 MB
> 	 run_time: 595.52 s
> 	 predict_time: 262.19 s
>
> =========Check 1130 Report========
> 	 total_page: 35
> 	 finished_page: 29
> 	 remain_page: 6
> 	 memory_used: 2492.59 MB
> 	 memory_need: 1040.21 MB
> 	 run_time: 600.74 s
> 	 predict_time: 250.70 s
>
> =========Check 1140 Report========
> 	 total_page: 35
> 	 finished_page: 29
> 	 remain_page: 6
> 	 memory_used: 2512.62 MB
> 	 memory_need: 1020.18 MB
> 	 run_time: 605.95 s
> 	 predict_time: 246.03 s
>
> =========Check 1150 Report========
> 	 total_page: 35
> 	 finished_page: 29
> 	 remain_page: 6
> 	 memory_used: 2529.68 MB
> 	 memory_need: 1003.12 MB
> 	 run_time: 611.19 s
> 	 predict_time: 242.36 s
>
> =========Check 1160 Report========
> 	 total_page: 35
> 	 finished_page: 29
> 	 remain_page: 6
> 	 memory_used: 2546.17 MB
> 	 memory_need: 986.63 MB
> 	 run_time: 616.53 s
> 	 predict_time: 238.90 s
> close : 30 !
>
> =========Check 1170 Report========
> 	 total_page: 35
> 	 finished_page: 30
> 	 remain_page: 5
> 	 memory_used: 2558.59 MB
> 	 memory_need: 974.21 MB
> 	 run_time: 621.91 s
> 	 predict_time: 236.80 s
> close : 32 !
> close : 35 !
>
> =========Check 1180 Report========
> 	 total_page: 35
> 	 finished_page: 32
> 	 remain_page: 3
> 	 memory_used: 2575.78 MB
> 	 memory_need: 957.02 MB
> 	 run_time: 627.31 s
> 	 predict_time: 233.08 s
> close : 31 !
> close : 34 !
>
> =========Check 1190 Report========
> 	 total_page: 35
> 	 finished_page: 34
> 	 remain_page: 1
> 	 memory_used: 2589.78 MB
> 	 memory_need: 943.02 MB
> 	 run_time: 632.59 s
> 	 predict_time: 230.35 s
>
> =========Check 1200 Report========
> 	 total_page: 35
> 	 finished_page: 34
> 	 remain_page: 1
> 	 memory_used: 2612.27 MB
> 	 memory_need: 920.53 MB
> 	 run_time: 637.75 s
> 	 predict_time: 224.74 s
> close : 33 !
> 15408
> successfully download the data!
> 1
>
> =========Check 1202 Report========
> 	 total_page: 35
> 	 finished_page: 35
> 	 remain_page: 0
> 	 memory_used: 2613.31 MB
> 	 memory_need: 919.49 MB
> 	 run_time: 638.95 s
> 	 predict_time: 224.81 s
> close: monitor ! 
>
> Process finished with exit code 0







+ 14页断网操作

> D:\Downloads\Anaconda\anaconda\python.exe "E:/大三上2020秋/1 现代程序设计技术/Homework/Week13/codes/VoaSpider.py"
> collect page1
> collect page2
> collect page3
> collect page4
> collect page5
> collect page6
> collect page7
> collect page8
> collect page9
> collect page10
> collect page11
> collect page12
> collect page13
> collect page14
> 0
>
> =========Check 10 Report========
> 	 total_page: 14
> 	 finished_page: 0
> 	 remain_page: 14
> 	 memory_used: 21.38 MB
> 	 memory_need: 1440.89 MB
> 	 run_time: 5.50 s
> 	 predict_time: 370.62 s
> 0
>
> =========Check 20 Report========
> 	 total_page: 14
> 	 finished_page: 0
> 	 remain_page: 14
> 	 memory_used: 28.50 MB
> 	 memory_need: 1433.77 MB
> 	 run_time: 10.64 s
> 	 predict_time: 535.39 s
> 0
>
> =========Check 30 Report========
> 	 total_page: 14
> 	 finished_page: 0
> 	 remain_page: 14
> 	 memory_used: 28.50 MB
> 	 memory_need: 1433.77 MB
> 	 run_time: 15.79 s
> 	 predict_time: 794.44 s
> [WinError 10065] 套接字操作尝试一个无法连接的主机。
> close : 7 !
> [Errno 11001] getaddrinfo failed
> close : 8 !
> [Errno 11001] getaddrinfo failed
> close : 9 !
> [Errno 11001] getaddrinfo failed
> close : 10 !
> [Errno 11001] getaddrinfo failed
> close : 11 !
> [Errno 11001] getaddrinfo failed
> close : 12 !
> [Errno 11001] getaddrinfo failed
> close : 13 !
> [Errno 11001] getaddrinfo failed
> close : 14 !
> 4
>
> =========Check 40 Report========
> 	 total_page: 14
> 	 finished_page: 4
> 	 remain_page: 10
> 	 memory_used: 28.50 MB
> 	 memory_need: 1015.98 MB
> 	 run_time: 21.07 s
> 	 predict_time: 751.16 s
> 8
>
> =========Check 50 Report========
> 	 total_page: 14
> 	 finished_page: 8
> 	 remain_page: 6
> 	 memory_used: 35.26 MB
> 	 memory_need: 591.43 MB
> 	 run_time: 26.31 s
> 	 predict_time: 441.36 s
> 8
>
> =========Check 60 Report========
> 	 total_page: 14
> 	 finished_page: 8
> 	 remain_page: 6
> 	 memory_used: 59.20 MB
> 	 memory_need: 567.49 MB
> 	 run_time: 31.59 s
> 	 predict_time: 302.85 s
> 8
>
> =========Check 70 Report========
> 	 total_page: 14
> 	 finished_page: 8
> 	 remain_page: 6
> 	 memory_used: 84.33 MB
> 	 memory_need: 542.36 MB
> 	 run_time: 36.83 s
> 	 predict_time: 236.86 s
> 8
>
> =========Check 80 Report========
> 	 total_page: 14
> 	 finished_page: 8
> 	 remain_page: 6
> 	 memory_used: 105.30 MB
> 	 memory_need: 521.39 MB
> 	 run_time: 42.01 s
> 	 predict_time: 208.03 s
> 8
>
> =========Check 90 Report========
> 	 total_page: 14
> 	 finished_page: 8
> 	 remain_page: 6
> 	 memory_used: 128.86 MB
> 	 memory_need: 497.83 MB
> 	 run_time: 47.29 s
> 	 predict_time: 182.72 s
> 8
>
> =========Check 100 Report========
> 	 total_page: 14
> 	 finished_page: 8
> 	 remain_page: 6
> 	 memory_used: 150.69 MB
> 	 memory_need: 476.00 MB
> 	 run_time: 52.77 s
> 	 predict_time: 166.70 s
> 8
>
> =========Check 110 Report========
> 	 total_page: 14
> 	 finished_page: 8
> 	 remain_page: 6
> 	 memory_used: 173.98 MB
> 	 memory_need: 452.71 MB
> 	 run_time: 58.09 s
> 	 predict_time: 151.15 s
> 8
>
> =========Check 120 Report========
> 	 total_page: 14
> 	 finished_page: 8
> 	 remain_page: 6
> 	 memory_used: 192.80 MB
> 	 memory_need: 433.89 MB
> 	 run_time: 63.42 s
> 	 predict_time: 142.71 s
> 8
>
> =========Check 130 Report========
> 	 total_page: 14
> 	 finished_page: 8
> 	 remain_page: 6
> 	 memory_used: 217.43 MB
> 	 memory_need: 409.26 MB
> 	 run_time: 68.98 s
> 	 predict_time: 129.84 s
> 8
>
> =========Check 140 Report========
> 	 total_page: 14
> 	 finished_page: 8
> 	 remain_page: 6
> 	 memory_used: 237.39 MB
> 	 memory_need: 389.30 MB
> 	 run_time: 74.34 s
> 	 predict_time: 121.90 s
> 8
>
> =========Check 150 Report========
> 	 total_page: 14
> 	 finished_page: 8
> 	 remain_page: 6
> 	 memory_used: 259.25 MB
> 	 memory_need: 367.44 MB
> 	 run_time: 79.87 s
> 	 predict_time: 113.20 s
> 8
>
> =========Check 160 Report========
> 	 total_page: 14
> 	 finished_page: 8
> 	 remain_page: 6
> 	 memory_used: 280.64 MB
> 	 memory_need: 346.05 MB
> 	 run_time: 85.52 s
> 	 predict_time: 105.46 s
> 8
>
> =========Check 170 Report========
> 	 total_page: 14
> 	 finished_page: 8
> 	 remain_page: 6
> 	 memory_used: 303.42 MB
> 	 memory_need: 323.27 MB
> 	 run_time: 90.90 s
> 	 predict_time: 96.85 s
> 8
>
> =========Check 180 Report========
> 	 total_page: 14
> 	 finished_page: 8
> 	 remain_page: 6
> 	 memory_used: 324.12 MB
> 	 memory_need: 302.57 MB
> 	 run_time: 96.51 s
> 	 predict_time: 90.09 s
> 8
>
> =========Check 190 Report========
> 	 total_page: 14
> 	 finished_page: 8
> 	 remain_page: 6
> 	 memory_used: 348.26 MB
> 	 memory_need: 278.43 MB
> 	 run_time: 101.81 s
> 	 predict_time: 81.40 s
> 8
>
> =========Check 200 Report========
> 	 total_page: 14
> 	 finished_page: 8
> 	 remain_page: 6
> 	 memory_used: 370.39 MB
> 	 memory_need: 256.30 MB
> 	 run_time: 107.15 s
> 	 predict_time: 74.15 s
> 8
>
> =========Check 210 Report========
> 	 total_page: 14
> 	 finished_page: 8
> 	 remain_page: 6
> 	 memory_used: 391.59 MB
> 	 memory_need: 235.09 MB
> 	 run_time: 112.61 s
> 	 predict_time: 67.60 s
> 8
>
> =========Check 220 Report========
> 	 total_page: 14
> 	 finished_page: 8
> 	 remain_page: 6
> 	 memory_used: 418.54 MB
> 	 memory_need: 208.15 MB
> 	 run_time: 118.26 s
> 	 predict_time: 58.81 s
> close : 3 !
> close : 6 !
> close : 2 !
> close : 4 !
> 8
>
> =========Check 230 Report========
> 	 total_page: 14
> 	 finished_page: 12
> 	 remain_page: 2
> 	 memory_used: 442.60 MB
> 	 memory_need: 184.09 MB
> 	 run_time: 123.50 s
> 	 predict_time: 51.37 s
> close : 1 !
> close : 5 !
> 2824
> successfully download the data!
> close: monitor ! 
>
> Process finished with exit code 0

breakpoint 信息

> {"2020-12-07 19:14:05": {"id": 7, "error": "URLError"}, "2020-12-07 19:14:06": {"id": 8, "error": "URLError"}, "2020-12-07 19:14:07": {"id": 9, "error": "URLError"}, "2020-12-07 19:14:08": {"id": 10, "error": "URLError"}, "2020-12-07 19:14:09": {"id": 11, "error": "URLError"}, "2020-12-07 19:14:10": {"id": 12, "error": "URLError"}, "2020-12-07 19:14:11": {"id": 13, "error": "URLError"}, "2020-12-07 19:14:12": {"id": 14, "error": "URLError"}}

