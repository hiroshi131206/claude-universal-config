# claude-peers MCP

複数のClaude Codeセッション間でメッセージ送受信・コンテキスト共有を可能にするMCPサーバー。

- 同一マシン上の複数Claudeセッションを相互発見
- セッション間でメッセージをリアルタイム送受信
- 各セッションの作業サマリーを共有
- スコープ指定（machine / directory / repo）での絞り込み

## セキュリティ注意事項

- ブローカーは `127.0.0.1:7899` のみバインド（外部公開なし）
- ブローカーに認証なし：同一マシン上の全プロセスがアクセス可能
  - ローカルの悪意あるプロセスが任意メッセージをClaudeに送れるため、
    信頼できる環境（個人開発機）でのみ使用を推奨
- `--dangerously-skip-permissions` は使用しないことを推奨
  - READMEに記載があるが、このフラグなしでも動作する
- `OPENAI_API_KEY` 設定時はディレクトリ名・ブランチ名・ファイル名がOpenAIに送信される

## セットアップ

### 1. インストール

```bash
git clone https://github.com/louislva/claude-peers-mcp.git ~/claude-peers-mcp
cd ~/claude-peers-mcp
bun install
```

### 2. MCPサーバーを登録

```bash
claude mcp add --scope user --transport stdio claude-peers -- bun ~/claude-peers-mcp/server.ts
```

### 3. Claude Codeを起動

```bash
# 推奨（--dangerously-skip-permissions は使わない）
claude --dangerously-load-development-channels server:claude-peers
```

## 使用可能なツール

| ツール | 説明 |
|---|---|
| `list_peers` | 他のClaude Codeインスタンスを検索（machine/directory/repo スコープ） |
| `send_message` | IDを指定して別インスタンスにメッセージを送信 |
| `set_summary` | 自分の作業サマリーを設定（他のインスタンスから参照可能） |
| `check_messages` | 未読メッセージを手動取得（チャンネル未使用時のフォールバック） |

## 設定

| 環境変数 | デフォルト | 説明 |
|---|---|---|
| `CLAUDE_PEERS_PORT` | `7899` | ブローカーのポート番号 |
| `CLAUDE_PEERS_DB` | `~/.claude-peers.db` | SQLiteデータベースのパス |
| `OPENAI_API_KEY` | なし | 設定時のみ自動サマリー生成（オプション） |

## 要件

- [Bun](https://bun.sh)
- Claude Code v2.1.80 以上
- claude.ai ログイン（チャンネル機能に必要）
