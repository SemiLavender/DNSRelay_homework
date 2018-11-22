

#coding:utf-8
#成帧模块，形成对外围权威服务器的询问帧
import socket

def make(re_ip, msg):
    print("msg:")
    print(msg)
    temp_list = []
    for ch in msg:
        temp_list.append(chr(ch))

    header = ord(temp_list[2])
    header = header | 1<<7
    temp_list[2] = chr(header)

    #问题数1，资源记录数1，授权资源记录数0，额外资源记录数0
    temp_list[4:12] = ['\x00','\x01','\x00','\x01','\x00','\x00','\x00','\x00']
    print("temp_list:")
    print(temp_list)
    temp_list = temp_list + ['\xc0','\x0c','\x00','\x01','\x00','\x01','\x00','\x00','\x02','\x58','\x00','\x04']

    #inet_aton(string) -> bytes giving packed 32-bit IP representation
    dive_ip = socket.inet_aton(re_ip)

    re_msg = "".join(temp_list).encode()
    re_msg += dive_ip
    print(re_msg)
    return re_msg
