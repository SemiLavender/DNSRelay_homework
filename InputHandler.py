# -*- coding: utf-8 -*-
import os
import pickle

from configuration import CONF


class InputHandler:

    def __init__(self):
        pass

    def getServerIPAndDNSInfo(self):
        self._getServerIPFromCommand()
        self._getDNSInfo()
        return self.serverIP, self.dnsInfo_dict, self.log_level

    def _getServerIPFromCommand(self):
        self.serverIP = CONF.conf()['DNSServerIP']
        self.info_path = CONF.conf()['ResourcePath']
        self.log_level = CONF.conf()['LOGLevel']
        flag = True
        while flag:
            print('<-----------DNSRelayServer---------->')
            command = input('Usage: dnsrelay [-d | -dd] [<dns-server>] [<db-file>] \n')
            command = command.split()
            if len(command) == 1:
                if command[0] == 'dnsrelay':
                    self.log_level = 0
                    flag = False
                    print('无调试信息输出')
                else:
                    print('Parameter error')
            elif len(command) == 2:
                if command[0] == 'dnsrelay' and command[1] == '-d':
                    self.log_level = 1
                    flag = False
                    print('调试信息级别1（仅输出时间坐标，序号，客户端IP地址，查询的域名)')
                elif command[0] == 'dnsrelay' and command[1] == '-dd':
                    self.log_level = 2
                    flag = False
                    print('调试信息级别2(输出冗长的调试信息)')
                else:
                    print('Parameter error')

            elif len(command) == 3:
                if command[0] == 'dnsrelay' and command[1] == '-d' and len(command[2].split('.')) == 4:
                    self.log_level = 1
                    self.serverIP = command[2]
                    flag = False
                    print('调试信息级别1（仅输出时间坐标，序号，客户端IP地址，查询的域名)')
                elif command[0] == 'dnsrelay' and command[1] == '-dd' and len(command[2].split('.')) == 4:
                    self.log_level = 2
                    self.serverIP = command[2]
                    flag = False
                    print('调试信息级别2(输出冗长的调试信息)')
                else:
                    print('Parameter error')
            elif len(command) == 4:
                if command[0] == 'dnsrelay' and command[1] == '-d' and len(command[2].split('.')) == 4:
                    if os.path.exists(command[3]):
                        self.log_level = 1
                        self.serverIP = command[2]
                        self.info_path = command[3]
                        flag = False
                        print('调试信息级别1（仅输出时间坐标，序号，客户端IP地址，查询的域名)')
                    else:
                        print("' file_path '" + command[3] + "' Not found'")
                elif command[0] == 'dnsrelay' and command[1] == '-dd' and len(command[2].split('.')) == 4:
                    if os.path.exists(command[3]):
                        self.log_level = 2
                        self.serverIP = command[2]
                        self.info_path = command[3]
                        flag = False
                        print('调试信息级别2(输出冗长的调试信息)')
                    else:
                        print("' file_path '" + command[3] + "' Not found'")
                else:
                    print('Parameter error')
            else:
                print('Parameter error')

    def _getDNSInfo(self):
        self.dnsInfo_dict = {}
        temp_dict = {}
        with open(self.info_path) as f:
            lines = f.readlines()
            for line in lines:
                tmp_ip, tmp_domain = line.strip().split(' ')
                temp_dict[tmp_domain] = tmp_ip
        new_name = 'newDNS.pickle'
        with open(self.info_path + new_name, 'wb') as f:
            pickle.dump(temp_dict, f)

        with open(self.info_path + new_name, 'rb') as f:
            self.dnsInfo_dict = pickle.load(f).copy()

    def endingResourceHandler(self, info_dict):
        pass


