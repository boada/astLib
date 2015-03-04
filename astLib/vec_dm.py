def vec_dm(z):
    """Calculates the transverse comoving distance (proper motion distance) in
    Mpc at redshift z.

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
    def yn(x, OMEGA_K, OMEGA_M0, OMEGA_L0):
        return (1.0/numpy.sqrt(OMEGA_M0*x + OMEGA_L0*numpy.power(x, 4) +
            OMEGA_K*numpy.power(x, 2)))

    def integral(yn, xMin, xMax, OMEGA_K, OMEGA_M0, OMEGA_L0):
        return integrate.quad(yn, xMin, xMax, args=(OMEGA_K, OMEGA_M0,
            OMEGA_L0))[0]

    #integralValue, integralError = integrate.quad(yn, xMin, xMax)
    vec_integral = numpy.vectorize(integral)
    integralValue = vec_integral(yn, xMin, xMax, OMEGA_K, OMEGA_M0, OMEGA_L0)

    if OMEGA_K > 0.0:
        DM = (C_LIGHT/H0 * numpy.power(abs(OMEGA_K), -0.5) *
            math.sinh(numpy.sqrt(abs(OMEGA_K)) * integralValue))
    elif OMEGA_K == 0.0:
        DM = C_LIGHT/H0 * integralValue
    elif OMEGA_K < 0.0:
        DM = (C_LIGHT/H0 * numpy.power(abs(OMEGA_K), -0.5) *
            math.sin(numpy.sqrt(abs(OMEGA_K)) * integralValue))

    return DM