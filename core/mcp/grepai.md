# grepai MCP

セマンティック検索でコードベースを探索し、Claude Code への入力トークンを最大 97% 削減する CLI ツール。
Embedding（ベクトル化）で「意味的に近いコード」を特定し、関連コードだけを Claude に渡す。

## 効果（公式ベンチマーク: Excalidraw 155k行 TypeScript）

| 指標 | 変化 |
|---|---|
| 入力トークン | **-97%** |
| API 課金額 | **-27.5%** |
| ツールコール | **-55%** |
| サブエージェント起動 | 5 → 0 |

※ キャッシュ読み取りは +30% 増加するためコスト削減は 27.5% に留まる。

## grepai vs Serena の使い分け

| | grepai | Serena |
|---|---|---|
| アプローチ | Embedding（意味検索） | LSP（シンボル単位） |
| 得意 | 「認証周りのコード探して」| 「この関数の呼び出し元を探す」 |
| 自然言語クエリ | ◎ | △ |
| 言語サポート | 11言語 | 30言語以上 |
| 依存 | Ollama / LM Studio / OpenAI | LSP サーバー |

曖昧な自然言語探索なら grepai、構造的・シンボルベースなら Serena。**併用も有効。**

## セキュリティ

- コードは一切外部に送信されない（Ollama/LM Studio 使用時は完全ローカル）
- MCP サーバーは stdio のみ（ネットワーク公開なし）
- OpenAI 使用時のみクエリテキストが API に送信される（コード本体は送られない）

## セットアップ

### 1. インストール

```bash
# macOS (Homebrew)
brew install yoanbernabeu/tap/grepai

# Linux / macOS (curl)
curl -sSL https://raw.githubusercontent.com/yoanbernabeu/grepai/main/install.sh | sh

# Windows (PowerShell)
irm https://raw.githubusercontent.com/yoanbernabeu/grepai/main/install.ps1 | iex
```

### 2. Embedding プロバイダーを用意する

**Ollama（推奨・完全ローカル）:**
```bash
# Ollama インストール: https://ollama.ai
ollama pull nomic-embed-text
```

**OpenAI（クラウド）:**
```bash
export OPENAI_API_KEY=sk-...
```

### 3. プロジェクトを初期化

```bash
cd your-project
grepai init      # .grepai/config.yaml を生成
grepai watch     # インデックスデーモン起動（バックグラウンド）
```

### 4. MCP サーバーとして Claude Code に登録

```bash
claude mcp add grepai -- grepai mcp-serve
```

これにより Claude Code が `/grepai_search`, `/grepai_trace_callers` などを直接ツールとして呼べるようになる。

## 主要コマンド

```bash
# セマンティック検索（英語クエリが最も精度高い）
grepai search "user authentication flow"
grepai search "error handling middleware"
grepai search "database connection pooling" --json --compact

# コールグラフ
grepai trace callers "HandleRequest" --json   # この関数を呼んでいる関数
grepai trace callees "ProcessOrder" --json    # この関数が呼んでいる関数
grepai trace graph "ValidateToken" --depth 3  # 双方向グラフ

# インデックス状態確認
grepai status
```

## Claude Code SKILL との併用

`skills: [grepai]` を `claude-config.yaml` に追加すると、SKILL.md が `.claude/skills/grepai/` に展開され、
Claude が自動的に Grep/Glob の代わりに `grepai search` を使うようになる。

## 設定（.grepai/config.yaml）

```yaml
embedder:
  provider: ollama       # ollama | openai | lmstudio
  model: nomic-embed-text
store:
  backend: gob           # gob（ファイル）| postgres
chunking:
  size: 512
  overlap: 64
```
