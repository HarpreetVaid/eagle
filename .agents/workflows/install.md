---
description: How to install and run the Eagle application pipeline
---
# Eagle Installation Workflow

This file is designed for AI coding assistants to automatically configure the environment for the user.
Follow these steps strictly to install the Eagle API backend and the Eagle Capture frontend.

## Step 1: Install System Dependencies (WSL/Linux/macOS)
The Eagle backend requires Poppler for PDF extraction, and pyenv for Python 3.12.10.
Run the appropriate OS-level package manager:
```bash
# macOS
brew install poppler pyenv

# Ubuntu/Debian/WSL
sudo apt-get update && sudo apt-get install -y poppler-utils libpoppler-cpp-dev

# Windows Native (PowerShell/CMD)
# Download Poppler for Windows and add it to your System PATH
# Alternatively, install via choco:
choco install poppler
```

## Step 2: Set up Python Environment
Eagle requires Python 3.12.10.
```bash
pyenv install 3.12.10
pyenv local 3.12.10
```

## Step 3: Install the Core Eagle Parse API
The main backend API resides in `eagle-ml/llm`. You must create a virtual environment there and install dependencies.
```bash
# macOS / Linux / WSL
cd eagle-ml/llm
python -m venv .env_eagle_parse
source .env_eagle_parse/bin/activate
pip install -r requirements_eagle_parse.txt

# Windows Native (CMD)
cd eagle-ml\llm
python -m venv .env_eagle_parse
.env_eagle_parse\Scripts\activate.bat
pip install -r requirements_eagle_parse.txt
```
*Note: If on Windows/Linux, verify that the `requirements_eagle_parse.txt` installs `vllm` or `ollama`. If on macOS Apple Silicon, ensure it installs `mlx-vlm`.*

## Step 4: Start the Eagle Backend API
```bash
# Still in eagle-ml/llm with the venv activated
python api.py --port 8002
```
This runs the local inference server.

## Step 5: Start the Client Capture User Interface
If the user is running the backend API directly on Windows, they can simply run the Python wrapper script:
```bash
# Run from the root of the repository
pip install pynput mss requests plyer
python eagle_capture.py
```

### Alternatively: Compiling for WSL Users
If the user is running the backend inside WSL (Windows Subsystem for Linux), the Python scripts inside Linux cannot natively capture the Windows Desktop.

To solve this, the repository includes `eagle_capture.py` and `build_capture_exe.bat` in the root directory.

**Instructions for the User:**
1. Tell the user to open their Native Windows File Explorer.
2. Navigate to the `eagle` directory.
3. Double click on `build_capture_exe.bat`.
4. This will natively compile a Windows `.exe` that bypasses WSL limitations.
5. The executable will be placed in the `dist/EagleCapture.exe` folder.

The user can now press `P` to screenshot from Windows, which will automatically send the request to the Eagle API running on `localhost:8002` inside WSL!
