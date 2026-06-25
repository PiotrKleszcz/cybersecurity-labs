# Network Diagram – Suricata IDS Lab

## Lab Topology

## Lab Topology

┌─────────────────────────────────────────────────────────────┐
│                   VMware Fusion NAT                          │
│                   192.168.253.0/24                           │
│                                                              │
│  ┌─────────────────┐         ┌─────────────────────────┐    │
│  │   Kali Linux    │─────────│    Ubuntu Desktop        │    │
│  │   (Attacker)    │ attacks │    (IDS Sensor)          │    │
│  │ 192.168.253.141 │────────▶│    192.168.253.142       │    │
│  │                 │         │                          │    │
│  │ Tools:          │         │ Suricata 8.0.3           │    │
│  │ - nmap          │         │ - fast.log               │    │
│  │ - hydra         │         │ - eve.json               │    │
│  │ - ping          │         │ - local.rules            │    │
│  └─────────────────┘         └─────────────────────────┘    │
│           │                                                  │
│           │ attacks                                          │
│           ▼                                                  │
│  ┌─────────────────┐                                         │
│  │  Windows 11 Pro │                                         │
│  │    (Victim)     │                                         │
│  │ 192.168.253.146 │                                         │
│  │                 │                                         │
│  │ Windows FW      │                                         │
│  │ blocks inbound  │                                         │
│  └─────────────────┘                                         │
└─────────────────────────────────────────────────────────────┘

## Traffic Flow

| Attack | From | To | Detected |
|---|---|---|---|
| ICMP Ping | Kali 141 | Ubuntu 142 | Yes - Suricata SID 1000001 |
| Nmap SYN Scan | Kali 141 | Ubuntu 142 | Yes - Suricata SID 1000002 |
| SSH Brute Force | Kali 141 | Ubuntu 142 | Yes - Suricata SID 1000005 |
| Nmap SYN Scan | Kali 141 | Windows 146 | No - Windows Firewall blocked |

## IDS Architecture Note

Suricata runs on Ubuntu Desktop in passive IDS mode (AF-PACKET).
It monitors all traffic on interface enp2s0 and generates alerts
without blocking traffic (no IPS mode in this lab).
