# Network Diagram – Firewall Lab

## Lab Environment

┌─────────────────────────────────────────────────────┐

│                VMware Fusion NAT                     │

│                192.168.253.0/24                      │

│                                                      │

│  ┌─────────────────┐      ┌─────────────────────┐   │

│  │   Kali Linux    │      │   Ubuntu Desktop    │   │

│  │   (Attacker)    │─────▶│   (Target)          │   │

│  │ 192.168.253.141 │      │ 192.168.253.142      │   │

│  │                 │      │                     │   │

│  │ Tools:          │      │ Firewall:           │   │

│  │ - nmap          │      │ - iptables (Ph.1)   │   │

│  │                 │      │ - nftables (Ph.2-3) │   │

│  └─────────────────┘      └─────────────────────┘   │

│                                                      │

│  ┌─────────────────┐                                 │

│  │  VMware Gateway │                                 │

│  │ 192.168.253.2   │                                 │

│  └─────────────────┘                                 │

└─────────────────────────────────────────────────────┘

## Traffic Flow

| Phase | Direction | Action |
|---|---|---|
| Phase 1 | Kali → Ubuntu | Blocked by iptables (DROP) |
| Phase 2 | Kali → Ubuntu | Blocked by nftables (DROP) |
| Phase 3 | Kali → Ubuntu | Blocked + logged (IPT-DROP:) |

## Allowed Traffic (all phases)

| Port | Protocol | Service |
|---|---|---|
| 22 | TCP | SSH |
| 53 | TCP/UDP | DNS |
| 80 | TCP | HTTP (Apache) |
