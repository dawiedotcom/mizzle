
DROP TABLE IF EXISTS mizzle_readings;
CREATE TABLE mizzle_readings (
  datetime timestamp without time zone,
  temp_air double precision,
  pressure double precision,
  humidity double precision,
  wind_dir_min double precision,
  wind_dir_ave double precision,
  wind_dir_max double precision,
  wind_speed_min double precision,
  wind_speed_ave double precision,
  wind_speed_max double precision,
  rain_accum double precision,
  rain_duration double precision,
  rain_intensity double precision,
  hail_accum double precision,
  hail_duration double precision,
  hail_intensity double precision
);

SELECT create_hypertable(
    'mizzle_readings'
  , 'datetime'
  --, chunk_time_interval => interval '1 hour'
);
