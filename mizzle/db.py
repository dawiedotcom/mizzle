from datetime import datetime
import psycopg2

from mizzle.protocols import NMEA

class DB:
    def __init__(self):
        self.connection_string = 'postgresql://postgres:testingtesting@localhost:5433/mizzle'
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
            match reading_type:
                case 'C0':
                    column_names += ('temp_air',)
                case 'P0':
                    column_names += ('pressure',)
                case 'H0':
                    column_names += ('humidity',)
                case 'A0':
                    column_names += ('wind_dir_min',)
                case 'A1':
                    column_names += ('wind_dir_ave',)
                case 'A2':
                    column_names += ('wind_dir_max',)
                case 'S0':
                    column_names += ('wind_speed_min',)
                case 'S1':
                    column_names += ('wind_speed_ave',)
                case 'S2':
                    column_names += ('wind_speed_max',)
                case 'V0':
                    column_names += ('rain_accum',)
                case 'Z0':
                    column_names += ('rain_duration',)
                case 'R0':
                    column_names += ('rain_intensity',)
                case 'V1':
                    column_names += ('hail_accum',)
                case 'Z1':
                    column_names += ('hail_duration',)
                case 'R1':
                    column_names += ('hail_intensity',)
        query = "INSERT INTO mizzle_readings {0} VALUES ({1})".format(
            str(column_names).replace("'", ''),
            ','.join(['%s']*len(column_names)),
        )
        #print(query)
        #print(str(reading_values))
        self.execute(query, reading_values)




