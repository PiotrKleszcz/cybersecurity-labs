#!/usr/bin/env python3
"""
hash_cracker_basic.py
Simple password cracker – Phase 1
Matches a known MD5 hash against a list of candidate passwords.
Educational use only.
"""

import hashlib
import sys

TARGET_HASH = "5f4dcc3b5aa765d61d8327deb882cf99"  # MD5 of "password"

CANDIDATES = [
    "123456",
    "letmein",
    "monkey",
    "password",
    "qwerty",
    "admin",
    "iloveyou",
]

def crack(target_hash, candidates):
    print(f"[*] Target hash: {target_hash}")
    print(f"[*] Trying {len(candidates)} candidates...\n")

    for word in candidates:
        attempt = hashlib.md5(word.encode()).hexdigest()
        print(f"    Trying: {word:<15} → {attempt}")
        if attempt == target_hash:
            print(f"\n[+] MATCH FOUND: '{word}'")
            return word

    print("\n[-] No match found.")
    return None

if __name__ == "__main__":
    crack(TARGET_HASH, CANDIDATES)
