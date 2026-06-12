@echo off
title CodeForge AI Launcher
cd /d "%~dp0"
echo ==========================================
echo Starting CodeForge AI Platform...
echo ==========================================

:: Check if virtual environment exists
if exist venv\Scripts\streamlit.exe (
    echo [INFO] Virtual environment detected. Starting Streamlit...
    venv\Scripts\streamlit.exe run app.py
) else if exist .venv\Scripts\streamlit.exe (
    echo [INFO] Virtual environment (.venv) detected. Starting Streamlit...
    .venv\Scripts\streamlit.exe run app.py
) else (
    echo [WARNING] Local virtual environment not detected.
    echo [INFO] Attempting to run using global python/streamlit installation...
    streamlit run app.py
)

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Failed to start Streamlit. Please ensure dependencies are installed.
    echo Run: pip install -r requirements.txt
    echo.
    pause
)
