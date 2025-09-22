#!/usr/bin/env python3

from cryptography.fernet import Fernet
import json
import os


#define global variables
KEY_FILE = "pdu_key.key"
CREDS_FILE = "pdu_creds.enc"


def key_gen():
    """
    Generates encrypted password to login to devices 
    """

    # generate and export an encryption key for credentials encryption/decryption
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    print(f"Encryption key generated and saved to '{KEY_FILE}'")

    # obtain credentials from user input
    username = input("Enter PDU username: ")
    password = input("Enter PDU password: ")

    # encrypt credentials
    creds = {"username": username, "password": password}
    encrypted_data = Fernet(key).encrypt(json.dumps(creds).encode())

    # export encrypted credentials
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
