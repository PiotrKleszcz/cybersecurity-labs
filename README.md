# Cybersecurity Labs 🛡️

Hands-on cybersecurity labs documenting real-world attack and defense scenarios using Kali Linux, VMware, and industry-standard tools.

---

## 🧪 Labs

| Project | Description | Tools | Status |
|---|---|---|---|
| [audit-report-generator](./audit-report-generator) | Automated network audit — Nmap scan, CVSS scoring, NIS2 Article 21 mapping, PDF report generation | Python, Nmap, ReportLab | ✅ Complete |
| [honeypot-cowrie](./honeypot-cowrie) | SSH honeypot deployment + Hydra brute-force + ELK Stack log analysis | Cowrie, Hydra, Elasticsearch, Kibana, Filebeat | ✅ Complete |
| [wifi-security-lab](./wifi-security-lab) | WPA2 handshake capture + GPU password cracking + PMKID attempt | Aircrack-ng, Hashcat, hcxdumptool, Alfa AWUS036ACH | ✅ Complete |
| [network-pentest-lab](./network-pentest-lab) | Internal network pentest — discovery, enumeration, SSH analysis | Nmap, VMware | ✅ Complete |
| [nmap-network-scan](./nmap-network-scan) | Basic network discovery and port scanning | Nmap | ✅ Complete |
| [basic-keylogger](./basic-keylogger) | Windows keylogger — Python script compiled and executed on Windows 11 | Python, Windows API | ✅ Complete |
| [digital-forensics-lab](./digital-forensics-lab) | DFIR — auth.log analysis, brute-force triage, forensic report | Python, Linux logs | ✅ Complete |
| [file-encryption-lab](./file-encryption-lab) | Cross-platform file encryption and decryption | Python, OpenSSL | ✅ Complete |
| [phishing-awareness-lab](./phishing-awareness-lab) | Phishing simulation — HTML email template + awareness landing page | HTML, Python HTTP server | ✅ Complete |
| [netsniff](./netsniff) | Python network sniffer — TCP/UDP/ICMP/ARP capture, BPF filters, PCAP+JSON export | Python, Scapy | ✅ Complete |
| [simple-password-cracker](./simple-password-cracker) | Password cracking — Python scripts, Hashcat, John, Hydra, SSH/HTTP brute-force | Python, Hashcat, John, Hydra | ✅ Complete |

---

## 🖥️ Lab Environment

| Role | System | IP | Purpose |
|---|---|---|---|
| 💣 Attacker | Kali Linux 2026.2 | 192.168.253.141 | Offensive tools, scripts |
| 🎯 Target 1 | Ubuntu Server 25.10 | 192.168.253.152 | Cowrie honeypot, SSH |
| 🎯 Target 2 | Windows 11 Pro | 192.168.253.136 | Keylogger target, SAM hashes |
| 🎯 Target 3 | Ubuntu Desktop | 192.168.253.142 | File encryption, phishing target |
| 🎯 Target 4 | Fedora Linux | 192.168.253.148 | Network enumeration |
| 🎯 Target 5 | Fedora Server | 192.168.253.149 | SSH/HTTP brute-force |
| 📡 Wireless | Alfa AWUS036ACH (RTL8812AU) | — | Monitor mode, packet injection |
| ⚙️ Hypervisor | VMware Fusion 26H1 | 192.168.253.2 | VM management (Bridged/NAT) |
| 💻 Host | MacBook Air M2 (16GB) | 192.168.1.198 | macOS host, GPU cracking (Metal) |

**Internal network scope:** `192.168.253.0/24`

---

## 🛠️ Tools & Technologies

`Kali Linux` `Nmap` `Aircrack-ng` `Hashcat` `hcxdumptool` `Cowrie` `Hydra` `Elasticsearch` `Kibana` `Filebeat` `Scapy` `Python` `OpenSSL` `John the Ripper` `VMware Fusion`

---

## 🎯 Goal

Build practical, documented cybersecurity skills through hands-on labs covering offensive security, network analysis, wireless attacks, and defensive monitoring — all conducted in a controlled VMware environment.

---

## ⚠️ Disclaimer

All labs are conducted in a controlled virtual environment for educational purposes only. No attacks were performed on systems without explicit authorization.
