# Phase 4 – Alert Analysis

Analyzing Suricata alert logs to identify attack patterns and understand log formats.

## Objective

- Analyze alerts in `fast.log` (human-readable format)
- Analyze alerts in `eve.json` (JSON format for SIEM integration)
- Identify attack patterns and statistics
- Document log structure and key fields

## Environment

| Machine | OS | IP | Role |
|---|---|---|---|
| Kali Linux | Kali 2026.2 | 192.168.253.141 | Attacker |
| Ubuntu Desktop | Ubuntu 25.10 | 192.168.253.142 | IDS Sensor |
| Windows 11 Pro | Windows 25H2 | 192.168.253.146 | Victim |

## Log Files

| File | Location | Format | Purpose |
|---|---|---|---|
| `fast.log` | `/var/log/suricata/fast.log` | Plain text | Quick human-readable alerts |
| `eve.json` | `/var/log/suricata/eve.json` | JSON | SIEM integration, detailed metadata |
| `stats.log` | `/var/log/suricata/stats.log` | Plain text | Performance statistics |

## fast.log Analysis

### Alert format
[timestamp] [**] [GID:SID:REV] MESSAGE [**] [Classification] [Priority] {PROTO} SRC:PORT -> DST:PORT

### Alert summary from lab

| SID | Alert | Count | Source |
|---|---|---|---|
| 1000001 | ICMP Ping Detected | 5 | 192.168.253.141 (Kali) |
| 1000002 | Nmap SYN Scan Detected | 100+ | 192.168.253.141 (Kali) |
| 1000005 | SSH Brute Force Attempt | 10+ | 192.168.253.141 (Kali) |
| 2013504 | ET INFO GNU/Linux APT User-Agent | multiple | 192.168.253.142 (Ubuntu) |
| 2022973 | ET INFO Possible Kali Linux hostname | 2 | 192.168.253.141 (Kali) DHCP |

## eve.json Analysis

eve.json provides structured JSON output ideal for SIEM tools like Splunk, Elastic, or Graylog.

### Key fields
- timestamp – event time
- event_type – alert, dns, http, flow
- src_ip / dest_ip – source and destination
- alert.signature – rule message
- alert.severity – priority level
- alert.category – classification

## Commands

```bash
# Count alerts by signature
sudo cat /var/log/suricata/fast.log | grep -oP '\[\*\*\] \K[^\[]+' | sort | uniq -c | sort -rn

# Count total alerts
sudo grep -c "alert" /var/log/suricata/fast.log

# Filter by source IP
sudo grep "192.168.253.141" /var/log/suricata/fast.log | wc -l
```

## Screenshots

| File | Description |
|---|---|
| `07_fastlog_summary.png` | fast.log alert summary |
| `08_evejson_alert.png` | eve.json alert in JSON format |
