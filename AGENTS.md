# Multi-Agent Development Guide

## 🎯 各エージェントの指示の場所

**重要**: 各エージェントは自分のworktreeを開いたら、以下を確認してください：
1. **このファイル (AGENTS.md)** - 自分の役割と担当モジュールの詳細
2. **TODO.md** - 自分のworktree内の具体的なタスクリスト
3. **担当ファイル** - src/内の自分が編集するPythonファイル

---

## 📋 Agent1: Camera Capture Module

**Branch**: `feature/camera-capture`
**Worktree**: `agent1-worktree/`
**担当ファイル**: `src/camera_capture.py`

### 役割
固定カメラからのリアルタイム映像取得を担当します。

### 実装すべき機能
1. **CameraCapture クラスの実装**
   - カメラの初期化（OpenCV VideoCapture）
   - フレームの取得とバッファ管理
   - カメラ設定の読み込み（config.yaml）
   - エラーハンドリング（カメラが開けない、フレーム取得失敗など）

2. **主要メソッド**
   ```python
   - __init__(config): カメラ初期化
   - start(): キャプチャ開始
   - get_frame(): フレーム取得
   - stop(): カメラ解放
   - is_opened(): カメラ状態確認
   ```

3. **技術要件**
   - OpenCVを使用
   - config.yamlから設定を読み込む
   - マルチスレッド対応（必要に応じて）
   - 適切なエラーメッセージ

### テスト
- `tests/test_camera_capture.py` にユニットテストを作成
- 実際のカメラでの動作確認

---

## 🤚 Agent2: Hand Detection & Tracking Module

**Branch**: `feature/hand-detection`
**Worktree**: `agent2-worktree/`
**担当ファイル**: `src/hand_detector.py`

### 役割
MediaPipe Handsを使用して手の検出と21個のランドマーク取得を担当します。

### 実装すべき機能
1. **HandDetector クラスの実装**
   - MediaPipe Handsの初期化
   - フレームから手の検出
   - 21個のランドマーク座標の取得
   - 複数の手の対応

2. **主要メソッド**
   ```python
   - __init__(config): MediaPipe初期化
   - detect(frame): 手を検出してランドマークを返す
   - draw_landmarks(frame, landmarks): デバッグ用描画
   - get_hand_count(results): 検出された手の数
   ```

3. **技術要件**
   - MediaPipe Hands使用
   - config.yamlからモデル設定を読み込む
   - ランドマークの座標正規化
   - 左右の手の区別

4. **出力データ形式**
   ```python
   {
       "hand_count": 1,
       "hands": [
           {
               "label": "Right",
               "landmarks": [[x1, y1, z1], [x2, y2, z2], ...],  # 21 points
               "confidence": 0.95
           }
       ],
       "timestamp": "2025-11-05T00:00:00"
   }
   ```

### テスト
- `tests/test_hand_detector.py` にユニットテストを作成
- サンプル画像での検出テスト

---

## 📏 Agent3: Joint Measurement & Data Processing Module

**Branch**: `feature/joint-measurement`
**Worktree**: `agent3-worktree/`
**担当ファイル**: `src/joint_measurement.py`

### 役割
手のランドマークから関節間の距離を計算し、データを整形します。

### 実装すべき機能
1. **JointMeasurement クラスの実装**
   - ランドマーク間の距離計算
   - ユークリッド距離の算出
   - 単位変換（ピクセル → cm）
   - データの正規化とバリデーション

2. **主要メソッド**
   ```python
   - __init__(config): 設定読み込み
   - calculate_distances(landmarks): 距離計算
   - normalize_data(data): データ正規化
   - format_output(measurements): 出力フォーマット整形
   ```

3. **技術要件**
   - NumPyを使用して効率的な計算
   - config.yamlから測定対象の関節ペアを読み込む
   - スケールファクターによる実寸への変換
   - 異常値の検出とフィルタリング

4. **出力データ形式**
   ```python
   {
       "hand_id": 0,
       "measurements": {
           "wrist_to_thumb": {"distance": 12.5, "unit": "cm"},
           "wrist_to_index": {"distance": 15.3, "unit": "cm"},
           "wrist_to_middle": {"distance": 16.8, "unit": "cm"},
           "wrist_to_ring": {"distance": 15.1, "unit": "cm"},
           "wrist_to_pinky": {"distance": 13.2, "unit": "cm"}
       },
       "timestamp": "2025-11-05T00:00:00"
   }
   ```

