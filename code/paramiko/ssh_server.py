# =-= coding: utf-8 =-= #

import os
import paramiko
import socket
import sys
import threading


CWD = os.path.dirname(os.path.realpath(__file__))
# 生成key： ssh-keygen -t rsa -f test_rsa.key
HOSTLEY = paramiko.RSAKey(filename=os.path.join(CWD, "test_rsa.key"))


class Server(paramiko.ServerInterface):
    def _init_(self):
        self.event = threading.Event()

    def check_channel_request(self, kind: str, chanid: int) -> int:
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username: str, password: str) -> int:
        if (username == "tim") and (password == "pass"):
            return paramiko.AUTH_SUCCESSFUL


if __name__ == "__main__":
    hostname = "192.168.58.1"
    ssh_port = 2222
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((hostname, ssh_port))
        sock.listen(100)
        print("[*] Listening for connection ... ")
        client, addr = sock.accept()
    except Exception as e:
        print(f"[-] Listen failed: {e}")
        sys.exit(1)
    else:
        print(f"[+] Got a connection! {client} {addr}")

    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(HOSTLEY)
    server = Server()
    bhSession.start_server(server=server)

    chan = bhSession.accept(20)
    if chan is None:
        print("*** No channel.")
        sys.exit(1)

    print("[+] Authenticated")
    print("[+] " + chan.recv(1024).decode())
    chan.send("Welcome to bh_ssh")
    try:
        while True:
            command = input("Command: ")
            print("> " + command)
            if command != "exit":
                chan.send(command)
                r = chan.recv(8192)
                try:
                    print(r.decode())
                except UnicodeDecodeError as e:
                    print(r.decode("GBK"))
            else:
                chan.send("exit")
                print("exiting")
                bhSession.close()
                break
    except KeyboardInterrupt:
        bhSession.close()
