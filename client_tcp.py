# CREATOR: HASHEM
import socket
SERVER_IP = ''
SERVER_PORT = 1729


def main():
    num = 18
    my_socket = socket.socket()
    my_socket.connect((SERVER_IP, SERVER_PORT))  # connect to the server
    while num < 30:
        my_socket.send(str(num).encode())
        data = my_socket.recv(1024).decode()
        data_list = data.split()
        if int(data_list[0]) == num+1:
            print(data_list[1])
        num += 1


if __name__ == '__main__':
    main()