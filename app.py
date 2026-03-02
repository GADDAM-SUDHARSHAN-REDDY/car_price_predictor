import streamlit as st
import pandas as pd
import joblib
import time
import plotly.graph_objects as go

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CarVal · Intelligent Car Valuation",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  DESIGN SYSTEM — Obsidian & Champagne Gold
# ─────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&family=Outfit:wght@200;300;400;500;600&display=swap');

:root {
  --gold:        #c9a84c;
  --gold-light:  #e2c06a;
  --gold-dim:    #8a6e30;
  --gold-glow:   rgba(201,168,76,0.12);
  --gold-border: rgba(201,168,76,0.2);
  --obsidian:    #080810;
  --surface-1:   #0e0e18;
  --surface-2:   #13131f;
  --surface-3:   #1a1a28;
  --text-1:      #f2ece0;
  --text-2:      #a89880;
  --text-3:      #584f44;
  --text-4:      #2e2820;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(201,168,76,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 50% 30% at 90% 90%, rgba(80,40,140,0.04) 0%, transparent 50%),
        #080810 !important;
    min-height: 100vh;
}
[data-testid="stMain"] { background: transparent !important; }
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"],
[data-testid="stSidebar"] { display: none !important; }
.block-container { max-width: 800px !important; padding: 0 2rem 6rem !important; }

/* ── NAVBAR ── */
.navbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.8rem 0 1.2rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    margin-bottom: 0;
}
.nav-logo { font-family: 'Playfair Display', serif; font-size: 1.25rem; font-weight: 400; color: var(--text-1); letter-spacing: 0.06em; }
.nav-logo em { color: var(--gold); font-style: italic; }
.nav-pill { font-family: 'Outfit', sans-serif; font-size: 0.58rem; font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase; color: var(--gold); background: var(--gold-glow); border: 1px solid var(--gold-border); padding: 0.28rem 0.85rem; border-radius: 20px; }

