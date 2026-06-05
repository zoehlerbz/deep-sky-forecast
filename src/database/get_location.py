import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')

class DatabaseLocation:

    def __init__(self) -> None:

        location = self.get_location_data()

        self.location_id = location[0]
        self.location_name = location[1]
        self.location_lat = location[2]
        self.location_lon = location[3]

    def engine(self):
        engine = create_engine(
            f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        )

        return engine
        
    def get_location_data(self):
        engine = self.engine()

        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM DimLocations"))
            rows = result.first()

            return rows