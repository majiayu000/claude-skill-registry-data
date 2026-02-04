---
name: tech-blog-frontend-optimizer
description: テックブログのフロントエンド改善を総合的に支援するスキル。PV数・滞在時間の向上、ユーザー満足度の改善、SEO最適化を目的に、パフォーマンス、アクセシビリティ、UI/UX、Core Web Vitalsの改善提案を実施。「フロントエンドを改善して」「パフォーマンスを最適化」「UXを向上させたい」などのリクエストで利用。
---

# Tech Blog Frontend Optimizer

## 概要

このスキルは、テックブログ（https://maasaablog.com/）のフロントエンド改善を総合的に支援する。PV数・滞在時間の向上、ユーザー満足度の改善、SEO最適化を目的に、以下の領域で具体的な改善提案と実装支援を行う:

- **パフォーマンス最適化**: Core Web Vitals、ページ読み込み速度、リソース最適化
- **アクセシビリティ**: WCAG 2.1準拠、スクリーンリーダー対応、キーボードナビゲーション
- **UI/UX改善**: ユーザー体験の向上、読みやすさ、エンゲージメント強化
- **SEO技術最適化**: 構造化データ、メタタグ、クローラビリティ

## 技術スタック

ブログの現在の技術構成:
- **フレームワーク**: Astro（静的サイトジェネレータ）
- **最適化ツール**: Partytown 0.10.2（スクリプト実行の最適化）
- **アナリティクス**: Google Analytics（G-V5DNQ95RRH）
- **レンダリング**: Web Componentsベースの「astro-island」、段階的ハイドレーション

## 使用するタイミング

以下のようなリクエストがあった場合、このスキルを使用する:

- 「フロントエンドを改善して」
- 「ページ速度を上げたい」
- 「UXを向上させたい」
- 「Core Web Vitalsのスコアを改善」
- 「アクセシビリティ対応をしたい」
- 「離脱率を下げたい」
- 「滞在時間を増やしたい」

## クイックスタート

### 基本的な改善フロー

1. **現状分析**: ブログの現在の状態を診断
2. **優先度付け**: ROIの高い改善項目を特定
3. **改善提案**: 具体的な実装方法を提示
4. **検証計画**: 効果測定の方法を提案

### 簡単な例

ユーザーから「ページ速度を上げたい」とリクエストされた場合:

1. Lighthouseスコアの取得方法を提示
2. 現在のボトルネックを分析（画像サイズ、JavaScriptなど）
3. Astroの特性を活かした最適化方法を提案
4. Before/After測定方法を案内

## 主な機能

### 1. パフォーマンス最適化

ページ読み込み速度とCore Web Vitalsの改善を実施する。

#### Core Web Vitals の改善

**対象指標:**
- **LCP（Largest Contentful Paint）**: 2.5秒以内が目標
- **FID（First Input Delay）**: 100ms以内が目標
- **CLS（Cumulative Layout Shift）**: 0.1以下が目標

**改善項目:**

```markdown
#### LCP改善（最大コンテンツの描画）

1. **画像最適化**
   - WebP/AVIF形式への変換
   - 適切なサイズ設定（srcset活用）
   - 遅延読み込み（loading="lazy"）
   - LCP要素は優先読み込み（fetchpriority="high"）

2. **リソースの最適化**
   - フォントの事前読み込み（preload）
   - 重要CSSのインライン化
   - サードパーティスクリプトの遅延実行（Partytownの活用）

#### FID改善（初回入力遅延）

1. **JavaScriptの最適化**
   - コード分割（dynamic import）
   - 不要なJavaScriptの削除
   - Astroの部分ハイドレーション活用（client:load, client:visible）

2. **メインスレッドの負荷軽減**
   - 長いタスクの分割
   - Web Workerの活用（Partytownで実装済み）

#### CLS改善（レイアウトシフト）

1. **画像・動画のサイズ指定**
   - width/height属性の明示
   - aspect-ratioの使用

2. **動的コンテンツの対応**
   - 広告・埋め込みのスペース確保
   - フォントの最適化（font-display: swap）
```

