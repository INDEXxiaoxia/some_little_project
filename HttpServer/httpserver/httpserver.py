# coding=utf-8
'''
name:INDEXxiaoxia
time:2018-09-28
email:
'''

from socket import *
import sys
import re
from threading import Thread
from setting import *
import time


class HTTPServer(object):
    def __init__(self, addr=('0.0.0.0', 80)):
        self.sockfd = socket()  # 创建ＴＣＰ套接字
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 配置套接字属性
        self.addr = addr
        self.bind(addr)

    def bind(self, addr):
        self.ip = addr[0]
        self.port = addr[1]
        self.sockfd.bind(addr)  # 绑定地址

    def serve_forver(self):
        '''启动ｈｔｔｐ服务器'''
        self.sockfd.listen(10)
        print('正在监听:%d' % self.port)
        while True:
            connfd, addr = self.sockfd.accept()  # 监听等待客户端链接,接收客户端套接字与地址
            print('已连接到', addr)
            handle_client = Thread(
                target=self.handle_request, args=(connfd,))  # 每连接一个客户端创建一个线程
            handle_client.setDaemon(True)
            handle_client.start()

    def handle_request(self, connfd):
        # 接收浏览器请求
        request = connfd.recv(4096)  # 接收请求内容
        request_lines = request.splitlines()
        # 获取请求行
        request_line = request_lines[0].decode()
        # 正则表达式提取方法和请求内容
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>/\S*)'
        try:
            # 捕获组的字典，名字为键，内容为值
            env = re.match(pattern, request_line).groupdict()
        except:
            response_headlers = "HTTP/1.1 500 Server ERROR! \r\n"
            response_headlers += '\r\n'
            response_body = "Server Error"
            response = response_handlers+response_body
            connfd.send(response.encode())  # 给客户端返回异常信息
            return
        print(env)  # {'METHOD': 'GET', 'PATH': '/'}
        # 发送给ｆｌａｍｅ得到返回结果
        status, response_body = self.send_request(env['METHOD'], env['PATH'])
        # 根据相应吗组织响应内容
        print('》》》》》》》》》》》。',status)
        response_headlers =self.get_headlers(status)
        # 将结果组织为ｈｔｔｐ　ｒｅｓｐｏｎｓｅ发送给客户端

        response = response_headlers+response_body
        connfd.send(response.encode())
        connfd.close()

    # 和ｆｒａｍｅ交互发送ｒｅｑｕｅｓｔｓ获取ｒｅｓｐｏｎｓｅ
    def send_request(self, method, path):
        s = socket()
        s.connect(frame_addr)
        # 向webframe发送method he path
        s.send(method.encode())
        time.sleep(0.1)
        s.send(path.encode())

        status=s.recv(128).decode()
        response_body=s.recv(4096).decode()
        return 200, response_body

    def get_headlers(self,status):
        if status == 200:
            response_headlers="HTTP/1.1 200 OK\r\n"
            response_headlers+='\r\n'
        elif status == 400:
            response_headlers="HTTP/1.1 400 NOT FOUND\r\n"
            response_headlers+='\r\n'
        return response_headlers  # 返回响应头


if __name__ == "__main__":
    httpd = HTTPServer(ADDR)  # 生成对象
    httpd.serve_forver()  # 启动服务器
