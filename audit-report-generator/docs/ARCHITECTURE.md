# Audit Report Generator — Architecture

## Overview

A modular Python security audit tool that scans a network with Nmap,
analyses open services against a local vulnerability database, maps findings
to NIS2 Article 21 controls, and generates a professional PDF report.

## Module Structure

```
audit-report-generator/
├── main.py                  # CLI entry point — argparse, orchestrates pipeline
├── src/
│   ├── scanner.py           # Nmap runner + XML parser → normalised host list
│   ├── analyser.py          # Maps ports → findings, CVSS scoring, sorting
│   ├── nis2_mapper.py       # Maps findings → NIS2 Article 21 controls
│   ├── console_report.py    # Colour-coded terminal output (tabulate)
│   └── pdf_builder.py       # Multi-page PDF generator (ReportLab Platypus)
├── data/
│   ├── vulnerability_db.json  # Port/service → finding definitions + CVSS
│   └── nis2_controls.json     # NIS2 Article 21 control descriptions
├── tests/
│   └── test_analyser.py     # Unit tests for finding detection and scoring
├── reports/                 # Generated PDF output (gitignored)
└── scans/                   # Nmap XML output files (gitignored)
```

## Data Flow

```
CLI (main.py)
     │
     ├─ --target → scanner.run_nmap() → nmap -sV -sC --open -oX scan.xml
     ├─ --xml    → scanner.parse_xml(file)
     └─ --demo   → scanner.load_demo_data()
          │
          ▼
     List[Host dict]   {ip, hostname, os, ports[{port, protocol, service, version}]}
          │
          ▼
     analyser.analyse()
       └─ lookup each open port in vulnerability_db.json
       └─ create Finding dataclass per match
       └─ sort by severity_rank (Critical → High → Medium → Low → Info)
          │
          ▼
     List[Finding]
          │
          ├─ nis2_mapper.build_compliance_map()
          │    └─ group findings by NIS2 article
          │    └─ assign compliance status per article
          │
          ├─ console_report.print_report()
          │    └─ host table, findings summary, findings table, NIS2 summary
          │
          └─ pdf_builder.build()
               └─ Cover page
               └─ Executive Summary (severity counts + risk statement)
               └─ Host Inventory table
               └─ Findings Overview table (all findings)
               └─ Detailed Findings (one card per finding)
               └─ NIS2 Compliance Mapping table
               └─ Appendix: Remediation Priority List
```

## Lab Environment

| Role     | System            | IP              | Purpose             |
|----------|-------------------|-----------------|---------------------|
| Attacker | Kali Linux 2026.2 | 192.168.253.141 | Run audit tool      |
| Target 1 | Ubuntu Server     | 192.168.253.152 | Cowrie, SSH, MySQL  |
| Target 2 | Windows 11 Pro    | 192.168.253.136 | IIS, RDP, SMB       |
| Target 3 | Ubuntu Desktop    | 192.168.253.142 | Apache, FTP         |
| Target 4 | Fedora Server     | 192.168.253.149 | PostgreSQL, Redis   |

## Dependencies

| Library      | Version | Purpose                            |
|--------------|---------|------------------------------------|
| reportlab    | 4.2.5   | PDF generation (Platypus engine)   |
| colorama     | 0.4.6   | Colour-coded terminal output       |
| tabulate     | 0.9.0   | Formatted terminal tables          |
| python-nmap  | 0.7.1   | Nmap subprocess wrapper (optional) |
