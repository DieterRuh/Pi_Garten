import webiopi
import datetime
#from sunrise import sun
 
GPIO = webiopi.GPIO
 
# GPIO pin using BCM numbering
OUT1 = 18           # Weglicht
OUT2 = 23           # Gartenlicht
OUT3 = 24           # Hoflicht
OUT4 = 25           # Brunnen

off_time_early = datetime.time( hour=22, minute=15, second=0)                   # Sonntag bis Donnerstag OFF at 22:15
off_time_late = datetime.time( hour=23, minute=15, second=0)                    # Freitag und Samstag OFF at 23:15
TIME_ON = datetime.time( hour=20, minute=30, second=0)                          # Einschaltzeit
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
    s = sun(lat=48.22,long=7.53)		# Friesenheim
    TIME_ON = s.sunset()
    TIME_ON = now + datetime.timedelta( minutes = 5 )
 
 
# loop function is repeatedly called by WebIOPi
def loop():
    global TIME_ON, TIME_OFF, off_time_early, off_time_late, tomorrow_is_holiday 
    # retrieve current datetime
    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta( days = 1 )

    # Um Mitternacht pruefen, ob naechster Tag ein Feiertag ist
#    if ( now.hour == 0 and now.minute == 0 and now.second == 0 ):
#        tomorrow_is_holiday = IstFeiertag( tomorrow )
#        s = sun(lat=48.22,long=7.53)		# Friesenheim
#        TIME_ON = s.sunset()
    
#    print( TIME_ON.strftime("%H:%M") )

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

# --------------------------------------------------------------------------------------------------------------

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
    # Ist Ostersonntag groe�er als 31, faellt Ostern in den April.
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

# --------------------------------------------------------------------------------------------------------------
from math import cos,sin,acos,asin,tan  
from math import degrees as deg, radians as rad  
#from datetime import date,datetime,time  
  
