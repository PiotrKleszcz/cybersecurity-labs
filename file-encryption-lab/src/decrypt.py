import os
from cryptography.fernet import Fernet

def decrypt_target_file(target_path, key):
    """Reads an encrypted file, decrypts it, and restores plaintext."""
    if not os.path.exists(target_path):
        print(f"[-] Error: Target file {target_path} does not exist.")
        return

    with open(target_path, "rb") as encrypted_file:
        ciphertext_data = encrypted_file.read()

    fernet_instance = Fernet(key)
    try:
        plaintext_data = fernet_instance.decrypt(ciphertext_data)
        with open(target_path, "wb") as decrypted_file:
            decrypted_file.write(plaintext_data)
        print(f"[+] Target file successfully decrypted: {target_path}")
    except Exception as e:
        print(f"[-] Decryption Failed: {e}")

if __name__ == "__main__":
    base_dir = "/home/fifthace/GitHub/cybersecurity-labs/file-encryption-lab"
    secret_key_path = os.path.join(base_dir, "src", "secret.key")
    victim_file_path = os.path.join(base_dir, "src", "victim_data.txt")

    if os.path.exists(secret_key_path):
        with open(secret_key_path, "rb") as key_file:
            saved_key = key_file.read()
        decrypt_target_file(victim_file_path, saved_key)
    else:
        print(f"[-] Error: Secret key not found at {secret_key_path}")
