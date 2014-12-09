#!/usr/bin/env python
""" Unit test for astCoords.py """

import unittest
try:
    from astLib import astCoords
except ImportError:
    print 'Failed to import astCoords. Properly installed?'

class KnownValues(unittest.TestCase):
    hms2decimal = ()
    dms2decimal = ()
    decimal2hms = ()
    decimal2dms = ()
    calcAngSepDeg = ()
    shiftRADec = ()
    convertCoords = ()
    calcRADecSearchBox = ()

    def testhms2decimal(self):
        for hms, result in self.hms2decimal:
            answer = astCoords.hms2decimal(hms, ':')
            self.assertEqual(result, answer)

    def testdms2decimal(self):
        for dms, result in self.dms2decimal:
            answer = astCoords.dms2decimal(dms, ':')
            self.assertEqual(result, answer)

    def testdecimal2hms(self):
        for dec, result in self.decimal2hms:
            answer = astCoords.decimal2hms(dec, ':')
            self.assertEqual(result, answer)

    def testdecimal2dms(self):
        for dec, result in self.decimal2dms:
            answer = astCoords.decimal2dms(dec, ':')
            self.assertEqual(result, answer)

    def testcalcAngSepDeg(self):
        for ra1, dec1, ra2, dec2, result in self.calcAngSepDeg:
            answer = astCoords.calcAngSepDeg(ra1, dec1, ra2, dec2)
            self.assertEqual(result, answer)

    def testshiftRADec(self):
        for ra, dec, deltara, deltadec, result in self.shiftRADec:
            answer = astCoords.shiftRADec(ra, dec, deltara, deltadec)
            self.assertEqual(result, answer)

    def testconvertCoords(self):
        for insystem, outsystem, xcoor, ycoor, epoch, result in self.convertCoords:
            answer = astCoords.convertCoords(insystem, outsystem, xcoor, ycoor, epoch)
            self.assertEqual(result, answer)

    def testcalcRADECSearchBox(self):
        for ra, dec, radius, result in self.calcRADecSearchBox:
            answer = astCoords.calcRADecSearchBox(ra, dec, radius)
            self.assertEqual(result, answer)

class BadInput(unittest.TestCase):
    def testString(self):
        self.assertRaises()

    def testDecimal(self):
        pass

class Sanity(unittest.TestCase):

    def hms(self):
        hms_orig = '12:34:56.78'
        decimal = astCoords.hms2decimal(hms_orig, ':')
        hms_new = astCoords.decimal2hms(decimal, ':')
        self.assertEqual(hms_new, hms_orig)

    def dms(self):
        dms_orig = '12:34:56.78'
        decimal = astCoords.dms2decimal(dms_orig, ':')
        dms_new = astCoords.decimal2dms(decimal, ':')
        self.assertEqual(dms_new, dms_orig)
