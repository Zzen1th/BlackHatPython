# =-= coding: utf8 =-= #

import socket
import threading


IP = "0.0.0.0"
PORT = 9997


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)
    print(f"[*] Listening on {IP}:{PORT}")

    while True:
        client, address = server.accept()
        print(f"[*] Accepted connection from {address[0]}:{address[1]}")
        client_handle = threading.Thread(target=handle_client, args=(client,))
        client_handle.start()


def handle_client(client_socket):
    with client_socket as sock:
        req = sock.recv(4096)
        print(f"[*] Received: {req.decode('utf8')}")
        sock.send(b"ACK")


if __name__ == "__main__":
    main()
