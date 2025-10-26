# -*- coding: utf-8 -*-
"""
World's Mood - News Analysis with GDELT Project
Truly unlimited, free global news coverage!
"""

import requests
import pandas as pd
from datetime import datetime
import time
from collections import Counter
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

# GDELT API Configuration
GDELT_DOC_API = 'http://api.gdeltproject.org/api/v2/doc/doc'

# Try to import NLTK
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

# Country codes for GDELT
# GDELT uses FIPS 10-4 country codes
# Coverage test: 5 articles per country for all countries in the world
COUNTRIES = {
    'Afghanistan': 'AF',
    'Albania': 'AL',
    'Algeria': 'AG',
    'Andorra': 'AN',
    'Angola': 'AO',
    'Antigua and Barbuda': 'AC',
    'Argentina': 'AR',
    'Armenia': 'AM',
    'Australia': 'AS',
    'Austria': 'AU',
    'Azerbaijan': 'AJ',
    'Bahamas': 'BF',
    'Bahrain': 'BA',
    'Bangladesh': 'BG',
    'Barbados': 'BB',
    'Belarus': 'BO',
    'Belgium': 'BE',
    'Belize': 'BH',
    'Benin': 'BN',
    'Bolivia': 'BL',
    'Bosnia and Herzegovina': 'BK',
    'Botswana': 'BC',
    'Brazil': 'BR',
    'Brunei': 'BX',
    'Bulgaria': 'BU',
    'Burkina Faso': 'UV',
    'Burundi': 'BY',
    'Cambodia': 'CB',
    'Cameroon': 'CM',
    'Canada': 'CA',
    'Cabo Verde': 'CV',
    'Central African Republic': 'CT',
    'Chad': 'CD',
    'Chile': 'CI',
    'China': 'CH',
    'Colombia': 'CO',
    'Comoros': 'CN',
    'Democratic Republic of the Congo': 'CG',
    'Republic of the Congo': 'CF',
    'Costa Rica': 'CS',
    'Cote d\'Ivoire': 'IV',
    'Croatia': 'HR',
    'Cuba': 'CU',
    'Cyprus': 'CY',
    'Czechia': 'EZ',
    'Denmark': 'DA',
    'Djibouti': 'DJ',
    'Dominica': 'DO',
    'Dominican Republic': 'DR',
    'Ecuador': 'EC',
    'Egypt': 'EG',
    'El Salvador': 'ES',
    'Equatorial Guinea': 'EK',
    'Eritrea': 'ER',
    'Estonia': 'EN',
    'Eswatini': 'WZ',
    'Ethiopia': 'ET',
    'Fiji': 'FJ',
    'Finland': 'FI',
    'France': 'FR',
    'Gabon': 'GB',
    'Gambia': 'GA',
    'Georgia': 'GG',
    'Germany': 'GM',
    'Ghana': 'GH',
    'Greece': 'GR',
    'Grenada': 'GJ',
    'Guatemala': 'GT',
    'Guinea': 'GV',
    'Guinea-Bissau': 'PU',
    'Guyana': 'GY',
    'Haiti': 'HA',
    'Honduras': 'HO',
    'Hungary': 'HU',
    'Iceland': 'IC',
    'India': 'IN',
    'Indonesia': 'ID',
    'Iran': 'IR',
    'Iraq': 'IZ',
    'Ireland': 'EI',
    'Israel': 'IS',
    'Italy': 'IT',
    'Jamaica': 'JM',
    'Japan': 'JA',
    'Jordan': 'JO',
    'Kazakhstan': 'KZ',
    'Kenya': 'KE',
    'Kiribati': 'KR',
    'North Korea': 'KN',
    'South Korea': 'KS',
    'Kosovo': 'KV',
    'Kuwait': 'KU',
    'Kyrgyzstan': 'KG',
    'Laos': 'LA',
    'Latvia': 'LG',
    'Lebanon': 'LE',
    'Lesotho': 'LT',
    'Liberia': 'LI',
    'Libya': 'LY',
    'Liechtenstein': 'LS',
    'Lithuania': 'LH',
    'Luxembourg': 'LU',
    'Madagascar': 'MA',
    'Malawi': 'MI',
    'Malaysia': 'MY',
    'Maldives': 'MV',
    'Mali': 'ML',
    'Malta': 'MT',
    'Marshall Islands': 'RM',
    'Mauritania': 'MR',
    'Mauritius': 'MP',
    'Mexico': 'MX',
    'Micronesia': 'FM',
    'Moldova': 'MD',
    'Monaco': 'MN',
    'Mongolia': 'MG',
    'Montenegro': 'MJ',
    'Morocco': 'MO',
    'Mozambique': 'MZ',
    'Myanmar': 'BM',
    'Namibia': 'WA',
    'Nauru': 'NR',
    'Nepal': 'NP',
    'Netherlands': 'NL',
    'New Zealand': 'NZ',
    'Nicaragua': 'NU',
    'Niger': 'NG',
    'Nigeria': 'NI',
    'North Macedonia': 'MK',
    'Norway': 'NO',
    'Oman': 'MU',
    'Pakistan': 'PK',
    'Palau': 'PS',
    'Panama': 'PM',
    'Papua New Guinea': 'PP',
    'Paraguay': 'PA',
    'Peru': 'PE',
    'Philippines': 'RP',
    'Poland': 'PL',
    'Portugal': 'PO',
    'Qatar': 'QA',
    'Romania': 'RO',
    'Russia': 'RS',
    'Rwanda': 'RW',
    'Saint Kitts and Nevis': 'SC',
    'Saint Lucia': 'ST',
    'Saint Vincent and the Grenadines': 'VC',
    'Samoa': 'WS',
    'San Marino': 'SM',
    'Sao Tome and Principe': 'TP',
    'Saudi Arabia': 'SA',
    'Senegal': 'SG',
    'Serbia': 'RI',
    'Seychelles': 'SE',
    'Sierra Leone': 'SL',
    'Singapore': 'SN',
    'Slovakia': 'LO',
    'Slovenia': 'SI',
    'Solomon Islands': 'BP',
    'Somalia': 'SO',
    'South Africa': 'SF',
    'South Sudan': 'OD',
    'Spain': 'SP',
    'Sri Lanka': 'CE',
    'Sudan': 'SU',
    'Suriname': 'NS',
    'Sweden': 'SW',
    'Switzerland': 'SZ',
    'Syria': 'SY',
    'Tajikistan': 'TI',
    'Tanzania': 'TZ',
    'Thailand': 'TH',
    'Timor-Leste': 'TT',
    'Togo': 'TO',
    'Tonga': 'TN',
    'Trinidad and Tobago': 'TD',
    'Tunisia': 'TS',
    'Turkey': 'TU',
    'Turkmenistan': 'TX',
    'Tuvalu': 'TV',
    'Uganda': 'UG',
    'Ukraine': 'UP',
    'United Arab Emirates': 'AE',
    'United Kingdom': 'UK',
    'United States': 'US',
    'Uruguay': 'UY',
    'Uzbekistan': 'UZ',
    'Vanuatu': 'NH',
    'Venezuela': 'VE',
    'Vietnam': 'VM',
    'Yemen': 'YM',
    'Zambia': 'ZA',
    'Zimbabwe': 'ZI',
}

