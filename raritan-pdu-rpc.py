#!/usr/bin/env python3

import sys
import os
import json
import concurrent.futures
import threading
import datetime # Import the datetime module

from raritan import rpc
import raritan.rpc.pdumodel as pdumodel
import raritan.rpc.net as net_rpc
from cryptography.fernet import Fernet

# Configuration Constants
PDU_FILE = "pdu_ip.txt"
KEY_FILE = "pdu_key.key"
CREDS_FILE = "pdu_key.enc"
MAX_WORKERS = 10 # Number of concurrent PDU connections

# A lock for thread-safe printing to the console
print_lock = threading.Lock()

def process_pdu(pdu_ip, username, password):
    """
    Connects to a Raritan PDU, retrieves info, builds output,
    then saves to file and prints to console.
    """
    output_buffer = []

    try:
        output_buffer.append(f"\n--- Processing PDU: {pdu_ip} ---")

        agent = rpc.Agent("https", pdu_ip, username, password, disable_certificate_verification=True)
        network = net_rpc.Net("/net", agent)
        pdu = pdumodel.Pdu("/model/pdu/0", agent)

        pdu_settings = pdu.getSettings()
        pdu_meta = pdu.getMetaData()
        net_settings = network.getSettings()
        eth0_if_map = net_settings.ifMap.get("eth0")
        dns_servers = ', '.join(net_settings.common.dns.serverAddrs) if net_settings.common.dns.serverAddrs else 'N/A'

        # Use multi-line f-strings for concise output formatting
        output_buffer.append(f"""
[DEVICE INFO]
    Hostname: {pdu_settings.name}
    Manufacturer: {pdu_meta.nameplate.manufacturer}
    Model: {pdu_meta.nameplate.model}
    SN: {pdu_meta.nameplate.serialNumber}
    FW Revision: {pdu_meta.fwRevision}
-------------------------------------------------------------------------------
[NETWORK INFO]
    IP Address: {eth0_if_map.ipv4.staticAddrCidr.addr}/{eth0_if_map.ipv4.staticAddrCidr.prefixLen}
    Gateway: {eth0_if_map.ipv4.staticDefaultGatewayAddr}
    DNS: {dns_servers}
-------------------------------------------------------------------------------
[POWER USAGE INFO & OUTLET DESCRIPTIONS]""")

        inlet_power = 0
        inlets = pdu.getInlets()
        if inlets:
            inlet_power = inlets[-1].getSensors().activePower.getReading().value

        outlets_info = []
        for outlet in pdu.getOutlets():
            outlet_power = outlet.getSensors().activePower.getReading().value
            power_state = str(outlet.getState().powerState).split('_')[-1]
            label_num = outlet.getMetaData().label
            label_name = outlet.getSettings().name
            outlets_info.append(f"{int(outlet_power)}\tW\tOutlet {label_num}\tStatus {power_state}\t{label_name}")
        
        if not outlets_info:
            output_buffer.append("\tNo outlets found.")
        else:
            output_buffer.extend(outlets_info)

        safe_pdu_ip = pdu_ip.replace('.', '_').replace(':', '-')
        filename = f"pdu_info_{pdu_settings.name}_{safe_pdu_ip}.txt"

        output_buffer.append(f"""----------------------------
Total Active Power: {int(inlet_power)} W
-------------------------------------------------------------------------------
PDU information for {pdu_ip} saved to '{filename}'

""") # Added extra newlines for better separation in terminal output

    except Exception as e:
        output_buffer.append(f"\nAn error occurred for PDU {pdu_ip}: {e}\n"
                             f"PDU information for {pdu_ip} could not be fully retrieved. Error logged to '{filename}' if file was created.\n\n")

    finally:
        full_output = "\n".join(output_buffer)
        try:
            with open(filename, 'w') as f: f.write(full_output)
        except Exception as file_e:
            # If writing to file fails, print a critical error to console
            with print_lock:
                print(f"CRITICAL ERROR: Could not write PDU info to file {filename}: {file_e}")
                print(f"Output for {pdu_ip}:\n{full_output}")
        
        # Print the full output to the console in a thread-safe manner
        with print_lock:
            print(full_output, end='') # Use end='' to avoid double newlines

def load_and_decrypt_credentials():
    """Loads, decrypts, and returns username and password."""
    try:
        with open(KEY_FILE, 'rb') as f: key = f.read()
        cipher_suite = Fernet(key)
        with open(CREDS_FILE, 'rb') as f: encrypted_data = f.read()
        creds = json.loads(cipher_suite.decrypt(encrypted_data).decode())
        return creds['username'], creds['password']
    except FileNotFoundError:
        print(f"Error: Credential files '{KEY_FILE}' or '{CREDS_FILE}' not found.\n"
              "Please run 'pdu_key.py' first to set up credentials.")
        sys.exit(1)
    except Exception as e:
        print(f"Error decrypting credentials: {e}\n"
              "Ensure the key and encrypted credentials are valid and not corrupted.")
        sys.exit(1)

if __name__ == "__main__":
    # Record script start time
    script_start_time = datetime.datetime.now()
    print(f"Script started at: {script_start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    username, password = load_and_decrypt_credentials()

    if not os.path.exists(PDU_FILE):
        print(f"Error: PDU IP file '{PDU_FILE}' not found. Create it with one PDU IP per line.")
        sys.exit(1)

    with open(PDU_FILE) as f:
        pdu_ips = [line.strip() for line in f if line.strip()]

    if not pdu_ips:
        print(f"Warning: No PDU IP addresses found in '{PDU_FILE}'. Exiting.")
        sys.exit(0)

    print(f"Starting PDU information retrieval for {len(pdu_ips)} PDUs...")

    # Use ThreadPoolExecutor for concurrent execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_pdu, ip, username, password) for ip in pdu_ips]
        concurrent.futures.wait(futures) # Wait for all submitted tasks to complete

    # Record script end time
    script_end_time = datetime.datetime.now()
    total_runtime = script_end_time - script_start_time

    # Format total runtime into HH:MM:SS
    total_seconds = int(total_runtime.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    runtime_formatted = f"{hours:02}:{minutes:02}:{seconds:02}"

    print("Completed.")
    print(f"\nScript ended at: {script_end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total script runtime: {runtime_formatted}")
