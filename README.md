# World's Mood 🌍

An interactive 3D globe visualizing sentiment and news trends from 180+ countries, powered by AI sentiment analysis.

**Live Site:** https://oskarengl.github.io/worlds-mood/

## What It Does

Analyzes news headlines from 180+ countries daily using AI-powered sentiment analysis. Each country is shaded from white (positive news) to black (negative news) based on the emotional tone of its headlines.

## Features

- **AI Sentiment Analysis** - DistilBERT transformer model analyzes headline sentiment with 98% confidence threshold
- **Color-Coded Globe** - Countries shaded by news sentiment (white = positive, grey = neutral, black = negative)
- **Interactive 3D Globe** - Spin and explore the world
- **Clickable Headlines** - See actual news headlines color-coded by sentiment
- **Sentiment Statistics** - View good/bad/neutral news percentages per country
- **Local Radio Integration** - Listen to local radio stations from each country
- **Historical Trends** - Track sentiment changes over time with line graphs
- **Colorblind Mode** - Accessibility toggle for color vision deficiency
- **Auto-Updates** - Refreshes every 6 hours via GitHub Actions

## How It Works

1. **Data Collection**: GDELT Project API fetches headlines from 180+ countries
2. **Sentiment Analysis**: DistilBERT AI model classifies each headline as positive, negative, or neutral
3. **Word Analysis**: Identifies distinctive words using prevalence scoring
4. **Color Mapping**: Countries are shaded based on sentiment balance (Good% - Bad%)
5. **Visualization**: Displays results on an interactive 3D globe
6. **Auto-Deploy**: GitHub Actions updates data and deploys to GitHub Pages

## Sentiment Analysis

Headlines are classified using **DistilBERT**, a state-of-the-art transformer model that understands context and meaning:

- **98% confidence threshold** for both positive and negative classifications
- Headlines below this threshold are marked as neutral
- Ultra-conservative approach prevents misclassification
- Results in ~69% neutral, ~13% positive, ~18% negative

## Color Coding

```
Sentiment Balance = Good% - Bad%
```

- **White (0.0)**: Very positive sentiment balance
- **Grey (0.5)**: Neutral or low data (< 10 articles)
- **Black (1.0)**: Very negative sentiment balance

Countries with fewer than 10 articles show as grey for statistical reliability.

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript (Globe.gl library)
- **AI/ML**: DistilBERT (HuggingFace Transformers)
- **Backend**: Python (GDELT API, NLTK, Pandas, PyTorch)
- **Hosting**: GitHub Pages
- **Automation**: GitHub Actions (cron: every 6 hours)
- **Data Source**: GDELT Project

## Project Structure

```
world news/
├── index.html                          # Main website with interactive globe
├── worldsmood_gdelt.py                 # News collection & filtering
├── sentiment_analysis.py               # DistilBERT sentiment classification
├── generate_country_data.py            # JSON generation with sentiment scores
├── save_historical_snapshot.py         # Historical data archiving
├── country_data.json                   # Country sentiment & word data
├── headlines_data.json                 # Raw headline storage
├── sentiment_analysis.json             # Sentiment classification results
├── requirements.txt                    # Python dependencies
├── .github/workflows/daily-update.yml  # Auto-update workflow
└── README.md                           # This file
```

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the data pipeline
python worldsmood_gdelt.py           # 1. Collect headlines (5-10 min)
python sentiment_analysis.py         # 2. Classify sentiment with AI (2-5 min)
python generate_country_data.py      # 3. Generate JSON for globe (instant)

# Start local server
python -m http.server 8000

# Open http://localhost:8000
```

**Note**: First run downloads DistilBERT model (~250MB). Subsequent runs are faster.

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

### Sentiment Color Mapping
- Sentiment balance scaled by factor of 3 for visual contrast
- Aggressive power function pushes values toward extremes
- Countries with < 10 articles shown as 50% grey (statistical reliability)
- Prevents unreliable data from dominating visually

## Credits

- **Data Source**: [GDELT Project](https://www.gdeltproject.org/)
- **AI Model**: [DistilBERT](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english) by HuggingFace
- **Globe Library**: [globe.gl](https://github.com/vasturiano/globe.gl)
- **Radio Integration**: [Radio Garden](https://radio.garden/)
- **Created**: October 2024

---

*Updated every 6 hours (UTC)*
