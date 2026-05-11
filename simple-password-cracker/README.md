# Simple Password Cracker

> Beginner-level cybersecurity lab – password cracking techniques  
> Part of the [cybersecurity-labs](https://github.com/PiotrKleszcz/cybersecurity-labs) homelab series running on VMware Fusion.

---

## ⚠️ Legal Disclaimer

This project is intended **strictly for educational purposes** within a controlled, isolated virtual lab environment. All techniques demonstrated here are performed on machines owned and operated by the author. Unauthorized access to systems you do not own is illegal. The author accepts no responsibility for misuse of this material.

---

## Project Overview

A step-by-step exploration of password cracking techniques — from basic Python scripts to real-world tools like Hashcat and John the Ripper. Each phase builds on the previous one, covering hash types, dictionary attacks, brute force, and network service attacks.

---

## Lab Environment

|  Machine |      OS       |   IP Address    |          Role          |
|----------|---------------|-----------------|------------------------|
| Attack   | Kali Linux    | 192.168.253.141 | Scripts, tools, GitHub |
| Target 1 | Windows 11    | 192.168.253.136 | SAM hash extraction    |
| Target 2 | Fedora Linux  | 192.168.253.148 | /etc/shadow hashes     |
| Target 3 | Fedora Server | 192.168.253.149 | SSH / HTTP brute-force |
| Target 4 | Ubuntu Server | 192.168.253.152 | MySQL / web login      |

> Network: `192.168.253.0/24` – VMware Fusion host-only, isolated from the internet.

---

## Project Phases

|                                 Phase                                   |                        Topic                        |
|-------------------------------------------------------------------------|-----------------------------------------------------|
| [Phase 1 – Setup & Hash Basics](./phase-1-setup/)                       | Environment setup, hash types, first Python cracker |
| [Phase 2 – Dictionary & Brute Force]](./phase-2-dictionary-bruteforce/) | Wordlist attacks, brute force logic, rockyou.txt    |
| [Phase 3 – Hashcat & John the Ripper](./phase-3-hashcat-john/)          | Real-world GPU/CPU cracking tools                   |   
| [Phase 4 – Network Services](./phase-4-network-services/)               | SSH brute-force, HTTP basic auth, countermeasures   |

---

## Tools Used

- Python 3 (custom scripts)
- Hashcat
- John the Ripper
- Hydra
- rockyou.txt wordlist
- VMware Fusion

---

## Related Labs in This Repo

- [Cowrie Honeypot](../honeypot-cowrie/) – SSH honeypot deployed on Ubuntu Server
- [Network Pentest Lab](../network-pentest-lab/) – full network enumeration and exploitation
- [Nmap Network Scan](../nmap-network-scan/) – network discovery and port scanning

---

## Documentation

- [Lab Environment Setup](./docs/lab-environment.md)
- [Legal Disclaimer](./docs/legal-disclaimer.md)
