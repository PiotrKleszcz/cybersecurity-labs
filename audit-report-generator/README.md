# Audit Report Generator

Automated network security audit tool — scans with Nmap, analyses findings against a local vulnerability database, maps results to NIS2 Directive Article 21 controls, and generates a professional PDF report.

---

## Lab Overview

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Network scan — Nmap XML output | ✅ Complete |
| 2 | Finding analysis — port/service → vulnerability mapping + CVSS scoring | ✅ Complete |
| 3 | NIS2 Article 21 compliance mapping | ✅ Complete |
| 4 | Terminal report — colour-coded findings table | ✅ Complete |
| 5 | PDF report generation — professional multi-page document | ✅ Complete |

---

## Tools Used

`Python 3` `Nmap` `ReportLab` `Scapy` `colorama` `tabulate`

---

## Lab Environment

| Role | System | IP | Purpose |
|------|--------|----|---------|
| Attacker | Kali Linux 2026.2 | 192.168.253.141 | Run audit tool |
| Target 1 | Ubuntu Server 25.10 | 192.168.253.152 | SSH, MySQL, Redis |
| Target 2 | Windows 11 Pro | 192.168.253.136 | IIS, RDP, SMB |
| Target 3 | Ubuntu Desktop | 192.168.253.142 | Apache, FTP |
| Target 4 | Fedora Server | 192.168.253.149 | PostgreSQL, SNMP |
| Hypervisor | VMware Fusion 26H1 | 192.168.253.2 | VM management |

**Internal network scope:** `192.168.253.0/24`

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Demo mode (no root, no nmap required)
python3 main.py --demo

# Live scan (requires root + nmap)
sudo python3 main.py --target 192.168.253.0/24

# Parse existing Nmap XML
python3 main.py --xml scans/existing_scan.xml

# Terminal output only (no PDF)
python3 main.py --demo --no-pdf

# Run unit tests
python3 tests/test_analyser.py
```

---

## Architecture

```
main.py              CLI entry — orchestrates the full pipeline
src/
  scanner.py         Nmap runner + XML parser → normalised host list
  analyser.py        Port/service → finding mapping, CVSS scoring, sorting
  nis2_mapper.py     Maps findings to NIS2 Article 21 controls
  console_report.py  Colour-coded terminal tables
  pdf_builder.py     Multi-page PDF report (ReportLab Platypus)
data/
  vulnerability_db.json   Port → finding definitions + CVSS scores
  nis2_controls.json      NIS2 Article 21 control descriptions
tests/
  test_analyser.py   8 unit tests for finding detection and scoring
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for full data flow diagram.

---

## PDF Report Structure

1. Cover page — Fifth Ace branding, target, date, confidential
2. Executive Summary — severity counts and risk statement
3. Host Inventory — all discovered hosts with OS and open ports
4. Findings Overview — sortable table of all findings
5. Detailed Findings — description + remediation card per finding
6. NIS2 Compliance Mapping — Article 21 gap analysis
7. Appendix — prioritised remediation list

---

## Vulnerability Database

The tool detects findings for 17 common service exposures:

| Severity | Services |
|----------|----------|
| Critical | Telnet (23), Redis (6379), MongoDB (27017) |
| High | FTP (21), NetBIOS (139), SMB (445), RDP (3389), SNMP (161), MySQL (3306), PostgreSQL (5432), MSSQL (1433), VNC (5900), POP3 (110) |
| Medium | HTTP (80), SMTP (25), DNS zone transfer (53), HTTP-alt (8080) |
| Info | HTTPS TLS check (443), HTTPS-alt (8443) |

---

## NIS2 Coverage

Findings are mapped to **NIS2 Directive (EU) 2022/2555 Article 21** controls:

- `21(2)(e)` — Network and information systems security
- `21(2)(g)` — Cyber hygiene and cybersecurity training
- `21(2)(h)` — Cryptography and encryption
- `21(2)(i)` — Human resources security and access control
- `21(2)(j)` — Multi-factor authentication

---

## ⚠️ Disclaimer

This tool is designed for authorised security assessments only. All testing must be conducted against systems you own or have explicit written permission to test. Unauthorised scanning is illegal. All lab scans were performed in a controlled VMware environment.
