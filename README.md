# Claude Universal Config

[![GitHub](https://img.shields.io/badge/GitHub-hiroshi131206%2Fclaude--universal--config-blue?logo=github)](https://github.com/hiroshi131206/claude-universal-config)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/hiroshi131206/claude-universal-config/pulls)

**言語・フレームワーク横断的なClaude Code設定ライブラリ**

プロジェクトごとに必要なルール、エージェント、コマンドを選択的に導入できる仕組みを提供します。

🔗 **Repository**: https://github.com/hiroshi131206/claude-universal-config

## 📋 目次

- [特徴](#特徴)
- [対応技術](#対応技術)
- [クイックスタート](#クイックスタート)
- [使い方](#使い方)
- [ディレクトリ構造](#ディレクトリ構造)
- [設定ファイル](#設定ファイル)
- [テンプレート](#テンプレート)
- [エンコーディング対応](#エンコーディング対応)
- [MCPサーバー](#mcpサーバー)
- [スキル・自律改善](#スキル自律改善)
- [カスタマイズ](#カスタマイズ)
- [コントリビューション](#コントリビューション)

---

## 特徴

✅ **汎用的なコアルール**: すべてのプロジェクトで共通（coding-style, security, testing, git）
✅ **技術スタック別ルール**: 必要なものだけを選択（Django, React, FastAPI, Vue, Go, Rust, etc.）
✅ **エージェントテンプレート**: 技術スタックに応じて自動生成（code-reviewer, tdd-guide, security-reviewer）
✅ **設定ファイル駆動**: `claude-config.yaml` で簡単設定
✅ **テンプレート提供**: 一般的な構成をすぐに使える（Django+React, FastAPI+Vue, etc.）
✅ **拡張可能**: プロジェクト固有のカスタムルールを追加可能
✅ **MCPサーバー対応**: `mcp:` セクションでセッション間通信などのMCPツールを組み込み可能
✅ **スキル・自律改善**: `skills:` セクションで autoresearch などの自律ループコマンドを導入可能

---

## 対応技術

### 言語
- Python
- TypeScript
- JavaScript
- Go
- Rust
- Java

### バックエンドフレームワーク
- **Python**: Django, FastAPI, Flask
- **Node.js**: Express, NestJS
- **Java**: Spring Boot
- **Go**: Gin, Echo
- **Rust**: Actix, Rocket

### フロントエンドフレームワーク
- React
- Vue
- Angular
- Svelte

### インフラ
- Docker
- Kubernetes
- Terraform
- AWS

### ドメイン
- Web Security (OWASP Top 10)
- Optimization (OR-Tools等)
- ML/AI
- Blockchain

---

## クイックスタート

### 1. リポジトリをクローン

```bash
git clone https://github.com/hiroshi131206/claude-universal-config.git
cd claude-universal-config
```

### 2. CLI依存関係をインストール

```bash
pip install -r cli/requirements.txt
```

### 3. 新規プロジェクトで使用

```bash
# プロジェクトディレクトリに移動
cd /path/to/your-project

# テンプレートから設定ファイルを作成
cp /path/to/claude-universal-config/templates/django-react-monorepo.yaml claude-config.yaml

# 設定を編集（必要に応じて）
vi claude-config.yaml

# Claude Code設定を生成
python /path/to/claude-universal-config/cli/generate.py claude-config.yaml .

# 生成された .claude/ ディレクトリを確認
ls -la .claude/
```

### 4. CLAUDE.md を作成

プロジェクト固有の指示を `CLAUDE.md` に記載します。

```markdown
# Your Project - Claude Code Guide

## Project Overview
[プロジェクトの概要]

## Tech Stack
- Backend: Django 5.x
- Frontend: React 18
- Database: PostgreSQL

## Development Commands
- Run: docker-compose up
- Test: python manage.py test

## Critical Patterns
[プロジェクト固有の重要パターン]
```

---

## 使い方

### 方法1: テンプレートから生成

```bash
# 利用可能なテンプレート一覧
ls templates/

# テンプレートをコピー
cp templates/django-react-monorepo.yaml claude-config.yaml

# 生成
python cli/generate.py claude-config.yaml .
```

### 方法2: ゼロから設定

`claude-config.yaml` を作成:

```yaml
name: my-awesome-project
version: 1.0.0

languages:
  - python
  - typescript

backend:
  - fastapi

frontend:
  - vue

infrastructure:
  - docker

domains:
  - web-security

agents:
  code-reviewer:
    enabled: true
    contexts: [python, typescript, fastapi, vue]
  tdd-guide:
    enabled: true
    contexts: [python, typescript]

commands:
  - review
  - tdd
  - test
  - debug
```

生成:

```bash
python cli/generate.py claude-config.yaml .
```

---

## ディレクトリ構造

```
claude-universal-config/
├── core/                      # 全プロジェクト共通（必須）
│   ├── rules/
│   │   ├── coding-style.md
│   │   ├── security.md
│   │   ├── testing.md
│   │   └── git.md
│   ├── agents/
│   │   ├── code-reviewer.template.md
│   │   ├── tdd-guide.template.md
│   │   └── security-reviewer.template.md
│   ├── commands/
│   │   ├── review.md
│   │   ├── tdd.md
│   │   ├── test.md
│   │   ├── autoresearch.md          # 自律改善ループ（メインコマンド）
│   │   └── autoresearch/            # サブコマンド群
│   │       ├── debug.md, fix.md, learn.md
│   │       ├── plan.md, predict.md, scenario.md
│   │       ├── security.md, ship.md
│   ├── skills/                      # コマンドが参照するプロトコルファイル
│   │   └── autoresearch/
│   │       ├── SKILL.md
│   │       └── references/
│   │           ├── autonomous-loop-protocol.md
│   │           ├── results-logging.md
│   │           └── (各ワークフロー参照ファイル)
│   └── mcp/
│       └── claude-peers.md
│
├── languages/                 # 言語別ルール（選択式）
│   ├── python/
│   ├── typescript/
│   ├── go/
│   ├── rust/
│   └── java/
│
├── frameworks/                # フレームワーク別ルール（選択式）
│   ├── backend/
│   │   ├── django/
│   │   ├── fastapi/
│   │   ├── flask/
│   │   ├── express/
│   │   ├── nestjs/
│   │   └── spring/
│   └── frontend/
│       ├── react/
│       ├── vue/
│       ├── angular/
│       └── svelte/
│
├── infrastructure/            # インフラ別ルール（選択式）
│   ├── docker/
│   ├── kubernetes/
│   ├── terraform/
│   └── aws/
│
├── domains/                   # ドメイン別スキル（選択式）
│   ├── web-security/
│   ├── optimization/
│   └── ml-ai/
│
├── templates/                 # プロジェクトテンプレート
│   ├── django-react-monorepo.yaml
│   ├── fastapi-vue-microservices.yaml
│   └── golang-microservices.yaml
│
└── cli/                       # CLIツール
    ├── generate.py
    └── requirements.txt
```

---

## 設定ファイル

`claude-config.yaml` の詳細:

```yaml
# プロジェクト名とバージョン
name: optima-shift-project
version: 1.0.0

# 言語選択（複数可）
languages:
  - python
  - typescript

# バックエンドフレームワーク（複数可）
backend:
  - django

# フロントエンドフレームワーク（複数可）
frontend:
  - react

# インフラ（複数可）
infrastructure:
  - docker
  - postgresql

# ドメイン固有スキル（複数可）
domains:
  - web-security
  - optimization

# エージェント有効化
agents:
  code-reviewer:
    enabled: true
    contexts: [python, typescript, django, react]
    custom_checks:
      - "Area-based permissions use get_managed_area_ids() correctly"
      - "API responses follow standard format"
  tdd-guide:
    enabled: true
    contexts: [python, typescript]
  security-reviewer:
    enabled: true
    contexts: [web-security]

# コマンド有効化
commands:
  - review
  - tdd
  - test
  - migrate  # Django専用
  - debug
  - feature
  - autoresearch  # 自律改善ループ（+サブコマンド autoresearch:debug/fix/security など）

# スキル有効化（コマンドが参照するプロトコルファイル）
skills:
  - autoresearch

commands:
  - encoding-fix  # Shift-JIS/EUC-JP/CP932 → UTF-8 変換

# カスタムルール（オプション）
custom_rules:
  - path: .claude/custom/area-permission-pattern.md
    description: "エリアスコープ権限パターン"

# MCPサーバー（オプション）
mcp:
  claude-peers:
    enabled: true
    scope: user                        # user | project
    install_path: ~/claude-peers-mcp   # インストール先パス
```

---

## テンプレート

### 用意されているテンプレート

#### `django-react-monorepo.yaml`
Django + React のモノレポ構成

#### `fastapi-vue-microservices.yaml`（今後追加予定）
FastAPI + Vue のマイクロサービス構成

#### `golang-microservices.yaml`（今後追加予定）
Go のマイクロサービス構成

---

## エンコーディング対応

Claude Code は Shift-JIS・EUC-JP・CP932 などの日本語エンコーディングを直接扱えない場合がある。
`tools/encoding-convert.py` と `/encoding-fix` コマンドで変換してから読み込むことで、古い日本語サイトや社内レガシーファイルの調査が格段に楽になる。

### `/encoding-fix` コマンド

```bash
# 古いWebサイトのページを取得して読む
/encoding-fix https://old-company-site.co.jp/report.html

# ローカルの Shift-JIS ファイルを変換
/encoding-fix ./legacy-data/customers.csv --from-encoding cp932

# ディレクトリ内の全HTMLを一括変換
/encoding-fix ./scraped-pages/ --recursive

# エンコーディングを確認するだけ（変換しない）
/encoding-fix ./document.txt --detect-only
```

### `tools/encoding-convert.py` — 直接利用

```bash
# URLから取得して変換（出力先指定）
python tools/encoding-convert.py https://example.com/page.html -o /tmp/page_utf8.html

# ファイルを上書き変換
python tools/encoding-convert.py ./report.html --from-encoding shift_jis

# ディレクトリ一括変換（.html/.htm/.txt/.csv が対象）
python tools/encoding-convert.py ./pages/ --recursive

# chardet をインストールすると自動検出の精度が上がる（オプション）
pip install chardet
```

### 対応エンコーディング

| エンコーディング | 別名 | よく見る場面 |
|---|---|---|
| `shift_jis` | SJIS | 古い日本語Webサイト |
| `cp932` | Windows-31J | Windowsで作ったテキスト・Excel CSV |
| `euc_jp` | EUC-JP | 古いUnix/Linuxサーバー |
| `iso2022_jp` | JIS | メール、一部の古いシステム |

---

## スキル・自律改善

`skills:` セクションでスキルファイル群（コマンドが内部参照するプロトコル）を `.claude/skills/` に展開します。

### `autoresearch` — 自律改善ループ

**概要:** 「修正 → 検証 → 採用/棄却 → 繰り返し」を自律的に実行するエージェントループ。測定可能な指標があれば何にでも適用可能。

**実績例:** スキルファイルの品質チェック通過率 66.7% → 100%（5ラウンド自動実行）

#### コマンド一覧

| コマンド | 説明 |
|---|---|
| `/autoresearch` | メイン：任意の指標を改善する自律ループ |
| `/autoresearch:debug` | バグ自動発見ループ（科学的仮説検証） |
| `/autoresearch:fix` | エラーゼロになるまで自動修正 |
| `/autoresearch:security` | STRIDE + OWASP Top10 自律セキュリティ監査 |
| `/autoresearch:learn` | コードベースを自動解析してドキュメント生成 |
| `/autoresearch:plan` | 目標からScope/Metric/Verifyを自動設計 |
| `/autoresearch:predict` | 複数ペルソナによるスウォーム予測分析 |
| `/autoresearch:scenario` | ユースケース・エッジケースを自動生成 |
| `/autoresearch:ship` | コード・コンテンツなど何でも自動シッピング |

#### 使い方

```bash
# 基本（unbounded: Ctrl+C で停止）
/autoresearch
Goal: テストカバレッジを70%から90%に改善
Scope: src/**/*.ts
Verify: npx jest --coverage 2>&1 | grep 'All files' | awk '{print $4}'

# 回数制限あり（N回で自動停止）
/autoresearch
Goal: APIレスポンスタイムを200ms以下に
Scope: src/api/**
Verify: wrk -t2 -c10 -d5s http://localhost:3000/api 2>&1 | grep 'Avg Lat' | awk '{print $2}'
Iterations: 10

# セキュリティ監査
/autoresearch:security --scope src/ --depth standard

# バグ自動修正
/autoresearch:fix --target "pytest" --scope src/
```

#### 動作の仕組み

```
Phase 0: git状態チェック（clean/dirty確認）
Phase 1: git履歴を読み込み（前回の成功/失敗を学習）
Phase 2: 次の実験を選択
Phase 3: ファイルをアトミックに変更（1変更/1イテレーション）
Phase 4: git commit（検証前にコミット → ロールバック可能）
Phase 5: 検証コマンド実行 → 指標を抽出
Phase 6: 改善なら KEEP / 悪化なら git revert
Phase 7: results.tsv にログ記録
Phase 8: Repeat（unboundedは無限、boundedはN回）
```

**セキュリティ設計:**
- `git add -A` を**禁止**（明示的ファイル指定のみ）
- `--no-verify` を**禁止**（フック経由で品質保護）
- テスト・ガードファイルの変更**禁止**
- `git revert` 優先（履歴として失敗も記録）

#### claude-config.yaml への記述例

```yaml
commands:
  - autoresearch

skills:
  - autoresearch
```

---

## MCPサーバー

`mcp:` セクションで外部MCPツールをプロジェクト設定に組み込めます。`generate.py` 実行時に `.mcp.json` の生成またはユーザー登録コマンドの案内が自動的に行われます。

### 対応MCPツール

#### `claude-peers` — セッション間通信

複数のClaude Codeセッション間でメッセージ送受信・コンテキスト共有を可能にします。

**セキュリティ注意事項:**
- ブローカーは `127.0.0.1` のみで動作（外部公開なし）
- ブローカーに認証なし：信頼できるローカル環境での使用を推奨
- `--dangerously-skip-permissions` は使用しないこと（なしでも動作する）
- `OPENAI_API_KEY` 設定時はパス情報がOpenAIに送信される（オプション機能）

**セットアップ:**

```bash
# 1. インストール
git clone https://github.com/louislva/claude-peers-mcp.git ~/claude-peers-mcp
cd ~/claude-peers-mcp && bun install

# 2. scope: user の場合は手動登録（generate.py が案内を出力する）
claude mcp add --scope user --transport stdio claude-peers -- bun ~/claude-peers-mcp/server.ts

# 3. Claude Code 起動（--dangerously-skip-permissions は不要）
claude --dangerously-load-development-channels server:claude-peers
```

**claude-config.yaml への記述例:**

```yaml
mcp:
  claude-peers:
    enabled: true
    scope: user                        # user | project
    install_path: ~/claude-peers-mcp   # インストール先パス
```

**scope の使い分け:**

| scope | 動作 |
|---|---|
| `user` | `~/.claude/` にグローバル登録（全プロジェクトで利用可）。generate.py が登録コマンドを案内 |
| `project` | プロジェクトルートの `.mcp.json` に自動出力 |

詳細は [`core/mcp/claude-peers.md`](core/mcp/claude-peers.md) を参照。

### 新しいMCPツールを追加

```bash
# 1. ドキュメントを追加
echo "# my-tool MCP" > core/mcp/my-tool.md

# 2. claude-config.yaml に追記
# mcp:
#   my-tool:
#     enabled: true
#     scope: project
#     command: node
#     args: [~/my-tool/index.js]
```

---

## カスタマイズ

### 新しいルールを追加

```bash
# 言語別ルールを追加
mkdir -p languages/rust/rules
echo "# Rust Coding Style" > languages/rust/rules/rust-style.md

# フレームワーク別ルールを追加
mkdir -p frameworks/backend/actix/rules
echo "# Actix Best Practices" > frameworks/backend/actix/rules/actix.md
```

### 新しいエージェントテンプレートを追加

```bash
# エージェントテンプレートを作成
cat > core/agents/performance-analyzer.template.md << 'EOF'
---
name: performance-analyzer
description: Performance analysis specialist
tools: Read, Bash, Grep
model: sonnet
---

You are a performance optimization expert.

{% if 'python' in languages %}
## Python Performance
- Profile with cProfile
- Check for N+1 queries
{% endif %}

{% if 'react' in frontend %}
## React Performance
- Identify unnecessary re-renders
- Optimize component memoization
{% endif %}
EOF
```

---

## コントリビューション

貢献を歓迎します！

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### コントリビューションガイドライン

- 新しい言語/フレームワークのルールを追加する際は、適切なディレクトリに配置してください
- エージェントテンプレートはJinja2形式で記述してください
- テンプレート変数: `{{ languages }}`, `{{ backend }}`, `{{ frontend }}`, `{{ contexts }}`
- 条件分岐: `{% if 'django' in backend %}...{% endif %}`

---

## ライセンス

MIT License

---

## クレジット

このプロジェクトは **OPTIMA Shift** プロジェクトのClaude Code設定から派生しました。

---

## サポート

- Issues: https://github.com/hiroshi131206/claude-universal-config/issues
- Discussions: https://github.com/hiroshi131206/claude-universal-config/discussions
