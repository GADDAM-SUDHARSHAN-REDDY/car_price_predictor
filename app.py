import streamlit as st
import pandas as pd
import joblib
import time
import plotly.graph_objects as go
import plotly.express as px

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CarVal · AI Price Predictor",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
#  GLOBAL CSS  — Luxury Dark Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600;700&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e0d4 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 0%, #1a1025 0%, #0a0a0f 60%) !important;
}

/* hide streamlit chrome */
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f0f18 !important;
    border-right: 1px solid rgba(255,220,150,0.08) !important;
}

/* ── Block container ── */
.block-container {
    max-width: 780px !important;
    padding: 2rem 1.5rem 4rem !important;
}

/* ── Hero Section ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: rgba(212,175,55,0.12);
    border: 1px solid rgba(212,175,55,0.3);
    color: #d4af37;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 20px;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: clamp(2.8rem, 7vw, 4.2rem) !important;
    font-weight: 300 !important;
    letter-spacing: -0.02em !important;
    line-height: 1.1 !important;
    color: #f0ebe3 !important;
    margin-bottom: 0.5rem !important;
}
.hero-title span {
    color: #d4af37;
    font-style: italic;
}
.hero-sub {
    font-size: 0.95rem;
    color: #7a7068;
    letter-spacing: 0.03em;
    font-weight: 300;
    margin-bottom: 2.5rem;
}
.divider {
    width: 60px;
    height: 1px;
    background: linear-gradient(90deg, transparent, #d4af37, transparent);
    margin: 0 auto 2.5rem;
}

/* ── Form Card — targets Streamlit's native block wrapper ── */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.025) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    backdrop-filter: blur(10px) !important;
    margin-bottom: 1.5rem !important;
}
.section-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #d4af37;
    margin-bottom: 1.2rem;
    display: block;
}

/* ── Streamlit widget overrides ── */
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label,
[data-testid="stTextInput"] label {
    font-size: 0.78rem !important;
    font-weight: 400 !important;
    color: #9a9088 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #e8e0d4 !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s !important;
}

[data-testid="stSelectbox"] > div > div:hover,
[data-testid="stNumberInput"] input:focus {
    border-color: rgba(212,175,55,0.5) !important;
}

/* ── Button ── */
[data-testid="stButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, #d4af37 0%, #b8962e 100%) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.85rem 2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 24px rgba(212,175,55,0.2) !important;
    margin-top: 1rem !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(212,175,55,0.35) !important;
    background: linear-gradient(135deg, #e0bc44 0%, #c4a035 100%) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Result Card ── */
.result-card {
    background: linear-gradient(135deg, rgba(212,175,55,0.08) 0%, rgba(212,175,55,0.03) 100%);
    border: 1px solid rgba(212,175,55,0.25);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin: 2rem 0;
}
.result-label {
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #d4af37;
    margin-bottom: 0.6rem;
}
.result-price {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(2.8rem, 8vw, 4rem);
    font-weight: 600;
    color: #f0ebe3;
    letter-spacing: -0.02em;
    line-height: 1;
    margin-bottom: 0.4rem;
}
.result-meta {
    font-size: 0.78rem;
    color: #5c5550;
}

/* ── Metric Pills ── */
.metric-row {
    display: flex;
    gap: 0.8rem;
    justify-content: center;
    margin-top: 1.5rem;
    flex-wrap: wrap;
}
.metric-pill {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 0.6rem 1.1rem;
    text-align: center;
}
.metric-pill-label {
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #5c5550;
    margin-bottom: 0.2rem;
}
.metric-pill-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.2rem;
    font-weight: 600;
    color: #c8b97a;
}

/* ── Chart container ── */
.chart-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
    font-weight: 400;
    color: #9a9088;
    letter-spacing: 0.04em;
    margin: 2rem 0 0.5rem;
}

/* ── Download Button ── */
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #9a9088 !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    padding: 0.5rem 1.2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.2s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    border-color: rgba(212,175,55,0.4) !important;
    color: #d4af37 !important;
}

/* ── Text Area ── */
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    color: #7a7068 !important;
    font-size: 0.82rem !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: #d4af37 !important; }

/* ── Progress bar ── */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #d4af37, #b8962e) !important;
}

