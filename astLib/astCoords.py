"""module for coordinate manipulation (conversions, calculations etc.)

(c) 2007-2012 Matt Hilton

(c) 2013-2014 Matt Hilton & Steven Boada

U{http://astlib.sourceforge.net}

"""

import numpy
from PyWCSTools import wcscon


#-----------------------------------------------------------------------------
def hms2decimal(RAString, delimiter):
    """Converts a delimited string of Hours:Minutes:Seconds format into decimal
    degrees.

    @type RAString: string
    @param RAString: coordinate string in H:M:S format
    @type delimiter: string
    @param delimiter: delimiter character in RAString
    @rtype: float
    @return: coordinate in decimal degrees

    """
    # is it in HH:MM:SS format?
    if delimiter == "":
        RABits = str(RAString).split()
    else:
        RABits = str(RAString).split(delimiter)
    if len(RABits) > 1:
        RAHDecimal = float(RABits[0])
        if len(RABits) > 1:
            RAHDecimal = RAHDecimal + (float(RABits[1]) / 60.0)
        if len(RABits) > 2:
            RAHDecimal = RAHDecimal + (float(RABits[2]) / 3600.0)
        RADeg = (RAHDecimal / 24.0) * 360.0
    else:
        RADeg = float(RAString)

    return RADeg


#-----------------------------------------------------------------------------
def dms2decimal(decString, delimiter):
    """Converts a delimited string of Degrees:Minutes:Seconds format into
    decimal degrees.

    @type decString: string
    @param decString: coordinate string in D:M:S format
    @type delimiter: string
    @param delimiter: delimiter character in decString
    @rtype: float
    @return: coordinate in decimal degrees

    """
    # is it in DD:MM:SS format?
    if delimiter == "":
        decBits = str(decString).split()
    else:
        decBits = str(decString).split(delimiter)
    if len(decBits) > 1:
        decDeg = float(decBits[0])
        if decBits[0].find("-") != -1:
            if len(decBits) > 1:
                decDeg = decDeg - (float(decBits[1]) / 60.0)
            if len(decBits) > 2:
                decDeg = decDeg - (float(decBits[2]) / 3600.0)
        else:
            if len(decBits) > 1:
                decDeg = decDeg + (float(decBits[1]) / 60.0)
            if len(decBits) > 2:
                decDeg = decDeg + (float(decBits[2]) / 3600.0)
    else:
        decDeg = float(decString)

    return decDeg


#-----------------------------------------------------------------------------
def decimal2hms(RADeg, delimiter):
    """Converts decimal degrees to string in Hours:Minutes:Seconds format with
    user specified delimiter.

    @type RADeg: float
    @param RADeg: coordinate in decimal degrees
    @type delimiter: string
    @param delimiter: delimiter character in returned string
    @rtype: string
    @return: coordinate string in H:M:S format

    """
    hours = (RADeg / 360.0) * 24
    #if hours < 10 and hours >= 1:
    if 1 <= hours < 10:
        sHours = "0" + str(hours)[0]
    elif hours >= 10:
        sHours = str(hours)[:2]
    elif hours < 1:
        sHours = "00"

    if str(hours).find(".") == -1:
        mins = float(hours) * 60.0
    else:
        mins = float(str(hours)[str(hours).index("."):]) * 60.0
    #if mins<10 and mins>=1:
    if 1 <= mins < 10:
        sMins = "0" + str(mins)[:1]
    elif mins >= 10:
        sMins = str(mins)[:2]
    elif mins < 1:
        sMins = "00"

    secs = (hours - (float(sHours) + float(sMins) / 60.0)) * 3600.0
    #if secs < 10 and secs>0.001:
    if 0.001 < secs < 10:
        sSecs = "0" + str(secs)[:str(secs).find(".") + 4]
    elif secs < 0.0001:
        sSecs = "00.001"
    else:
        sSecs = str(secs)[:str(secs).find(".") + 4]
    if len(sSecs) < 5:
        sSecs = sSecs + "00"  # So all to 3dp

    if float(sSecs) == 60.000:
        sSecs = "00.00"
        sMins = str(int(sMins) + 1)
    if int(sMins) == 60:
        sMins = "00"
        #sDeg = str(int(sDeg)+1)

    return sHours + delimiter + sMins + delimiter + sSecs


