# 🌍 World News Mood Globe - Project Structure

## ✨ Essential Files Only

### Core Files (Required)

| File | Purpose | When to use |
|------|---------|-------------|
| `worldsmood.py` | Collects RSS feeds & analyzes words | Run daily to update data |
| `generate_globe_data.py` | Converts CSV to JSON | Runs after worldsmood.py |
| `minimalist_globe.html` | The interactive globe | Open in browser via server |
| `country_data.json` | Live data file | Auto-generated, don't edit |
| `prevalent_words_rss_*.csv` | Data backup | Auto-generated |

### Convenience Files

| File | Purpose |
|------|---------|
| `update_globe.bat` | One-click updater (Windows) |
| `check_status.py` | Quick status check |
| `QUICKSTART.md` | User guide |

### Data Storage

| Directory | Contents |
|-----------|----------|
| `photos/` | Screenshots/videos of the globe |

---

## 🚀 Quick Workflow

### Daily Update
```bash
# Windows: Double-click
update_globe.bat

# Or manually:
python worldsmood.py
python generate_globe_data.py
python -m http.server 8000
```

### View Globe
```
http://localhost:8000/minimalist_globe.html
```

### Check Status
```bash
python check_status.py
```

---

## 📁 Clean Structure

```
world news/
├── worldsmood.py              ← Data collector
├── generate_globe_data.py     ← Data converter
├── minimalist_globe.html      ← The globe
├── country_data.json          ← Live data
├── prevalent_words_*.csv      ← Data backup
├── update_globe.bat           ← Quick updater
├── check_status.py            ← Status checker
├── QUICKSTART.md              ← User guide
└── photos/                    ← Screenshots
```

---

## 🎯 Current Status

- **14 countries** with data
- **496 articles** analyzed
- **Minimalist design** - black & white
- **Interactive** - drag, zoom, click
- **Auto-updates** - run update_globe.bat

---

**No clutter. Just the essentials.** ✨



