from scapy.all import IP, TCP, UDP, ICMP, ARP
from colorama import Fore, Style
from datetime import datetime

def parse_packet(pkt):
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]

    if pkt.haslayer(ARP):
        print(f"{Fore.YELLOW}[{ts}] ARP  {pkt[ARP].psrc:16} → {pkt[ARP].pdst}{Style.RESET_ALL}")
        return {"time": ts, "proto": "ARP", "src": pkt[ARP].psrc, "dst": pkt[ARP].pdst}

    if not pkt.haslayer(IP):
        return None

    src = pkt[IP].src
    dst = pkt[IP].dst

    if pkt.haslayer(TCP):
        sport, dport = pkt[TCP].sport, pkt[TCP].dport
        flags = pkt[TCP].flags
        print(f"{Fore.CYAN}[{ts}] TCP  {src}:{sport:5} → {dst}:{dport:5}  flags={flags}{Style.RESET_ALL}")
        return {"time": ts, "proto": "TCP", "src": src, "sport": sport, "dst": dst, "dport": dport, "flags": str(flags)}

    if pkt.haslayer(UDP):
        sport, dport = pkt[UDP].sport, pkt[UDP].dport
        print(f"{Fore.GREEN}[{ts}] UDP  {src}:{sport:5} → {dst}:{dport:5}{Style.RESET_ALL}")
        return {"time": ts, "proto": "UDP", "src": src, "sport": sport, "dst": dst, "dport": dport}

    if pkt.haslayer(ICMP):
        itype = pkt[ICMP].type
        print(f"{Fore.MAGENTA}[{ts}] ICMP {src:16} → {dst:16}  type={itype}{Style.RESET_ALL}")
        return {"time": ts, "proto": "ICMP", "src": src, "dst": dst, "type": itype}

    print(f"{Fore.WHITE}[{ts}] IP   {src} → {dst}{Style.RESET_ALL}")
    return {"time": ts, "proto": "IP", "src": src, "dst": dst}
