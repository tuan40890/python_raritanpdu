#!/usr/bin/env python3

import sys
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

def get_pdu_info_and_save(filename="pdu_info.txt"):
    """
    Connects to a Raritan PDU, retrieves device and network information,
    power usage, and saves the formatted output to a specified text file,
    while also printing to the terminal.
    """
    original_stdout = sys.stdout
    file_handle = None # Initialize file_handle to None

    try:
        file_handle = open(filename, 'w')
        # Redirect stdout to a Tee object that writes to both original stdout and the file
        sys.stdout = Tee(original_stdout, file_handle)

        # Initialize RPC agent and PDU/Network objects
        agent = rpc.Agent("https", "192.168.1.10", "admin", "admin", disable_certificate_verification=True)
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
        inlet_energy_sensor = 0 # Will store the last inlet's reading as per original logic
        for inlet in pdu.getInlets():
            inlet_energy_sensor = inlet.getSensors().activePower.getReading().value

        # Obtain outlet names and their active power
        for outlet in pdu.getOutlets():
            outlet_energy_sensor = outlet.getSensors().activePower.getReading().value
            label_num = outlet.getMetaData().label
            label_name = outlet.getSettings().name
            print(f"{int(outlet_energy_sensor)} W\tOutlet {label_num}\t{label_name}")

        print("----------------------------")
        print(f"Total Active Power: {int(inlet_energy_sensor)} W")
        print("-------------------------------------------------------------------------------")

    except Exception as e:
        # Print error to both console and file if Tee is active, otherwise just console
        if sys.stdout is not original_stdout:
            sys.stdout.write(f"\nAn error occurred: {e}\n")
        else:
            print(f"\nAn error occurred: {e}\n")
    finally:
        # Restore original stdout
        sys.stdout = original_stdout
        # Close the file handle if it was opened
        if file_handle:
            file_handle.close()
        # This message should only go to the console
        print(f"PDU information successfully saved to '{filename}'")

# Execute the function
if __name__ == "__main__":
    get_pdu_info_and_save()
