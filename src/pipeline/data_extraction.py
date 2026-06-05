import pandas as pd

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from src.database.get_location import DatabaseLocation

from src.extract.get_climate_hourly_data import ClimateHourly
from src.extract.get_moon_hourly_data import MoonHourly
from src.extract.get_moon_daily_data import MoonDaily

class DataExtraction:

    def __init__(self, latitude, longitude) -> None:

        location = DatabaseLocation()

        self.latitude = location.location_lat
        self.longitude = location.location_lon
        self.date_now = datetime.now(ZoneInfo("America/Sao_Paulo")).replace(
                            hour=0,
                            minute=0,
                            second=0,
                            microsecond=0
                        )

    def run(self):
        # Moon daily data
        daily_data = self.get_daily_data()

        # Moon + climate hourly data
        hourly_data = self.get_hourly_data()

        return daily_data, hourly_data

    def get_hourly_data(self):  # moon + climate
        climate_hourly = ClimateHourly(
            latitude=self.latitude,
            longitude=self.longitude
        )
        climate_hourly_data = climate_hourly.get_climate_hourly_data()

        moon_hourly = MoonHourly(
            latitude=self.latitude,
            longitude=self.longitude,
            date_now=self.date_now
        )
        moon_hourly_data = moon_hourly.get_moon_hourly_data()

        full_hourly_data = pd.merge(left=climate_hourly_data, right=moon_hourly_data, how='outer', on='datetime')

        return full_hourly_data

    def get_daily_data(self):  # moon
        moon_daily = MoonDaily(
            latitude=self.latitude,
            longitude=self.longitude,
            date_now=self.date_now
        )

        return moon_daily.get_moon_daily_data()