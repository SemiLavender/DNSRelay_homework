# -*- coding: utf-8 -*-
class PackageHandler:
    def __init__(self):
        pass

    @staticmethod
    def packageHandler(msg_list):
        my_list = []
        new_list = []
        my_list.extend(msg_list)  # 为什么用extend?list()能否替代
        length = my_list[0]
        # ord()函数以一个字符作为参数，返回对应的ASCII数值
        try:
            while length != 0:
                tmp_str = ""
                for i in range(1, length + 1):
                    tmp_str += chr(my_list[i])
                new_list.append(tmp_str)
                my_list[0:length + 1] = []
                length = my_list[0]
                new_list.append('.')
        except IndexError:
            print("报文格式错误！")
        new_list.pop()  # 去掉最后的'.'
        return new_list


