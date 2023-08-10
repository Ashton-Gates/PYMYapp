@echo off

REM Check if Python is installed
python --version > NUL 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.x and try again.
    pause
    exit
)

REM Create a virtual environment (Optional)
python -m venv venv
call venv\Scripts\activate

REM Install required dependencies
pip install email six extract-msg PyMISP

REM Create necessary directories
mkdir C:\pymisp_app

REM Print success message
echo Installation and setup are complete! You can now run your Python script.

pip install --upgrade PyUpdater[all]


pip install cryptography

pip install pyinstaller

pause
