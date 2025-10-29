@echo off
title Python Project Runner



:: Step 2: Virtual environment activate karo
echo [2/4] Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo ❌ Error in activating virtual environment!
    pause
    exit /b
)

:: Step 3: Requirements install karo
echo [3/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error in installing dependencies!
    pause
    exit /b
)

:: Step 4: Run run.py
echo [4/4] Starting run.py...
python run.py

echo ✅ run.py finished, terminal will stay open.
cmd /k