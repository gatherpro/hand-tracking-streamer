# 🎭 エージェント起動マニュアル

このファイルは、各エージェントを起動するための完全なガイドです。
**コピペするだけ**で各エージェントが作業を開始できます。

---

## 📋 開くべきウィンドウ数: **6個**

| ウィンドウ | 役割 | ディレクトリ |
|-----------|------|-------------|
| **ウィンドウ1** | オーケストレーター（あなた） | `hand-tracking-streamer/` |
| **ウィンドウ2** | Agent1 - Camera Capture | `agent1-worktree/` |
| **ウィンドウ3** | Agent2 - Hand Detection | `agent2-worktree/` |
| **ウィンドウ4** | Agent3 - Joint Measurement | `agent3-worktree/` |
| **ウィンドウ5** | Agent4 - Data Sender | `agent4-worktree/` |
| **ウィンドウ6** | Agent5 - Main Controller | `agent5-worktree/` |

---

## 🚀 起動手順

### ステップ1: Claude Codeウィンドウを6個開く

各ウィンドウで以下のディレクトリを開いてください：

```bash
# ウィンドウ1（オーケストレーター）
C:\Users\81905\Documents\hand-tracking-streamer

# ウィンドウ2（Agent1）
C:\Users\81905\Documents\agent1-worktree

# ウィンドウ3（Agent2）
C:\Users\81905\Documents\agent2-worktree

# ウィンドウ4（Agent3）
C:\Users\81905\Documents\agent3-worktree

# ウィンドウ5（Agent4）
C:\Users\81905\Documents\agent4-worktree

# ウィンドウ6（Agent5）
C:\Users\81905\Documents\agent5-worktree
```

### ステップ2: 各ウィンドウで以下の指示をコピペ

---

## 📝 各ウィンドウへの指示（コピペ用）

### 🎭 ウィンドウ1: オーケストレーター（あなた）

**開くディレクトリ**: `C:\Users\81905\Documents\hand-tracking-streamer`

**最初のメッセージ（コピペ）**:
```
あなたはオーケストレーターAIです。ORCHESTRATOR.mdを読んで、あなたの役割を理解してください。

今、5人のエージェントが並行して作業を開始します。
あなたの役割は：
1. 各エージェントの進捗を監視する
2. 問題が発生したら解決をサポートする
3. PRが作成されたらレビューする
4. マージのタイミングを管理する

まず、ORCHESTRATOR.mdを読んで、現在の状況を確認してください。
その後、定期的に全エージェントの進捗をチェックしてください。
```

---

### 🎬 ウィンドウ2: Agent1 - Camera Capture

**開くディレクトリ**: `C:\Users\81905\Documents\agent1-worktree`

**最初のメッセージ（コピペ）**:
```
あなたはAgent1です。Camera Capture Moduleの実装を担当します。

START_HERE.mdを読んで、あなたの役割とタスクを理解してください。
その後、以下の順序で作業を進めてください：

1. START_HERE.mdを読む
2. AGENTS.mdのAgent1セクションを読む
3. TODO.mdでタスクを確認
4. src/camera_capture.py の実装を開始
5. tests/test_camera_capture.py のテストを書く
6. テストを実行して確認
7. コミット＆プッシュ
8. PRを作成

まず、START_HERE.mdを読んで作業を開始してください。
```

---

### 🤚 ウィンドウ3: Agent2 - Hand Detection

**開くディレクトリ**: `C:\Users\81905\Documents\agent2-worktree`

**最初のメッセージ（コピペ）**:
```
あなたはAgent2です。Hand Detection & Tracking Moduleの実装を担当します。

START_HERE.mdを読んで、あなたの役割とタスクを理解してください。
その後、以下の順序で作業を進めてください：

1. START_HERE.mdを読む
2. AGENTS.mdのAgent2セクションを読む
3. TODO.mdでタスクを確認
4. src/hand_detector.py の実装を開始
5. tests/test_hand_detector.py のテストを書く
6. テストを実行して確認
7. コミット＆プッシュ
8. PRを作成

まず、START_HERE.mdを読んで作業を開始してください。
```

---

### 📏 ウィンドウ4: Agent3 - Joint Measurement

**開くディレクトリ**: `C:\Users\81905\Documents\agent3-worktree`

