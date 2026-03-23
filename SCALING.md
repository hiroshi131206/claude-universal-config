# Scaling Guide

現在の構成は個人〜チーム利用として完結している。
このファイルは「必要になったとき」に何をどう追加するかを記録したもの。

---

## 現在の構成（個人〜チーム用途として適切）

```
core/skills/<skill>/
├── SKILL.md          # 指示・フロントマター
└── references/       # ドメイン知識・詳細仕様（複雑なスキルのみ）
```

| スキル | SKILL.md | references |
|---|---|---|
| autoresearch | ✅ | ✅ 11ファイル |
| frontend-design | ✅ | — (シンプルな用途) |
| grepai | ✅ | — (ツールラッパー) |
| skill-creator | ✅ | ✅ 4ファイル |
| swiftui-pro | ✅ | ✅ 9ファイル |

---

## 拡張コンポーネント一覧

### 1. `evaluation/` — スキルの品質検証

**トリガー（こうなったら追加）:**
- 「このスキルちゃんと動いてる？」と疑い始めたとき
- チームや他プロジェクトに展開する前
- スキルを修正したあと、意図せず挙動が変わっていないか確認したいとき

**追加手順:**
```
core/skills/<skill>/
└── evaluation/
    ├── should-trigger.md    # トリガーすべきクエリ 10件
    ├── should-not-trigger.md # トリガーすべきでないクエリ 10件
    └── expected-outputs.md  # 主要ユースケースの期待出力
```

`should-trigger.md` の書き方:
```markdown
# Should Trigger

- "SwiftUI のビューをレビューして"
- "このコードを iOS 向けに最適化して"
- "SwiftUI で NavigationStack を使いたい"
...（10件）
```

検証方法: 各クエリを実際に Claude に投げ、スキルがロードされるか確認。
目標: 10件中 9件以上でトリガー。

---

### 2. `assets/` — スキルが参照する静的ファイル

**トリガー（こうなったら追加）:**
- スキルの指示の中で「このテンプレートを使って」と言いたいファイルが出てきたとき
- スキルが参照する設定ファイル・サンプルコード・チェックリストが増えてきたとき
- references/ に入れるには「コード」や「テンプレート」であるとき

**追加手順:**
```
core/skills/<skill>/
└── assets/
    └── <ファイル名>    # テンプレート、サンプルコード、設定例など
```

SKILL.md 内での参照方法:
```markdown
`assets/component-template.tsx` を雛形として使うこと。
```

---

### 3. `scripts/` — 決定論的バリデーション

**トリガー（こうなったら追加）:**
- 「Claude の判断」ではなく「コードで確実に検証したい」ことが出てきたとき
- フォーマットチェック・lint・テスト実行など、スクリプトで代替できる検証があるとき
- quality-checklist.md の項目をスクリプトで自動化したいとき

**追加手順:**
```
core/skills/<skill>/
└── scripts/
    └── validate.py    # or validate.sh
```

SKILL.md 内での参照方法:
```markdown
### Step 2: Validate
Run: `python scripts/validate.py --input <file>`
```

---

### 4. `claude -p` — 自動化・CI/CD 組み込み

**トリガー（こうなったら追加）:**
- 「PR が作られるたびに自動でレビューしたい」など、人間が手動実行しなくていい状況が出てきたとき
- GitHub Actions・Cron・他ツールから Claude を呼び出したいとき

**追加手順:**

1. `.github/workflows/` などに YAML を作成
2. スキルの内容をシステムプロンプトとして渡す
3. 出力を Slack・PR コメントなどに送る

```bash
# 基本形
echo "レビュー対象コード" | claude -p "swiftui-pro スキルでレビューして"

# CI での使用例
git diff main | claude -p "$(cat core/skills/swiftui-pro/SKILL.md)" > review.txt
```

注意: references/ は `claude -p` では自動ロードされない。
必要なら SKILL.md に参照先の内容を事前にマージするか、プロンプトに含める。

---

### 5. Anthropic SDK — アプリ・API への組み込み

**トリガー（こうなったら追加）:**
- Web アプリ・Slack Bot・VS Code 拡張など、UI を持つツールにスキルを埋め込みたいとき
- 複数のスキルを組み合わせて独自のワークフローを API として提供したいとき
- `claude -p` では制御が足りなくなったとき（ストリーミング、複数ターン、ツール呼び出しなど）

**追加手順:**

```python
import anthropic
from pathlib import Path

client = anthropic.Anthropic()

def run_skill(skill_name: str, user_input: str) -> str:
    skill_path = Path(f"core/skills/{skill_name}/SKILL.md")
    system_prompt = skill_path.read_text()

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_input}]
    )
    return response.content[0].text
```

注意: references/ は SDK では自動ロードされない。
必要な references を system prompt に結合して渡すか、ユーザーメッセージに含める。

---

## 判断フロー

```
スキルが期待通り動かない        → evaluation/ を追加して原因を特定
スキルが参照するファイルが増えた → assets/ を追加
検証をコードで自動化したい       → scripts/ を追加
人間なしで自動実行したい         → claude -p を検討
UIやAPIに組み込みたい           → SDK を検討
```

いずれも「必要になってから追加」。先回りして全部入れない。
