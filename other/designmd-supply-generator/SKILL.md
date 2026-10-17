---
name: designmd-supply-generator
description: Generate DESIGN.md files from any website using Context.dev APIs for design tokens, brand data, and visual extraction
triggers:
  - generate a design system document from a website
  - create a DESIGN.md file for this domain
  - extract design tokens and brand identity from a URL
  - build a design system spec from a live site
  - scrape design guidelines from a website
  - turn this website into a design system document
  - generate design documentation for a domain
  - create design specs using Context.dev
---

# designmd-supply-generator

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## What It Does

`designmd-supply` is a Next.js application that transforms any website into a comprehensive `DESIGN.md` design system document. It orchestrates four Context.dev APIs (Styleguide, Brand, Screenshot, Markdown) and uses an LLM via Vercel AI Gateway to generate structured design documentation with YAML frontmatter covering colors, typography, layout, components, and brand guidelines.

The system caches all API responses and generated documents in Turso (libSQL) for fast subsequent access.

## Installation

```bash
git clone https://github.com/context-dot-dev/designmd-supply.git
cd designmd-supply
npm install
```

### Environment Setup

```bash
cp .env.example .env
```

Required variables in `.env`:

```bash
CONTEXT_DEV_API_KEY=your_context_dev_key
VERCEL_AI_GATEWAY_API_KEY=your_vercel_ai_key

# Optional: Turso cache (auto-injected on Vercel)
designmd_TURSO_DATABASE_URL=libsql://your-db.turso.io
designmd_TURSO_AUTH_TOKEN=your_turso_token
```

Get API keys:
- Context.dev: https://context.dev
- Vercel AI Gateway: https://vercel.com/ai-gateway
- Turso: https://turso.tech

### Development

```bash
npm run dev
# Open http://localhost:3000
```

## Core API Endpoints

### 1. Generate DESIGN.md

**POST** `/api/design-md`

```typescript
// Request body
{
  "domain": "stripe.com"
}

// Response
{
  "markdown": "---\ntitle: Stripe Design System\n...",
  "cached": false
}
```

### 2. Get Cached Design Doc

**GET** `/api/design-md?domain=stripe.com`

Returns cached `DESIGN.md` if available, otherwise triggers generation.

### 3. Fetch Brand Data

**GET** `/api/brand?domain=stripe.com`

Returns Context.dev Brand API response (cached):

```json
{
  "domain": "stripe.com",
  "name": "Stripe",
  "logo": "https://...",
  "colors": ["#635BFF", "#0A2540"],
  "industry": "Financial Technology"
}
```

### 4. Fetch Styleguide Tokens

**GET** `/api/styleguide?domain=stripe.com`

Returns design tokens (colors, typography, spacing, radii, components).

### 5. Get Screenshot

**GET** `/api/screenshot?domain=stripe.com`

Returns high-quality screenshot of homepage.

## Usage Patterns

### Basic: Generate Design Doc for a Domain

```typescript
import { generateDesignMd } from '@/lib/design-md';

async function createDesignDoc(domain: string) {
  const result = await fetch('/api/design-md', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ domain })
  });
  
  const { markdown } = await result.json();
  return markdown;
}

// Usage
const designDoc = await createDesignDoc('figma.com');
console.log(designDoc);
```

### Advanced: Use Context.dev APIs Directly

```typescript
import { createContextClient } from 'context.dev';

const contextClient = createContextClient({
  apiKey: process.env.CONTEXT_DEV_API_KEY!
});

// Extract styleguide tokens
async function getDesignTokens(domain: string) {
  const styleguide = await contextClient.web.extractStyleguide({
    url: `https://${domain}`
  });
  
  return {
    colors: styleguide.colors,
    typography: styleguide.typography,
    spacing: styleguide.spacing,
    borderRadius: styleguide.borderRadius
  };
}

// Get brand intelligence
async function getBrandData(domain: string) {
  const brand = await contextClient.brand.retrieve({
    domain
  });
  
  return {
    name: brand.name,
    logo: brand.logo,
    colors: brand.colors,
    slogan: brand.slogan,
    industry: brand.industry
  };
}
```

### Server-Side: Complete Pipeline

```typescript
import { createContextClient } from 'context.dev';
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

