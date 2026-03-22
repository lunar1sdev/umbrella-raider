@echo off
chcp 65001 >nul
echo ===================================================
echo    UMBRELLA CORPORATION - BUILD SYSTEM
echo ===================================================
echo.

echo [1/4] Installing build dependencies...
..\venv\Scripts\python.exe -m pip install pyinstaller pillow

echo.
echo [2/4] Creating Umbrella Corporation icon...
..\venv\Scripts\python.exe create_icon.py

echo.
echo [3/4] Building Umbrella.exe (Folder Mode)...
..\venv\Scripts\python.exe -m PyInstaller Umbrella_Folder.spec --clean --noconfirm

echo.
echo [4/4] Finalizing...
if exist "dist\Umbrella\Umbrella.exe" (
    echo.
    echo ===================================================
    echo    BUILD SUCCESSFUL!
    echo ===================================================
    echo.
    echo Umbrella.exe created in: dist\Umbrella\Umbrella.exe
    echo.
    echo You can now run: dist\Umbrella\Umbrella.exe
    echo Or copy the entire dist\Umbrella folder
    echo.
) else (
    echo.
    echo ===================================================
    echo    BUILD FAILED!
    echo ===================================================
    echo.
)

pause
