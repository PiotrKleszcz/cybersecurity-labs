# Phase 2 – nftables

Configuring and testing firewall rules using `nftables` on Ubuntu Desktop.

## Objective

- Clear iptables rules from Phase 1
- Apply equivalent rules using nftables syntax
- Verify with nmap scan from Kali
- Compare nftables vs iptables syntax

## Environment

| Machine | IP | Role |
|---|---|---|
| Kali Linux | 192.168.253.141 | Attacker / Scanner |
| Ubuntu Desktop | 192.168.253.142 | Hardened Target |

## iptables vs nftables Syntax Comparison

| Rule | iptables | nftables |
|---|---|---|
| Default DROP | `iptables -P INPUT DROP` | `policy drop` |
| Established | `--state ESTABLISHED,RELATED -j ACCEPT` | `ct state established,related accept` |
| Loopback | `-i lo -j ACCEPT` | `iif lo accept` |
| Allow port | `--dport 80 -j ACCEPT` | `tcp dport 80 accept` |

## Steps

### Step 1 – Clear Phase 1 rules
Flush iptables and remove nft table from iptables-nft backend.

### Step 2 – Create nftables ruleset
Add table, chain with DROP policy, and allow rules.

### Step 3 – Verification scan
Nmap from Kali confirms rules working correctly.

## Screenshots

| File | Description |
|---|---|
| `01_nft_baseline.png` | Empty nft ruleset before rules |
| `02_nft_rules_applied.png` | nftables rules applied (Ubuntu) |
| `03_nft_verification_nmap.png` | Nmap scan after nftables rules (Kali) |

## Results

| Port | Before | After |
|---|---|---|
| 22 | not shown | closed |
| 53 | not shown | closed |
| 80 | open | open |
| remaining | closed | filtered |
