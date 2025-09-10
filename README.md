# Display Active Power
- This script uses RPC to obtain and display general info and active power usage of the Raritan Rack PDUs.
- It also displays outlet number, power status, and description
- Outputs are generated into separate output files.
- First, run `pdu_key.py` to enter credentials to generate the encrypted files `pdu_key.key` and `pdu_key.enc`
- The two encrypted files are required for the script `raritan-pdu-rpc.py` to run 
# Output Example:
```
(.venv) PS C:\Users\test-user\python_raritanpdu> python .\raritan-pdu-rpc.py                       
                                                                                                                             
--- Processing PDU: 192.168.1.10 ---
[DEVICE INFO]
        Hostname: examplepdu1
        Manufacturer: Raritan
        Model: PX3-5464V
        SN: TT9283792387
        FW Revision: 4.1
-------------------------------------------------------------------------------
[NETWORK INFO]
        IP Address: 192.168.1.10/24
        Gateway: 192.168.1.1
        DNS: ['8.8.8.8', '4.4.4.4']
-------------------------------------------------------------------------------
0       W       Outlet 1        Status ON
0       W       Outlet 2        Status ON
0       W       Outlet 3        Status ON
167     W       Outlet 4        Status ON       bm1tbv
167     W       Outlet 5        Status ON       bm2sbfsb
0       W       Outlet 6        Status ON
165     W       Outlet 7        Status ON       bm3fdbz
149     W       Outlet 8        Status ON       bm4cbzm
141     W       Outlet 9        Status ON       bm5sz
143     W       Outlet 10       Status ON       bm6bfw
0       W       Outlet 11       Status ON
177     W       Outlet 12       Status ON       bm7dvxcb
14      W       Outlet 13       Status ON       bm8bzcn
188     W       Outlet 14       Status ON       bm9sgwe
185     W       Outlet 15       Status ON       bm10dbn
0       W       Outlet 16       Status ON
172     W       Outlet 17       Status ON       bm11zbsz
176     W       Outlet 18       Status ON       bm12cbsz
118     W       Outlet 19       Status ON       bm13xcb
123     W       Outlet 20       Status ON       bm14ewg
----------------------------
Total Active Power: 2085 W
-------------------------------------------------------------------------------
PDU information for 192.168.1.10 saved to 'pdu_info_192_168_1_10.txt'




--- Processing PDU: 192.168.1.11 ---
[DEVICE INFO]
        Hostname: examplepdu2
        Manufacturer: Raritan
        Model: PX3-5464V
        SN: TT9141926387
        FW Revision: 4.1
-------------------------------------------------------------------------------
[NETWORK INFO]
        IP Address: 192.168.1.11/24
        Gateway: 192.168.1.1
        DNS: ['8.8.8.8', '4.4.4.4']
-------------------------------------------------------------------------------
0       W       Outlet 1        Status ON
152     W       Outlet 2        Status ON       bm15vdb
154     W       Outlet 3        Status ON       bm16zdzb
171     W       Outlet 4        Status ON       bm17dvzdsb
162     W       Outlet 5        Status ON       bm18BSSdb
0       W       Outlet 6        Status ON
164     W       Outlet 7        Status ON       bm19bsc
160     W       Outlet 8        Status ON       bm20cxbzcb
126     W       Outlet 9        Status ON       bm21cbs
141     W       Outlet 10       Status ON       bm22sbd
0       W       Outlet 11       Status ON
12      W       Outlet 12       Status ON       bm23zbs
10      W       Outlet 13       Status ON       bm24sBBs
177     W       Outlet 14       Status ON       bm25Sb
186     W       Outlet 15       Status ON       bm26bbsb
0       W       Outlet 16       Status ON
158     W       Outlet 17       Status ON       bm27bzdfn
173     W       Outlet 18       Status ON       bm28fv
125     W       Outlet 19       Status ON       bm29wfmh
44      W       Outlet 20       Status ON       bm30fx
----------------------------
Total Active Power: 2111 W
-------------------------------------------------------------------------------
PDU information for 192.168.1.11 saved to 'pdu_info_192_168_1_11.txt'
```
