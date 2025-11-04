# Python 3.12 セットアップガイド

完全な手検出機能を使用するには、Python 3.12が必要です。

## 📥 インストール手順

### ステップ1: Python 3.12をダウンロード

ブラウザが自動的に開きます。開かない場合は以下のURLにアクセス：
```
https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe
```

### ステップ2: インストール

1. ダウンロードした`python-3.12.8-amd64.exe`を実行
2. **重要**: "Add Python 3.12 to PATH"にチェック
3. "Install Now"をクリック
4. インストール完了を待つ

### ステップ3: インストール確認

新しいターミナルを開いて：
```bash
py -3.12 --version
# または
python3.12 --version
```

Python 3.12.8と表示されればOK

---

## 🚀 完全テストの実行

### ステップ1: 仮想環境作成（推奨）

```bash
cd C:\Users\81905\Documents\hand-tracking-streamer

# Python 3.12で仮想環境を作成
py -3.12 -m venv venv312

# 仮想環境を有効化
venv312\Scripts\activate

# プロンプトが(venv312)になることを確認
```

### ステップ2: 依存関係インストール

```bash
# 仮想環境内で
pip install --upgrade pip
pip install -r requirements.txt
```

### ステップ3: システムテスト実行

```bash
# 完全なシステムテスト
python src/main.py
```

---

## 📝 現在のセットアップスクリプト

セットアップを自動化するスクリプトを作成しました：

### `setup_python312.bat`

```batch
@echo off
echo Python 3.12 Environment Setup
echo ================================
echo.

REM 仮想環境作成
echo [1/4] Creating virtual environment with Python 3.12...
py -3.12 -m venv venv312
if errorlevel 1 (
    echo ERROR: Python 3.12 not found. Please install Python 3.12 first.
    pause
    exit /b 1
)
echo   -> Virtual environment created

REM 仮想環境有効化
echo [2/4] Activating virtual environment...
call venv312\Scripts\activate.bat
echo   -> Activated

REM pipアップグレード
echo [3/4] Upgrading pip...
python -m pip install --upgrade pip
echo   -> pip upgraded

REM 依存関係インストール
echo [4/4] Installing dependencies...
pip install -r requirements.txt
echo   -> Dependencies installed

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo To use this environment:
echo   1. Open a new terminal
echo   2. Run: venv312\Scripts\activate
echo   3. Run: python src/main.py
echo.
pause
```

### `run_with_python312.bat`

```batch
@echo off
echo Starting Hand Tracking Streamer with Python 3.12
echo ================================================
echo.

REM 仮想環境確認
if not exist "venv312\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found.
    echo Please run setup_python312.bat first.
    pause
    exit /b 1
)

REM 仮想環境有効化
call venv312\Scripts\activate.bat

REM アプリケーション実行
echo Starting application...
echo.
python src/main.py

REM 終了時に環境を非アクティブ化
deactivate

pause
```

---

## 🎯 クイックスタート（Python 3.12インストール後）

```bash
# 1. セットアップスクリプト実行
setup_python312.bat

# 2. アプリケーション実行
run_with_python312.bat
```

---

## ⚠️ トラブルシューティング

### Python 3.12が見つからない

```bash
# インストール確認
py --list

# Python 3.12がリストにない場合は再インストール
```

### MediaPipeインストール失敗

```bash
# 仮想環境を再作成
rmdir /s venv312
py -3.12 -m venv venv312
venv312\Scripts\activate
pip install -r requirements.txt
```

### カメラが動作しない

- カメラが他のアプリで使用中でないか確認
- `config.yaml`の`device_id`を変更してみる（0 → 1など）

---

## 📚 参考情報

- Python 3.12公式: https://www.python.org/downloads/release/python-3128/
- MediaPipe公式: https://google.github.io/mediapipe/
- プロジェクトREADME: `README.md`

---

## 🎉 完了後

Python 3.12環境で実行すると、以下が全て動作します：

1. ✅ カメラキャプチャ
2. ✅ 手の検出（MediaPipe）
3. ✅ 関節距離計測
4. ✅ データ送信
5. ✅ 統合システム

完全な手検出システムをお楽しみください！
