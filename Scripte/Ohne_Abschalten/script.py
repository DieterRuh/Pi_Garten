import webiopi
import datetime
 
GPIO = webiopi.GPIO
 
OUT1 = 18 # GPIO pin using BCM numbering
OUT2 = 23 
OUT3 = 24 
OUT4 = 25 
 
HOUR_OFF = 22 # Turn OUT1 OFF at 22:15
MIN_OFF = 15
 
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
 
    # toggle OUT1 ON all days at the correct time
    if ((now.hour == HOUR_OFF) and (now.minute == MIN_OFF) and (now.second == 0)):
        GPIO.digitalWrite(OUT1, GPIO.HIGH)
        GPIO.digitalWrite(OUT2, GPIO.HIGH)
        GPIO.digitalWrite(OUT3, GPIO.HIGH)
        GPIO.digitalWrite(OUT4, GPIO.HIGH)
 
    # gives CPU some time before looping again
    webiopi.sleep(1)
 
# destroy function is called at WebIOPi shutdown
def destroy():
    GPIO.digitalWrite(OUT1, GPIO.LOW)
    GPIO.digitalWrite(OUT2, GPIO.LOW)
    GPIO.digitalWrite(OUT3, GPIO.LOW)
    GPIO.digitalWrite(OUT4, GPIO.LOW)
 
