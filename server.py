# CREATOR: HASHEM
import socket
SERVER_PORT = 1729


def main():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', SERVER_PORT))
    server_socket.listen(1)
    client_socket, client_address = server_socket.accept()
    while True:
        data = client_socket.recv(1024).decode()
        client_socket.send((str(int(data)+1) + " " + "abc").encode())


if __name__ == '__main__':
    main()