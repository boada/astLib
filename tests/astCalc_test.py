#!/usr/bin/env python
""" Unit test for astCalc.py """

import unittest
try:
    from astLib import astCalc
except ImportError:
    print 'Failed to import astCalc. Properly installed?'

class KnownValues(unittest.TestCase):
    dl = ((0, 0.0),
        (1, 6612.2319979526665),
        (2, 15550.344054914269),
        (3, 25440.341543071634),
        (4, 35876.65177919497),
        (5, 46684.519634690674),
        (6, 57768.4047652542),
        (7, 69068.60070419929),
        (8, 80544.56794980433),
        (9, 92167.18110251875))

    da = ((1, 1653.0579994881666),
        (2, 1727.8160061015853),
        (3, 1590.0213464419771),
        (4, 1435.0660711677988),
        (5, 1296.792212074741),
        (6, 1178.947036025596),
        (7, 1079.1968860031138),
        (8, 994.3773820963498),
        (9, 921.6718110251875))

    dm = ((0, 0.0),
        (1, 3306.1159989763332),
        (2, 5183.448018304756),
        (3, 6360.0853857679085),
        (4, 7175.3303558389935),
        (5, 7780.753272448446),
        (6, 8252.629252179171),
        (7, 8633.57508802491),
        (8, 8949.396438867148),
        (9, 9216.718110251875))

    dc = ((0, 0.0),
        (1, 3306.1159989763332),
        (2, 5183.448018304756),
        (3, 6360.0853857679085),
        (4, 7175.3303558389935),
        (5, 7780.753272448446),
        (6, 8252.629252179171),
        (7, 8633.57508802491),
        (8, 8949.396438867148),
        (9, 9216.718110251875))

    dVcdz = ((0, 0.0),
        (1, 26600280192.66566),
        (2, 38802056165.96738),
        (3, 38841188497.89972),
        (4, 35676544335.38647),
        (5, 32032593827.202312),
        (6, 28649280632.351032),
        (7, 25688996003.091682),
        (8, 23145042336.61615),
        (9, 20965966219.94618))

    dl2z = ((0, 1.9073486328125e-05),
        (1, 0.0002288818359375),
        (2, 0.000457763671875),
        (3, 0.0006866455078125),
        (4, 0.00091552734375),
        (5, 0.0011444091796875),
        (6, 0.00141143798828125),
        (7, 0.00164031982421875),
        (8, 0.00186920166015625),
        (9, 0.00209808349609375))

    dc2z = ((0, 1.9073486328125e-05),
        (1, 0.0002288818359375),
        (2, 0.000457763671875),
        (3, 0.0006866455078125),
        (4, 0.00091552734375),
        (5, 0.0011444091796875),
        (6, 0.00141143798828125),
        (7, 0.00164031982421875),
        (8, 0.00186920166015625),
        (9, 0.00209808349609375))

    t0 = 13.42416860510653

    tl = ((0, 0.0),
        (1, 7.690807770237435),
        (2, 10.20779990292559),
        (3, 11.318357734246861),
        (4, 11.912986798684514),
        (5, 12.273081995586207),
        (6, 12.510106985762318),
        (7, 12.675741669812332),
        (8, 12.79680613047769),
        (9, 12.888439847755699))

    tz = ((0, 13.42416860510653),
        (1, 5.733360834869095),
        (2, 3.21636870218094),
        (3, 2.105810870859669),
        (4, 1.511181806422016),
        (5, 1.1510866095203234),
        (6, 0.9140616193442117),
        (7, 0.7484269352941979),
        (8, 0.6273624746288409),
        (9, 0.5357287573508316))

    tl2z = ((0, 3.814697265625e-05),
        (1, 0.075836181640625),
        (2, 0.160675048828125),
        (3, 0.2569580078125),
        (4, 0.367431640625),
        (5, 0.49652099609375),
        (6, 0.650634765625),
        (7, 0.84014892578125),
        (8, 1.08154296875),
        (9, 1.4056396484375))

    tz2z = ((1, 5.595703125),
        (2, 3.14208984375),
        (3, 2.14599609375),
        (4, 1.58081054688),
        (5, 1.20666503906),
        (6, 0.93505859375),
        (7, 0.726013183594),
        (8, 0.558471679688),
        (9, 0.419616699219))

    absMag = ()

    Ez = ((0, 1.00004119915),
        (2, 2.9676041515),
        (4, 6.18477970505),
        (6, 10.1881226141),
        (8, 14.8303953555),
        (10, 20.0301377529),
        (12, 25.732342031),
        (14, 31.8962615364),
        (16, 38.4900263757),
        (18, 45.4877835292))

    Ez2 = ((0, 1.0000824),
        (2, 8.8066744),
        (4, 38.2515),
        (6, 103.7978424),
        (8, 219.9406264),
        (10, 401.2064184),
        (12, 662.1534264),
        (14, 1017.3715),
        (16, 1481.4821304),
        (18, 2069.1384504))

    OmegaMz = ((0, 0.299975282037),
        (2, 0.919756951614),
        (4, 0.980353711619),
        (6, 0.991350086098),
        (8, 0.99435926677),
        (10, 0.99524828539),
        (12, 0.995388642151),
        (14, 0.995211680296),
        (16, 0.994882064222),
        (18, 0.994471877705))

    OmegaLz = ((0, 0.699942324752),
        (2, 0.079485168658),
        (4, 0.0182999359502),
        (6, 0.00674387813672),
        (8, 0.00318267712272),
        (10, 0.00174473779057),
        (12, 0.00105715680398),
        (14, 0.000688047581439),
        (16, 0.000472499793036),
        (18, 0.000338305056322))

    OmegaRz = ((0, 8.23932107994e-05),
        (2, 0.00075787972813),
        (4, 0.00134635243062),
        (6, 0.00190603576554),
        (8, 0.00245805610746),
        (10, 0.00300697681959),
        (12, 0.00355420104491),
        (14, 0.00410027212282),
        (16, 0.00464543598521),
        (18, 0.00518981723911))

    DeltaVz = ((0, 101.139502722),
        (2, 170.821830326),
        (4, 176.026830483),
        (6, 176.94066826),
        (8, 177.189098198),
        (10, 177.262358049),
        (12, 177.273918556),
        (14, 177.259342812),
        (16, 177.232186948),
        (18, 177.198381346))

    RVirialXRayCluster = ()

    def testdl(self):
        """ astLib.dl should give known result with known input """
        for z, result in self.dl:
            answer = astCalc.dl(z)
            self.assertAlmostEqual(result, answer)

    def testda(self):
        """ astLib.da should give known result with known input """
        for z, result in self.da:
            answer = astCalc.da(z)
            self.assertAlmostEqual(result, answer)

    def testdm(self):
        """ astlib.dm should give known result with known input """
        for z, result in self.dm:
            answer = astCalc.dm(z)
            self.assertAlmostEqual(result, answer)

    def testdc(self):
        """ astlib.dc should give known result with known input """
        for z, result in self.dc:
            answer = astCalc.dc(z)
            self.assertAlmostEqual(result, answer)

    def testdVcdz(self):
        """ astlib.dVcdz should give known result with known input """
        for z, result in self.dVcdz:
            answer = astCalc.dVcdz(z)
            self.assertAlmostEqual(result, answer)

    def testdl2z(self):
        """ astCalc.dl2z should give known result with known input """
        for distance, result in self.dl2z:
            answer = astCalc.dl2z(distance)
            self.assertAlmostEqual(result, answer)

    def testdc2z(self):
        """ astCalc.dc2z should give known result with known input """
        for distance, result in self.dc2z:
            answer = astCalc.dc2z(distance)
            self.assertAlmostEqual(result, answer)

    def testt0(self):
        """ astCalc.t0 should give known result with known input """
        answer = astCalc.t0()
        self.assertAlmostEqual(self.t0, answer)

    def testtl(self):
        """ astCalc.tl should give known result with known input """
        for z, result in self.tl:
            answer = astCalc.tl(z)
            self.assertAlmostEqual(result, answer)

    def testtz(self):
        """ astCalc.tz should give known result with known input """
        for z, result in self.tz:
            answer = astCalc.tz(z)
            self.assertAlmostEqual(result, answer)

    def testtl2z(self):
        """ astCalc.tl2z should give known result with known input """
        for time, result in self.tl2z:
            answer = astCalc.tl2z(time)
            self.assertAlmostEqual(result, answer)

    def testtz2z(self):
        """ tz2z should give known result with known input """
        for time, result in self.tz2z:
            answer = astCalc.tz2z(time)
            self.assertAlmostEqual(result, answer)

    #def testabsMag(self):
    #    """ astCalc.absMag should give known result with known input """
    #    for appMag, dist, result in self.absMag:
    #        answer = astCalc.absMag(appMag, dist)
    #        self.assertAlmostEqual(result, answer)

    def testEz(self):
        """ astCalc.Ez should give known result with known input """
        for z, result in self.Ez:
            answer = astCalc.Ez(z)
            self.assertAlmostEqual(result, answer)

    def testEz2(self):
        """ astCalc.Ez2 should give known result with known input """
        for z, result in self.Ez2:
            answer = astCalc.Ez2(z)
            self.assertAlmostEqual(result, answer)

    def testOmegaMz(self):
        """ astCalc.Omegaz should give known result with known input """
        for z, result in self.OmegaMz:
            answer = astCalc.OmegaMz(z)
            self.assertAlmostEqual(result, answer)

    def testOmegaLz(self):
        """ astCalc.OmegaLz should give known result with known input """
        for z, result in self.OmegaLz:
            answer = astCalc.OmegaLz(z)
            self.assertAlmostEqual(result, answer)

    def testOmegaRz(self):
        """ astCalc.OmegzRz should give known result with known input """
        for z, result in self.OmegaRz:
            answer = astCalc.OmegaRz(z)
            self.assertAlmostEqual(result, answer)

    def testDeltaVz(self):
        """ astCalc.DeltaVz should give known result with known input """
        for z, result in self.DeltaVz:
            answer = astCalc.DeltaVz(z)
            self.assertAlmostEqual(result, answer)

    #def testRVirialXRayCluster(self):
    #    """ astCalc.RVirialXRayCluster should give known result with known
    #        input """
    #    for kt, z, betaT, result in self.RVirialXRayCluster:
    #        answer = astCalc.RVirialXRayCluster(z)
    #        self.assertAlmostEqual(result, answer)

