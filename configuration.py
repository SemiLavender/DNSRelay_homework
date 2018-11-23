# -*- coding: utf-8 -*-
class CONF:
    def __init__(self):
        pass

    @classmethod
    def conf(cls):
        conf_dict = {
            'DNSServerIP': '114.114.114.114',
            'ResourcePath': 'DNS.txt',
            'LOGLevel': 1,
            'TimeOut': 2
        }
        return conf_dict

