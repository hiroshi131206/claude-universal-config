---
name: encoding-fix
description: Shift-JIS/EUC-JP/CP932 ファイルまたはURLをUTF-8に変換してから内容を読み込む。古い日本語サイト・ファイルの調査に使う。
argument-hint: "<file-or-url> [--from-encoding shift_jis|euc_jp|cp932] [--save <output>] [--recursive]"
---

Claude Code は Shift-JIS・EUC-JP・CP932 などの日本語エンコーディングを直接読めない場合がある。
このコマンドは `tools/encoding-convert.py` を使って UTF-8 に変換してから内容を読み込む。

## 実行手順

### 1. ソースを特定する

$ARGUMENTS からソースを抽出する:
- ファイルパス（例: `./data/report.html`）
- URL（例: `https://example.com/old-page.html`）
- ディレクトリ（`--recursive` フラグと組み合わせ）

オプションを抽出する:
- `--from-encoding <enc>` — エンコーディングを手動指定
- `--save <path>` または `-o <path>` — 変換後のファイルを保存
- `--recursive` または `-r` — ディレクトリ内の全対象ファイルを処理
- `--detect-only` — 変換せずエンコーディングを確認するだけ

### 2. エンコーディングを確認する（オプション）

変換前に検出結果を確認したい場合:

```bash
python tools/encoding-convert.py <source> --detect-only
```

出力例:
```
./data/report.html: shift_jis (confidence: 90%)
```

### 3. 変換を実行する

**ファイルの場合（一時ファイルに出力）:**
```bash
python tools/encoding-convert.py <file> -o /tmp/converted.html
```

**URLの場合（一時ファイルに保存）:**
```bash
python tools/encoding-convert.py <url> -o /tmp/page_utf8.html
```

**ディレクトリ一括変換:**
```bash
python tools/encoding-convert.py <dir> --recursive
```

**エンコーディング手動指定:**
```bash
python tools/encoding-convert.py <file> --from-encoding shift_jis -o /tmp/out.html
```

### 4. 変換後のファイルを読み込む

変換が成功したら Read ツールでファイルを読み込む。

```
Read: /tmp/converted.html  (または指定した出力先)
```

### 5. 内容を報告する

読み込んだ内容を整理してユーザーに報告する。HTMLの場合は：
- タグを除去して本文テキストを抽出
- テーブルや見出しは Markdown 形式で整形
- 文字化けが残る場合は `--from-encoding` で別のエンコーディングを試す

## よくあるエンコーディングと用途

| エンコーディング | 別名 | よく見る場面 |
|---|---|---|
| `shift_jis` | SJIS, S-JIS | 古い日本語Webサイト、Windowsで作ったテキスト |
| `cp932` | Windows-31J | Windows日本語環境のファイル（SJIS拡張） |
| `euc_jp` | EUC-JP | 古いUnix/Linuxサーバーのコンテンツ |
| `iso2022_jp` | JIS | メール、一部の古いシステム |

## トラブルシューティング

**文字化けが直らない場合:**
```bash
# 別のエンコーディングを試す
python tools/encoding-convert.py <file> --from-encoding cp932 -o /tmp/out.html
python tools/encoding-convert.py <file> --from-encoding euc_jp -o /tmp/out.html
```

**chardet をインストールするとより精度が上がる:**
```bash
pip install chardet
# 以降は自動検出の精度が向上する
```

**URLアクセスがタイムアウトする場合:**
- URLをブラウザで開いて「名前を付けて保存」してから、ファイルとして渡す

## 使用例

```
/encoding-fix https://old-company-site.co.jp/report.html
/encoding-fix ./legacy-data/customers.csv --from-encoding cp932
/encoding-fix ./scraped-pages/ --recursive
/encoding-fix ./document.txt --detect-only
```
