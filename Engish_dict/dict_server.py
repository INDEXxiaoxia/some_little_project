'''
name:
date:
email:
modules:
'''
from socket import *
import os
import time
import signal
import pymysql
import sys
print('waiting for content...')
#定义全局变量
DICT_TEXT='./dict.txt'
HOST='0.0.0.0'
PORT=8000
ADDR=(HOST,PORT)

#流程控制
def main():
    #创建数据库链接
    db=pymysql.connect('localhost','root','123456','dict')
    #创建套接字
    s=socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)
    #忽略子进程信号,,僵尸进城
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try:
            c,addr=s.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        #创建子进程
        pid=os.fork()
        if pid==0:
            s.close()
            do_child(c,db)#子进程函数
            sys.exit()
        else:
            c.close()
            continue
def do_child(c,db):
    #循环接收请求
    while True:
        data=c.recv(1024).decode()
        print(c.getpeername(),":",data)#
        if (not data) or (data[0] =='E'):
            c.close()
            sys.exit(0)
        elif data[0]=='R':
            do_register(c,db,data)#调用注册方法
        elif data[0]=='L':
            do_login(c,db,data)
        elif data[0]=='Q':
            do_query(c,db,data)   
        elif data[0]=='H':
            do_hist(c,db,data)             


#注册函数  
def do_register(c,db,data):
    print("注册")
    l=data.split(' ')
    name=l[1]
    passwd=l[2]
    cursor=db.cursor()
    sql="select name from user where name='%s'"%name#查找用户名是否存在
    cursor.execute(sql)
    r=cursor.fetchone()
    if r!=None:
        c.send(b'EXISTS')
        return
    #用户不存在插入用户
    sql="insert into user (name,passwd) values('%s','%s')"%(name,passwd)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except:
        db.rooback()
        c.send(b'FALL')
    else:
        print("%s注册成功"%name)
#登录函数
def do_login(c,db,data):
    print('登录操作')
    l=data.split(' ')
    name=l[1]
    passwd=l[2]
    cursor=db.cursor()
    sql="select *from user where name='%s' and passwd = '%s'"%(name,passwd)
    cursor.execute(sql)
    r=cursor.fetchone()
    if r==None:
        c.send(b'FALL')
    else:
        c.send(b'OK')

def do_query(c,db,data):
    print('查询操作')
    l=data.split(' ')
    name=l[1]
    word=l[2]
    cursor=db.cursor()
    def insert_history():
        time0=time.ctime()
        print('正在插入历史记录')
        sql="insert into hist(name,word,time) values('%s','%s','%s')"%(name,word,time0)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print('插入失败')
            db.rollback
    #文本查询
    try:
        f=open(DICT_TEXT,"rt")
    except:
        c.send(b'FALL')
        return
    for line in f:
        tmp=line.split(' ')[0]#首字母
        if tmp>word:
            c.send(b'FALL')
            f.close()
            
            return
        elif tmp == word:
            c.send(b'OK')
            time.sleep(0.1)
            c.send(line.encode())
            insert_history()
            return
    c.send(b'FALL')
    f.close()
def do_hist(c,db,data):
    print('历史记录操作')
    l=data.split(' ')
    name=l[1]
    cursor=db.cursor()
    sql="select * from hist where name='%s'"%name
    cursor.execute(sql)
    r=cursor.fetchall()
    if not r:
        c.send(b"FALL")
        return
    else:
        c.send(b'OK')
    for i in r:
        time.sleep(0.1)
        msg = "%s    %s    %s"%(i[1],i[2],i[3])
        c.send(msg.encode())
    time.sleep(0.1)
    c.send(b'##')
if __name__=="__main__":
    main()