**詳細**: `references/performance-optimization.md` を参照

#### リソース最適化

**画像の最適化:**
```astro
---
// Astroの画像最適化コンポーネント
import { Image } from 'astro:assets';
import myImage from '../assets/image.png';
---

<Image
  src={myImage}
  alt="説明文"
  width={800}
  height={600}
  format="webp"
  quality={80}
  loading="lazy"
  decoding="async"
/>
```

**フォントの最適化:**
```html
<!-- 重要フォントの事前読み込み -->
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>

<!-- フォント表示の最適化 -->
<style>
@font-face {
  font-family: 'MainFont';
  src: url('/fonts/main.woff2') format('woff2');
  font-display: swap; /* FOIT回避 */
}
</style>
```

**サードパーティスクリプトの最適化:**
```astro
---
// Partytownを活用したGoogle Analytics
---
<script type="text/partytown">
  // Google Analytics等のスクリプト
  // Web Workerで実行され、メインスレッドをブロックしない
</script>
```

**詳細**: `references/resource-optimization.md` を参照

### 2. アクセシビリティ改善

WCAG 2.1レベルAA準拠を目指した改善を実施する。

#### セマンティックHTML

**改善前:**
```html
<div class="article-card" onclick="location.href='/blog/post1'">
  <div class="image">
    <img src="thumbnail.png">
  </div>
  <div class="title">記事タイトル</div>
  <div class="date">2024-01-01</div>
</div>
```

**改善後:**
```html
<article class="article-card">
  <a href="/blog/post1" aria-label="記事タイトル - 2024年1月1日公開">
    <img src="thumbnail.webp" alt="記事のサムネイル画像" width="400" height="300" loading="lazy">
    <h2>記事タイトル</h2>
    <time datetime="2024-01-01">2024年1月1日</time>
  </a>
</article>
```

#### キーボードナビゲーション

**フォーカス管理:**
```css
/* フォーカス時の視覚的フィードバック */
a:focus-visible,
button:focus-visible {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

/* スキップリンクの実装 */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

**HTML:**
```html
<a href="#main-content" class="skip-link">メインコンテンツへスキップ</a>

<main id="main-content" tabindex="-1">
  <!-- メインコンテンツ -->
</main>
```

#### ARIA属性の適切な使用

```html
<!-- ページネーション -->
<nav aria-label="ページネーション">
  <ul>
    <li><a href="/page/1" aria-label="1ページ目">1</a></li>
    <li><a href="/page/2" aria-current="page" aria-label="現在のページ、2ページ目">2</a></li>
    <li><a href="/page/3" aria-label="3ページ目">3</a></li>
  </ul>
</nav>

<!-- カテゴリフィルター -->
<section aria-label="カテゴリフィルター">
  <h2>カテゴリ</h2>
  <ul role="list">
    <li><a href="/category/claude">Claude</a></li>
    <li><a href="/category/ai">生成AI</a></li>
  </ul>
</section>
```

**詳細**: `references/accessibility.md` を参照

### 3. UI/UX改善

ユーザーエンゲージメントと満足度を向上させる改善を実施する。

#### 読みやすさの向上

**タイポグラフィの最適化:**
```css
/* 本文の読みやすさ改善 */
article {
  /* 行の長さ: 45-75文字が理想 */
  max-width: 70ch;
  margin: 0 auto;

  /* 行間: 1.5-1.8が読みやすい */
  line-height: 1.6;

  /* フォントサイズ: 最低16px */
  font-size: 16px;

  /* コントラスト比: 4.5:1以上（WCAG AA） */
  color: #333;
  background: #fff;
}

/* 見出しの階層を明確に */
h2 {
  font-size: 2em;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 700;
}

