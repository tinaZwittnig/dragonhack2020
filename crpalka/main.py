from mqtt import MQTTClient
from network import WLAN
import machine
import time

# connect to network
wlan = WLAN(mode=WLAN.STA)
wlan.connect("gmc", auth=(WLAN.WPA2, "12345678"), timeout=5000)

while not wlan.isconnected():
    machine.idle()
print("Device is now online :)")

# setup MQTT connection to broker and callbacks
client = MQTTClient("crpakla", "openfarm.v8.si",user="malina", password="Malina1234", port=1883)
#define subscription callback
def mqtt_cb(topic, msg):
    if topic == "crpalka/control":
        if msg == "force_stop":
            mqtt_override = 1
            mqtt_override_val = 0
        elif msg == "force_run":
            mqtt_override = 1
            mqtt_override_val = 1
        elif msg == "deactivate":
            mqtt_override = 0
            mqtt_override_val = None
client.set_callback(mqtt_cb)
client.connect()
client.subscribe(topic="crpalka/control")


# enter main loop
while True:
    

    #publish messages
    client.publish(topic="youraccount/feeds/lights", msg="OFF")

    # check for MQTT messages
    client.check_msg()
    # sleep for 1 s
    time.sleep(1)
