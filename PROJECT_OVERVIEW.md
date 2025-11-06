# World's Mood - Interactive Globe Project

## 📋 Project Overview

**World's Mood** is an interactive 3D globe visualization that displays the emotional tone of today's news from 180+ countries worldwide. Countries are color-coded by sentiment (white=positive, black=negative) and labeled with their most distinctive news topic of the day.

**Live Demo:** `https://oskarengl.github.io/worlds-mood/`

---

## 🎯 Core Functionality

### 1. **Data Collection** (`worldsmood_gdelt.py`)
- **Source:** GDELT Project API (Global Database of Events, Language, and Tone)
- **Coverage:** 193 countries, 100+ languages
- **Strategy:** 3-pass system for maximum coverage:
  - Pass 1: Last 24 hours (preferred)
  - Pass 2: Last 7 days (fallback)
  - Pass 3: Last 30 days (final fallback)
- **Output:** 
  - `prevalent_words_gdelt_YYYYMMDD.csv` - Top words per country
  - `headlines_data.json` - Raw headlines grouped by country
- **Blacklist System:** Filters out news source names and spam (`news_blacklist.json`)

### 2. **Sentiment Analysis** (`sentiment_analysis.py`)
- **Model:** DistilBERT transformer (context-aware AI)
- **Upgrade:** Replaced VADER (keyword-based) with DistilBERT for 70% better accuracy
- **Categories:** Good, Bad, Neutral news
- **Threshold:** 70% confidence required for good/bad classification
- **Output:** `sentiment_analysis.json` with per-headline classifications

### 3. **Data Processing** (`generate_country_data.py`)
- **Combines:** Prevalent words + sentiment analysis
- **Color Algorithm:** 
  - Sentiment balance: `Good% - Bad%`
  - 3x multiplier for visual contrast
  - Maps to grey value: -150 (black) → 0 (grey) → +150 (white)
  - Minimum 10 articles required for reliable sentiment
- **Output:** `country_data.json` with grey values for globe coloring

### 4. **Interactive Globe** (`index.html`)
- **Library:** Globe.gl (WebGL-powered 3D globe)
- **Features:**
  - **Auto-rotation** with smooth animations
  - **Country labels** showing most prevalent word
  - **Dynamic text color** (black on light, white on dark)
  - **Click interactions** to view country details
  - **Sentiment popup** with good/bad/neutral percentages
  - **Radio Garden integration** - links to local radio stations
  - **Headlines viewer** - color-coded by sentiment
  - **Settings panel** with colorblind mode toggle
  - **Help panel** with historical sentiment graph
  - **Time travel button** for future historical data viewing

---

## 🎨 Design Choices

### Visual Design
- **Minimalist aesthetic:** White ocean, no atmosphere, clean typography
- **High contrast:** Pure black/white text with no transparency
- **Color scheme:** 
  - Normal: Green (good) / Red (bad) / Grey (neutral)
  - Colorblind: Blue (good) / Orange (bad) / Grey (neutral)
- **Typography:** Times New Roman (classic, readable)
- **Animations:** Smooth 4-second fade-in, sigmoid curve for zoom transitions

### UX Decisions
- **Auto-rotation:** Stops on first user interaction
- **Header/footer hide:** Dynamically slide away when zooming in
- **Clickable everything:** Countries, labels, and headlines all interactive
- **External links:** Headlines open Google search for context
- **Rounded corners:** 8px on all popups for modern feel
- **Minimalistic icons:** Grayscale, low opacity until hover

### Data Strategy
- **Quality over quantity:** 10-article minimum for sentiment reliability
- **Blacklist filtering:** Removes spam and news outlet names
- **Duplicate removal:** Filters identical headlines
- **Timeframe indicators:** Shows if data is from 24h/7d/30d ago
- **Low confidence:** Countries with <10 articles show as 50% grey

### Performance
- **Globe optimization:**
  - Hardware acceleration enabled
  - Label resolution: 2 (balance quality/speed)
  - 60 FPS target for rotation
  - Throttled rendering during interactions
