---
name: reel
description: Remotion で SNS リール・プロダクトデモ動画を生成する。シーン設計 → React コンポーネント生成 → タイミング調整の流れを自動化。
argument-hint: "<topic-or-product> [--scenes N] [--format reel|demo|landing] [--duration <seconds>] [--brand <colors>]"
---

Remotion（React ベースの動画生成）を使って SNS リールやプロダクトデモを作る。
コンポーネントを書くだけで動画になる。Claude がスキャフォールドするので、あとはコピーとタイミングを調整してエクスポートするだけ。

## Argument Parsing（最初に行う）

$ARGUMENTS から抽出する:
- テーマ・プロダクト名（例: `SaaSのサインアップフロー`）
- `--scenes N` — シーン数（デフォルト: 3）
- `--format` — `reel`（縦型 9:16）/ `demo`（横型 16:9）/ `landing`（Webアニメーション）
- `--duration <seconds>` — 動画の長さ（デフォルト: reel=10秒, demo=30秒）
- `--brand <colors>` — ブランドカラー（例: `#0066FF,#FFFFFF,#0A0A0A`）

## 実行手順

### Phase 1: 環境確認

```bash
# Remotion がインストールされているか確認
cat package.json | grep remotion
```

インストールされていなければ案内する:
```bash
npm install remotion @remotion/cli @remotion/transitions
# TypeScript プロジェクトなら
npm install --save-dev @types/react
```

### Phase 2: プロジェクト構造を確認・作成

```bash
ls src/remotion/ 2>/dev/null || echo "remotion ディレクトリが存在しない"
```

存在しない場合は以下のファイルをスキャフォールドする:
- `src/remotion/Root.tsx`
- `src/remotion/constants.ts`

### Phase 3: シーン設計

ユーザーのテーマ・プロダクトからシーン構成を設計する。

**リール（SNS）の基本構成（10秒）:**
```
シーン1: フック（1.5秒）— 「この課題、ありますよね？」
シーン2: ソリューション提示（5秒）— 機能デモ・アニメーション
シーン3: 結果・CTA（3.5秒）— 「試してみよう」
```

**プロダクトデモの基本構成（30秒）:**
```
シーン1: 課題提示（5秒）
シーン2: 機能紹介①（8秒）
シーン3: 機能紹介②（8秒）
シーン4: ビフォー/アフター（5秒）
シーン5: CTA（4秒）
```

設計したシーン構成をユーザーに確認する（`AskUserQuestion`）。

### Phase 4: コンポーネント生成

承認されたシーン構成で以下を生成する:

1. **`src/remotion/constants.ts`** — FPS・デュレーション・ブランドカラー定数
2. **`src/remotion/scenes/<SceneName>.tsx`** — 各シーン（`useCurrentFrame` + `interpolate` ベース）
3. **`src/remotion/compositions/Main.tsx`** — `Series` でシーンを繋いだメインコンポジション
4. **`src/remotion/Root.tsx`** — コンポジション登録（フォーマットに応じた解像度）

**フォーマット別解像度:**
| フォーマット | width | height | 用途 |
|---|---|---|---|
| `reel` | 1080 | 1920 | Instagram/TikTok/YouTube Shorts |
| `demo` | 1920 | 1080 | YouTube/LP埋め込み |
| `landing` | 1200 | 675 | Webランディングページ |

### Phase 5: プレビュー起動

```bash
npx remotion studio
```

ユーザーに以下を伝える:
- ブラウザで `http://localhost:3000` を開いてプレビューできる
- フレームスライダーでタイミングを確認する
- `constants.ts` の DURATION 定数を変えてシーン長を調整する

### Phase 6: エクスポート

タイミングが確定したらエクスポートコマンドを提示する:

```bash
# MP4（YouTube/LP向け）
npx remotion render src/remotion/Root.tsx Main out/demo.mp4 --codec=h264

# GIF（SNS向け・ファイルサイズ小）
npx remotion render src/remotion/Root.tsx Main out/demo.gif --codec=gif

# WebM（Webページ埋め込み向け）
npx remotion render src/remotion/Root.tsx Main out/demo.webm --codec=vp8
```

## 再利用のコツ

- 作ったシーンコンポーネントは **props化**して再利用する
  - `<FeatureScene title="..." icon="..." color="..." />`
- 2本目以降は既存シーンのコピー＆タイミング変更のみ → 10分以内で完成
- `constants.ts` のブランドカラーだけ変えれば別プロダクト向けに転用できる

## 使用例

```
/reel SaaSのダッシュボード機能
/reel ユーザー登録フローのデモ --format demo --duration 30
/reel 新機能リリース告知 --scenes 3 --format reel --brand "#FF6B35,#FFFFFF,#1A1A1A"
```
