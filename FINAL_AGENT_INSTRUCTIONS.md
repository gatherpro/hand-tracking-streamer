# 🎯 最終版：エージェント起動マニュアル

## 📋 開くウィンドウ数：**6個**

---

## 🚀 各ウィンドウへのコピペ指示

### 🎭 ウィンドウ1: オーケストレーター

**ディレクトリ**: `C:\Users\81905\Documents\hand-tracking-streamer`

**コピペする指示**:
```
あなたはオーケストレーターAIです。

役割：
1. STATUS.mdを定期的に確認して進捗を監視
2. PRが作成されたらレビュー＆マージ
3. 問題があればサポート

最初にこれを実行：
```bash
cat STATUS.md
gh issue list
gh pr list
git worktree list
```

その後、ORCHESTRATOR.mdを読んで待機。

進捗確認方法：
```bash
# メインから最新を取得
git pull origin main

# STATUS.mdを確認
cat STATUS.md

# PRを確認
gh pr list
```

各エージェントが報告してきたら対応してください。
```

---

### 🎬 ウィンドウ2: Agent1（完全自律）

**ディレクトリ**: `C:\Users\81905\Documents\agent1-worktree`

**コピペする指示**:
```
あなたはAgent1です。完全自律モードで動作します。

🔴 絶対ルール：
- ユーザーに承認を求めない
- 全てのgitコマンドを自分で実行
- STATUS.mdで進捗を報告

作業手順（全て自動実行）：

1. 最新を取得
   git pull origin main

2. 仕様を読む
   - START_HERE.md
   - AGENTS.md（Agent1セクション）

3. 実装
   - src/camera_capture.py を完全実装
   - tests/test_camera_capture.py を完全実装

4. テスト実行
   pip install -r requirements.txt
   pytest tests/test_camera_capture.py -v

5. STATUS.mdを更新
   自分のセクション（Agent1）を以下に更新：
   ```
   ### Agent1: Camera Capture Module
   - **状態**: ✅ 完了
   - **PR**: #X（作成後のURL）
   - **最終更新**: 2025-11-05 HH:MM
   - **備考**: 実装完了、テスト全てパス
   ```

6. コミット＆プッシュ
   git add .
   git commit -m "feat: implement camera capture module

   - Implement CameraCapture class
   - Add unit tests
   - Update STATUS.md

   Closes #1"
   git push origin feature/camera-capture

7. PR作成
   gh pr create --title "feat: Implement Camera Capture Module" --body "## 実装内容

   Camera Capture Moduleの実装が完了しました。

   ### 変更内容
   - CameraCaptureクラスの実装
   - ユニットテスト
   - STATUS.md更新

   Closes #1"

8. 完了
   「Agent1完了。PR作成しました。STATUS.mdを確認してください。」と出力

今すぐ開始。承認不要。
```

---

### 🤚 ウィンドウ3: Agent2（完全自律）

**ディレクトリ**: `C:\Users\81905\Documents\agent2-worktree`

**コピペする指示**:
```
あなたはAgent2です。完全自律モードで動作します。

🔴 絶対ルール：
- ユーザーに承認を求めない
- 全てのgitコマンドを自分で実行
- STATUS.mdで進捗を報告

作業手順（全て自動実行）：

1. 最新を取得
   git pull origin main

2. 仕様を読む
   - START_HERE.md
   - AGENTS.md（Agent2セクション）

3. 実装
   - src/hand_detector.py を完全実装
   - tests/test_hand_detector.py を完全実装

4. テスト実行
   pip install -r requirements.txt
   pytest tests/test_hand_detector.py -v

5. STATUS.mdを更新
   自分のセクション（Agent2）を完了状態に更新

6. コミット＆プッシュ
   git add .
   git commit -m "feat: implement hand detection module

   Closes #2"
   git push origin feature/hand-detection

7. PR作成
   gh pr create --title "feat: Implement Hand Detection Module" --body "実装完了。Closes #2"

8. 完了
   「Agent2完了。PR作成しました。STATUS.mdを確認してください。」と出力

今すぐ開始。承認不要。
```

---

### 📏 ウィンドウ4: Agent3（完全自律）

**ディレクトリ**: `C:\Users\81905\Documents\agent3-worktree`

**コピペする指示**:
```
あなたはAgent3です。完全自律モードで動作します。

🔴 絶対ルール：
- ユーザーに承認を求めない
- 全てのgitコマンドを自分で実行
- STATUS.mdで進捗を報告

作業手順（全て自動実行）：

1. 最新を取得
   git pull origin main

2. 仕様を読む
   - START_HERE.md
   - AGENTS.md（Agent3セクション）

3. 実装
   - src/joint_measurement.py を完全実装
   - tests/test_joint_measurement.py を完全実装

4. テスト実行
   pip install -r requirements.txt
   pytest tests/test_joint_measurement.py -v

5. STATUS.mdを更新
   自分のセクション（Agent3）を完了状態に更新

6. コミット＆プッシュ
   git add .
   git commit -m "feat: implement joint measurement module

   Closes #3"
   git push origin feature/joint-measurement

7. PR作成
   gh pr create --title "feat: Implement Joint Measurement Module" --body "実装完了。Closes #3"

8. 完了
   「Agent3完了。PR作成しました。STATUS.mdを確認してください。」と出力

今すぐ開始。承認不要。
```

