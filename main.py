import network
import urequests
import ujson
import time
from machine import Pin
import dht

# ---------------------------------------------------------
# 1. WiFi Config
# ---------------------------------------------------------
WIFI_SSID = "PW05"
WIFI_PASS = "0898037979"

# ---------------------------------------------------------
# 2. LINE API Token + User ID
# ---------------------------------------------------------
CHANNEL_ACCESS_TOKEN = "DMaZnxE+XP69XjNTJ3W2QBRPBGS6txmoi53zLyIykciLYaH6AY5qLut19ykvfkfkLXiB1V/BWJuDDUxj6YB69Q+IlJJewpICwA48f52rsDbsLorgtfL435ARmws5IgqoVbYSIGO4Q26+cY7SQlRrCwdB04t89/1O/w1cDnyilFU="
TO_USER_ID = "U9c67d37c74f4058a9f517922971ec2e8"

# ---------------------------------------------------------
# 3. Connect WiFi
# ---------------------------------------------------------
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)

    print("Connecting WiFi...", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\nConnected:", wlan.ifconfig())

# ---------------------------------------------------------
# 4. Function ส่งข้อความ LINE
# ---------------------------------------------------------
def send_line_message(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + CHANNEL_ACCESS_TOKEN
    }
    data = {
        "to": TO_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    try:
        payload = ujson.dumps(data)
        print("JSON Payload:", payload)   # Debug ดู payload ก่อนส่ง
        response = urequests.post(url, headers=headers, data=payload)
        print("LINE Response:", response.text)
        response.close()
    except Exception as e:
        print("Send LINE Error:", e)
# ---------------------------------------------------------
# 5. ตั้งค่าเซนเซอร์ DHT22
# ---------------------------------------------------------
sensor_pin = Pin(28, Pin.IN, Pin.PULL_UP)  # GP28
sensor = dht.DHT22(sensor_pin)

# ---------------------------------------------------------
# 6. Main Program Loop
# ---------------------------------------------------------
connect_wifi()

while True:
    try:
        sensor.measure()

        temp = round(sensor.temperature(), 1)
        hum = round(sensor.humidity(), 1)

        print("Temperature:", temp)
        print("Humidity:", hum)

        message = "Temp: {} C\nHumidity: {} %".format(temp, hum)
        send_line_message(message)

    except Exception as e:
        print("Sensor Error:", e)

    time.sleep(60)   # ส่งทุก 60 วินาที (ปรับได้)
