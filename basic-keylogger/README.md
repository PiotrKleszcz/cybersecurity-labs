# Basic Windows Keylogger for Educational Practice

## Disclaimer
This project is created for educational and research purposes only. The primary objective is to analyze how local keyboard hooks interact with the Windows API and how endpoint monitoring utilities log such events. Do not execute this software on any system without explicit, prior written authorization from the system owner.

## Lab Environment Specifications
* **Hypervisor:** VMware Fusion 26H1
* **Development / Attacker Machine:** * OS: Kali GNU/Linux Rolling (Version 2026.2)
    * IP Address: `192.168.253.141`
    * User Account: `fifthace`
* **Target Machine:** * OS: Microsoft Windows 11 Pro (Version 10.0.26200.8457)
    * IP Address: `192.168.253.136`
    * User Account: `piotr`

## Directory Structure
```text
basic-keylogger/
├── build/
├── screenshots/
│   ├── 01_project_structure.png
│   ├── 02_source_code_verification.png
│   ├── 03_compiled_executable.png
│   └── 04_execution_evidence.png
├── src/
│   └── keylogger.py
└── README.md
