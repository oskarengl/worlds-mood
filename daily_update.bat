@echo off
REM Daily automatic update script for World News Globe
REM This runs data collection and optionally deploys to Netlify

cd /d "%~dp0"

set PYTHON=C:\Users\orang\AppData\Local\Programs\Python\Python314\python.exe

echo ============================================================
echo   WORLD NEWS MOOD GLOBE - DAILY UPDATE
echo   %date% %time%
echo ============================================================
echo.

echo [1/2] Collecting and analyzing news...
"%PYTHON%" worldsmood.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to run worldsmood.py
    exit /b 1
)

echo.
echo [2/2] Generating globe data...
"%PYTHON%" generate_globe_data.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to generate globe data
    exit /b 1
)

echo.
echo ============================================================
echo   SUCCESS! Data updated at %time%
echo ============================================================
echo.

REM Optional: Deploy to Netlify (uncomment if using Git)
REM git add country_data.json
REM git commit -m "Daily update %date%"
REM git push

exit /b 0

