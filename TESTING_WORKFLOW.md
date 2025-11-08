# Testing GitHub Actions Workflow

## Manual Trigger Steps

1. **Go to GitHub Repository**
   - Navigate to: `https://github.com/YOUR_USERNAME/YOUR_REPO`

2. **Open Actions Tab**
   - Click on "Actions" tab at the top

3. **Select Workflow**
   - In the left sidebar, click "Daily World News Update"

4. **Run Workflow**
   - Click the "Run workflow" dropdown button
   - Select branch (usually `main` or `master`)
   - Click green "Run workflow" button

5. **Monitor Progress**
   - Watch the workflow run in real-time
   - Click on the running workflow to see detailed logs
   - Each step will show output as it executes

## What to Look For

### ✅ Success Indicators:
- All steps show green checkmarks
- "Collect news and analyze" step completes
- "Analyze sentiment" step completes  
- "Generate globe data" step completes
- "Commit and push if changed" step completes
- New commit appears in repository with message like "🌍 Daily update: 2025-01-XX XX:XX"

### ❌ Failure Indicators:
- Red X mark on any step
- Error messages in the step logs
- No new commit created

## Checking Generated Files

After a successful run, verify these files exist in your repository:
- `country_data.json` - Should be updated with latest data
- `headlines_data.json` - Should contain latest headlines
- `prevalent_words_gdelt_YYYYMMDD.csv` - Should have today's date
- `sentiment_analysis.json` - Should contain sentiment classifications

## Viewing Logs

1. Click on a workflow run
2. Click on a specific job ("update-globe")
3. Expand any step to see detailed output:
   - Checkout repository
   - Set up Python
   - Install dependencies
   - Collect news and analyze
   - Analyze sentiment
   - Generate globe data
   - Commit and push if changed

## Scheduled Runs

The workflow runs automatically every 6 hours:
- 00:00 UTC
- 06:00 UTC
- 12:00 UTC
- 18:00 UTC

To verify scheduled runs are working:
- Check Actions tab for runs at these times
- Note: First scheduled run happens after the workflow file is pushed to default branch

## Troubleshooting

### Workflow doesn't appear in Actions tab
- Make sure the `.github/workflows/daily-update.yml` file is committed and pushed
- Check that it's on the default branch (main/master)

### Workflow fails at "Generate globe data"
- Check if `sentiment_analysis.json` exists (should be created by previous step)
- Check if `prevalent_words_gdelt_*.csv` exists (should be created by news collection step)
- Review error logs in the step output

### No commit is created
- Check if files actually changed (workflow only commits if there are changes)
- Review "Commit and push if changed" step logs
- Verify repository permissions allow writing

### Dependencies fail to install
- Check `requirements.txt` exists and is valid
- Review "Install dependencies" step logs for specific package errors

