# Phase 2 – Custom Detection Rules

Creating and loading custom Suricata rules for detecting common attack patterns.

## Objective

- Write custom rules in `local.rules`
- Load rules into Suricata alongside Emerging Threats ruleset
- Verify rules are loaded correctly

## Environment

| Machine | OS | IP | Role |
|---|---|---|---|
| Kali Linux | Kali 2026.2 | 192.168.253.141 | Attacker |
| Ubuntu Desktop | Ubuntu 25.10 | 192.168.253.142 | IDS Sensor |
| Windows 11 Pro | Windows 25H2 | 192.168.253.146 | Victim |

## Custom Rules Overview

| SID | Rule | Description |
|---|---|---|
| 1000001 | ICMP Ping Detected | Detects any ICMP echo request to HOME_NET |
| 1000002 | Nmap SYN Scan Detected | Detects SYN flood pattern (5 packets/2s) |
| 1000003 | Nmap NULL Scan Detected | Detects TCP packets with no flags |
| 1000004 | Nmap FIN Scan Detected | Detects TCP FIN packets |
| 1000005 | SSH Brute Force Attempt | Detects 5+ SSH connections in 60 seconds |
| 1000006 | HTTP Port Scan Detected | Detects SYN packets to port 80 |

## Configuration

Rules file location on sensor: `/var/lib/suricata/rules/local.rules`

Added to `/etc/suricata/suricata.yaml`:
```yaml
rule-files:
  - suricata.rules
  - local.rules
```

## Commands

```bash
# Copy rules to Suricata rules directory
sudo cp local.rules /var/lib/suricata/rules/local.rules

# Restart Suricata to load new rules
sudo kill -9 $(cat /var/run/suricata/suricata.pid)
sudo rm -f /var/run/suricata/suricata.pid
sudo suricata -c /etc/suricata/suricata.yaml -i enp2s0 -D

# Verify rules loaded
sudo tail -5 /var/log/suricata/suricata.log
```

## Screenshots

| File | Description |
|---|---|
| `03_local_rules_loaded.png` | Suricata log showing 2 rule files, 50,866 signatures |
