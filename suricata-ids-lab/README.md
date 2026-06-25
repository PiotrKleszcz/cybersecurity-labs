# Suricata IDS Lab

Hands-on intrusion detection lab using **Suricata 8.0.3** on a local virtual network. Demonstrates real-time detection of network attacks including port scans, ICMP floods, and SSH brute force attempts.

## Lab Environment

| Machine | OS | IP | Role |
|---|---|---|---|
| Kali Linux | Kali 2026.2 | 192.168.253.141 | Attacker |
| Ubuntu Desktop | Ubuntu 25.10 | 192.168.253.142 | IDS Sensor |
| Windows 11 Pro | Windows 25H2 | 192.168.253.146 | Victim |

**Network:** 192.168.253.0/24 (VMware Fusion NAT)

## Phases

| Phase | Topic | Status |
|---|---|---|
| 1 | Suricata installation & configuration | ✅ Complete |
| 2 | Custom detection rules (local.rules) | ✅ Complete |
| 3 | Attack detection – nmap, ICMP, SSH brute force | ✅ Complete |
| 4 | Alert analysis – fast.log, eve.json | ✅ Complete |

## Tools Used

- `suricata` 8.0.3 (IDS sensor)
- `suricata-update` (Emerging Threats ruleset)
- `nmap` (reconnaissance & attack simulation)
- `hydra` (SSH brute force simulation)
- `journalctl` / `fast.log` / `eve.json` (log analysis)

## Key Concepts

- Network-based IDS (NIDS) architecture
- Suricata rule syntax (sid, msg, threshold)
- Emerging Threats Open ruleset
- Custom rule writing and loading
- Alert log analysis (fast.log, eve.json)

## Network Diagram

See [docs/network-diagram.md](docs/network-diagram.md)
