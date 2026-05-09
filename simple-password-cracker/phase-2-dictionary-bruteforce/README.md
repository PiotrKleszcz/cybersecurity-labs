# Phase 2 – Dictionary Attack

## Objectives

- Understand how dictionary attacks work against network services
- Write a Python SSH brute-force script using paramiko
- Use rockyou.txt wordlist to crack a weak SSH password
- Observe SSH rate-limiting behaviour during an attack

## Lab Machines Used in This Phase

|    Machine    |       IP        |          Purpose          |
|---------------|-----------------|---------------------------|
| Kali Linux    | 192.168.253.141 | Running the attack script |
| Ubuntu Server | 192.168.253.152 | SSH target                |

---

## Background – How Dictionary Attacks Work

A dictionary attack tries passwords from a pre-built wordlist rather than generating every possible combination (brute force). This is effective because most users choose common, memorable passwords that appear in leaked password databases.

The wordlist used in this phase is **rockyou.txt** – a real-world dataset of 14,344,392 passwords leaked in the 2009 RockYou data breach. It is pre-installed on Kali Linux at `/usr/share/wordlists/rockyou.txt`.

---

## Step 1 – Target Setup

A dedicated test user was created on Ubuntu Server specifically for this exercise. The main user account (`fifthace`) was never used as an attack target.

```bash
# Kali Linux
ssh fifthace@192.168.253.152
```

```bash
# Ubuntu Server
sudo adduser testuser
# Password set to: sunshine (intentionally weak for demo purposes)
id testuser
exit
```

**Output:**
