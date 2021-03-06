"""module for performing common calculations

(c) 2007-2011 Matt Hilton

(c) 2013-2014 Matt Hilton & Steven Boada

U{http://astlib.sourceforge.net}

The focus in this module is at present on calculations of distances in a given
cosmology. The parameters for the cosmological model are set using the
variables OMEGA_M0, OMEGA_L0, OMEGA_R0, H0 in the module namespace (see below
for details).

@var OMEGA_M0: The matter density parameter at z=0.
@type OMEGA_M0: float

@var OMEGA_L0: The dark energy density (in the form of a cosmological
    constant) at z=0.
@type OMEGA_L0: float

@var OMEGA_R0: The radiation density at z=0 (note this is only used currently
    in calculation of L{Ez}).
@type OMEGA_R0: float

@var H0: The Hubble parameter (in km/s/Mpc) at z=0.
@type H0: float

@var C_LIGHT: The speed of light in km/s.
@type C_LIGHT: float

"""

OMEGA_M0 = 0.3
OMEGA_L0 = 0.7
OMEGA_R0 = 8.24E-5
H0 = 70.0

C_LIGHT = 3.0e5

try:
    import numpy
except:
    print("WARNING: astCalc failed to import numpy modules -",)
    print("please use non-vectorized functions.")
try:
    from scipy import integrate
except ImportError:
    print("WARNING: astCalc failed to import scipy modules - ",)
    print("some functions will not work")

#------------------------------------------------------------------------------
def dl(z):
    """Calculates the luminosity distance in Mpc at redshift z.

    @type z: float
    @param z: redshift
    @rtype: float
    @return: luminosity distance in Mpc

    """

    DM = dm(z)
    DL = (1.0+z)*DM

    return DL

#------------------------------------------------------------------------------
def da(z):
    """Calculates the angular diameter distance in Mpc at redshift z.

    @type z: float
    @param z: redshift
    @rtype: float
    @return: angular diameter distance in Mpc

    """
    DM = dm(z)
    DA = DM/(1.0+z)

    return DA

#------------------------------------------------------------------------------
#@numpy.vectorize
def dm(z):
    """Calculates the transverse comoving distance (proper motion distance) in
    Mpc at redshift z.

    @type z: float
    @param z: redshift
    @rtype: float
    @return: transverse comoving distance (proper motion distance) in Mpc

    """

    OMEGA_K = 1.0 - OMEGA_M0 - OMEGA_L0

    N = 1000

    # Integration limits
    xMax = numpy.ones(len(z))
    xMin = 1.0 / (1.0 + z)
    xStep = (xMax - xMin)/N

    # Running total of y as we integrate
    yTotal = numpy.zeros(len(z))

    # Simpson's rule integration
    for n in range(N):
        x = xMin + xStep * n

        # Function to be integrated
        yn = (1.0/numpy.sqrt(OMEGA_M0*x + OMEGA_L0*numpy.power(x, 4) +
            OMEGA_K*numpy.power(x, 2)))

        if n==0 or n== N:
            yTotal += yn
        else:
            oddness = n/2.0
            fractPart = numpy.modf(oddness)[0]
            if fractPart == 0.5: # odd
                yTotal += (4. * yn)
            else:
                yTotal += (2.* yn)

    integralValue = (xMax - xMin)/ (3*N) * yTotal
    #integralValue, integralError = integrate.quad(yn, xMin, xMax)

    if OMEGA_K > 0.0:
        DM = (C_LIGHT/H0 * numpy.power(abs(OMEGA_K), -0.5) *
            numpy.sinh(numpy.sqrt(abs(OMEGA_K)) * integralValue))
    elif OMEGA_K == 0.0:
        DM = C_LIGHT/H0 * integralValue
    elif OMEGA_K < 0.0:
        DM = (C_LIGHT/H0 * numpy.power(abs(OMEGA_K), -0.5) *
            numpy.sin(numpy.sqrt(abs(OMEGA_K)) * integralValue))

    return DM