### テスト
- `tests/test_joint_measurement.py` にユニットテストを作成
- 既知の座標での距離計算検証

---

## 📤 Agent4: Data Sender Module

**Branch**: `feature/data-sender`
**Worktree**: `agent4-worktree/`
**担当ファイル**: `src/data_sender.py`

### 役割
計測データをWEBアプリケーションに送信します。

### 実装すべき機能
1. **DataSender クラスの実装**
   - REST API または WebSocketでのデータ送信
   - 接続管理と再接続処理
   - リトライロジック
   - データのシリアライゼーション

2. **主要メソッド**
   ```python
   - __init__(config): 送信設定の初期化
   - connect(): WEBアプリへの接続
   - send_data(data): データ送信
   - disconnect(): 接続終了
   - is_connected(): 接続状態確認
   ```

3. **技術要件**
   - requestsライブラリ（REST API）またはwebsocketsライブラリ
   - JSONフォーマットでデータ送信
   - エラーハンドリングとリトライ機能
   - タイムアウト設定

4. **送信データ例**
   ```json
   {
       "timestamp": "2025-11-05T00:00:00",
       "hand_data": {
           "hand_count": 1,
           "measurements": [
               {
                   "hand_id": 0,
                   "label": "Right",
                   "joints": {
                       "wrist_to_thumb": 12.5,
                       "wrist_to_index": 15.3
                   }
               }
           ]
       }
   }
   ```

### テスト
- `tests/test_data_sender.py` にユニットテストを作成
- モックサーバーでの送信テスト

---

## 🎮 Agent5: Main Controller & Integration

**Branch**: `feature/main-controller`
**Worktree**: `agent5-worktree/`
**担当ファイル**: `src/main.py`

### 役割
全モジュールを統合し、メインループを実装します。

### 実装すべき機能
1. **メインアプリケーションの実装**
   - 各モジュールの初期化
   - メインループの実装
   - 全体のフロー制御
   - 設定管理とロギング

2. **主要コンポーネント**
   ```python
   - load_config(): config.yaml読み込み
   - setup_logging(): ロギング設定
   - main_loop(): メインループ
   - handle_shutdown(): 終了処理
   ```

3. **処理フロー**
   ```
   1. 設定読み込み
   2. 各モジュール初期化
   3. カメラ起動
   4. WEBアプリ接続
   5. ループ開始:
      - フレーム取得
      - 手検出
      - 距離計測
      - データ送信
   6. 終了処理
   ```

4. **技術要件**
   - PyYAMLで設定管理
   - python-json-loggerでロギング
   - 適切なエラーハンドリング
   - Ctrl+Cでの正常終了

5. **統合テスト**
   - 各モジュールが正しく連携するか確認
   - エンドツーエンドのテスト
   - パフォーマンステスト

### テスト
- `tests/test_integration.py` に統合テストを作成
- 全体の動作確認

---

## 🔄 開発ワークフロー

### 1. 各エージェントの作業開始
```bash
# 自分のworktreeディレクトリで作業
cd agent{N}-worktree/
# TODO.mdを確認
cat TODO.md
# 作業開始
```

### 2. 開発とテスト
```bash
# 担当ファイルを編集
# テストを書く
pytest tests/test_{module}.py
```

### 3. コミットとプッシュ
```bash
git add src/{your_file}.py tests/test_{your_file}.py
git commit -m "feat: implement {feature}"
git push origin feature/{your-branch}
```

### 4. プルリクエスト作成
```bash
gh pr create --title "{Feature name}" --body "実装内容の説明"
```

---

## 📦 モジュール間の依存関係

```
main.py (Agent5)
  ├── camera_capture.py (Agent1) ← フレーム提供
  ├── hand_detector.py (Agent2) ← ランドマーク検出
  ├── joint_measurement.py (Agent3) ← 距離計算
  └── data_sender.py (Agent4) ← データ送信
```

各エージェントは独立して開発できますが、インターフェースを統一してください。

---

## ✅ 完了条件

各エージェントは以下を満たした時点で完了とします：
1. 担当ファイルが実装完了
2. ユニットテストがパス
3. ドキュメント（docstring）が記述されている
4. プルリクエストが作成されている

---

## 🆘 困った時は

- **設定が不明**: `config.yaml`を確認
- **他モジュールとの連携**: このファイルのデータ形式を確認
- **エラー**: ログを確認（`hand_tracker.log`）
