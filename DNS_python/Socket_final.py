# coding:utf-8
# 完成缓存检测，确定是回应，还是转发，如果是回应，确定是本地回应还是外部应答转发
import socket
import Mydic
import Charhandle
import Makeframe
import datetime
import command
import struct

# 创建套接字
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 53

# 获取调试信息等级
db_level, server_ip, db_file = command.getdb_level()
# the_dic负责从域名到IP的转换
the_dic = Mydic.get_web_ip(db_file)
# 保存客户端的请求
client_request = {}
client_request_index = {}
key_record = 0
client_wait = []
# 绑定到当前地址的53号端口
s.bind(('', port))
time_rest = 0
request_general = ''

# dnsrelay -dd 10.3.9.5 dnsrelay.txt

# 程序开始运行
print("running")
while True:
    try:
        # 接受UDP套接字的数据
        msg, (client, port) = s.recvfrom(1024)
    except:
        # 当没有接受到报文时，输出no message
        print("No message received")
        continue
    request = []
    request = list(msg)  # 接受到的UDP查询报文
    request_web = Charhandle.get_request(request[12:])  # 将查询报文报头之后的部分进行解析得到域名
    website = ''.join(request_web)  # 解析后的域名
    if (msg[2] & (1 << 7)) == 128:  # QR为1则说明是由dns服务器返回的应答报文
        answer = []
        answer = list(msg)
        print("Type:Remote Response")
        print('remote answer is:')
        print(msg)
        if db_level == 2:
            print('QR:', int(msg[2] & 1 << 7 == 128))
            print('AA:', int(msg[2] & 1 << 2 == 8))
            print('RD:', int(msg[2] & 1 == 1))
            print('RCODE:', int(msg[3] & 15))
            temp = struct.unpack('>HHIH', bytes(msg[-14:-4]))
            # print(msg[-14:-4])
            # print(temp)
            print('type:', temp[0])
            print('class:', temp[1])
            print('TTL:', temp[2])
            print('RDLENTH:', temp[3])

        if (answer[3] & 3) > 0:  # 检查RCODE是否为3，如果为3，说明是错误报文
            print("return a error message.")
        elif (answer[3] & 15) == 0:  # RCODE为0，得到一个正确的报文，返回ip地址
            response_ip = bytes([msg[-4], msg[-3], msg[-2], msg[-1]])  # 返回的报文中IP地址在报文的最后四个字节
            # print(response_ip)
            char_ip = socket.inet_ntoa(response_ip)  # 将ip转为点分格式
            print(website + ' has the ip: ' + char_ip)
            # fre = Mydic.storeForUpdate(website, char_ip)
            # print('with the frequence of ' + str(fre))

        for each_client in client_wait:
            # 判断该报文是不是由该client发出
            if (str(request[0]) + str(request[1]) + str(each_client)) in client_request:
                # 如果该报文是由该client发出的话，则进行处理
                (request_general, begin_time, oldmsg) = client_request[
                    str(request[0]) + str(request[1]) + str(each_client)]
                # client_request_index[request_general] = (client, port) 根据record编号得到对应的主机和端口
                # 这里需要考虑超时的情况
                now = datetime.datetime.now()
                delta = now - begin_time
                if db_level >= 1:
                    print("UDP报文从发送到收到回应经过了：" + str(delta.seconds) + "s")
                if delta.seconds > 2:  # 设置报文超时间隔
                    if db_level >= 1:
                        print("这是一个迟到应答")
                    frame = Makeframe.make("0.0.0.0", msg)  # 产生一个错误报文
                    s.sendto(frame, client_request_index[request_general])  # 将返回的报文直接发送给主机和端口
                    if db_level >= 1:
                        print("Response to ip and Client port:")
                        print(client_request_index[request_general])
                    # 从字典中删除这个记录
                    del client_request[str(request[0]) + str(request[1]) + str(client)]
                    break
                else:
                    if client_request_index.get(request_general) is not None:
                        # 在client_wait中找到发出这个查询报文的socket
                        s.sendto(msg, client_request_index[request_general])  # 将返回的报文直接发送给主机和端口
                        if db_level >= 1:
                            print("Response to ip and Client port:")
                            print(client_request_index[request_general])
                        # 从字典中删除这个记录
                        del client_request[str(request[0]) + str(request[1]) + str(each_client)]
                        break

    else:  # QR==0 则说明查询报文来自客户端查询
        print("Type:Client Request")
        print(msg)
        if db_level >= 1:
            print("ip and port:")
            print(client, port)
            print("Request website:" + website)
        if db_level == 2:
            print('QR:', int(msg[2] & 1 << 7 == 128))
            print('AA:', int(msg[2] & 1 << 2 == 8))
            print('RD:', int(msg[2] & 1 == 1))
            print('RCODE:', int(msg[3] & 15))

        if the_dic.get(website) is not None and request[-3] == 1:  # 只处理ipv4的查询报文):
            # 字典中有这个域名
            print("dnsrelay.txt has this domian name...")
            re_ip = the_dic.get(website)  # 查询得到的IP地址
            print(website + ' has the ip: ' + re_ip[0])
            # fre = Mydic.storeForUpdate(website)
            # print(re_ip[0] + ' with frequence ' + str(fre))
            frame = Makeframe.make(re_ip[0], msg)  # 将查询得到的IP包成帧，传回socket
            s.sendto(frame, (client, port))

        else:  # 如果字典中没有这个网址的话，则询问远程服务机
            print("need to ask remote server")
            if db_level >= 1:
                print("报文ID为：")
                print(str(request[0]) + str(request[1]))
            key_record = key_record + 1  # 编号自增1
            request_general = key_record  # 记录当前的编号
            # request是接受到的UDP查询报文
            # request[0] + request[1]是报文ID，用ID和client（id地址）一起标识一个请求
            # 用于ID转换
            client_request[str(request[0]) + str(request[1]) + str(client)] = (
                request_general, datetime.datetime.now(), msg)  # 存储当前请求编号和发送时间
            client_request_index[request_general] = (client, port)

            if client not in client_wait:
                client_wait.append(client)
            # select authority DNS server as you wish
            s.sendto(msg, (server_ip, 53))  # 将报文转发给默认dns服务器

    now = datetime.datetime.now()
    for key, value in client_request.items():
        delta = now - value[1]
        # print(key)
        # print("时间间隔为:"+ str(delta.seconds) + 's')
        if delta.seconds >= 1:  # 设置超时间隔
            # 报文超时，进行处理
            print("###################")
            print("超时未应答，返回报文Non-existent domain")
            frame = Makeframe.make("0.0.0.0", value[2])  # 产生一个错误报文
            my_key = value[0]
            s.sendto(frame, client_request_index[my_key])  # 将返回的报文直接发送给主机和端口
            print("Response to ip and Client port:")
            print(client_request_index[my_key])
            print("##################")
            # 从字典中删除这个记录
            del client_request[key]
            break

    # time_rest = time_rest + 1
    #
    # try:
    #     if(time_rest == 50):
    #         print("pay attention")
    #         print("####################")
    #         Mydic.updateCache()
    #         print("####################")
    #         the_dic = Mydic.get_web_ip()
    #         time_rest = 0
    # except:
    #     print('not valid frequence')

    print('------------------')

s.close()