h3 {
  font-size: 1.5em;
  margin-top: 1.2em;
  margin-bottom: 0.4em;
  font-weight: 600;
}
```

#### ユーザーエンゲージメント強化

**1. プログレスインジケーター（読書進捗バー）:**
```astro
---
// components/ReadingProgress.astro
---
<div id="reading-progress" role="progressbar" aria-label="記事の読書進捗" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>

<script>
  const progressBar = document.getElementById('reading-progress');

  window.addEventListener('scroll', () => {
    const winScroll = document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;

    progressBar.style.width = scrolled + '%';
    progressBar.setAttribute('aria-valuenow', Math.round(scrolled));
  });
</script>

<style>
  #reading-progress {
    position: fixed;
    top: 0;
    left: 0;
    height: 4px;
    background: linear-gradient(to right, #0066cc, #00ccff);
    z-index: 1000;
    transition: width 0.2s ease;
  }
</style>
```

**2. 目次の自動生成（既存機能の強化）:**
```astro
---
// components/TableOfContents.astro
// H2要素から自動生成（既存機能）を強化
---
<nav class="toc" aria-label="目次">
  <h2>目次</h2>
  <ul id="toc-list">
    <!-- JavaScript で動的生成 -->
  </ul>
</nav>

<script>
  // 現在の見出しをハイライト（スクロール連動）
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const id = entry.target.getAttribute('id');
      const tocLink = document.querySelector(`#toc-list a[href="#${id}"]`);

      if (entry.isIntersecting) {
        tocLink?.classList.add('active');
      } else {
        tocLink?.classList.remove('active');
      }
    });
  }, {
    rootMargin: '-80px 0px -80% 0px'
  });

  // 全てのH2要素を監視
  document.querySelectorAll('h2[id]').forEach(heading => {
    observer.observe(heading);
  });
</script>
```

**3. 関連記事のレコメンデーション:**
```astro
---
// components/RelatedArticles.astro
interface Props {
  currentCategory: string;
  currentTags: string[];
  excludeSlug: string;
}

const { currentCategory, currentTags, excludeSlug } = Astro.props;

// カテゴリとタグの類似性で関連記事を取得
const relatedPosts = await getRelatedPosts(currentCategory, currentTags, excludeSlug);
---

<section aria-label="関連記事">
  <h2>関連記事</h2>
  <ul class="related-articles">
    {relatedPosts.map(post => (
      <li>
        <article>
          <a href={`/blog/${post.slug}`}>
            <img src={post.thumbnail} alt="" width="200" height="150" loading="lazy">
            <h3>{post.title}</h3>
            <p>{post.excerpt}</p>
          </a>
        </article>
      </li>
    ))}
  </ul>
</section>
```

**4. ダークモードの実装:**
```astro
---
// components/ThemeToggle.astro
---
<button
  id="theme-toggle"
  aria-label="ダークモード切替"
  aria-pressed="false"
>
  <span class="light-icon">☀️</span>
  <span class="dark-icon">🌙</span>
</button>

<script>
  const theme = (() => {
    if (typeof localStorage !== 'undefined' && localStorage.getItem('theme')) {
      return localStorage.getItem('theme');
    }
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light';
  })();

  if (theme === 'light') {
    document.documentElement.classList.remove('dark');
  } else {
    document.documentElement.classList.add('dark');
  }

  window.localStorage.setItem('theme', theme);

  const handleToggleClick = () => {
    const element = document.documentElement;
    element.classList.toggle('dark');

    const isDark = element.classList.contains('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');

    // ARIA属性更新
    document.getElementById('theme-toggle')?.setAttribute('aria-pressed', isDark);
  };

  document.getElementById('theme-toggle')?.addEventListener('click', handleToggleClick);
</script>

