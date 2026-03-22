@echo off
chcp 65001 >nul
echo ===================================================
echo    UMBRELLA - ONE FILE BUILD
echo ===================================================
echo.
echo NOTE: This creates a single EXE but may have issues
echo with tls_client DLLs. Use build_umbrella.bat for
echo folder mode if this fails.
echo.
pause

echo [1/4] Installing build dependencies...
..\venv\Scripts\python.exe -m pip install pyinstaller pillow

echo.
echo [2/4] Creating icon...
..\venv\Scripts\python.exe create_icon.py

echo.
echo [3/4] Building single file...
..\venv\Scripts\python.exe -m PyInstaller Umbrella.spec --clean --noconfirm

echo.
echo [4/4] Done!
if exist "dist\Umbrella.exe" (
    echo SUCCESS: dist\Umbrella.exe
) else (
    echo FAILED - Try build_umbrella.bat instead
)

pause