#------------------------------------------------------------------------------
def decimal2dms(decDeg, delimiter):
    """Converts decimal degrees to string in Degrees:Minutes:Seconds format
    with user specified delimiter.

    @type decDeg: float
    @param decDeg: coordinate in decimal degrees
    @type delimiter: string
    @param delimiter: delimiter character in returned string
    @rtype: string
    @return: coordinate string in D:M:S format

    """
    # Positive
    if decDeg > 0:
        #if decDeg < 10 and decDeg>=1:
        if 1 <= decDeg < 10:
            sDeg = "0" + str(decDeg)[0]
        elif decDeg >= 10:
            sDeg = str(decDeg)[:2]
        elif decDeg < 1:
            sDeg = "00"

        if str(decDeg).find(".") == -1:
            mins = float(decDeg) * 60.0
        else:
            mins = float(str(decDeg)[str(decDeg).index("."):]) * 60
        #if mins<10 and mins>=1:
        if 1 <= mins < 10:
            sMins = "0" + str(mins)[:1]
        elif mins >= 10:
            sMins = str(mins)[:2]
        elif mins < 1:
            sMins = "00"

        secs = (decDeg - (float(sDeg) + float(sMins) / 60.0)) * 3600.0
        #if secs<10 and secs>0:
        if 0 < secs < 10:
            sSecs = "0" + str(secs)[:str(secs).find(".") + 3]
        elif secs < 0.001:
            sSecs = "00.00"
        else:
            sSecs = str(secs)[:str(secs).find(".") + 3]
        if len(sSecs) < 5:
            sSecs = sSecs + "0"  # So all to 2dp

        if float(sSecs) == 60.00:
            sSecs = "00.00"
            sMins = str(int(sMins) + 1)
        if int(sMins) == 60:
            sMins = "00"
            sDeg = str(int(sDeg) + 1)

        return "+" + sDeg + delimiter + sMins + delimiter + sSecs

    else:
        #if decDeg>-10 and decDeg<=-1:
        if -10 < decDeg <= -1:
            sDeg = "-0" + str(decDeg)[1]
        elif decDeg <= -10:
            sDeg = str(decDeg)[:3]
        elif decDeg > -1:
            sDeg = "-00"

        if str(decDeg).find(".") == -1:
            mins = float(decDeg) * -60.0
        else:
            mins = float(str(decDeg)[str(decDeg).index("."):]) * 60
        #if mins<10 and mins>=1:
        if 1 <= mins < 10:
            sMins = "0" + str(mins)[:1]
        elif mins >= 10:
            sMins = str(mins)[:2]
        elif mins < 1:
            sMins = "00"

        secs = (decDeg - (float(sDeg) - float(sMins) / 60.0)) * 3600.0
        #if secs>-10 and secs<0:
        # so don't get minus sign
        if -10 < secs < 0:
            sSecs = "0" + str(secs)[1:str(secs).find(".") + 3]
        elif secs > -0.001:
            sSecs = "00.00"
        else:
            sSecs = str(secs)[1:str(secs).find(".") + 3]
        if len(sSecs) < 5:
            sSecs = sSecs + "0"  # So all to 2dp

        if float(sSecs) == 60.00:
            sSecs = "00.00"
            sMins = str(int(sMins) + 1)
        if int(sMins) == 60:
            sMins = "00"
            sDeg = str(int(sDeg) - 1)

        return sDeg + delimiter + sMins + delimiter + sSecs


