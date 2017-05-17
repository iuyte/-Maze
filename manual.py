from time import sleep
import termios, tty, sys
def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(fd)
		ch = sys.stdin.read(1)
	finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def set(value):
	with open('data.txt', mode='w') as data:
		data.write(str(value))

def get():
	with open('data.txt', mode='r') as data:
		try:
			return int(data.read())
		except:
			return 0

def loop():
	while True:
		key = getch()
		if key == "q":
			print("|-----------------|\n|----Quitting!----|\n|-----------------|\n|_________________|")
			exit()
		if key == " ":
			if get() == 0:
				set(1)
				print("|-----------------|\n|----LED is ON----|\n|-----------------|")
			else:
				set(0)
				print("|-----------------|\n|---LED now OFF---|\n|-----------------|")

print("___________________\n|-----------------|\n|------Ready------|\n|-----------------|")
loop()
