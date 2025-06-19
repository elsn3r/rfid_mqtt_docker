import time
import paho.mqtt.client as mqtt
from pirc522 import RFID
import RPi.GPIO as GPIO

# === CONFIG ===
MQTT_BROKER = "mqtt-dashboard.com"  # Deine MQTT-Broker-IP
MQTT_PORT = 8884
MQTT_TOPIC = "rfid/scan"

RST_PIN = 25  # Reset-Pin des RC522

# === Setup ===
rdr = RFID(pin_rst=RST_PIN)
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Verbunden mit MQTT-Broker")
    else:
        print(f"❌ Fehler beim Verbinden: {rc}")

# === Connect to MQTT ===
mqtt_client.on_connect = on_connect
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

mqtt_client.publish(MQTT_TOPIC, "Test")
print("🔍 Bereit, RFID-Tags zu lesen. Drücke STRG+C zum Beenden.")

try:
    while True:
        rdr.wait_for_tag()
        (error, data) = rdr.request()
        if not error:
            print("💳 Tag erkannt")
            (error, uid) = rdr.anticoll()
            if not error:
                uid_str = "-".join(map(str, uid))
                print(f"📡 UID: {uid_str}")
                mqtt_client.publish(MQTT_TOPIC, uid_str)
                time.sleep(2)  # Debounce

except KeyboardInterrupt:
    print("\n🛑 Beende Script...")

finally:
    rdr.cleanup()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    GPIO.cleanup()
