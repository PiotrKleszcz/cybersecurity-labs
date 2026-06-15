# Firewall Lab

Hands-on firewall configuration and testing lab using **iptables** and **nftables** on a local virtual network.

## Lab Environment

| Machine | OS | IP | Role |
|---|---|---|---|
| Kali Linux | Kali 2026.2 | 192.168.253.141 | Attacker / Scanner |
| Ubuntu Desktop | Ubuntu | 192.168.253.142 | Victim / Hardened Target |

**Network:** 192.168.253.0/24 (VMware Fusion NAT)

## Phases

| Phase | Topic | Status |
|---|---|---|
| 1 | iptables – rules, blocking, INPUT/OUTPUT/FORWARD | ✅ Complete |
| 2 | nftables – modern syntax, same scenarios | ✅ Complete |
| 3 | Logging blocked traffic with nftables + journalctl | ✅ Complete |

## Tools Used

- `iptables` / `ip6tables`
- `nftables` / `nft`
- `nmap` (reconnaissance & verification)
- `journalctl` (log analysis)

## Key Concepts

- Stateless vs stateful packet filtering
- Chain policies: INPUT, OUTPUT, FORWARD
- DROP vs REJECT
- Logging with `log` target before DROP
- iptables vs nftables syntax comparison
- Kernel log analysis via journalctl

## Methodology

1. Baseline scan from Kali (before firewall rules)
2. Apply firewall rules on Ubuntu
3. Verification scan from Kali (after rules)
4. Analyze blocked traffic in logs

## Results Summary

| Tool | Default Policy | Ports Allowed | Logged |
|---|---|---|---|
| iptables | INPUT DROP | 22, 53, 80 | No |
| nftables | INPUT DROP | 22, 53, 80 | Yes (IPT-DROP:) |

## Network Diagram

See [docs/network-diagram.md](docs/network-diagram.md)
