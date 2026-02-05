---
name: frontend-performance
description: フロントエンドパフォーマンス最適化ガイド。Core Web Vitals改善、バンドルサイズ削減、レンダリング最適化、画像最適化など、高速なWebアプリケーション構築のベストプラクティス。
---

# Frontend Performance Skill

## 📋 目次

### 基礎編（このファイル）
1. [概要](#概要)
2. [いつ使うか](#いつ使うか)
3. [Core Web Vitals](#core-web-vitals)
4. [バンドルサイズ削減](#バンドルサイズ削減)
5. [レンダリング最適化](#レンダリング最適化)
6. [画像最適化](#画像最適化)
7. [実践例](#実践例)
8. [計測ツール](#計測ツール)
9. [Agent連携](#agent連携)

### 詳細ガイド（完全版）
1. [Core Web Vitals完全ガイド](./guides/core-web-vitals/core-web-vitals-complete.md) - 30,000文字
2. [バンドル最適化完全ガイド](./guides/bundle/bundle-optimization-complete.md) - 26,000文字
3. [レンダリング最適化完全ガイド](./guides/rendering/rendering-optimization-complete.md) - 27,000文字

---

## 概要

このSkillは、フロントエンドパフォーマンス最適化をカバーします：

- **Core Web Vitals** - LCP, INP, CLS, TTFB
- **バンドルサイズ削減** - Code Splitting, Tree Shaking
- **レンダリング最適化** - SSR, SSG, ISR
- **画像最適化** - WebP, Next/Image
- **キャッシング** - CDN, Service Worker
- **計測** - Lighthouse, Web Vitals

## 📚 公式ドキュメント・参考リソース

**このガイドで学べること**: Core Web Vitals改善、バンドル最適化、レンダリング戦略、画像最適化、キャッシング戦略
**公式で確認すべきこと**: 最新のパフォーマンス指標、ブラウザアップデート、フレームワーク最適化機能

### 主要な公式ドキュメント

- **[web.dev Performance](https://web.dev/performance/)** - Googleパフォーマンスガイド
  - [Core Web Vitals](https://web.dev/vitals/)
  - [Optimize LCP](https://web.dev/optimize-lcp/)
  - [Optimize INP](https://web.dev/optimize-inp/)

- **[Next.js Performance](https://nextjs.org/docs/app/building-your-application/optimizing)** - Next.js最適化ガイド
  - [Images](https://nextjs.org/docs/app/building-your-application/optimizing/images)
  - [Fonts](https://nextjs.org/docs/app/building-your-application/optimizing/fonts)

- **[Chrome DevTools](https://developer.chrome.com/docs/devtools/)** - パフォーマンス分析ツール
  - [Performance Panel](https://developer.chrome.com/docs/devtools/performance/)

- **[WebPageTest Documentation](https://docs.webpagetest.org/)** - パフォーマンス測定

### 関連リソース

- **[Lighthouse](https://developer.chrome.com/docs/lighthouse/)** - 自動パフォーマンス監査
- **[Bundle Analyzer](https://github.com/webpack-contrib/webpack-bundle-analyzer)** - バンドル分析
- **[Can I Use](https://caniuse.com/)** - ブラウザサポート確認

---

### 📚 詳細ガイド

**プロダクションレベルの最適化を学ぶには、以下の完全ガイドを参照してください：**

#### 1. [Core Web Vitals完全ガイド](./guides/core-web-vitals/core-web-vitals-complete.md)
**30,000文字 | 実測値データ | 業界別ベンチマーク**

- LCP、INP、CLS、TTFBの完全解説
- 各指標の改善手法（25以上のパターン）
- 実測値データ（ECサイト、ブログ、ダッシュボード）
  - LCP改善: 4.2秒 → 1.8秒 (-57.1%)
  - INP改善: 280ms → 65ms (-76.8%)
  - CLS改善: 0.25 → 0.05 (-80.0%)
- よくある間違いと解決策
- 業界別ベンチマーク（EC、メディア、SaaS）
- CI/CDでの継続的モニタリング戦略

#### 2. [バンドル最適化完全ガイド](./guides/bundle/bundle-optimization-complete.md)
**26,000文字 | Code Splitting | 依存関係管理**

- バンドル分析ツール完全活用
- Code Splitting戦略（5パターン）
- Tree Shakingの完全理解
- 依存関係の最適化（moment → date-fns等）
- Webpack/Vite設定最適化
- 実測値データ
  - 初期バンドル削減: 850KB → 180KB (-78.8%)
  - ページロード時間: 3.2秒 → 1.1秒 (-65.6%)
- パフォーマンスバジェット設定

#### 3. [レンダリング最適化完全ガイド](./guides/rendering/rendering-optimization-complete.md)
**27,000文字 | SSR・ISR | React最適化 | 仮想化**

- レンダリング戦略の選択（SSR、SSG、ISR、CSR）
- Next.js App Routerでの実装
- React最適化パターン（15以上）
  - React.memo、useMemo、useCallback詳解
  - コンポーネント分割戦略
  - 状態管理の最適化
- 仮想化（react-window完全ガイド）
- 実測値データ
  - 仮想化: メモリ -75% (380MB → 95MB)、FPS +300% (15 → 60)
  - SSR vs CSR: LCP -77% (2,200ms → 500ms)

**合計: 83,000文字 | 40以上の完全実装例 | 実プロジェクトの測定データ**

---

### 🎓 学習パス

#### 初心者向け
1. このファイルで基礎を理解
2. [Core Web Vitals完全ガイド](./guides/core-web-vitals/core-web-vitals-complete.md)でパフォーマンス指標を習得
3. 自サイトでLighthouse実行

#### 中級者向け
1. [バンドル最適化完全ガイド](./guides/bundle/bundle-optimization-complete.md)でバンドルサイズ削減
2. [レンダリング最適化完全ガイド](./guides/rendering/rendering-optimization-complete.md)でReact最適化
3. 実プロジェクトで測定→改善のサイクル

#### 上級者向け
1. 全ての詳細ガイドを参照しながら、大規模アプリケーションを最適化
2. パフォーマンスバジェット設定
3. CI/CDパイプラインにLighthouse CI組み込み

---

## いつ使うか

### 🎯 必須のタイミング

- [ ] プロダクションデプロイ前
- [ ] パフォーマンス問題発生時
- [ ] 新機能追加時（パフォーマンス影響確認）
- [ ] 画像・メディア追加時

### 🔄 定期的に

- [ ] 週次（Lighthouse スコア計測）
- [ ] 月次（バンドルサイズ分析）

---

## Core Web Vitals

### 主要指標

| 指標 | 説明 | 目標 |
|-----|------|------|
| **LCP** (Largest Contentful Paint) | 最大コンテンツの表示時間 | < 2.5秒 |
| **FID** (First Input Delay) | 初回入力遅延 | < 100ms |
| **CLS** (Cumulative Layout Shift) | レイアウトシフト | < 0.1 |

### LCP改善

#### 1. Server-Side Rendering（SSR）

```tsx
// Next.js App Router（デフォルトでSSR）
export default async function Page() {
  const data = await fetch('https://api.example.com/data')
  return <div>{/* content */}</div>
}
```

#### 2. 画像最適化

```tsx
// Next.js Image（自動最適化）
import Image from 'next/image'

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // Above the fold
/>
```

#### 3. フォント最適化

```tsx
// next.config.js
module.exports = {
  optimizeFonts: true,
}

// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({ children }) {
  return (
    <html lang="ja" className={inter.className}>
      <body>{children}</body>
    </html>
  )
}
```

### FID改善

#### 1. コード分割

```tsx
// 動的インポート
import dynamic from 'next/dynamic'

const HeavyComponent = dynamic(() => import('@/components/HeavyComponent'), {
  loading: () => <p>Loading...</p>,
})

export default function Page() {
  return <HeavyComponent />
}
```

#### 2. JavaScript削減

```tsx
// ❌ 悪い例（不要なライブラリ）
import moment from 'moment' // 288KB

// ✅ 良い例（軽量ライブラリ）
import { format } from 'date-fns' // 13KB
```

### CLS改善

#### 1. 画像サイズ指定

```tsx
// ❌ 悪い例（サイズ未指定 → レイアウトシフト）
<img src="/image.jpg" alt="Image" />

// ✅ 良い例（サイズ指定）
<Image
  src="/image.jpg"
  alt="Image"
  width={800}
  height={600}
/>
```

#### 2. フォント表示戦略

```css
/* ❌ 悪い例（フォント読み込み待ち → レイアウトシフト） */
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2');
  font-display: block;
}

/* ✅ 良い例（フォールバックフォント表示） */
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2');
  font-display: swap;
}
```

---

## バンドルサイズ削減

### 分析

```bash
# Next.js バンドル分析
pnpm add -D @next/bundle-analyzer

# next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer({
  // ...
})

# 実行
ANALYZE=true pnpm build
```

### Tree Shaking

```tsx
// ❌ 悪い例（全体インポート）
import _ from 'lodash' // 全体がバンドルされる

// ✅ 良い例（個別インポート）
import debounce from 'lodash/debounce'

// または
import { debounce } from 'lodash-es' // ES Modules版
```

### Code Splitting

```tsx
// ルートベース分割（Next.jsは自動）
app/
├── page.tsx        # Bundle 1
├── about/page.tsx  # Bundle 2
└── blog/page.tsx   # Bundle 3

// コンポーネント分割
const Modal = dynamic(() => import('@/components/Modal'))

function Page() {
  const [showModal, setShowModal] = useState(false)

  return (
    <>
      <button onClick={() => setShowModal(true)}>Open</button>
      {showModal && <Modal />} // 必要なときのみロード
    </>
  )
}
```

---

## レンダリング最適化

### SSG（Static Site Generation）

```tsx
// Next.js（ビルド時に生成）
export default async function Page() {
  const posts = await getPosts()
  return <PostList posts={posts} />
}

// 静的パス生成
export async function generateStaticParams() {
  const posts = await getPosts()
  return posts.map(post => ({ slug: post.slug }))
}
```

### ISR（Incremental Static Regeneration）

```tsx
// 60秒ごとに再生成
export const revalidate = 60

export default async function Page() {
  const posts = await fetch('https://api.example.com/posts', {
    next: { revalidate: 60 }
  }).then(r => r.json())

  return <PostList posts={posts} />
}
```

### React最適化

```tsx
// React.memo
const ExpensiveComponent = React.memo(({ data }) => {
  return <div>{/* ... */}</div>
})

// useMemo
function Component({ items }) {
  const sortedItems = useMemo(() => {
    return items.sort((a, b) => a.name.localeCompare(b.name))
  }, [items])

  return <List items={sortedItems} />
}

// useCallback
function Parent() {
  const handleClick = useCallback(() => {
    console.log('clicked')
  }, [])

  return <Child onClick={handleClick} />
}
```

---

## 画像最適化

### Next.js Image

```tsx
import Image from 'next/image'

// ✅ 自動最適化
<Image
  src="/images/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  quality={75} // デフォルト75
  priority // Above the fold
/>

// ✅ レスポンシブ画像
<Image
  src="/images/hero.jpg"
  alt="Hero"
  fill
  style={{ objectFit: 'cover' }}
  sizes="(max-width: 768px) 100vw, 50vw"
/>
```

### WebP形式

```tsx
// Next.jsは自動でWebPに変換
<Image src="/image.jpg" alt="Image" width={800} height={600} />
// → 自動的にWebPで配信（ブラウザサポート時）
```

### 遅延ローディング

```tsx
// デフォルトで遅延ローディング
<Image src="/image.jpg" alt="Image" width={800} height={600} />

// priorityで無効化（Above the fold画像）
<Image src="/hero.jpg" alt="Hero" width={1200} height={600} priority />
```

---

## 実践例

### Example 1: パフォーマンス監視

```tsx
// app/layout.tsx
import { SpeedInsights } from '@vercel/speed-insights/next'
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <SpeedInsights />
        <Analytics />
      </body>
    </html>
  )
}
```

### Example 2: 画像ギャラリー最適化

```tsx
import Image from 'next/image'

export default function Gallery({ images }) {
  return (
    <div className="grid grid-cols-3 gap-4">
      {images.map((image, index) => (
        <Image
          key={image.id}
          src={image.url}
          alt={image.alt}
          width={400}
          height={300}
          loading={index < 6 ? 'eager' : 'lazy'} // 最初の6枚は即座に読み込み
          quality={75}
        />
      ))}
    </div>
  )
}
```

### Example 3: 重いコンポーネントの遅延ローディング

```tsx
import dynamic from 'next/dynamic'

const Chart = dynamic(() => import('@/components/Chart'), {
  loading: () => <div>Loading chart...</div>,
  ssr: false, // クライアントサイドのみ
})

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Chart data={data} />
    </div>
  )
}
```

---

## 計測ツール

### Lighthouse

```bash
# Chrome DevTools → Lighthouse
# または
pnpm add -D lighthouse

npx lighthouse https://example.com --view
```

### Web Vitals計測

```bash
pnpm add web-vitals
```

```tsx
// app/layout.tsx
'use client'

import { useEffect } from 'react'
import { onCLS, onFID, onLCP } from 'web-vitals'

export function WebVitals() {
  useEffect(() => {
    onCLS(console.log)
    onFID(console.log)
    onLCP(console.log)
  }, [])

  return null
}
```

### Bundle Analyzer

```bash
ANALYZE=true pnpm build
```

---

## Agent連携

### 📖 Agentへの指示例

**パフォーマンス分析**
```
Lighthouse スコアを実行して、改善点を提案してください。
```

**バンドルサイズ削減**
```
バンドルサイズを分析して、大きな依存関係を特定してください。
軽量な代替ライブラリを提案してください。
```

**画像最適化**
```
/public/images 内の画像をNext.js Imageコンポーネントに置き換えてください。
```

---

## まとめ

### パフォーマンス最適化チェックリスト

- [ ] Core Web Vitals目標達成（LCP < 2.5s, FID < 100ms, CLS < 0.1）
- [ ] 画像最適化（Next/Image, WebP）
- [ ] バンドルサイズ削減（< 200KB初期ロード）
- [ ] Code Splitting実装
- [ ] Lighthouse スコア90+

---

_Last updated: 2025-12-26_
