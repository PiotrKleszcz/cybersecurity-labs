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
| 1 | iptables – rules, blocking, INPUT/OUTPUT/FORWARD | 🔄 In Progress |
| 2 | nftables – modern syntax, same scenarios | ⏳ Planned |
| 3 | Logging blocked traffic | ⏳ Planned |

## Tools Used

- `iptables` / `ip6tables`
- `nftables` / `nft`
- `nmap` (reconnaissance & verification)
- `ufw` (Ubuntu frontend)

## Key Concepts

- Stateless vs stateful packet filtering
- Chain policies: INPUT, OUTPUT, FORWARD
- DROP vs REJECT
- Logging with `LOG` target before DROP
- iptables vs nftables syntax comparison

## Methodology

1. Baseline scan (before firewall rules)
2. Apply firewall rules
3. Verification scan (after rules)
4. Document findings
EOF
