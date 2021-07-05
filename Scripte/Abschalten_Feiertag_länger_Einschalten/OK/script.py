import webiopi
import datetime
import sunrise
 
GPIO = webiopi.GPIO
 
OUT1 = 18 # GPIO pin using BCM numbering
OUT2 = 23 
OUT3 = 24 
OUT4 = 25 

off_time_early = datetime.time( hour=22, minute=15, second=0)                   # Sonntag bis Donnerstag OFF at 22:15
off_time_late = datetime.time( hour=23, minute=0, second=0)                     # Freitag und Samstag OFF at 23:00
TIME_ON = datetime.time( hour=20, minute=0, second=0)                           # Einschaltzeit
TIME_OFF = off_time_early
tomorrow_is_holiday = False

# setup function is automatically called at WebIOPi startup
def setup():
    global TIME_ON, tomorrow_is_holiday 
    # set the GPIO used by the OUT1 to output
    GPIO.setFunction(OUT1, GPIO.OUT)
    GPIO.setFunction(OUT2, GPIO.OUT)
    GPIO.setFunction(OUT3, GPIO.OUT)
    GPIO.setFunction(OUT4, GPIO.OUT)
    now = datetime.datetime.now()
    tomorrow_is_holiday = IstFeiertag( now + datetime.timedelta( days = 1) )
    s = sunrise.sun(lat=48.22,long=7.53)		# Friesenheim
    #TIME_ON = s.sunset()
    TIME_ON = datetime.time( hour=2, minute=25, second=0)
 
 
# loop function is repeatedly called by WebIOPi
def loop():
    global TIME_ON, TIME_OFF, off_time_early, off_time_late, tomorrow_is_holiday 
    # retrieve current datetime
    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta( days = 1 )

    # Um Mitternacht pruefen, ob naechster Tag eine Feiertag ist
    if ( now.hour == 0 and now.minute == 0 and now.second == 0 ):
        tomorrow_is_holiday = IstFeiertag( tomorrow )
        s = sunrise.sun(lat=48.22,long=7.53)		# Friesenheim
        TIME_ON = s.sunset()
    
    print( TIME_ON.strftime("%H:%M") )

    # retrieve day of week 0 = Monday
    weekday = now.weekday()

    TIME_OFF = off_time_early

    # test for the day of week
    if ( weekday == 4 or weekday == 5 or tomorrow_is_holiday):
        TIME_OFF = off_time_late
 
    # toggle OUT1 OFF all days at the correct time
    if ((now.hour == TIME_OFF.hour) and (now.minute == TIME_OFF.minute) and (now.second == 0)):
        GPIO.digitalWrite(OUT1, GPIO.HIGH)
        GPIO.digitalWrite(OUT2, GPIO.HIGH)
        GPIO.digitalWrite(OUT3, GPIO.HIGH)
        GPIO.digitalWrite(OUT4, GPIO.HIGH)

    # toggle OUT1 ON all days at the correct time
    if ((now.hour == TIME_ON.hour) and (now.minute == TIME_ON.minute) and (now.second == 0)):
        GPIO.digitalWrite(OUT2, GPIO.LOW)
        GPIO.digitalWrite(OUT3, GPIO.LOW)
        GPIO.digitalWrite(OUT4, GPIO.LOW)

    # gives CPU some time before looping again
    webiopi.sleep(1)
 
# destroy function is called at WebIOPi shutdown
def destroy():
    GPIO.digitalWrite(OUT1, GPIO.LOW)
    GPIO.digitalWrite(OUT2, GPIO.LOW)
    GPIO.digitalWrite(OUT3, GPIO.LOW)
    GPIO.digitalWrite(OUT4, GPIO.LOW)
 
@webiopi.macro
def getLightHours():
    return "%s;%s" % (TIME_ON.strftime("%H:%M"), TIME_OFF.strftime("%H:%M"))

