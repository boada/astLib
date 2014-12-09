import unittest
try:
        from astLib import astStats
except:
    print 'Failed to import astCalc. Properly installed?'

class KnownValues(unittest.TestCase):
# Generate the testing data
    datalist = [i for i in range(100)]
    datalist_short = [i for i in range(10)]
    datalist_weighted = [(i,0.5) for i in range(100)]
    
# These are the tests
    mean = ((datalist, 49.5),)
    weightedMean = ((datalist, 49.5),)
    stdev = ((datalist, 29.011491975882016),)
    rms = ((datalist, 57.301832431432764),)
    weightedStdev = ((datalist_weighted, 29.01149197588202),)
    median = ((datalist, 49.5),)
    modeEstimate = ((datalist, 49.5),)
    MAD = ((datalist, 25.0),)
    biweightLocation = ((datalist, 6.0, 49.5),)
    biweightScale = ((datalist, 9.0, 30.094338485893395),)
    biweightClipped = ((datalist, 6.0, 1.0, {'biweightLocation':49.5, 
        'biweightScale':1.8919771279665285, 'dataList':[48, 49, 50, 51]}),)
    biweightTransform = (datalist_short, 6.0, [[0, 1.0],
        [1, 0.9972583974514575],
        [2, 0.9890561699229076],
        [3, 0.9754610577655844],
        [4, 0.9565859615648774],
        [5, 0.9325889421403316],
        [6, 0.9036732205456486],
        [7, 0.870087178068685],
        [8, 0.8321243562314538],
        [9, 0.7901234567901234]])

    def testmean(self):
        """ astStats.mean should give known result with known input """
        for data, result in self.mean:
            answer = astStats.mean(data)
            self.assertEqual(result, answer)

    def testweightedMean(self):
        """ astStats.weightedMean should give known result with known input """
        for data, result in self.weightedMean:
            answer = astStats.weightedMean(data)
            self.assertEqual(result, answer)

    def teststdev(self):
        """ astStats.stdev should give known result with known input """
        for data, result in self.stdev:
            answer = astStats.stdev(data)
            self.assertAlmostEqual(result, answer)
    
    def testrms(self):
        """ astStats.rms should give known result with known input """
        for data, result in self.rms:
            answer = astStats.rms(data)
            self.assertAlmostEqual(result, answer)

    def testweightedStdev(self):
        """ astStats.weightedStdev should give known result with known input """
        for data, result in self.weightedStdev:
            answer = astStats.weightedStdev(data)
            self.assertAlmostEqual(result, answer)

    def testmedian(self):
        """ astStats.median should give known result with known input """
        for data, result in self.median:
            answer = astStats.median(data)
            self.assertEqual(result, answer)

    def testmodeEstimate(self):
        """ astStats.modeEstimate should give known result with known input """
        for data, result in self.modeEstimate:
            answer = astStats.modeEstimate(data)
            self.assertEqual(result, answer)

    def testMAD(self):
        """ astStats.MAD should give known result with known input """
        for data, result in self.MAD:
            answer = astStats.MAD(data)
            self.assertEqual(result, answer)
       
    def testbiweightLocation(self):
        """ astStats.biweightLocation should give known result with known input """
        for data, TC, result in self.biweightLocation:
            answer = astStats.biweightLocation(data, TC)
            self.assertEqual(answer, result)

    def testbiweightScale(self):
        """ astStats.biweightScale should give known result with known input """
        for data, TC, result in self.biweightScale:
            answer = astStats.biweightScale(data, TC)
            self.assertAlmostEqual(result, answer)

    def testbiweightClipped(self):
        """ astStats.biweightClipped should give known result with known input """
        for data, TC, sigma, result in self.biweightClipped:
            answer = astStats.biweightClipped(data, TC, sigma)
            self.assertEqual(answer['biweightLocation'], 
                            result['biweightLocation'])
            self.assertAlmostEqual(answer['biweightScale'], 
                            result['biweightScale'])
            self.assertListEqual(answer['dataList'],
                            result['dataList'])
if __name__ == "__main__":
    unittest.main()

