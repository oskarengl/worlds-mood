# -*- coding: utf-8 -*-
"""
Sentiment Analysis for News Headlines
Classifies headlines as Good News, Bad News, or Neutral
Uses DistilBERT transformer model for context-aware sentiment
"""

import json
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# Initialize transformer model
print("Initializing sentiment analysis model...")
print("First run will download DistilBERT (~250MB) - please wait...")

try:
    from transformers import pipeline
    
    # Load pre-trained sentiment analysis pipeline
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=-1,  # Use CPU
        truncation=True,
        max_length=512
    )
    print("[OK] Model loaded successfully!\n")
except ImportError:
    print("\n[ERROR] transformers library not installed!")
    print("Please run: pip install transformers torch\n")
    exit(1)
except Exception as e:
    print(f"\n[ERROR] Failed to load model: {e}\n")
    exit(1)

def classify_sentiment(text, model=None):
    """
    Classify a headline as good, bad, or neutral news using DistilBERT
    Returns: 'good', 'bad', or 'neutral'
    
    Ultra-conservative threshold: 99% confidence required for both good and bad
    - Only extremely clear positive sentiment → good
    - Only extremely clear negative sentiment → bad
    - Everything else → neutral (vast majority will be neutral)
    """
    try:
        # Get prediction from transformer model
        result = sentiment_pipeline(text[:512])[0]  # Truncate long texts
        label = result['label']  # 'POSITIVE' or 'NEGATIVE'
        score = result['score']  # Confidence score 0-1
        
        # Ultra-high confidence threshold (99%) for both good and bad
        # Vast majority of headlines will be neutral with this threshold
        if label == 'POSITIVE' and score >= 0.99:
            return 'good'
        elif label == 'NEGATIVE' and score >= 0.99:
            return 'bad'
        else:
            # Everything else = neutral
            return 'neutral'
    except Exception as e:
        print(f"Error classifying '{text[:50]}...': {e}")
        return 'neutral'

def main():
    print("="*80)
    print("SENTIMENT ANALYSIS - News Headlines")
    print("="*80)
    print()
    
    # Load headlines data
    print("Loading headlines data...")
    with open('headlines_data.json', 'r', encoding='utf-8') as f:
        headlines_data = json.load(f)
    
    print(f"Loaded headlines for {len(headlines_data)} countries\n")
    
    # Process all headlines
    sentiment_results = {}
    global_stats = {'good': 0, 'bad': 0, 'neutral': 0, 'total': 0}
    country_stats = {}
    
    print("Analyzing sentiment for each headline using DistilBERT...")
    print("(This may take a few minutes for the first run)")
    print()
    
    for country, data in headlines_data.items():
        all_headlines = data['with_word'] + data['without_word']
        
        if not all_headlines:
            continue
        
        country_sentiments = {'good': 0, 'bad': 0, 'neutral': 0}
        classified_headlines = {
            'good': [],
            'bad': [],
            'neutral': []
        }
        
        for headline in all_headlines:
            sentiment = classify_sentiment(headline)
            country_sentiments[sentiment] += 1
            global_stats[sentiment] += 1
            global_stats['total'] += 1
            
            classified_headlines[sentiment].append(headline)
        
        total = len(all_headlines)
        country_stats[country] = {
            'good': country_sentiments['good'],
            'bad': country_sentiments['bad'],
            'neutral': country_sentiments['neutral'],
            'total': total,
            'good_pct': (country_sentiments['good'] / total * 100) if total > 0 else 0,
            'bad_pct': (country_sentiments['bad'] / total * 100) if total > 0 else 0,
            'neutral_pct': (country_sentiments['neutral'] / total * 100) if total > 0 else 0
        }
        
        sentiment_results[country] = classified_headlines
        
        print(f"[{country}] Good: {country_sentiments['good']}, "
              f"Bad: {country_sentiments['bad']}, "
              f"Neutral: {country_sentiments['neutral']}")
    
    # Calculate global percentages
    print()
    print("="*80)
    print("GLOBAL SENTIMENT ANALYSIS RESULTS")
    print("="*80)
    print(f"\nTotal headlines analyzed: {global_stats['total']}")
    print()
    print(f"Good News:    {global_stats['good']:4d} headlines "
          f"({global_stats['good']/global_stats['total']*100:5.2f}%)")
    print(f"Bad News:     {global_stats['bad']:4d} headlines "
          f"({global_stats['bad']/global_stats['total']*100:5.2f}%)")
    print(f"Neutral News: {global_stats['neutral']:4d} headlines "
          f"({global_stats['neutral']/global_stats['total']*100:5.2f}%)")
    print()
    
    # Find countries with highest bad news percentage
    sorted_by_bad = sorted(country_stats.items(), 
                           key=lambda x: x[1]['bad_pct'], 
                           reverse=True)
    
    print("="*80)
    print("TOP 10 COUNTRIES BY BAD NEWS PERCENTAGE")
    print("="*80)
    for i, (country, stats) in enumerate(sorted_by_bad[:10], 1):
        print(f"{i:2d}. {country:30s} - {stats['bad_pct']:5.1f}% bad "
              f"({stats['bad']}/{stats['total']} headlines)")
    
    print()
    
    # Find countries with highest good news percentage
    sorted_by_good = sorted(country_stats.items(), 
                            key=lambda x: x[1]['good_pct'], 
                            reverse=True)
    
    print("="*80)
    print("TOP 10 COUNTRIES BY GOOD NEWS PERCENTAGE")
    print("="*80)
    for i, (country, stats) in enumerate(sorted_by_good[:10], 1):
        print(f"{i:2d}. {country:30s} - {stats['good_pct']:5.1f}% good "
              f"({stats['good']}/{stats['total']} headlines)")
    
    print()
    print("="*80)
    
    # Save detailed results
    output = {
        'global_stats': {
            'total_headlines': global_stats['total'],
            'good_count': global_stats['good'],
            'bad_count': global_stats['bad'],
            'neutral_count': global_stats['neutral'],
            'good_percentage': round(global_stats['good']/global_stats['total']*100, 2),
            'bad_percentage': round(global_stats['bad']/global_stats['total']*100, 2),
            'neutral_percentage': round(global_stats['neutral']/global_stats['total']*100, 2)
        },
        'country_stats': country_stats,
        'classified_headlines': sentiment_results
    }
    
    with open('sentiment_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Detailed results saved to: sentiment_analysis.json")
    print()

if __name__ == "__main__":
    main()

