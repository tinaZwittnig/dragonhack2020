
import datetime
import psycopg2
import paho.mqtt.client as mqtt

MQTT_ADDRESS = 'openfarm.v8.si'
MQTT_USER = 'user'
MQTT_PASSWORD = 'password'
MQTT_CLIENT_ID = 'Consumer'
CONNECTION = "postgres://user:password@openfarm.v8.si/iotfarm"
# conn = psycopg2.connect(CONNECTION)
# cur = conn.cursor()
# query_create_sensors_temperature =  """CREATE TABLE temperature (
#                                            time TIMESTAMP NOT NULL,
#                                            device_id INTEGER,
#                                            temperature DOUBLE PRECISION
#                                            );"""
# query_create_sensors_voltage =  """CREATE TABLE voltage (
#                                            time TIMESTAMP NOT NULL,
#                                            device_id INTEGER,
#                                            voltage DOUBLE PRECISION
#                                            );"""
# cur.execute(query_create_sensors_temperature)
# cur.execute(query_create_sensors_voltage)
# conn.commit()
# cur.close()


def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe('pastir/napetost')
    client.subscribe('pastir/temperatura')



def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(float(msg.payload.decode("utf-8"))))
    if msg.topic == 'pastir/temperatura':
        temp = float(msg.payload.decode("utf-8"))
        try:
            conn = psycopg2.connect(CONNECTION)
            with conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO temperature (time, device_id, temperature) VALUES ('{}',{},{});".format(str(datetime.datetime.now()),0,temp))
                conn.commit()
        except Exception as e:
            print(e)


    elif msg.topic == 'pastir/napetost':
        voltage = float(msg.payload.decode("utf-8"))
        try:
            conn = psycopg2.connect(CONNECTION)
            with conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO voltage (time, device_id, voltage)  VALUES ('{}',{},{});".format(str(datetime.datetime.now()),0,voltage))
                conn.commit()
        except:
            print("something went wrong!")


def main():

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to DB bridge')
    main()
