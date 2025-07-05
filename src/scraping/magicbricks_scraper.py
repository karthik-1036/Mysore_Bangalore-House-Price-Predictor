# src/scraping/magicbricks_scraper.py
from __future__ import annotations
import json
import re
from time import sleep
from typing import List, Dict
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

TITLE_SEL      = "h2.mb-srp__card--title"
PRICE_SEL      = "div.mb-srp__card__price--amount"
AREA_SEL       = 'div[data-summary="super-area"] .mb-srp__card__summary--value'
LOCATION_SEL   = "div.mb-srp__card--title"      # locality can be parsed from title
CARD_SEL       = "div.mb-srp__card"

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

def parse_float(text: str) -> float | None:
    if not text:
        return None
    num = re.sub(r"[^\d.]", "", text)
    try:
        return float(num)
    except ValueError:
        return None



def scrape_magicbricks(max_pages: int = 10, city_name: str = "Bangalore") -> List[Dict]:
    results: List[Dict] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=UA)
        page = context.new_page()

        for pg in range(1, max_pages + 1):
            url = (
                "https://www.magicbricks.com/property-for-sale/"
                "residential-real-estate?"
                "proptype=Multistorey-Apartment,Builder-Floor-Apartment,"
                "Penthouse,Studio-Apartment"
                f"&cityName={city_name}&page={pg}"
            )
            print(f"🔎  Page {pg}: {url}")
            try:
                page.goto(url, timeout=60000)
                page.wait_for_selector(CARD_SEL, timeout=15000)
            except PlaywrightTimeout:
                print("⏰  Timeout – no cards found, skipping page")
                continue

            if page.locator(CARD_SEL).count() < 25:
                page.mouse.wheel(0, 3000)
                sleep(2)

            for card in page.locator(CARD_SEL).all():
                try:
                    title = card.locator(TITLE_SEL).inner_text().strip()
                    price_txt = card.locator(PRICE_SEL).inner_text().strip()
                    area_txt  = card.locator(AREA_SEL).inner_text().strip()

                    results.append(
                        {
                            "title": title,
                            "bhk": re.search(r"(\d)\s*BHK", title).group(1) if re.search(r"(\d)\s*BHK", title) else None,
                            "location": title.split(" in ", 1)[-1].split(",")[0].strip(),
                            "price_text": price_txt,
                            "area_text": area_txt,
                        }
                    )
                except Exception:
                    continue

        browser.close()
    return results

