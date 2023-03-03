#!/bin/env python3

import argparse
from datetime import datetime
import sys
import serial

from mizzle.db import (DB, Readings)

def run_from_stdin(args):
    # Batch process data from stdin and commit everything to the database.
    # The expected format is '<timestap> <xdr_data>'.
    db_readings = []

    for line in sys.stdin:
        ts_str, xdr_txt = line.split(' ')
        ts = datetime.strptime(ts_str, '%Y-%m-%dT%H:%M:%S.%f')
        db_readings.append(Readings.fromXDR(ts, xdr_txt))

    db = DB()
    with db.session() as session:
        session.add_all(db_readings)
        session.commit()

def run_from_serial(args):
    # Reads data directly from the serial device and commits readings to
    # the database as they arrive
    ws = serial.Serial(args.port, baudrate=args.baudrate)
    db = DB()
    while True:
        xdr_txt = ws.readline().decode()
        ts = datetime.now()

        reading = Readings.fromXDR(ts, xdr_txt)

        with db.session() as session:
            session.add_all([reading])
            session.commit()

def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('-p', '--port',
                      help='Serial port')
    argp.add_argument('-b', '--baudrate', default=19200, type=int,
                      help='Serial port baudrate')

    args = argp.parse_args()

    if args.port:
        run_from_serial(args)
    else:
        run_from_stdin(args)


if __name__ == '__main__':
    main()
