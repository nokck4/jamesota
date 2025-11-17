from machine import Pin
from time import sleep

# กำหนดขา LED บนบอร์ด (Pico/Pico W ใช้ GPIO25)
led = Pin("LED", Pin.OUT)

while True:
    led.value(1)  # เปิด LED
    sleep(0.5)    # รอ 0.5 วินาที
    led.value(0)  # ปิด LED
    sleep(0.5)    # รอ 0.5 วินาที
    print("hello world")



