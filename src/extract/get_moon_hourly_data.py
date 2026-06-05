import pandas as pd

from skyfield.api import load, Topos
from skyfield import almanac
from datetime import timedelta

class MoonHourly:
    def __init__(self, latitude, longitude, date_now) -> None:
        self.latitude = round(float(latitude), 5)
        self.longitude = round(float(longitude), 5)
        self.date_now = date_now

    def get_moon_hourly_data(self) -> pd.DataFrame:
        # carregar efemérides
        ts = load.timescale()
        eph = load('de421.bsp')

        earth = eph['earth']
        moon = eph['moon']

        # localização
        location = earth + Topos(
            latitude_degrees=self.latitude,
            longitude_degrees=self.longitude
        )

        # intervalo horário
        start = self.date_now
        hours = [start + timedelta(hours=i) for i in range(384)]  # Previsão para os próximos 16 dias

        rows = []

        for dt in hours:
            t = ts.from_datetime(dt)

            astrometric = location.at(t).observe(moon)
            alt, az, distance = astrometric.apparent().altaz()
            illumination = almanac.fraction_illuminated(eph, 'moon', t)

            rows.append({
                "datetime": dt,
                "altitude": alt.degrees,
                "azimuth": az.degrees,
                "distance_km": distance.km,
                "illumination_pct": illumination*100
            })

        hourly_dataframe = pd.DataFrame(rows)

        return hourly_dataframe