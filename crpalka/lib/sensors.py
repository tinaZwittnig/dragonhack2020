import machine
from onewire import DS18X20
from onewire import OneWire

ow = OneWire(machine.Pin('P7'))


# read 12 V
def measure_voltage():
    adc = machine.ADC()             # create an ADC object
    apin = adc.channel(pin='P16')   # create an analog pin on P16
    return apin() * 0.0031

# check water level
def check_water():
    p_in = machine.Pin('P9', mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
    if p_in() > 0:
        return 0
    else:
        return 1
    return p_in()

# read temperature
def read_temperature():
    temp = DS18X20(ow)
    t_val = temp.read_temp_async()
    temp.start_conversion()
    return t_val
