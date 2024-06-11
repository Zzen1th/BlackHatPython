# -- coding:utf8 --

import socket

target_host = "www.qq.com"
target_port = 80


# 创建一个 socket 对象
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 建立 tcp 连接
client.connect((target_host, target_port))

# 发送请求
client.send(b"GET / HTTP/1.1\r\nHost: www.qq.com\r\n\r\n")

# 接收响应
resp = client.recv(4096)

print(resp.decode())

# 关闭连接
client.close()
