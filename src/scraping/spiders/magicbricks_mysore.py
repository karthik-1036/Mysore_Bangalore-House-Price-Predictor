
import sys
import json
from pathlib import Path
from src.scraping.magicbricks_scraper import scrape_magicbricks

if __name__ == "__main__":
    pages = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    listings = scrape_magicbricks(max_pages=pages, city_name="Mysore")

    output_path = Path("data/raw/magicbricks_mysore.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(listings, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(listings)} rows → {output_path}")