#------------------------------------------------------------------------------
@numpy.vectorize
def dc(z):
    """Calculates the line of sight comoving distance in Mpc at redshift z.

    @type z: float
    @param z: redshift
    @rtype: float
    @return: transverse comoving distance (proper motion distance) in Mpc

    """

    OMEGA_K = 1.0 - OMEGA_M0 - OMEGA_L0

    # Integration limits
    xMax = 1.0
    xMin = 1.0 / (1.0 + z)

    # Function to be integrated
    yn = lambda x: (1.0/numpy.sqrt(OMEGA_M0*x + OMEGA_L0*numpy.power(x, 4) +
            OMEGA_K*numpy.power(x, 2)))

    integralValue, integralError = integrate.quad(yn, xMin, xMax)

    DC= C_LIGHT/H0*integralValue

    return DC

#------------------------------------------------------------------------------
def dVcdz(z):
    """Calculates the line of sight comoving volume element per steradian dV/dz
    at redshift z.

    @type z: float
    @param z: redshift
    @rtype: float
    @return: comoving volume element per steradian

    """

    dH = C_LIGHT/H0
    dVcdz=(dH*(numpy.power(da(z),2))*(numpy.power(1+z,2))/Ez(z))

    return dVcdz

#------------------------------------------------------------------------------
def dl2z(distanceMpc):
    """Calculates the redshift z corresponding to the luminosity distance given
    in Mpc.

    @type distanceMpc: float
    @param distanceMpc: distance in Mpc
    @rtype: float
    @return: redshift

    """

    dTarget = distanceMpc
    toleranceMpc = 0.1

    zMin = numpy.zeros(len(dTarget))
    zMax = 10* numpy.ones(len(dTarget))

    diff = dl(zMax) - dTarget
    while 1:
        x = diff < 0
        if not x.all():
            break
        zMax[x] += 5.
        diff[x] = dl(zMax[x]) - dTarget

    zTrial = zMin + (zMax - zMin)/2.

    dTrial = dl(zTrial)
    diff = dTrial - dTarget
    while 1:
        x = numpy.abs(diff) < toleranceMpc
        if x.all():
            break
        y = diff > 0
        zMax[y] -= (zMax[y] - zMin[y])/2.
        zMin[~y] += (zMax[~y] - zMin[~y])/2.

        zTrial[~x] = zMin[~x] + (zMax[~x] - zMin[~x])/2.
        dTrial = dl(zTrial)
        diff = dTrial - dTarget

    return zTrial

#------------------------------------------------------------------------------
def dc2z(distanceMpc):
    """Calculates the redshift z corresponding to the comoving distance given
    in Mpc.

    @type distanceMpc: float
    @param distanceMpc: distance in Mpc
    @rtype: float
    @return: redshift

    """

    dTarget = distanceMpc
    toleranceMpc = 0.1

    zMin = numpy.zeros(len(dTarget))
    zMax = 10* numpy.ones(len(dTarget))

    diff = dc(zMax) - dTarget
    while 1:
        x = diff < 0
        if not x.all():
            break
        zMax[x] += 5.
        diff[x] = dc(zMax[x]) - dTarget

    zTrial = zMin + (zMax - zMin)/2.

    dTrial = dc(zTrial)
    diff = dTrial - dTarget
    while 1:
        x = numpy.abs(diff) < toleranceMpc
        if x.all():
            break
        y = diff > 0
        zMax[y] -= (zMax[y] - zMin[y])/2.
        zMin[~y] += (zMax[~y] - zMin[~y])/2.

        zTrial[~x] = zMin[~x] + (zMax[~x] - zMin[~x])/2.
        dTrial = dc(zTrial)
        diff = dTrial - dTarget

    return zTrial

#------------------------------------------------------------------------------
def t0():
    """Calculates the age of the universe in Gyr at z=0 for the current set of
    cosmological parameters.

    @rtype: float
    @return: age of the universe in Gyr at z=0

    """

    OMEGA_K = 1.0 - OMEGA_M0 - OMEGA_L0

    # Integration limits
    xMax = 1.0
    xMin = 0

    # Function to be integrated
    yn = lambda x: (x/numpy.sqrt(OMEGA_M0*x + OMEGA_L0*numpy.power(x, 4) +
            OMEGA_K*numpy.power(x, 2)))

    integralValue, integralError = integrate.quad(yn, xMin, xMax)

    T0 = (1.0/H0*integralValue*3.08e19)/3.16e7/1e9

    return T0

