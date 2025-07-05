import streamlit as st
import joblib
import pandas as pd
from pathlib import Path
from src.utils import value_for_money_suggestions

# ── Load model and data paths ─────────────────────────────
MODELS = {
    "Bangalore": Path("models/price_model.joblib"),
    "Mysore": Path("models/price_model_mysore.joblib")
}

DATASETS = {
    "Bangalore": Path("data/processed/magicbricks_blr.parquet"),
    "Mysore": Path("data/processed/magicbricks_mysore.parquet")
}

# ── UI config ─────────────────────────────────────────────
st.set_page_config("🏠 House Price Predictor", layout="centered")
st.title("🏙️ Multi‑City House Price Predictor")

# ── City selection ───────────────────────────────────────
city = st.selectbox("🏙️ City", list(MODELS.keys()))
model = joblib.load(MODELS[city])
df = pd.read_parquet(DATASETS[city])
df["price_psf"] = df["price"] / df["area_sqft"]
df["total_price"] = df["price"] * df["area_sqft"]

# ── Locality from encoder ────────────────────────────────
localities = list(model.named_steps["preprocessor"]
    .transformers_[0][1].categories_[0])
localities.sort()

# ── User inputs ──────────────────────────────────────────
locality = st.selectbox("📍 Locality", localities)
bhk = st.number_input("🛏️ BHK", min_value=1, max_value=10, value=2)
area = st.number_input("📐 Area (sq ft)", min_value=200, max_value=10000, value=1000)

# ── Sidebar tweaks ───────────────────────────────────────
st.sidebar.header("🔧 Suggestion Settings")
tolerance = st.sidebar.slider("Price tolerance ± %", 5, 30, 10)
top_k     = st.sidebar.slider("Max suggestions", 3, 10, 5)

# ── Predict ──────────────────────────────────────────────
if st.button("🔮 Predict"):
    X = pd.DataFrame([{"locality": locality, "bhk": bhk, "area_sqft": area}])
    price_psf = model.predict(X)[0]
    total     = price_psf * area

    st.success(f"📊 **Estimated ₹/sq ft:** ₹ {price_psf:,.0f}")
    st.success(f"💰 **Estimated Total Price:** ₹ {total:,.0f}")

    sugg_raw = value_for_money_suggestions(
        df, locality,
        price_tolerance=tolerance / 100,
        top_k=top_k
    )

    st.markdown("### 💡 Value‑for‑Money Localities")
    if sugg_raw.empty:
        st.info("No better-area suggestions found.")
    else:
        sugg = sugg_raw.rename(columns={
            "locality": "Recommended Locality",
            "median_price_psf": "Median ₹/sq ft",
            "median_area": "Median Area (sq ft)",
            "area_gain": "Extra Area vs. current (sq ft)"
        })
        st.dataframe(sugg, hide_index=True)
        
