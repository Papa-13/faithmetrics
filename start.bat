@echo off
echo ==========================================
echo   FaithMetrics - Church Analytics Platform
echo   Quick Start Script (Windows)
echo ==========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.9 or higher.
    pause
    exit /b 1
)

echo √ Python found
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo √ Virtual environment created
) else (
    echo √ Virtual environment already exists
)

echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo √ Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo X Failed to install dependencies
    pause
    exit /b 1
)

echo √ Dependencies installed successfully
echo.

REM Check if data exists
if not exist "data_members.csv" (
    echo Generating synthetic church data...
    python generate_church_data.py
    
    if errorlevel 1 (
        echo X Failed to generate data
        pause
        exit /b 1
    )
    
    echo √ Data generated successfully
) else (
    echo √ Data files already exist
)

echo.
echo ==========================================
echo   Starting FaithMetrics...
echo ==========================================
echo.
echo The application will open in your browser
echo URL: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

REM Run Streamlit
streamlit run faithmetrics_app.py
