#coding:utf-8
import threading
import socketserver
import Mydic
import Charhandle
import Makeframe
import datetime
import socket
import command
import struct

db_level,server_ip,db_file=command.getdb_level()#获取调试信息等级
the_dic = Mydic.get_web_ip(db_file)#从newdnsrelay.pickle中读取数据
client_request = {}#客户端查询(报文ID:index)
client_request_index = {}#客户端查询索引(index:(clientIP,port))，一般来讲由外部dns返回的应答报文ID找到index，再由index找到发送该报文的clientIP和port
reverse_map = {}
key_record = 0#发送的报文数，用做index
client_wait = []#

time_rest = 0
request_general = ''

#dnsrelay -dd 10.3.9.5 dnsrelay.txt


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        global the_dic  # 从newdnsrelay.pickle中读取数据
        global client_request  # 客户端查询(报文ID:index)
        global client_request_index   # 客户端查询索引(index:(clientIP,port))，一般来讲由外部dns返回的应答报文ID找到index，再由index找到发送该报文的clientIP和port
        global reverse_map
        global key_record  # 发送的报文数，用做index
        global client_wait   #
        global time_rest
        global request_general

        msg = self.request[0]#msg为接收到的报文,self.client_address为（发送该报文的客户端的IP，接受端口）
        Socket = self.request[1]#socket为套接字
        request = list(msg)

        request_web = Charhandle.get_request(request[12:])
        website = ''.join(request_web)  # 解析后的网址
        #print(request[-3])
        #if (request[-3]==1):  # 只处理ipv4的查询报文
        print('接收到的报文:\n', msg)
        print("Type:Client Request")
        if db_level >= 1:
            print("ip and port:")
            print(self.client_address)
            print("Request website:" + website)
            print('time', datetime.datetime.now())
        if db_level == 2:
            print('QR:', int(msg[2] & 1 << 7 == 128))
            print('AA:', int(msg[2] & 1 << 2 == 8))
            print('RD:', int(msg[2] & 1 == 1))
            print('RCODE:', int(msg[3] & 15))

        if (the_dic.get(website) != None and request[-3] == 1):
            # 字典中有这个域名
            print("dnsrelay.txt has this domian name...")
            # print("Request website:" + website)
            re_ip = the_dic.get(website)
            print(website + ' has the ip: ' + re_ip[0])
            # fre = Mydic.storeForUpdate(website)
            # print(re_ip[0] + ' with frequence ' + str(fre))
            frame = Makeframe.make(re_ip[0], msg)  # 将ip包成帧，传回client port
            Socket.sendto(frame, self.client_address)

        else:  # 如果字典中没有这个网址的话，则询问远程服务机
            print("need to ask remote server")
            if db_level >= 1:
                print("报文ID为：")
                print(str(request[0]) + str(request[1]))
            key_record = key_record + 1
            request_general = key_record
            client_request[str(request[0]) + str(request[1]) + str(self.client_address[0])] = request_general
            client_request_index[request_general] = self.client_address

            if self.client_address[0] not in client_wait:
                client_wait.append(self.client_address[0])
            # select authority DNS server as you wish
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # s.bind(('localhost', 53))
            s.sendto(msg, (server_ip, 53))
            socket.setdefaulttimeout(3)
            try:
                msg, (client, port) = s.recvfrom(1024)
                print('------------------')
                print("Type:Remote Response")
                print("remote answer is:\n", msg)
                # print(msg[-1])
                response_ip = bytes([msg[-4], msg[-3], msg[-2], msg[-1]])  # msg最后四位为ip的字节码
                char_ip = socket.inet_ntoa(response_ip)  # 将ip由字节码(长度为4个字节的二进制字符串)的形式\x转换为IPV4地址字符串 109.xx.xx.xx
                if db_level >= 1:
                    print('port:', port)
                    # print("response_ip:", response_ip)
                    print('time', datetime.datetime.now())
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
                print(website + ' has the ip: ' + char_ip)
                # fre = Mydic.storeForUpdate(website,
                #                            char_ip)  # 更新newdnsrelay.pickle,若该域名-IP在本地已存在，则frequence+1，否则record for a new site
                # print(' with the frequence of ' + str(fre))

                for each_client in client_wait:
                    my_key = client_request[str(request[0]) + str(request[1]) + str(each_client)]
                    if client_request_index.get(my_key) != None:
                        Socket.sendto(msg, client_request_index[my_key])  # 找到发送查询报文但因为需要远程服务机查询而进行等待的的主机IP将该响应报文发送过去
                        if db_level >= 1:
                            print("Response to ip and Client port:")
                            print(client_request_index[my_key])
                            break
            except:
                print('请求超时')
                for each_client in client_wait:
                    my_key = client_request[str(request[0]) + str(request[1]) + str(each_client)]
                    if client_request_index.get(my_key) != None:
                        frame = Makeframe.make("0.0.0.0", msg)  # 产生一个错误报文
                        Socket.sendto(frame, client_request_index[my_key])
                        print(frame)
                        print('产生一个错误报文并发送',client_request_index[my_key])
                        break

        print('------------------')

            # socket.sendto(msg.upper(), self.client_address)
            # response = bytes("{}: {}".format(cur_thread.name, msg), 'ascii')
            # self.request.sendall(response)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

# def client(ip, port, message):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#         sock.connect((ip, port))
#         sock.sendall(bytes(message, 'ascii'))
#         response = str(sock.recv(1024), 'ascii')
#         print("Received: {}".format(response))

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 53
    print("running")  # 程序开始运行
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    with server:
        ip, port = server.server_address
        server.serve_forever()
        # Start a thread with the server -- that thread will then start one
        # more thread for each request