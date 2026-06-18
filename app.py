import os
import streamlit as st

from src.database.get_location import DatabaseLocation

location = DatabaseLocation()

st.text(f'{location.location_id} - {location.location_name} ({location.location_lat}, {location.location_lon})')