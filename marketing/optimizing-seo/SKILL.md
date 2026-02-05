---
name: optimizing-seo
description: オーガニック検索流入を高めるためのSEO施策を設計・実行します。キーワード戦略、オンページ最適化、構造化データ、内部リンク計画、テクニカルSEOを提供します。検索順位向上、サイトクローラビリティ改善が必要な場合に使用してください。
disable-model-invocation: false
---

# SEO最適化

## 概要

オーガニック検索流入を最大化するための包括的なSEO施策を設計・実行するスキルです。キーワード戦略、オンページ最適化、構造化データ、内部リンク計画、テクニカルSEOをカバーします。

## 実行フロー

### Step 1: キーワード戦略と検索意図分析

#### キーワード選定

**キーワードタイプ:**

| タイプ | 例 | 検索意図 | 優先度 |
|--------|-----|----------|--------|
| トランザクショナル | "購入"、"申し込み" | 購買意欲高 | 高 |
| ナビゲーショナル | ブランド名 | 特定サイト探索 | 中 |
| インフォメーショナル | "方法"、"とは" | 情報収集 | 中-高 |
| コマーシャル | "比較"、"おすすめ" | 検討段階 | 高 |

#### 検索意図マッピング

```markdown
## キーワードクラスタリング

### クラスタ1: [メインキーワード]
- プライマリ: [volume: XXX, difficulty: XX]
- セカンダリ: [関連キーワード1], [関連キーワード2]
- ロングテール: [具体的なフレーズ]
```

### Step 2: オンページSEO最適化

#### タイトルタグ最適化

**ベストプラクティス:**

- 文字数: 50-60文字（表示制限: 約30文字）
- プライマリキーワードを前方配置
- ブランド名は末尾
- クリックを誘う表現（数字、年号、"方法"など）

**例:**

```html
<!-- Good -->
<title>SEO対策完全ガイド2025 | 検索上位表示の実践テクニック - ブランド名</title>

<!-- Bad -->
<title>ブランド名 | SEO</title>
```

#### メタディスクリプション

**要件:**

- 文字数: 120-160文字
- プライマリ・セカンダリキーワードを自然に含める
- 行動を促す表現（"今すぐ確認"、"詳しく見る"）
- ページの価値提案を明確化

#### 見出し構造（H1-H6）

**階層設計:**

```markdown
# H1: メインキーワードを含むページタイトル（1つのみ）
## H2: セクション見出し（プライマリ・セカンダリキーワード）
### H3: サブセクション（ロングテールキーワード）
#### H4-H6: 詳細な階層化
```

**注意点:**

- H1は1ページに1つのみ
- 見出しの階層をスキップしない（H2 → H4は不可）
- 見出しだけで内容が理解できる構成

#### 本文最適化

**キーワード密度:**

- 目安: 2-3%（過度な詰め込みは逆効果）
- LSI（Latent Semantic Indexing）キーワードを自然に含める
- 同義語・関連語を活用

**可読性:**

- 段落: 3-4文（150-200文字）
- 箇条書き・リストの活用
- 適切な改行と余白

### Step 3: 構造化データ（Schema.org）

#### 主要なスキーマタイプ

**Article（記事）:**

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "記事タイトル",
  "author": {
    "@type": "Person",
    "name": "著者名"
  },
  "datePublished": "2025-01-15",
  "dateModified": "2025-01-20",
  "image": "https://example.com/image.jpg",
  "publisher": {
    "@type": "Organization",
    "name": "組織名",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.jpg"
    }
  }
}
```

**Product（商品）:**

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "商品名",
  "image": "https://example.com/product.jpg",
  "description": "商品説明",
  "brand": {
    "@type": "Brand",
    "name": "ブランド名"
  },
  "offers": {
    "@type": "Offer",
    "price": "1000",
    "priceCurrency": "JPY",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "89"
  }
}
```

**FAQ:**

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "質問内容",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "回答内容"
    }
  }]
}
```

**Breadcrumb（パンくずリスト）:**

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [{
    "@type": "ListItem",
    "position": 1,
    "name": "ホーム",
    "item": "https://example.com/"
  }, {
    "@type": "ListItem",
    "position": 2,
    "name": "カテゴリ",
    "item": "https://example.com/category/"
  }]
}
```

### Step 4: 内部リンク戦略

#### サイトアーキテクチャの最適化

**理想的な構造:**

```
トップページ（権威が最も高い）
├── カテゴリページ（2-3クリック以内）
│   ├── サブカテゴリ
│   │   └── 個別ページ
│   └── 個別ページ
└── 重要ページ
```

