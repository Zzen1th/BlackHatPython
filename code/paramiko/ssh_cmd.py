# =-= utf-8 =-= #

import paramiko


def ssh_command(hostname, server_port, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=server_port, username=user, password=passwd)

    _, stdout, stderr = client.exec_command(command)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print(">--- Output --->")
        for line in output:
            print(line.strip())


if __name__ == "__main__":
    import getpass

    username = input("Username: ")
    password = getpass.getpass()
    Hostname = input("Hostname: ") or "192.168.58.128"
    Server_port = input("Server Port or <CR>: ") or 22
    cmd = input("Command or <CR>: ") or "id"
    ssh_command(Hostname, Server_port, username, password, cmd)
