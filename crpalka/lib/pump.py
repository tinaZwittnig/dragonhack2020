import machine


def start():
    p_out = machine.Pin('P9', mode=machine.Pin.OUT)
    p_out.value(1)


def stop():
    p_out = machine.Pin('P9', mode=machine.Pin.OUT)
    p_out.value(0)
