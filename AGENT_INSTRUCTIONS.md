# 🤖 エージェント自律動作マニュアル

## 重要原則

**各エージェントは完全に自律して動作します。**
- ❌ ユーザーに承認を求めない
- ✅ 自分で判断して実装を進める
- ✅ 自分でコミット・プッシュ・PR作成まで完了させる
- ✅ 完了したらオーケストレーターに報告のみ

---

## 📝 各ウィンドウへの指示（コピペ用）

### 🎭 ウィンドウ1: オーケストレーター

**ディレクトリ**: `C:\Users\81905\Documents\hand-tracking-streamer`

**指示**:
```
あなたはオーケストレーターAIです。

あなたの役割：
1. 各エージェントの進捗を監視
2. 各エージェントからの完了報告を受け取る
3. PRをレビューしてマージ
4. 問題があれば解決をサポート

重要：各エージェントは自律的に動きます。あなたは承認ではなく「監視」と「統合」を行います。

まず、以下のコマンドで初期状態を確認してください：
```bash
gh issue list
git worktree list
```

その後、ORCHESTRATOR.mdを読んで待機してください。
エージェントから報告が来たら対応します。
```

---

### 🎬 ウィンドウ2: Agent1 - Camera Capture（自律モード）

**ディレクトリ**: `C:\Users\81905\Documents\agent1-worktree`

**指示**:
```
あなたはAgent1です。Camera Capture Moduleの実装を完全自律で行います。

重要ルール：
- ユーザーに承認を求めずに自分で判断して進める
- 実装→テスト→コミット→プッシュ→PR作成まで一気に完了させる
- 完了したらオーケストレーターに報告する

作業手順：
1. START_HERE.mdとAGENTS.mdを読んで仕様を理解
2. src/camera_capture.pyを実装
3. tests/test_camera_capture.pyを実装
4. テストを実行して確認
5. コミット＆プッシュ
6. PRを作成
7. 「Agent1完了。PR作成しました。」と報告

承認を求めずに、すぐに作業を開始してください。
読むべきファイル：START_HERE.md, AGENTS.md（Agent1セクション）
```

---

### 🤚 ウィンドウ3: Agent2 - Hand Detection（自律モード）

**ディレクトリ**: `C:\Users\81905\Documents\agent2-worktree`

**指示**:
```
あなたはAgent2です。Hand Detection Moduleの実装を完全自律で行います。

重要ルール：
- ユーザーに承認を求めずに自分で判断して進める
- 実装→テスト→コミット→プッシュ→PR作成まで一気に完了させる
- 完了したらオーケストレーターに報告する

作業手順：
1. START_HERE.mdとAGENTS.mdを読んで仕様を理解
2. src/hand_detector.pyを実装
3. tests/test_hand_detector.pyを実装
4. テストを実行して確認
5. コミット＆プッシュ
6. PRを作成
7. 「Agent2完了。PR作成しました。」と報告

承認を求めずに、すぐに作業を開始してください。
読むべきファイル：START_HERE.md, AGENTS.md（Agent2セクション）
```

---

### 📏 ウィンドウ4: Agent3 - Joint Measurement（自律モード）

**ディレクトリ**: `C:\Users\81905\Documents\agent3-worktree`

**指示**:
```
あなたはAgent3です。Joint Measurement Moduleの実装を完全自律で行います。

重要ルール：
- ユーザーに承認を求めずに自分で判断して進める
- 実装→テスト→コミット→プッシュ→PR作成まで一気に完了させる
- 完了したらオーケストレーターに報告する

作業手順：
1. START_HERE.mdとAGENTS.mdを読んで仕様を理解
2. src/joint_measurement.pyを実装
3. tests/test_joint_measurement.pyを実装
4. テストを実行して確認
5. コミット＆プッシュ
6. PRを作成
7. 「Agent3完了。PR作成しました。」と報告

承認を求めずに、すぐに作業を開始してください。
読むべきファイル：START_HERE.md, AGENTS.md（Agent3セクション）
```

---

### 📤 ウィンドウ5: Agent4 - Data Sender（自律モード）

**ディレクトリ**: `C:\Users\81905\Documents\agent4-worktree`

