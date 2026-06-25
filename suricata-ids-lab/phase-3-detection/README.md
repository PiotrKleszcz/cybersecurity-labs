# Phase 3 – Attack Detection

Real-time detection of network attacks using Suricata custom rules and Emerging Threats signatures.

## Objective

- Generate attack traffic from Kali against Ubuntu and Windows 11
- Verify Suricata detects attacks via custom local.rules
- Document detection results in fast.log

## Environment

| Machine | OS | IP | Role |
|---|---|---|---|
| Kali Linux | Kali 2026.2 | 192.168.253.141 | Attacker |
| Ubuntu Desktop | Ubuntu 25.10 | 192.168.253.142 | IDS Sensor / Target |
| Windows 11 Pro | Windows 25H2 | 192.168.253.146 | Victim |

## Attacks & Detection Results

| Attack | Tool | Target | SID | Detected |
|---|---|---|---|---|
| ICMP Ping | ping | 192.168.253.142 | 1000001 | ✅ Yes |
| Nmap SYN Scan | nmap -sS | 192.168.253.142 | 1000002 | ✅ Yes |
| SSH Brute Force | hydra | 192.168.253.142 | 1000005 | ✅ Yes |
| Nmap SYN Scan | nmap -sS | 192.168.253.146 | 1000002 | ❌ No – Windows Firewall blocked packets |

## Windows 11 Finding

Windows 11 default firewall blocked all inbound packets before they could be detected by Suricata. This is a realistic finding – host-based firewalls can limit network-based IDS visibility. In a real environment, IDS should be deployed at the network perimeter (e.g. on a router or dedicated sensor) rather than relying solely on host traffic.

## Commands

```bash
# ICMP ping from Kali
ping -c 5 192.168.253.142

# Nmap SYN scan from Kali
nmap -sS 192.168.253.142

# SSH brute force from Kali
hydra -l root -P /usr/share/wordlists/rockyou.txt 192.168.253.142 ssh -t 4 -W 1

# Monitor alerts on Ubuntu
sudo tail -f /var/log/suricata/fast.log
```

## Screenshots

| File | Description |
|---|---|
| `04_icmp_detected.png` | ICMP Ping Detected alerts in fast.log |
| `05_nmap_syn_detected.png` | Nmap SYN Scan Detected alerts in fast.log |
| `06_ssh_bruteforce_detected.png` | SSH Brute Force Attempt alerts in fast.log |
