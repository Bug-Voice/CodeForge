@echo off
title DevSentry AI Pipeline Launcher
setlocal enabledelayedexpansion

:: Check if the Python launcher 'py' is installed
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] The Python launcher 'py' is not installed or not added to your PATH.
    echo Please install Python 3.10+ and check "Add Python to PATH" or install the launcher.
    pause
    exit /b
)

:: Activate Virtual Environment if it exists
if exist "%~dp0venv\Scripts\activate.bat" (
    echo [INFO] Activating virtual environment...
    call "%~dp0venv\Scripts\activate.bat"
) else (
    echo [WARNING] Virtual environment 'venv' not found. Running with global py...
)

:: Check if a file was drag-and-dropped onto the batch file
if "%~1" neq "" (
    set "TARGET_FILE=%~1"
    echo [INFO] Target acquired from drag-and-drop: !TARGET_FILE!
    goto run_pipeline
)

:: Prompt user for the target file
echo ==============================================
echo       DevSentry Autonomous AI Dev Team       
echo ==============================================
echo.
set /p "TARGET_FILE=Enter the path of the file to secure (or drag and drop it here): "

:: Remove quotes if the user dragged and dropped into the prompt
set "TARGET_FILE=!TARGET_FILE:"=!"

:run_pipeline
if not exist "!TARGET_FILE!" (
    echo.
    echo [ERROR] File not found: !TARGET_FILE!
    echo Please check the path and try again.
    echo.
    pause
    exit /b
)

echo.
echo Running pipeline on: !TARGET_FILE!
echo ==============================================
py "%~dp0main.py" "!TARGET_FILE!"
echo ==============================================
echo.
echo Pipeline execution complete.
pause