**最初のメッセージ（コピペ）**:
```
あなたはAgent3です。Joint Measurement & Data Processing Moduleの実装を担当します。

START_HERE.mdを読んで、あなたの役割とタスクを理解してください。
その後、以下の順序で作業を進めてください：

1. START_HERE.mdを読む
2. AGENTS.mdのAgent3セクションを読む
3. TODO.mdでタスクを確認
4. src/joint_measurement.py の実装を開始
5. tests/test_joint_measurement.py のテストを書く
6. テストを実行して確認
7. コミット＆プッシュ
8. PRを作成

まず、START_HERE.mdを読んで作業を開始してください。
```

---

### 📤 ウィンドウ5: Agent4 - Data Sender

**開くディレクトリ**: `C:\Users\81905\Documents\agent4-worktree`

**最初のメッセージ（コピペ）**:
```
あなたはAgent4です。Data Sender Moduleの実装を担当します。

START_HERE.mdを読んで、あなたの役割とタスクを理解してください。
その後、以下の順序で作業を進めてください：

1. START_HERE.mdを読む
2. AGENTS.mdのAgent4セクションを読む
3. TODO.mdでタスクを確認
4. src/data_sender.py の実装を開始
5. tests/test_data_sender.py のテストを書く
6. テストを実行して確認
7. コミット＆プッシュ
8. PRを作成

まず、START_HERE.mdを読んで作業を開始してください。
```

---

### 🎮 ウィンドウ6: Agent5 - Main Controller

**開くディレクトリ**: `C:\Users\81905\Documents\agent5-worktree`

**最初のメッセージ（コピペ）**:
```
あなたはAgent5です。Main Controller & Integrationの実装を担当します。

重要：あなたのモジュールは他の4つのモジュール（Agent1-4）に依存します。
まずは他のエージェントの進捗を確認してから作業を始めてください。

START_HERE.mdを読んで、あなたの役割とタスクを理解してください。
その後、以下の順序で作業を進めてください：

1. START_HERE.mdを読む
2. AGENTS.mdのAgent5セクションを読む
3. TODO.mdでタスクを確認
4. 他のエージェント（1-4）の実装状況を確認
5. src/main.py の実装を開始（モックを使ってテスト可能）
6. tests/test_integration.py のテストを書く
7. テストを実行して確認
8. コミット＆プッシュ
9. PRを作成

まず、START_HERE.mdを読んで作業を開始してください。
```

---

## 📊 進捗管理（オーケストレーター用）

オーケストレーターは定期的に以下のコマンドで進捗を確認してください：

```bash
# 全エージェントの状況確認
gh issue list
gh pr list

# 各ブランチの最新コミット
git log --all --oneline --graph --decorate -10

# worktree一覧
git worktree list
```

---

## 🌳 プロジェクトツリー構造

```
hand-tracking-streamer (GitHub)
│
├── main ブランチ
│   └── オーケストレーター（あなた）がここで管理
│
├── feature/camera-capture
│   └── Agent1がagent1-worktreeで作業
│
├── feature/hand-detection
│   └── Agent2がagent2-worktreeで作業
│
├── feature/joint-measurement
│   └── Agent3がagent3-worktreeで作業
│
├── feature/data-sender
│   └── Agent4がagent4-worktreeで作業
│
└── feature/main-controller
    └── Agent5がagent5-worktreeで作業
```

**サブツリー（必要に応じて）**:
各エージェントが必要に応じてさらにサブブランチを作成できますが、
オーケストレーターに必ず報告してください。

例：
```
feature/camera-capture
├── feature/camera-capture-bugfix
└── feature/camera-capture-optimization
```

---

## ✅ チェックリスト

開始前に確認：

- [ ] 6個のClaude Codeウィンドウを開いた
- [ ] 各ウィンドウで正しいディレクトリを開いている
- [ ] 各ウィンドウに指示をコピペした
- [ ] オーケストレーターがORCHESTRATOR.mdを読んだ
- [ ] 各エージェントがSTART_HERE.mdを読み始めた

開始後の確認（オーケストレーター）：

- [ ] 全エージェントが作業を開始した
- [ ] 各エージェントの初回コミットを確認
- [ ] 問題が発生していないか確認
- [ ] PRが作成されたらレビュー

---

## 🆘 トラブルシューティング

### エージェントが困っている場合

1. 該当エージェントのウィンドウで状況を確認
2. AGENTS.mdの該当セクションを再度読むよう指示
3. config.yamlの設定を確認
4. 必要に応じてオーケストレーターがサポート

### ブランチが混乱した場合

```bash
# 各worktreeのブランチ確認
git worktree list

# 特定のworktreeの状態確認
cd agent1-worktree && git status
```

---

準備完了！各ウィンドウに指示をコピペして、プロジェクトを開始してください🚀
