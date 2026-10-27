@echo off
echo Starting Text-to-SQL Generator...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate

REM Check if database exists
if not exist "business_data.db" (
    echo Initializing database...
    python database.py
    echo.
)

REM Start Streamlit app
echo Starting Streamlit application...
streamlit run app.py

pause
