# Display Active Power
- This script uses RPC to obtain and display general info and active power usage of the Raritan Rack PDU
# Output Example:
```
[DEVICE INFO]
        Hostname: examplePDU1
        Manufacturer: Raritan
        Model: PX3-5464V
        SN: TT6234236235
        FW Revision: 4.0.0
-------------------------------------------------------------------------------
[NETWORK INFO]
        IP Address: 192.168.1.10/24
        Gateway: 192.168.1.1
        DNS: ['8.8.8.8', '4.4.4.4']
-------------------------------------------------------------------------------
0 W     Outlet 1
0 W     Outlet 2
0 W     Outlet 3
166 W   Outlet 4        baremetal1 PSU1
161 W   Outlet 5        baremetal2 PSU1
0 W     Outlet 6
165 W   Outlet 7        baremetal3 PSU1
149 W   Outlet 8        baremetal4 PSU1
140 W   Outlet 9        baremetal5 PSU1
144 W   Outlet 10       baremetal6 PSU1
----------------------------
Total Active Power: 925 W
-------------------------------------------------------------------------------
PDU information successfully saved to 'pdu_info.txt'
```
