# Usage Guide

## Installation

```bash
cd audit-report-generator
pip install -r requirements.txt
```

Nmap must also be installed:
```bash
sudo apt install nmap      # Kali / Debian / Ubuntu
sudo dnf install nmap      # Fedora
```

---

## Modes

### 1. Demo mode (no root, no nmap required)
```bash
python3 main.py --demo
```
Uses built-in sample data representing a 5-host SMB network.
Generates terminal report + PDF in `reports/`.

### 2. Live scan
```bash
sudo python3 main.py --target 192.168.1.0/24
sudo python3 main.py --target 192.168.1.100
sudo python3 main.py --target 192.168.1.100 --ports 22,80,443,3306,3389
```
Runs `nmap -sV -sC --open` against the target. Requires root.
Saves Nmap XML to `scans/` before analysis.

### 3. Parse existing Nmap XML
```bash
# First scan manually:
sudo nmap -sV -sC --open -oX scans/myscan.xml 192.168.1.0/24

# Then generate report:
python3 main.py --xml scans/myscan.xml
```

---

## Options

| Flag        | Description                                       |
|-------------|---------------------------------------------------|
| `--target`  | IP address or CIDR range to scan                  |
| `--xml`     | Parse an existing Nmap XML file                   |
| `--demo`    | Use built-in sample data                          |
| `--ports`   | Port range for live scan (default: 1-65535)       |
| `--output`  | Custom PDF output path                            |
| `--no-pdf`  | Print terminal report only, skip PDF generation   |

---

## Running Tests

```bash
python3 tests/test_analyser.py
# or with pytest:
pip install pytest
python3 -m pytest tests/ -v
```

---

## Output

**Terminal:** colour-coded tables for hosts, findings, and NIS2 compliance.

**PDF report** (saved to `reports/`):
1. Cover page
2. Executive Summary with severity counts
3. Host Inventory
4. Findings Overview table
5. Detailed Findings with description + remediation per finding
6. NIS2 Article 21 Compliance Mapping
7. Appendix: Remediation Priority List
