#!/bin/bash
scrapy runspider src/scraping/spiders/magicbricks_blr.py -o data/raw/magicbricks_blr.json -s FEED_EXPORT_ENCODING=utf-8
