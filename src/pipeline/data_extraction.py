import pandas as pd

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from src.extract.get_climate_hourly_data import ClimateHourly
from src.extract.get_moon_hourly_data import MoonHourly
from src.extract.get_moon_daily_data import MoonDaily

class DataExtraction:

    def __init__(self, latitude, longitude, timezone) -> None:

        self.latitude = latitude
        self.longitude = longitude
        self.date_now = datetime.now(ZoneInfo(timezone))

    def run(self):

        date_now = self.date_now.replace(
                            hour=0,
                            minute=0,
                            second=0,
                            microsecond=0
                        )

        # Moon daily data
        daily_data = self.get_daily_data(date_now=date_now)

        # Moon + climate hourly data
        hourly_data = self.get_hourly_data(date_now=date_now)

        return daily_data, hourly_data

    def get_hourly_data(self, date_now):  # moon + climate
        climate_hourly = ClimateHourly(
            latitude=self.latitude,
            longitude=self.longitude
        )
        climate_hourly_data = climate_hourly.get_climate_hourly_data()

        moon_hourly = MoonHourly(
            latitude=self.latitude,
            longitude=self.longitude,
            date_now=date_now
        )
        moon_hourly_data = moon_hourly.get_moon_hourly_data()

        full_hourly_data = pd.merge(left=climate_hourly_data, right=moon_hourly_data, how='outer', on='datetime')

        return full_hourly_data

    def get_daily_data(self, date_now):  # moon
        moon_daily = MoonDaily(
            latitude=self.latitude,
            longitude=self.longitude,
            date_now=date_now
        )

        return moon_daily.get_moon_daily_data()