from scapy.all import sniff, conf
from src.packet_parser import parse_packet

conf.verb = 0

def start_capture(interface="eth0", bpf_filter="", count=0, duration=None, callback=None):
    print(f"[*] Sniffing on {interface} | filter: '{bpf_filter or 'none'}' | duration: {duration or 'unlimited'}s")
    sniff(
        iface=interface,
        filter=bpf_filter,
        count=count,
        timeout=duration,
        prn=callback or parse_packet,
        store=False
    )
