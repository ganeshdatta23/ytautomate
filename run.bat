@echo off
REM Quick run script for Windows

echo ========================================
echo YouTube Automation - Quick Run
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate

REM Install dependencies if needed
if not exist "venv\Lib\site-packages\edge_tts\" (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Run based on argument
if "%1"=="test" (
    echo Running system test...
    python test_system.py
) else if "%1"=="setup" (
    echo Running setup...
    python setup.py
) else if "%1"=="batch" (
    echo Generating batch videos...
    python main.py --mode batch --count %2 --no-upload
) else (
    echo Generating single video...
    python main.py --mode single --no-upload
)

echo.
echo ========================================
echo Done!
echo ========================================
pause
