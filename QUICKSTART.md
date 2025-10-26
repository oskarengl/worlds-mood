# 🌍 World News Mood Globe - Quick Start

## The Simplest Way to Get Started

### Windows Users (EASIEST!)

1. **Double-click** `update_globe.bat`
2. Wait for it to finish (2-3 minutes)
3. Browser will show: `http://localhost:8000/minimalist_globe.html`
4. Done! 🎉

### All Platforms

```bash
# Run the pipeline
python worldsmood.py              # Collect news (2-3 min)
python generate_globe_data.py     # Generate JSON
python -m http.server 8000        # Start server

# Open browser
http://localhost:8000/minimalist_globe.html
```

### Windows - Start Localhost Server Only

**To view `index.html` on localhost:**

```powershell
cd "c:\projects\world news"
py -m http.server 8000
```

Then open: **http://localhost:8000** or **http://localhost:8000/index.html**

*(Note: Use `py` command on Windows, not `python` or `python3`)*

---

## What You'll See

- **A beautiful minimalistic globe** in black & white
- **14 countries** with their most prevalent news words
- **Interactive**: Drag to spin, click countries for details
- **Live data** from today's news (October 24, 2025)

---

## How to Update Data

### Daily Updates

The globe shows whatever is in `country_data.json`. To refresh:

1. Run `update_globe.bat` (Windows)
2. OR run `python worldsmood.py` then `python generate_globe_data.py`
3. Refresh the browser (Ctrl+R)

### Automatic Updates (Optional)

**Windows Task Scheduler:**
- Create task to run `update_globe.bat` daily at 6 AM

**Linux/Mac cron:**
```bash
0 6 * * * cd /path/to/project && python worldsmood.py && python generate_globe_data.py
```

---

## Current Data (as of last run)

```
Countries: 14
Articles: 496
Last updated: 2025-10-24T23:16:10

Sample countries:
  • Spain       -> "periodista"  (Spanish news focus)
  • China       -> "nanjing"     (28% of articles)
  • Russia      -> "rate"        (24% of articles)
  • Brazil      -> "anos"        (Portuguese word)
  • Nigeria     -> "nigeria"     (very common)
```

---

## Files You Need

| File | What it does |
|------|--------------|
| `worldsmood.py` | The brain - collects & analyzes news |
| `generate_globe_data.py` | Converts data to JSON |
| `minimalist_globe.html` | The globe visualization |
| `country_data.json` | Your live data file |
| `update_globe.bat` | One-click updater (Windows) |

---

## Troubleshooting

### "Error loading country data"
→ Run `python worldsmood.py` first

### Globe is empty/white
→ Make sure server is running: `python -m http.server 8000`
→ Access via http:// not file://

### Words look weird
→ Check `check_status.py` to see what data was collected
→ Some RSS feeds have technical issues

### Want more countries?
→ Edit `worldsmood.py` and change `MAX_COUNTRIES = 20` to a higher number

---

## Check Status Anytime

```bash
python check_status.py
```

This shows:
- How many countries have data
- What words were found
- When data was last updated

---

## How It Works

```
RSS Feeds → worldsmood.py → CSV → generate_globe_data.py → JSON → Globe
   ↓           (analyzer)      ↓        (converter)          ↓      ↓
 News        Word Analysis   Data      country_data.json   HTML  Visualization
```

---

## Interactive Features

- **🖱️ Drag**: Rotate the globe
- **🔍 Scroll**: Zoom in/out
- **👆 Click country**: See detailed tooltip with article counts
- **🎯 Release drag**: Globe continues spinning with soft momentum

---

## What the Words Mean

Each word shown is:
- **Most locally prevalent**: Common in that country's news
- **Globally rare**: Not common in other countries
- **Filtered**: Technical artifacts (http, www) removed

Example: "periodista" appears in 4.8% of Spanish articles but rarely elsewhere.

---

## Next Steps

1. ✅ Basic pipeline working
2. ✅ Interactive globe with 14 countries
3. 🎯 **YOU ARE HERE** - Test with more countries
4. 📅 Set up daily automation
5. 🚀 Deploy to web server (optional)

---

## Need Help?

1. Run `python check_status.py` to see what's working
2. Check `PIPELINE_SUMMARY.txt` for technical details
3. Read `PIPELINE_README.md` for full documentation

---

**Made with ❤️ and world news**


