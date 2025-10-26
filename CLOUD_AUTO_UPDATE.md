# ☁️ Cloud Auto-Update Setup (No Computer Needed!)

Your World News Globe will update **every day automatically in the cloud** - even when your computer is off!

---

## 🎯 How It Works

1. **GitHub Actions** runs in the cloud every day at 6 AM UTC
2. Collects fresh news from around the world
3. Generates new data
4. Pushes changes to your GitHub repository
5. **Netlify** detects the changes and auto-deploys
6. Your website is updated! 🎉

**Cost:** 100% FREE ✨

---

## 📋 Setup Steps (One-Time, 10 minutes)

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `world-news-globe` (or any name you like)
3. Make it **Public** (required for free GitHub Actions)
4. **DO NOT** initialize with README
5. Click "Create repository"

### Step 2: Push Your Project to GitHub

Open PowerShell in your project folder and run:

```powershell
cd "c:\projects\world news"

# Initialize Git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: World News Globe"

# Connect to your GitHub repo (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/world-news-globe.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Important:** Replace `YOUR_USERNAME` and `world-news-globe` with your actual GitHub username and repository name!

### Step 3: Enable GitHub Actions

GitHub Actions is automatically enabled for public repositories. The workflow file (`.github/workflows/daily-update.yml`) will start working immediately!

### Step 4: Connect Netlify to GitHub

1. Go to https://app.netlify.com
2. Click **"Add new site"** → **"Import an existing project"**
3. Choose **"Deploy with GitHub"**
4. Authorize Netlify to access your GitHub
5. Select your `world-news-globe` repository
6. Build settings:
   - **Build command:** (leave empty)
   - **Publish directory:** `/`
7. Click **"Deploy site"**

### Step 5: Enable Auto-Deploy

1. In Netlify, go to **Site settings** → **Build & deploy**
2. Under **Continuous Deployment**, make sure it says "Active"
3. Under **Deploy contexts**, enable "Deploy previews" and "Branch deploys"

**Done!** 🎉

---

## ✅ Testing Your Setup

### Test manually (before waiting 24 hours):

1. Go to your GitHub repository
2. Click **"Actions"** tab
3. Click on **"Daily World News Update"** workflow
4. Click **"Run workflow"** button (on the right)
5. Click green **"Run workflow"**
6. Watch it run! (takes 2-3 minutes)

If successful:
- ✅ You'll see a green checkmark
- ✅ New commit in your repository
- ✅ Netlify will auto-deploy
- ✅ Your site is updated!

---

## 🕐 Schedule (When It Runs)

**Current setting:** Every day at **6:00 AM UTC**

### Convert to Your Timezone:

- **PST (Los Angeles):** 10:00 PM previous day
- **EST (New York):** 1:00 AM
- **CET (Paris/Berlin):** 7:00 AM
- **IST (India):** 11:30 AM
- **AEST (Sydney):** 4:00 PM

### Change the Schedule:

Edit `.github/workflows/daily-update.yml` line 5:

```yaml
- cron: '0 6 * * *'  # Format: 'minute hour day month weekday'
```

Examples:
- `'0 0 * * *'` = Midnight UTC (12 AM)
- `'0 12 * * *'` = Noon UTC (12 PM)
- `'0 18 * * *'` = 6 PM UTC
- `'0 */6 * * *'` = Every 6 hours
- `'0 6 * * 1-5'` = 6 AM UTC, Monday-Friday only

---

## 📊 Monitoring

### Check if it's working:

1. **GitHub Actions:**
   - Go to your repo → **Actions** tab
   - See all runs and their status
   - Green ✅ = success, Red ❌ = failed

2. **Netlify:**
   - Check **Deploys** tab in your Netlify dashboard
   - See automatic deploys triggered by GitHub

3. **Your Website:**
   - Check the "Updated:" timestamp in the footer
   - Should update daily!

---

## 🚨 Troubleshooting

### "Actions not running"
- Make sure repository is **Public** (GitHub Actions free tier requires this)
- Check Actions tab → Workflows → Make sure it's enabled
- Check the cron schedule time

### "Actions failing"
- Click on the failed run to see error logs
- Common issues:
  - RSS feeds timing out (normal, will work next day)
  - Python dependencies missing (check workflow file)

### "Netlify not deploying"
- Check if new commits appear in GitHub
- Verify Netlify is connected to the correct branch (usually `main`)
- Check Netlify deploy logs for errors

### "Website showing old data"
- Hard refresh: `Ctrl + Shift + R` or `Ctrl + F5`
- Check if `country_data.json` was actually updated in GitHub
- Verify the timestamp in the footer

---

## 💰 Costs

- **GitHub Actions:** FREE (2,000 minutes/month for public repos)
- **GitHub Repository:** FREE (unlimited public repos)
- **Netlify Hosting:** FREE (100GB bandwidth/month)

**Total:** $0/month ✨

---

## 🎛️ Advanced Options

### Run Multiple Times Per Day

Edit `.github/workflows/daily-update.yml`:

```yaml
on:
  schedule:
    - cron: '0 6 * * *'   # 6 AM UTC
    - cron: '0 12 * * *'  # Noon UTC
    - cron: '0 18 * * *'  # 6 PM UTC
```

### Add Email Notifications

Add this to your workflow (after installing):

```yaml
- name: Send notification
  if: failure()
  run: |
    echo "Update failed! Check GitHub Actions logs."
    # Add email notification service here
```

### Include More Countries

Edit `worldsmood.py` and change:
```python
MAX_COUNTRIES = 20  # Increase this number
```

Then commit and push the change.

---

## 🎉 What Happens Now

Every single day at 6 AM UTC:

1. ⏰ GitHub Actions wakes up in the cloud
2. 🌍 Collects news from 40+ countries
3. 📊 Analyzes most prevalent words
4. 💾 Updates `country_data.json`
5. 📤 Commits and pushes to GitHub
6. 🚀 Netlify detects changes and deploys
7. ✅ Your website shows fresh data!

**All automatic. No computer needed. Forever.** 🚀

---

## 📱 Next Steps

After setup:
1. ✅ Star your GitHub repo (optional, but cool!)
2. ✅ Share your Netlify URL
3. ✅ Forget about it - it just works!
4. ✅ Check back anytime to see fresh news

---

## ❓ Questions?

- **Check Actions logs:** GitHub repo → Actions tab
- **Check deploy logs:** Netlify dashboard → Deploys
- **Run manual test:** Actions → Run workflow button

**Enjoy your self-updating globe!** 🌍✨

