import pandas as pd
from datetime import datetime


class DataTransformation:

    def __init__(self, location_id) -> None:

        self.location_id = location_id

        self.VALID_MOON_PHASES = {
            "NEW_MOON":1,
            "WAXING_CRESCENT":2,
            "FIRST_QUARTER":3,
            "WAXING_GIBBOUS":4,
            "FULL_MOON":5,
            "WANING_GIBBOUS":6,
            "LAST_QUARTER":7,
            "WANING_CRESCENT":8
        }


    def transform_daily_data(self, daily_data):

        # Clean time
        time_cols = ['morning_astronomical_twilight_begin', 'morning_astronomical_twilight_end', 'morning_golden_hour_begin', 'morning_golden_hour_end', 'evening_astronomical_twilight_begin', 'evening_astronomical_twilight_end', 'evening_golden_hour_begin', 'evening_golden_hour_end', 'night_begin', 'night_end', 'day_length', 'sunrise', 'sunset', 'moonrise', 'moonset']
        for time_col in time_cols:
            daily_data[time_col] = daily_data[time_col].apply(self._clean_hour)

        # Clean date
        daily_data['date'] = daily_data['date'].apply(self._clean_date)

        # Moon phase
        daily_data['moon_phase'] = daily_data['moon_phase'].apply(self._clean_moon_phase)

        daily_data['location_id'] = self.location_id

        return daily_data


    def transform_hourly_data(self, hourly_data):
        
        hourly_data['datetime'] = hourly_data['datetime'].apply(self._clean_datetime_tz)
        hourly_data['temperature_2m'] = hourly_data['temperature_2m'].apply(self._clean_float, args=(-999.9, 999.9, 1))
        hourly_data['cloud_cover'] = hourly_data['cloud_cover'].apply(self._clean_int, args=(0, 100)) 
        hourly_data['visibility'] = hourly_data['visibility'].apply(self._clean_int, args=(0, 999999))  
        hourly_data['precipitation_probability'] = hourly_data['precipitation_probability'].apply(self._clean_int, args=(0, 100))
        hourly_data['wind_speed_10m'] = hourly_data['wind_speed_10m'].apply(self._clean_float, args=(-999.9, 999.9, 1))
        hourly_data['wind_direction_10m'] = hourly_data['wind_direction_10m'].apply(self._clean_float, args=(0, 360, 3)) 
        hourly_data['altitude'] = hourly_data['altitude'].apply(self._clean_float, args=(-90000, 90000, 3))
        hourly_data['azimuth'] = hourly_data['azimuth'].apply(self._clean_float, args=(0, 360, 3)) 
        hourly_data['distance_km'] = hourly_data['distance_km'].apply(self._clean_int, args=(0, 999999)) 
        hourly_data['illumination_pct'] = hourly_data['illumination_pct'].apply(self._clean_int, args=(0, 100))

        hourly_data['location_id'] = self.location_id

        return hourly_data


    def _clean_text(self, value):

        try:
            value = str(value)
            return value

        except:
            pass

        return None


    # Clean location_name
    def _clean_location(self, value):

        try:
            if value == '':
                raise ValueError(f"Location name can't be Null")

            if value == None:
                raise ValueError(f"Location name can't be Null")

            value = self._clean_text(value)
            
            return value

        except Exception as exc:
            raise ValueError(f"Location error: {exc}")


    # Clean lat and lon
    def _clean_coordinates(self, value):

        try:
            value = float(value)

            if -999.99999 <= value <= 999.99999:
                return round(value, 5)
            
        except:
            pass

        return None


    # Clean moon_phase
    def _clean_moon_phase(self, value):

        try:
            value = self._clean_text(value)

            if value in self.VALID_MOON_PHASES.keys():
                return self.VALID_MOON_PHASES[value]
        
        except Exception as exc:
            raise ValueError(f"Moon phase error: {exc}")
        

    # Clean datetime (FactHourlyData)
    def _clean_datetime_tz(self, value):

        try:
            value = pd.to_datetime(value, errors="coerce")

            if pd.isna(value):
                raise ValueError(f"Datetime can't be Null")
            
            if value.tzinfo is None:
                raise ValueError(f"Datetime timezone can't be Null")
            
            return value
            
        except Exception as exc:
            raise ValueError(f"Datetime error: {exc}")


    # Clean temperature, wind_speed, wind_direction, altitude, azimuth
    def _clean_float(self, value, min, max, decimal):

        try:
            value = float(value)

            if min <= value <= max:
                return round(value, decimal)

        except:
            pass

        return None


    # Clean cloud_cover, visibility, precipitation_probability, distance_km, illumination_pct
    def _clean_int(self, value, min, max):

        try:
            value = int(value)

            if min <= value <= max:
                return round(value)

        except:
            pass

        return None


    # Clean date (FactDailyData)
    def _clean_date(self, value):
        
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        
        except Exception as exc:
            raise ValueError(f"Date error: {exc}")


    # Clean morning_astronomical_twilight_begin, morning_astronomical_twilight_end, morning_golden_hour_begin, morning_golden_hour_end, evening_astronomical_twilight_begin, evening_astronomical_twilight_end, evening_golden_hour_begin, evening_golden_hour_end, night_begin, night_end, day_length, sunrise, sunset, moonrise, moonset
    def _clean_hour(self, value):

        try:
            return datetime.strptime(value, "%H:%M").time()

        except:
            return None