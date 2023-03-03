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

        result = self.parser.parse(txt)

        for meas_res, meas_exp in zip(result, expect):
            for r, e in zip(meas_res, meas_exp):
                self.assertEqual(r, e)

    def test_simple_MWV(self):
        txt = '$WIMWV,057,R,2.7,M,A*39'
        expect = [(57.0, 2.7)]

        result = self.parser.parse(txt)

        self.assertEqual(result[0], 57.0)
        self.assertEqual(result[1], 2.7)

    def test_I60(self):
        txt = (
            '$WIXDR,' +
            'A,008,D,0,' +
            'A,343,D,1,' +
            'A,320,D,2,' +
            'S,1.6,M,0,' +
            'S,2.2,M,1,' +
            'S,3.1,M,2,' +
            'C,5.5,C,0,' +
            'H,61.7,P,0,' +
            'P,1021.5,H,0,' +
            'V,0.60,M,0,' +
            'Z,2470,s,0,' +
            'R,0.0,M,0,' +
            'V,0.0,M,1,' +
            'Z,0,s,1,' +
            'R,0.0,M,1' +
            '*42'
        )
        expect = [
            (8, 'A0', 'AD'),
            (343, 'A1', 'AD'),
            (320, 'A2', 'AD'),
            (1.6, 'S0', 'SM'),
            (2.2, 'S1', 'SM'),
            (3.1, 'S2', 'SM'),
            (5.5, 'C0', 'CC'),
            (61.7, 'H0', 'HP'),
            (1021.5, 'P0', 'PH'),
            (0.60, 'V0', 'VM'),
            (2470, 'Z0', 'Zs'),
            (0.0, 'R0', 'RM'),
            (0.0, 'V1', 'VM'),
            (0.0, 'Z1', 'Zs'),
            (0.0, 'R1', 'RM'),
        ]

        result = self.parser.parse(txt)
        for r, e in zip(result, expect):
            for i in range(3):
                self.assertEqual(e[i], r[i])
        self.assertEqual(len(result), len(expect))


    def test_unkown_token(self):
        with self.assertRaises(Exception):
            self.parser.parse(None, "aaou")

if __name__ == '__main__':
    unittest.main()
