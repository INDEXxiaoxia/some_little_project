功能： 
httpserver
获取http请求
解析http请求
将请求发送给webframe
从WebFrame接收数据
将数据组织为Response格式发送给客户端
WebFrame：
从httpserver接收具体请求
根据请求进行逻辑处理和数据处理
静态页面
逻辑数据
将需要的数据反馈给httpserver
升级点：
1.采用httpserver和应用处理分离的模式
2.降低耦合度
3.原则上httpserver可以搭配任意的webFrame

