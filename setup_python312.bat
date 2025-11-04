@echo off
echo ========================================
echo Python 3.12 Environment Setup
echo ========================================
echo.

REM 仮想環境作成
echo [1/4] Creating virtual environment with Python 3.12...
py -3.12 -m venv venv312
if errorlevel 1 (
    echo.
    echo ERROR: Python 3.12 not found.
    echo.
    echo Please install Python 3.12 first:
    echo https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe
    echo.
    echo After installation, run this script again.
    echo.
    pause
    exit /b 1
)
echo   --^> Virtual environment created successfully
echo.

REM 仮想環境有効化
echo [2/4] Activating virtual environment...
call venv312\Scripts\activate.bat
echo   --^> Activated
echo.

REM pipアップグレード
echo [3/4] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo   --^> pip upgraded
echo.

REM 依存関係インストール
echo [4/4] Installing dependencies...
echo   (This may take a few minutes...)
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo.
    echo WARNING: Some packages may have failed to install.
    echo Continuing anyway...
    echo.
)
echo   --^> Dependencies installed
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Python 3.12 environment is ready at: venv312\
echo.
echo To run the application:
echo   1. Double-click: run_with_python312.bat
echo   OR
echo   2. Manual:
echo      venv312\Scripts\activate
echo      python src/main.py
echo.
pause
