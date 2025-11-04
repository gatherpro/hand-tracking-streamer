@echo off
echo ========================================
echo Hand Tracking Streamer - Test Mode
echo ========================================
echo.

REM 仮想環境確認
if not exist "venv312\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found.
    echo Please run setup_python312.bat first!
    echo.
    pause
    exit /b 1
)

REM 仮想環境有効化
call venv312\Scripts\activate.bat

echo Running tests...
echo ========================================
echo.

REM 全テスト実行
pytest tests/ -v

echo.
echo ========================================
echo Tests complete
echo ========================================
echo.

call venv312\Scripts\deactivate.bat

pause