class badinput(unittest.TestCase):
    def testNegative(self):
        """ Functions should fail with negative input """
        self.assertRaises(ZeroDivisionError, astCalc.dl, -1)
        self.assertRaises(ZeroDivisionError, astCalc.da, -1)
        self.assertRaises(ZeroDivisionError, astCalc.dm, -1)
        self.assertRaises(ZeroDivisionError, astCalc.dc, -1)
        self.assertRaises(ZeroDivisionError, astCalc.dVcdz, -1)
        self.assertRaises(ZeroDivisionError, astCalc.tl, -1)
        self.assertRaises(ZeroDivisionError, astCalc.tz, -1)
        self.assertRaises(ValueError, astCalc.tl2z, -1)
        self.assertRaises(ValueError, astCalc.tz2z, -1)

    #def testTooOld(self):
    #    """ Functions should fail when time is older than Universe """
        #self.assertRaises(ValueError, astCalc.tl2z, 14)
        #self.assertRaises(ZeroDivisionError, astCalc.tz2z, 14)

class sanity(unittest.TestCase):
    def testsanity(self):
        """ Functions should work both backward and forward. To err <= 1E-5 """
        dl = astCalc.dl(1)
        z = astCalc.dl2z(dl)
        self.assertAlmostEqual(1, z, places=5)

        dc = astCalc.dc(1)
        z = astCalc.dc2z(dc)
        self.assertAlmostEqual(1, z, places=5)

        tl = astCalc.tl(1)
        z = astCalc.tl2z(tl)
        self.assertAlmostEqual(1, z, places=5)
        
        tz = astCalc.tz(1)
        z = astCalc.tz2z(tz)
        self.assertAlmostEqual(1, z, places=5)

if __name__ == '__main__':
    unittest.main()
