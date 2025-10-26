@echo off
REM Quick setup script to push project to GitHub
REM This makes setup easier for cloud auto-updates

echo ============================================================
echo   GITHUB SETUP FOR CLOUD AUTO-UPDATES
echo ============================================================
echo.
echo This will push your project to GitHub for automatic updates.
echo.
echo BEFORE RUNNING THIS:
echo 1. Create a repository at https://github.com/new
echo 2. Make it PUBLIC (required for free GitHub Actions)
echo 3. Copy the repository URL
echo.
pause

cd /d "%~dp0"

echo.
echo Initializing Git...
git init
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git not installed. Install from https://git-scm.com/
    pause
    exit /b 1
)

echo.
echo Adding files...
git add .

echo.
echo Creating first commit...
git commit -m "Initial commit: World News Globe with auto-update"

echo.
echo ============================================================
echo   ENTER YOUR GITHUB REPOSITORY URL
echo   Example: https://github.com/yourusername/world-news-globe.git
echo ============================================================
set /p REPO_URL="Repository URL: "

echo.
echo Connecting to GitHub...
git remote add origin %REPO_URL%

echo.
echo Setting branch to main...
git branch -M main

echo.
echo Pushing to GitHub...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo   SUCCESS! 
    echo   Your project is now on GitHub!
    echo.
    echo   NEXT STEPS:
    echo   1. Go to your GitHub repo -^> Actions tab
    echo   2. Click "Run workflow" to test
    echo   3. Connect Netlify to your GitHub repo
    echo   4. Done! Auto-updates every day!
    echo.
    echo   See CLOUD_AUTO_UPDATE.md for detailed instructions.
    echo ============================================================
) else (
    echo.
    echo ============================================================
    echo   ERROR: Failed to push to GitHub
    echo   
    echo   Common fixes:
    echo   - Make sure the repository URL is correct
    echo   - Check if you're logged into GitHub
    echo   - Try: git push -u origin main
    echo ============================================================
)

echo.
pause

