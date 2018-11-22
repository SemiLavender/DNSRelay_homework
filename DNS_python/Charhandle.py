# coding:utf-8
# DNS查询报文中问题部分的格式为：查询名、查询类型、查询类
# 查询名是要查找的名字，它是一个或多个标识符的序列。
# 每个标识符以首字节的计数值来说明随后标识符的字节长度，每个名字以最后字节为0借书，长度为0的标识符是根标识符。
# get_request函数用于将查询名还原为可用于查找的域名。


def get_request(your_list):
    my_list = []
    new_list = []
    my_list.extend(your_list)  # 为什么用extend?list()能否替代
    length = my_list[0]
    # ord()函数以一个字符作为参数，返回对应的ASCII数值
    try:
        while length != 0:
            str = ""
            for i in range(1, length + 1):
                str += chr(my_list[i])
            new_list.append(str)
            my_list[0:length + 1] = []
            length = my_list[0]
            new_list.append('.')
    except IndexError:
        print("报文格式错误！")
    new_list.pop()  # 去掉最后的'.'
    return new_list
