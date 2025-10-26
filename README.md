# 🌍 World's Mood

An interactive globe visualization showing the most prevalent words from global news, updated every 6 hours.

**Live Site:** https://oskarengl.github.io/worlds-mood/

## ✨ Features

- Interactive 3D globe with news words from 40+ countries
- Dynamic opacity based on word prevalence (darker = more confident)
- Auto-updates every 6 hours via GitHub Actions
- Clean, minimalist design with Times New Roman typography

## 🔄 How It Works

1. **GitHub Actions** runs every 6 hours
2. Collects news from RSS feeds worldwide
3. Analyzes most prevalent words per country
4. Updates `country_data.json`
5. GitHub Pages auto-deploys the updated site

## 📁 Project Structure

```
├── index.html                    # Main website
├── country_data.json             # Current news data
├── worldsmood.py                 # News collection & analysis
├── generate_globe_data.py        # Data processing
├── requirements.txt              # Python dependencies
├── .github/workflows/
│   └── daily-update.yml          # Automation workflow
└── CLOUD_AUTO_UPDATE.md          # Detailed setup guide
```

## 🛠️ Local Development

```bash
# Start local server
py -m http.server 8001

# Open browser
http://localhost:8001/index.html
```

## 📊 Update Schedule

Runs automatically at:
- 1 AM German time
- 7 AM German time
- 1 PM German time
- 7 PM German time

Or manually trigger at: https://github.com/oskarengl/worlds-mood/actions

## 🎨 Opacity Gradient

Words appear darker based on prevalence:
- **5% or less**: Very light grey (barely visible)
- **70% or more**: Solid black (high confidence)
- **Between**: Quadratic gradient curve

## 📝 License

Free to use and modify.

---

**Made with ❤️ and global news**


