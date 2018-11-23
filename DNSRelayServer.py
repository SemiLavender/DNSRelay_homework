# -*- coding: utf-8 -*-

import datetime
import socket
import logging

# 创建套接字对象
from InputHandler import InputHandler
from PackageHandler import PackageHandler
from ResponseHandler import ResponseHandler
from configuration import CONF

Timeout = CONF.conf()['TimeOut']

socketObject = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 获得服务器IP 和 返回DNS解析字典以及日志等级 log_level = 1 为'error'  and 2 = 'debug' and 3 = 'info'
serverIP, info_dic, log_level = InputHandler.getServerIPAndDNSInfo(InputHandler())
# 设置日志等级
if log_level == 1:
    print(log_level)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
elif log_level == 2:
    print(log_level)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    print(log_level)
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
# 保存客户端的请求信息
client_request = {}
client_request_map = {}
key_record = 0
client_wait = []
# 绑定监听
socketObject.bind(('', 53))

time_rest = 0
requestID = ''
print("..........DNSRelayServer Status: ACTIVE..........")
while True:
    try:
        # 接受UDP套接字的数据
        msg, (clientIP, clientPort) = socketObject.recvfrom(1024)
        print('##############  NEW MESSAGE  ###########')
        logger.info('requestMessage from IP and Port: %s:%d' % (clientIP, clientPort))
        logger.info('requestMessage: %s' % msg)
    except:
        logger.debug('There is no message!')
        continue
    request = list(msg)
    # 数据包请求的域名
    requestDomainName = ''.join(PackageHandler.packageHandler(request[12:]))
    # 判断是否为客户端发过来的消息 QR ==0
    if (msg[2] & (1 << 7)) == 0:
        logger.info('requestDomainName: %s' % requestDomainName)
        logger.info('Message Type: Client Data')
        logger.debug('clientIP and clientPort: %s:%d' % (clientIP, clientPort))
        logger.debug('Request website: %s' % requestDomainName)
        # 如果本地有这个域名的IPv4地址
        if info_dic.get(requestDomainName) is not None and request[-3] == 1:
            logger.info('DNSRelayServer has this domain_name.')
            responseIP = info_dic.get(requestDomainName)
            logger.info('Doamin_Name %s \'s IP is %s ' % (requestDomainName, responseIP))
            response = ResponseHandler.responseHandler(responseIP, msg)
            logger.debug('responseMessage:%s' % response)
            logger.info('the response message send to address %s:%d' % (clientIP, clientPort))
            socketObject.sendto(response, (clientIP, clientPort))
        # 本地不存在域名
        else:
            logger.info('The request need to send to remote server.')
            logger.info('报文ID:%s' % (str(request[0]) + str(request[1])))
            # 编号自加一
            key_record = key_record + 1
            requestID = key_record
            # 存储当前请求编号和发送时间以及信息
            client_request[str(request[0]) + str(request[1]) + str(clientIP)] = (
                requestID, datetime.datetime.now(), msg)
            logger.debug('requestID: %s and request time: %s ' % (requestID, datetime.datetime.now()))
            logger.debug('msg: %s' % msg)
            # 让请求的ID和请求的地址映射
            client_request_map[requestID] = (clientIP, clientPort)
            # 加入等待返回信息队列
            if clientIP not in client_wait:
                client_wait.append(clientIP)
            logger.info('message was sent to remote server %s:%s' % (serverIP, 53))
            socketObject.sendto(msg, (serverIP, 53))
    # 远端dns server返回的数据 QR == 1
    else:
        logger.info('Message Type: Remote Data')
        answer = list(msg)
        logger.debug('msg: %s' % msg)
        # 检查RCODE是否为3，如果为3，说明是错误报文
        if (answer[3] & 3) > 0:
            logger.error('The remote data is error message!')
        # RCODE为0，得到一个正确的报文，返回ip地址
        elif (answer[3] & 15) == 0:
            responseIP = bytes([msg[-4], msg[-3], msg[-2], msg[-1]])
            responseIP = socket.inet_ntoa(responseIP)
            logger.debug('the request domain name\'s ip is: %s' % responseIP)
        for client in client_wait:
            # 如果该报文是由该client发出的话，则进行处理
            tmp_str = str(request[0]) + str(request[1]) + str(client)
            if tmp_str in client_request:
                (requestID, begin_time, oldMsg) = client_request[tmp_str]
                deltaTime = datetime.datetime.now() - begin_time
                logger.info('UDP报文从发送到收到回应经过了：%s' % str(deltaTime))
                if deltaTime.seconds > Timeout:
                    logger.debug('这是一个迟到应答.')
                    #   生成错误报文
                    response = ResponseHandler.responseHandler('0.0.0.0', msg)
                    logger.debug('time out response: %s' % response)
                    socketObject.sendto(response, client_request_map[requestID])
                    logger.debug('remove the {%s %s %s}from client_request.' % client_request[tmp_str])
                    del client_request[tmp_str]
                    break
                else:
                    if client_request_map.get(requestID) is not None:
                        logger.debug('客户端在等待队列。')
                        socketObject.sendto(msg, client_request_map[requestID])
                        logger.info('Response to ip and Client port:%s %s' % client_request_map[requestID])
                        # 把这次查找的域名加入到本地
                        info_dic['requestDomainName'] = responseIP
                        del client_request[tmp_str]
                        break
    now = datetime.datetime.now()
    logger.debug('检测请求队列中请求是否超时')
    for key, value in client_request.items():
        delta = now - value[1]
        if delta.seconds >= 1:
            logger.debug('进行超时处理。')
            logger.info('超时未应答，返回报文Non-existent domain')
            print(value[2])
            response = ResponseHandler.responseHandler('0.0.0.0', value[2])
            logger.info('response is : %s' % response)
            socketObject.sendto(response, client_request_map[value[0]])
            logger.info('Response to ip and Client port:%s %s' % client_request_map[value[0]])
            del client_request[key]
            break
socketObject.close()



