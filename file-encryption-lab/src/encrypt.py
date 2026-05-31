import os
from cryptography.fernet import Fernet

def generate_and_save_key(key_path):
    """Generates a secure symmetric key and saves it to disk."""
    key = Fernet.generate_key()
    with open(key_path, "wb") as key_file:
        key_file.write(key)
    print(f"[+] Key generated: {key_path}")
    return key

def encrypt_file(target_path, key):
    """Encrypts a file and overwrites it with ciphertext."""
    if not os.path.exists(target_path):
        print(f"[-] Error: {target_path} not found.")
        return

    with open(target_path, "rb") as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)

    with open(target_path, "wb") as f:
        f.write(encrypted_data)
    
    print(f"[+] File encrypted: {target_path}")

if __name__ == "__main__":
    # Path configuration
    key_file = "secret.key"
    target = "victim_data.txt"

    # Create dummy data if it doesn't exist
    if not os.path.exists(target):
        with open(target, "w") as f:
            f.write("SECRET_DB_PASSWORD=Password123!")

    # Execute
    my_key = generate_and_save_key(key_file)
    encrypt_file(target, my_key)
