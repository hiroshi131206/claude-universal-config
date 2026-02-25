# Claude Universal Config

**言語・フレームワーク横断的なClaude Code設定ライブラリ**

プロジェクトごとに必要なルール、エージェント、コマンドを選択的に導入できる仕組みを提供します。

## 📋 目次

- [特徴](#特徴)
- [対応技術](#対応技術)
- [クイックスタート](#クイックスタート)
- [使い方](#使い方)
- [ディレクトリ構造](#ディレクトリ構造)
- [設定ファイル](#設定ファイル)
- [テンプレート](#テンプレート)
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
git clone https://github.com/YOUR_ORG/claude-universal-config.git
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
│   └── commands/
│       ├── review.md
│       ├── tdd.md
│       └── test.md
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

# カスタムルール（オプション）
custom_rules:
  - path: .claude/custom/area-permission-pattern.md
    description: "エリアスコープ権限パターン"
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

- Issues: https://github.com/YOUR_ORG/claude-universal-config/issues
- Discussions: https://github.com/YOUR_ORG/claude-universal-config/discussions
