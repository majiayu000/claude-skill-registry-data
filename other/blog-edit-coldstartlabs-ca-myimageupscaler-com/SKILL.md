---
name: blog-edit
description: Edit existing blog posts - update content, metadata, title, description, slug, categories, tags, and featured images. Use when asked to improve, update, fix, or enhance existing blog posts.
---

# Blog Post Editor for MyImageUpscaler

Edit existing blog posts to improve quality, SEO, or fix issues.

---

## Quick Reference

| Endpoint                                | Purpose            |
| --------------------------------------- | ------------------ |
| `GET /api/blog/posts`                   | List all posts     |
| `GET /api/blog/posts/[slug]`            | Get single post    |
| `PATCH /api/blog/posts/[slug]`          | Update post        |
| `DELETE /api/blog/posts/[slug]`         | Delete post        |
| `POST /api/blog/posts/[slug]/publish`   | Publish post       |
| `POST /api/blog/posts/[slug]/unpublish` | Unpublish to draft |
| `POST /api/blog/images/upload`          | Upload new image   |

**Authentication**: Use `x-api-key` header with `BLOG_API_KEY` from `.env.api`

---

## Changelog

**Before starting:** Read recent entries and SEO backlogs to understand what has already been done.

```bash
tail -60 .claude/skills/blog-changelog.md
sed -n '1,140p' docs/SEO/maintenance/seo-changes-backlog.md
sed -n '1,120p' docs/SEO/maintenance/gsc-request-indexing-backlog.md
```

If the target post was recently refreshed, redirected, unpublished, queued for indexing, or is waiting for GSC data lag, do not rewrite it again unless the user explicitly asks or `blog-performance-monitor` has produced an `edit-now` escalation with its action threshold met. Treat non-escalated recent-refresh tasks as validation-only or request-indexing follow-up.

**After finishing:** Append a brief entry.

```bash
cat >> .claude/skills/blog-changelog.md << 'EOF'

## YYYY-MM-DD

### [Type]: [Short title]
**Affected:** [slug(s)]
**Why:** [reasoning]
**Changes:**
- `slug` — what was done
EOF
```

---

## Workflow

```
1. CHANGELOG → Read recent blog changelog and SEO maintenance backlogs first
2. FETCH     → GET /api/blog/posts/[slug]
3. ANALYZE   → Review current content/SEO
4. IMPROVE   → Generate new content/image if needed
5. UPDATE    → PATCH /api/blog/posts/[slug]
6. VERIFY    → Check changes applied
7. CHANGELOG → Append entry with what changed and why
```

---

## Step 1: Fetch & Analyze Post

```bash
# Load environment
source scripts/load-env.sh
API_KEY=$(grep BLOG_API_KEY .env.api | cut -d'=' -f2)

# Get post with full details
curl -s http://localhost:3000/api/blog/posts/how-to-upscale-images \
  -H "x-api-key: $API_KEY" | jq '{
  title,
  description,
  status,
  titleLength: (.title | length),
  descriptionLength: (.description | length),
  category,
  tags
}'
```

---

## Step 2: Update Post

All fields are optional. Only include what you want to change.

```bash
# Update specific fields
curl -s -X PATCH http://localhost:3000/api/blog/posts/how-to-upscale-images \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "How to Upscale Images 4x: Complete Guide [2026]",
    "description": "Upscale images 4x quality instantly with AI. Free tool for photos, graphics, artwork. No quality loss."
  }' | jq '{title, updated_at}'
```

### Updatable Fields

| Field                | Type   | Notes                                      |
| -------------------- | ------ | ------------------------------------------ |
| `title`              | string | 5-200 chars                                |
| `slug`               | string | Lowercase with hyphens only                |
| `description`        | string | 20-500 chars                               |
| `content`            | string | Min 100 chars                              |
| `author`             | string | Default: "MyImageUpscaler Team"            |
| `category`           | string | Guides, Tips, Comparisons, News, Technical |
| `tags`               | array  | Array of tag strings                       |
| `featured_image_url` | string | AI-generated uploaded URL                  |
| `featured_image_alt` | string | Alt text for accessibility                 |
| `seo_title`          | string | Max 70 chars                               |
| `seo_description`    | string | Max 160 chars                              |

---

## Step 3: Update Featured Image

### Generate with AI (Recommended)

Use the AI image generation skill for unique, contextual images:

