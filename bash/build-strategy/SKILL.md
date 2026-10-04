---
name: build-strategy
description: Detailed guide for ISR/SSG/SSR rendering strategies. Use when asked about "build strategy", "ISR", "SSG", "SSR", or when changing the deployment / rendering approach.
---

# Build Strategy Guide: ISR / SSG / SSR

This system supports 3 rendering strategies configured via `site.buildStrategy` in settings-storage.

## Configuration

- **Settings key**: `site` → `site.buildStrategy`: `"isr"` | `"ssg"` | `"ssr"`
- **Self-hosted**: `loadSettings('site')` (DB)
- **Serverless**: Cloud storage `_settings/site.json` (via Admin UI)
- **Build-time**: `scripts/prebuild-strategy.ts` auto-reads setting and sets `BUILD_STRATEGY` env var

## Comparison Table

| Item | ISR | SSG | SSR |
|------|-----|-----|-----|
| Build time | Short | Depends on article count | Short |
| First access | Slow (3-5s) | Fast (<50ms) | Medium (200-500ms) |
| Subsequent | Fast (<100ms) | Fast (<50ms) | Medium (200-500ms) |
| Content update | Auto (revalidate) | Requires rebuild | Immediate |
| Scalability | Excellent | Limited | Good |
| Recommended articles | 100+ | <100 | Any |
| External CDN | Not needed | Not needed | Recommended |

## 1. ISR (Incremental Static Regeneration) — Default

**Flow**: First access generates page → cached → subsequent requests served from cache.

```
User → Edge → Cache hit?
               ├─ Yes → Return cached (<100ms)
               └─ No → Render at origin (3-5s) → Cache → Return
```

### On-Demand Revalidation

Saving/deleting articles via Admin automatically clears the affected page cache:

```typescript
// app/baan-admin/api/storage/file/route.ts
revalidatePath(`/${locale}/posts/${articleId}`);
revalidatePath(`/${locale}`);  // Also update home page
```

### External Revalidation API

```bash
curl "https://example.com/api/revalidate?secret=YOUR_TOKEN&path=article-id&locale=ja"
```

Requires `REVALIDATE_TOKEN` environment variable.

---

## 2. SSG (Static Site Generation)

**Flow**: All pages pre-generated at build time → served as static files.

```
Build: Loop all articles → Generate HTML → Deploy to CDN
Access: User → CDN → Static HTML (<50ms)
```

Build time scales with article count (100 articles ≈ 10-15 min).

### generateStaticParams

```typescript
export async function generateStaticParams() {
    if (!isSSGMode()) return [];  // Only in SSG mode
    const posts = await getAllPosts(locale);
    return posts.map(post => ({ slug: post.id }));
}
```

---

## 3. SSR (Server-Side Rendering)

**Flow**: Every request renders fresh. No Next.js cache.

```
User → Server → Render (200-500ms) → Return
```

### Cache Disabling

```typescript
import { unstable_noStore as noStore } from "next/cache";

export default async function Post({ params }) {
    if (isSSRMode()) { noStore(); }
    // ...
}
```

### External CDN for Performance

SSR alone re-renders every request. Use Cloudflare/CloudFront for edge caching:

```
User → Cloudflare (edge cache) → Origin (SSR)
         ↓
  Cache HIT → Return immediately (<50ms)
  Cache MISS → Forward to origin → Cache → Return
```

**Cloudflare config**:
```
Cache-Control: s-maxage=3600, stale-while-revalidate=86400
```

**Cache purge on content update**:
```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/purge_cache" \
  -H "Authorization: Bearer {CF_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{"files":["https://example.com/ja/posts/article-id"]}'
```

---

## Strategy Selection Guide

```
Articles > 100?
├─ Yes → ISR (fast builds)
└─ No → Update frequency?
         ├─ Daily → ISR (auto-revalidation)
         ├─ Weekly → SSG (fastest delivery)
         └─ Realtime needed → SSR + external CDN
```

## Implementation Files

| File | Role |
|------|------|
| `scripts/prebuild-strategy.ts` | Reads setting, sets BUILD_STRATEGY env var |
| `lib/build-config.ts` | Strategy detection functions (isISRMode, isSSGMode, isSSRMode) |
| `lib/settings-storage.ts` | Settings read/write (both environments) |
| `app/api/revalidate/route.ts` | External revalidation API |
| `app/baan-admin/api/storage/file/route.ts` | Auto-revalidation on save |

## FAQ

**Q: ISR content not updating?**
A: Save via Admin (auto-clears cache). Direct storage edits require calling `/api/revalidate`.

**Q: SSG build too slow?**
A: Switch to ISR. SSG build time scales with article count.

**Q: SSR performance poor?**
A: Add external CDN (Cloudflare/CloudFront) for edge caching.