class sun:  
 """  
 Calculate sunrise and sunset based on equations from NOAA 
 http://www.srrb.noaa.gov/highlights/sunrise/calcdetails.html 
 
 typical use, calculating the sunrise at the present day: 
  
 import datetime 
 import sunrise 
 s = sun(lat=48.22,long=7.53) 
 print('sunrise at ',s.sunrise(), '   sunset at ', s.sunset()) 
 """  
 def __init__(self,lat=48.22,long=7.53): # Friesenheim 
  self.lat=lat  
  self.long=long  
    
 def sunrise(self,when=None):  
  """ 
  return the time of sunrise as a datetime.time object 
  when is a datetime.datetime object. If none is given 
  a local time zone is assumed (including daylight saving 
  if present) 
  """  
  if when is None : when = datetime.now(tz=LocalTimezone())  
  self.__preptime(when)  
  self.__calc()  
  return sun.__timefromdecimalday(self.sunrise_t)  
    
 def sunset(self,when=None):  
  if when is None : when = datetime.datetime.now(tz=LocalTimezone())  
  self.__preptime(when)  
  self.__calc()  
  return sun.__timefromdecimalday(self.sunset_t)  
    
 def solarnoon(self,when=None):  
  if when is None : when = datetime.now(tz=LocalTimezone())  
  self.__preptime(when)  
  self.__calc()  
  return sun.__timefromdecimalday(self.solarnoon_t)  
   
 @staticmethod  
 def __timefromdecimalday(day):  
  """ 
  returns a datetime.time object. 
   
  day is a decimal day between 0.0 and 1.0, e.g. noon = 0.5 
  """  
  hours  = 24.0*day  
  h      = int(hours)  
  minutes= (hours-h)*60  
  m      = int(minutes)  
  seconds= (minutes-m)*60  
  s      = int(seconds)  
  return datetime.time(hour=h,minute=m,second=s)  
  
 def __preptime(self,when):  
  """ 
  Extract information in a suitable format from when,  
  a datetime.datetime object. 
  """  
  # datetime days are numbered in the Gregorian calendar  
  # while the calculations from NOAA are distibuted as  
  # OpenOffice spreadsheets with days numbered from  
  # 1/1/1900. The difference are those numbers taken for   
  # 18/12/2010  
  self.day = when.toordinal()-(734124-40529)  
  t=when.time()  
  self.time= (t.hour + t.minute/60.0 + t.second/3600.0)/24.0  
    
  self.timezone=0  
  offset=when.utcoffset()  
  if not offset is None:  
   self.timezone=offset.seconds/3600.0  
    
 def __calc(self):  
  """ 
  Perform the actual calculations for sunrise, sunset and 
  a number of related quantities. 
   
  The results are stored in the instance variables 
  sunrise_t, sunset_t and solarnoon_t 
  """  
  timezone = self.timezone # in hours, east is positive  
  longitude= self.long     # in decimal degrees, east is positive  
  latitude = self.lat      # in decimal degrees, north is positive  
  
  time  = self.time # percentage past midnight, i.e. noon  is 0.5  
  day      = self.day     # daynumber 1=1/1/1900  
   
  Jday     =day+2415018.5+time-timezone/24 # Julian day  
  Jcent    =(Jday-2451545)/36525    # Julian century  
  
  Manom    = 357.52911+Jcent*(35999.05029-0.0001537*Jcent)  
  Mlong    = 280.46646+Jcent*(36000.76983+Jcent*0.0003032)%360  
  Eccent   = 0.016708634-Jcent*(0.000042037+0.0001537*Jcent)  
  Mobliq   = 23+(26+((21.448-Jcent*(46.815+Jcent*(0.00059-Jcent*0.001813))))/60)/60  
  obliq    = Mobliq+0.00256*cos(rad(125.04-1934.136*Jcent))  
  vary     = tan(rad(obliq/2))*tan(rad(obliq/2))  
  Seqcent  = sin(rad(Manom))*(1.914602-Jcent*(0.004817+0.000014*Jcent))+sin(rad(2*Manom))*(0.019993-0.000101*Jcent)+sin(rad(3*Manom))*0.000289  
  Struelong= Mlong+Seqcent  
  Sapplong = Struelong-0.00569-0.00478*sin(rad(125.04-1934.136*Jcent))  
  declination = deg(asin(sin(rad(obliq))*sin(rad(Sapplong))))  
    
  eqtime   = 4*deg(vary*sin(2*rad(Mlong))-2*Eccent*sin(rad(Manom))+4*Eccent*vary*sin(rad(Manom))*cos(2*rad(Mlong))-0.5*vary*vary*sin(4*rad(Mlong))-1.25*Eccent*Eccent*sin(2*rad(Manom)))  
  
  hourangle= deg(acos(cos(rad(90.833))/(cos(rad(latitude))*cos(rad(declination)))-tan(rad(latitude))*tan(rad(declination))))  
  
  self.solarnoon_t=(720-4*longitude-eqtime+timezone*60)/1440  
  self.sunrise_t  =self.solarnoon_t-hourangle*4/1440  
  self.sunset_t   =self.solarnoon_t+hourangle*4/1440  


# --------------------------------------------------------------------------------------------------------------

 
ZERO = datetime.timedelta(0)
HOUR = datetime.timedelta(hours=1)
SECOND = datetime.timedelta(seconds=1)

# A class capturing the platform's idea of local time.
# (May result in wrong values on historical times in
#  timezones where UTC offset and/or the DST rules had
#  changed in the past.)
import time as _time

STDOFFSET = datetime.timedelta(seconds = -_time.timezone)
if _time.daylight:
    DSTOFFSET = datetime.timedelta(seconds = -_time.altzone)
else:
    DSTOFFSET = STDOFFSET

DSTDIFF = DSTOFFSET - STDOFFSET

class LocalTimezone(datetime.tzinfo):

    def fromutc(self, dt):
        assert dt.tzinfo is self
        stamp = (dt - datetime.datetime(1970, 1, 1, tzinfo=self)) // SECOND
        args = _time.localtime(stamp)[:6]
        dst_diff = DSTDIFF // SECOND
        # Detect fold
        fold = (args == _time.localtime(stamp - dst_diff))
# PR�FEN!!!		
#        return datetime.datetime(*args, microsecond=dt.microsecond, tzinfo=self, fold=fold)
        return datetime.datetime(*args, microsecond=dt.microsecond, tzinfo=self)

    def utcoffset(self, dt):
        if self._isdst(dt):
            return DSTOFFSET
        else:
            return STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return DSTDIFF
        else:
            return ZERO

    def tzname(self, dt):
        return _time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, 0)
        stamp = _time.mktime(tt)
        tt = _time.localtime(stamp)
        return tt.tm_isdst > 0