/* ── Success / Warning / Error ── */
[data-testid="stSuccess"] {
    background: rgba(212,175,55,0.08) !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
    border-radius: 8px !important;
    color: #c8b97a !important;
}
[data-testid="stWarning"] {
    border-radius: 8px !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    margin-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.05);
}
.footer-brand {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.4rem;
    font-weight: 600;
    color: #d4af37;
    letter-spacing: 0.1em;
    display: block;
    margin-bottom: 0.6rem;
}
.footer-line {
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #2e2b28;
}
.footer-line .dot { color: #3a3530; margin: 0 0.5rem; }
.footer-line .highlight { color: #d4af37; font-weight: 500; }

/* ── Columns gap ── */
[data-testid="column"] { padding: 0 0.4rem !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2a2520; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LOAD ARTIFACTS
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    model = joblib.load("final_linear_model.pkl")
    columns = joblib.load("model_columns.pkl")
    return model, columns

@st.cache_data
def load_brand_model_map():
    try:
        return joblib.load("brand_model_map.pkl")
    except FileNotFoundError:
        return None

def indian_format(n):
    """Format number in Indian style: 1,23,45,678"""
    n = int(n)
    s = str(n)
    if len(s) <= 3:
        return s
    last3 = s[-3:]
    rest = s[:-3]
    groups = []
    while len(rest) > 2:
        groups.append(rest[-2:])
        rest = rest[:-2]
    if rest:
        groups.append(rest)
    return ','.join(reversed(groups)) + ',' + last3

model, columns = load_model()
brand_model_map = load_brand_model_map()

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">AI-Powered Valuation</div>
    <div class="hero-title">What's your car<br><span>worth today?</span></div>
    <p class="hero-sub">Instant market price estimation · Indian used car market</p>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FORM
# ─────────────────────────────────────────────
st.markdown('<span class="section-label">Vehicle Details</span>', unsafe_allow_html=True)

# ── Row 1: Brand + Model (if map available) or simple inputs ──
if brand_model_map:
    col1, col2 = st.columns(2)
    with col1:
        brand = st.selectbox("Brand", sorted(brand_model_map.keys()))
    with col2:
        car_model = st.selectbox("Model", sorted(brand_model_map.get(brand, [])))
else:
    brand, car_model = None, None

# ── Row 2: Year + KM ──
col3, col4 = st.columns(2)
with col3:
    year = st.number_input("Year of Manufacture", min_value=1990, max_value=2025, value=2020)
with col4:
    km_driven = st.number_input("Kilometres Driven", min_value=0, max_value=1000000, value=45000, step=1000)

# ── Row 3: Fuel + Transmission ──
col5, col6 = st.columns(2)
with col5:
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
with col6:
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

# ── Row 4: Seller Type + Owner ──
col7, col8 = st.columns(2)
with col7:
    seller_type = st.selectbox("Seller Type", ["Individual", "Dealer", "Trustmark Dealer"])
with col8:
    owner = st.selectbox("Ownership", ["First Owner", "Second Owner", "Third Owner", "Fourth & Above Owner", "Test Drive Car"])


# ─────────────────────────────────────────────
#  VALIDATION
# ─────────────────────────────────────────────
if km_driven < 0:
    st.warning("KM Driven cannot be negative.")
    st.stop()

# ─────────────────────────────────────────────
#  PREDICT BUTTON
# ─────────────────────────────────────────────
predict_clicked = st.button("✦  Estimate Value", key="predict")

if predict_clicked:
    with st.spinner("Analysing market data…"):
        time.sleep(0.8)

        # ── Build input row ──
        input_data = dict.fromkeys(columns, 0)
        input_data['Year'] = year
        input_data['KM_Driven'] = km_driven

        # Map column names exactly as produced by pd.get_dummies on the training set
        mappings = [
            (f"Brand_{brand}", 1) if brand else None,
            (f"Model_{car_model}", 1) if car_model else None,
            (f"Fuel_{fuel_type}", 1),
            # Transmission: drop_first=True drops Automatic, so Manual is the flag
            ("Transmission_Manual", 1) if transmission == "Manual" else None,
            (f"Seller_Type_{seller_type}", 1),
            (f"Owner_{owner}", 1),
        ]
        for item in mappings:
            if item and item[0] in input_data:
                input_data[item[0]] = item[1]

        input_df = pd.DataFrame([input_data])

        try:
            predicted_price = model.predict(input_df)[0]
            predicted_price = max(predicted_price, 0)  # no negative prices

            # ── Result Card ──
            formatted = f"₹{indian_format(predicted_price)}"
            lakh_str = f"{predicted_price/100000:.2f} Lakh"
            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">Estimated Market Value</div>
                <div class="result-price">{formatted}</div>
                <div class="result-meta">{lakh_str}</div>
                <div class="metric-row">
                    <div class="metric-pill">
                        <div class="metric-pill-label">Year</div>
                        <div class="metric-pill-value">{year}</div>
                    </div>
                    <div class="metric-pill">
                        <div class="metric-pill-label">KM Driven</div>
                        <div class="metric-pill-value">{km_driven:,}</div>
                    </div>
                    <div class="metric-pill">
                        <div class="metric-pill-label">Fuel</div>
                        <div class="metric-pill-value">{fuel_type}</div>
                    </div>
                    <div class="metric-pill">
                        <div class="metric-pill-label">Gearbox</div>
                        <div class="metric-pill-value">{transmission}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Benchmark Chart ──
            avg_price   = 550000
            min_price   = 100000
            max_price   = 1500000

            fig = go.Figure()
            bar_colors = ['#d4af37', '#3d3530', '#2a2520', '#1f1c18']
            labels = ['Your Car', 'Market Avg', 'Min Range', 'Max Range']
            values = [predicted_price, avg_price, min_price, max_price]

            for label, val, color in zip(labels, values, bar_colors):
                fig.add_trace(go.Bar(
                    name=label, x=[label], y=[val],
                    marker_color=color,
                    marker_line_width=0,
                    text=f"₹{val/100000:.1f}L",
                    textposition='outside',
                    textfont=dict(color='#7a7068', size=11, family='DM Sans')
                ))

            fig.update_layout(
                barmode='group',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='DM Sans', color='#7a7068'),
                showlegend=True,
                legend=dict(
                    orientation='h', yanchor='bottom', y=1.02,
                    xanchor='right', x=1,
                    font=dict(size=10, color='#5c5550')
                ),
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(
                    showgrid=True, gridcolor='rgba(255,255,255,0.04)',
                    zeroline=False, tickfont=dict(size=10),
                    tickformat=',.0f', tickprefix='₹'
                ),
                margin=dict(l=10, r=10, t=40, b=10),
                height=300,
            )
            st.markdown('<p class="chart-title">Price Benchmark</p>', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # ── KM Trend Chart ──
            km_range = [max(0, km_driven - 30000), max(0, km_driven - 15000),
                        km_driven, km_driven + 15000, km_driven + 30000]
            trend_prices = []
            for k in km_range:
                row = dict.fromkeys(columns, 0)
                row['Year'] = year
                row['KM_Driven'] = k
                for item in mappings:
                    if item and item[0] in row:
                        row[item[0]] = item[1]
                trend_prices.append(max(model.predict(pd.DataFrame([row]))[0], 0))

            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=km_range, y=trend_prices,
                mode='lines+markers',
                line=dict(color='#d4af37', width=2),
                marker=dict(color='#d4af37', size=6),
                fill='tozeroy',
                fillcolor='rgba(212,175,55,0.05)',
                name='Price'
            ))
            # Highlight current point
            fig2.add_trace(go.Scatter(
                x=[km_driven], y=[predicted_price],
                mode='markers',
                marker=dict(color='#d4af37', size=12, line=dict(color='#0a0a0f', width=2)),
                name='Your Car',
                showlegend=False
            ))
            fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='DM Sans', color='#7a7068'),
                showlegend=False,
                xaxis=dict(
                    title='KM Driven', showgrid=False, zeroline=False,
                    tickfont=dict(size=10), title_font=dict(size=11)
                ),
                yaxis=dict(
                    title='Est. Price (₹)', showgrid=True,
                    gridcolor='rgba(255,255,255,0.04)',
                    zeroline=False, tickfont=dict(size=10),
                    tickformat=',.0f', title_font=dict(size=11)
                ),
                margin=dict(l=10, r=10, t=20, b=10),
                height=260,
            )
            st.markdown('<p class="chart-title">Price vs Kilometres</p>', unsafe_allow_html=True)
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

            # ── Download ──
            st.markdown("""
            <div style="background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.25);
            border-radius:10px;padding:0.9rem 1.2rem;text-align:center;margin:1rem 0;">
                <span style="font-size:0.72rem;letter-spacing:0.15em;text-transform:uppercase;
                color:#d4af37;font-family:'DM Sans',sans-serif;">✦ &nbsp;Valuation Complete</span>
            </div>
            """, unsafe_allow_html=True)
            result_df = pd.DataFrame({
                "Brand": [brand or "—"],
                "Model": [car_model or "—"],
                "Year": [year],
                "KM Driven": [km_driven],
                "Fuel": [fuel_type],
                "Transmission": [transmission],
                "Seller Type": [seller_type],
                "Owner": [owner],
                "Estimated Price (₹)": [indian_format(predicted_price)],
            })
            col_dl, col_share = st.columns([1, 2])
            with col_dl:
                st.download_button(
                    "↓ Download Report",
                    result_df.to_csv(index=False),
                    "carval_report.csv",
                    mime="text/csv"
                )
            with col_share:
                share_text = (
                    f"{brand or ''} {car_model or ''} ({year}, {km_driven:,} km, {fuel_type}) "
                    f"— Estimated at ₹{indian_format(predicted_price)} by CarVal AI"
                )
                st.text_area("Share", value=share_text, height=70, label_visibility="collapsed")

        except Exception as e:
            st.error(f"Prediction error: {e}")

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <span class="footer-brand">CarVal</span>
    <div class="footer-line">
        AI Car Price Predictor
        <span class="dot">·</span>
        Made by <span class="highlight">Sudharshan</span>
        <span class="dot">·</span>
        © 2025
    </div>
</div>
""", unsafe_allow_html=True)