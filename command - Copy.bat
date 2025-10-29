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


:: Step 4: Run app.py
echo [4/4] Starting app.py...
python app.py

echo ✅ app.py finished, terminal will stay open.
cmd /k