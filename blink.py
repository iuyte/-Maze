from gpiozero import LED
from time import sleep

def get():
	with open("data.txt", mode="r") as data:
		try:
			return int(data.read()[0])
		except:
			return 0

led = LED(27)
led.value = 0
set = 0

def loop():
	while True:
		led.value = get()		

loop()
