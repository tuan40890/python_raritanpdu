#!/usr/bin/env python3

from cryptography.fernet import Fernet
import json
import os

#define global variables
KEY_FILE = "key.key"
CREDS_FILE = "creds.enc"


def key_gen():
    """
    Generates encrypted password for authentication
    """

    # generate and export an encryption key for credentials encryption and decryption
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    print(f"Encryption key generated and saved to '{KEY_FILE}'")

    # obtain credentials from user input
    username = input("Enter username: ")
    password = input("Enter password: ")

    # encrypt credentials
    creds = {"username": username, "password": password}
    encrypted_data = Fernet(key).encrypt(json.dumps(creds).encode())

    # export encrypted credentials
    with open(CREDS_FILE, "wb") as creds_file:
        creds_file.write(encrypted_data)
    print(f"Credentials encrypted and saved to '{CREDS_FILE}'")


if __name__ == "__main__":
    key_gen()
