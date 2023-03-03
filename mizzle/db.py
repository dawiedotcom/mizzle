from datetime import datetime
from sqlalchemy import (
    create_engine,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Session,
    Mapped,
    DeclarativeBase,
    mapped_column,
)

from mizzle.protocols import NMEA

class Base(DeclarativeBase):
    pass

class Readings(Base):
    __tablename__ = 'mizzle_readings'
    __table_args__ = (
        UniqueConstraint('datetime'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[datetime] 

    temp_air: Mapped[float]
    pressure: Mapped[float]
    humidity: Mapped[float]

    wind_dir_min: Mapped[float]
    wind_dir_ave: Mapped[float]
    wind_dir_max: Mapped[float]

    wind_speed_min: Mapped[float]
    wind_speed_ave: Mapped[float]
    wind_speed_max: Mapped[float]

    rain_accum: Mapped[float]
    rain_duration: Mapped[float]
    rain_intensity: Mapped[float]

    hail_accum: Mapped[float]
    hail_duration: Mapped[float]
    hail_intensity: Mapped[float]

    @staticmethod
    def fromXDR(timestamp, txt):
        parser = NMEA()
        tokens = parser.parse(txt)
        result = Readings(
            datetime = timestamp
        )
        for token in tokens:
            match token:
                case (value, 'C0', _):
                    result.temp_air = value
                case (value, 'P0', _):
                    result.pressure = value
                case (value, 'H0', _):
                    result.humidity = value
                case (value, 'A0', _):
                    result.wind_dir_min = value
                case (value, 'A1', _):
                    result.wind_dir_ave = value
                case (value, 'A2', _):
                    result.wind_dir_max = value
                case (value, 'S0', _):
                    result.wind_speed_min = value
                case (value, 'S1', _):
                    result.wind_speed_ave = value
                case (value, 'S2', _):
                    result.wind_speed_max = value
                case (value, 'V0', _):
                    result.rain_accum = value
                case (value, 'Z0', _):
                    result.rain_duration = value
                case (value, 'R0', _):
                    result.rain_intensity = value
                case (value, 'V1', _):
                    result.hail_accum = value
                case (value, 'Z1', _):
                    result.hail_duration = value
                case (value, 'R1', _):
                    result.hail_intensity = value
        return result


class DB:
    def __init__(self):
        self.connection_string = 'postgresql://postgres:testingtesting@localhost:5433/mizzle'
        self.engine = create_engine(self.connection_string)
        Base.metadata.create_all(self.engine)
    def session(self):
        return Session(self.engine)

