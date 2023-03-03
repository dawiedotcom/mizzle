#!/bin/env python3

import argparse
from datetime import datetime
import sys

from mizzle.protocols import NMEA

reading_type_description = {
    'C0': 'Air temperature',
    'C1': 'Internal temperature',
    'C2': 'Heating temperature',
    'C3': 'Aux. temperature',
    'H0': 'Relative humidity',
    'V0': 'Rain acculumulation',
    'V1': 'Hail accumulation',
    'Z0': 'Rain duration',
    'Z1': 'Hail duration',
    'R0': 'Rain current intensity',
    'R1': 'Hail current intensity',
    'U0': 'Supply voltage',
    'U1': 'Heating voltage',
    'U2': '3.5V ref. voltage',
    'U3': 'Solar radiation',
    'U4': 'Ultrasonic level sensor',
    'A0': 'Wind direction min',
    'A1': 'Wind direction average',
    'A2': 'Wind direction max',
    'S0': 'Wind speed min',
    'S1': 'Wind speed average',
    'S2': 'Wind speed max',
    'P0': 'Pressure',
}

def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('-p', '--port', help='Serial port')

    args = argp.parse_args()

    if args.port:
        return
    else:
        input = sys.stdin

    parser = NMEA()
    aggregated = {}
    for line in input:
        ts = datetime.now()
        readings = parser.parse(ts, line)
        for reading in readings:
            print(reading)
            reading_type = reading[2]
            if not reading_type in aggregated:
                aggregated[reading_type] = []
            aggregated[reading_type].append(reading)
        print()
    for k,v in aggregated.items():
        print(f'{reading_type_description.get(k, k):30}: {len(v)}')

if __name__ == '__main__':
    main()
