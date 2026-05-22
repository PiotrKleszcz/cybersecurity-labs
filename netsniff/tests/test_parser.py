import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import MagicMock
from src.packet_parser import parse_packet

def make_pkt(layers):
    pkt = MagicMock()
    pkt.haslayer = lambda l: l in layers
    if 'IP' in layers:
        pkt.__getitem__ = lambda self, l: MagicMock(
            src="192.168.253.142",
            dst="192.168.253.141",
            sport=12345,
            dport=80,
            flags="S",
            type=8
        )
    if 'ARP' in layers:
        pkt.__getitem__ = lambda self, l: MagicMock(
            psrc="192.168.253.142",
            pdst="192.168.253.141"
        )
    return pkt

def test_tcp_packet():
    from scapy.all import IP, TCP, Ether
    from scapy.layers.inet import IP, TCP
    pkt = Ether()/IP(src="192.168.253.142", dst="192.168.253.141")/TCP(sport=12345, dport=80, flags="S")
    result = parse_packet(pkt)
    assert result is not None
    assert result["proto"] == "TCP"
    assert result["src"] == "192.168.253.142"
    assert result["dport"] == 80
    print("[+] test_tcp_packet passed")

def test_icmp_packet():
    from scapy.all import IP, ICMP, Ether
    pkt = Ether()/IP(src="192.168.253.142", dst="192.168.253.141")/ICMP(type=8)
    result = parse_packet(pkt)
    assert result is not None
    assert result["proto"] == "ICMP"
    assert result["type"] == 8
    print("[+] test_icmp_packet passed")

def test_arp_packet():
    from scapy.all import ARP, Ether
    pkt = Ether()/ARP(psrc="192.168.253.142", pdst="192.168.253.141")
    result = parse_packet(pkt)
    assert result is not None
    assert result["proto"] == "ARP"
    print("[+] test_arp_packet passed")

if __name__ == "__main__":
    test_tcp_packet()
    test_icmp_packet()
    test_arp_packet()
    print("\n[+] All tests passed")
