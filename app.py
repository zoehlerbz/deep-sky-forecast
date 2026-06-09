import streamlit as st
from datetime import datetime, timedelta

from src.pipeline.data_extraction import DataExtraction

pipeline_data_extraction = DataExtraction()

daily_data, hourly_data = pipeline_data_extraction.run()


###############
#     APP     #
###############

st.text(f"Localização: {pipeline_data_extraction.location} ({pipeline_data_extraction.latitude}, {pipeline_data_extraction.longitude})")
st.text(f"Última atualização: {pipeline_data_extraction.date_now}")

day_0 = datetime.today()
day_1 = day_0 + timedelta(days=1)
day_2 = day_0 + timedelta(days=2)
day_3 = day_0 + timedelta(days=3)

tab1, tab2, tab3, tab4 = st.tabs(
    [day_0.strftime("%Y-%m-%d"), day_1.strftime("%Y-%m-%d"), day_2.strftime("%Y-%m-%d"), day_3.strftime("%Y-%m-%d")]
)

with tab1:
    data1 = hourly_data[hourly_data['datetime'].dt.strftime("%Y-%m-%d") == day_0.strftime("%Y-%m-%d")]
    
    st.write(f"Dia {day_0.strftime("%Y-%m-%d")}")
    st.dataframe(data1)

with tab2:
    data2 = hourly_data[hourly_data['datetime'].dt.strftime("%Y-%m-%d") == day_1.strftime("%Y-%m-%d")]
    
    st.write(f"Dia {day_1.strftime("%Y-%m-%d")}")
    st.dataframe(data2)

with tab3:
    data3 = hourly_data[hourly_data['datetime'].dt.strftime("%Y-%m-%d") == day_2.strftime("%Y-%m-%d")]
    
    st.write(f"Dia {day_2.strftime("%Y-%m-%d")}")
    st.dataframe(data3)

with tab4:
    data4 = hourly_data[hourly_data['datetime'].dt.strftime("%Y-%m-%d") == day_3.strftime("%Y-%m-%d")]
    
    st.write(f"Dia {day_3.strftime("%Y-%m-%d")}")
    st.dataframe(data4)





#st.text("Daily data")
#st.dataframe(daily_data)

#st.text("Hourly data")
#st.dataframe(hourly_data)