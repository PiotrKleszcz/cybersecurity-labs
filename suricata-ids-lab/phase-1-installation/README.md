# Phase 1 – Installation & Configuration

Installing and configuring Suricata 8.0.3 IDS on Ubuntu Desktop.

## Objective

- Install Suricata on Ubuntu Desktop (sensor)
- Configure network interface for packet capture
- Download Emerging Threats ruleset
- Verify Suricata is running and rules are loaded

## Environment

| Machine | OS | IP | Role |
|---|---|---|---|
| Kali Linux | Kali 2026.2 | 192.168.253.141 | Attacker |
| Ubuntu Desktop | Ubuntu 25.10 | 192.168.253.142 | IDS Sensor |
| Windows 11 Pro | Windows 25H2 | 192.168.253.146 | Victim |

## Installation Notes

Suricata is not available in Ubuntu 25.10 default repositories via snap/apt search for snort.
Installed via: `sudo apt install suricata`
Version installed: **Suricata 8.0.3**

## Configuration

### Network interface
Changed default interface from `eth0` to `enp2s0` in `/etc/suricata/suricata.yaml`.

### Rules
- Downloaded **Emerging Threats Open** ruleset via `suricata-update`
- **50,860 rules** loaded from Emerging Threats
- Custom `local.rules` added (Phase 2)

## Commands

```bash
# Install Suricata
sudo apt install suricata

# Download and update rules
sudo suricata-update

# Run Suricata in IDS mode (daemon)
sudo suricata -c /etc/suricata/suricata.yaml -i enp2s0 -D

# Check logs
sudo tail -20 /var/log/suricata/suricata.log
```

## Screenshots

| File | Description |
|---|---|
| `01_suricata_version.png` | Suricata version confirmation |
| `02_suricata_running.png` | Suricata running with 50,865 signatures loaded |
