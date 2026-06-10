Configuring and testing firewall rules using `iptables` on Ubuntu Desktop.

## Objective

- Perform baseline nmap scan from Kali (before rules)
- Apply INPUT/OUTPUT/FORWARD rules on Ubuntu
- Block specific ports and services
- Verify rules with second nmap scan from Kali

## Environment

| Machine | IP | Role |
|---|---|---|
| Kali Linux | 192.168.253.141 | Attacker / Scanner |
| Ubuntu Desktop | 192.168.253.142 | Victim → Hardened |

## Steps

### Step 1 – Baseline scan
Nmap scan from Kali before any firewall rules applied.

### Step 2 – Install & verify iptables on Ubuntu
Confirm iptables is available, check default policy.

### Step 3 – Apply firewall rules
Block incoming ports, set default policies, configure FORWARD chain.

### Step 4 – Verification scan
Repeat nmap scan from Kali – confirm ports are blocked.

### Step 5 – Review rules
List all active iptables rules on Ubuntu.

## Screenshots

| File | Description |
|---|---|
| `01_baseline_nmap.png` | Nmap scan before firewall rules |
| `02_rules_applied.png` | Firewall rules applied |
| `03_verification_nmap.png` | Nmap scan after firewall rules |
| `04_iptables_list.png` | Final iptables rules list (Ubuntu) |

## Results

> To be filled after lab completion.
EOF