```bash
# Generate a blog-optimized featured image (1200x630)
yarn tsx .claude/skills/ai-image-generation/scripts/generate-ai-image.ts \
  "Modern laptop showing AI image upscaling interface, before and after comparison, professional setup, blue lighting, photorealistic" \
  ./new-featured.png \
  1200 630

# Upload to Supabase Storage
UPLOAD=$(curl -s -X POST http://localhost:3000/api/blog/images/upload \
  -H "x-api-key: $API_KEY" \
  -F "file=@./new-featured.png" \
  -F "alt_text=AI image upscaling before and after comparison")

IMAGE_URL=$(echo "$UPLOAD" | jq -r '.data.url')

# Update post with new URL
curl -s -X PATCH http://localhost:3000/api/blog/posts/[slug] \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"featured_image_url\": \"$IMAGE_URL\", \"featured_image_alt\": \"AI image upscaling before and after comparison\"}"
```

See `/ai-image-generation` skill for prompt templates and best practices.

### Upload Local Image

Images are automatically compressed to WebP format (max 1920x1080, 80% quality) before storage.

```bash
# Upload (auto-converts to WebP)
UPLOAD=$(curl -s -X POST http://localhost:3000/api/blog/images/upload \
  -H "x-api-key: $API_KEY" \
  -F "file=@./new-featured.jpg" \
  -F "alt_text=New featured image")

IMAGE_URL=$(echo "$UPLOAD" | jq -r '.data.url')

# Update post with new URL
curl -s -X PATCH http://localhost:3000/api/blog/posts/[slug] \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"featured_image_url\": \"$IMAGE_URL\"}"
```

**Storage details:**

- **Format:** WebP (auto-converted)
- **Max dimensions:** 1920x1080
- **Compression:** 80% quality
- **Cache:** 1 year CDN cache

---

## Step 4: Add/Update Inline Images

Posts should have 2-3 inline images in the markdown content. To add or update them:

```bash
# Generate new inline images
yarn tsx .claude/skills/ai-image-generation/scripts/generate-ai-image.ts \
  "Split screen: pixelated photo left, sharp enhanced photo right, dramatic comparison" \
  ./new-inline.png 800 600

# Upload to storage
INLINE_URL=$(curl -s -X POST http://localhost:3000/api/blog/images/upload \
  -H "x-api-key: $API_KEY" \
  -F "file=@./new-inline.png" \
  -F "alt_text=Before and after comparison" | jq -r '.data.url')

echo "Use this in content: ![Before and after comparison]($INLINE_URL)"
```

Then update the content with the new image markdown (see Step 5).

---

## Step 5: Update Content

For large content updates, write to file first. Include inline images in markdown:

```bash
cat > /tmp/content-update.json << 'EOF'
{
  "content": "# Updated H1 Title\n\nNew intro with primary keyword...\n\n## Section 1\n\nImproved content with more details...\n\n![Inline image 1 description](https://your-supabase-url/inline-1.webp)\n\n## Section 2\n\nMore comprehensive content...\n\n![Inline image 2 description](https://your-supabase-url/inline-2.webp)\n\n## Conclusion\n\nSummary and [CTA](https://myimageupscaler.com)."
}
EOF

curl -s -X PATCH http://localhost:3000/api/blog/posts/[slug] \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/content-update.json | jq '{title, updated_at}'
```

**Inline Image Rules:**

- Place 2-3 images evenly throughout content
- Place after the section they illustrate
- Use descriptive alt text for SEO

---

## SEO Improvement Checklist

### Title Optimization

- [ ] 50-70 chars (optimal range)
- [ ] Keyword in first 5 words
- [ ] Has numbers: `5 Ways`, `7 Methods`
- [ ] Has brackets: `[2026]`, `[Guide]`, `[Free]`

### Description Optimization

- [ ] 150-160 chars (optimal range)
- [ ] Contains primary keyword
- [ ] Ends with CTA: "Try free now", "Learn more"

### CTA (Call-to-Action) Requirements

**CRITICAL**: Every blog post MUST have hyperlinked CTAs.

**Required CTA Placements:**

- [ ] **Primary CTA in conclusion**
- [ ] **1-2 contextual CTAs** within content body
- [ ] **Description CTA** - Meta description ends with action

**CTA Templates:**

```markdown
<!-- Primary Conclusion CTA -->

[Start upscaling your images now](https://myimageupscaler.com) - free, no signup.

<!-- Contextual CTA -->

[Try our AI upscaler](https://myimageupscaler.com) and see the difference.

<!-- Benefit-focused -->

[Upload your photo](https://myimageupscaler.com) - 4x enhancement in seconds.

<!-- Quality CTA -->

Professional results with our [free image upscaler](https://myimageupscaler.com).
```

**Best Practices:**

- ✅ Use markdown links: `[text](https://myimageupscaler.com)`
- ✅ Place after explaining value
- ✅ Action-oriented: "Start upscaling", "Upload your photo"
- ✅ Emphasize free
- ❌ No plain text CTAs
- ❌ No arrow-only CTAs: "Try free →"

