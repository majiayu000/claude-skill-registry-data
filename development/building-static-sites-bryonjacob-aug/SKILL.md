---
name: building-static-sites
description: Use when creating static websites with Next.js static export - covers YAML-based content, image optimization, form handling, SEO, and deployment to GitHub Pages/Netlify/Vercel
---

# Building Static Sites

## Overview

Static site generation with **Next.js** (`output: 'export'`) for marketing sites, documentation, portfolios, and blogs.

Extends `building-with-nextjs` for static export.

## When to Use

✅ **Good for:**
- Marketing websites
- Documentation sites
- Blogs and portfolios
- Landing pages
- No authentication needed

❌ **Not suitable for:**
- Real-time dashboards
- E-commerce with inventory
- User authentication
- API routes or server actions

## Configuration

**next.config.ts:**
```typescript
const nextConfig = {
  output: 'export',  // Enable static HTML export
  images: {
    unoptimized: true,  // Or use optimizer plugin
  },
}
```

**Build output:** `out/` directory with static HTML

## YAML-Based Content (Recommended)

**Structure:**
```
content/
├── global.yaml          # Site-wide content
├── features.yaml        # Reusable blocks
└── pages/
    ├── home.yaml
    ├── about.yaml
    └── contact.yaml
```

**Type-safe loading:**
```typescript
// lib/content-types.ts
export interface GlobalContent {
  site: { title: string; description: string; url: string }
  navigation: { links: Array<{ href: string; label: string }> }
}

// lib/content.ts
import fs from 'fs'
import path from 'path'
import yaml from 'js-yaml'

export function getGlobalContent(): GlobalContent {
  const filePath = path.join(process.cwd(), 'content', 'global.yaml')
  const content = fs.readFileSync(filePath, 'utf8')
  return yaml.load(content) as GlobalContent
}
```

**Example YAML:**
```yaml
# content/global.yaml
site:
  title: "My Company"
  description: "We build great things"

navigation:
  links:
    - href: "/"
      label: "Home"
    - href: "/about"
      label: "About"
```

**Usage:**
```typescript
// app/page.tsx
import { getHomeContent } from '@/lib/content'

export default function HomePage() {
  const content = getHomeContent()
  return <h1>{content.hero.headline}</h1>
}
```

**Dependencies:**
```bash
pnpm add js-yaml
pnpm add -D @types/js-yaml
```

## Image Optimization

**Option 1: Pre-optimize manually**
```bash
pnpm add -D sharp-cli
sharp resize 1920 --quality 85 --format webp public/images/*.{jpg,png}
```

**Option 2: Build-time optimization**
```bash
pnpm add -D next-image-export-optimizer
```

**Option 3: CDN-based (Recommended)**
- Use Cloudflare Images, imgix, or similar
- No build processing needed

## Form Handling

See `integrating-formspree-forms` skill for complete setup.

**Quick example:**
```typescript
'use client'
import { useForm } from '@formspree/react'

export default function ContactForm() {
  const [state, handleSubmit] = useForm("YOUR_FORM_ID")

  if (state.succeeded) {
    return <p>Thanks for your message!</p>
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" name="email" required />
      <textarea name="message" required />
      <button type="submit">Send</button>
    </form>
  )
}
```

## SEO

**Metadata configuration:**
```typescript
// app/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: { default: 'My Site', template: '%s | My Site' },
  description: 'Site description',
  openGraph: {
    title: 'My Site',
    description: 'Site description',
    images: [{ url: 'https://example.com/og-image.png' }],
  },
}
```

**Sitemap generation:**
```typescript
// app/sitemap.ts
import type { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: 'https://example.com',
      lastModified: new Date(),
      priority: 1,
    },
  ]
}
```

**robots.txt:**
```typescript
// app/robots.ts
export default function robots() {
  return {
    rules: { userAgent: '*', allow: '/' },
    sitemap: 'https://example.com/sitemap.xml',
  }
}
```

## Testing

**Content validation:**
```javascript
// scripts/validate-yaml.js
import fs from 'fs'
import yaml from 'js-yaml'

function validateYaml(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8')
    yaml.load(content)
    console.log(`✅ ${filePath}`)
  } catch (error) {
    console.error(`❌ ${filePath}: ${error.message}`)
    process.exit(1)
  }
}
```

**Build verification:**
```javascript
// scripts/verify-build.js
import fs from 'fs'
import path from 'path'

const requiredPages = ['index.html', 'about/index.html']

requiredPages.forEach(page => {
  const fullPath = path.join(process.cwd(), 'out', page)
  if (!fs.existsSync(fullPath)) {
    console.error(`❌ Missing: ${page}`)
    process.exit(1)
  }
})
console.log('✅ Build verification passed')
```

## Deployment

**GitHub Pages:**
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - run: pnpm install
      - run: pnpm build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./out
```

**Netlify:**
```toml
# netlify.toml
[build]
  command = "pnpm build"
  publish = "out"
```

**Vercel:**
Auto-detects Next.js, no config needed.

## justfile Commands

```just
build-static:
    pnpm build
    @echo "✅ Static site built to ./out"

validate-content:
    node scripts/validate-yaml.js

verify-build:
    node scripts/verify-build.js

check-all: format lint typecheck validate-content test coverage test-e2e a11y verify-build
    @echo "✅ All static site checks passed"
```

## Limitations & Workarounds

**No dynamic content:**
- ✅ Use client-side fetching for dynamic data
- ✅ Rebuild site periodically (scheduled CI)

**No API routes:**
- ✅ Use third-party services (Formspree, Supabase)

**Image optimization disabled:**
- ✅ Use CDN-based optimization
- ✅ Pre-optimize with sharp-cli