<style>
  :root {
    --bg-color: #ffffff;
    --text-color: #333333;
  }

  :root.dark {
    --bg-color: #1a1a1a;
    --text-color: #e0e0e0;
  }

  body {
    background-color: var(--bg-color);
    color: var(--text-color);
    transition: background-color 0.3s ease, color 0.3s ease;
  }
</style>
```

**詳細**: `references/ux-improvements.md` を参照

#### モバイル最適化

**レスポンシブデザイン:**
```css
/* モバイルファースト */
.article-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  padding: 1rem;
}

/* タブレット */
@media (min-width: 768px) {
  .article-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
    padding: 2rem;
  }
}

/* デスクトップ */
@media (min-width: 1024px) {
  .article-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 2.5rem;
  }
}
```

**タッチ対応:**
```css
/* タップターゲットサイズ: 最低44x44px */
.card-link {
  min-height: 44px;
  min-width: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* タッチ時のフィードバック */
@media (hover: none) {
  .card-link:active {
    background-color: rgba(0, 0, 0, 0.1);
  }
}
```

### 4. SEO技術最適化

検索エンジンのクローラビリティとインデックス品質を向上させる。

#### 構造化データの実装

**記事ページ（Article Schema）:**
```astro
---
// layouts/BlogPost.astro
const { frontmatter } = Astro.props;

const structuredData = {
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": frontmatter.title,
  "description": frontmatter.description,
  "image": frontmatter.image,
  "datePublished": frontmatter.pubDate,
  "dateModified": frontmatter.updatedDate || frontmatter.pubDate,
  "author": {
    "@type": "Person",
    "name": "Masayan",
    "url": "https://maasaablog.com/about"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Masayan Tech Blog",
    "logo": {
      "@type": "ImageObject",
      "url": "https://maasaablog.com/logo.png"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": `https://maasaablog.com/blog/${frontmatter.slug}`
  }
};
---

<script type="application/ld+json" set:html={JSON.stringify(structuredData)} />
```

**パンくずリスト（BreadcrumbList Schema）:**
```astro
---
const breadcrumbData = {
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "ホーム",
      "item": "https://maasaablog.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "ブログ",
      "item": "https://maasaablog.com/blog"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": frontmatter.title,
      "item": `https://maasaablog.com/blog/${frontmatter.slug}`
    }
  ]
};
---

<script type="application/ld+json" set:html={JSON.stringify(breadcrumbData)} />
```

**詳細**: `references/seo-technical.md` を参照

#### メタタグの最適化

```astro
---
// components/SEOHead.astro
interface Props {
  title: string;
  description: string;
  image?: string;
  publishDate?: Date;
  updateDate?: Date;
}

const { title, description, image, publishDate, updateDate } = Astro.props;
const canonicalURL = new URL(Astro.url.pathname, Astro.site);
const socialImage = image || '/default-og-image.png';
---

<!-- 基本メタタグ -->
<title>{title} | Masayan Tech Blog</title>
<meta name="description" content={description} />
<link rel="canonical" href={canonicalURL} />

<!-- Open Graph -->
<meta property="og:type" content="article" />
<meta property="og:url" content={canonicalURL} />
<meta property="og:title" content={title} />
<meta property="og:description" content={description} />
<meta property="og:image" content={new URL(socialImage, Astro.site)} />
<meta property="og:site_name" content="Masayan Tech Blog" />
{publishDate && <meta property="article:published_time" content={publishDate.toISOString()} />}
{updateDate && <meta property="article:modified_time" content={updateDate.toISOString()} />}

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:url" content={canonicalURL} />
<meta name="twitter:title" content={title} />
<meta name="twitter:description" content={description} />
<meta name="twitter:image" content={new URL(socialImage, Astro.site)} />
```

#### サイトマップとRSSの最適化

**サイトマップ（既存のRSS.xmlを強化）:**
```xml
<!-- public/sitemap.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://maasaablog.com/</loc>
    <lastmod>2025-10-25</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <!-- 各記事ページ -->
  <url>
    <loc>https://maasaablog.com/blog/post-slug</loc>
    <lastmod>2025-10-20</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