/* ── HERO ── */
.hero { padding: 5rem 0 3rem; text-align: center; position: relative; }
.hero::before { content:''; position:absolute; top:40%; left:50%; transform:translate(-50%,-50%); width:500px; height:200px; background:radial-gradient(ellipse, rgba(201,168,76,0.05) 0%, transparent 70%); pointer-events:none; }
.hero-eyebrow { font-family:'Outfit',sans-serif; font-size:0.6rem; font-weight:500; letter-spacing:0.35em; text-transform:uppercase; color:var(--gold); margin-bottom:1.5rem; display:flex; align-items:center; justify-content:center; gap:0.8rem; }
.hero-eyebrow::before, .hero-eyebrow::after { content:''; width:28px; height:1px; background:var(--gold-dim); }
.hero-h1 { font-family:'Playfair Display',serif !important; font-size:clamp(2.8rem,7.5vw,4.8rem) !important; font-weight:300 !important; line-height:1.1 !important; letter-spacing:-0.01em !important; color:var(--text-1) !important; margin-bottom:0.2rem !important; }
.hero-h1 .accent { font-style:italic; background:linear-gradient(135deg,#e2c06a 0%,#c9a84c 50%,#a07830 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.hero-sub { font-family:'Outfit',sans-serif; font-size:0.88rem; font-weight:300; color:var(--text-3); letter-spacing:0.06em; margin-top:1.2rem; margin-bottom:3rem; }
.hero-orn { display:flex; align-items:center; justify-content:center; gap:0.6rem; }
.hero-orn-l { width:48px; height:1px; background:linear-gradient(90deg,transparent,var(--gold-dim)); }
.hero-orn-r { width:48px; height:1px; background:linear-gradient(90deg,var(--gold-dim),transparent); }
.hero-orn-d { font-size:0.38rem; color:var(--gold); opacity:0.6; }

/* ── STATS STRIP ── */
.stats-strip { display:grid; grid-template-columns:repeat(3,1fr); gap:1px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.05); border-radius:14px; overflow:hidden; margin:2.5rem 0 3rem; }
.stat-item { background:var(--surface-1); padding:1.2rem 1rem; text-align:center; }
.stat-num { font-family:'Playfair Display',serif; font-size:1.55rem; font-weight:400; color:var(--gold); letter-spacing:-0.02em; display:block; line-height:1; margin-bottom:0.3rem; }
.stat-label { font-family:'Outfit',sans-serif; font-size:0.56rem; font-weight:400; letter-spacing:0.18em; text-transform:uppercase; color:var(--text-3); }

/* ── FORM HEADER ── */
.form-header { display:flex; align-items:center; gap:1rem; margin-bottom:1.8rem; }
.form-header-line { flex:1; height:1px; background:rgba(255,255,255,0.05); }
.form-header-text { font-family:'Outfit',sans-serif; font-size:0.58rem; font-weight:500; letter-spacing:0.25em; text-transform:uppercase; color:var(--gold); white-space:nowrap; }

/* ── STEP BADGE ── */
.step-badge { display:inline-flex; align-items:center; gap:0.5rem; margin-bottom:0.7rem; }
.step-num { width:20px; height:20px; border-radius:50%; background:var(--gold-glow); border:1px solid var(--gold-border); font-family:'Outfit',sans-serif; font-size:0.58rem; font-weight:600; color:var(--gold); display:flex; align-items:center; justify-content:center; }
.step-text { font-family:'Outfit',sans-serif; font-size:0.6rem; font-weight:500; letter-spacing:0.15em; text-transform:uppercase; color:var(--text-2); }

/* ── WIDGETS ── */
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label {
    font-family:'Outfit',sans-serif !important; font-size:0.63rem !important; font-weight:400 !important;
    letter-spacing:0.15em !important; text-transform:uppercase !important; color:var(--text-3) !important; margin-bottom:0.25rem !important;
}
[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] input {
    background:var(--surface-2) !important; border:1px solid rgba(255,255,255,0.07) !important;
    border-radius:10px !important; color:var(--text-1) !important; font-family:'Outfit',sans-serif !important;
    font-size:0.88rem !important; font-weight:300 !important; transition:all 0.2s ease !important;
}
[data-testid="stSelectbox"] > div > div:hover { border-color:rgba(201,168,76,0.35) !important; background:var(--surface-3) !important; }
[data-testid="stNumberInput"] input:focus { border-color:rgba(201,168,76,0.5) !important; box-shadow:0 0 0 3px rgba(201,168,76,0.05) !important; background:var(--surface-3) !important; outline:none !important; }
[data-testid="stSelectbox"] svg { color:var(--gold-dim) !important; }
[data-testid="stNumberInput"] button { background:var(--surface-3) !important; border-color:rgba(255,255,255,0.07) !important; color:var(--text-2) !important; border-radius:8px !important; }
[data-testid="stNumberInput"] button:hover { border-color:var(--gold-border) !important; color:var(--gold) !important; }

/* ── CTA BUTTON ── */
[data-testid="stButton"] > button {
    width:100% !important;
    background:linear-gradient(135deg,#c9a84c 0%,#9a7828 50%,#c9a84c 100%) !important;
    background-size:200% 100% !important;
    color:#06060c !important; border:none !important; border-radius:12px !important;
    padding:1.05rem 2rem !important; font-family:'Outfit',sans-serif !important;
    font-size:0.75rem !important; font-weight:600 !important; letter-spacing:0.22em !important;
    text-transform:uppercase !important; cursor:pointer !important; transition:all 0.35s ease !important;
    box-shadow:0 0 40px rgba(201,168,76,0.12), 0 4px 20px rgba(0,0,0,0.5) !important;
    margin-top:1.5rem !important;
}
[data-testid="stButton"] > button:hover { transform:translateY(-3px) !important; box-shadow:0 0 60px rgba(201,168,76,0.25),0 10px 30px rgba(0,0,0,0.6) !important; background-position:right center !important; }
[data-testid="stButton"] > button:active { transform:translateY(-1px) !important; }

/* ── RESULT CARD ── */
.result-outer { position:relative; margin:2.5rem 0; border-radius:20px; padding:1px; background:linear-gradient(135deg,rgba(201,168,76,0.5) 0%,rgba(201,168,76,0.08) 40%,rgba(201,168,76,0.3) 100%); }
.result-inner { background:linear-gradient(160deg,#13131f 0%,#080810 100%); border-radius:19px; padding:3rem 2.5rem 2.5rem; text-align:center; position:relative; overflow:hidden; }
.result-inner::before { content:''; position:absolute; top:-80px; left:50%; transform:translateX(-50%); width:320px; height:180px; background:radial-gradient(ellipse,rgba(201,168,76,0.07) 0%,transparent 70%); pointer-events:none; }
.result-eyebrow { font-family:'Outfit',sans-serif; font-size:0.56rem; font-weight:500; letter-spacing:0.38em; text-transform:uppercase; color:var(--gold-dim); margin-bottom:1rem; }
.result-price { font-family:'Playfair Display',serif; font-size:clamp(3rem,9vw,5.5rem); font-weight:300; letter-spacing:-0.02em; line-height:1; color:var(--text-1); margin-bottom:0.3rem; }
.result-price .rupee { font-size:0.6em; vertical-align:0.15em; color:var(--gold); font-style:italic; }
.result-lakh { font-family:'Outfit',sans-serif; font-size:0.78rem; font-weight:300; color:var(--text-4); letter-spacing:0.12em; margin-bottom:2.5rem; }
.result-lakh span { color:var(--gold-dim); }
.pills-row { display:flex; justify-content:center; gap:0.6rem; flex-wrap:wrap; }
.pill { background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:0.6rem 1rem; text-align:center; min-width:75px; }
.pill-label { font-family:'Outfit',sans-serif; font-size:0.5rem; font-weight:500; letter-spacing:0.2em; text-transform:uppercase; color:var(--text-3); margin-bottom:0.28rem; }
.pill-value { font-family:'Playfair Display',serif; font-size:0.95rem; font-weight:400; color:var(--text-2); }

/* ── CHART HEADERS ── */
.chart-header { margin:2.5rem 0 0.6rem; display:flex; align-items:baseline; gap:0.8rem; }
.chart-title { font-family:'Playfair Display',serif; font-size:1.05rem; font-weight:400; font-style:italic; color:var(--text-2); }
.chart-sub { font-family:'Outfit',sans-serif; font-size:0.58rem; font-weight:400; letter-spacing:0.12em; color:var(--text-3); text-transform:uppercase; }

/* ── COMPLETE BANNER ── */
.complete-banner { display:flex; align-items:center; justify-content:center; gap:0.8rem; padding:0.9rem 1.5rem; margin:1.5rem 0; background:linear-gradient(135deg,rgba(201,168,76,0.05),rgba(201,168,76,0.02)); border:1px solid rgba(201,168,76,0.15); border-radius:12px; }
.complete-line { flex:1; height:1px; background:rgba(201,168,76,0.08); }
.complete-icon { color:var(--gold); font-size:0.6rem; opacity:0.7; }
.complete-text { font-family:'Outfit',sans-serif; font-size:0.6rem; font-weight:500; letter-spacing:0.28em; text-transform:uppercase; color:var(--gold); }

/* ── DOWNLOAD / SHARE ── */
[data-testid="stDownloadButton"] > button { background:rgba(201,168,76,0.08) !important; border:1px solid rgba(201,168,76,0.35) !important; color:#c9a84c !important; border-radius:10px !important; font-family:'Outfit',sans-serif !important; font-size:0.68rem !important; font-weight:500 !important; letter-spacing:0.12em !important; padding:0.65rem 1.4rem !important; transition:all 0.2s !important; margin-top:0 !important; box-shadow:0 0 20px rgba(201,168,76,0.08) !important; }
[data-testid="stDownloadButton"] > button:hover { background:rgba(201,168,76,0.15) !important; border-color:rgba(201,168,76,0.6) !important; color:#e2c06a !important; transform:translateY(-2px) !important; box-shadow:0 4px 20px rgba(201,168,76,0.15) !important; }
[data-testid="stTextArea"] textarea { background:rgba(255,255,255,0.04) !important; border:1px solid rgba(255,255,255,0.12) !important; border-radius:10px !important; color:#a89880 !important; font-family:'Outfit',sans-serif !important; font-size:0.78rem !important; font-weight:300 !important; resize:none !important; line-height:1.6 !important; padding:0.7rem 1rem !important; }
[data-testid="stTextArea"] label { display:none !important; }

/* ── FOOTER ── */
.footer-section { margin-top:5rem; padding-top:3rem; position:relative; text-align:center; }
.footer-top-border { position:absolute; top:0; left:50%; transform:translateX(-50%); width:100%; height:1px; background:linear-gradient(90deg,transparent 0%,rgba(255,255,255,0.05) 25%,rgba(201,168,76,0.5) 50%,rgba(255,255,255,0.05) 75%,transparent 100%); }
.footer-wordmark { font-family:'Playfair Display',serif; font-size:clamp(2rem,5vw,3.2rem); font-weight:300; letter-spacing:0.35em; text-transform:uppercase; color:rgba(242,236,224,0.08); display:block; margin-bottom:1.5rem; line-height:1; user-select:none; }
.footer-wordmark em { font-style:italic; color:rgba(201,168,76,0.15); }
.footer-mid { display:flex; align-items:center; justify-content:center; gap:0.8rem; margin-bottom:0.9rem; }
.footer-brand-sm { font-family:'Playfair Display',serif; font-size:0.9rem; font-weight:400; color:rgba(201,168,76,0.75); letter-spacing:0.1em; }
.footer-brand-sm em { font-style:italic; color:rgba(201,168,76,0.9); }
.footer-tag { font-family:'Outfit',sans-serif; font-size:0.56rem; letter-spacing:0.22em; text-transform:uppercase; color:rgba(201,168,76,0.45); }
.footer-sep-sm { color:rgba(255,255,255,0.25); font-size:0.4rem; }
.footer-meta { font-family:'Outfit',sans-serif; font-size:0.56rem; font-weight:300; letter-spacing:0.18em; text-transform:uppercase; color:#6a5e52; display:flex; align-items:center; justify-content:center; gap:0.9rem; flex-wrap:wrap; }
.footer-meta .name { color:#c9a84c; font-weight:500; letter-spacing:0.22em; }
.footer-meta .dot { color:#3a3028; opacity:1; }

/* ── MISC ── */
[data-testid="column"] { padding:0 0.35rem !important; }
::-webkit-scrollbar { width:3px; }
::-webkit-scrollbar-track { background:#080810; }
::-webkit-scrollbar-thumb { background:#1a1a28; border-radius:2px; }
[data-testid="stSpinner"] p { color:var(--gold) !important; font-family:'Outfit',sans-serif !important; font-size:0.78rem !important; letter-spacing:0.1em !important; }
</style>
""",
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────
#  LOAD ARTIFACTS
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    m = joblib.load("final_linear_model.pkl")
    c = joblib.load("model_columns.pkl")
    return m, c


@st.cache_data
def load_brand_model_map():
    try:
        return joblib.load("brand_model_map.pkl")
    except FileNotFoundError:
        return None


def indian_format(n):
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
    return ",".join(reversed(groups)) + "," + last3


model, columns = load_model()
brand_model_map = load_brand_model_map()

# ─────────────────────────────────────────────
#  NAVBAR
# ─────────────────────────────────────────────
st.markdown(
    """
<div class="navbar">
    <div class="nav-logo">Car<em>Val</em></div>
    <div class="nav-pill">India · 2025</div>
</div>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown(
    """
<div class="hero">
    <div class="hero-eyebrow">Intelligent Valuation Engine</div>
    <div class="hero-h1">Know the true<br><span class="accent">worth of your car</span></div>
    <div class="hero-sub">Machine-learning powered &nbsp;·&nbsp; 3,500+ real transactions &nbsp;·&nbsp; Indian market</div>
    <div class="hero-orn">
        <span class="hero-orn-l"></span>
        <span class="hero-orn-d">◆</span>
        <span class="hero-orn-r"></span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
#  STATS STRIP
# ─────────────────────────────────────────────
st.markdown(
    """
<div class="stats-strip">
    <div class="stat-item">
        <span class="stat-num">3,500+</span>
        <span class="stat-label">Transactions Analysed</span>
    </div>
    <div class="stat-item">
        <span class="stat-num">29</span>
        <span class="stat-label">Brands Covered</span>
    </div>
    <div class="stat-item">
        <span class="stat-num">~80%</span>
        <span class="stat-label">Accuracy</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
#  FORM
# ─────────────────────────────────────────────
st.markdown(
    """
<div class="form-header">
    <div class="form-header-line"></div>
    <div class="form-header-text">Vehicle Details</div>
    <div class="form-header-line"></div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="step-badge"><div class="step-num">1</div><div class="step-text">Identity</div></div>',
    unsafe_allow_html=True,
)
if brand_model_map:
    c1, c2 = st.columns(2)
    with c1:
        brand = st.selectbox("Brand", sorted(brand_model_map.keys()))
    with c2:
        car_model = st.selectbox("Model", sorted(brand_model_map.get(brand, [])))
else:
    brand, car_model = None, None

st.markdown(
    '<div class="step-badge" style="margin-top:1.2rem;"><div class="step-num">2</div><div class="step-text">Usage History</div></div>',
    unsafe_allow_html=True,
)
c3, c4 = st.columns(2)
with c3:
    year = st.number_input(
        "Year of Manufacture", min_value=1990, max_value=2025, value=2019
    )
with c4:
    km_driven = st.number_input(
        "Kilometres Driven", min_value=0, max_value=1000000, value=45000, step=1000
    )

st.markdown(
    '<div class="step-badge" style="margin-top:1.2rem;"><div class="step-num">3</div><div class="step-text">Specifications</div></div>',
    unsafe_allow_html=True,
)
c5, c6 = st.columns(2)
with c5:
    fuel_type = st.selectbox(
        "Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"]
    )
with c6:
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

st.markdown(
    '<div class="step-badge" style="margin-top:1.2rem;"><div class="step-num">4</div><div class="step-text">Ownership</div></div>',
    unsafe_allow_html=True,
)
c7, c8 = st.columns(2)
with c7:
    seller_type = st.selectbox(
        "Seller Type", ["Individual", "Dealer", "Trustmark Dealer"]
    )
with c8:
    owner = st.selectbox(
        "Owner History",
        [
            "First Owner",
            "Second Owner",
            "Third Owner",
            "Fourth & Above Owner",
            "Test Drive Car",
        ],
    )

# ─────────────────────────────────────────────
#  CTA
# ─────────────────────────────────────────────
predict_clicked = st.button("◈   Estimate My Car's Value", key="predict")

# ─────────────────────────────────────────────
#  PREDICTION
# ─────────────────────────────────────────────
if predict_clicked:
    if km_driven < 0:
        st.warning("KM Driven cannot be negative.")
        st.stop()

    with st.spinner("Analysing market data…"):
        time.sleep(0.9)

        input_data = dict.fromkeys(columns, 0)

        # ── Basic features ──
        input_data["Year"] = year
        input_data["KM_Driven"] = km_driven

        # ── Engineered features (must match Colab training exactly) ──
        car_age = max(2025 - year, 0)
        if "Car_Age" in input_data:
            input_data["Car_Age"] = car_age
        if "KM_Per_Year" in input_data:
            input_data["KM_Per_Year"] = km_driven / max(car_age, 1)
        if "Age_x_KM" in input_data:
            input_data["Age_x_KM"] = car_age * km_driven
        if "Is_New" in input_data:
            input_data["Is_New"] = 1 if car_age <= 3 else 0
        if "Is_High_KM" in input_data:
            input_data["Is_High_KM"] = 1 if km_driven > 100000 else 0

        brand_avg_map = {
            "Maruti": 450000,
            "Hyundai": 550000,
            "Honda": 650000,
            "Toyota": 800000,
            "Ford": 500000,
            "Volkswagen": 700000,
            "Skoda": 750000,
            "Renault": 400000,
            "Datsun": 280000,
            "Tata": 400000,
            "Mahindra": 600000,
            "BMW": 2000000,
            "Audi": 2500000,
            "Mercedes-Benz": 3000000,
            "Jeep": 1500000,
            "Kia": 900000,
            "MG": 1000000,
            "Nissan": 450000,
            "Fiat": 350000,
            "Chevrolet": 350000,
            "Volvo": 2000000,
            "Land": 3500000,
            "Mitsubishi": 800000,
            "Jaguar": 2500000,
            "Daewoo": 180000,
            "Force": 500000,
            "Isuzu": 700000,
            "OpelCorsa": 200000,
            "Ambassador": 150000,
        }
        fuel_avg_map = {
            "Petrol": 450000,
            "Diesel": 650000,
            "CNG": 300000,
            "LPG": 250000,
            "Electric": 800000,
        }
        if "Brand_Avg_Price" in input_data:
            input_data["Brand_Avg_Price"] = brand_avg_map.get(brand, 500000)
        if "Fuel_Avg_Price" in input_data:
            input_data["Fuel_Avg_Price"] = fuel_avg_map.get(fuel_type, 450000)

        # ── One-hot encoded categoricals ──
        mappings = [
            (f"Brand_{brand}", 1) if brand else None,
            (f"Model_{car_model}", 1) if car_model else None,
            (f"Fuel_{fuel_type}", 1),
            ("Transmission_Manual", 1) if transmission == "Manual" else None,
            (f"Seller_Type_{seller_type}", 1),
            (f"Owner_{owner}", 1),
        ]
        for item in mappings:
            if item and item[0] in input_data:
                input_data[item[0]] = item[1]

        try:
            predicted_price = max(model.predict(pd.DataFrame([input_data]))[0], 0)
            fmt = indian_format(predicted_price)
            lakh = f"{predicted_price/100000:.2f} Lakh"

            # RESULT CARD
            st.markdown(
                f"""
            <div class="result-outer">
              <div class="result-inner">
                <div class="result-eyebrow">Estimated Market Value</div>
                <div class="result-price"><span class="rupee">₹</span>{fmt}</div>
                <div class="result-lakh">≈ <span>{lakh}</span></div>
                <div class="pills-row">
                    <div class="pill"><div class="pill-label">Brand</div><div class="pill-value">{brand or '—'}</div></div>
                    <div class="pill"><div class="pill-label">Year</div><div class="pill-value">{year}</div></div>
                    <div class="pill"><div class="pill-label">KM</div><div class="pill-value">{km_driven:,}</div></div>
                    <div class="pill"><div class="pill-label">Fuel</div><div class="pill-value">{fuel_type}</div></div>
                    <div class="pill"><div class="pill-label">Gear</div><div class="pill-value">{transmission}</div></div>
                </div>
              </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # BENCHMARK CHART
            fig = go.Figure()
            for label, val, color in [
                ("Your Car", predicted_price, "#c9a84c"),
                ("Mkt Avg", 550000, "#3a3028"),
                ("Min Range", 80000, "#252020"),
                ("Max Range", 1500000, "#1e1a18"),
            ]:
                fig.add_trace(
                    go.Bar(
                        name=label,
                        x=[label],
                        y=[val],
                        marker_color=color,
                        marker_line_width=0,
                        text=f"₹{val/100000:.1f}L",
                        textposition="outside",
                        textfont=dict(color="#584f44", size=10, family="Outfit"),
                    )
                )
            fig.update_layout(
                barmode="group",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Outfit", color="#584f44", size=10),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    font=dict(size=9, color="#584f44"),
                    bgcolor="rgba(0,0,0,0)",
                ),
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.03)",
                    zeroline=False,
                    tickfont=dict(size=9),
                    tickformat=",.0f",
                    tickprefix="₹",
                ),
                margin=dict(l=10, r=10, t=44, b=10),
                height=290,
                bargap=0.35,
            )
            st.markdown(
                '<div class="chart-header"><span class="chart-title">Price Benchmark</span><span class="chart-sub">vs Indian Market</span></div>',
                unsafe_allow_html=True,
            )
            st.plotly_chart(
                fig, use_container_width=True, config={"displayModeBar": False}
            )

            # KM TREND CHART
            km_range = [
                max(0, km_driven - 40000),
                max(0, km_driven - 20000),
                km_driven,
                km_driven + 20000,
                km_driven + 40000,
            ]
            trend_prices = []
            for k in km_range:
                row = dict.fromkeys(columns, 0)
                row["Year"] = year
                row["KM_Driven"] = k
                ca = max(2025 - year, 0)
                if "Car_Age" in row:
                    row["Car_Age"] = ca
                if "KM_Per_Year" in row:
                    row["KM_Per_Year"] = k / max(ca, 1)
                if "Age_x_KM" in row:
                    row["Age_x_KM"] = ca * k
                if "Is_New" in row:
                    row["Is_New"] = 1 if ca <= 3 else 0
                if "Is_High_KM" in row:
                    row["Is_High_KM"] = 1 if k > 100000 else 0
                if "Brand_Avg_Price" in row:
                    row["Brand_Avg_Price"] = brand_avg_map.get(brand, 500000)
                if "Fuel_Avg_Price" in row:
                    row["Fuel_Avg_Price"] = fuel_avg_map.get(fuel_type, 450000)
                for item in mappings:
                    if item and item[0] in row:
                        row[item[0]] = item[1]
                trend_prices.append(max(model.predict(pd.DataFrame([row]))[0], 0))

            fig2 = go.Figure()
            fig2.add_trace(
                go.Scatter(
                    x=km_range,
                    y=trend_prices,
                    mode="lines",
                    line=dict(color="rgba(201,168,76,0.25)", width=2),
                    fill="tozeroy",
                    fillcolor="rgba(201,168,76,0.03)",
                    showlegend=False,
                    hovertemplate="%{x:,} km → ₹%{y:,.0f}<extra></extra>",
                )
            )
            fig2.add_trace(
                go.Scatter(
                    x=km_range,
                    y=trend_prices,
                    mode="markers",
                    marker=dict(
                        color="rgba(201,168,76,0.45)",
                        size=5,
                        line=dict(color="#080810", width=1),
                    ),
                    showlegend=False,
                )
            )
            fig2.add_trace(
                go.Scatter(
                    x=[km_driven],
                    y=[predicted_price],
                    mode="markers",
                    marker=dict(
                        color="#c9a84c", size=14, line=dict(color="#080810", width=2.5)
                    ),
                    showlegend=False,
                    hovertemplate=f"Your Car: ₹{fmt}<extra></extra>",
                )
            )
            fig2.add_vline(
                x=km_driven,
                line_width=1,
                line_dash="dot",
                line_color="rgba(201,168,76,0.15)",
            )
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Outfit", color="#584f44", size=10),
                showlegend=False,
                xaxis=dict(
                    title=dict(text="Kilometres Driven", font=dict(size=10)),
                    showgrid=False,
                    zeroline=False,
                    tickfont=dict(size=9),
                ),
                yaxis=dict(
                    title=dict(text="Estimated Price", font=dict(size=10)),
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.03)",
                    zeroline=False,
                    tickfont=dict(size=9),
                    tickformat=",.0f",
                    tickprefix="₹",
                ),
                margin=dict(l=10, r=10, t=20, b=10),
                height=260,
                hovermode="x unified",
            )
            st.markdown(
                '<div class="chart-header"><span class="chart-title">Depreciation Curve</span><span class="chart-sub">Price vs KM Driven</span></div>',
                unsafe_allow_html=True,
            )
            st.plotly_chart(
                fig2, use_container_width=True, config={"displayModeBar": False}
            )

            # COMPLETE BANNER
            st.markdown(
                """
            <div class="complete-banner">
                <span class="complete-line"></span>
                <span class="complete-icon">◈</span>
                <span class="complete-text">Valuation Complete</span>
                <span class="complete-icon">◈</span>
                <span class="complete-line"></span>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # DOWNLOAD + SHARE
            result_df = pd.DataFrame(
                {
                    "Brand": [brand or "—"],
                    "Model": [car_model or "—"],
                    "Year": [year],
                    "KM Driven": [km_driven],
                    "Fuel": [fuel_type],
                    "Transmission": [transmission],
                    "Seller Type": [seller_type],
                    "Owner": [owner],
                    "Estimated Price (₹)": [indian_format(predicted_price)],
                }
            )
            col_dl, col_share = st.columns([1, 2])
            with col_dl:
                st.download_button(
                    "↓  Download Report",
                    result_df.to_csv(index=False),
                    "carval_report.csv",
                    mime="text/csv",
                )
            with col_share:
                st.text_area(
                    "share",
                    value=f"{car_model or ''} · {year} · {km_driven:,} km · {fuel_type} — Valued at ₹{indian_format(predicted_price)} by CarVal AI",
                    height=72,
                )

        except Exception as e:
            st.error(f"Prediction error: {e}")

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown(
    """
<div class="footer-section">
    <div class="footer-top-border"></div>
    <span class="footer-wordmark">Car<em>Val</em></span>
    <div class="footer-mid">
        <span class="footer-brand-sm">Car<em>Val</em></span>
        <span class="footer-sep-sm">◆</span>
        <span class="footer-tag">Intelligent Valuation</span>
    </div>
    <div class="footer-meta">
        <span>Built with Machine Learning</span>
        <span class="dot">·</span>
        <span>Indian Used Car Market</span>
        <span class="dot">·</span>
        <span>Crafted by <span class="name">Sudharshan</span></span>
        <span class="dot">·</span>
        <span>© 2025</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)
