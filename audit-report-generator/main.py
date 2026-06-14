#!/usr/bin/env python3
"""
Fifth Ace — Audit Report Generator
Scans a target network with Nmap, analyses findings, maps to NIS2 Article 21,
and produces a professional PDF security audit report.

Usage:
  sudo python3 main.py --target 192.168.1.0/24
  sudo python3 main.py --target 192.168.1.100 --ports 1-1024
       python3 main.py --xml scans/scan.xml
       python3 main.py --demo
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.scanner import run_nmap, parse_xml, load_demo_data
from src.analyser import analyse
from src.nis2_mapper import build_compliance_map
from src.console_report import print_report
from src.pdf_builder import build as build_pdf


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fifth Ace — Network Security Audit Report Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sudo python3 main.py --target 192.168.1.0/24
  sudo python3 main.py --target 192.168.1.100 --ports 22,80,443,3306
       python3 main.py --xml scans/existing_scan.xml
       python3 main.py --demo
       python3 main.py --demo --no-pdf
        """,
    )

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--target", metavar="IP/CIDR",
                      help="Target IP or CIDR range to scan (requires root + nmap)")
    mode.add_argument("--xml", metavar="FILE",
                      help="Parse existing Nmap XML file instead of scanning")
    mode.add_argument("--demo", action="store_true",
                      help="Use built-in demo data (no root or nmap required)")

    parser.add_argument("--ports", default="1-65535", metavar="PORTS",
                        help="Port range for live scan (default: 1-65535)")
    parser.add_argument("--output", default="", metavar="FILE",
                        help="PDF output filename (default: auto-generated in reports/)")
    parser.add_argument("--no-pdf", action="store_true",
                        help="Print terminal report only, skip PDF generation")

    return parser.parse_args()


def main():
    args = parse_args()

    print("\n" + "=" * 60)
    print("  Fifth Ace — Audit Report Generator")
    print("=" * 60)

    if args.demo:
        print("[*] Mode: DEMO (built-in sample data)\n")
        hosts = load_demo_data()
        target = "192.168.1.0/24 (demo)"
    elif args.xml:
        print(f"[*] Mode: XML parse — {args.xml}\n")
        hosts = parse_xml(args.xml)
        target = args.xml
    else:
        print(f"[*] Mode: Live scan — {args.target}\n")
        xml_path = run_nmap(args.target, args.ports)
        hosts = parse_xml(xml_path)
        target = args.target

    if not hosts:
        print("[-] No active hosts found. Exiting.")
        sys.exit(0)

    print(f"[+] Hosts discovered: {len(hosts)}")

    findings = analyse(hosts)
    print(f"[+] Findings identified: {len(findings)}")

    compliance_map = build_compliance_map(findings)

    print_report(hosts, findings, compliance_map)

    if not args.no_pdf:
        try:
            pdf_path = build_pdf(hosts, findings, compliance_map, target, args.output)
            print(f"\n[+] Done. Open report: {pdf_path}")
        except ImportError:
            print("\n[!] reportlab not installed. Run: pip install reportlab")
            print("    Terminal report printed above.")


if __name__ == "__main__":
    main()
