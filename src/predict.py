# src/predict.py

import sys
import joblib
import pandas as pd
from pathlib import Path

def load_model(model_path: Path):
    return joblib.load(model_path)

def predict(model, locality: str, bhk: int, area_sqft: float):
    input_df = pd.DataFrame([{
        "locality": locality,
        "bhk": bhk,
        "area_sqft": area_sqft
    }])
    
    price_psf = model.predict(input_df)[0]
    total_price = price_psf * area_sqft
    return price_psf, total_price

def main():
    if len(sys.argv) != 5:
        print("Usage: python src/predict.py <model.joblib> <locality> <bhk> <area_sqft>")
        sys.exit(1)

    model_path = Path(sys.argv[1])
    locality = sys.argv[2]
    bhk = int(sys.argv[3])
    area_sqft = float(sys.argv[4])

    model = load_model(model_path)
    price_psf, total_price = predict(model, locality, bhk, area_sqft)

    print(f"📊 Predicted Price per sqft: ₹{price_psf:.2f}")
    print(f"💰 Estimated Total Price: ₹{total_price:,.2f}")

if __name__ == "__main__":
    main()
