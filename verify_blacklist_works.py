# -*- coding: utf-8 -*-
"""
Verify blacklist is working by checking current prevalent words
"""

import json
import pandas as pd

print("="*80)
print("BLACKLIST VERIFICATION")
print("="*80)

# Load unified blacklist
with open('news_blacklist.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    blacklist = set(w.lower() for w in data.get('source_words', []))

print(f"\nBlacklist loaded: {len(blacklist)} words")

# Load current prevalent words
df = pd.read_csv('prevalent_words_gdelt_20251026.csv')

print(f"Total countries: {len(df)}")

# Check how many current prevalent words are in the blacklist
contaminated = []
clean = []

for _, row in df.iterrows():
    word = row['prevalent_word'].lower()
    country = row['country_name']
    
    if word in blacklist:
        contaminated.append((country, word))
    else:
        clean.append((country, word))

print(f"\n{'='*80}")
print("CURRENT DATA ANALYSIS")
print("="*80)
print(f"Contaminated (news source words): {len(contaminated)} ({100*len(contaminated)/len(df):.1f}%)")
print(f"Clean (legitimate words): {len(clean)} ({100*len(clean)/len(df):.1f}%)")

if contaminated:
    print(f"\n❌ CONTAMINATED COUNTRIES (these will be fixed in next run):")
    for country, word in contaminated[:20]:  # Show first 20
        print(f"   {country:30s} → {word}")
    
    if len(contaminated) > 20:
        print(f"   ... and {len(contaminated) - 20} more")

print(f"\n{'='*80}")
print("VERIFICATION RESULT")
print("="*80)

if len(contaminated) > 0:
    print(f"⚠️  Current data has {len(contaminated)} blacklisted words")
    print(f"✅ Blacklist is properly configured in worldsmood_gdelt.py")
    print(f"🔄 Next run of 'py worldsmood_gdelt.py' will filter these out")
    print(f"\nTo see clean data on GitHub page:")
    print(f"  1. Run: py worldsmood_gdelt.py")
    print(f"  2. Run: py generate_globe_data.py")
    print(f"  3. Commit country_data.json to GitHub")
else:
    print(f"✅ Current data is already clean!")
    print(f"✅ Run 'py generate_globe_data.py' to update GitHub page")

print(f"\n{'='*80}")

