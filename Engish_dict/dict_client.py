#!/usr/bin/python3
#coding=utf-8

from socket import *
import sys
import getpass

#创建网络连接
def main():
    if len(sys.argv)<3:
        print("argv is error")
        return
    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    s=socket()
    try:
        s.connect((HOST,PORT))
    except Exception as e:
        print(e)
        return
    while True:
        print("======WELCOME======")
        print("1.注册2.登录3.退出")
        print("===================")
        cmd=input("输入>>")
        s.send(cmd.encode())
        if cmd not in["1","2","3"]:
            print('输入错误!!!')
            sys.stdin.flush()#清除标准输入
        elif cmd == '1':
            r=do_register(s)
            if r==0:
                print('注册成功')
                # login(s,name)#自动登录进去
            elif r==1:
                print('用户存在')
            else:
                print('注册失败')
        elif cmd=='2':
            name=do_login(s)
            if name:
                print('登录成功')
                login(s,name)

            else:
                print('用户名或密码错误')
        elif cmd=='3':
            s.send(b'E')
            sys.exit('退出')



def do_register(s):
    while True:
        name=input("用户名:")
        passwd=getpass.getpass('密码:')
        if (' ' in name) or (' ' in passwd):
            print("用户名或密码中不能有空格")
            continue
        msg='R {} {}'.format(name,passwd)
        s.send(msg.encode())#发送请求
        data=s.recv(128).decode()#等待回复
        if data == "OK":#成功
            return 0
        elif data == 'EXISTS':#用户名已存在
            return 1
        else:
            return 2
    
    s.send(msg.encode())
    data=s.recv(1024).decode()
    print(data)
def do_login(s):
    name=input("用户名:")
    passwd=getpass.getpass('密码:')
    msg='L {} {}'.format(name,passwd)
    s.send(msg.encode())#发送请求
    data=s.recv(128).decode()#等待回复
    if data =='OK':#登录成功
        return name
    else:#失败
        return
def login(s,name):
    while True:
        print("=====查询界面=====")
        print("1.查词2.记录3.退出")
        print("=================")   
        cmd=input("输入>>")
        s.send(cmd.encode())
        if cmd not in["1","2","3"]:
            print('输入错误!!!')
            sys.stdin.flush()#清除标准输入
        elif cmd == '1':
            print('查词启动')
            do_query(s,name)

        elif cmd=='2':
            print('记录')
            do_hist(s,name)
        elif cmd=='3':
            return

def do_query(s,name):
    while True:
        word=input('单词:')
        if word=="##":
            break
        msg='Q {} {}'.format(name,word)
        s.send(msg.encode())
        data=s.recv(128).decode()
        if data=='OK':
            data=s.recv(2048).decode()
        else:
            print('没有查到！')
        print(data)

def do_hist(s,name):
    msg='H {}'.format(name)
    s.send(msg.encode())
    data=s.recv(128).decode()
    if data=='OK':
        print('查到了')
        while True:
            data = s.recv(1024).decode()
            if data =='##':
                break
            print(data)
    else:
        print('无历史')
if __name__=="__main__":
    main()