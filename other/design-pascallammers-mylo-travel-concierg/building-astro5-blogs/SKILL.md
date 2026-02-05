---
name: building-astro5-blogs
description: Astro 5.x静的ブログ構築のベストプラクティス集。Islands Architecture、SSG、Content Layer API、画像最適化、ビルド最適化、SEOなど、パフォーマンスとUXを最大化するための公式推奨手法を提供。Astroコンポーネント/ページ作成時、Content Collections設定、画像最適化、クライアントディレクティブ選択、SEO実装時に使用。
---

# Astro 5.x Blog Best Practices

Astro 5.xを使用した静的ブログ構築における公式推奨のベストプラクティス。パフォーマンスとUXを最大化するための実装パターンを提供。

## 概要

このスキルは、Astro 5.xでSSG（Static Site Generation）ブログを構築する際の最新ベストプラクティスを提供する。特に以下の点に焦点を当てる：

- **Islands Architecture**: 最小限のJavaScriptで高速なページロード
- **Content Layer API**: Astro 5.0の新しいコンテンツ管理システム
- **画像最適化**: ビルド時の自動最適化とレスポンシブ対応
- **ビルド最適化**: キャッシングと並列処理による高速ビルド
- **SEO**: RSS、サイトマップ、構造化データ

## 核心原則

### 1. デフォルトは静的

Astroの最大の強みはSSG。すべてのページをビルド時に静的生成し、JavaScriptは最小限に。

```astro
---
// ✅ 良い例: デフォルトで静的HTML
import { Image } from 'astro:assets';
import hero from '../assets/hero.png';
---

<article>
  <h1>{title}</h1>
  <Image src={hero} alt="Hero" />
  <p>{content}</p>
</article>
```

### 2. Islands Architectureで最小限のJavaScript

インタラクティブ性が必要な部分だけJavaScriptを送信。

```astro
---
import CommentForm from '../components/CommentForm';
import ShareButtons from '../components/ShareButtons';
---

<!-- 静的コンテンツ: JavaScriptなし -->
<article>{content}</article>

<!-- アイランド1: ページロード時に必要 -->
<CommentForm client:load />

<!-- アイランド2: スクロールして表示されたら -->
<ShareButtons client:visible />
```

**クライアントディレクティブの選択**:
- `client:load` - すぐに必要（ヘッダーメニュー、モーダル）
- `client:visible` - スクロール先にある（シェアボタン、コメント）
- `client:idle` - 優先度低い（チャットウィジェット、分析）
- `client:media` - 特定画面サイズ（モバイル専用メニュー）

詳細は [islands-architecture.md](references/islands-architecture.md) を参照。

### 3. Content Layer APIで型安全なコンテンツ管理

Astro 5.0の新しいContent Layer APIを使用。

```typescript
// src/content/config.ts
import { z, defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/[^_]*.md', base: './src/blog' }),
  schema: z.object({
    title: z.string(),
    pubDate: z.date(),
    description: z.string(),
    tags: z.array(z.string())
  })
});

export const collections = { blog };
```

**利点**:
- TypeScriptによる型安全性
- Zodによるバリデーション
- ビルド間のキャッシング
- 数万件のコンテンツに対応

詳細は [content-layer-api.md](references/content-layer-api.md) を参照。

## 基本ワークフロー

### Step 1: Content Collectionのセットアップ

1. `src/content/config.ts`を作成
2. コレクションとスキーマを定義
3. Markdownファイルを`src/blog/`に配置

### Step 2: ページの作成

```astro
// src/pages/blog/index.astro - 記事一覧
const posts = await getCollection('blog');
```

```astro
// src/pages/blog/[slug].astro - 個別記事
export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.id },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await render(post);
```

### Step 3: 画像最適化

```astro
---
import { Image } from 'astro:assets';
import hero from '../assets/hero.png';
---

<!-- ヒーロー画像: 優先読み込み -->
<Image src={hero} alt="Hero" priority />

<!-- 記事内画像: レスポンシブ -->
<Image
  src={image}
  alt="..."
  layout="constrained"
  widths={[400, 800, 1200]}
/>
```

詳細は [image-optimization.md](references/image-optimization.md) を参照。

### Step 4: ビルド最適化

```javascript
// astro.config.mjs
export default defineConfig({
  // キャッシュディレクトリ
  cacheDir: './node_modules/.astro',
});
```

**重要**:
- ビルド間でキャッシュディレクトリを保持
- データ取得を並列化
- コンポーネント分離でストリーミング活用

詳細は [build-optimization.md](references/build-optimization.md) を参照。

### Step 5: SEOとRSS

```javascript
// src/pages/rss.xml.js
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = await getCollection("blog");
  return rss({
    title: 'My Blog',
    description: 'My blog description',
    site: context.site,
    items: posts.map((post) => ({
      title: post.data.title,
      pubDate: post.data.pubDate,
      description: post.data.description,
      link: `/blog/${post.id}/`,
    })),
  });
}
```

```javascript
// astro.config.mjs
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://example.com',
  integrations: [sitemap()],
});
```