### Content Quality

- [ ] 1000+ words for competitive keywords
- [ ] Exactly 1 H1 heading
- [ ] 4+ H2 sections
- [ ] 1 featured image (1200x630)
- [ ] 2-3 inline images (800x600) in markdown content
- [ ] 3-5 internal links to other blog posts
- [ ] CTA links to homepage

### Slug Optimization

- [ ] 3-5 words
- [ ] Contains primary keyword
- [ ] Lowercase with hyphens only

---

## Publishing Workflow

### Draft → Published

```bash
curl -s -X POST http://localhost:3000/api/blog/posts/[slug]/publish \
  -H "x-api-key: $API_KEY" | jq '{status, published_at}'
```

### Published → Draft (Unpublish)

```bash
curl -s -X POST http://localhost:3000/api/blog/posts/[slug]/unpublish \
  -H "x-api-key: $API_KEY" | jq '{status, published_at}'
```

### Delete Post

```bash
curl -s -X DELETE http://localhost:3000/api/blog/posts/[slug] \
  -H "x-api-key: $API_KEY"
```

---

## Categories & Tags

**Categories:** `Guides`, `Tips`, `Comparisons`, `News`, `Technical`

**Tags:** `upscale`, `AI`, `tutorial`, `photo`, `image`, `enhancement`, `resolution`, `prints`, `social-media`, `graphics`, `artwork`, `logo`, `product-photos`, `ecommerce`, `restoration`, `batch`, `free`, `online`

---

## Humanizing Content

### AI Patterns to AVOID

| Category            | Words to Avoid                                 |
| ------------------- | ---------------------------------------------- |
| **Overused**        | delve, tapestry, nuanced, landscape, testament |
| **Corporate**       | leverage, facilitate, streamline, utilize      |
| **Filler**          | "It's important to note", "worth noting"       |
| **Hype**            | groundbreaking, revolutionary, game-changing   |
| **Throat-clearing** | "In today's world", "Here's the thing"         |

### Human Writing Techniques

```markdown
❌ AI: "Image upscaling represents a significant advancement in AI technology."
✅ Human: "I've tested dozens of upscalers. Most make your photos look like plastic."

❌ AI: "This solution offers numerous benefits."
✅ Human: "Here's what makes this different: it actually preserves details."

❌ AI: "The process facilitates enhanced quality."
✅ Human: "Your photos get sharper. Period."
```

**Writing Rules:**

- First sentence delivers value immediately
- Use active voice
- Keep paragraphs short (2-4 sentences)
- Mix sentence lengths
- Use first-person occasionally

---

## Verify Changes

```bash
# API check
curl -s http://localhost:3000/api/blog/posts/[slug] \
  -H "x-api-key: $API_KEY" | jq '{title, updated_at, status}'

# Frontend check
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/blog/[slug]
```

---

## Common Operations

### List All Posts

```bash
curl -s "http://localhost:3000/api/blog/posts?status=published&limit=50" \
  -H "x-api-key: $API_KEY" | jq '.data[] | {slug, title, status}'
```

### Bulk Update Categories

```bash
# Get all posts with old category
curl -s "http://localhost:3000/api/blog/posts?category=OldCategory" \
  -H "x-api-key: $API_KEY" | jq '.data[].slug' | while read slug; do
  # Update each post
  curl -s -X PATCH "http://localhost:3000/api/blog/posts/$slug" \
    -H "x-api-key: $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"category": "NewCategory"}'
done
```

### Republish Post (triggers updated_at)

```bash
# Unpublish first
curl -s -X POST http://localhost:3000/api/blog/posts/[slug]/unpublish \
  -H "x-api-key: $API_KEY"

# Then publish
curl -s -X POST http://localhost:3000/api/blog/posts/[slug]/publish \
  -H "x-api-key: $API_KEY"
```

---

## Environment Configuration

```bash
# Load environment
source scripts/load-env.sh
API_KEY=$(grep BLOG_API_KEY .env.api | cut -d'=' -f2)
```

---

## Troubleshooting

### Post not found (404)

- Check slug is correct (lowercase, hyphens only)
- For unpublished posts, use API endpoint not frontend URL

### Update not applying

- Check `updated_at` timestamp changed
- Verify JSON is valid
- Check `x-api-key` header is correct

### Publish/Unpublish Not Working

- Post must exist first
- Check status before and after operation
- `published_at` is set/unset accordingly

---

## Related Skills

- `/ai-image-generation` - Generate featured and inline images with AI
- `/blog-publish` - Create new blog posts from scratch
