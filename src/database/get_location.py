import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from src.settings.config import user, password, host, port, database

class DatabaseLocation:

    def __init__(self) -> None:

        location = self.get_location_data()

        self.location_id = location[0]
        self.location_name = location[1]
        self.location_lat = location[2]
        self.location_lon = location[3]
        self.location_timezone = location[4]

    def engine(self):
        engine = create_engine(
            f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"
        )

        return engine
        
    def get_location_data(self):
        engine = self.engine()

        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM DimLocations"))
            rows = result.first()

            return rows