#@webiopi.macro 
def OsterSonntag( jahr ):
    "Berechnet den Ostersonntag fuer ein gegebenes Jahr"
    tag = 0
    monat = 0
    A = 0
    B = 0
    C = 0
    E = 0
    D = 0
    # Berechnen von A, B und C
    A = jahr % 19
    B = jahr % 4
    C = jahr % 7
    # Ermitteln von M und N
    result = GetMundN( jahr )
    M = result[0]
    N = result[1]
    # Berechnung fortsetzen
    # Berechnen von D
    D = ((19 * A) + M) % 30
    E = ((2 * B) + (4 * C) + (6 * D) + N) % 7
    # Tag berechnen
    tag = 22 + D + E
    # Ausnahmen pruefen
    # Ist Ostersonntag groeßer als 31, faellt Ostern in den April.
    # Der Tag wird dann wie folgt berechnet: Ostersonntag =D+E-9.
    if (tag > 31):
        monat = 4
        tag = D + E - 9
    # weitere Ausnahmen pruefen
    elif (tag == 26):
        # Ist Ostersonntag der 26. April faellt Ostern
        # auf den 19. April
        tag = 19
    elif (tag == 25):
        # Ist Ostersonntag der 25. April und gleichzeitig
        # A > 10 und D = 28, dann ist Ostersonntag der 18. April
        if (A > 10 and B == 28):
            tag = 18
    else:
        monat = 3
    # Gueltigkeitspruefung durchfuehren
    # Pruefen, ob das Datum gueltig ist.
    if (monat > 0 and tag > 0):
        date = datetime.datetime( jahr, monat, tag )
        # pruefen, ob das berechnete Datum ein Sonntag ist.
        if (date.weekday() != 6):
            raise Exception( 'Berechnungsfehler: Ostersonntag liegt nicht an einem Sonntag!' )
        return date.date()
    else:
        raise Exception( 'Berechnungsfehler!' )

@webiopi.macro
def GetMundN( jahr ):
    "Berechnet M und N"
    M = 0
    N = 0
    if (jahr >= 1582 and jahr <= 1699):
        M = 22
        N = 2
    elif (jahr >= 1700 and jahr <= 1799):
        M = 23
        N = 3
    elif (jahr >= 1800 and jahr <= 1899):
        M = 23;
        N = 4
    elif (jahr >= 1900 and jahr <= 2099):
        M = 24
        N = 5
    elif (jahr >= 2100 and jahr <= 2199):
        M = 24
        N = 6
    elif (jahr >= 2200 and jahr <= 2299):
        M = 25
        N = 0
    elif (jahr >= 2300 and jahr <= 2399):
        M = 26
        N = 1
    elif (jahr >= 2400 and jahr <= 2499):
        M = 25
        N = 1
    else:
        raise Exception( 'Die Jahreszahl muss zwischen 1581 und 2500 liegen!' )
    return M, N

@webiopi.macro
def OsterMontag( jahr ):
    "Liefert das Datum fuer den OsterMonntag einen gegebenen Jahres"
    return OsterSonntag( jahr ) + datetime.timedelta( days = 1)

@webiopi.macro
def KarFreitag( jahr ):
    return OsterSonntag( jahr ) + datetime.timedelta( days = -2)

@webiopi.macro
def PfingstSonntag( jahr ):
    return OsterSonntag( jahr ) + datetime.timedelta( days = 49)

@webiopi.macro
def PfingstMontag( jahr ):
    return OsterSonntag( jahr ) + datetime.timedelta( days = 50)

@webiopi.macro
def Himmelfahrt( jahr ):
    return OsterSonntag( jahr ) + datetime.timedelta( days = 39)

@webiopi.macro
def Fronleichnam( jahr ):
    return OsterSonntag( jahr ) + datetime.timedelta( days = 60)

@webiopi.macro
def IstFeiertag( date ):
    jahr = date.year
    return (date.date == KarFreitag( jahr )
    or date.date() == OsterSonntag( jahr )
    or date.date() == OsterMontag( jahr )
    or date.date() == PfingstSonntag( jahr )
    or date.date() == PfingstMontag( jahr )
    or date.date() == Himmelfahrt( jahr )
    or date.date() == Fronleichnam( jahr )
    or date.date() == datetime.datetime( jahr, 1, 1 ).date()
    or date.date() == datetime.datetime( jahr, 5, 1 ).date()
    or date.date() == datetime.datetime( jahr, 10, 3 ).date()
    or date.date() == datetime.datetime( jahr, 11, 1 ).date()
    or date.date() == datetime.datetime( jahr, 12, 25 ).date()
    or date.date() == datetime.datetime( jahr, 12, 26 ).date())
 
