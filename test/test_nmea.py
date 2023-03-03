from datetime import datetime
import unittest

from mizzle.protocols import NMEA

class TestNMEA(unittest.TestCase):

    parser = NMEA()

    def test_simple_XDR(self):
        txt = '$WIXDR,C,5.7,C,0,H,80.5,P,0,P,1018.1,H,0*48'
        expect = [
            (5.7, 'C0', 'CC'),
            (80.5, 'H0', 'HP'),
            (1018.1, 'P0', 'PH'),
        ]
        ts = datetime.now()

        result = self.parser.parse(ts, txt)

        for meas_res, meas_exp in zip(result, expect):
            self.assertEqual(ts, meas_res[0])
            for r, e in zip(meas_res[1:], meas_exp):
                self.assertEqual(r, e)

    def test_simple_MWV(self):
        txt = '$WIMWV,057,R,2.7,M,A*39'
        expect = [(57.0, 2.7)]
        ts = datetime.now()

        result = self.parser.parse(ts, txt)

        self.assertEqual(result[0], ts)
        self.assertEqual(result[1], 57.0)
        self.assertEqual(result[2], 2.7)

    def test_unkown_token(self):
        with self.assertRaises(Exception):
            self.parser.parse(None, "aaou")

if __name__ == '__main__':
    unittest.main()
