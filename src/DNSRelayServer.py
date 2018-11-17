import socket
from concurrent.futures import ThreadPoolExecutor

from etc.conf import CONF


def Handler(request):
    """
    处理客户端发送来的数据，并返回结果
    :type request: 从客户得到的数据
    :return
    """
    isNext = True
    response = str.encode(bytes.decode(request) + " 数据被处理")
    return isNext, response


def CallBack(args):
    """
    线程回调函数
    :param args: 参数元祖（套接字连接对象，）
    :return: null
    """
    connection = args[0]
    while True:
        request = connection.recv(1024)
        isNext, response = Handler(request)
        if isNext is False:
            break
        connection.send(response)


def Connection():
    serverSocket = socket.socket()
    serverSocket.bind((CONF.Host, CONF.Port))
    executor = ThreadPoolExecutor(max_workers=CONF.Max_working)
    serverSocket.listen()
    while True:
        connection, clientIP = serverSocket.accept()

        task = executor.submit(CallBack, (connection,))
        print(task.done())


Connection()