# Maximum articles to fetch per country
MAX_ARTICLES_PER_COUNTRY = 30

def fetch_news_for_country(country_name, country_code, timespan='24h'):
    """Fetch news from GDELT for a specific country"""
    
    timespan_label = timespan if timespan != '24h' else ''
    print(f"Fetching news for {country_name}{' ('+timespan_label+')' if timespan_label else ''}...", end='', flush=True)
    
    # GDELT DOC API parameters
    params = {
        'query': f'sourcecountry:{country_code}',
        'mode': 'artlist',
        'maxrecords': MAX_ARTICLES_PER_COUNTRY,
        'format': 'json',
        'timespan': timespan,  # Can be '24h', '7d', etc.
        'sort': 'datedesc'  # Most recent first
    }
    
    try:
        response = requests.get(GDELT_DOC_API, params=params, timeout=30)
        
        if response.status_code == 200:
            try:
                data = response.json()
            except json.JSONDecodeError:
                # GDELT sometimes returns HTML or other formats
                print(f" -> JSON error (likely no data)")
                return []
            
            if 'articles' in data and data['articles']:
                articles = []
                for article in data['articles']:
                    # Extract title and description
                    title = article.get('title', '')
                    seendate = article.get('seendate', '')
                    url = article.get('url', '')
                    domain = article.get('domain', '')
                    
                    if title.strip():
                        articles.append({
                            'title': title,
                            'text': title,  # Only analyze headlines
                            'source': domain,
                            'date': seendate,
                            'url': url
                        })
                
                print(f" -> {len(articles)} articles")
                return articles
            else:
                print(f" -> 0 articles")
                return []
        else:
            print(f" -> HTTP {response.status_code}")
            return []
            
    except requests.Timeout:
        print(f" -> Timeout")
        return []
    except Exception as e:
        print(f" -> Error: {str(e)[:30]}")
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
                         'which', 'who', 'when', 'where', 'why', 'how', 'said', 'says', 'after',
                         'over', 'up', 'down', 'out', 'off', 'into', 'than', 'their', 'them'])
    
    word_counts = Counter()
    
    for text in texts:
        # Clean text
        text = text.lower()
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        # Remove special characters but keep letters and apostrophes
        text = re.sub(r'[^a-z\s\']', ' ', text)
        # Remove extra apostrophes
        text = re.sub(r'\'s\b', '', text)
        
        # Tokenize
        if USE_NLTK:
            try:
                words = word_tokenize(text)
            except:
                words = text.split()
        else:
            words = text.split()
        
        # Filter words
        for word in words:
            word = word.strip("'")
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
    global_rarity = 1.0 / (global_freq + 1)
    
    # Combined score: local prevalence * global rarity
    score = local_pct * global_rarity * 1000
    
    return score, local_pct

