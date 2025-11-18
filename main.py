from machine import Pin
import dht
import time

sensor_pin = Pin(28, Pin.IN, Pin.PULL_UP)   # ใช้ขา GP28
sensor = dht.DHT22(sensor_pin)

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        print("Temperature: ", temp, "°C")
        print("Humidity: ", hum, "%")
        
    except Exception as e:
        print("Error:", e)

    time.sleep(2)   # อ่านทุก 2 วินาที


