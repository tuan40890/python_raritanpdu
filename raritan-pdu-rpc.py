#!/usr/bin/env python3

import json
import datetime
import concurrent.futures
import pandas as pd
from cryptography.fernet import Fernet
from raritan import rpc
import raritan.rpc.pdumodel as pdumodel
import raritan.rpc.net as net_rpc
import raritan.rpc.datetime as ntp


# define variables to access files
PDU_IP_ADDRESSES = "pdu_ip.txt"
KEY_FILE = "pdu_key.key"
CREDS_FILE = "pdu_creds.enc"


def load_creds():
    '''
    Load the credentials from .key and .enc files
    '''

    try:
        # open .key file in read & binary mode "rb" 
        key = open(KEY_FILE, "rb").read()

        # use the .key file to unlock the encrypted .enc file and decrypt it
        data = Fernet(key).decrypt(open(CREDS_FILE, "rb").read())

        # after decryption, data is still a byte string, decode it into normal strings
        str_creds = json.loads(data.decode())

        # extract the decoded strings to return the values
        return str_creds["username"], str_creds["password"]
    except Exception as e:
        print(f"Credential error: {e}")
        sys.exit(1)


def pdu_retrieve_info(ip, user, password):
    '''
    Retrieve PDU info and export it to a .txt file
    '''

    # set an empty list to obtain sectional outputs after
    display_output = []

    try:

        # create an agent
        agent = rpc.Agent("https", ip, user, password, disable_certificate_verification=True)
        network = net_rpc.Net("/net", agent)
        pdu = pdumodel.Pdu("/model/pdu/0", agent)
        pdu_inlet = pdumodel.Inlet("/model/inlet/0", agent)
        ntpservers = ntp.DateTime("/datetime", agent)

        # set variables to store PDU data
        retrieve_hostname = pdu.getSettings().name
        retrieve_manufacturer = pdu.getMetaData().nameplate.manufacturer
        retrieve_model = pdu.getMetaData().nameplate.model
        retrieve_inlet = pdu_inlet.getMetaData().plugType[5:]
        retrieve_serial = pdu.getMetaData().nameplate.serialNumber
        retrieve_fw_ver = pdu.getMetaData().fwRevision

        # retrieve data and append output
        display_output.append("[DEVICE INFO]\n"
        f"Hostname : {retrieve_hostname}\n"
        f"Manufacturer : {retrieve_manufacturer}\n"
        f"Model : {retrieve_model}\n"
        f"Inlet Type : {retrieve_inlet}\n"
        f"Serial Number : {retrieve_serial}\n"
        f"FW Revision : {retrieve_fw_ver}\n"
        "-------------------------------------------------------------------------------\n")

        # set variables to store network data
        retrieve_net = network.getSettings()
        retrieve_eth_addr = retrieve_net.ifMap.get("eth0").ipv4.staticAddrCidr.addr
        retrieve_eth_prefixLen = retrieve_net.ifMap.get("eth0").ipv4.staticAddrCidr.prefixLen
        retrieve_eth_gw = retrieve_net.ifMap.get("eth0").ipv4.staticDefaultGatewayAddr
        retrieve_dns = retrieve_net.common.dns.serverAddrs
        retrieve_ntp = ntpservers.getActiveNtpServers()

        # retrieve data and append output
        display_output.append("[NETWORK INFO]\n"
        f"IP Address : {retrieve_eth_addr}/{retrieve_eth_prefixLen}\n"
        f"Gateway : {retrieve_eth_gw}\n"
        f"DNS : {retrieve_dns}\n"
        f"NTP : {retrieve_ntp}\n"
        "-------------------------------------------------------------------------------\n")

        display_output.append("[OUTLET INFO]")

        # set an empty list to store all the looped outputs in this section
        all_outlets_data = []

        # store the column headers in the headers variable
        header = ["Watts", "Outlet", "Type", "Status", "Description"]

        # loop over each outlet to obtain outlet data
        for outlet in pdu.getOutlets():

            # set variables to store outlet data
            retrieve_outlet_watts = round(outlet.getSensors().activePower.getReading().value)
            retrieve_outlet_label = outlet.getMetaData().label
            retrieve_outlet_receptacletype = outlet.getMetaData().receptacleType[-3:]
            retrieve_outlet_status = str(outlet.getState().powerState).split("_")[-1]
            retrieve_outlet_description = outlet.getSettings().name

            # then store the variables from above into a new list
            each_outlet_data = [retrieve_outlet_watts,
                                retrieve_outlet_label,
                                retrieve_outlet_receptacletype,
                                retrieve_outlet_status,
                                retrieve_outlet_description]
            
            # append the new list to the current list
            all_outlets_data.append(each_outlet_data)
        
        # create a table using pandas, hide index number and align left
        df = pd.DataFrame(all_outlets_data, columns=header).to_string(index=False, justify='left')
        display_output.append(df)

        # display inlet's current active power
        inlet_power = round(pdu.getInlets()[-1].getSensors().activePower.getReading().value)
        display_output.append(f"----------------------------\nTotal Active Power: {inlet_power} W")
        display_output.append("-------------------------------------------------------------------------------\n")

        # name the output variable and append output data to it
        output_file_name = f"pdu_{retrieve_hostname}.txt"
        display_output.append(f"PDU info is exported to '{output_file_name}'\n\n")
    except Exception as e:
        display_output.append(f"\nError for {retrieve_hostname} with IP {ip}: {e}\n")

    # join all outputs into one string, remove the \n from the list
    joining_output = "\n".join(display_output)
    
    try:
        with open(output_file_name, "w") as file:
            file.write(joining_output)
    except Exception as e:
        joining_output += f"\nCRITICAL: cannot write {output_file_name}: {e}\n"
    return joining_output


if __name__ == "__main__":

    '''all the print statements here provide terminal outputs, they're not exported to a file'''

    # start timer before running the script to estimate how long the script takes to complete
    script_starting_time = datetime.datetime.now()
    print(f"\nScript started at {script_starting_time:%H:%M:%S} on {script_starting_time:%m-%d-%Y}\n")

    # load the credentials (to be used for concurrency later)
    user, password = load_creds()

    # check if file pdu_ip.txt exists in the same directory, a failure occurs if it's not, stop running the script
    if not os.path.exists(PDU_IP_ADDRESSES):
        print(f"Missing '{PDU_IP_ADDRESSES}'")
        sys.exit(1)

    # use list comprehension to include only the stripped IP addresses
    ip_addresses = [each_line.strip() for each_line in open(PDU_IP_ADDRESSES) if each_line.strip()]
    if not ip_addresses:
        print("No IPs found. Exiting.")
        # if no IPs found, and there's no error, stop running the script
        sys.exit(0)

    print(f"Starting PDU information retrieval for {len(ip_addresses)} PDUs...\n")
    # deploy ThreadPoolExecutor to use multi-threading to achieve concurrency
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor_object:
        for future_object in concurrent.futures.as_completed(
            executor_object.submit(pdu_retrieve_info, ip, user, password) for ip in ip_addresses
        ):
            # future_object.result() is the result that came from the pdu_retrieve_info()
            print(future_object.result(), end="")

    script_ending_time = datetime.datetime.now()
    duration = int((script_ending_time - script_starting_time).total_seconds())
    hour, remainder = divmod(duration, 3600)
    minute, second = divmod(remainder, 60)

    print("Completed.")
    print(f"\nScript ended at {script_ending_time:%H:%M:%S} on {script_ending_time:%m-%d-%Y}")
    print(f"Total script runtime: {hour:02}:{minute:02}:{second:02}")
