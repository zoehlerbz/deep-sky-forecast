import streamlit as st

from src.database.get_location import DatabaseLocation
from src.pipeline.data_extraction import DataExtraction

location = DatabaseLocation()

pipeline_data_extraction = DataExtraction(
    latitude=location.location_lat,
    longitude=location.location_lon,
    timezone=location.location_timezone
)

daily_data, hourly_data = pipeline_data_extraction.run()


###############
#     APP     #
###############

st.title("Teste app!")
st.header("Testando Streamlit.")
st.text("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

st.text(f"ID: {location.location_id}")
st.text(f"Localização: {location.location_name}")
st.text(f"Latitude: {location.location_lat}")
st.text(f"Longitude: {location.location_lon}")
st.text(f"Timezone: {location.location_timezone}")
st.text(f"Última atualização: {pipeline_data_extraction.date_now}")

st.text("Daily data")
st.dataframe(daily_data)

st.text("Hourly data")
st.dataframe(hourly_data)