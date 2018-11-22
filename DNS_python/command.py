# coding:utf-8
# 获取调试信息模块，命令行解析，输入参数为dnsrelay [-d | -dd] [<dns-server>] [<db-file>]，根据解析结果返回调试信息等级:db_level值

import os


def getdb_level():
    flag = 0
    db_level = 0
    server_ip = '127.0.0.1'
    db_file = 'dnsrelay.txt'
    while flag != 1:
        print('----------------------------------------------')
        command = input('Usage: dnsrelay [-d | -dd] [<dns-server>] [<db-file>]----dnsrelay -dd 10.3.9.5 dnsrelay.txt\n')
        command = command.split()
        if len(command) == 1:
            if command[0] == 'dnsrelay':
                db_level = 0
                flag = 1
                print('无调试信息输出')
            else:
                print('Parameter error')
        elif len(command) == 2:
            if command[0] == 'dnsrelay' and command[1] == '-d':
                db_level = 1
                flag = 1
                print('调试信息级别1（仅输出时间坐标，序号，客户端IP地址，查询的域名)')
            elif command[0] == 'dnsrelay' and command[1] == '-dd':
                db_level = 2
                flag = 1
                print('调试信息级别2(输出冗长的调试信息)')
            else:
                print('Parameter error')

        elif len(command) == 3:
            if command[0] == 'dnsrelay' and command[1] == '-d' and len(command[2].split('.')) == 4:
                db_level = 1
                server_ip = command[2]
                flag = 1
                print('调试信息级别1（仅输出时间坐标，序号，客户端IP地址，查询的域名)')
            elif command[0] == 'dnsrelay' and command[1] == '-dd' and len(command[2].split('.')) == 4:
                db_level = 2
                server_ip = command[2]
                flag = 1
                print('调试信息级别2(输出冗长的调试信息)')
            else:
                print('Parameter error')
        elif len(command) == 4:
            if command[0] == 'dnsrelay' and command[1] == '-d' and len(command[2].split('.')) == 4:
                if os.path.exists(command[3]):
                    db_level = 1
                    server_ip = command[2]
                    db_file = command[3]
                    flag = 1
                    print('调试信息级别1（仅输出时间坐标，序号，客户端IP地址，查询的域名)')
                else:
                    print("' file_path '" + command[3] + "' Not found'")
            elif command[0] == 'dnsrelay' and command[1] == '-dd' and len(command[2].split('.')) == 4:
                if os.path.exists(command[3]):
                    db_level = 2
                    server_ip = command[2]
                    db_file = command[3]
                    flag = 1
                    print('调试信息级别2(输出冗长的调试信息)')
                else:
                    print("' file_path '" + command[3] + "' Not found'")
            else:
                print('Parameter error')
        else:
            print('Parameter error')

    print('----------------------------------------------')
    return db_level, server_ip, db_file

# getdb_level()
