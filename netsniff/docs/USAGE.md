# NetSniff — Usage Guide

## Requirements

- Kali Linux (or any Debian-based Linux)
- Python 3.10+
- Root/sudo privileges
- Scapy, colorama, tabulate (see requirements.txt)

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/cybersecurity-labs.git
cd cybersecurity-labs/netsniff
pip3 install -r requirements.txt --break-system-packages
```

## Basic Usage

```bash
sudo python3 main.py -i eth0 -d 30
```

## All Flags

|         Flag        |         Description         | Default |
|---------------------|-----------------------------|---------|
| `-i`, `--interface` | Network interface           | `eth0`  |
| `-f`, `--filter`    | BPF filter or preset        | none    |
| `-d`, `--duration`  | Duration in seconds         | `30`    |
| `-c`, `--count`     | Max packets (0 = unlimited) | `0`     |
| `-o`, `--output`    | Output JSON filename        | auto    |
| `--no-report`       | Skip summary report         | off     |

## Filter Presets

| Preset  | BPF equivalent |
|---------|----------------|
| `http`  | `tcp port 80`  |
| `https` | `tcp port 443` |
| `dns`   | `udp port 53`  |
| `ftp`   | `tcp port 21`  |
| `ssh`   | `tcp port 22`  |
| `icmp`  | `icmp`         |
| `arp`   | `arp`          |

## Examples

```bash
# Capture all traffic for 30 seconds
sudo python3 main.py -i eth0 -d 30

# Capture HTTP only
sudo python3 main.py -i eth0 -f http -d 60

# Capture HTTPS with custom output file
sudo python3 main.py -i eth0 -f https -d 30 -o https_capture.json

# Capture ICMP (ping monitoring)
sudo python3 main.py -i eth0 -f icmp -d 120

# Capture 500 packets, skip report
sudo python3 main.py -i eth0 -c 500 --no-report
```

## Output Files

- `captures/*.pcap` — open in Wireshark
- `logs/*.json` — parse with Python or jq
