# -*- coding: utf-8 -*-
"""
World's Mood - News Analysis with NewsData.io API
Collects global news and finds prevalent words per country
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import time
from collections import Counter
import re
import sys

# NewsData.io API Configuration
NEWSDATA_API_KEY = 'pub_71fe0e3734f842bf902a7589008061b0'
NEWSDATA_API_URL = 'https://newsdata.io/api/1/news'

# Try to import NLTK, but work without it if not available
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords', quiet=True)
    USE_NLTK = True
except:
    USE_NLTK = False
    print("NLTK not available, using basic tokenization")

# Country codes for NewsData.io API
# Format: 'Display Name': 'ISO 2-letter code'
COUNTRIES = {
    'United States': 'us',
    'United Kingdom': 'gb',
    'Canada': 'ca',
    'Germany': 'de',
    'France': 'fr',
    'Italy': 'it',
    'Spain': 'es',
    'Netherlands': 'nl',
    'Belgium': 'be',
    'Switzerland': 'ch',
    'Austria': 'at',
    'Poland': 'pl',
    'Portugal': 'pt',
    'Greece': 'gr',
    'Sweden': 'se',
    'Norway': 'no',
    'Denmark': 'dk',
    'Finland': 'fi',
    'Ireland': 'ie',
    'Czech Republic': 'cz',
    'Hungary': 'hu',
    'Romania': 'ro',
    'Bulgaria': 'bg',
    'Croatia': 'hr',
    'Serbia': 'rs',
    'Slovakia': 'sk',
    'Slovenia': 'si',
    'Lithuania': 'lt',
    'Latvia': 'lv',
    'Estonia': 'ee',
    'Japan': 'jp',
    'South Korea': 'kr',
    'China': 'cn',
    'India': 'in',
    'Indonesia': 'id',
    'Thailand': 'th',
    'Vietnam': 'vn',
    'Philippines': 'ph',
    'Singapore': 'sg',
    'Malaysia': 'my',
    'Australia': 'au',
    'New Zealand': 'nz',
    'Brazil': 'br',
    'Mexico': 'mx',
    'Argentina': 'ar',
    'Chile': 'cl',
    'Colombia': 'co',
    'Peru': 'pe',
    'Egypt': 'eg',
    'Nigeria': 'ng',
    'South Africa': 'za',
    'Kenya': 'ke',
    'Morocco': 'ma',
    'Turkey': 'tr',
    'Israel': 'il',
    'Saudi Arabia': 'sa',
    'United Arab Emirates': 'ae',
    'Pakistan': 'pk',
    'Bangladesh': 'bd',
    'Russia': 'ru',
    'Ukraine': 'ua',
}

# Articles to fetch per country
ARTICLES_PER_COUNTRY = 10

def fetch_news_for_country(country_name, country_code):
    """Fetch news from NewsData.io API for a specific country"""
    
    print(f"Fetching news for {country_name}...")
    
    params = {
        'apikey': NEWSDATA_API_KEY,
        'country': country_code,
        'language': 'en',  # English only for consistency
        'size': ARTICLES_PER_COUNTRY,
    }
    
    try:
        response = requests.get(NEWSDATA_API_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['status'] == 'success' and 'results' in data:
                articles = []
                for article in data['results']:
                    # Combine title and description for text analysis
                    text = ''
                    if article.get('title'):
                        text += article['title'] + ' '
                    if article.get('description'):
                        text += article['description']
                    
                    if text.strip():
                        articles.append({
                            'title': article.get('title', ''),
                            'text': text.strip(),
                            'source': article.get('source_id', 'unknown'),
                            'pubDate': article.get('pubDate', '')
                        })
                
                print(f"  [OK] Found {len(articles)} articles")
                return articles
            else:
                print(f"  [WARN] No results in response")
                return []
        else:
            print(f"  [ERROR] API error: {response.status_code}")
            if response.status_code == 429:
                print("  [WARN] Rate limit reached! Consider upgrading API plan.")
            return []
            
    except Exception as e:
        print(f"  [ERROR] Error: {e}")
        return []

def get_word_frequency(texts):
    """Analyze text and return word frequencies"""
    
    if USE_NLTK:
        stop_words = set(stopwords.words('english'))
    else:
        # Basic English stop words
        stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                         'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                         'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                         'would', 'could', 'should', 'may', 'might', 'can', 'it', 'its', 'this',
                         'that', 'these', 'those', 'i', 'you', 'he', 'she', 'we', 'they', 'what',
                         'which', 'who', 'when', 'where', 'why', 'how', 'said', 'says'])
    
    word_counts = Counter()
    
    for text in texts:
        # Clean text
        text = text.lower()
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        # Remove special characters but keep letters
        text = re.sub(r'[^a-z\s]', ' ', text)
        
        # Tokenize
        if USE_NLTK:
            words = word_tokenize(text)
        else:
            words = text.split()
        
        # Filter words
        for word in words:
            if (len(word) > 3 and  # At least 4 characters
                word not in stop_words and
                not word.isdigit()):
                word_counts[word] += 1
    
    return word_counts

def calculate_prevalence_score(word, country_freq, global_freq, num_articles):
    """Calculate how prevalent a word is locally vs globally"""
    
    # Local percentage (how often it appears in this country's articles)
    local_pct = (country_freq / num_articles) * 100
    
    # Global rarity (inverse of global frequency)
    global_rarity = 1.0 / (global_freq + 1)  # +1 to avoid division by zero
    
    # Combined score: local prevalence * global rarity
    score = local_pct * global_rarity * 1000  # Scale up for readability
    
    return score, local_pct

def main():
    print("="*80)
    print("WORLD'S MOOD - NEWS ANALYSIS (NewsData.io API)")
    print("="*80)
    print(f"\nStarted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Countries to analyze: {len(COUNTRIES)}")
    print(f"Articles per country: {ARTICLES_PER_COUNTRY}")
    print(f"Total API calls needed: {len(COUNTRIES)}")
    print("\n" + "="*80 + "\n")
    
    # Collect all articles
    all_country_data = {}
    all_articles_text = []
    
    for country_name, country_code in COUNTRIES.items():
        articles = fetch_news_for_country(country_name, country_code)
        
        if articles:
            all_country_data[country_name] = articles
            all_articles_text.extend([article['text'] for article in articles])
        
        # Small delay to be nice to the API
        time.sleep(0.5)
    
    if not all_country_data:
        print("\n[ERROR] No articles collected! Check your API key and internet connection.")
        sys.exit(1)
    
    print(f"\n{'='*80}")
    print(f"Total articles collected: {len(all_articles_text)}")
    print(f"Countries with data: {len(all_country_data)}")
    print(f"{'='*80}\n")
    
    # Calculate global word frequencies
    print("Calculating global word frequencies...")
    global_word_freq = get_word_frequency(all_articles_text)
    print(f"  Found {len(global_word_freq)} unique words globally\n")
    
    # Analyze each country
    print("Analyzing prevalent words per country...\n")
    results = []
    
    for country_name, articles in all_country_data.items():
        print(f"Analyzing {country_name}...")
        
        texts = [article['text'] for article in articles]
        country_word_freq = get_word_frequency(texts)
        
        if not country_word_freq:
            print(f"  No words found\n")
            continue
        
        # Calculate prevalence scores for each word
        word_scores = []
        for word, country_count in country_word_freq.items():
            global_count = global_word_freq.get(word, 0)
            score, local_pct = calculate_prevalence_score(
                word, country_count, global_count, len(articles)
            )
            word_scores.append((word, score, local_pct, country_count))
        
        # Sort by score and get top word
        word_scores.sort(key=lambda x: x[1], reverse=True)
        
        if word_scores:
            prevalent_word, score, percentage, frequency = word_scores[0]
            
            results.append({
                'country_name': country_name,
                'week': datetime.now().strftime('%Y-W%U'),
                'prevalent_word': prevalent_word,
                'word_frequency': frequency,
                'word_percentage': round(percentage, 2),
                'prevalence_score': round(score, 2),
                'num_articles': len(articles)
            })
            
            print(f"  [OK] Most prevalent: '{prevalent_word}' ({percentage:.1f}%, score: {score:.2f})\n")
        else:
            print(f"  [WARN] No prevalent word found\n")
    
    # Create DataFrame and save
    df = pd.DataFrame(results)
    
    if len(df) == 0:
        print("\n[ERROR] No results to save!")
        sys.exit(1)
    
    # Sort by prevalence score
    df = df.sort_values('prevalence_score', ascending=False)
    
    print("\n" + "="*80)
    print("PREVALENT WORD ANALYSIS RESULTS")
    print("="*80)
    print(df[['country_name', 'prevalent_word', 'word_percentage', 'prevalence_score', 'num_articles']].to_string(index=False))
    print("="*80)
    
    # Save to CSV
    output_file = f'prevalent_words_api_{datetime.now().strftime("%Y%m%d")}.csv'
    df.to_csv(output_file, index=False)
    print(f"\n[OK] Results saved to: {output_file}")
    
    # Summary
    print("\nSummary:")
    print(f"   Countries analyzed: {len(df)}")
    print(f"   Total articles processed: {int(df['num_articles'].sum())}")
    
    if len(df) > 0:
        max_idx = df['prevalence_score'].idxmax()
        print(f"   Most prevalent word globally: '{df.loc[max_idx, 'prevalent_word']}' "
              f"in {df.loc[max_idx, 'country_name']}")
    
    print(f"\n[SUCCESS] Script completed at {datetime.now().strftime('%H:%M:%S')}!")
    sys.exit(0)

if __name__ == "__main__":
    main()

