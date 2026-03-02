import streamlit as st
import requests
import os
import joblib
import numpy as np

st.title(" Weather Prediction Web App")

# Load ML Model
try:
    model = joblib.load("models/weather_model.pkl")
except:
    st.error("Model not found! Run train_model.py")
    st.stop()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if API_KEY is None:
    st.error("API Key not set!")
    st.stop()

city = st.text_input("Enter City Name", "Hyderabad")

if st.button("Get Live Weather"):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        st.success("Weather Data Fetched")

        st.write("Temperature:", temp,"°C")
        st.write("Humidity:", humidity,"%")
        st.write("Pressure:", pressure,"hPa")
        st.write("Wind Speed:", wind,"m/s")

        input_data = np.array([[temp,humidity,pressure,wind]])

        prediction = model.predict(input_data)

        st.subheader("Prediction Result")

        if prediction[0]==1:
            st.error(" Rain Expected Tomorrow")
        else:
            st.success(" No Rain Tomorrow")

    else:
        st.error("City not found")