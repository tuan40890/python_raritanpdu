# Display Active Power
- This script uses RPC to obtain and display general info and active power usage of the Raritan Rack PDUs.
- Outputs are generated into separate output files.
# Output Example:
```
(.venv) PS C:\Users\test-user\python_raritanpdu> python .\raritan-pdu-rpc.py

--- Processing PDU: 192.168.1.10 ---
[DEVICE INFO]
        Hostname: examplepdu1
        Manufacturer: Raritan
        Model: PX3-5464V
        SN: TT546843548
        FW Revision: 4.2
-------------------------------------------------------------------------------
[NETWORK INFO]
        IP Address: 192.168.1.10/24
        Gateway: 192.168.1.1
        DNS: ['8.8.8.8', '4.4.4.4']
-------------------------------------------------------------------------------
0 W     Outlet 1        Status OFF
0 W     Outlet 2        Status OFF
0 W     Outlet 3        Status OFF
167 W   Outlet 4        Status ON       example1 PSU1
160 W   Outlet 5        Status ON       example2 PSU1
0 W     Outlet 6        Status OFF
164 W   Outlet 7        Status ON       example3 PSU1
149 W   Outlet 8        Status ON       example4 PSU1
141 W   Outlet 9        Status ON       example5 PSU1
143 W   Outlet 10       Status ON       example6 PSU1
0 W     Outlet 11       Status OFF
179 W   Outlet 12       Status ON       example7 PSU1
14 W    Outlet 13       Status ON       example8 PSU1
186 W   Outlet 14       Status ON       example9 PSU1
184 W   Outlet 15       Status ON       example10 PSU1
0 W     Outlet 16       Status OFF
172 W   Outlet 17       Status ON       example11 PSU1
176 W   Outlet 18       Status ON       example12 PSU1
119 W   Outlet 19       Status ON       example13 PSU1
123 W   Outlet 20       Status ON       example14 PSU1
----------------------------
Total Active Power: 2084 W
-------------------------------------------------------------------------------
PDU information for 192.168.1.10 saved to 'pdu_info_192.168.1.10.txt'

--- Processing PDU: 192.168.1.11 ---
[DEVICE INFO]
        Hostname: examplepdu2
        Manufacturer: Raritan
        Model: PX3-5464V
        SN: TT464834453
        FW Revision: 4.2
-------------------------------------------------------------------------------
[NETWORK INFO]
        IP Address: 192.168.1.11/24
        Gateway: 192.168.1.1
        DNS: ['8.8.8.8', '4.4.4.4']
-------------------------------------------------------------------------------
0 W     Outlet 1        Status OFF
157 W   Outlet 2        Status ON       example11 PSU2
158 W   Outlet 3        Status ON       example22 PSU2
169 W   Outlet 4        Status ON       example33 PSU2
162 W   Outlet 5        Status ON       example44 PSU2
0 W     Outlet 6        Status OFF
163 W   Outlet 7        Status ON       example55 PSU2
160 W   Outlet 8        Status ON       example66 PSU2
126 W   Outlet 9        Status ON       example77 PSU2
135 W   Outlet 10       Status ON       example88 PSU2
0 W     Outlet 11       Status OFF
12 W    Outlet 12       Status ON       example99 PSU2
11 W    Outlet 13       Status ON       example100 PSU2
174 W   Outlet 14       Status ON       example111 PSU2
186 W   Outlet 15       Status ON       example122 PSU2
0 W     Outlet 16       Status OFF
158 W   Outlet 17       Status ON       example133 PSU2
173 W   Outlet 18       Status ON       example144 PSU2
124 W   Outlet 19       Status ON       example155 PSU2
44 W    Outlet 20       Status ON       example166 PSU2
----------------------------
Total Active Power: 2115 W
-------------------------------------------------------------------------------
PDU information for 192.168.1.11 saved to 'pdu_info_192.168.1.11.txt'
```
