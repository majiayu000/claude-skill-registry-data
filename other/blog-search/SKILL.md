---
name: blog-search
description: Search and browse blog posts by keyword, slug, status, category, or tags. Use when asked to find, list, or look up existing blog posts.
---

# Blog Search for MyImageUpscaler

Search and browse existing blog posts without modifying anything.

---

## Quick Reference

| Endpoint           | Purpose              |
| ------------------ | -------------------- |
| `GET /api/blog/posts`        | List / search posts  |
| `GET /api/blog/posts/[slug]` | Get single post      |

**Authentication**: Use `x-api-key` header with `BLOG_API_KEY` from `.env.api`

---

## Environment Setup

```bash
source scripts/load-env.sh
API_KEY=$(grep BLOG_API_KEY .env.api | cut -d'=' -f2)
```

---

## Search Operations

### List All Published Posts

```bash
curl -s "http://localhost:3000/api/blog/posts?status=published&limit=50" \
  -H "x-api-key: $API_KEY" | jq '.data[] | {slug, title, status, category}'
```

### List All Drafts

```bash
curl -s "http://localhost:3000/api/blog/posts?status=draft&limit=50" \
  -H "x-api-key: $API_KEY" | jq '.data[] | {slug, title, status}'
```

### List All Posts (Any Status)

```bash
curl -s "http://localhost:3000/api/blog/posts?limit=100" \
  -H "x-api-key: $API_KEY" | jq '.data[] | {slug, title, status, category}'
```

### Get Single Post by Slug

```bash
curl -s "http://localhost:3000/api/blog/posts/[slug]" \
  -H "x-api-key: $API_KEY" | jq '{title, slug, status, category, tags, description, published_at, updated_at}'
```

### Get Full Post Content

```bash
curl -s "http://localhost:3000/api/blog/posts/[slug]" \
  -H "x-api-key: $API_KEY" | jq '{title, slug, content}'
```

### Filter by Category

```bash
curl -s "http://localhost:3000/api/blog/posts?category=Guides&limit=50" \
  -H "x-api-key: $API_KEY" | jq '.data[] | {slug, title, category}'
```

**Categories:** `Guides`, `Tips`, `Comparisons`, `News`, `Technical`

### Count Posts by Status

```bash
curl -s "http://localhost:3000/api/blog/posts?limit=100" \
  -H "x-api-key: $API_KEY" | jq '{
    total: (.data | length),
    published: ([.data[] | select(.status == "published")] | length),
    draft: ([.data[] | select(.status == "draft")] | length)
  }'
```

### Count Posts by Category

```bash
curl -s "http://localhost:3000/api/blog/posts?status=published&limit=100" \
  -H "x-api-key: $API_KEY" | jq '[.data[].category] | group_by(.) | map({category: .[0], count: length})'
```

### Search by Keyword in Title

```bash
KEYWORD="upscale"
curl -s "http://localhost:3000/api/blog/posts?limit=100" \
  -H "x-api-key: $API_KEY" | jq --arg k "$KEYWORD" '[.data[] | select(.title | ascii_downcase | contains($k | ascii_downcase))] | .[] | {slug, title}'
```

### Get SEO Metadata for a Post

```bash
curl -s "http://localhost:3000/api/blog/posts/[slug]" \
  -H "x-api-key: $API_KEY" | jq '{
    title, seo_title, description, seo_description,
    titleLength: (.title | length),
    descriptionLength: (.description | length),
    seoTitleLength: ((.seo_title // "") | length),
    seoDescriptionLength: ((.seo_description // "") | length)
  }'
```

### List Recent Posts (Sorted by Date)

```bash
curl -s "http://localhost:3000/api/blog/posts?status=published&limit=10" \
  -H "x-api-key: $API_KEY" | jq '[.data[] | {slug, title, published_at}] | sort_by(.published_at) | reverse'
```

### List Posts with Tags

```bash
curl -s "http://localhost:3000/api/blog/posts?limit=100" \
  -H "x-api-key: $API_KEY" | jq '.data[] | {slug, title, tags}'
```

### Search by Tag

```bash
TAG="AI"
curl -s "http://localhost:3000/api/blog/posts?limit=100" \
  -H "x-api-key: $API_KEY" | jq --arg t "$TAG" '[.data[] | select(.tags | any(. == $t))] | .[] | {slug, title, tags}'
```

---

## Troubleshooting

### Post not found (404)

- Check slug is correct (lowercase, hyphens only)
- Post may be deleted — try listing all posts first

### Empty results

- Check API key is loaded: `echo $API_KEY`
- Check dev server is running: `curl -s http://localhost:3000/api/health`

---

## Related Skills

- `/blog-edit` - Edit existing blog posts
- `/blog-publish` - Create new blog posts
