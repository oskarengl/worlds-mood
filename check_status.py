#!/usr/bin/env python3
"""
Quick status check for the World News Globe pipeline
"""

import json
from pathlib import Path
from datetime import datetime

def check_status():
    print("\n" + "="*60)
    print("WORLD NEWS GLOBE - STATUS CHECK")
    print("="*60 + "\n")
    
    # Check if country_data.json exists
    json_file = Path("country_data.json")
    if not json_file.exists():
        print("[X] country_data.json NOT FOUND")
        print("   Run: python worldsmood.py")
        return
    
    print("[OK] country_data.json found")
    
    # Load and analyze the data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    metadata = data.get('metadata', {})
    countries = data.get('countries', {})
    
    print(f"\nData Statistics:")
    print(f"   Generated: {metadata.get('generated_at', 'Unknown')}")
    print(f"   Countries: {len(countries)}")
    print(f"   Total Articles: {metadata.get('total_articles', 0)}")
    
    print(f"\nCountries with data:")
    for country, info in sorted(countries.items()):
        word = info['prevalent_word']
        pct = info['word_percentage']
        articles = info['num_articles']
        print(f"   - {country:20s} -> \"{word}\" ({pct:.1f}% of {articles} articles)")
    
    # Check HTML file
    html_file = Path("minimalist_globe.html")
    if html_file.exists():
        print(f"\n[OK] minimalist_globe.html found")
    else:
        print(f"\n[X] minimalist_globe.html NOT FOUND")
    
    # Check CSV file
    csv_files = list(Path(".").glob("prevalent_words_rss_*.csv"))
    if csv_files:
        latest_csv = max(csv_files, key=lambda p: p.stat().st_mtime)
        print(f"\n[OK] Latest CSV: {latest_csv.name}")
    
    print("\n" + "="*60)
    print("To view the globe:")
    print("   1. Start server: python -m http.server 8000")
    print("   2. Open: http://localhost:8000/minimalist_globe.html")
    print("="*60 + "\n")

if __name__ == "__main__":
    check_status()