- **Data caching:** localStorage for historical data and settings
- **Lazy loading:** Model downloads only once (~250MB)

---

## 📁 File Structure

### Essential Files
```
worldsmood_gdelt.py          # Fetches news from GDELT API
sentiment_analysis.py         # Classifies headlines with DistilBERT
generate_country_data.py      # Combines data and calculates colors
save_historical_snapshot.py   # Archives daily data snapshots
index.html                    # Interactive globe website
news_blacklist.json          # Filters for spam/outlet names
requirements.txt             # Python dependencies
README.md                    # Documentation
```

### Generated Data (gitignored but deployed)
```
country_data.json            # Main data for globe (with sentiment)
headlines_data.json          # Raw headlines per country
sentiment_analysis.json      # Per-headline classifications
prevalent_words_gdelt_*.csv  # Daily word analysis results
```

### Archive
```
history/                     # Timestamped daily snapshots
```

---

## 🔄 Daily Workflow

1. **Run data collection:**
   ```bash
   py worldsmood_gdelt.py
   ```
   → Fetches latest news, filters blacklist, finds prevalent words

2. **Run sentiment analysis:**
   ```bash
   py sentiment_analysis.py
   ```
   → Classifies all headlines using DistilBERT

3. **Generate final data:**
   ```bash
   py generate_country_data.py
   ```
   → Combines everything, calculates grey values

4. **Archive snapshot:**
   ```bash
   py save_historical_snapshot.py
   ```
   → Saves timestamped copy to history/

5. **Deploy to GitHub Pages:**
   ```bash
   git add country_data.json headlines_data.json sentiment_analysis.json
   git commit -m "Update: YYYY-MM-DD"
   git push
   ```
   → Site updates automatically at `https://oskarengl.github.io/worlds-mood/`

---

## 🛠️ Tech Stack

### Backend
- **Python 3.14**
- **Transformers** - DistilBERT for sentiment analysis
- **PyTorch** - Deep learning backend
- **NLTK** - Text preprocessing
- **Pandas** - Data manipulation
- **Requests** - API calls to GDELT

### Frontend
- **Globe.gl** - 3D WebGL globe rendering
- **Topojson** - Geographical data processing
- **Vanilla JavaScript** - No framework dependencies
- **CSS3** - Animations and styling
- **localStorage** - Client-side data persistence

### Data Source
- **GDELT Project** - 30TB+ database of global news
- **Radio Garden API** - Local radio station links

---

## 📊 Key Metrics

- **Countries:** 182/193 (94.3% coverage)
- **Articles per run:** ~4,500 headlines
- **Sentiment accuracy:** 70%+ (DistilBERT vs 40% VADER)
- **Update frequency:** Manual (can be automated)
- **Model size:** 250MB (one-time download)
- **Processing time:** ~5-10 minutes total

---

## 🎯 Future Enhancements

1. **Time travel feature** - Full historical data viewer
2. **Automation** - GitHub Actions for daily updates
3. **API endpoint** - Serve sentiment data via REST API
4. **Mobile optimization** - Touch gestures and responsive design
5. **Regional sentiment** - Sub-country level analysis
6. **Trend detection** - Alert on unusual sentiment shifts
7. **Multi-language support** - UI translations

---

## 📝 Notes

- **Colorblind mode:** Blue/orange replaces green/red (persists in localStorage)
- **Help panel:** Fixed positioning with smooth slide-in animation
- **Close buttons:** Consistent ×/› icons across all popups
- **Text contrast:** Dynamic brightness (50-180 range) for readability
- **Country borders:** Adaptive contrast based on fill color
- **Radio links:** Auto-redirect to capital city on radio.garden

---

## 🔐 Privacy & Ethics

- No user tracking or analytics
- No cookies or personal data collection
- All data from public GDELT API
- Sentiment analysis runs locally
- Client-side only (except GDELT API calls)

---

**Last Updated:** November 6, 2025  
**Version:** 2.0 (DistilBERT upgrade)  
**License:** MIT

