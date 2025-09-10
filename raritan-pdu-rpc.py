#!/usr/bin/env python3

import sys
import os
from raritan import rpc
from raritan.rpc import pdumodel
import raritan.rpc.net as net_rpc

# Define a Tee class to write to multiple streams
class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # Ensure immediate write to all streams

    def flush(self):
        for f in self.files:
            f.flush()

def get_pdu_info_and_save(pdu_ip, username, password):
    """
    Connects to a Raritan PDU, retrieves device and network information,
    power usage, and saves the formatted output to a specified text file,
    while also printing to the terminal.
    """
    # Sanitize IP for filename to avoid issues with special characters
    safe_pdu_ip = pdu_ip.replace('.', '_').replace(':', '-')
    filename = f"pdu_info_{safe_pdu_ip}.txt"

    original_stdout = sys.stdout
    file_handle = None

    print(f"\n--- Processing PDU: {pdu_ip} ---") # Print to original stdout

    try:
        file_handle = open(filename, 'w')
        # Redirect stdout to a Tee object that writes to both original stdout and the file
        sys.stdout = Tee(original_stdout, file_handle)

        # Initialize RPC agent and PDU/Network objects
        agent = rpc.Agent("https", pdu_ip, username, password, disable_certificate_verification=True)
        network = net_rpc.Net("/net", agent)
        pdu = pdumodel.Pdu("/model/pdu/0", agent)

        # Retrieve common settings and metadata once for efficiency
        pdu_settings = pdu.getSettings()
        pdu_meta = pdu.getMetaData()
        net_settings = network.getSettings()
        eth0_if_map = net_settings.ifMap.get("eth0")

        # DEVICE INFO
        hostname = pdu_settings.name
        manufacturer = pdu_meta.nameplate.manufacturer
        model = pdu_meta.nameplate.model
        serial = pdu_meta.nameplate.serialNumber
        fw = pdu_meta.fwRevision

        print(f"[DEVICE INFO]\n"
              f"\tHostname: {hostname}\n"
              f"\tManufacturer: {manufacturer}\n"
              f"\tModel: {model}\n"
              f"\tSN: {serial}\n"
              f"\tFW Revision: {fw}")

        print("-------------------------------------------------------------------------------")

        # NETWORK INFO
        ip = eth0_if_map.ipv4.staticAddrCidr.addr
        subnet = eth0_if_map.ipv4.staticAddrCidr.prefixLen
        gw = eth0_if_map.ipv4.staticDefaultGatewayAddr
        dns = net_settings.common.dns.serverAddrs

        print(f"[NETWORK INFO]\n"
              f"\tIP Address: {ip}/{subnet}\n"
              f"\tGateway: {gw}\n"
              f"\tDNS: {dns}")

        print("-------------------------------------------------------------------------------")

        # POWER USAGE INFO
        # Obtain currently active power usage in Watts per PDU inlet
        # Note: The original logic captures only the last inlet's reading if multiple exist.
        inlet_energy_sensor = 0
        inlets = pdu.getInlets()
        if inlets:
            for inlet in inlets:
                inlet_energy_sensor = inlet.getSensors().activePower.getReading().value

        # Obtain outlet names and their active power
        for outlet in pdu.getOutlets():
            outlet_energy_sensor = outlet.getSensors().activePower.getReading().value
            outlet_pwstat = str(outlet.getState().powerState)
            splitted_outlet_pwstat = outlet_pwstat.split('_')[-1]
            label_num = outlet.getMetaData().label
            label_name = outlet.getSettings().name
            print(f"{int(outlet_energy_sensor)} W\tOutlet {label_num}\tStatus {splitted_outlet_pwstat}\t{label_name}")

        print("----------------------------")
        print(f"Total Active Power: {int(inlet_energy_sensor)} W")
        print("-------------------------------------------------------------------------------")

    except Exception as e:
        # Print error to both console and file if Tee is active, otherwise just console
        if sys.stdout is not original_stdout:
            sys.stdout.write(f"\nAn error occurred for PDU {pdu_ip}: {e}\n")
        else:
            print(f"\nAn error occurred for PDU {pdu_ip}: {e}\n")
    finally:
        # Restore original stdout
        sys.stdout = original_stdout
        # Close the file handle if it was opened
        if file_handle:
            file_handle.close()
        # This message should only go to the console
        if 'filename' in locals():
            print(f"PDU information for {pdu_ip} saved to '{filename}'\n\n\n")
        else:
            print(f"PDU information for {pdu_ip} could not be saved to a file due to an earlier error.\n\n\n")

# Execute the function
if __name__ == "__main__":
    pdu_file = "pdu_ip.txt"
    username = "admin" # PDU username
    password = "admin" # PDU password

    if not os.path.exists(pdu_file):
        print(f"Error: PDU IP file '{pdu_file}' not found.")
        print("Please create 'pdu_ip.txt' with one PDU IP address per line.")
        sys.exit(1)

    with open(pdu_file, 'r') as f:
        # Read non-empty lines and strip whitespace
        pdu_ips = [line.strip() for line in f if line.strip()]

    if not pdu_ips:
        print(f"Warning: No PDU IP addresses found in '{pdu_file}'. Exiting.")
        sys.exit(0)

    for ip in pdu_ips:
        get_pdu_info_and_save(ip, username, password)