### 5. 分析と測定

改善効果を測定し、継続的な最適化を実施する。

#### 測定指標（KPI）

**1. パフォーマンス指標:**
```markdown
| 指標 | 現状 | 目標 | 測定方法 |
|------|------|------|---------|
| Lighthouse Performance | ? | 90+ | Chrome DevTools |
| LCP | ? | <2.5s | PageSpeed Insights |
| FID | ? | <100ms | PageSpeed Insights |
| CLS | ? | <0.1 | PageSpeed Insights |
| ページ読み込み時間 | ? | <3s | Google Analytics |
```

**2. ユーザーエンゲージメント指標:**
```markdown
| 指標 | 現状 | 目標 | 測定方法 |
|------|------|------|---------|
| 平均セッション時間 | ? | +30% | Google Analytics |
| 直帰率 | ? | <50% | Google Analytics |
| ページ/セッション | ? | 2.5+ | Google Analytics |
| スクロール深度 | ? | 75%+ | Google Analytics（イベント） |
```

**3. SEO指標:**
```markdown
| 指標 | 現状 | 目標 | 測定方法 |
|------|------|------|---------|
| オーガニック流入 | ? | +50% | Google Search Console |
| 平均掲載順位 | ? | Top 10 | Google Search Console |
| クリック率（CTR） | ? | 5%+ | Google Search Console |
| インデックス数 | 400記事 | 全記事 | Google Search Console |
```

#### Google Analyticsイベント設定

```html
<!-- 重要なユーザーアクションを追跡 -->
<script type="text/partytown">
  // スクロール深度
  window.addEventListener('scroll', () => {
    const scrollPercent = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;

    if (scrollPercent > 25 && !window.scrolled25) {
      gtag('event', 'scroll', { 'depth': '25%' });
      window.scrolled25 = true;
    }
    if (scrollPercent > 50 && !window.scrolled50) {
      gtag('event', 'scroll', { 'depth': '50%' });
      window.scrolled50 = true;
    }
    if (scrollPercent > 75 && !window.scrolled75) {
      gtag('event', 'scroll', { 'depth': '75%' });
      window.scrolled75 = true;
    }
  });

  // 外部リンククリック
  document.querySelectorAll('a[href^="http"]').forEach(link => {
    link.addEventListener('click', (e) => {
      gtag('event', 'click', {
        'event_category': 'outbound',
        'event_label': e.target.href
      });
    });
  });

  // 記事読了時間
  const startTime = Date.now();
  window.addEventListener('beforeunload', () => {
    const timeSpent = Math.round((Date.now() - startTime) / 1000);
    gtag('event', 'timing_complete', {
      'name': 'read_time',
      'value': timeSpent
    });
  });
</script>
```

**詳細**: `references/analytics.md` を参照

## 改善実施手順

### ステップ1: 現状診断

```markdown
## 診断チェックリスト

### パフォーマンス
- [ ] Lighthouse スコアを取得（Performance, Accessibility, Best Practices, SEO）
- [ ] PageSpeed Insights でCore Web Vitals確認
- [ ] WebPageTest で詳細分析
- [ ] Chrome DevTools でネットワーク分析

### アクセシビリティ
- [ ] WAVE でアクセシビリティチェック
- [ ] axe DevTools で詳細診断
- [ ] スクリーンリーダー（NVDA/JAWS）でテスト
- [ ] キーボードのみでナビゲーション確認

### UX
- [ ] Google Analytics でユーザー行動分析
- [ ] ヒートマップツール（Hotjar等）でクリック/スクロール分析
- [ ] モバイルデバイスで実機テスト
- [ ] 異なるブラウザでテスト

### SEO
- [ ] Google Search Console でインデックス状況確認
- [ ] 構造化データテストツールで検証
- [ ] モバイルフレンドリーテスト
- [ ] 被リンク・内部リンク構造確認
```

