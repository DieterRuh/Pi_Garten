import datetime

def OsterSonntag( jahr ):
    "Berechnet den Ostersonntag für ein gegebenes Jahr"
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
    # Ausnahmen prüfen
    # Ist Ostersonntag größer als 31, fällt Ostern in den April.
    # Der Tag wird dann wie folgt berechnet: Ostersonntag =D+E-9.
    if (tag > 31):
        monat = 4
        tag = D + E - 9
    # weitere Ausnahmen prüfen
    elif (tag == 26):
        # Ist Ostersonntag der 26. April fällt Ostern
        # auf den 19. April
        tag = 19
    elif (tag == 25):
        # Ist Ostersonntag der 25. April und gleichzeitig
        # A > 10 und D = 28, dann ist Ostersonntag der 18. April
        if (A > 10 and B == 28):
            tag = 18
    else:
        monat = 3
    # Gültigkeitsprüfung durchführen
    # Prüfen, ob das Datum gültig ist.
    if (monat > 0 and tag > 0):
        date = datetime.datetime( jahr, monat, tag )
        # prüfen, ob das berechnete Datum ein Sonntag ist.
        if (date.weekday() != 6):
            raise Exception( 'Berechnungsfehler: Ostersonntag liegt nicht an einem Sonntag!' )
        return date.date()
    else:
        raise Exception( 'Berechnungsfehler!' )


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


def OsterMontag( jahr ):
    "Liefert das Datum für den OsterMonntag einen gegebenen Jahres"
    return OsterSonntag( jahr ) + datetime.timedelta( days = 1)

def KarFreitag( jahr ):
    return OsterSonntag( jahr ) + datetime.timedelta( days = -2)

def PfingstSonntag( jahr ):
    return OsterSonntag( jahr ) + datetime.timedelta( days = 49)

def PfingstMontag( jahr ):
    return OsterSonntag( jahr ) + datetime.timedelta( days = 50)

def Himmelfahrt( jahr ):
    return OsterSonntag( jahr ) + datetime.timedelta( days = 39)

def Fronleichnam( jahr ):
    return OsterSonntag( jahr ) + datetime.timedelta( days = 60)

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
    
