import time
import logging
import paho.mqtt.client as mqtt
from pirc522 import RFID
import RPi.GPIO as GPIO

# === CONFIG ===
MQTT_BROKER = "mqtt-dashboard.com"  # The MQTT Broker; free Internet version
MQTT_PORT = 8884
MQTT_TOPIC = "rfid/scan"

RST_PIN = 25  # Reset-Pin RC522

# === Setup ===
rdr = RFID(pin_rst=RST_PIN)
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0: # rc=return code
        logging.info("Connectet with MQTT broker")
    else:
        logging.info(f"Error while connecting: {rc}")

# === Connect to MQTT ===
mqtt_client.on_connect = on_connect
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

mqtt_client.publish(MQTT_TOPIC, "Test") # Message to test the connection and seeing if the message gets pushed to the broker.
logging.info("Reading RFID tags now")

try:
    while True: # waitting for rfid chip
        rdr.wait_for_tag()
        (error, data) = rdr.request() # the data gets read
        if not error:
            logging.info("Tag found")
            (error, uid) = rdr.anticoll()
            if not error:
                uid_str = "-".join(map(str, uid))
                logging.info(f"ID of Tag {uid_str}")
                mqtt_client.publish(MQTT_TOPIC, uid_str)
                time.sleep(2)  # After to seconds ready for new tag

except Exception as e:
    logging.error(f"An Error occured: {e}")

finally:
    rdr.cleanup()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    GPIO.cleanup()