### ステップ2: 優先順位付け

改善項目をROI（投資対効果）でランク付け:

**高優先度（即実施）:**
- Core Web Vitals の改善（LCP, FID, CLS）
- 画像の最適化（WebP変換、サイズ最適化）
- 構造化データの実装
- アクセシビリティの基本対応（alt属性、セマンティックHTML）

**中優先度（1-2週間以内）:**
- ダークモード実装
- 関連記事レコメンデーション
- 読書進捗バー
- メタタグの最適化

**低優先度（長期的改善）:**
- A/Bテスト実施
- パーソナライゼーション
- PWA化
- オフライン対応

### ステップ3: 実装

優先度の高い項目から順次実装:

1. **Performance Quick Wins（即効性のある改善）:**
   - 画像をWebP化
   - 遅延読み込み実装
   - フォントの最適化

2. **Accessibility Baseline（基本対応）:**
   - alt属性追加
   - セマンティックHTML修正
   - キーボードナビゲーション確保

3. **UX Enhancements（体験向上）:**
   - 読書進捗バー追加
   - 目次のスクロール連動
   - 関連記事表示

4. **SEO Technical（技術SEO）:**
   - 構造化データ実装
   - メタタグ最適化
   - サイトマップ改善

### ステップ4: 測定と改善

```markdown
## 効果測定サイクル（2週間ごと）

1. **データ収集**
   - Google Analytics: セッション時間、直帰率、PV
   - Search Console: 流入数、CTR、順位
   - PageSpeed Insights: Core Web Vitals

2. **分析**
   - 目標値との比較
   - 改善効果の定量評価
   - 新たなボトルネック特定

3. **次のアクション決定**
   - さらなる最適化項目の特定
   - 新機能の検討
   - A/Bテストの計画

4. **レポート作成**
   - ステークホルダーへの報告
   - ナレッジの蓄積
```

## ベストプラクティス

### 1. Astroの特性を最大限活用

Astroは「ゼロJavaScriptがデフォルト」の思想:

```astro
---
// 静的コンテンツはJavaScriptなしでレンダリング
---
<article>
  <h1>{title}</h1>
  <p>{content}</p>
</article>

<!-- インタラクティブ要素のみJavaScript -->
<ThemeToggle client:load />
<CommentSection client:visible />
```

**部分ハイドレーションの戦略:**
- `client:load`: 即座に必要（例: テ���マ切替）
- `client:visible`: 画面に表示されたら（例: コメント欄）
- `client:idle`: アイドル時（例: 分析スクリプト）
- `client:media`: 特定画面サイズ（例: モバイルメニュー）

### 2. プログレッシブエンハンスメント

基本機能はJavaScriptなしでも動作させる:

```html
<!-- JavaScript無効でも動作 -->
<form action="/search" method="GET">
  <input type="text" name="q" placeholder="検索...">
  <button type="submit">検索</button>
</form>

<!-- JavaScriptで体験向上 -->
<script>
  // フェッチAPIで非同期検索
  // ただし、JavaScript無効でもフォーム送信は動作
</script>
```

### 3. パフォーマンス予算の設定

```markdown
## パフォーマンス予算

| リソース | 上限 |
|---------|-----|
| HTML | 50KB |
| CSS | 50KB |
| JavaScript（First-party） | 100KB |
| JavaScript（Third-party） | 50KB |
| 画像（ページあたり） | 500KB |
| フォント | 100KB |
| 合計ページサイズ | 1MB |
```

### 4. コンテンツ戦略との連携

フロントエンド改善はコンテンツ戦略と連動:

- **滞在時間向上**: 関連記事、目次、読書進捗バー
- **PV向上**: 内部リンク、カテゴリナビ、検索機能
- **エンゲージメント**: コメント欄、SNSシェアボタン、ニュースレター登録

