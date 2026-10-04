---
name: content-management
description: Guide for the content management pipeline — path resolution, taxonomy, static pages, and search indexing. Use when asked about "taxonomy", "categories", "tags", "search index", "static pages", or when modifying the content pipeline.
---

# Content Management Pipeline

## Overview

```
Admin Editor → Storage API (storagePutFile)
  ↓
Storage (GCS / S3 / R2 / Local)
  ↓ lib/path-resolver.ts (path resolution)
  ↓ lib/posts.ts (article retrieval)
  ↓ lib/taxonomy.ts (category / tag registration)
Browser
  ↓
Search Index (Orama + CJK tokenizer)
```

## 1. Path Resolution (`lib/path-resolver.ts`)

Content paths change based on `siteSettings.language.multiLanguage`:

**Single language** (`multiLanguage: false`):
```
storage/article-id/index.en.md   # always index.{locale}.md — bare index.md is not read
```

**Multilingual** (`multiLanguage: true`):
```
storage/article-id/index.ja.md
storage/article-id/index.en.md
```

**Key functions:**
- `getContentPath(locale, slug)` → full path to markdown file (`index.{locale}.md`)
- `getContentPathWithFallback(locale, slug)` → returns `['article-id/index.{locale}.md']` (no index.md fallback despite doc comment)
- `getImagePath(articleId, imageName)` → `{articleId}/images/{imageName}`
- `extractLocaleFromFileName(fileName)` → `'ja'` from `'index.ja.md'`, `null` from `'index.md'`
- `parseArticleFilePath(filePath)` → `{ articleId, locale, fileName }`

## 3. Taxonomy (`lib/taxonomy.ts`)

Categories and tags have **dual storage**: DB (master list) + article frontmatter (per-article copy).

**Registration:**
```typescript
import { registerTaxonomyValues } from '@/lib/taxonomy';

// Called after article save/import
await registerTaxonomyValues(categories, tags);
```

- **Idempotent**: Skips DB write if nothing new
- Uses Set for deduplication, auto-sorts alphabetically
- Trims whitespace, filters empty strings

**Frontmatter parsing** (`parseFrontmatterTaxonomy`):

Supports multiple YAML formats:
```yaml
# Inline
category: "Tech"
tags: ["React", "Next.js"]

# YAML list
categories:
  - Tech
  - Web
tags:
  - React
  - Next.js
```

## 4. Static Pages (`lib/pages-storage.ts`, `lib/pages.ts`)

**Independent from blog articles.** Manages About, Contact, Terms, Privacy etc.

**Storage:**
```
content-pages/
├── about.md
├── contact.md
├── terms.md
└── privacy.md
```

**Environment handling:**
| Environment | Read from | Write to |
|-------------|-----------|----------|
| Self-hosted | Local `content-pages/` | Local `content-pages/` |
| Serverless | Cloud storage `content-pages/` | Cloud storage `content-pages/` |

**Key functions:**
- `readPage(slug)` / `writePage(slug, content)` / `deletePage(slug)`
- `pageExists(slug)` / `listPageSlugs()`
- `syncLocalToCloudStorage()` — Serverless build step (auto-runs)

**Page config** (via `loadSettings('pages')`):
```typescript
interface PagesConfig {
    homepage: { type: 'posts' | 'page'; slug?: string };
    pages: PageData[];
    navigation: { header: NavigationItem[]; footer?: NavigationItem[] };
}
```

**System pages** (cannot be deleted): `posts`, `home`, `terms`, `privacy`

## 5. Search Indexing

**Engine:** Orama (locale-specific indexes)

**Build-time generation:** `scripts/generate-search-index.ts`
- Generates per-locale index files
- CJK languages (ja, zh, ko) use **n-gram tokenizer** (bigram + trigram)
- Non-CJK languages use space-splitting
- Output: `public/search-index/{locale}.json`

**Index fields:** title, excerpt, category, tags, tokens

## 6. Frontmatter Required Fields

```yaml
---
title: "Article Title"    # Required
date: "2025-01-15"        # Required (ISO format)
category: "Tech"          # Required
id: "article-id"          # Required (matches directory name)
tags: ["Next.js"]         # Required
---
```

## Key Conventions

- **Storage abstraction**: Always use `storageGetFile`/`storagePutFile`, never direct `fs`
- **Path resolution**: Always use `lib/path-resolver.ts`, never hardcode paths
- **Taxonomy sync**: Call `registerTaxonomyValues()` after any article save/import
- **Search index**: Rebuild after content changes (`scripts/generate-search-index.ts`)
- **Serverless pages**: Cloud storage is the source of truth, not git-pushed `content-pages/`
