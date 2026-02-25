# Contributing to Claude Universal Config

Claude Universal Configへの貢献を歓迎します！

## 貢献の方法

### 1. 新しい言語/フレームワークのルールを追加

```bash
# 例: Rustのルールを追加
mkdir -p languages/rust/rules
cat > languages/rust/rules/rust-style.md << 'EOF'
# Rust Coding Style Rules

## Ownership & Borrowing
- Always prefer borrowing over cloning
- Use `&str` instead of `String` for function parameters
- Avoid unnecessary `clone()` calls

## Error Handling
- Use `Result<T, E>` for recoverable errors
- Use `panic!` only for unrecoverable errors
- Prefer `?` operator over manual error propagation

## Memory Safety
- Minimize use of `unsafe` blocks
- Always document why `unsafe` is necessary
- Use safe abstractions when possible
EOF
```

### 2. 新しいエージェントテンプレートを追加

```bash
cat > core/agents/performance-analyzer.template.md << 'EOF'
---
name: performance-analyzer
description: Performance optimization specialist
tools: Read, Bash, Grep
model: sonnet
---

You are a performance optimization expert.

{% if 'python' in languages %}
## Python Performance
- Use cProfile for profiling
- Check for list comprehensions vs loops
- Avoid global variable lookups in loops
{% endif %}

{% if 'react' in frontend %}
## React Performance
- Identify unnecessary re-renders with React DevTools
- Use React.memo for pure components
- Optimize useEffect dependencies
{% endif %}
EOF
```

### 3. 新しいテンプレートを追加

```bash
cat > templates/fastapi-vue-spa.yaml << 'EOF'
# FastAPI + Vue SPA Template

name: fastapi-vue-spa
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
  security-reviewer:
    enabled: true

commands:
  - review
  - tdd
  - test
  - debug
EOF
```

## Pull Requestのガイドライン

### 前提条件
- Python 3.8以上
- 依存関係: `pip install -r cli/requirements.txt`

### PRを送る前に

1. **テスト**: 生成スクリプトが正常に動作することを確認
```bash
python cli/generate.py templates/your-template.yaml /tmp/test-output
ls -la /tmp/test-output/.claude/
```

2. **ドキュメント**: README.mdに追加内容を記載

3. **コミットメッセージ**: 以下の形式に従う
```
feat: Add Rust language rules
fix: Fix template rendering for Vue
docs: Update README with FastAPI example
```

### PRタイトル形式

- `feat: 新機能追加`
- `fix: バグ修正`
- `docs: ドキュメント更新`
- `refactor: リファクタリング`
- `test: テスト追加`

### レビュープロセス

1. PRを作成
2. CIが通ることを確認（将来実装）
3. メンテナーがレビュー
4. 承認後マージ

## コーディング規約

### Markdown
- 見出しは `#` から開始
- コードブロックは言語指定（```python, ```yaml, etc.）
- 箇条書きは `-` を使用

### YAML設定ファイル
- インデント: スペース2つ
- キーは小文字、ハイフン区切り（`backend-framework`）
- 配列は `-` で記述

### Jinja2テンプレート
- 変数: `{{ variable_name }}`
- 条件分岐: `{% if 'django' in backend %}...{% endif %}`
- ループ: `{% for item in items %}...{% endfor %}`

## バグ報告

Issueを作成する際は以下の情報を含めてください：

1. **環境**
   - OS: Windows/macOS/Linux
   - Python version
   - 使用した設定ファイル

2. **再現手順**
   ```bash
   python cli/generate.py my-config.yaml .
   ```

3. **期待される動作**

4. **実際の動作**

5. **エラーメッセージ（あれば）**

## 機能リクエスト

新しい機能の提案は大歓迎です！Issueに以下を記載してください：

1. **ユースケース**: どんな場面で必要か
2. **提案する機能**: 具体的な内容
3. **代替案**: 他の実装方法があれば

## コミュニティ

- **Discussions**: 質問、アイデア共有
- **Issues**: バグ報告、機能リクエスト
- **Pull Requests**: コード貢献

## ライセンス

このプロジェクトに貢献することで、MITライセンスに同意したことになります。