def main():
    print("="*80)
    print("WORLD'S MOOD - NEWS ANALYSIS (GDELT Project)")
    print("="*80)
    print(f"\nStarted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Countries to analyze: {len(COUNTRIES)}")
    print(f"Max articles per country: {MAX_ARTICLES_PER_COUNTRY}")
    print(f"Timeframe: Last 24 hours")
    print(f"No rate limits - Unlimited queries!")
    print("\n" + "="*80 + "\n")
    
    # FIRST PASS: Collect articles from last 24 hours
    all_country_data = {}
    all_articles_text = []
    missing_countries = {}  # Track countries with no data for second pass
    country_timeframe = {}  # Track which timeframe was used for each country
    
    total_countries = len(COUNTRIES)
    completed = 0
    
    print("FIRST PASS: Last 24 hours\n")
    
    # Use ThreadPoolExecutor for parallel requests (10 at a time)
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all tasks
        future_to_country = {
            executor.submit(fetch_news_for_country, country_name, country_code): (country_name, country_code)
            for country_name, country_code in COUNTRIES.items()
        }
        
        # Process results as they complete
        for future in as_completed(future_to_country):
            country_name, country_code = future_to_country[future]
            completed += 1
            
            print(f"\n[{completed}/{total_countries}] ", end='')
            
            try:
                articles = future.result()
                if articles:
                    all_country_data[country_name] = articles
                    all_articles_text.extend([article['text'] for article in articles])
                    country_timeframe[country_name] = '24h'
                else:
                    # No data - add to missing list for second pass
                    missing_countries[country_name] = country_code
            except Exception as e:
                print(f"{country_name} -> Exception: {str(e)[:30]}")
                missing_countries[country_name] = country_code
    
    # SECOND PASS: Try last 7 days for countries with no 24h data
    still_missing = {}
    if missing_countries:
        print(f"\n\n{'='*80}")
        print(f"SECOND PASS: Trying last 7 days for {len(missing_countries)} countries with no 24h data")
        print(f"{'='*80}\n")
        
        completed_second = 0
        total_missing = len(missing_countries)
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit all tasks with 7-day timespan
            future_to_country = {
                executor.submit(fetch_news_for_country, country_name, country_code, '7d'): (country_name, country_code)
                for country_name, country_code in missing_countries.items()
            }
            
            # Process results as they complete
            for future in as_completed(future_to_country):
                country_name, country_code = future_to_country[future]
                completed_second += 1
                
                print(f"\n[{completed_second}/{total_missing}] ", end='')
                
                try:
                    articles = future.result()
                    if articles:
                        all_country_data[country_name] = articles
                        all_articles_text.extend([article['text'] for article in articles])
                        country_timeframe[country_name] = '7d'
                    else:
                        # Still no data - add to third pass
                        still_missing[country_name] = country_code
                except Exception as e:
                    print(f"{country_name} -> Exception: {str(e)[:30]}")
                    still_missing[country_name] = country_code
    
    # THIRD PASS: Try last 30 days for countries still missing
    if still_missing:
        print(f"\n\n{'='*80}")
        print(f"THIRD PASS: Trying last 30 days for {len(still_missing)} countries still missing")
        print(f"{'='*80}\n")
        
        completed_third = 0
        total_still_missing = len(still_missing)
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit all tasks with 30-day timespan
            future_to_country = {
                executor.submit(fetch_news_for_country, country_name, country_code, '30d'): country_name
                for country_name, country_code in still_missing.items()
            }
            
            # Process results as they complete
            for future in as_completed(future_to_country):
                country_name = future_to_country[future]
                completed_third += 1
                
                print(f"\n[{completed_third}/{total_still_missing}] ", end='')
                
                try:
                    articles = future.result()
                    if articles:
                        all_country_data[country_name] = articles
                        all_articles_text.extend([article['text'] for article in articles])
                        country_timeframe[country_name] = '30d'
                except Exception as e:
                    print(f"{country_name} -> Exception: {str(e)[:30]}")
    
    if not all_country_data:
        print("\n[ERROR] No articles collected! Check your internet connection.")
        sys.exit(1)
    
    print(f"\n{'='*80}")
    print(f"COLLECTION SUMMARY")
    print(f"{'='*80}")
    print(f"Total articles collected: {len(all_articles_text)}")
    print(f"Countries with data: {len(all_country_data)}")
    print(f"Coverage: {len(all_country_data)}/{total_countries} ({100*len(all_country_data)/total_countries:.1f}%)")
    print(f"Average articles per country: {len(all_articles_text) / len(all_country_data):.1f}")
    
    # Calculate recovery stats
    first_pass_count = total_countries - len(missing_countries)
    if missing_countries:
        second_pass_recovered = len(missing_countries) - len(still_missing)
        third_pass_recovered = len(still_missing) if still_missing else 0
        final_missing = total_countries - len(all_country_data)
        
        print(f"\nData source breakdown:")
        print(f"  24-hour data: {first_pass_count} countries")
        if second_pass_recovered > 0:
            print(f"  7-day fallback: +{second_pass_recovered} countries")
        if still_missing and (len(still_missing) - final_missing) > 0:
            print(f"  30-day fallback: +{len(still_missing) - final_missing} countries")
        print(f"  No data found: {final_missing} countries")
    
    print(f"{'='*80}\n")
    
    # Calculate global word frequencies
    print("Calculating global word frequencies...")
    global_word_freq = get_word_frequency(all_articles_text)
    print(f"  Found {len(global_word_freq)} unique words globally\n")
    
    # Analyze each country and store headlines
    print("Analyzing prevalent words per country...\n")
    results = []
    headlines_data = {}  # Store headlines for each country
    
    total_to_analyze = len(all_country_data)
    for idx, (country_name, articles) in enumerate(all_country_data.items(), 1):
        print(f"[{idx}/{total_to_analyze}] Analyzing {country_name}...")
        
        texts = [article['text'] for article in articles]
        country_word_freq = get_word_frequency(texts)
        
        if not country_word_freq:
            print(f"  [WARN] No words found\n")
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
                'num_articles': len(articles),
                'timeframe': country_timeframe.get(country_name, '24h')
            })
            
            # Store headlines: separate those with prevalent word from others
            headlines_with_word = []
            headlines_without_word = []
            
            # Use word boundary matching to avoid false positives
            # e.g., "test" should not match "protesters"
            word_pattern = r'\b' + re.escape(prevalent_word.lower()) + r'\b'
            
            for article in articles:
                headline = article['title']
                # Check if prevalent word appears as a whole word in headline (case-insensitive)
                if re.search(word_pattern, headline.lower()):
                    headlines_with_word.append(headline)
                else:
                    headlines_without_word.append(headline)
            
            # Store all headlines (those with word on top, others below)
            headlines_data[country_name] = {
                'with_word': headlines_with_word,
                'without_word': headlines_without_word
            }
            
            print(f" -> '{prevalent_word}' ({percentage:.1f}%)")
        else:
            print(f" -> No word found")
    
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
    output_file = f'prevalent_words_gdelt_{datetime.now().strftime("%Y%m%d")}.csv'
    df.to_csv(output_file, index=False)
    print(f"\n[OK] Results saved to: {output_file}")
    
    # Save headlines to JSON
    import json
    headlines_file = 'headlines_data.json'
    with open(headlines_file, 'w', encoding='utf-8') as f:
        json.dump(headlines_data, f, indent=2, ensure_ascii=False)
    print(f"[OK] Headlines saved to: {headlines_file}")
    
    # Summary
    print("\nSummary:")
    print(f"   Countries analyzed: {len(df)}")
    print(f"   Total articles processed: {int(df['num_articles'].sum())}")
    print(f"   Average articles per country: {df['num_articles'].mean():.1f}")
    print(f"   Countries with 50+ articles: {len(df[df['num_articles'] >= 50])}")
    print(f"   Countries with 10-49 articles: {len(df[(df['num_articles'] >= 10) & (df['num_articles'] < 50)])}")
    print(f"   Countries with <10 articles: {len(df[df['num_articles'] < 10])}")
    
    if len(df) > 0:
        max_idx = df['prevalence_score'].idxmax()
        print(f"\n   Most prevalent word globally: '{df.loc[max_idx, 'prevalent_word']}' "
              f"in {df.loc[max_idx, 'country_name']}")
    
    print(f"\n[SUCCESS] Script completed at {datetime.now().strftime('%H:%M:%S')}!")
    sys.exit(0)

if __name__ == "__main__":
    main()

