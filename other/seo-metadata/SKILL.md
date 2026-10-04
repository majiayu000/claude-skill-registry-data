---
name: seo-metadata
description: Next.js SEO 完整配置。涵盖 Metadata API、Open Graph、JSON-LD 结构化数据、Sitemap、Robots.txt。新建页面或 SEO 整改时加载。
trigger: 需要配置 SEO 元数据
input: 网站信息
output: SEO 配置代码
next: 无
dependencies: 无
---

# SEO Metadata 完整指南

## 一、Metadata 结构

### 每页必须做的事

```tsx
// 每个 page.tsx 顶部
import type { Metadata } from 'next'
import { getSiteConfig } from '@/lib/site'
import { generateSiteMetadata } from '@/lib/seo'   // 来自共享包

const site = getSiteConfig()

export const metadata: Metadata = generateSiteMetadata(site, {
  pageTitle: '页面标题 — 品牌名 (2026)',
  pageDescription: '描述文字 150-155 字符，含目标关键词。',
  canonicalPath: '/page-path',
  robots: { index: true, follow: true },
  // 追加关键词（非必须，但有助于长尾）
  keywords: [...(site.keywords || []), '额外长尾词1', '额外长尾词2'],
})
```

### Metadata 规则

| 项 | 规则 |
|---|---|
| **pageTitle** | 含品牌名 `MECCHA CHAMELEON`，不拼错。格式：`主题 — 子主题` （em dash，前后空格） |
| **pageDescription** | **150-155 字符**。一段完整的描述，含 2-3 个目标关键词。不要截断、不要清单 |
| **canonicalPath** | 必填。从 `/` 开始，如 `/platforms`。空字符串 `''` 表示首页 |
| **robots** | 内容页 `{ index: true, follow: true }`，法律页 `{ index: false, follow: false }` |
| **keywords** | 只在 `/platforms`、`/buy`、`/requirements` 等需要大量长尾词覆盖的页面追加 |

### 首页（根 page.tsx）

首页也需要单独的 `metadata` 导出——不要只依赖 layout.tsx 默认值。

```tsx
import { generateSiteMetadata } from '@/lib/seo'

const site = getSiteConfig()

export const metadata: Metadata = generateSiteMetadata(site, {
  pageTitle: 'Paint Yourself Invisible | Hide-and-Seek Party Game (2026)',
  pageDescription: 'MECCHA CHAMELEON is a creative hide-and-seek party game on Steam (PC). Paint to blend in. $5.99, Very Positive, 2-10 players. Tips, requirements, and guide.',
  canonicalPath: '',
  robots: { index: true, follow: true },
})
```

### 法律页面（privacy, tos, disclaimer）

**必须用 `generateSiteMetadata`**，不能手写原始 `Metadata` 对象。否则缺 canonical URL、OG、Twitter Card。

```tsx
import { getSiteConfig } from '@/lib/site'
import { generateSiteMetadata } from '@/lib/seo'

const site = getSiteConfig()

export const metadata: Metadata = generateSiteMetadata(site, {
  pageTitle: 'Privacy Policy',
  pageDescription: 'Privacy policy for MECCHA CHAMELEON guide. Data collection, cookies, and your rights.',
  canonicalPath: '/privacy',
  robots: { index: false, follow: false },
})
```

### layout.tsx 根配置

```tsx
export const metadata: Metadata = generateSiteMetadata(site, {
  pageTitle: 'Paint Yourself Invisible | Hide-and-Seek Party Game (2026)',
})
```

## 二、Title & Description 质量检查

### Title 格式

```
✅ MECCHA CHAMELEON Platforms — PS5, Mac, Mobile & PC Support (2026)
❌ MECCA CHAMELEON Platforms —PS5, Mac, Mobile & PC Support (2026)
❌ MECCHA CHAMELEON Platforms —PS5...   // em dash 后缺空格
```

**规则：**
- 品牌名拼写正确（MECCHA 不是 MECCA）
- em dash（`—`）前后各加一个空格
- 尾部加 `(2026)` 年号
- 长度 50-65 字符

### Description 长度

| 状态 | 字符数 |
|---|---|
| ✅ 理想 | 150-155 |
| ⚠️ 可接受 | 145-160 |
| ❌ 太长 | >165（Google 会截断） |
| ❌ 太短 | <100（浪费曝光机会） |

**裁剪技巧：**
```
原本: "MECCHA CHAMELEON tips and tricks —best camouflage techniques ranked S to B, Seeker search strategies, common beginner mistakes, and how to find hidden players. Master both roles with pro strategies."  (168 chars)
裁剪: "MECCHA CHAMELEON tips and tricks — ranked camouflage techniques S to B, Seeker strategies, beginner mistakes, and how to find hidden players. Master both roles."  (152 chars)
```

关键：删冗余副词、合并同类项、去掉不必要的修饰词。

## 三、JSON-LD 结构化数据

### 页面 -> Schema 对应表

| 页面类型 | JSON-LD Schema | 必须字段 |
|---------|---------------|---------|
| 首页 | `VideoGame` + `WebSite` | aggregateRating, offers, operatingSystem |
| 评测 | `Review` + `VideoGame` | reviewRating, itemReviewed, aggregateRating |
| FAQ | `FAQPage`（多条 Question/Answer） | 至少 5 个问答对 |
| 购买指南 | `Product` + `Offer` | offers.price, offers.availability |
| 平台/需求/模式 | `VideoGame` | aggregateRating, offers, operatingSystem |
| 所有内容页 | `BreadcrumbList` | 通过 `generateBreadcrumbJsonLd` 自动生成 |