#------------------------------------------------------------------------------
@numpy.vectorize
def tl(z):
    """ Calculates the lookback time in Gyr to redshift z for the current set
    of cosmological parameters.

    @type z: float
    @param z: redshift
    @rtype: float
    @return: lookback time in Gyr to redshift z

    """
    OMEGA_K = 1.0 - OMEGA_M0 - OMEGA_L0

    # Integration limits
    xMax = 1.0
    xMin = 1./(1.+z)

    # Function to be integrated
    yn = lambda x: (x/numpy.sqrt(OMEGA_M0*x + OMEGA_L0*numpy.power(x, 4) +
            OMEGA_K*numpy.power(x, 2)))

    integralValue, integralError = integrate.quad(yn, xMin, xMax)

    T0 = (1.0/H0*integralValue*3.08e19)/3.16e7/1e9

    return T0

#------------------------------------------------------------------------------
def tz(z):
    """Calculates the age of the universe at redshift z for the current set of
    cosmological parameters.

    @type z: float
    @param z: redshift
    @rtype: float
    @return: age of the universe in Gyr at redshift z

    """

    TZ = t0() - tl(z)

    return TZ

#------------------------------------------------------------------------------
def tl2z(tlGyr):
    """Calculates the redshift z corresponding to lookback time tlGyr given in
    Gyr.

    @type tlGyr: float
    @param tlGyr: lookback time in Gyr
    @rtype: float
    @return: redshift

    @note: Raises ValueError if tlGyr is not positive.

    """
    if tlGyr.any() < 0.:
        raise ValueError('Lookback time must be positive')

    tTarget = tlGyr

    toleranceGyr = 0.001

    zMin = numpy.zeros(len(tTarget))
    zMax = 10. * numpy.ones(len(tTarget))

    diff = tl(zMax) - tTarget
    while 1:
        x = diff < 0
        if not x.all():
            zMax[x]  += 5.0
            diff[x] = tl(zMax[x]) - tTarget

    zTrial = zMin + (zMax - zMin)/2.0

    tTrial = tl(zTrial)
    diff = tTrial - tTarget
    while 1:
        x = numpy.abs(diff) < toleranceGyr
        if x.all():
            break
        y = diff > 0
        zMax[y] -= (zMax[y] - zMin[y])/2.
        zMin[~y] += (zMax[~y] - zMin[~y])/2.

        zTrial[~x] = zMin[~x] + (zMax[~x] - zMin[~x])/2.
        tTrial = tl(zTrial)
        diff = tTrial - tTarget

    return zTrial

#------------------------------------------------------------------------------
def tz2z(tzGyr):
    """Calculates the redshift z corresponding to age of the universe tzGyr
    given in Gyr.

    @type tzGyr: float
    @param tzGyr: age of the universe in Gyr
    @rtype: float
    @return: redshift

    @note: Raises ValueError if Universe age not positive

    """
    if tzGyr.any() <= 0:
        raise ValueError('Universe age must be positive.')
    tl = t0() - tzGyr
    z = tl2z(tl)

    return z

#------------------------------------------------------------------------------
def absMag(appMag, distMpc):
    """Calculates the absolute magnitude of an object at given luminosity
    distance in Mpc.

    @type appMag: float
    @param appMag: apparent magnitude of object
    @type distMpc: float
    @param distMpc: distance to object in Mpc
    @rtype: float
    @return: absolute magnitude of object

    """
    absMag = appMag - (5.0*numpy.log10(distMpc*1.0e5))

    return absMag

#------------------------------------------------------------------------------
def Ez(z):
    """Calculates the value of E(z), which describes evolution of the Hubble
    parameter with redshift, at redshift z for the current set of cosmological
    parameters. See, e.g., Bryan & Norman 1998 (ApJ, 495, 80).

    @type z: float
    @param z: redshift
    @rtype: float
    @return: value of E(z) at redshift z

    """

    Ez = numpy.sqrt(Ez2(z))

    return Ez

#------------------------------------------------------------------------------
def Ez2(z):
    """Calculates the value of E(z)^2, which describes evolution of the Hubble
    parameter with redshift, at redshift z for the current set of cosmological
    parameters. See, e.g., Bryan & Norman 1998 (ApJ, 495, 80).

    @type z: float
    @param z: redshift
    @rtype: float
    @return: value of E(z)^2 at redshift z

    """
    # This form of E(z) is more reliable at high redshift. It is basically the
    # same for all redshifts below 10. But above that, the radiation term
    # begins to dominate. From Peebles 1993.

    Ez2 = (OMEGA_R0 * numpy.power(1.0+z, 4) +
        OMEGA_M0* numpy.power(1.0+z, 3) +
        (1.0- OMEGA_M0- OMEGA_L0) *
        numpy.power(1.0+z, 2) + OMEGA_L0)

    return Ez2

