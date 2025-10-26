# Automatic Daily Updates Setup Guide

## 🎯 Goal
Make your World News Globe automatically update every day with fresh news data and deploy to Netlify.

---

## ⚙️ Setup Methods

### Method 1: Windows Task Scheduler (Recommended)

This will run the update script automatically every day at a time you choose.

#### Step-by-Step Instructions:

1. **Press `Win + R`** and type `taskschd.msc`, press Enter

2. **Click "Create Basic Task"** in the right panel

3. **Name it:** `World News Globe Daily Update`

4. **Trigger:** Select "Daily"

5. **Time:** Choose when to run (e.g., 6:00 AM)

6. **Action:** Select "Start a program"

7. **Program/script:** Browse to:
   ```
   C:\projects\world news\daily_update.bat
   ```

8. **Start in:** Set to:
   ```
   C:\projects\world news
   ```

9. **Finish** and you're done!

#### Advanced Settings (Optional):

- Right-click your task → **Properties**
- **General tab:** Check "Run whether user is logged on or not"
- **Conditions tab:** Uncheck "Start only if on AC power" (for laptops)
- **Settings tab:** Check "Run task as soon as possible after a scheduled start is missed"

---

### Method 2: Git Auto-Deploy to Netlify

If you want automatic deployment to Netlify after data updates:

#### One-Time Setup:

1. **Initialize Git** (if not already done):
   ```bash
   cd "c:\projects\world news"
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Create GitHub Repository:**
   - Go to https://github.com/new
   - Create a new repository
   - Copy the repository URL

3. **Connect to GitHub:**
   ```bash
   git remote add origin YOUR_GITHUB_URL
   git branch -M main
   git push -u origin main
   ```

4. **Connect Netlify to GitHub:**
   - Go to your Netlify dashboard
   - Click "Add new site" → "Import an existing project"
   - Choose GitHub and select your repository
   - Deploy settings:
     - **Build command:** (leave empty)
     - **Publish directory:** `/`
   - Click "Deploy site"

5. **Enable Automatic Deploys:**
   - In Netlify site settings → Build & deploy
   - Enable "Auto publishing"

#### Daily Workflow:

Now your Task Scheduler can run both scripts:

1. **Edit `daily_update.bat`** and uncomment these lines at the end:
   ```batch
   git add country_data.json index.html
   git commit -m "Daily update %date%"
   git push
   ```

This will automatically push changes to GitHub, which triggers Netlify to redeploy!

---

## 🧪 Testing Your Setup

### Test the update script manually:
```bash
cd "c:\projects\world news"
daily_update.bat
```

### Test the deployment script:
```bash
cd "c:\projects\world news"
deploy_to_netlify.bat
```

---

## 📋 What Gets Updated Automatically

1. ✅ `country_data.json` - Fresh news data
2. ✅ CSV files with word analysis
3. ✅ Netlify deployment (if Git method enabled)

---

## 🔍 Monitoring

### Check if it's working:

1. **Task Scheduler:**
   - Open Task Scheduler
   - Find your task
   - Check "Last Run Result" (should be 0x0 for success)

2. **Check log files:**
   You can modify `daily_update.bat` to save logs:
   ```batch
   daily_update.bat >> update_log.txt 2>&1
   ```

3. **Netlify:**
   - Check your Netlify dashboard for recent deploys
   - Look at deployment timestamps

---

## 🚨 Troubleshooting

### "Task didn't run"
- Check Task Scheduler → your task → Last Run Result
- Make sure computer isn't sleeping at scheduled time
- Check "Run whether user is logged on or not"

### "Script runs but no changes"
- Check Python path in `daily_update.bat`
- Run manually to see error messages
- Check `country_data.json` modification date

### "Git push fails"
- Make sure you're authenticated with GitHub
- Check if remote is configured: `git remote -v`
- Try running `git push` manually first

### "Netlify not updating"
- Verify GitHub repository is connected
- Check Netlify build logs
- Make sure files are actually being pushed to GitHub

---

## 🎛️ Customization

### Change update time:
- Edit your Task Scheduler task
- Go to Triggers → Edit
- Change the time

### Update multiple times per day:
- Create multiple triggers in Task Scheduler
- Or use "Repeat task every X hours"

### Update only certain files:
Edit `daily_update.bat` Git section:
```batch
git add country_data.json
REM Don't add index.html if you want to preserve design changes
```

---

## 📊 Expected Behavior

### Daily at 6:00 AM (or your chosen time):
1. ⏰ Task Scheduler wakes up
2. 🔄 Runs `worldsmood.py` (collects news, ~2-3 min)
3. 📊 Runs `generate_globe_data.py` (creates JSON)
4. 📤 (If enabled) Pushes to GitHub
5. 🚀 (If connected) Netlify auto-deploys
6. ✅ Your website is updated with today's news!

---

## 🎉 You're All Set!

Once configured, your globe will automatically update every day with fresh news data from around the world!

**Need help?** Check the scripts or run them manually to see detailed error messages.

