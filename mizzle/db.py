from datetime import datetime
import psycopg2
import os

from mizzle.protocols import NMEA

class DB:
    def __init__(self):
        self.connection_string = os.environ.get('POSTGRES_URL')
        self.conn = psycopg2.connect(self.connection_string)
    def __del__(self):
        self.conn.close()

    def execute(self, *args):
        cur = self.conn.cursor()
        cur.execute(*args)
        cur.close()
        self.conn.commit()

    def insert_reading(self, timestamp, txt):
        parser = NMEA()
        tokens = parser.parse(txt)

        column_names = ('datetime',)
        reading_values = (timestamp,)

        for value, reading_type, _ in tokens:
            reading_values += (value,)
            if reading_type == 'C0':
                column_names += ('temp_air',)
            elif reading_type == 'P0':
                column_names += ('pressure',)
            elif reading_type == 'H0':
                column_names += ('humidity',)
            elif reading_type == 'A0':
                column_names += ('wind_dir_min',)
            elif reading_type == 'A1':
                column_names += ('wind_dir_ave',)
            elif reading_type == 'A2':
                column_names += ('wind_dir_max',)
            elif reading_type == 'S0':
                column_names += ('wind_speed_min',)
            elif reading_type == 'S1':
                column_names += ('wind_speed_ave',)
            elif reading_type == 'S2':
                column_names += ('wind_speed_max',)
            elif reading_type == 'V0':
                column_names += ('rain_accum',)
            elif reading_type == 'Z0':
                column_names += ('rain_duration',)
            elif reading_type == 'R0':
                column_names += ('rain_intensity',)
            elif reading_type == 'V1':
                column_names += ('hail_accum',)
            elif reading_type == 'Z1':
                column_names += ('hail_duration',)
            elif reading_type == 'R1':
                column_names += ('hail_intensity',)
        query = "INSERT INTO mizzle_readings {0} VALUES ({1})".format(
            str(column_names).replace("'", ''),
            ','.join(['%s']*len(column_names)),
        )
        #print(query)
        #print(str(reading_values))
        self.execute(query, reading_values)