### VideoGame JSON-LD 完整版

不要只写 `name` + `url` + `description`。**aggregateRating 和 offers 是最重要的**——它们触发搜索结果的星级评分和价格标签。

```tsx
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{
    __html: JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'VideoGame',
      name: data.name,
      url: 'https://meccha-chameleon.info/classes',
      description: '页面描述',
      operatingSystem: 'Windows 10/11 64-bit',
      applicationCategory: 'GameApplication',
      aggregateRating: {
        '@type': 'AggregateRating',
        ratingValue: data.rating,        // 4.3
        bestRating: data.ratingMax,       // 5
        ratingCount: data.ratingCount,    // 16348
      },
      offers: {
        '@type': 'Offer',
        price: '5.99',
        priceCurrency: 'USD',
        availability: 'https://schema.org/InStock',
        url: data.steamUrl,
      },
    }),
  }}
/>
```

### FAQPage JSON-LD

内容页是手风琴 `<details>`，JSON-LD 需要**所有问答对**：

```tsx
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{
    __html: JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      mainEntity: data.faqs.map((faq) => ({
        '@type': 'Question',
        name: faq.q,
        acceptedAnswer: {
          '@type': 'Answer',
          text: faq.a,    // 纯文本，不要含 HTML 标签
        },
      })),
    }),
  }}
/>
```

**注意：** `acceptedAnswer.text` 里不要含 `<a>` 标签或 HTML。Schema 解析器偏好纯文本。

## 四、Sitemap & Robots

### sitemap.ts

```tsx
export default function sitemap(): MetadataRoute.Sitemap {
  const site = getSiteConfig()
  const baseUrl = `https://${site.domain}`

  const mainPages = ['', '/guide', '/review', '/faq', '/classes', '/tier', '/items', '/platforms', '/buy', '/requirements']
  const legalPages = ['/privacy', '/tos', '/disclaimer']

  const entries: MetadataRoute.Sitemap = [
    ...mainPages.map(path => ({
      url: `${baseUrl}${path}`,
      changeFrequency: (path === '' ? 'weekly' : 'monthly') as 'weekly' | 'monthly',
      priority: path === '' ? 1.0 : 0.8,
    })),
    ...legalPages.map(path => ({
      url: `${baseUrl}${path}`,
      changeFrequency: 'monthly' as const,
      priority: 0.3,
    })),
  ]

  return entries
}
```

**原则：**
- 首页 priority 1.0，内容页 0.8，法律页 0.3
- `/jump`（跳转中间页）不加入 sitemap
- 新增页面时同步更新 `mainPages` 数组

### robots.ts

```tsx
export default function robots(): MetadataRoute.Robots {
  const site = getSiteConfig()
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: ['/jump', '/api/'],
    },
    sitemap: `https://${site.domain}/sitemap.xml`,
  }
}
```

## 五、内部链接网络

### 链接密度要求

| 页面类型 | 最低外链数（指向站内其他页） |
|---------|--------------------------|
| 首页 | 至少 5 个 |
| 指南类页面 | 至少 3 个（指向其他指南页） |
| 购买/平台/需求页 | 至少 3 个 |
| FAQ | 至少 6 个（涵盖所有内容页） |
| 法律页 | 1-2 个即可 |

### 指南页交叉链接模式

每个指南页（guide/classes/items/tier）在底部 CTA 前加导航栏：

```tsx
<section className="section" style={{ padding: '2rem 0' }}>
  <div className="container">
    <div style={{ maxWidth: '800px', margin: '0 auto' }} className="reveal">
      <p style={{ textAlign: 'center' }}>
        <strong>Related guides:</strong>{' '}
        <a href="/guide">Beginner's Guide</a> —
        <a href="/classes">Game Modes</a> —
        <a href="/items">Camouflage Guide</a>
      </p>
    </div>
  </div>
</section>
```

### FAQ 内链

在 FAQ 的 `a` 答案文本中嵌入指向对应详细页面的链接：

> "MECCHA CHAMELEON is currently available exclusively on PC via Steam. See our `<a href="/platforms">Platform Availability Guide</a>` for full breakdown."

## 六、关键词驱动的页面规划

### 从搜索数据找内容缺口

从 Google Search Console / 关键词工具导出的 CSV 中，提取：

1. **高搜索量 + 0 覆盖** → 需要新建页面
2. **高增长（↑%）+ 低覆盖** → 需要强化现有页面

示例优先级矩阵：

| 关键词 | 搜索量 | 增长 | 动作 |
|--------|--------|------|------|
| ps5, mac, mobile | 20+ | 20%+ | 新建 `/platforms` |
| steam key | 5+ | 30%+ | 新建 `/buy` |
| cloud save error | 1+ | 160%+ | 强化 `/requirements` |
| tips, how to play | 一致 | 稳定 | 已有覆盖 ✅ |

## 七、低优先级但值得做的事

| 项目 | 说明 |
|------|------|
| **OG 图片** | 每个页面用独立的 OG 图片（至少不同标题 overlay）。当前只有一张 `capsule.jpg` |
| **favicon** | 至少 `favicon.svg` + `apple-touch-icon.png`。考虑 PWA 的 `icon-192x192.png` |
| **字体数量** | 最多 3 个 Google Font 家族。5 个以上影响 LCP |
| **hreflang** | 如果支持多语言，在 `alternates` 中添加 hreflang 标签 |
| **WebP/AVIF** | 图片用 WebP 格式替代 JPEG，减小传输体积 |
