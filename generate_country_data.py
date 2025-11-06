# -*- coding: utf-8 -*-
"""
Generate enhanced country data with sentiment analysis
Combines prevalent words with sentiment statistics for visualization
"""

import pandas as pd
import json
from datetime import datetime

def main():
    print("="*80)
    print("GENERATING ENHANCED COUNTRY DATA")
    print("="*80)
    print()
    
    # Load CSV data
    print("Loading prevalent words data...")
    import glob
    csv_files = glob.glob('prevalent_words_gdelt_*.csv')
    if not csv_files:
        print("[ERROR] No CSV files found!")
        return
    
    csv_file = sorted(csv_files)[-1]  # Get most recent
    print(f"  Using: {csv_file}")
    df = pd.read_csv(csv_file)
    print(f"  Loaded {len(df)} countries\n")
    
    # Load sentiment analysis
    print("Loading sentiment analysis...")
    with open('sentiment_analysis.json', 'r', encoding='utf-8') as f:
        sentiment_data = json.load(f)
    
    global_stats = sentiment_data['global_stats']
    country_stats = sentiment_data['country_stats']
    print(f"  Loaded sentiment data for {len(country_stats)} countries\n")
    
    # Calculate average bad news percentage (for scaling)
    avg_bad_pct = global_stats['bad_percentage']
    print(f"Global bad news percentage: {avg_bad_pct:.2f}%")
    print(f"This will be mapped to 50% grey (middle point)")
    print(f"0% bad news -> white")
    print(f"{avg_bad_pct*2:.2f}% bad news -> black")
    print()
    
    # Minimum articles threshold for statistical significance
    MIN_ARTICLES = 10
    print(f"Minimum articles threshold: {MIN_ARTICLES}")
    print(f"Countries with fewer articles will be shown as 50% grey (low confidence)")
    print()
    
    # Convert to dictionary format with sentiment data
    country_data = {}
    countries_with_sentiment = 0
    countries_low_confidence = 0
    
    for _, row in df.iterrows():
        country_name = row['country_name']
        
        # Base data from CSV
        country_info = {
            'prevalent_word': row['prevalent_word'],
            'word_percentage': float(row['word_percentage']),
            'word_frequency': int(row['word_frequency']),
            'prevalence_score': float(row['prevalence_score']),
            'num_articles': int(row['num_articles']),
            'timeframe': row['timeframe']
        }
        
        # Add sentiment data if available
        if country_name in country_stats:
            stats = country_stats[country_name]
            country_info['sentiment'] = {
                'good': stats['good'],
                'bad': stats['bad'],
                'neutral': stats['neutral'],
                'good_pct': round(stats['good_pct'], 2),
                'bad_pct': round(stats['bad_pct'], 2),
                'neutral_pct': round(stats['neutral_pct'], 2)
            }
            
            # Calculate grey value based on SENTIMENT BALANCE (Good% - Bad%)
            # If less than MIN_ARTICLES, use 50% grey (low confidence)
            if stats['total'] < MIN_ARTICLES:
                country_info['grey_value'] = 0.5  # 50% grey (low confidence)
                country_info['low_confidence'] = True
                countries_low_confidence += 1
            else:
                # Use net sentiment: Good% - Bad%
                # This ranges from -100 (all bad) to +100 (all good)
                # Neutral news naturally balances out
                # 
                # Grey value mapping with exponential curve for more contrast:
                # -100 (all bad, no good) → 1.0 (black)
                # 0 (balanced or all neutral) → 0.5 (grey)
                # +100 (all good, no bad) → 0.0 (white)
                
                good_pct = stats['good_pct']
                bad_pct = stats['bad_pct']
                net_sentiment = good_pct - bad_pct  # Range: -100 to +100
                
                # Apply aggressive scaling for visible contrast
                # Most countries have small net sentiments (5-25%)
                # Multiply by 3 to expand the range, then clamp
                # This makes even small differences very visible
                scaled_sentiment = net_sentiment * 3
                
                # Convert to grey value (0=white, 1=black)
                # Map: +150 -> 0.0 (white), 0 -> 0.5 (grey), -150 -> 1.0 (black)
                grey_value = 0.5 - (scaled_sentiment / 300)
                
                # Clamp to valid range [0, 1]
                grey_value = max(0.0, min(1.0, grey_value))
                
                country_info['grey_value'] = round(grey_value, 3)
                country_info['low_confidence'] = False
                countries_with_sentiment += 1
        else:
            # No sentiment data - use 50% grey
            country_info['grey_value'] = 0.5
            country_info['low_confidence'] = True
            country_info['sentiment'] = None
            countries_low_confidence += 1
        
        country_data[country_name] = country_info
    
    print(f"Countries with full sentiment data: {countries_with_sentiment}")
    print(f"Countries with low confidence (< {MIN_ARTICLES} articles): {countries_low_confidence}")
    print()
    
    # Create output with metadata
    output = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_countries': len(country_data),
            'data_source': 'GDELT Project',
            'min_articles_threshold': MIN_ARTICLES,
            'global_sentiment': {
                'total_headlines': global_stats['total_headlines'],
                'good_percentage': global_stats['good_percentage'],
                'bad_percentage': global_stats['bad_percentage'],
                'neutral_percentage': global_stats['neutral_percentage'],
                'avg_bad_pct_for_scaling': avg_bad_pct
            }
        },
        'countries': country_data
    }
    
    # Write to JSON
    with open('country_data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Generated country_data.json with sentiment-based grey values")
    
    # Show some examples
    print()
    print("="*80)
    print("EXAMPLE GREY VALUES")
    print("="*80)
    
    # Sort by grey value
    sorted_countries = sorted(country_data.items(), 
                             key=lambda x: x[1].get('grey_value', 0.5),
                             reverse=True)
    
    print("\nDarkest (most bad news):")
    for country, data in sorted_countries[:5]:
        if not data['low_confidence'] and data['sentiment']:
            print(f"  {country:30s} - Grey: {data['grey_value']:.3f} "
                  f"({data['sentiment']['bad_pct']:.1f}% bad news)")
    
    print("\nLightest (least bad news):")
    for country, data in sorted_countries[-5:]:
        if not data['low_confidence'] and data['sentiment']:
            print(f"  {country:30s} - Grey: {data['grey_value']:.3f} "
                  f"({data['sentiment']['bad_pct']:.1f}% bad news)")
    
    print()
    print("="*80)

if __name__ == "__main__":
    main()

