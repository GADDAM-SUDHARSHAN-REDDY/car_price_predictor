import streamlit as st
import pandas as pd
import joblib
import requests
from streamlit_lottie import st_lottie
import time
import plotly.graph_objects as go
import plotly.express as px

# -------------------- APP CONFIG --------------------
st.set_page_config(
    page_title="Ultimate Car Price Predictor",
    page_icon="🚘",
    layout="centered",  # Changed from "wide"
    initial_sidebar_state="auto"
)

# -------------------- HELPER FUNCTIONS --------------------
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def animate_progress(seconds=1):
    progress = st.progress(0)
    for i in range(101):
        time.sleep(seconds/100)
        progress.progress(i)

# -------------------- LOAD MODEL --------------------
model = joblib.load("final_linear_model.pkl")
columns = joblib.load("model_columns.pkl")

# -------------------- SIDEBAR --------------------
st.sidebar.image("car.png", use_container_width=True)
st.sidebar.header("Ultimate Car Price Predictor")
st.sidebar.write("Powered by Streamlit & AI")
st.sidebar.markdown("Made by Sudharshan")

# Lottie animation on sidebar (optional)
lottie_sidebar = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_nC6xPV.json")
if lottie_sidebar:
    st_lottie(lottie_sidebar, height=200, key="sidebar_lottie")

# -------------------- HEADER --------------------
st.markdown("<h1 style='text-align:center;color:#1f77b4;'>Ultimate Car Price Prediction App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;font-size:18px;'>Enter car details below and get an instant AI-powered price prediction!</p>", unsafe_allow_html=True)
st.markdown("---")

# -------------------- INPUT SECTION --------------------
st.subheader("Enter Car Details:")

with st.container():
    col1, col2, col3 = st.columns([1.2,1.2,1])
    
    with col1:
        year = st.number_input("Year of Manufacture", min_value=1990, max_value=2035, value=2020)
        km_driven = st.number_input("KM Driven", min_value=0, value=50000)
    
    with col2:
        fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
        transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
    
    with col3:
        lottie_car = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_nC6xPV.json")
        if lottie_car:
            st_lottie(lottie_car, height=200, key="car_anim")

# -------------------- INPUT VALIDATION --------------------
if km_driven < 0:
    st.warning("KM Driven cannot be negative!")
    st.stop()
if year < 1990 or year > 2035:
    st.warning("Enter a realistic year!")
    st.stop()

# -------------------- PREDICT BUTTON --------------------
predict_button = st.button("Predict Price", key="predict")

if predict_button:
    with st.spinner('Calculating Price...'):
        time.sleep(1)

        # -------------------- PREPARE INPUT --------------------
        input_data = dict.fromkeys(columns, 0)
        input_data['Year'] = year
        input_data['KM_Driven'] = km_driven

        fuel_col = f"Fuel_{fuel_type}"
        trans_col = f"Transmission_{transmission}"
        if fuel_col in input_data:
            input_data[fuel_col] = 1
        if trans_col in input_data:
            input_data[trans_col] = 1

        input_df = pd.DataFrame([input_data])

        # -------------------- PREDICTION --------------------
        try:
            predicted_price = model.predict(input_df)[0]
            
            # Animate progress bar
            animate_progress(1)

            # -------------------- DISPLAY RESULT --------------------
            st.markdown(
                f"<h2 style='text-align:center;color:#ff4b4b;'>Predicted Car Price: ₹{predicted_price:,.2f}</h2>", 
                unsafe_allow_html=True
            )

            # -------------------- INTERACTIVE CHARTS --------------------
            avg_price = 500000  # Replace with dataset average if available
            min_price = 100000
            max_price = 1500000
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Predicted Price', x=['Price'], y=[predicted_price], marker_color='#1f77b4'))
            fig.add_trace(go.Bar(name='Average Price', x=['Price'], y=[avg_price], marker_color='#ff6361'))
            fig.add_trace(go.Bar(name='Min Price', x=['Price'], y=[min_price], marker_color='#ffa500'))
            fig.add_trace(go.Bar(name='Max Price', x=['Price'], y=[max_price], marker_color='#2ca02c'))
            fig.update_layout(title='Price Comparison', barmode='group', template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)

            # Price trend vs KM
            km_values = [max(0, km_driven - 10000), km_driven, km_driven + 10000]
            trend_data = []
            for k in km_values:
                row = dict.fromkeys(columns, 0)
                row['Year'] = year
                row['KM_Driven'] = k
                if fuel_col in row:
                    row[fuel_col] = 1
                if trans_col in row:
                    row[trans_col] = 1
                trend_data.append(model.predict(pd.DataFrame([row]))[0])
            fig2 = px.line(x=km_values, y=trend_data, labels={'x':'KM Driven','y':'Predicted Price'}, title='Price Trend vs KM Driven')
            st.plotly_chart(fig2, use_container_width=True)

            st.success("Prediction Complete")

            # -------------------- DOWNLOADABLE RESULT --------------------
            result_df = pd.DataFrame({
                "Year": [year],
                "KM Driven": [km_driven],
                "Fuel Type": [fuel_type],
                "Transmission": [transmission],
                "Predicted Price": [f"₹{predicted_price:,.2f}"]
            })
            st.download_button("Download Prediction Summary", result_df.to_csv(index=False), "car_price_prediction.csv")

            share_text = f"My car ({fuel_type}, {transmission}, {year}, {km_driven} km) is worth ₹{predicted_price:,.2f}!"
            st.text_area("Share this result", value=share_text, height=100)

        except Exception as e:
            st.error(f"Error during prediction: {e}")

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown("<p style='text-align:center;'>Made by Sudharshan | Ultimate Streamlit Demo</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>© 2024 All rights reserved.</p>", unsafe_allow_html=True)

# -------------------- FEEDBACK FORM --------------------
st.markdown("---")
st.subheader("💬 Feedback")
feedback = st.text_area("Any feedback or suggestions?")
if st.button("Submit Feedback"):
    st.success("Thanks for your feedback!")