#-----------------------------------------------------------------------------
def eq2cart(RA, DEC, r):
    """
    Convert Equatorial coordinates to Cartesian coordinates. Return a tuple
    (x, y, z) in the same unit of the input distance. This is the inverse of
    cart2eq.

    @type RA: float
    @param RA: Right Ascension in decimal degrees
    @type DEC: float
    @param DEC: Declination in decimal degrees
    @type r: float
    @param r: Distance to the object.
    @rtype: tuple
    @return: Tuple of (x, y, z) in same unit as the input distance.

    """

    RA = numpy.radians(RA)
    DEC = numpy.radians(DEC)

    x = r * numpy.cos(RA) * numpy.cos(DEC)
    y = r * numpy.sin(RA) * numpy.cos(DEC)
    z = r * numpy.sin(DEC)

    return x, y, z


#-----------------------------------------------------------------------------
def cart2eq(x, y, z):
    """
    Convert Cartesian coordinates to Equatorial coordinates. Returns a tuple of
    (RA, DEC, r), with RA and DEC given in decimal degrees and r in the same
    unit as the input.

    @type x: float
    @param x: x coordinate
    @type y: float
    @param y: x coordinate
    @type z: float
    @param z: x coordinate
    @rtype: tuple
    @return: Tuple of (RA, DEC, r)

    """

    r = numpy.sqrt(numpy.power(x, 2) + numpy.power(y, 2) + numpy.power(z, 2))
    ra = numpy.arctan2(y, x)
    try:
        ra[ra < 0] = 2.0 * numpy.pi + ra[ra < 0]
    except TypeError:
        ra = ra if ra >= 0 else (2.0 * numpy.pi + ra)
    dec = numpy.arcsin(z / r)

    ra = numpy.degrees(ra)
    dec = numpy.degrees(dec)

    return ra, dec, r


#-----------------------------------------------------------------------------
def calcAngSepDeg(RADeg1, decDeg1, RADeg2, decDeg2):
    """Calculates the angular separation of two positions on the sky (specified
    in decimal degrees) in decimal degrees, assuming a tangent plane projection
    (so separation has to be <90 deg). Note that RADeg2, decDeg2 can be numpy
    arrays.

    @type RADeg1: float
    @param RADeg1: R.A. in decimal degrees for position 1
    @type decDeg1: float
    @param decDeg1: dec. in decimal degrees for position 1
    @type RADeg2: float or numpy array
    @param RADeg2: R.A. in decimal degrees for position 2
    @type decDeg2: float or numpy array
    @param decDeg2: dec. in decimal degrees for position 2
    @rtype: float or numpy array, depending upon type of RADeg2, decDeg2
    @return: angular separation in decimal degrees

    """

    if not isinstance(RADeg1, float):
        RADeg1 = hms2decimal(RADeg1, ':')
    if not isinstance(decDeg1, float):
        decDeg1 = dms2decimal(decDeg1, ':')
    if not isinstance(RADeg2, float):
        RADeg2 = hms2decimal(RADeg2, ':')
    if not isinstance(decDeg2, float):
        decDeg2 = dms2decimal(decDeg2, ':')

    cRA = numpy.radians(RADeg1)
    cDec = numpy.radians(decDeg1)

    gRA = numpy.radians(RADeg2)
    gDec = numpy.radians(decDeg2)

    #dRA = cRA-gRA
    #dDec = gDec-cDec
    cosC = ((numpy.sin(gDec) * numpy.sin(cDec)) +
            (numpy.cos(gDec) * numpy.cos(cDec) * numpy.cos(gRA - cRA)))
    x = (numpy.cos(cDec) * numpy.sin(gRA - cRA)) / cosC
    y = (((numpy.cos(gDec) * numpy.sin(cDec)) -
          (numpy.sin(gDec) * numpy.cos(cDec) * numpy.cos(gRA - cRA))) / cosC)
    r = numpy.degrees(numpy.sqrt(x * x + y * y))

    return r


