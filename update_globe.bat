@echo off
REM Quick script to update the World News Globe
REM Usage: Just double-click this file!

echo.
echo ============================================================
echo           WORLD NEWS MOOD GLOBE - UPDATER
echo ============================================================
echo.

cd /d "%~dp0"

set PYTHON=C:\Users\orang\AppData\Local\Programs\Python\Python314\python.exe

echo [1/3] Collecting and analyzing news...
"%PYTHON%" worldsmood.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to run worldsmood.py
    pause
    exit /b 1
)

echo.
echo [2/3] Generating globe data...
"%PYTHON%" generate_globe_data.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to generate globe data
    pause
    exit /b 1
)

echo.
echo [3/3] Starting web server...
echo.
echo ============================================================
echo   SUCCESS! Open your browser to:
echo   http://localhost:8000/minimalist_globe.html
echo ============================================================
echo.
echo Press Ctrl+C to stop the server
echo.

"%PYTHON%" -m http.server 8000


