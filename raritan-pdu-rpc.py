#!/usr/bin/env python3
import sys, os, json, datetime, concurrent.futures
from cryptography.fernet import Fernet
from raritan import rpc
import raritan.rpc.pdumodel as pdumodel
import raritan.rpc.net as net_rpc

PDU_FILE, KEY_FILE, CREDS_FILE, MAX_WORKERS = "pdu_ip.txt", "pdu_key.key", "pdu_key.enc", 10

def load_creds():
    try:
        key = open(KEY_FILE,'rb').read()
        data = Fernet(key).decrypt(open(CREDS_FILE,'rb').read())
        c = json.loads(data.decode());  return c["username"], c["password"]
    except Exception as e:
        print(f"Credential error: {e}"); sys.exit(1)

def process_pdu(ip, user, pw):
    out = [f"\n--- Processing PDU: {ip} ---"]
    safe = ip.replace('.','_').replace(':','-')
    fn = f"pdu_info_{safe}.txt"
    try:
        a = rpc.Agent("https", ip, user, pw, disable_certificate_verification=True)
        net = net_rpc.Net("/net", a)
        pdu = pdumodel.Pdu("/model/pdu/0", a)

        s = pdu.getSettings(); m = pdu.getMetaData(); ns = net.getSettings()
        eth = ns.ifMap.get("eth0")
        dns = ', '.join(ns.common.dns.serverAddrs) if ns.common.dns.serverAddrs else 'N/A'
        fn = f"pdu_info_{s.name}.txt"

        out.append(f"""
[DEVICE INFO]
    Hostname: {s.name}
    Manufacturer: {m.nameplate.manufacturer}
    Model: {m.nameplate.model}
    SN: {m.nameplate.serialNumber}
    FW Revision: {m.fwRevision}
-------------------------------------------------------------------------------
[NETWORK INFO]
    IP Address: {eth.ipv4.staticAddrCidr.addr}/{eth.ipv4.staticAddrCidr.prefixLen}
    Gateway: {eth.ipv4.staticDefaultGatewayAddr}
    DNS: {dns}
-------------------------------------------------------------------------------
[POWER USAGE INFO & OUTLET DESCRIPTIONS]""")

        inlets = pdu.getInlets()
        inlet_power = inlets[-1].getSensors().activePower.getReading().value if inlets else 0

        outs = []
        for o in pdu.getOutlets():
            w = int(o.getSensors().activePower.getReading().value)
            state = str(o.getState().powerState).split('_')[-1]
            outs.append(f"{w}\tW\tOutlet {o.getMetaData().label}\tStatus {state}\t{o.getSettings().name}")

        out.extend(outs or ["\tNo outlets found."])
        out.append(f"""----------------------------
Total Active Power: {int(inlet_power)} W
-------------------------------------------------------------------------------
PDU information for {ip} saved to '{fn}'

""")
    except Exception as e:
        out.append(f"\nError for {ip}: {e}\n")

    txt = "\n".join(out)
    try:
        with open(fn,'w') as f: f.write(txt)
    except Exception as e:
        txt += f"\nCRITICAL: cannot write {fn}: {e}\n"
    return txt

if __name__ == "__main__":
    start = datetime.datetime.now()
    print(f"Script started at: {start:%Y-%m-%d %H:%M:%S}\n")
    user, pw = load_creds()

    if not os.path.exists(PDU_FILE):
        print(f"Missing '{PDU_FILE}'"); sys.exit(1)
    ips = [l.strip() for l in open(PDU_FILE) if l.strip()]
    if not ips:
        print("No IPs found. Exiting."); sys.exit(0)

    print(f"Starting PDU information retrieval for {len(ips)} PDUs...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        for fut in concurrent.futures.as_completed(ex.submit(process_pdu, ip, user, pw) for ip in ips):
            print(fut.result(), end='')

    end = datetime.datetime.now()
    dur = int((end - start).total_seconds()); h, r = divmod(dur, 3600); m, s = divmod(r, 60)
    print("Completed.")
    print(f"\nScript ended at: {end:%Y-%m-%d %H:%M:%S}")
    print(f"Total script runtime: {h:02}:{m:02}:{s:02}")
