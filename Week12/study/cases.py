# -*- coding=utf-8 -*-
# @Time:
# @Author: zjh
# @File: cases.py
# @Software: PyCharm

import os
from multiprocessing import Pool,Process,Manager


def copy_file(q,file_name, old_folder_name, new_folder_name):
    """
    完成文件的复制
    :return:
    """
    # print(f"=====>模拟copy文件{file_name},从{old_folder_name}到{new_folder_name}")
    old_f = open(old_folder_name + "/" + file_name, "rb")
    content = old_f.read()

    old_f.close()

    new_f = open(new_folder_name + "/" + file_name, "wb")
    new_f.write(content)
    new_f.close()
    # 如果拷贝完了文件,那么就像队列中写入一个消息,表示已完成
    q.put(file_name)
    print(content)

def main():
    # 1.获取用户要copy的文件夹的名字
    #old_folder_name = input("请输入要copy的文件夹的名字：")
    old_folder_name = "E:\大三上2020秋\\1 现代程序设计技术\\Homework\\Week12\\study\\test"
    # 2.创建一个新的文件夹
    try:
        new_folder_name = old_folder_name + "[复件]"
        os.mkdir(new_folder_name)
    except:
        pass
    # 3.获取文件夹中所有的待copy的名字  os模块中listdir()
    file_names = os.listdir(old_folder_name)
    print(file_names)
    # 赋值源文件夹中的文件到新文件夹中的文件去
    # 4.创建进程池
    po = Pool(5)
    # 5.创建一个队列
    q = Manager().Queue()


    # 6.向进程池中添加copy文件的任务
    for file_name in file_names:
        po.apply_async(copy_file,args=(q,file_name, old_folder_name, new_folder_name))


    po.close()
    # 测一下所有文件个数
    all_file_number = len(file_names)
    copy_ok_num = 0
    while True:
        file_name = q.get()
        copy_ok_num += 1
        print(f"已经完成copy{file_name}")
        print(f"拷贝的进度为{(copy_ok_num/all_file_number)*100}%",end="\r")
        if copy_ok_num >= all_file_number:
            break

    po.join()


if __name__ == "__main__":
    main()
