#!/usr/bin/env python3

from raritan import rpc
from raritan.rpc import pdumodel

agent = rpc.Agent("https", "10.102.4.2", "admin", "admin", disable_certificate_verification = True)
pdu = pdumodel.Pdu("/model/pdu/0", agent)

# obtain currently active power usage in Watts per PDU inlet
for inlet in pdu.getInlets():
    energy_sensor = inlet.getSensors().activePower
    print("%d W" % energy_sensor.getReading().value)

