# 🏙️ Mysore-Banglore House Price Price Prediction

This project is a **machine learning-powered web app** that predicts **house prices per square foot** and **total apartment cost** based on location, area, and BHK configuration in two Indian cities — **Mysore** and **Bangalore**.

Built with:
- 🐍 Python
- 🧠 Scikit-learn (ML pipeline)
- 🌐 Streamlit (interactive UI)
- 🕷️ Playwright (web scraping)
- 📊 Pandas, PyArrow (data processing)

---

## 🔍 Features

### ✅ Web App (Streamlit UI)
- Choose a city (Bangalore or Mysore)
- Select locality from real scraped data
- Enter apartment size (BHK & area in sqft)
- Predict:
  - 💸 Price per square foot
  - 🏠 Total price
- 💡 Smart Locality Suggestions:
  - Suggests nearby localities with more space for similar price (value-for-money)
  - Interactive bar chart comparing area gain

### 🕸️ Web Scraping with Playwright
- Scrapes apartment listings from MagicBricks.com
- Extracts: Title, Price, Area, BHK, Locality
- Saved as structured JSON → cleaned into Parquet

### 🧠 Machine Learning Pipeline
- Preprocessing:
  - OneHotEncoder for localities
  - Scaler for numeric columns
- Model: `Ridge()` regression for price prediction
- Trained separately for Bangalore and Mysore

---

## 🧪 Project Structure

```
bangalore-price-predictor/
├── data/
│   ├── raw/
│   │   └── magicbricks_blr.json
│   │   └── magicbricks_mysore.json
│   └── processed/
│       └── magicbricks_blr.parquet
│       └── magicbricks_mysore.parquet
├── models/
│   └── price_model.joblib
│   └── price_model_mysore.joblib
├── src/
│   ├── app/
│   │   └── streamlit_app.py     👈 Main UI
│   ├── pipelines/
│   │   └── build_dataset.py     👈 Raw JSON ➝ Cleaned Parquet
│   │   └── train.py             👈 Train model
│   ├── scraping/
│   │   ├── magicbricks_scraper.py       👈 Reusable scraper
│   │   └── spiders/
│   │       └── magicbricks_blr.py       👈 Run & save for Bangalore
│   │       └── magicbricks_mysore.py    👈 Run & save for Mysore
│   └── utils.py                  👈 Smart locality suggestions
```

---

## 🚀 How to Run Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Scrape data

```bash
python src/scraping/spiders/magicbricks_blr.py 20
python src/scraping/spiders/magicbricks_mysore.py 20
```

### 3. Clean and process

```bash
python src/pipelines/build_dataset.py data/raw/magicbricks_blr.json data/processed/magicbricks_blr.parquet
python src/pipelines/build_dataset.py data/raw/magicbricks_mysore.json data/processed/magicbricks_mysore.parquet
```

### 4. Train model

```bash
python src/training/train.py data/processed/magicbricks_blr.parquet models/price_model.joblib
python src/training/train.py data/processed/magicbricks_mysore.parquet models/price_model_mysore.joblib
```

### 5. Launch app

```bash
streamlit run src/app/streamlit_app.py
```

---

## 👨‍💼 Why This Project?
- Scraped real Indian property data
- Trained separate ML models for different cities
- Made interactive & useful predictions
- Shows smart suggestions using clustering
- Recruiters can test this like a working product

---

## 📩 Contact

📧 **Karthik P** – [LinkedIn](https://linkedin.com/in/karthik-prasad-ai) | [Email](mailto:karthikprasad2206@gmail.com)