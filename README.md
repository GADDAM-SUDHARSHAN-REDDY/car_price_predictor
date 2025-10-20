# car_price_predictor
A Streamlit app that predicts car prices using machine learning”

---

## 🚗 Car Price Prediction App

Welcome to the Car Price Prediction App! This interactive web application uses a linear regression model to estimate the price of a car based on user-input features. Built with Python, pandas, and Streamlit, the app is designed for clarity, reproducibility, and ease of use.

### 📌 Features

- Predict car prices based on key attributes like brand, year, fuel type, transmission, and mileage
- Clean, user-friendly interface powered by Streamlit
- Indian-style output formatting for intuitive readability
- Automated model loading and input validation
- Professional summary tables and visualizations

### 🧠 Model Overview

- **Algorithm**: Linear Regression
- **Training Data**: Cleaned dataset of Indian car listings
- **Preprocessing**: One-hot encoding, feature scaling, outlier removal
- **Evaluation**: R² score, MAE, RMSE

### 🛠️ Tech Stack

| Tool        | Purpose                          |
|-------------|----------------------------------|
| Python      | Core programming language        |
| pandas      | Data manipulation and analysis   |
| scikit-learn| Model training and evaluation    |
| Streamlit   | Web app deployment               |
| Git & GitHub| Version control and collaboration|

### 🚀 How to Run Locally

```bash
# Clone the repository
git clone https://github.com/your-username/Car_Price_app.git
cd Car_Price_app


# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run app.py
```

### 📁 Repository Structure

```
Car_Price_app/
├── data/                 # Raw and cleaned datasets
├── model/                # Saved model and preprocessing pipeline
├── app.py                # Streamlit app script
├── utils.py              # Helper functions
├── requirements.txt      # Dependencies
└── README.md             # Project overview
```


### 📚 Future Enhancements

- Add support for more car brands and features
- Integrate model explainability (e.g., SHAP values)
- Deploy on cloud platforms (Streamlit Sharing, Hugging Face Spaces, etc.)
- Add user authentication for secure access

### 🙌 Acknowledgements

- Dataset sourced from [Kaggle](https://www.kaggle.com/)
- Inspired by real-world car resale platforms in India

---