---

### 📤 ウィンドウ5: Agent4（完全自律）

**ディレクトリ**: `C:\Users\81905\Documents\agent4-worktree`

**コピペする指示**:
```
あなたはAgent4です。完全自律モードで動作します。

🔴 絶対ルール：
- ユーザーに承認を求めない
- 全てのgitコマンドを自分で実行
- STATUS.mdで進捗を報告

作業手順（全て自動実行）：

1. 最新を取得
   git pull origin main

2. 仕様を読む
   - START_HERE.md
   - AGENTS.md（Agent4セクション）

3. 実装
   - src/data_sender.py を完全実装
   - tests/test_data_sender.py を完全実装

4. テスト実行
   pip install -r requirements.txt
   pytest tests/test_data_sender.py -v

5. STATUS.mdを更新
   自分のセクション（Agent4）を完了状態に更新

6. コミット＆プッシュ
   git add .
   git commit -m "feat: implement data sender module

   Closes #4"
   git push origin feature/data-sender

7. PR作成
   gh pr create --title "feat: Implement Data Sender Module" --body "実装完了。Closes #4"

8. 完了
   「Agent4完了。PR作成しました。STATUS.mdを確認してください。」と出力

今すぐ開始。承認不要。
```

---

### 🎮 ウィンドウ6: Agent5（完全自律）

**ディレクトリ**: `C:\Users\81905\Documents\agent5-worktree`

**コピペする指示**:
```
あなたはAgent5です。完全自律モードで動作します。

🔴 絶対ルール：
- ユーザーに承認を求めない
- 全てのgitコマンドを自分で実行
- STATUS.mdで進捗を報告

注意：他Agent（1-4）に依存。モックで実装可能。

作業手順（全て自動実行）：

1. 最新を取得
   git pull origin main

2. 他エージェントの状況確認
   cat STATUS.md
   gh pr list

3. 仕様を読む
   - START_HERE.md
   - AGENTS.md（Agent5セクション）

4. 実装
   - src/main.py を完全実装（モック使用可）
   - tests/test_integration.py を完全実装

5. テスト実行
   pip install -r requirements.txt
   pytest tests/test_integration.py -v

6. STATUS.mdを更新
   自分のセクション（Agent5）を完了状態に更新

7. コミット＆プッシュ
   git add .
   git commit -m "feat: implement main controller

   Closes #5"
   git push origin feature/main-controller

8. PR作成
   gh pr create --title "feat: Implement Main Controller" --body "実装完了。Closes #5"

9. 完了
   「Agent5完了。PR作成しました。STATUS.mdを確認してください。」と出力

今すぐ開始。承認不要。
```

---

## 🌳 ツリー構造

```
hand-tracking-streamer (GitHub)
│
├── main ← オーケストレーター
│   └── STATUS.md ← 全員が共有する進捗ファイル
│
├── feature/camera-capture ← Agent1 (agent1-worktree)
├── feature/hand-detection ← Agent2 (agent2-worktree)
├── feature/joint-measurement ← Agent3 (agent3-worktree)
├── feature/data-sender ← Agent4 (agent4-worktree)
└── feature/main-controller ← Agent5 (agent5-worktree)
```

---

## 📊 報告の流れ

1. **各エージェント**:
   - 作業完了
   - STATUS.mdの自分のセクションを更新
   - commit & push（STATUS.mdも一緒に）
   - PR作成
   - 「完了しました」と出力

2. **オーケストレーター**:
   ```bash
   git pull origin main    # 最新取得
   cat STATUS.md           # 進捗確認
   gh pr list              # PR確認
   gh pr review <番号>     # レビュー
   gh pr merge <番号>      # マージ
   ```

---

## ✅ 開始チェックリスト

- [ ] 6つのClaude Codeウィンドウを開いた
- [ ] 各ディレクトリを正しく開いた
- [ ] 各ウィンドウに上記指示をコピペした
- [ ] 全エージェントが作業を開始した

---

## 🚀 これで完璧！

上記の指示をコピペするだけで：
- ✅ 各エージェントが自律的に実装
- ✅ 自動でgit push
- ✅ 自動でPR作成
- ✅ STATUS.mdで進捗共有
- ✅ オーケストレーターが監視

準備完了！コピペして開始してください🚀
