# Phase 3 – Logging

Logging blocked traffic using nftables `log` target and `journalctl` on Ubuntu Desktop.

## Objective

- Add logging rule to existing nftables ruleset
- Generate blocked traffic from Kali (nmap scan)
- Observe and analyze blocked packets in system logs

## Environment

| Machine | IP | Role |
|---|---|---|
| Kali Linux | 192.168.253.141 | Attacker / Scanner |
| Ubuntu Desktop | 192.168.253.142 | Hardened Target |

## Steps

### Step 1 – Add logging rule
Added `log` target with prefix `IPT-DROP:` before default DROP policy.

### Step 2 – Generate blocked traffic
Nmap SYN scan from Kali triggers logging on Ubuntu.

### Step 3 – Analyze logs
Blocked packets visible in kernel log via `journalctl`.

## Commands

```bash
# Add logging rule
sudo nft add rule ip filter INPUT counter log prefix '"IPT-DROP: "' drop

# View blocked traffic logs
sudo journalctl -k | grep "IPT-DROP"
```

## Log Analysis

| Field | Value | Meaning |
|---|---|---|
| `SRC=192.168.253.141` | Kali IP | Source of blocked traffic |
| `PROTO=TCP` | TCP | Nmap SYN scan packets |
| `PROTO=ICMP TYPE=8` | ICMP | Blocked ping attempts |
| `SYN URGP=0` | SYN flag | Characteristic nmap -sS signature |
| `IPT-DROP:` | Log prefix | Our custom identifier |

## Screenshots

| File | Description |
|---|---|
| `01_logging_rule_added.png` | nftables ruleset with logging rule |
| `02_logs_top.png` | Blocked traffic logs - top |
| `03_logs_bottom.png` | Blocked traffic logs - bottom |