#------------------------------------------------------------------------------
def OmegaMz(z):
    """Calculates the matter density of the universe at redshift z. See, e.g.,
    Bryan & Norman 1998 (ApJ, 495, 80).

    @type z: float
    @param z: redshift
    @rtype: float
    @return: matter density of universe at redshift z

    """
    ez2 = Ez2(z)

    Omega_Mz = (OMEGA_M0*numpy.power(1.0+z, 3))/ez2

    return Omega_Mz

#------------------------------------------------------------------------------
def OmegaLz(z):
    """ Calculates the dark energy density of the universe at redshift z.

    @type z: float
    @param z: redshift
    @rtype: float
    @return: dark energy density of universe at redshift z

    """
    ez2 = Ez2(z)

    return OMEGA_L0/ez2

#------------------------------------------------------------------------------
def OmegaRz(z):
    """ Calculates the radiation density of the universe at redshift z.

    @type z: float
    @param z: redshift
    @rtype: float
    @return: radiation density of universe at redshift z

    """
    ez2 = Ez2(z)

    return OMEGA_R0*numpy.power(1+z, 4)/ez2

#------------------------------------------------------------------------------
def DeltaVz(z):
    """Calculates the density contrast of a virialised region S{Delta}V(z),
    assuming a S{Lambda}CDM-type flat cosmology. See, e.g., Bryan & Norman
    1998 (ApJ, 495, 80).

    @type z: float
    @param z: redshift
    @rtype: float
    @return: density contrast of a virialised region at redshift z

    @note: If OMEGA_M0+OMEGA_L0 is not equal to 1, this routine exits and
    prints an error
    message to the console.

    """

    OMEGA_K = 1.0 - OMEGA_M0 - OMEGA_L0

    if OMEGA_K == 0.0:
        Omega_Mz = OmegaMz(z)
        deltaVz = (18.0*numpy.power(numpy.pi, 2)+82.0*(Omega_Mz-1.0)-39.0 *
                numpy.power(Omega_Mz-1, 2))
        return deltaVz
    else:
        raise Exception("cosmology is NOT flat.")

#------------------------------------------------------------------------------
def RVirialXRayCluster(kT, z, betaT):
    """Calculates the virial radius (in Mpc) of a galaxy cluster at redshift z
    with X-ray temperature kT, assuming self-similar evolution and a flat
    cosmology. See Arnaud et al. 2002 (A&A, 389, 1) and Bryan & Norman 1998
    (ApJ, 495, 80). A flat S{Lambda}CDM-type flat cosmology is assumed.

    @type kT: float
    @param kT: cluster X-ray temperature in keV
    @type z: float
    @param z: redshift
    @type betaT: float
    @param betaT: the normalisation of the virial relation, for which Evrard et
    al. 1996 (ApJ,469, 494) find a value of 1.05
    @rtype: float
    @return: virial radius of cluster in Mpc

    @note: If OMEGA_M0+OMEGA_L0 is not equal to 1, this routine exits and
    prints an error message to the console.

    """

    OMEGA_K = 1.0 - OMEGA_M0 - OMEGA_L0

    if OMEGA_K == 0.0:
        Omega_Mz = OmegaMz(z)
        deltaVz = (18.0 * numpy.power(numpy.pi, 2) + 82.0 * (Omega_Mz-1.0)- 39.0 *
                numpy.power(Omega_Mz-1, 2))
        deltaz = (deltaVz*OMEGA_M0)/(18.0*numpy.power(numpy.pi, 2)*Omega_Mz)

        # The equation quoted in Arnaud, Aghanim & Neumann is for h50, so need
        # to scale it
        h50 = H0/50.0
        Rv = (3.80*numpy.sqrt(betaT)*numpy.power(deltaz, -0.5) *
            numpy.power(1.0+z, (-3.0/2.0)) * numpy.sqrt(kT/10.0)*(1.0/h50))

        return Rv

    else:
        raise Exception("cosmology is NOT flat.")

#------------------------------------------------------------------------------

