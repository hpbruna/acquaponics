import RPi.GPIO as GPIO #Import GPIO Library
import time
import datetime
from pprint import pprint #data naar het scherm loggen.

GPIO.setmode(GPIO.BOARD)
gpio_pump=1 #hier definieve pinnummers invoeren.
gpio_drain=2
tempPin = 3
niveauPin =4
flowPin = 5
phPin = 6

GPIO.setwarnings(False)
GPIO.setup(gpio_pump, GPIO.OUT)
GPIO.output(gpio_pump, True)
GPIO.setup(gpio_drain, GPIO.OUT)
GPIO.output(gpio_drain, True)
GPIO.setup(tempPin, GPIO.IN)
GPIO.setup(niveauPin, GPIO.IN)
GPIO.setup(flowPin, GPIO.IN)
GPIO.setup(phPin, GPIO.IN)

def pumpcycle():
	pump_time_input = 1 #aantal minuten pompen
	hold_time_input = 5 #aantal minuten in het bed
	drain_time_input = 1 #aantal minuten afpompen
	pause_time_input = 5 #minuten tot de volgende ronde
	cycle_count_input = 1 #Hoe vaak pompen en afpompen

	if cycle_count == 0:
		cycle_count=999

	for i in range(0,cycle_count): ## Aantal keren pompen/afpompen

		GPIO.output(gpio_pump, False) ## Pomp aan
		pprint('Pomp 1 AAN')
		time.sleep(pump_time*60) ## timer

		GPIO.output(gpio_pump, True) ## Pomp uit
		pprint('Pomp 1 UIT')
		time.sleep(hold_time*60) ## Wachten

		## Afpompen
		GPIO.output(gpio_drain, False) ## 2e pomp aan
		pprint('Pomp 2 AAN')
		time.sleep(drain_time*60) ## timer

		GPIO.output(gpio_drain, True) ## 2e pomp uit
		pprint('Pomp 2 UIT')
		time.sleep(pause_time*60) ## Wachten

	GPIO.cleanup()

def getTemp():
	temp = GPIO.input(tempPin)
	pprint('Temperatuur: ' + temp)
	return temp

def getLevel():
	niveau = GPIO.input(niveauPin)
	pprint('Niveau: ' + niveau)
	return niveau

def getFlow():
	flow = GPIO.input(flowPin)
	pprint('Flow: ' + flow)
	return flow

def getPh():
	ph = GPIO.input(phPin)
	pprint('PH: ' + ph)
	return ph


def main():
	while True:
		if getPh() < 6.5:
			pumpcycle()
		if getPh() > 7.5:
			pumpcycle()
		if getTemp() < 18:
			pumpcycle()
		if getTemp() > 25:
			pumpcycle()
		if getLevel() < 100:
			pumpcycle()
		if getLevel() > 110:
			pumpcycle()

		time.sleep(hold_time*60) ## Wachten tot een volgende meet en log ronde.

	print('Dit proces zou door moeten lopen en nu gaat dat fout')

# Proces laten lopen
main()

