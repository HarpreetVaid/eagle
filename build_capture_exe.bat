@echo off
echo ==============================================
echo EAGLE CAPTURE - WINDOWS EXECUTABLE BUILDER
echo ==============================================
echo This script will install dependencies and build eagle_capture.exe
echo Make sure you have Python installed on Windows!
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH!
    echo Please install Python from python.org and try again.
    pause
    exit /b
)

echo [1/3] Installing required Python libraries...
pip install pynput mss requests plyer pyinstaller

echo.
echo [2/3] Building the executable...
pyinstaller --onefile --noconsole --name "EagleCapture" eagle_capture.py

echo.
echo [3/3] Cleaning up build files...
rmdir /s /q build
del EagleCapture.spec

echo.
echo ==============================================
echo Build Complete!
echo You can find your new EagleCapture.exe in the 'dist' folder.
echo You can drag EagleCapture.exe to your Desktop or Taskbar.
echo ==============================================
pause
