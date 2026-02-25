#!/bin/bash
# Claude Universal Config - GitHub Push Script

echo "🚀 Pushing Claude Universal Config to GitHub..."

cd "d:\Document-D\個人開発\claude-universal-config"

# 1. GitHub認証確認
echo "📝 Checking GitHub authentication..."
gh auth status
if [ $? -ne 0 ]; then
    echo "❌ Not authenticated. Please run: gh auth login"
    exit 1
fi

# 2. 新規リポジトリ作成
echo "📦 Creating GitHub repository..."
gh repo create claude-universal-config \
    --public \
    --source=. \
    --description="Language-agnostic Claude Code configuration library. Select rules, agents, and commands for any tech stack." \
    --push

if [ $? -eq 0 ]; then
    echo "✅ Repository created and pushed successfully!"
    echo ""
    echo "🔗 Repository URL:"
    gh repo view --web
else
    echo "❌ Failed to create repository"
    exit 1
fi

echo ""
echo "📋 Next steps:"
echo "  1. Add topics: claude-code, ai-coding, development-tools"
echo "  2. Enable Issues and Discussions"
echo "  3. Add LICENSE file (MIT recommended)"
echo "  4. Share with the community!"
