@echo off
echo Launching Car Price Predictor...
cd /d D:\Projects\car_price_app
call .venv\Scripts\activate
streamlit run app.py
pause