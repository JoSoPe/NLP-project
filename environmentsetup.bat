@echo off
:: Set up the directory structure
echo Creating folder structure...
if not exist "audio" mkdir audio
if not exist "processed_mp3" mkdir processed_mp3  :: Create the processed_mp3 folder

:: Check if Python is installed
echo Checking for Python installation...
where python > nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and add it to the PATH.
    exit /b 1
)

:: Set up a virtual environment if not already present
echo Setting up virtual environment...
if not exist "venv\Scripts\activate" (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

:: Activate the virtual environment
call venv\Scripts\activate

:: Upgrade pip to make sure we're using the latest version
echo Upgrading pip...
pip install --upgrade pip

:: Install required libraries using requirements.txt
echo Installing required Python libraries...
pip install -r requirements.txt

:: Install additional necessary libraries
echo Installing scikit-learn...
pip install scikit-learn

:: Check if FFmpeg is installed (optional check)
echo Checking for FFmpeg installation...
ffmpeg -version > nul 2>nul
if %errorlevel% neq 0 (
    echo FFmpeg is not installed or not in the PATH. Please install it manually from https://ffmpeg.org/download.html and add it to your PATH.
    exit /b 1
)

:: Final instructions
echo All required libraries are installed. You can now run the project.

:: Deactivate virtual environment
deactivate

pause