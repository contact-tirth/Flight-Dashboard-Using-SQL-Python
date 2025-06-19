import datetime

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pyodbc
from dbhelper import DB
import plotly.graph_objects as go

db = DB()

st.set_page_config(layout='wide',page_title='Flight Interative Dashboard')
st.markdown("<div style='text-align: center;font-size: 36px; font-weight: bold;'>Flight Interactive Dashboard</div>", unsafe_allow_html=True)

st.sidebar.title('Flight Analytics')
user_option = st.sidebar.selectbox('Select Your Choice',['Select One','Check Flights','Flight Analytics'])

if user_option == 'Check Flights':
    st.markdown("<div style='text-align: center;color:royalblue;font-size: 25px; font-weight: bold;'>Flight Details</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    city = db.fetch_cities()
    with col1:
        source = st.selectbox("Source", sorted(city))
    with col2:
        destination = st.selectbox("Destination", sorted(city))
    # st.checkbox('Only Non Stop')
    selected_date = st.date_input('Travel Date',
                  min_value=datetime.date(2019, 1, 1),
                  max_value=datetime.date(2019, 12, 31))
    if source==destination:
        st.error('Source & Destination Cannot be Same')
    else:
        if st.checkbox('Only Non Stop'):
            if st.button('Search Flight'):
                flag=1
                f_data = db.fetch_flight_details(source,destination,flag)
                if f_data=='No Direct Flights Available':
                    st.markdown("<div style='text-align: center;color:red;font-size: 25px; font-weight: bold;'>No Direct Flights Available</div>", unsafe_allow_html=True)
                else:
                    df = pd.DataFrame.from_records(f_data, columns=['Airline', 'Route', 'Dep_Time', 'Duration', 'Price'])
                    st.dataframe(df)
        else:
            if st.button('Search Flight'):
                flag=0
                f_data = db.fetch_flight_details(source, destination,flag)
                if f_data == 'No Direct Flights Available':
                    st.markdown(
                        "<div style='text-align: center;color:red;font-size: 25px; font-weight: bold;'>No Direct Flights Available</div>",
                        unsafe_allow_html=True)
                else:
                    df = pd.DataFrame.from_records(f_data,
                                                   columns=['Airline', 'Route', 'Dep_Time', 'Duration', 'Price'])
                    st.dataframe(df)

elif user_option == 'Flight Analytics':
    st.markdown("<div style='text-align: center;color:royalblue;font-size: 25px; font-weight: bold;'>Flight Analstics</div>",
                unsafe_allow_html=True)

    #Pie Chart
    airline, frequency = db.fetch_airline_fre()

    df = pd.DataFrame({
        'Airline': airline,
        'Flights': frequency
    })
    fig = px.pie(df, names='Airline', values='Flights')
    # Render in Streamlit
    st.title("Flight Data Pie Chart")
    st.plotly_chart(fig, use_container_width=True)

    #Bar Chart
    airport, no_of_flight = db.busiest_airpot()
    df1 = pd.DataFrame({
        'Airport': airport,
        'No_Of_Flights': no_of_flight
    })
    # Create the pie chart
    fig1 = px.bar(df1, x='Airport', y='No_Of_Flights',  color='Airport')
    # Render in Streamlit
    st.title("Busiest Airport Bar Chart")
    st.plotly_chart(fig1, use_container_width=True)

    #Line Chart
    doj , total_flight = db.daily_flights_airline()

    df2 = pd.DataFrame({
        'DoJ': doj,
        'Total_Flights': total_flight
    })

    fig2 = px.line(df2, x='DoJ', y='Total_Flights')
    # Render in Streamlit
    st.title("Flights Distribution by Date")
    st.plotly_chart(fig2, use_container_width=True)




