# Display PDU Info
- This python script interacts with the RPC API to obtain and display data from the Raritan Rack PDUs
- It also uses the cryptography library to encrypt the password that the user enters
- First, run `key_gen.py` to enter credentials to generate the encrypted files `key.key` and `creds.enc`
- These two encrypted files are required for the script `raritan-pdu-rpc.py` to run
- Below is the output example for all PDUs on the terminal, and it includes the starting and ending time
- In additiona, output for each PDU is generated into separate .txt files
# Output Example:
```
test-user@test-vm:~/python_raritanpdu_rpc$ uv run raritan-pdu-rpc.py 

Script started at 21:22:19 on 09-10-2025

Retrieving data for 4 devices...

[DEVICE INFO]
Hostname : examplePDU1
Manufacturer : Raritan
Model : PX3-5464V
Inlet Type : L6-30P
Serial Number : 54646352323
FW Revision : 4.3.0.5-51180
-------------------------------------------------------------------------------

[NETWORK INFO]
IP Address : 192.168.1.10/24
Gateway : 192.168.1.1
DNS : ['8.8.8.8', '4.4.4.4']
NTP : ['0.north-america.pool.ntp.org', '1.north-america.pool.ntp.org']
-------------------------------------------------------------------------------

[OUTLET INFO]
 Watts Outlet Type Status Description           
  0     1     C19  OFF                          
156     2     C13   ON           machine1 PSU1
160     3     C13   ON           machine2 PSU1
150     4     C13   ON           machine3 PSU1
149     5     C13   ON           machine4 PSU1
  0     6     C19  OFF                          
163     7     C13   ON           machine5 PSU1
164     8     C13   ON           machine6 PSU1
189     9     C13   ON           machine7 PSU1
  0    10     C13  OFF                          
  0    11     C19  OFF                          
  0    12     C13  OFF                          
  0    13     C13  OFF                          
  0    14     C13  OFF                          
  0    15     C13  OFF                          
  0    16     C19  OFF                          
  0    17     C13  OFF                          
  0    18     C13  OFF                          
140    19     C13   ON            machine8 PSU2
 41    20     C13   ON            machine9 PSU2
----------------------------
Total Active Power: 1311 W
-------------------------------------------------------------------------------

Output is exported to 'examplePDU1.txt'

[DEVICE INFO]
Hostname : examplePDU2
Manufacturer : Raritan
Model : PX3-5464V
Inlet Type : L6-30P
Serial Number : 42352342363
FW Revision : 4.3.0.5-51180
-------------------------------------------------------------------------------

[NETWORK INFO]
IP Address : 192.168.1.11/24
Gateway : 192.168.1.1
DNS : ['8.8.8.8', '4.4.4.4']
NTP : ['0.north-america.pool.ntp.org', '1.north-america.pool.ntp.org']
-------------------------------------------------------------------------------

[OUTLET INFO]
 Watts Outlet Type Status Description           
  0     1     C19  OFF                          
146     2     C13   ON           machine11 PSU2
159     3     C13   ON           machine12 PSU2
159     4     C13   ON           machine13 PSU2
161     5     C13   ON           machine14 PSU2
  0     6     C19  OFF                          
149     7     C13   ON           machine15 PSU2
157     8     C13   ON           machine16 PSU2
185     9     C13   ON           machine17 PSU2
  0    10     C13  OFF                          
  0    11     C19  OFF                          
  0    12     C13  OFF                          
  0    13     C13  OFF                          
  0    14     C13  OFF                          
  0    15     C13  OFF                          
  0    16     C19  OFF                          
  0    17     C13  OFF                          
  0    18     C13  OFF                          
146    19     C13   ON            machine18 PSU1
 29    20     C13   ON            machine19 PSU1
----------------------------
Total Active Power: 1284 W
-------------------------------------------------------------------------------

Output is exported to 'examplePDU2.txt'
```
