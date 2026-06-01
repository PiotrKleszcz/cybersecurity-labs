# Wireless Security Assessment and Hardening Laboratory (iOS Hotspot Sandbox)

## Disclaimer
This laboratory project is conducted strictly for educational purposes and localized wireless security auditing. All analysis scenarios are documented within a controlled sandbox environment utilizing a personal mobile hotspot as the target Access Point (AP). The operator maintains full ownership over all equipment.

## Lab Environment Specifications
* **Hypervisor:** VMware Fusion 26H1 (Bridged Network Mode)
* **Auditing Platform:** OS: Kali GNU/Linux Rolling (Version 2026.2)
  * Wireless Interface: External USB Adapter (Monitor Mode Enabled)
* **Target Environment:** iOS Personal Hotspot 
  * Security Architecture: WPA2-PSK (Passphrase: `weakpassword123`)

## Repository Directory Structure
```text
wifi-security-lab/
├── screenshots/
│   ├── 01_project_structure.png
│   └── 02_source_code_verification.png
├── src/
│   └── cap_analysis.txt
└── README.md
