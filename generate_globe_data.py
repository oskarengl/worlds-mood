# -*- coding: utf-8 -*-
"""
Data Generator for World's Mood Interactive Globe
Converts Python analysis results to JSON format for the website
"""

import json
import pandas as pd
from datetime import datetime
import os

def generate_globe_data():
    """Generate JSON data for the interactive globe"""
    
    # Try to load the latest CSV file
    csv_files = [f for f in os.listdir('.') if f.startswith('prevalent_words_rss_') and f.endswith('.csv')]
    
    if not csv_files:
        print("No CSV data found. Please run worldsmood.py first.")
        return None
    
    # Get the most recent CSV file
    latest_csv = max(csv_files, key=os.path.getctime)
    print(f"Loading data from: {latest_csv}")
    
    try:
        df = pd.read_csv(latest_csv)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None
    
    # Convert DataFrame to dictionary format
    country_data = {}
    
    for _, row in df.iterrows():
        country_name = row['country_name']
        country_data[country_name] = {
            'prevalent_word': row['prevalent_word'],
            'word_percentage': float(row['word_percentage']),
            'prevalence_score': float(row['prevalence_score']),
            'num_articles': int(row['num_articles']),
            'week': row.get('week', datetime.now().strftime('%Y-W%U'))
        }
    
    # Add metadata
    globe_data = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_countries': len(country_data),
            'total_articles': int(df['num_articles'].sum()),
            'data_source': latest_csv
        },
        'countries': country_data
    }
    
    # Save to JSON file
    output_file = 'country_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(globe_data, f, indent=2, ensure_ascii=False)
    
    print(f"Globe data saved to: {output_file}")
    print(f"Countries processed: {len(country_data)}")
    
    return globe_data

def create_globe_coordinates():
    """Create country coordinates for the 3D globe"""
    
    # Simplified country coordinates (latitude, longitude)
    country_coords = {
        'United States': {'lat': 39.8283, 'lon': -98.5795},
        'Canada': {'lat': 56.1304, 'lon': -106.3468},
        'United Kingdom': {'lat': 55.3781, 'lon': -3.4360},
        'Germany': {'lat': 51.1657, 'lon': 10.4515},
        'France': {'lat': 46.2276, 'lon': 2.2137},
        'Japan': {'lat': 36.2048, 'lon': 138.2529},
        'Australia': {'lat': -25.2744, 'lon': 133.7751},
        'Brazil': {'lat': -14.2350, 'lon': -51.9253},
        'India': {'lat': 20.5937, 'lon': 78.9629},
        'South Korea': {'lat': 35.9078, 'lon': 127.7669}
    }
    
    # Convert to 3D coordinates on sphere
    coords_3d = {}
    for country, coords in country_coords.items():
        lat_rad = coords['lat'] * 3.14159 / 180
        lon_rad = coords['lon'] * 3.14159 / 180
        
        x = 1.1 * (lat_rad / 90) * (lon_rad / 180)
        y = 1.1 * (lat_rad / 90)
        z = 1.1 * (lon_rad / 180)
        
        coords_3d[country] = {'x': x, 'y': y, 'z': z}
    
    return coords_3d

if __name__ == "__main__":
    print("Generating globe data...")
    data = generate_globe_data()
    
    if data:
        print("\nSample data:")
        for country, info in list(data['countries'].items())[:3]:
            print(f"  {country}: {info['prevalent_word']} ({info['word_percentage']}%)")
        
        print(f"\nGlobe data ready! Open index.html in your browser to view the interactive globe.")
        import sys
        sys.exit(0)  # Explicit success exit
    else:
        print("Failed to generate globe data.")
        import sys
        sys.exit(1)  # Explicit failure exit
