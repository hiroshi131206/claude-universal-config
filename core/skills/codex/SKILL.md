---
name: codex
description: Delegates tasks to OpenAI Codex CLI when the user explicitly requests it. Use when asked to "use codex", "ask codex", "codex でレビュー", "codex に相談", or when web search rate limits are being hit and the user wants Codex to handle the data gathering. Do NOT use for general research or codebase analysis — those are handled by autoresearch. Codex handles explicit delegations; Claude handles communication and synthesis.
license: MIT
allowed-tools: Bash
metadata:
  author: claude-universal-config
  version: "1.0"
  category: research
---

# Codex

Claude Code から Codex CLI を呼び出して、リサーチ・コードレビュー・大量データ分析を委譲するスキル。
Codex が調査、Claude が合成・コミュニケーションを担う役割分担で、トークンとレートリミットを節約する。

## 前提条件

Codex CLI がインストールされていること:
```bash
npm install -g @openai/codex
```

`OPENAI_API_KEY` が環境変数に設定されていること。

---

## 実行フォーマット

```bash
codex exec --full-auto --sandbox read-only --cd <project_dir> "<request>"
```

| パラメータ | 役割 |
|---|---|
| `--full-auto` | 確認なしで完全自動実行 |
| `--sandbox read-only` | ファイル書き込みを禁止（読み取り専用） |
| `--cd <dir>` | 対象プロジェクトのルートディレクトリ |

---

## 手順

### Step 1: 依頼内容を確認
ユーザーの依頼から以下を特定する:
- **タスク**: 何を調査・分析・レビューするか
- **対象ディレクトリ**: どのプロジェクトを対象にするか（未指定なら現在の作業ディレクトリ）

### Step 2: リクエストを構築
Codex へのリクエスト末尾に必ず以下を追加する:

> 確認や質問は不要です。具体的な提案・修正案まで自主的に出力してください。

これを省くと Codex が途中で止まり、無応答になる。

### Step 3: Codex を実行
```bash
codex exec --full-auto --sandbox read-only --cd <dir> "<task>。確認や質問は不要です。具体的な提案・修正案まで自主的に出力してください。"
```

実行中はターミナル出力をリアルタイムで確認する。
出力が意図しない方向に進んでいたら即座に中断すること。

### Step 4: 結果を合成してユーザーに報告
Codex の出力をそのまま返すのではなく、Claude が以下を行う:
- 重要な発見を要約
- 優先度の高い問題を先頭に置く
- ユーザーの元の質問に対応した回答に整形

---

## ユースケース別コマンド例

### コードレビュー
```bash
codex exec --full-auto --sandbox read-only --cd /path/to/project \
"このプロジェクトのコードをレビューし、品質上の問題と改善点を指摘してください。確認や質問は不要です。具体的な提案・修正案まで自主的に出力してください。"
```

### バグ調査
```bash
codex exec --full-auto --sandbox read-only --cd /path/to/project \
"<エラーメッセージ> の原因を調査し、修正方法を提案してください。確認や質問は不要です。具体的な提案・修正案まで自主的に出力してください。"
```

### アーキテクチャ分析
```bash
codex exec --full-auto --sandbox read-only --cd /path/to/project \
"このプロジェクトのアーキテクチャを分析し、構造上の問題点とリファクタリング案を提示してください。確認や質問は不要です。具体的な提案・修正案まで自主的に出力してください。"
```

### 大量データのリサーチ（Web Search 代替）
```bash
codex exec --full-auto --sandbox read-only --cd /path/to/project \
"<調査テーマ> について調査し、関連するコードや設計パターンを洗い出してください。確認や質問は不要です。具体的な提案・修正案まで自主的に出力してください。"
```

---

## Claude / Codex の役割分担

| タスク | 担当 |
|---|---|
| 大規模コードベースの探索・分析 | Codex |
| Web 検索が大量に必要な調査 | Codex |
| 複数ファイルにまたがるレビュー | Codex |
| 結果の要約・優先度付け | Claude |
| ユーザーとのコミュニケーション | Claude |
| 実装・ファイル編集 | Claude |

---

## トラブルシューティング

### Codex が途中で止まる / 無応答
リクエスト末尾の「確認や質問は不要です」が抜けている。必ず追加すること。

### セッション混在の問題
複数プロジェクトを切り替えて使う場合、`resume <session_id>` は使わない。
プロジェクトをまたぐとセッションの文脈が混同される。毎回新規セッションで実行すること。

### `codex: command not found`
```bash
npm install -g @openai/codex
```
インストール後、`codex --version` で確認。

### OPENAI_API_KEY が見つからない
```bash
export OPENAI_API_KEY="sk-..."
```
または `.env` ファイルに追記してシェルに読み込む。
