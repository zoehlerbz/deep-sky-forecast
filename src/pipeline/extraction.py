import os
import pandas as pd

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from src.extract.get_climate_hourly_data import ClimateHourly
from src.extract.get_moon_hourly_data import MoonHourly
from src.extract.get_moon_daily_data import MoonDaily

from src.database.get_location import DatabaseLocation

class DataExtraction:

    def __init__(self) -> None:

        location = DatabaseLocation()

        self.id = location.location_id
        self.location = location.location_name
        self.latitude = location.location_lat
        self.longitude = location.location_lon
        self.timezone = location.location_timezone
        self.date_now = datetime.now(ZoneInfo(self.timezone))

    def get_hourly_data(self):

        date_now = self._standardize_date_now()
        hourly_data = self._hourly_data(date_now=date_now)

        return hourly_data

    def get_daily_data(self):
        
        date_now = self._standardize_date_now()
        daily_data = self._daily_data(date_now=date_now)

        return daily_data

    def _standardize_date_now(self):

        date_now = self.date_now.replace(
                            hour=0,
                            minute=0,
                            second=0,
                            microsecond=0
                        )

        return date_now

    def _hourly_data(self, date_now):  # moon + climate
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

    def _daily_data(self, date_now):  # moon
        moon_daily = MoonDaily(
            latitude=self.latitude,
            longitude=self.longitude,
            date_now=date_now
        )

        return moon_daily.get_moon_daily_data()