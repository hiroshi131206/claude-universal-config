# Remotion コーディングルール

Remotion は React コンポーネントをそのまま動画・アニメーションとしてレンダリングするライブラリ。
Claude Code でコンポーネントを生成し、プロダクトデモ・SNS リール・ランディングページアニメーションを効率的に作る。

## 基本原則

- **1シーン = 1コンポーネント**: 各シーンを独立したReactコンポーネントにする
- **アニメーションは `useCurrentFrame` + `interpolate` で制御**: 時間軸に基づいた宣言的な記述
- **マジックナンバー禁止**: FPS・デュレーションは定数として定義する
- **型安全**: すべてのプロパティに TypeScript の型を付ける

## ファイル構造

```
src/
  remotion/
    Root.tsx              # 全コンポジションの登録
    constants.ts          # FPS, DURATION などの共通定数
    compositions/
      ProductDemo.tsx     # コンポジション（動画全体）
    scenes/
      Intro.tsx           # シーン1
      FeatureShowcase.tsx # シーン2
      CTA.tsx             # シーン3
    components/
      AnimatedText.tsx    # 再利用可能なアニメーションコンポーネント
      SVGIllustration.tsx
    styles/
      brand.ts            # ブランドカラー・フォント定数
```

## 定数管理

```typescript
// constants.ts
export const FPS = 30;
export const DURATION_INTRO = 3 * FPS;      // 3秒
export const DURATION_FEATURE = 5 * FPS;    // 5秒
export const DURATION_CTA = 2 * FPS;        // 2秒
export const TOTAL_DURATION = DURATION_INTRO + DURATION_FEATURE + DURATION_CTA;

export const BRAND = {
  primary: '#0066FF',
  secondary: '#FF6B35',
  bg: '#0A0A0A',
  text: '#FFFFFF',
  fontFamily: 'Inter, sans-serif',
};
```

## アニメーションパターン

### フェードイン

```typescript
import { useCurrentFrame, interpolate, AbsoluteFill } from 'remotion';

const FadeIn: React.FC<{ children: React.ReactNode; start?: number; duration?: number }> = ({
  children,
  start = 0,
  duration = 20,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [start, start + duration], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return <div style={{ opacity }}>{children}</div>;
};
```

### スライドイン

```typescript
const slideY = interpolate(frame, [0, 20], [40, 0], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
// style={{ transform: `translateY(${slideY}px)` }}
```

### スケールアニメーション（spring）

```typescript
import { spring, useVideoConfig } from 'remotion';

const { fps } = useVideoConfig();
const scale = spring({ frame, fps, config: { stiffness: 100, damping: 12 } });
// style={{ transform: `scale(${scale})` }}
```

## シーン構成パターン（プロダクトデモ）

```typescript
// compositions/ProductDemo.tsx
import { Series } from 'remotion';

export const ProductDemo: React.FC = () => (
  <AbsoluteFill style={{ background: BRAND.bg }}>
    <Series>
      <Series.Sequence durationInFrames={DURATION_INTRO}>
        <Intro />
      </Series.Sequence>
      <Series.Sequence durationInFrames={DURATION_FEATURE}>
        <FeatureShowcase />
      </Series.Sequence>
      <Series.Sequence durationInFrames={DURATION_CTA}>
        <CTA />
      </Series.Sequence>
    </Series>
  </AbsoluteFill>
);
```

## SVGイラスト生成ルール

- SVGコンポーネントは `viewBox="0 0 400 300"` などで固定サイズを持つ
- アニメーションは `strokeDashoffset` / `opacity` / `transform` で付ける
- パスの描画アニメーション（手書き風）には `strokeDasharray` + `interpolate` を使う

```typescript
const pathLength = 300;
const draw = interpolate(frame, [10, 40], [pathLength, 0], { extrapolateRight: 'clamp' });
// <path strokeDasharray={pathLength} strokeDashoffset={draw} ... />
```

## テキストアニメーション

- タイプライター効果: `text.slice(0, Math.floor(interpolate(frame, [0, 30], [0, text.length])))`
- ワードごとのフェードイン: 単語を `<span>` で分割して `delay` をずらす
- グラデーションテキスト: CSS `background-clip: text` + `WebkitTextFillColor: transparent`

## トランジション（remotion-transitions）

```typescript
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { slide } from '@remotion/transitions/slide';

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneA />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 15 })}
  />
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneB />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

## レンダリング・エクスポート

```bash
# プレビュー
npx remotion studio

# 動画レンダリング（MP4）
npx remotion render src/remotion/Root.tsx ProductDemo out/demo.mp4 --codec=h264

# GIF（SNS向け）
npx remotion render src/remotion/Root.tsx ProductDemo out/demo.gif --codec=gif

# 静止画（サムネイル）
npx remotion still src/remotion/Root.tsx ProductDemo out/thumb.png --frame=30
```

## SNS リール向け設定

```typescript
// Root.tsx
registerRoot(() => (
  <Composition
    id="Reel"
    component={ReelComposition}
    durationInFrames={300}   // 10秒 @ 30fps
    fps={30}
    width={1080}
    height={1920}            // 縦型 9:16（Instagram/TikTok/Shorts）
  />
));
```

## パフォーマンス

- 重い計算は `useMemo` でキャッシュする
- 画像は `staticFile()` で参照する（`public/` 以下に配置）
- フォントは `@remotion/google-fonts` を使う（ビルド時に埋め込み）
- シーンが多い場合は `lazyComponent` でコード分割する

## アンチパターン

- `useEffect` でアニメーション制御しない → `useCurrentFrame` で宣言的に書く
- `setTimeout` / `setInterval` 使用禁止 → フレーム数で制御する
- `Math.random()` をレンダリング中に使わない → 毎フレーム値が変わる
  → シード付き乱数（`seedrandom` など）か、静的な値を使う
