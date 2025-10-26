@echo off
REM Deploy to Netlify after updating data
REM Make sure you have Git configured and connected to your Netlify site

cd /d "%~dp0"

echo ============================================================
echo   DEPLOYING TO NETLIFY
echo ============================================================
echo.

REM Check if git is initialized
if not exist ".git" (
    echo ERROR: Git not initialized. Run 'git init' first.
    pause
    exit /b 1
)

echo Adding updated files...
git add index.html country_data.json

echo Committing changes...
git commit -m "Auto update: %date% %time%"

echo Pushing to repository...
git push

echo.
echo ============================================================
echo   DEPLOYMENT COMPLETE!
echo   Netlify will auto-deploy in a few moments.
echo ============================================================
echo.

exit /b 0

