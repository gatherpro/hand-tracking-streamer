#!/bin/bash
# スクリプト: 全エージェントのworktreeを一括作成
# 使用方法: ./create_all_worktrees.sh

set -e

echo "🎭 全エージェントのworktreeを作成します..."

# メインリポジトリのディレクトリを確認
if [ ! -d ".git" ]; then
    echo "エラー: このスクリプトはgitリポジトリのルートで実行してください"
    exit 1
fi

# 親ディレクトリのパス
PARENT_DIR=$(dirname $(pwd))

# 各エージェントのworktreeを作成
AGENTS=(
    "1:camera-capture:Camera Capture"
    "2:hand-detection:Hand Detection"
    "3:joint-measurement:Joint Measurement"
    "4:data-sender:Data Sender"
    "5:main-controller:Main Controller"
)

for agent_info in "${AGENTS[@]}"; do
    IFS=':' read -r agent_num module_name display_name <<< "$agent_info"

    BRANCH_NAME="feature/${module_name}"
    WORKTREE_PATH="${PARENT_DIR}/agent${agent_num}-worktree"

    echo ""
    echo "📦 Agent${agent_num}: ${display_name}"
    echo "   ブランチ: ${BRANCH_NAME}"
    echo "   パス: ${WORKTREE_PATH}"

    # ブランチが存在するか確認
    if git show-ref --verify --quiet refs/heads/${BRANCH_NAME}; then
        echo "   ⚠️  ブランチ ${BRANCH_NAME} は既に存在します"
    else
        # ブランチを作成
        git branch ${BRANCH_NAME}
        echo "   ✅ ブランチを作成しました"
    fi

    # worktreeが存在するか確認
    if [ -d "${WORKTREE_PATH}" ]; then
        echo "   ⚠️  Worktree ${WORKTREE_PATH} は既に存在します"
    else
        # worktreeを作成
        git worktree add "${WORKTREE_PATH}" ${BRANCH_NAME}
        echo "   ✅ Worktreeを作成しました"
    fi

    # TODO.mdを作成
    TODO_FILE="${WORKTREE_PATH}/TODO.md"
    cat > "${TODO_FILE}" << EOF
# TODO for Agent${agent_num}: ${display_name}

## 📋 担当タスク

このファイルはAgent${agent_num}の具体的なタスクリストです。
詳細な仕様は \`AGENTS.md\` を確認してください。

## ✅ タスクリスト

- [ ] \`AGENTS.md\` で自分の役割と要件を理解する
- [ ] 担当モジュールのコードを読む
- [ ] ユニットテストの実装
- [ ] 機能の実装
- [ ] テストがパスすることを確認
- [ ] コミットとプッシュ
- [ ] プルリクエストの作成

## 🚀 開始方法

\`\`\`bash
# 依存関係のインストール
pip install -r requirements.txt

# テストの実行
pytest tests/test_*.py -v

# 実装開始
# src/ 内の担当ファイルを編集
\`\`\`

## 📝 メモ

このスペースは自由に使ってください。
EOF
    echo "   ✅ TODO.mdを作成しました"
done

echo ""
echo "🎉 全てのworktreeが作成されました！"
echo ""
echo "📊 Worktree一覧:"
git worktree list

echo ""
echo "🔄 次のステップ:"
echo "   1. 各worktreeに移動して作業を開始"
echo "   2. 'git worktree list' でworktree一覧を確認"
echo "   3. 各エージェントは並行して作業可能"
