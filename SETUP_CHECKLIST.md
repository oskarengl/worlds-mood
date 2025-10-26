# ✅ Cloud Auto-Update Setup Checklist

Follow these steps to enable **automatic daily updates** that run in the cloud (no computer needed!)

---

## 📝 Quick Checklist

### ☐ Step 1: Create GitHub Account
- Go to https://github.com/signup
- Create free account (if you don't have one)

### ☐ Step 2: Create Repository
- Go to https://github.com/new
- Repository name: `world-news-globe`
- Visibility: **PUBLIC** ⚠️ (required for free automation)
- Do NOT initialize with README
- Click "Create repository"

### ☐ Step 3: Push Your Code
**Option A - Easy Way:**
```powershell
cd "c:\projects\world news"
.\setup_github.bat
```
(Then paste your GitHub repo URL when asked)

**Option B - Manual:**
```powershell
cd "c:\projects\world news"
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/world-news-globe.git
git branch -M main
git push -u origin main
```

### ☐ Step 4: Verify GitHub Actions
- Go to your repo on GitHub
- Click **"Actions"** tab
- You should see "Daily World News Update" workflow
- Click **"Run workflow"** to test it manually

### ☐ Step 5: Connect Netlify
- Go to https://app.netlify.com
- Click **"Add new site"** → **"Import an existing project"**
- Choose **GitHub**
- Select your `world-news-globe` repository
- Build command: (leave empty)
- Publish directory: `/`
- Click **"Deploy site"**

### ☐ Step 6: Test Everything
- Wait for first deploy to finish
- Visit your Netlify URL
- Check if the site works

### ☐ Step 7: Test Auto-Update (Optional)
- Go to GitHub repo → Actions
- Click "Run workflow" manually
- Wait 2-3 minutes
- Check if new commit appears
- Check if Netlify auto-deploys
- Visit your site - data should be fresh!

---

## ✨ Done!

Your globe now updates automatically every day at 6 AM UTC!

**No computer needed. No maintenance. Just works.** 🚀

---

## 🔍 How to Check if It's Working

Every day after 6 AM UTC, check:

1. **GitHub:**
   - New commit with "🌍 Daily update" message
   - Actions tab shows green checkmark

2. **Netlify:**
   - New deploy in Deploys tab
   - Shows "Triggered by GitHub"

3. **Your Website:**
   - Footer shows today's date
   - New words on countries

---

## 🆘 If Something Goes Wrong

1. Check GitHub Actions logs (repo → Actions → click on failed run)
2. Check Netlify deploy logs (dashboard → Deploys → click on deploy)
3. Make sure repo is PUBLIC
4. Make sure Netlify is connected to correct branch (main)

---

## 📚 Reference Files

- `CLOUD_AUTO_UPDATE.md` - Detailed setup guide
- `.github/workflows/daily-update.yml` - The automation script
- `setup_github.bat` - Easy GitHub setup tool

---

**Time to complete:** 10 minutes  
**Cost:** $0 (100% free)  
**Result:** Automatic daily updates forever! ✨