export async function generateDesignMdFull(domain: string) {
  const client = createContextClient({
    apiKey: process.env.CONTEXT_DEV_API_KEY!
  });
  
  // Parallel fetch all Context.dev data
  const [styleguide, brand, screenshot, markdown] = await Promise.all([
    client.web.extractStyleguide({ url: `https://${domain}` }),
    client.brand.retrieve({ domain }),
    client.web.screenshot({ 
      url: `https://${domain}`,
      width: 1920,
      height: 1080
    }),
    client.web.webScrapeMd({ url: `https://${domain}` })
  ]);
  
  // Compose prompt
  const prompt = `Generate a DESIGN.md for ${domain}.
  
Styleguide tokens:
${JSON.stringify(styleguide, null, 2)}

Brand data:
${JSON.stringify(brand, null, 2)}

Page content:
${markdown.content}

Create comprehensive design system documentation with sections:
- Overview
- Colors
- Typography
- Layout & Spacing
- Components
- Do's and Don'ts`;

  // Generate with LLM
  const { text } = await generateText({
    model: openai('gpt-4o'),
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { 
            type: 'image', 
            image: screenshot.base64,
            mimeType: 'image/png'
          }
        ]
      }
    ]
  });
  
  return text;
}
```

## Turso Caching Integration

### Cache Operations

```typescript
import { getCached, setCached, listDomains } from '@/lib/turso';

// Read from cache
const cached = await getCached('stripe.com', 'designmd');
if (cached) {
  return JSON.parse(cached);
}

// Write to cache
await setCached('stripe.com', 'styleguide', JSON.stringify(styleguideData));
await setCached('stripe.com', 'brand', JSON.stringify(brandData));
await setCached('stripe.com', 'designmd', generatedMarkdown);

// List all cached domains
const domains = await listDomains();
// Returns: ['stripe.com', 'figma.com', ...]
```

### Batch Read for Directory

```typescript
import { getCachedBatch } from '@/lib/turso';

async function buildDirectory(domains: string[]) {
  const kinds = ['brand', 'screenshot'];
  const batch = await getCachedBatch(domains, kinds);
  
  return domains.map(domain => ({
    domain,
    brand: batch[domain]?.brand ? JSON.parse(batch[domain].brand) : null,
    screenshot: batch[domain]?.screenshot || null
  }));
}
```

## Adding Domains to Directory

Edit `lib/domains.ts`:

```typescript
export const TOP_DOMAINS = [
  'stripe.com',
  'figma.com',
  'linear.app',
  'notion.so',
  'vercel.com',
  // Add your domain here
  'yoursite.com'
];
```

The cache populates on first visit. Pre-render at build:

```typescript
// app/guides/[domain]/page.tsx
export async function generateStaticParams() {
  const domains = await listDomains();
  return domains.map(domain => ({ domain }));
}
```

## Component: Design Doc Display

```typescript
'use client';

import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