#-----------------------------------------------------------------------------
def shiftRADec(ra1, dec1, deltaRA, deltaDec):
    """Computes new right ascension and declination shifted from the original
    by some delta RA and delta DEC. Input position is decimal degrees. Shifts
    (deltaRA, deltaDec) are arcseconds, and output is decimal degrees. Based on
    an IDL routine of the same name.

    @param ra1: float
    @type ra1: R.A. in decimal degrees
    @param dec1: float
    @type dec1: dec. in decimal degrees
    @param deltaRA: float
    @type deltaRA: shift in R.A. in arcseconds
    @param deltaDec: float
    @type deltaDec: shift in dec. in arcseconds
    @rtype: float [newRA, newDec]
    @return: shifted R.A. and dec.

    """

    d2r = numpy.pi / 180.
    as2r = numpy.pi / 648000.

    # Convert everything to radians
    #rara1 = ra1*d2r
    dcrad1 = dec1 * d2r
    shiftRArad = deltaRA * as2r
    #shiftDCrad = deltaDec*as2r

    # Shift!
    #deldec2 = 0.0
    sindis = numpy.sin(shiftRArad / 2.0)
    sindelRA = sindis / numpy.cos(dcrad1)
    delra = 2.0 * numpy.arcsin(sindelRA) / d2r

    # Make changes
    ra2 = ra1 + delra
    dec2 = dec1 + deltaDec / 3600.0

    # Make sure 0 < RA < 360.
    if ra2 > 360:
        ra2 -= 360
    elif ra2 < 0:
        ra2 += 360

    return ra2, dec2


#-----------------------------------------------------------------------------
def convertCoords(inputSystem, outputSystem, coordX, coordY, epoch):
    """Converts specified coordinates (given in decimal degrees) between J2000,
    B1950, and Galactic.

    @type inputSystem: string
    @param inputSystem: system of the input coordinates (either "J2000",
        "B1950" or "GALACTIC")
    @type outputSystem: string
    @param outputSystem: system of the returned coordinates (either "J2000",
        "B1950" or "GALACTIC")
    @type coordX: float
    @param coordX: longitude coordinate in decimal degrees, e.g. R. A.
    @type coordY: float
    @param coordY: latitude coordinate in decimal degrees, e.g. dec.
    @type epoch: float
    @param epoch: epoch of the input coordinates
    @rtype: list
    @return: coordinates in decimal degrees in requested output system

    """

    if inputSystem == "J2000" or inputSystem == "B1950" or inputSystem == "GALACTIC":
        if outputSystem == "J2000" or outputSystem == "B1950" or \
                                    outputSystem == "GALACTIC":

            outCoords = wcscon.wcscon(
                wcscon.wcscsys(inputSystem), wcscon.wcscsys(outputSystem), 0,
                0, coordX, coordY, epoch)

            return outCoords

    raise Exception("inputSystem and outputSystem must be 'J2000', 'B1950'"
                    "or 'GALACTIC'")


#-----------------------------------------------------------------------------
def calcSkyArea(RA1, RA2, DEC1, DEC2, units=True):
    """ Calculates the area of the quadrangle on the sky given by the
    intersection of a right ascension lune and declination zone. By default,
    the area is returned in square degrees.

    @type RA1: float
    @param RA1: Right ascension in decimal degrees
    @type RA2: float
    @param RA2: Right ascension in decimal degrees
    @type DEC1: float
    @param DEC1: Declination in decimal degrees
    @type DEC2: float
    @param DEC2: Declination in decimal degrees
    @type units: bool
    @param units: True: Area is given in square degrees. False: Area is given
    as a fraction of the total sky.

    """

    # convert to radians
    RA1 = numpy.radians(RA1)
    RA2 = numpy.radians(RA2)
    DEC1 = numpy.radians(DEC1)
    DEC2 = numpy.radians(DEC2)

    if units:
        return abs(RA1 - RA2) * abs(numpy.sin(DEC1) - numpy.sin(DEC2)) *\
                (180 / numpy.pi)**2
    else:
        return abs(RA1 - RA2) * abs(numpy.sin(DEC1) - numpy.sin(DEC2))


