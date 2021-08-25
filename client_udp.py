# CREATOR: HASHEM
import socket
SERVER_IP = '192.168.1.33'
SERVER_PORT = 1729


def main():
    num = 18
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.bind(('0.0.0.0', 1729))
    while num < 30:
        my_socket.sendto(str(num).encode(), (SERVER_IP, SERVER_PORT))
        data, remote_address = my_socket.recvfrom(1024)
        data = data.decode()
        data_list = data.split()
        if int(data_list[0]) == num+1:
            print(data_list[0]+" "+data_list[1])
        num += 1


if __name__ == '__main__':
    main()