## トラブルシューティング

### 問題1: Lighthouse スコアが上がらない

**原因と対策:**
```markdown
1. **サードパーティスクリプトの影響**
   - 対策: Partytown でWeb Worker化（実装済み）
   - 検証: Lighthouse の「Third-party」セクション確認

2. **画像サイズが大きい**
   - 対策: Astro の Image コンポーネントで自動最適化
   - 検証: Network タブで実際のサイズ確認

3. **未使用CSS/JavaScript**
   - 対策: PurgeCSS、Tree Shaking
   - 検証: Coverage タブで確認

4. **サーバーレスポンス時間**
   - 対策: CDN利用、静的ホスティング最適化
   - 検証: TTFB（Time To First Byte）測定
```

### 問題2: アクセシビリティエラーが多い

**よくあるエラーと修正:**
```markdown
1. **画像にalt属性がない**
   ```html
   <!-- 修正前 -->
   <img src="image.png">

   <!-- 修正後 -->
   <img src="image.png" alt="説明文">
   ```

2. **コントラスト比不足**
   ```css
   /* 修正前: コントラスト比 2.5:1 */
   color: #999;
   background: #fff;

   /* 修正後: コントラスト比 4.7:1（WCAG AA準拠） */
   color: #666;
   background: #fff;
   ```

3. **見出しレベルがスキップ**
   ```html
   <!-- 修正前: H2の次にH4 -->
   <h2>見出し2</h2>
   <h4>見出し4</h4>

   <!-- 修正後: 階層を正しく -->
   <h2>見出し2</h2>
   <h3>見出し3</h3>
   ```
```

### 問題3: モバイルでのパフォーマンスが悪い

**対策:**
```markdown
1. **画像の遅延読み込み**
   - ファーストビュー以外はlazy load
   - ファーストビューはfetchpriority="high"

2. **フォントの最適化**
   - WOFF2形式を使用
   - font-display: swap
   - 可変フォント（Variable Fonts）検討

3. **JavaScriptの削減**
   - Astroの部分ハイドレーション活用
   - 不要なライブラリの削除
```

## リファレンスファイル

### references/performance-optimization.md
パフォーマンス最適化の詳細ガイド:
- Core Web Vitals の各指標の改善方法
- リソース最適化のベストプラクティス
- Astro特有の最適化テクニック
- パフォーマンス測定ツールの使い方

### references/accessibility.md
アクセシビリティ対応ガイド:
- WCAG 2.1 チェックリスト
- セマンティックHTMLのパターン集
- ARIA属性の正しい使い方
- スクリーンリーダー対応

### references/ux-improvements.md
UX改善のアイデア集:
- エンゲージメント強化施策
- モバイルUXのベストプラクティス
- ダークモード実装ガイド
- マイクロインタラクション

### references/seo-technical.md
技術SEOガイド:
- 構造化データの実装例
- メタタグ最適化
- サイトマップ・RSS
- クローラビリティ改善

### references/analytics.md
分析・測定ガイド:
- KPIの設定方法
- Google Analytics イベント設定
- A/Bテストの実施方法
- レポート作成テンプレート

## まとめ

このスキルは、テックブログのフロントエンドを総合的に改善し、PV数・滞在時間の向上、ユーザー満足度の改善、SEO最適化を実現する。

**改善の優先順位:**
1. **パフォーマンス**: Core Web Vitals、画像最適化、リソース削減
2. **アクセシビリティ**: セマンティックHTML、ARIA、キーボードナビゲーション
3. **UX**: 読書進捗、関連記事、ダークモード
4. **SEO**: 構造化データ、メタタグ、内部リンク

**測定と改善:**
定期的に効果を測定し、データに基づいて継続的に最適化を実施する。

**Astroの活用:**
ゼロJavaScriptがデフォルトの思想を活かし、必要な部分のみインタラクティブにすることで、高速で使いやすいブログを実現する。
