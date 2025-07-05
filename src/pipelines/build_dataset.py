import re
import sys
import json
import pandas as pd
from pathlib import Path


PRICE_PATTERN = re.compile(r"([\d.]+)\s*(Cr|Lac)?", re.I)
AREA_PATTERN = re.compile(r"([\d,.]+)\s*sqft", re.I)
BHK_PATTERN = re.compile(r"(\d)\s*BHK")


def parse_price(text: str) -> float | None:
    if not text:
        return None
    match = PRICE_PATTERN.search(text)
    if not match:
        return None
    num, unit = match.groups()
    value = float(num.replace(",", ""))
    if unit and unit.lower().startswith("c"):
        value *= 1e7
    elif unit and unit.lower().startswith("l"):
        value *= 1e5
    return value



def parse_area(text: str) -> float:
    if not text:
        return None
    num = AREA_PATTERN.search(text).group(1)
    return float(num.replace(",", ""))


def parse_bhk(text: str) -> int | None:
    m = BHK_PATTERN.search(text or "")
    return int(m.group(1)) if m else None


def clean(raw_json: Path) -> pd.DataFrame:
    with open(raw_json, encoding="utf‑8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df["price"] = df["price_text"].apply(parse_price)
    df["area_sqft"] = df["area_text"].apply(parse_area)
    df["bhk"] = df["title"].apply(parse_bhk)
    df["locality"] = (
        df["title"]
        .str.split(" in ", n=1)
        .str[-1]
        .str.split(",", n=1)
        .str[0]
        .str.strip()
    )
    df = df[["title", "locality", "bhk", "area_sqft", "price",]]
    df.dropna(subset=["area_sqft", "price"], inplace=True)
    df["price_psf"] = df["price"] / df["area_sqft"]
    return df


def main():
    if len(sys.argv) != 3:
        print("Usage: python -m pipelines.build_dataset <raw.json> <out.parquet>")
        sys.exit(1)
    src, dest = Path(sys.argv[1]), Path(sys.argv[2])
    dest.parent.mkdir(parents=True, exist_ok=True)
    df = clean(src)
    df.to_parquet(dest, index=False)
    print(f"Saved {len(df)} rows → {dest}")


if __name__ == "__main__":
    main()
