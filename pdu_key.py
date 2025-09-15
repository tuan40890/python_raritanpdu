#!/usr/bin/env python3

from cryptography.fernet import Fernet
import json
import os

KEY_FILE = "pdu_key.key"
CREDS_FILE = "pdu_key.enc"

def key_gen():
    """
    Generates an encryption key, prompts for PDU credentials, encrypts them, and saves both to files.
    """
    # Generate and save encryption key
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    print(f"Encryption key generated and saved to '{KEY_FILE}'")

    # Get credentials from user input
    username = input("Enter PDU username: ")
    password = input("Enter PDU password: ")

    # Encrypt credentials
    creds = {"username": username, "password": password}
    encrypted_data = Fernet(key).encrypt(json.dumps(creds).encode())

    # Save encrypted credentials
    with open(CREDS_FILE, "wb") as creds_file:
        creds_file.write(encrypted_data)
    print(f"Credentials encrypted and saved to '{CREDS_FILE}'")
    print("\nIMPORTANT: Keep 'pdu_key.key' and 'pdu_creds.enc' secure.")
    print(
        "For better security, consider storing the key in an environment variable or a dedicated secret management solution."
    )


if __name__ == "__main__":
    if os.path.exists(KEY_FILE) or os.path.exists(CREDS_FILE):
        response = input(
            f"Warning: '{KEY_FILE}' or '{CREDS_FILE}' already exist. Overwrite? (y/N): "
        )
        if response.lower() != "y":
            print("Operation cancelled.")
            exit()
    key_gen()
