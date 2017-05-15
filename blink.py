from gpiozero import LED
from time import sleep

led = LED(17)

def on():
    led.on()

def off():
    led.off()
