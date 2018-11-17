from numpy import *


class Utils:
    """
    工具类
    """

    @classmethod
    def byteArrayToShort(cls, varArray, offset):
        """
        一维字节数组转 short 值(2 字节)
        :param varArray: byte数组变量
        :param offset: 偏移量
        :return: short
        """
        return short((varArray[offset] & 0xff) << 8 | (varArray[offset + 1] & 0xff))

    @classmethod
    def shortToByteArray(cls, varShort):
        """
        将 short 类型数据转为 byte[]
        :param varShort: short 变量
        :return: byte类型的数组
        """
        return [byte((varShort >> 8) & 0xff), byte(varShort & 0xff)]

    @classmethod
    def byteToInt(cls, varShort):
        """
        byte 转 int
        :param varShort: short 变量
        :return: int
        """
        return varShort & 0xff

    @classmethod
    def byteArrayToInt(cls, varArray, offset):
        """
        一维字节数组转 int 值(4 字节)
        :param offset: 偏移量
        :param varArray: byte数组
        :return: int
        """
        value = 0
        for i in range(4):
            shift = (4 - 1 - i) * 8
            value += (varArray[i] & 0x000000ff) << shift
        return value

    @classmethod
    def intToByteArray(cls, varInt):
        """
        将 int 类型数据转为 byte[]
        :param varInt: 整型变量
        :return: byte数组
        """
        return [byte((varInt >> 24) & 0xff), byte((varInt >> 16) & 0xff),
                byte((varInt >> 8) & 0xff), byte(varInt & 0xff)]

    @classmethod
    def domainTobyte(cls, domain):
        re = b''
        for substr in domain.split('.'):
            re += (len(substr) + str.encode(substr))