#### 内部リンクのベストプラクティス

**アンカーテキスト:**

- 説明的で関連性のあるテキスト（"こちら"は避ける）
- ターゲットページのキーワードを含める
- 自然な文脈での配置

**リンク配置:**

- コンテンツの文脈内（コンテキストリンク）が最も効果的
- 関連記事セクション
- パンくずリスト
- サイトマップ

**リンク構造の指標:**

- 孤立ページ（orphan page）を作らない
- 3クリック以内で全ページにアクセス可能
- ページランクを効果的に分配

### Step 5: テクニカルSEO

#### クローラビリティ

**robots.txt:**

```txt
User-agent: *
Disallow: /admin/
Disallow: /api/
Allow: /

Sitemap: https://example.com/sitemap.xml
```

**XML Sitemap:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page/</loc>
    <lastmod>2025-01-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

#### ページ速度最適化

**Core Web Vitals目標:**

- LCP (Largest Contentful Paint) < 2.5秒
- FID (First Input Delay) < 100ms
- CLS (Cumulative Layout Shift) < 0.1

**最適化施策:**

- 画像の最適化（WebP、遅延読み込み）
- CSS/JSの圧縮・最小化
- ブラウザキャッシュの活用
- CDNの利用

**注:** 詳細なパフォーマンス最適化は `optimizing-performance` スキルを参照

#### モバイル対応

**要件:**

- レスポンシブデザイン（viewport設定）
- モバイルフレンドリーなフォントサイズ（16px以上）
- タップターゲットの適切なサイズ（48x48px以上）
- モバイルページ速度の最適化

#### セキュリティ

**HTTPS化:**

- SSL/TLS証明書の導入
- HTTPSへのリダイレクト設定
- Mixed Content（混在コンテンツ）の解消

### Step 6: コンテンツ戦略

#### E-E-A-T原則

**Experience（経験）:**

- 実体験に基づく情報
- オリジナルの画像・データ

**Expertise（専門性）:**

- 専門家による執筆・監修
- 著者プロフィールの明示

**Authoritativeness（権威性）:**

- 外部サイトからの引用・言及
- 業界認定・資格の表示

**Trustworthiness（信頼性）:**

- 正確な情報源の明示
- 定期的な情報更新
- プライバシーポリシー・利用規約の整備

#### コンテンツ更新戦略

**フレッシュネスシグナル:**

- 定期的な情報更新（最終更新日の表示）
- 古い情報の削除・修正
- 新しいセクションの追加

### Step 7: ローカルSEO（該当する場合）

#### Googleビジネスプロフィール

**最適化項目:**

- 正確なNAP情報（Name, Address, Phone）
- 営業時間の設定
- カテゴリの選択
- 写真の追加
- レビューへの返信

#### ローカル構造化データ

**LocalBusiness Schema:**

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "ビジネス名",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "住所",
    "addressLocality": "市区町村",
    "postalCode": "郵便番号",
    "addressCountry": "JP"
  },
  "telephone": "+81-XX-XXXX-XXXX",
  "openingHours": "Mo-Fr 09:00-18:00"
}
```

## 出力成果物

1. **キーワード戦略ドキュメント**: ターゲットキーワード、検索意図、優先度
2. **オンページSEOチェックリスト**: タイトル、メタ、見出し、本文の最適化状況
3. **構造化データ実装**: JSON-LD形式のスキーママークアップ
4. **内部リンクマップ**: サイト構造と推奨リンク配置
5. **テクニカルSEO監査レポート**: クローラビリティ、速度、モバイル対応の評価
6. **コンテンツ改善提案**: E-E-A-Tに基づく具体的な改善策

## ベストプラクティス

1. **ユーザー第一**: 検索エンジンより先にユーザー価値を優先
2. **自然な最適化**: キーワードの過度な詰め込みを避ける
3. **データドリブン**: Search Console、Analyticsのデータに基づく改善
4. **継続的改善**: SEOは一度きりではなく継続的なプロセス
5. **ホワイトハット**: Googleのガイドラインを遵守

## 関連スキル

- **creating-content**: SEO最適化されたコンテンツ作成との協働
- **optimizing-performance**: テクニカルSEO（速度改善）の詳細実装
- **analyzing-websites**: 競合サイトのSEO分析

## 参考リソース

- [Google検索セントラル](https://developers.google.com/search)
- [Schema.org](https://schema.org/)
- [Core Web Vitals](https://web.dev/vitals/)
