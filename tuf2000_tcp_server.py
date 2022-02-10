"""
EXAMPLE
TUF2000F <- HF2211 -> Ethernet Modbus TCP Server

## Setup on TUF Device:
Menu 62: 9600, None, 0, 1
Menu 63: Modbus RTU Only 
Menu 26: Save to Default 1 

## Setup on HF2211 485 to Ethernet:
Protocol: TCP Server
Uart: 9600 / 8 / 1 / None / half duplex
Uart protocol: modbus
modbus timeout: auto
"""

from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import encode_ieee, decode_ieee, \
                              long_list_to_word, word_list_to_long

# Modbus TCP Server Address and Device Port
device_address = '192.168.1.10'
device_port= 502

# Register List (More list can be found at TUF-2000M User Manual)
ADDR_FLOW = 1
ADDR_EFR = 3
ADDR_T1 = 33
ADDR_T2 = 35
ADDR_SIGNAL_QUALITY = 92

# Functions to read float / integer value
class FloatModbusClient(ModbusClient):
    def read_float(self, address):
        """Read float(s) with read holding registers."""
        _reg = self.read_holding_registers(address, 2)
        if _reg:
            _temp = [decode_ieee(f) for f in word_list_to_long(_reg)]
            return float(*_temp)
        else:
            return None
    def read_integer(self, address):
        """Read integer with read holding registers."""
        _reg = self.read_holding_registers(address, 1)
        if _reg:
            return int(*_reg)
        else:
            return None

if __name__ == '__main__':
    # init modbus client
    c = FloatModbusClient(host=device_address, port=device_port, auto_open=True)

    """
    Example 1: get a float value (REAL 4 bytes), start from an address
    """
    flow = c.read_float(ADDR_FLOW)
    print("flow = ", flow, " m3/h")

    inlet_temp = c.read_float(ADDR_T1)
    print("inlet_temp = ", inlet_temp, " C")

    outlet_temp = c.read_float(ADDR_T2)
    print("outlet_temp = ", outlet_temp, " C")

    """
    Example 2: get a integer value (2 bytes), start from an address
    """
    signal_quality = c.read_integer(ADDR_SIGNAL_QUALITY)
    print("signal_quality = ", signal_quality)

    c.close()
