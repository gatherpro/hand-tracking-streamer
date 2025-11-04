#!/bin/bash
# スクリプト: 全worktreeを削除してクリーンアップ
# 使用方法: ./cleanup_worktrees.sh

set -e

echo "🧹 Worktreeのクリーンアップを開始します..."

# メインリポジトリのディレクトリを確認
if [ ! -d ".git" ]; then
    echo "エラー: このスクリプトはgitリポジトリのルートで実行してください"
    exit 1
fi

# 親ディレクトリのパス
PARENT_DIR=$(dirname $(pwd))

# worktreeリストを取得
echo "現在のworktree一覧:"
git worktree list

# 確認プロンプト
echo ""
read -p "全てのagent worktreeを削除しますか？ (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "キャンセルしました"
    exit 0
fi

# agent worktreeを削除
for i in {1..5}; do
    WORKTREE_PATH="${PARENT_DIR}/agent${i}-worktree"
    BRANCH_NAME=$(git worktree list | grep "agent${i}-worktree" | awk '{print $3}' | tr -d '[]' || echo "")

    if [ -d "${WORKTREE_PATH}" ]; then
        echo "🗑️  Worktree agent${i}-worktree を削除中..."
        git worktree remove "${WORKTREE_PATH}" --force || true
        echo "   ✅ 削除完了"
    fi

    # ブランチも削除するか確認
    if [ ! -z "$BRANCH_NAME" ]; then
        read -p "   ブランチ ${BRANCH_NAME} も削除しますか？ (yes/no): " delete_branch
        if [ "$delete_branch" == "yes" ]; then
            git branch -D ${BRANCH_NAME} || true
            echo "   ✅ ブランチを削除しました"
        fi
    fi
done

echo ""
echo "✅ クリーンアップが完了しました"
echo ""
echo "残っているworktree:"
git worktree list
