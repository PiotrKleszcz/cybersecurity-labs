# NetSniff — Architecture

## Overview

NetSniff is a modular Python network sniffer built on Scapy.
Each module has a single responsibility.

## Module Structure

netsniff/
├── main.py               # CLI entry point — argparse, orchestrates all modules
├── src/
│   ├── packet_capture.py # Scapy sniff engine — opens raw socket, captures packets
│   ├── packet_parser.py  # Protocol decoder — TCP, UDP, ICMP, ARP, IP
│   ├── filters.py        # BPF filter presets — maps friendly names to BPF syntax
│   ├── logger.py         # Export module — saves .pcap and .json to disk
│   └── reporter.py       # Analysis module — stats, top IPs, port scan detection

## Data Flow

Network interface (eth0)
↓
packet_capture.py  — Scapy sniff(), raw socket, promiscuous mode
↓
packet_parser.py   — decode layers: Ether → IP → TCP/UDP/ICMP/ARP
↓
callback()     — collect parsed dicts + raw packets
↓
     ┌────┴────┐
logger.py   reporter.py
.pcap .json   stats + alerts

## Lab Environment

|       VM       |      OS      |       IP        |         Role         |
|----------------|--------------|-----------------|----------------------|
| Kali Linux     | Kali 2026    | 192.168.253.141 | Sniffer              |
| Ubuntu Desktop | Ubuntu 26.04 | 192.168.253.142 | Target — Apache HTTP |
| Windows 11 Pro | Windows 11   | TBD             | Target — HTTP/ICMP   |
| Fedora Linux   | Fedora 44    | TBD             | Observer             |

## Dependencies

| Library  | Version |           Purpose           |
|----------|---------|-----------------------------|
| scapy    | 2.5.0   | Packet capture and parsing  |
| colorama | 0.4.6   | Color-coded terminal output |
| tabulate | 0.9.0   | Formatted report tables     |