#-----------------------------------------------------------------------------
def calcRADecSearchBox(RADeg, decDeg, radiusSkyDeg):
    """Calculates minimum and maximum RA, dec coords needed to define a box
    enclosing a circle of radius radiusSkyDeg around the given RADeg, decDeg
    coordinates. Useful for freeform queries of e.g. SDSS, UKIDSS etc.. Uses
    L{calcAngSepDeg}, so has the same limitations.

    @type RADeg: float
    @param RADeg: RA coordinate of centre of search region
    @type decDeg: float
    @param decDeg: dec coordinate of centre of search region
    @type radiusSkyDeg: float
    @param radiusSkyDeg: radius in degrees on the sky used to define search
        region
    @rtype: list
    @return: [RAMin, RAMax, decMin, decMax] - coordinates in decimal degrees
        defining search box

    """

    tolerance = 1e-5  # in degrees on sky
    targetHalfSizeSkyDeg = radiusSkyDeg
    funcCalls = ["calcAngSepDeg(RADeg, decDeg, guess, decDeg)",
                 "calcAngSepDeg(RADeg, decDeg, guess, decDeg)",
                 "calcAngSepDeg(RADeg, decDeg, RADeg, guess)",
                 "calcAngSepDeg(RADeg, decDeg, RADeg, guess)"]
    coords = [RADeg, RADeg, decDeg, decDeg]
    signs = [1.0, -1.0, 1.0, -1.0]
    results = []
    for f, c, sign in zip(funcCalls, coords, signs):
        # Initial guess range
        maxGuess = sign * targetHalfSizeSkyDeg * 10.0
        minGuess = sign * targetHalfSizeSkyDeg / 10.0
        guessStep = (maxGuess - minGuess) / 10.0
        guesses = numpy.arange(minGuess + c, maxGuess + c, guessStep)
        for i in range(50):
            minSizeDiff = 1e6
            bestGuess = None
            for guess in guesses:
                sizeDiff = abs(eval(f) - targetHalfSizeSkyDeg)
                if sizeDiff < minSizeDiff:
                    minSizeDiff = sizeDiff
                    bestGuess = guess
            if minSizeDiff < tolerance:
                break
            else:
                guessRange = abs((maxGuess - minGuess))
                maxGuess = bestGuess + guessRange / 4.0
                minGuess = bestGuess - guessRange / 4.0
                guessStep = (maxGuess - minGuess) / 10.0
                guesses = numpy.arange(minGuess, maxGuess, guessStep)
        results.append(bestGuess)

    RAMax = results[0]
    RAMin = results[1]
    decMax = results[2]
    decMin = results[3]

    return [RAMin, RAMax, decMin, decMax]


def aitoff(lon, lat):
    """
    Make Aitoff map projection.

    Take traditional longitude and latitude in radians and return a
    tuple (x, y).

    Notice that traditionally longitude is in [-pi:pi] from the meridian,
    and latitude is in [-pi/2:pi/2] from the equator. So, for example, if
    you would like to make a galactic map projection centered on the galactic
    center, before passing galactic longitude l to the function you should
    first do:
    l = l if l <= numpy.pi else l - 2 * numpy.pi

    Keyword arguments:
    lon -- Traditional longitude in radians, in range [-pi:pi]
    lat -- Traditional latitude in radians, in range [-pi/2:pi/2]
    """

    def sinc(x):
        # a quick unnormalized sinc function, with discontinuity removed
        if not x:
            return 0
        else:
            return numpy.sin(x) / x

    x = numpy.zeros_like(lon)
    y = numpy.zeros_like(lat)

    # check if the input values are in the range
    if lon > numpy.pi or lon < -numpy.pi or lat > numpy.pi / 2 or \
            lat < -numpy.pi / 2:
        print('Aitoff: Input longitude and latitude out of range.\n')
        print('           lon: [-pi,pi]; lat: [-pi/2,pi/2].\n')
        return None

    # take care of the sigularity at (0, 0), otherwise division by zero may
    # happen
    if lon == 0 and lat == 0:
        return 0.0, 0.0

    alpha = numpy.acos(numpy.cos(lat) * numpy.cos(lon / 2.0))

    # the sinc function used here is the unnormalized sinc function
    x = 2.0 * numpy.cos(lat) * numpy.sin(lon / 2.0) / sinc(alpha)

    y = numpy.sin(lat) / sinc(alpha)

    return x, y
