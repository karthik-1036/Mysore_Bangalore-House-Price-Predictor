from __future__ import annotations
import pandas as pd
from sklearn.cluster import KMeans

def value_for_money_suggestions(
    df: pd.DataFrame,
    target_locality: str,
    price_tolerance: float = 0.10,
    top_k: int = 5,
    k_clusters: int = 4,
):
    """
    Recommend up to `top_k` localities that deliver more median sqft
    for roughly the same ₹/sqft as `target_locality`, using K‑Means clusters.

    Parameters
    ----------
    df : DataFrame with cols ["locality", "price", "area_sqft"]
    target_locality : locality chosen by user
    price_tolerance : ± band around target median price_psf (if cluster fails)
    top_k : max suggestions
    k_clusters : number of clusters for K‑Means
    """
    # Ensure price_psf is calculated correctly
    df["price_psf"] = df["price"] / df["area_sqft"]

    # per‑locality medians
    g = (
        df.groupby("locality")
          .agg(
              med_price_psf=("price_psf", "median"),
              med_area=("area_sqft", "median")
          )
          .reset_index()
    )

    if target_locality not in g["locality"].values:
        return pd.DataFrame()  # unknown locality

    # K‑Means clustering on (price_psf, area)
    km = KMeans(n_clusters=min(k_clusters, len(g)), random_state=42, n_init="auto")
    g[["c_price", "c_area"]] = g[["med_price_psf", "med_area"]]
    g["cluster"] = km.fit_predict(g[["c_price", "c_area"]])

    target_cluster = g.loc[g["locality"] == target_locality, "cluster"].iloc[0]
    cand = g[g["cluster"] == target_cluster].copy()

    # Fallback to ± tolerance if needed
    if len(cand) < 3:
        tgt_price = g.loc[g["locality"] == target_locality, "med_price_psf"].iloc[0]
        lo, hi = tgt_price * (1 - price_tolerance), tgt_price * (1 + price_tolerance)
        cand = g[(g["med_price_psf"] >= lo) & (g["med_price_psf"] <= hi)].copy()

    # Only recommend localities with better (larger) area
    tgt_area = g.loc[g["locality"] == target_locality, "med_area"].iloc[0]
    cand = cand[cand["med_area"] > tgt_area]
    cand["area_gain"] = cand["med_area"] - tgt_area

    return (
        cand.sort_values("area_gain", ascending=False)
            .head(top_k)
            .reset_index(drop=True)
            .loc[:, ["locality", "med_price_psf", "med_area", "area_gain"]]
            .rename(columns={
                "locality": "Recommended Locality",
                "med_price_psf": "Median ₹/sq ft",
                "med_area": "Median Area (sq ft)",
                "area_gain": "Extra Area vs. current (sq ft)",
            })
    )
