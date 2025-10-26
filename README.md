# World's Mood 🌍

An interactive 3D globe visualizing today's most prevalent words from news headlines around the world.

**Live Site:** https://oskarengl.github.io/worlds-mood/

## What It Does

Analyzes news headlines from 180+ countries daily and displays the most distinctive word for each country on an interactive globe. Words that appear frequently locally but rarely globally rise to the top.

## Features

- **Interactive 3D Globe** - Spin and explore the world
- **Clickable Headlines** - See actual news headlines and search them on Google
- **Dynamic Opacity** - Word darkness indicates prevalence percentage
- **Timeframe Tracking** - Shows if data is from today, last 7 days, or last 30 days
- **Auto-Updates** - Refreshes every 6 hours via GitHub Actions
- **Help Panel** - Built-in guide with scoring methodology

## How It Works

1. **Data Collection**: GDELT Project API fetches headlines from 180+ countries
2. **Word Analysis**: Identifies distinctive words using prevalence scoring
3. **Visualization**: Displays results on an interactive 3D globe
4. **Auto-Deploy**: GitHub Actions updates data and deploys to GitHub Pages

## Scoring Formula

```
Prevalence Score = (Local % × Global Rarity) × 1000
```

This balances local frequency against global uniqueness to highlight what makes each country's news distinctive.

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript (Globe.gl library)
- **Backend**: Python (GDELT API, NLTK, Pandas)
- **Hosting**: GitHub Pages
- **Automation**: GitHub Actions (cron: every 6 hours)
- **Data Source**: GDELT Project

## Project Structure

```
world news/
├── index.html                          # Main website
├── worldsmood_gdelt.py                 # News collection & analysis
├── generate_globe_data.py              # JSON generation
├── country_data.json                   # Country word data
├── headlines_data.json                 # Headline storage
├── requirements.txt                    # Python dependencies
├── .github/workflows/daily-update.yml  # Auto-update workflow
└── README.md                           # This file
```

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Collect news data
python worldsmood_gdelt.py

# Generate JSON
python generate_globe_data.py

# Start local server
python -m http.server 8000

# Open http://localhost:8000
```

## Key Features Explained

### Word Counting
- Each headline counted once (duplicates removed)
- Word boundaries used (e.g., "test" won't match "protesters")
- Each word counted once per article, regardless of repetitions

### Data Collection
- **24h pass**: Primary data from last 24 hours
- **7d pass**: Fallback for countries with no recent data
- **30d pass**: Second fallback for maximum coverage
- Parallel processing (10 countries simultaneously)

### Opacity Rules
- Linear gradient from 2% (light grey) to 50% (black)
- Words in articles with ≤4 articles capped at 50% opacity
- Prevents low-sample words from dominating visually

## Credits

- **Data Source**: [GDELT Project](https://www.gdeltproject.org/)
- **Globe Library**: [globe.gl](https://github.com/vasturiano/globe.gl)
- **Created**: October 2025

---

*Updated every 6 hours (UTC)*