**指示**:
```
あなたはAgent4です。Data Sender Moduleの実装を完全自律で行います。

重要ルール：
- ユーザーに承認を求めずに自分で判断して進める
- 実装→テスト→コミット→プッシュ→PR作成まで一気に完了させる
- 完了したらオーケストレーターに報告する

作業手順：
1. START_HERE.mdとAGENTS.mdを読んで仕様を理解
2. src/data_sender.pyを実装
3. tests/test_data_sender.pyを実装
4. テストを実行して確認
5. コミット＆プッシュ
6. PRを作成
7. 「Agent4完了。PR作成しました。」と報告

承認を求めずに、すぐに作業を開始してください。
読むべきファイル：START_HERE.md, AGENTS.md（Agent4セクション）
```

---

### 🎮 ウィンドウ6: Agent5 - Main Controller（自律モード）

**ディレクトリ**: `C:\Users\81905/Documents/agent5-worktree`

**指示**:
```
あなたはAgent5です。Main Controller & Integrationの実装を完全自律で行います。

重要ルール：
- ユーザーに承認を求めずに自分で判断して進める
- 実装→テスト→コミット→プッシュ→PR作成まで一気に完了させる
- 完了したらオーケストレーターに報告する

注意：あなたは他のAgent（1-4）に依存します。
- 他のAgentが完成していない場合、モックを使って実装を進める
- 統合テストは他のAgentのPRがマージされた後に実行

作業手順：
1. START_HERE.mdとAGENTS.mdを読んで仕様を理解
2. 他のエージェントの進捗を確認（gh pr list）
3. src/main.pyを実装（モック使用可）
4. tests/test_integration.pyを実装
5. テストを実行して確認
6. コミット＆プッシュ
7. PRを作成
8. 「Agent5完了。PR作成しました。」と報告

承認を求めずに、すぐに作業を開始してください。
読むべきファイル：START_HERE.md, AGENTS.md（Agent5セクション）
```

---

## 🌳 現在のツリー構造

```
hand-tracking-streamer (main)
├── Agent1: feature/camera-capture → agent1-worktree
├── Agent2: feature/hand-detection → agent2-worktree
├── Agent3: feature/joint-measurement → agent3-worktree
├── Agent4: feature/data-sender → agent4-worktree
└── Agent5: feature/main-controller → agent5-worktree
```

### サブツリーを作る場合（エージェントが必要と判断した場合）

エージェントが作業中に新しいブランチが必要と判断したら、自分で作成できます：

```bash
# 例：Agent1がバグ修正用のサブブランチを作成
git checkout -b feature/camera-capture-bugfix
git push -u origin feature/camera-capture-bugfix
```

その場合、オーケストレーターに報告：
「サブブランチ feature/camera-capture-bugfix を作成しました。理由：〇〇」

---

## 📊 オーケストレーターの監視コマンド

```bash
# 進捗確認
gh pr list
gh issue list

# ツリー構造確認
git branch -a --format='%(refname:short)' | grep -E '(feature/|main)'

# 各エージェントの最新状況
git log --all --oneline --graph --decorate -20
```

---

## ✅ 開始チェックリスト

**ユーザー（あなた）がやること：**
- [ ] 6個のClaude Codeウィンドウを開く
- [ ] 各ウィンドウで正しいディレクトリを開く
- [ ] 各ウィンドウに上記の指示をコピペする
- [ ] 各エージェントが自律的に作業を開始するのを確認

**その後は監視のみ：**
- [ ] 定期的にオーケストレーターウィンドウで進捗確認
- [ ] PRが作成されたらレビュー＆マージ
- [ ] 問題があればサポート

---

## 🚀 すぐに開始

以下を順番にコピペしてください：

1. **ウィンドウ1（オーケストレーター）を開く**
   - ディレクトリ：`C:\Users\81905\Documents\hand-tracking-streamer`
   - 上記のオーケストレーター指示をコピペ

2. **ウィンドウ2-6（Agent1-5）を開く**
   - 各ディレクトリを開いて、対応する指示をコピペ

3. **完了を待つ**
   - 各エージェントが「完了しました」と報告するまで待機
   - オーケストレーターウィンドウでPRを確認・マージ

---

準備完了！コピペして開始してください🚀
