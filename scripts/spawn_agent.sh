#!/bin/bash
# スクリプト: 新しいエージェント用のgit worktreeを作成
# 使用方法: ./spawn_agent.sh <agent_number> <issue_number>

set -e

if [ $# -ne 2 ]; then
    echo "使用方法: $0 <agent_number> <issue_number>"
    echo "例: $0 1 10"
    exit 1
fi

AGENT_NUM=$1
ISSUE_NUM=$2
BRANCH_NAME=""
WORKTREE_NAME="agent${AGENT_NUM}-worktree"

# エージェント番号に応じてブランチ名を決定
case $AGENT_NUM in
    1)
        BRANCH_NAME="feature/${ISSUE_NUM}-camera-capture"
        MODULE_NAME="Camera Capture Module"
        ;;
    2)
        BRANCH_NAME="feature/${ISSUE_NUM}-hand-detection"
        MODULE_NAME="Hand Detection Module"
        ;;
    3)
        BRANCH_NAME="feature/${ISSUE_NUM}-joint-measurement"
        MODULE_NAME="Joint Measurement Module"
        ;;
    4)
        BRANCH_NAME="feature/${ISSUE_NUM}-data-sender"
        MODULE_NAME="Data Sender Module"
        ;;
    5)
        BRANCH_NAME="feature/${ISSUE_NUM}-main-controller"
        MODULE_NAME="Main Controller Module"
        ;;
    *)
        echo "エラー: agent_numberは1-5の範囲で指定してください"
        exit 1
        ;;
esac

echo "🚀 Agent${AGENT_NUM}のworktreeを作成します..."
echo "   ブランチ: ${BRANCH_NAME}"
echo "   Worktree: ${WORKTREE_NAME}"
echo "   モジュール: ${MODULE_NAME}"

# ブランチを作成
git checkout -b ${BRANCH_NAME}

# 初期コミット
git commit --allow-empty -m "chore(${ISSUE_NUM}): init branch for Agent${AGENT_NUM}

Initialize ${MODULE_NAME} development branch

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# リモートにプッシュ
git push -u origin ${BRANCH_NAME}

# mainに戻る
git checkout main

# worktreeを作成
cd ..
git worktree add ${WORKTREE_NAME} ${BRANCH_NAME}

echo "✅ Agent${AGENT_NUM}のworktreeが作成されました: ../${WORKTREE_NAME}"
echo "📝 次のステップ:"
echo "   1. cd ../${WORKTREE_NAME}"
echo "   2. AGENTS.mdを確認して自分の役割を理解する"
echo "   3. TODO.mdを確認してタスクを開始する"