export function DesignDocViewer({ domain }: { domain: string }) {
  const [markdown, setMarkdown] = useState('');
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    async function load() {
      const res = await fetch(`/api/design-md?domain=${domain}`);
      const data = await res.json();
      setMarkdown(data.markdown);
      setLoading(false);
    }
    load();
  }, [domain]);
  
  if (loading) return <div>Generating design system...</div>;
  
  return (
    <article className="prose prose-lg max-w-4xl">
      <ReactMarkdown>{markdown}</ReactMarkdown>
    </article>
  );
}
```

## Common Workflows

### 1. Generate and Download Design Doc

```typescript
async function downloadDesignMd(domain: string) {
  const res = await fetch('/api/design-md', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ domain })
  });
  
  const { markdown } = await res.json();
  
  const blob = new Blob([markdown], { type: 'text/markdown' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${domain}-DESIGN.md`;
  a.click();
}
```

### 2. Search and Preview

```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export function DomainSearch() {
  const [domain, setDomain] = useState('');
  const router = useRouter();
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const cleaned = domain.replace(/^https?:\/\//, '').split('/')[0];
    router.push(`/guides/${cleaned}`);
  };
  
  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={domain}
        onChange={(e) => setDomain(e.target.value)}
        placeholder="Enter domain (e.g., stripe.com)"
        className="flex-1 px-4 py-2 border rounded"
      />
      <button type="submit" className="px-6 py-2 bg-blue-600 text-white rounded">
        Generate
      </button>
    </form>
  );
}
```

### 3. Batch Generate for Multiple Domains

```typescript
async function batchGenerate(domains: string[]) {
  const results = await Promise.allSettled(
    domains.map(domain =>
      fetch('/api/design-md', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ domain })
      }).then(r => r.json())
    )
  );
  
  return results.map((result, i) => ({
    domain: domains[i],
    success: result.status === 'fulfilled',
    markdown: result.status === 'fulfilled' ? result.value.markdown : null
  }));
}
```

## Troubleshooting

### Issue: API Rate Limits

**Solution:** Context.dev APIs have rate limits. Cache aggressively and use batch operations:

```typescript
// Check cache first
const cached = await getCached(domain, 'styleguide');
if (cached) return JSON.parse(cached);

// Space out API calls
await new Promise(resolve => setTimeout(resolve, 1000));
const data = await contextClient.web.extractStyleguide({ url });
```

### Issue: LLM Generation Timeout

**Solution:** Increase timeout for Vercel AI SDK:

```typescript
const { text } = await generateText({
  model: openai('gpt-4o'),
  messages: [...],
  maxRetries: 3,
  abortSignal: AbortSignal.timeout(60000) // 60 seconds
});
```

### Issue: Missing Turso Environment Variables

**Symptom:** Cache writes fail silently.

**Solution:** Verify environment variables are set:

```typescript
if (!process.env.designmd_TURSO_DATABASE_URL) {
  console.warn('Turso not configured, cache disabled');
  return null; // Fallback to live API
}
```

### Issue: Screenshot Too Large

**Solution:** Compress or reduce dimensions:

```typescript
const screenshot = await client.web.screenshot({
  url: `https://${domain}`,
  width: 1280, // Reduce from 1920
  height: 720,  // Reduce from 1080
  format: 'jpeg', // Use JPEG instead of PNG
  quality: 80
});
```

### Issue: Domain Not Resolving

**Solution:** Validate and normalize domain input:

```typescript
function normalizeDomain(input: string): string {
  return input
    .replace(/^https?:\/\//, '')
    .replace(/^www\./, '')
    .split('/')[0]
    .toLowerCase()
    .trim();
}
```

## Build and Deploy

```bash
npm run build
npm run start
```

Deploy to Vercel:

```bash
vercel
```

Turso integration auto-configures on Vercel Marketplace. For other platforms, manually set `designmd_TURSO_DATABASE_URL` and `designmd_TURSO_AUTH_TOKEN`.

## Type Safety

```typescript
// lib/types.ts
export interface DesignMdResponse {
  markdown: string;
  cached: boolean;
  domain: string;
  generatedAt?: string;
}

export interface StyleguideData {
  colors: Array<{ name: string; value: string; usage?: string }>;
  typography: Array<{ name: string; fontFamily: string; fontSize: string }>;
  spacing: Record<string, string>;
  borderRadius: Record<string, string>;
  components: Array<{ name: string; description: string }>;
}

export interface BrandData {
  domain: string;
  name: string;
  logo?: string;
  backdrop?: string;
  colors: string[];
  slogan?: string;
  industry?: string;
}
```

## Performance Optimization

```typescript
// Use React.cache for request deduplication
import { cache } from 'react';

export const getCachedDesignMd = cache(async (domain: string) => {
  const cached = await getCached(domain, 'designmd');
  if (cached) return cached;
  
  const generated = await generateDesignMdFull(domain);
  await setCached(domain, 'designmd', generated);
  return generated;
});
```