詳細は [seo-rss.md](references/seo-rss.md) を参照。

## Markdownパイプラインのカスタマイズ

```javascript
// astro.config.mjs
import remarkGfm from 'remark-gfm';
import rehypeSlug from 'rehype-slug';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';

export default defineConfig({
  markdown: {
    // Remarkプラグイン（Markdown AST処理）
    remarkPlugins: [remarkGfm],
    // Rehypeプラグイン（HTML AST処理）
    rehypePlugins: [
      rehypeSlug,
      [rehypeAutolinkHeadings, { behavior: 'append' }]
    ],
  },
});
```

**よく使われるプラグイン**:
- `remark-gfm`: GitHub Flavored Markdown
- `remark-toc`: 目次自動生成
- `rehype-slug`: 見出しにID付与
- `rehype-autolink-headings`: アンカーリンク生成

詳細は [markdown-pipeline.md](references/markdown-pipeline.md) を参照。

## パフォーマンスチェックリスト

### Islands Architecture
- [ ] デフォルトは静的（ディレクティブなし）
- [ ] `client:load`は最小限（重要なUIのみ）
- [ ] `client:visible`で遅延読み込み活用
- [ ] `client:idle`で優先度低いコンポーネント

### Content Collections
- [ ] Content Layer APIを使用
- [ ] Zodスキーマでバリデーション
- [ ] `getCollection()`でフィルタリング
- [ ] ビルド間でキャッシュ保持

### 画像最適化
- [ ] `<Image />`コンポーネントを使用
- [ ] ヒーロー画像に`priority`属性
- [ ] レスポンシブ画像を設定
- [ ] `alt`属性は必須

### ビルド最適化
- [ ] データ取得を並列化
- [ ] コンポーネント分離でストリーミング
- [ ] キャッシュディレクトリを保持
- [ ] 不要な依存関係を削除

### SEO
- [ ] RSSフィードを提供
- [ ] サイトマップを生成
- [ ] 構造化データ（JSON-LD）を実装
- [ ] メタタグを適切に設定

## よくあるアンチパターン

### ❌ すべてをclient:loadで読み込む

```astro
<!-- 悪い例 -->
<Header client:load />
<Article client:load />
<Footer client:load />
```

**問題**: 大量のJavaScriptが送信され、パフォーマンス低下。

**解決**:
```astro
<!-- 良い例 -->
<Header />  <!-- 静的 -->
<Article /> <!-- 静的 -->
<Footer />  <!-- 静的 -->
<CommentForm client:visible /> <!-- 必要な部分だけ -->
```

### ❌ HTML `<img>`タグを使用

```astro
<!-- 悪い例 -->
<img src="/images/photo.jpg" alt="Photo" />
```

**問題**: 最適化されず、パフォーマンス低下。

**解決**:
```astro
<!-- 良い例 -->
<Image src={photo} alt="Photo" />
```

### ❌ データ取得を順次処理

```astro
---
// 悪い例
const posts = await getCollection('blog');
const authors = await getCollection('authors');
---
```

**問題**: 取得時間が合計される。

**解決**:
```astro
---
// 良い例
const [posts, authors] = await Promise.all([
  getCollection('blog'),
  getCollection('authors')
]);
---
```

## リファレンス

詳細な実装パターンは以下のリファレンスを参照：

- **[islands-architecture.md](references/islands-architecture.md)** - クライアントディレクティブの詳細、サーバーアイランド、状態共有
- **[content-layer-api.md](references/content-layer-api.md)** - Content Collectionsの詳細、クエリパターン、Legacy APIからの移行
- **[markdown-pipeline.md](references/markdown-pipeline.md)** - remarkプラグイン、rehypeプラグイン、カスタムプラグイン作成
- **[image-optimization.md](references/image-optimization.md)** - `<Image />`、`<Picture />`、レスポンシブ画像、`getImage()`
- **[build-optimization.md](references/build-optimization.md)** - キャッシング、並列処理、ストリーミング、MDX最適化
- **[seo-rss.md](references/seo-rss.md)** - RSSフィード、サイトマップ、構造化データ、メタタグ

## Astro 5.xでの重要な変更点

### Content Layer API（新機能）

Astro 5.0で導入された新しいコンテンツ管理システム。従来のContent Collectionsから移行する場合：

1. `loader`プロパティを追加
2. `glob`ローダーでファイルパターンを指定
3. 既存のスキーマ定義はそのまま使用可能

### パフォーマンス改善

- ビルド間のキャッシング強化
- 数万件のエントリに対応
- 画像最適化の高速化

## まとめ

Astro 5.xでSSGブログを構築する際の核心原則：

1. **デフォルトは静的** - JavaScriptは最小限
2. **Islands Architecture** - 必要な部分だけインタラクティブ
3. **Content Layer API** - 型安全なコンテンツ管理
4. **画像最適化** - 自動最適化とレスポンシブ対応
5. **ビルド最適化** - キャッシングと並列処理
6. **SEO** - RSS、サイトマップ、構造化データ

これらを実践することで、高速でUXに優れたブログを構築できる。
