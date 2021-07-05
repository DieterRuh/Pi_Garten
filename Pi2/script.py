import webiopi
import datetime
 
GPIO = webiopi.GPIO
 
OUT1 = 19 # GPIO pin using BCM numbering
OUT2 = 35 
OUT3 = 24 
OUT4 = 25 
 
HOUR_OFF_EARLY = 19 # Sonntag bis Donnerstag OFF at 22:15
MIN_OFF_EARLY = 38

HOUR_OFF_LATE = 23 # Freitag und Sammstag OFF at 23:00
MIN_OFF_LATE = 00
 
# setup function is automatically called at WebIOPi startup
def setup():
    # set the GPIO used by the OUT1 to output
    GPIO.setFunction(OUT1, GPIO.OUT)
    GPIO.setFunction(OUT2, GPIO.OUT)
    GPIO.setFunction(OUT3, GPIO.OUT)
    GPIO.setFunction(OUT4, GPIO.OUT)
 
    # retrieve current datetime
    now = datetime.datetime.now()
 
# loop function is repeatedly called by WebIOPi
def loop():
    # retrieve current datetime
    now = datetime.datetime.now()
	
    # retrieve day of week 0 = Monday
    weekday = datetime.date.today().weekday()

    hour_off = 0
    min_off = 0
	
	# test for the day of week	
    if ( ( weekday < 4) or (weekday == 7 )):
        hour_off = HOUR_OFF_EARLY
        min_off = MIN_OFF_EARLY
    else:
        hour_off = HOUR_OFF_LATE
        min_off = MIN_OFF_LATE
 
    # toggle OUT1 ON all days at the correct time
    if ((now.hour == hour_off) and (now.minute == min_off) and (now.second == 0)):
        GPIO.digitalWrite(OUT1, GPIO.HIGH)
        GPIO.digitalWrite(OUT2, GPIO.HIGH)
        GPIO.digitalWrite(OUT3, GPIO.HIGH)
        GPIO.digitalWrite(OUT4, GPIO.HIGH)
 
    # gives CPU some time before looping again
    webiopi.sleep(1)
#    print(datetime.datetime.now.second)
 
# destroy function is called at WebIOPi shutdown
def destroy():
    GPIO.digitalWrite(OUT1, GPIO.LOW)
    GPIO.digitalWrite(OUT2, GPIO.LOW)
    GPIO.digitalWrite(OUT3, GPIO.LOW)
    GPIO.digitalWrite(OUT4, GPIO.LOW)
 
