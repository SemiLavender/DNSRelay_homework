import socket

from etc.conf import CONF


def packHandler(rowData):
    """
    处理原生数据
    :param rowData:
    :return: isNext, request
    """
    isNext = True
    if rowData == 'exit':
        isNext = False
    return isNext, str.encode(rowData)


def unpackHandler(response):
    return bytes.decode(response)


def Connection():
    # 生成socket对象
    s = socket.socket()
    # 与服务端建立连接
    s.connect((CONF.Host, CONF.Port))
    while True:
        rowData = input()
        isNext, request = packHandler(rowData)
        s.send(request)
        if isNext is False:
            break
        result = unpackHandler(s.recv(1024))
        print(result)
    s.close()


Connection()
