@echo off
echo ========================================
echo Hand Tracking Streamer (Python 3.12)
echo ========================================
echo.

REM 仮想環境確認
if not exist "venv312\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found.
    echo.
    echo Please run setup_python312.bat first!
    echo.
    pause
    exit /b 1
)

REM 仮想環境有効化
echo Activating Python 3.12 environment...
call venv312\Scripts\activate.bat
echo.

REM アプリケーション実行
echo Starting Hand Tracking Streamer...
echo ========================================
echo.
echo Press Ctrl+C to stop the application
echo.

python src/main.py

REM 終了処理
echo.
echo ========================================
echo Application stopped
echo ========================================
echo.

REM 環境を非アクティブ化
call venv312\Scripts\deactivate.bat

pause
