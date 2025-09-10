#!/usr/bin/env python3

import sys
import os
from raritan import rpc
from raritan.rpc import pdumodel
import raritan.rpc.net as net_rpc
from cryptography.fernet import Fernet
import json

# Configuration Constants
PDU_FILE = "pdu_ip.txt"
KEY_FILE = "pdu_key.key"
CREDS_FILE = "pdu_key.enc"

# Tee class to write to multiple streams (stdout and a file)
class Tee:
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()
    def flush(self):
        for f in self.files:
            f.flush()

def load_and_decrypt_credentials():
    """
    Loads the encryption key and encrypted credentials from files,
    then decrypts and returns the username and password.
    """
    try:
        with open(KEY_FILE, 'rb') as f:
            key = f.read()
        cipher_suite = Fernet(key)

        with open(CREDS_FILE, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
        creds = json.loads(decrypted_data)
        return creds['username'], creds['password']
    except FileNotFoundError:
        print(f"Error: Credential files '{KEY_FILE}' or '{CREDS_FILE}' not found.")
        print("Please run 'pdu_key.py' first to set up credentials.")
        sys.exit(1)
    except Exception as e:
        print(f"Error decrypting credentials: {e}")
        print("Ensure the key and encrypted credentials are valid and not corrupted.")
        sys.exit(1)

def get_pdu_info_and_save(pdu_ip, username, password):
    """
    Connects to a Raritan PDU, retrieves device and network information,
    power usage, and saves/prints the formatted output.
    """
    safe_pdu_ip = pdu_ip.replace('.', '_').replace(':', '-')
    filename = f"pdu_info_{safe_pdu_ip}.txt"
    original_stdout = sys.stdout
    file_handle = None

    print(f"\n--- Processing PDU: {pdu_ip} ---")

    try:
        file_handle = open(filename, 'w')
        sys.stdout = Tee(original_stdout, file_handle)

        agent = rpc.Agent("https", pdu_ip, username, password, disable_certificate_verification=True)
        network = net_rpc.Net("/net", agent)
        pdu = pdumodel.Pdu("/model/pdu/0", agent)

        pdu_settings = pdu.getSettings()
        pdu_meta = pdu.getMetaData()
        net_settings = network.getSettings()
        eth0_if_map = net_settings.ifMap.get("eth0")

        # DEVICE INFO
        print(f"[DEVICE INFO]\n"
              f"\tHostname: {pdu_settings.name}\n"
              f"\tManufacturer: {pdu_meta.nameplate.manufacturer}\n"
              f"\tModel: {pdu_meta.nameplate.model}\n"
              f"\tSN: {pdu_meta.nameplate.serialNumber}\n"
              f"\tFW Revision: {pdu_meta.fwRevision}")
        print("-------------------------------------------------------------------------------")

        # NETWORK INFO
        print(f"[NETWORK INFO]\n"
              f"\tIP Address: {eth0_if_map.ipv4.staticAddrCidr.addr}/{eth0_if_map.ipv4.staticAddrCidr.prefixLen}\n"
              f"\tGateway: {eth0_if_map.ipv4.staticDefaultGatewayAddr}\n"
              f"\tDNS: {net_settings.common.dns.serverAddrs}")
        print("-------------------------------------------------------------------------------")

        # POWER USAGE INFO
        inlet_power = 0
        inlets = pdu.getInlets()
        if inlets:
            # Note: This captures power of the last inlet if multiple exist.
            inlet_power = inlets[-1].getSensors().activePower.getReading().value

        for outlet in pdu.getOutlets():
            outlet_power = outlet.getSensors().activePower.getReading().value
            power_state = str(outlet.getState().powerState).split('_')[-1]
            label_num = outlet.getMetaData().label
            label_name = outlet.getSettings().name
            print(f"{int(outlet_power)} W\tOutlet {label_num}\tStatus {power_state}\t{label_name}")

        print("----------------------------")
        print(f"Total Active Power: {int(inlet_power)} W")
        print("-------------------------------------------------------------------------------")

    except Exception as e:
        sys.stdout.write(f"\nAn error occurred for PDU {pdu_ip}: {e}\n")
    finally:
        sys.stdout = original_stdout
        if file_handle:
            file_handle.close()
        print(f"PDU information for {pdu_ip} saved to '{filename}'\n\n\n")

if __name__ == "__main__":
    # Load and decrypt credentials
    username, password = load_and_decrypt_credentials()

    if not os.path.exists(PDU_FILE):
        print(f"Error: PDU IP file '{PDU_FILE}' not found. Create it with one PDU IP per line.")
        sys.exit(1)

    with open(PDU_FILE) as f:
        pdu_ips = [line.strip() for line in f if line.strip()]

    if not pdu_ips:
        print(f"Warning: No PDU IP addresses found in '{PDU_FILE}'. Exiting.")
        sys.exit(0)

    for ip in pdu_ips:
        get_pdu_info_and_save(ip, username, password)
