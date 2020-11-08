import datetime
import psycopg2
import paho.mqtt.client as mqtt
import os
from twilio.rest import Client
import time

import smtplib
from email.mime.text import MIMEText




port = 465
smtp_server = "example@gmail.si"
sender_email = "alert@marta.v8.si"
receiver_email = "farma@gmail.com"
smtp_password = "farma1234"



MQTT_ADDRESS = 'openfarm.v8.si'
MQTT_USER = 'user'
MQTT_PASSWORD = 'pass'
MQTT_CLIENT_ID = 'Alert'

account_sid = 'user'
auth_token = 'pass'
sms_client = Client(account_sid, auth_token)

last_send_temp = 0
last_send_voltage = 0


def send_mail(type, value):

    msg = ""
    if type == 'temperature':
        msg = MIMEText(
            """Temperature of in the pasture is {}! You should check if everything is ok with animals.""".format(
                                                                                                                 value))
        msg['Subject'] = '[IOT FARM] Temperature of pasture'

    elif type == 'voltage':
        msg = MIMEText(
            """Volatage of battery is {}V. You should recharge it now!""".format(
                                                                                                                 value))
        msg['Subject'] = '[IOT FARM] Voltage of battery'


    msg['From'] = sender_email
    msg['To'] = receiver_email

    server = smtplib.SMTP_SSL(smtp_server, port)
    server.login(sender_email, smtp_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("mail successfully sent")
    return None

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe('pastir/napetost')
    client.subscribe('pastir/temperatura')



def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(float(msg.payload.decode("utf-8"))),'burek')
    global last_send_temp
    global last_send_voltage
    if msg.topic == 'pastir/temperatura':
        temp = float(msg.payload.decode("utf-8"))
        if temp > 30:
            timenow = time.time()
            if abs(timenow - last_send_temp) > 600:
                try:
                    send_mail('temperature', temp)
                    message = sms_client.messages.create(
                        body='[IOT FARM] Temperature in the pasture is {}! You should check if animals are OK.'.format(temp),
                        from_='+17472236425',
                        to='+38641537822'
                    )
                    last_send_temp = timenow
                    #print(message.sid)
                except Exception as e:
                    print("Something wentr wrong :",e)

    elif msg.topic == 'pastir/napetost':
        voltage = float(msg.payload.decode("utf-8"))
        if voltage<11.5:
            timenow = time.time()

            if abs(timenow - last_send_voltage) > 600:
                try:
                    send_mail('temperature', voltage)
                    message = sms_client.messages.create(
                        body='Voltage in the "pastir" has dropped below 11.5V! You should recharged it.',
                        from_='+17472236425',
                        to='+38651384469'
                     )
                    last_send_voltage = timenow
                    print(message.sid)
                except Exception as e:
                    print("Something wentr wrong :", e)


mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_ADDRESS, 1883)
mqtt_client.loop_forever()

