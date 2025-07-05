import sys
import joblib
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error

def load_data(parquet_path: Path) -> pd.DataFrame:
    return pd.read_parquet(parquet_path)

def train_model(df: pd.DataFrame):
    X = df[["locality", "bhk", "area_sqft"]]
    y = df["price_psf"]

    categorical_features = ["locality"]
    numeric_features = ["bhk", "area_sqft"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ],
        remainder="passthrough",  # pass numeric features through unchanged
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(n_estimators=100, random_state=42)),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Mean Absolute Error: {mae:.2f}")

    return model

def main():
    if len(sys.argv) != 3:
        print("Usage: python -m src.models.train_model <input.parquet> <output.joblib>")
        sys.exit(1)
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    df = load_data(input_path)
    model = train_model(df)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)
    print(f"Model saved → {output_path}")

if __name__ == "__main__":
    main()
