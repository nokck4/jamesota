import network
import time
import ujson
from machine import Pin
import dht
from simple import MQTTClient  # ตรวจสอบว่ามี simple.py สำหรับ MQTT

# ---------------- CONFIG ----------------
WIFI_SSID = "PW05"
WIFI_PASS = "0898037979"

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/dht22"
CLIENT_ID = "pico_w_dht"

SEND_INTERVAL = 60       # วินาที
MAX_FAIL_COUNT = 5
# ---------------------------------------

fail_count = 0
sensor = dht.DHT22(Pin(28, Pin.IN, Pin.PULL_UP))

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(WIFI_SSID, WIFI_PASS)

    print("Connecting WiFi...")
    for _ in range(30):   # 30*0.5=15 วิ
        if wlan.isconnected():
            print("WiFi Connected:", wlan.ifconfig())
            return wlan
        time.sleep(0.5)
    print("WiFi Connect Failed")
    return None

def disconnect_wifi(wlan):
    wlan.disconnect()
    wlan.active(False)
    print("WiFi disconnected")

def send_mqtt(temp, hum):
    try:
        client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
        client.connect()
        payload = ujson.dumps({"temp": temp, "humidity": hum})
        client.publish(MQTT_TOPIC, payload)
        print("MQTT Sent:", payload)
        client.disconnect()
        return True
    except Exception as e:
        print("MQTT ERROR:", e)
        return False

# =========================
#          MAIN LOOP
# =========================
while True:
    print("\n===== NEW CYCLE ======")

    wlan = connect_wifi()

    if wlan:
        try:
            time.sleep(1)       # DHT22 ต้องรอ
            sensor.measure()
            temp = round(sensor.temperature(), 1)
            hum = round(sensor.humidity(), 1)
            print("Sensor Read: Temp =", temp, "Hum =", hum)

            ok = send_mqtt(temp, hum)
            if not ok:
                fail_count += 1
            else:
                fail_count = 0

        except Exception as e:
            print("Sensor ERROR:", e)
            fail_count += 1

        disconnect_wifi(wlan)
    else:
        fail_count += 1

    # รีบูตถ้า fail หลายรอบ
    if fail_count >= MAX_FAIL_COUNT:
        print("Too many errors! Rebooting...")
        time.sleep(2)
        import machine
        machine.reset()

    # รอแบบไม่ block นานเกินไป
    for _ in range(SEND_INTERVAL):
        time.sleep(1)
