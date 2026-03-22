@echo off
echo Installing Cwelium dependencies into venv...
echo.

echo Step 1: Installing pip in venv...
..\venv\Scripts\python.exe -m ensurepip --upgrade
..\venv\Scripts\python.exe -m pip install --upgrade pip

echo.
echo Step 2: Installing requirements in venv...
..\venv\Scripts\python.exe -m pip install -r requirements.txt

echo.
echo Installation complete!
pause
