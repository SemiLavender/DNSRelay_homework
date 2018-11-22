# coding:utf-8
# Mydic.py完成本地查询
import pickle
import os
import threading

A = []
d_web_ip = {}
d_ip_web = {}
update_dic = {}


# 读取dnerelay.txt文件

def get_web_ip(flie_name):
    global A
    global d_web_ip
    global d_ip_web
    global update_dic

    data = open(flie_name)
    for each_line in data:
        try:
            (ip, site_old) = each_line.split(' ', 1)  # 将每一行中的ip地址和site地址用空格分开
            (site, nothing) = str(site_old).split('\n', 1)  # 将site地址中的换行符去掉
            d_web_ip[site] = [ip, 1]
            d_ip_web[ip] = site
        except:
            print('File error')

    # print(d_web_ip["sp8.googleusercontent.com"])
    data.close()
    pickle_name = str('new' + flie_name.split('.')[0] + '.pickle')
    # 新建一个newdnsrelay.pickle文件，存储d_web_ip,即web和ip的对应
    try:
        with open(pickle_name, 'wb') as newdnsrelay_file:
            pickle.dump(d_web_ip, newdnsrelay_file)  # 利用pickle模块将web_ip字典存储成二进制文件
    except IOError as err:
        print('File error:' + str(err))
    except pickle.PickleError as perr:
        print('Picking error' + str(perr))

    with open(pickle_name, 'rb') as f:
        global update_dic
        update_dic = pickle.load(f)
        return update_dic.copy()
    return (None)
