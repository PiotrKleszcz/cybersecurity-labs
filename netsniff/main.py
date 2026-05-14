#!/usr/bin/env python3
import argparse
import sys
from src.packet_capture import start_capture
from src.packet_parser import parse_packet
from src.logger import save_json, save_pcap
from src.reporter import generate_report
from src.filters import get_filter
from scapy.all import sniff

def main():
    parser = argparse.ArgumentParser(
        description="NetSniff — Network Traffic Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sudo python3 main.py -i eth0
  sudo python3 main.py -i eth0 -f http -d 30 -o capture.json
  sudo python3 main.py -i eth0 --filter "tcp port 443" -d 60
        """
    )
    parser.add_argument("-i", "--interface", default="eth0", help="Network interface (default: eth0)")
    parser.add_argument("-f", "--filter", default="", help="BPF filter or preset: http, https, dns, ssh, icmp, arp")
    parser.add_argument("-d", "--duration", type=int, default=30, help="Capture duration in seconds (default: 30)")
    parser.add_argument("-c", "--count", type=int, default=0, help="Max packets (0 = unlimited)")
    parser.add_argument("-o", "--output", default="", help="Output JSON filename")
    parser.add_argument("--no-report", action="store_true", help="Skip summary report")
    args = parser.parse_args()

    bpf = get_filter(args.filter)
    records = []
    packets = []

    def callback(pkt):
        packets.append(pkt)
        parsed = parse_packet(pkt)
        if parsed:
            records.append(parsed)

    try:
        start_capture(
            interface=args.interface,
            bpf_filter=bpf,
            count=args.count,
            duration=args.duration,
            callback=callback
        )
    except KeyboardInterrupt:
        print("\n[*] Capture stopped by user.")
    except PermissionError:
        print("[!] Run as root: sudo python3 main.py ...")
        sys.exit(1)

    if packets:
        save_pcap(packets)
    if records:
        fname = args.output or ""
        save_json(records, fname or None)
    if not args.no_report:
        generate_report(records)

if __name__ == "__main__":
    main()
