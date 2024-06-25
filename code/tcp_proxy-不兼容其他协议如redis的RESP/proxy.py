# =-= coding: utf8 =-= #

import sys
import socket
import threading
import time

HEX_FILTER = "".join([(len(repr(chr(i))) == 3) and chr(i) or "." for i in range(256)])


def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        try:
            src = src.decode("utf-8")
        except UnicodeDecodeError:
            src = src.decode("iso-8859-1")
    results = list()
    for i in range(0, len(src), length):  # range(开始, 末尾, 步进)
        word = str(src[i : i + length])
        # translate 会根据 HEX_FILTER 的列表推导式进行映射：
        #   将(len(repr(chr(i))) == 3)的映射为“chr(i)”;
        #   将(len(repr(chr(i))) 1= 3)映射为“.”：
        printable = word.translate(HEX_FILTER)
        hexa = " ".join(
            [f"{ord(c):02X}" for c in word]
        )  # 02X 表示以长度为2、大写的16进制输出；二进制为b；八进制为o
        hexwidth = length * 3
        results.append(f"{i:04x}    {hexa:<{hexwidth}}  {printable}")
    if show:
        for line in results:
            print(line)
    else:
        return results


def receive_from(connection):
    buffer = b""
    local_time = time.localtime(time.time())
    now_time = f"{local_time.tm_year}/{local_time.tm_mon}/{local_time.tm_mday} {local_time.tm_hour}:{local_time.tm_min}:{local_time.tm_sec}"
    print(f"[{now_time}] [*] Receiving...")
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
        local_time = time.localtime(time.time())
        now_time = f"{local_time.tm_year}/{local_time.tm_mon}/{local_time.tm_mday} {local_time.tm_hour}:{local_time.tm_min}:{local_time.tm_sec}"
        print(f"[{now_time}] [*] Recevied!")
    except Exception as e:
        local_time = time.localtime(time.time())
        now_time = f"{local_time.tm_year}/{local_time.tm_mon}/{local_time.tm_mday} {local_time.tm_hour}:{local_time.tm_min}:{local_time.tm_sec}"
        print(f"[{now_time}] [!] Problem on connection: %r" % e)
    return buffer


def request_handler(buffer):
    # 请求修改.....
    """
    直接通过这里修改然后return
    """
    return buffer


def response_handler(buffer):
    # 响应修改......
    """
    直接通过这里修改然后return
    """
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)

    if len(remote_buffer):
        print(f"[<==] Sending {len(remote_buffer)} bytes to localhost.")
        client_socket.send(remote_buffer)
    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print(f"[==>] Recevied {len(local_buffer)} bytes from localhost.")
            hexdump(local_buffer)

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print(f"[==>] Recevied {len(remote_buffer)} bytes from remote.")
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sending to localhost.")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break


def server_loop(local_host, local_port, remote_host, remote_port, recevie_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print("[!] Problem on bind: %r" % e)

        print(f"[!] Failed to listen on {local_host}:{local_port}")
        print("[!] Check for other listening sockets or correct permissions")
        sys.exit(0)

    print(f"[*] Listening on {local_host}:{local_port}")
    server.listen(5)
    client_socket, addr = server.accept()
    print(f"> Recevied incoming connection from {addr[0]}:{addr[1]}")
    proxy_thread = threading.Thread(
        target=proxy_handler,
        args=(client_socket, remote_host, remote_port, recevie_first),
    )
    proxy_thread.start()


def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport]", end="")
        print("[remotehost] [remoteport] [recevie_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit()

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    recevie_first = sys.argv[5]

    if recevie_first == "True":
        recevie_first = True
    else:
        recevie_first = False

    server_loop(local_host, local_port, remote_host, remote_port, recevie_first)


if __name__ == "__main__":
    main()
