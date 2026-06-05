import os
import json
import requests
import pandas as pd

from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

IPGEOLOCATION_APIKEY = os.getenv('IPGEOLOCATION_APIKEY')

class MoonDaily:
    def __init__(self, latitude, longitude, date_now) -> None:
        self.latitude = str(round(latitude, 5))
        self.longitude = str(round(longitude, 5))
        self.start_date = date_now.date()  # Obtem apenas a data
        self.end_date = self.start_date + timedelta(days=16)  # Define a data em 16 dias

    def get_moon_daily_data(self) -> pd.DataFrame:
        url = f"https://api.ipgeolocation.io/v3/astronomy/timeSeries?apiKey={IPGEOLOCATION_APIKEY}&lat={self.latitude}&long={self.longitude}&elevation=10&dateStart={self.start_date}&dateEnd={self.end_date}"
        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data={})
        response_json = json.loads(response.text)

        astronomy_data = response_json['astronomy']

        astronomy_dataframe = self.data_to_dataframe(astronomy_data)

        return astronomy_dataframe
    
    def data_to_dataframe(self, api_data: list) -> pd.DataFrame:
        rows = []

        for data in api_data:
            rows.append({
                'date':data['date'],
                'night_end':data['night_end'],
                'sunrise':data['sunrise'],
                'sunset':data['sunset'],
                'night_begin':data['night_begin'],
                'day_length':data['day_length'],
                'moon_phase':data['moon_phase'],
                'moonrise':data['moonrise'],
                'moonset':data['moonset'],
                'morning_astronomical_twilight_begin':data['morning']['astronomical_twilight_begin'],
                'morning_astronomical_twilight_end':data['morning']['astronomical_twilight_end'],
                'morning_golden_hour_begin':data['morning']['golden_hour_begin'],
                'morning_golden_hour_end':data['morning']['golden_hour_end'],
                'evening_astronomical_twilight_begin':data['evening']['astronomical_twilight_begin'],
                'evening_astronomical_twilight_end':data['evening']['astronomical_twilight_end'],
                'evening_golden_hour_begin':data['evening']['golden_hour_begin'],
                'evening_golden_hour_end':data['evening']['golden_hour_end']
            })

        dataframe = pd.DataFrame(rows)

        return dataframe