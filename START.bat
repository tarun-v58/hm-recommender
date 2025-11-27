@echo off
REM ============================================
REM H&M RECOMMENDER - PERMANENT STARTUP
REM ============================================

setlocal enabledelayedexpansion

REM Kill any existing processes
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
timeout /t 3 >nul

cls
echo.
echo ============================================
echo H^&M RECOMMENDER - STARTUP SCRIPT
echo ============================================
echo.

REM Start Backend
echo Starting Backend (Flask on port 5000)...
start "HM_BACKEND" cmd /k "cd /d c:\Users\tarun\Desktop\hm-recommender\backend && python app.py"
timeout /t 4 >nul

REM Start Frontend
echo Starting Frontend (React on port 3000)...
start "HM_FRONTEND" cmd /k "cd /d c:\Users\tarun\Desktop\hm-recommender\frontend && npm start"
timeout /t 6 >nul

cls
echo.
echo ============================================
echo SUCCESS - WEBSITE IS READY
echo ============================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo OPENING WEBSITE IN BROWSER...
echo.
timeout /t 2 >nul

REM Open the website
start http://localhost:3000

echo Website should open automatically.
echo Keep this window open while using the website.
echo.
pause
