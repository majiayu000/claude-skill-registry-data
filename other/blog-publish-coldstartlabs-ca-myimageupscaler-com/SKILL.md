---
name: blog-publish
description: Create and publish SEO-optimized blog posts about image upscaling, AI enhancement, and photo editing. Use when asked to write blog posts, publish content, or create SEO content.
---

# Blog Publishing for MyImageUpscaler

Create SEO-optimized blog posts about image upscaling, AI photo enhancement, and related topics.

---

## Quick Reference

| Endpoint                              | Purpose                |
| ------------------------------------- | ---------------------- |
| `GET /api/blog/images`                | Search existing images |
| `POST /api/blog/posts`                | Create draft post      |
| `POST /api/blog/posts/[slug]/publish` | Publish post           |
| `POST /api/blog/images/upload`        | Upload featured image  |
| `GET /api/blog/posts`                 | List posts             |

**Authentication**: Use `x-api-key` header with `BLOG_API_KEY` from `.env.api`

---

## Changelog

**Before starting:** Read recent entries to avoid repeating work or conflicting with recent changes.

```bash
tail -60 .claude/skills/blog-changelog.md
```

**After publishing:** Append a brief entry.

```bash
cat >> .claude/skills/blog-changelog.md << 'EOF'

## YYYY-MM-DD

### Publish: [slug]
**Why:** [keyword opportunity / user intent]
**Changes:**
- Published `slug` — [topic summary, target keyword]
EOF
```

---

## Workflow

```
0. CHANGELOG       → Read recent entries first
1. ROADMAP CHECK   → Read keyword-strategy-roadmap-*.md for prioritized topics
2. TRACKING        → Check topics-covered.md to avoid duplication
3. SELECT TOPIC    → Choose from roadmap Segment A/B (highest priority)
4. SEARCH IMAGES   → GET /api/blog/images (check for reusable images first)
5. GENERATE IMAGES → Generate ONLY if no suitable images found (1 featured + 2-3 inline)
6. UPLOAD IMAGES   → POST /api/blog/images/upload (with metadata: tags, description, prompt)
7. CREATE POST     → POST /api/blog/posts (include inline image URLs in markdown content)
8. INTERNAL LINKS  → Scan pSEO sitemaps for relevant pages; embed 2-3 contextual links in content
9. UPDATE          → PATCH /api/blog/posts/[slug] (add featured image URL + updated content)
10. PUBLISH        → POST /api/blog/posts/[slug]/publish
11. VERIFY         → Check at /blog/[slug]
12. TRACK          → Update topics-covered.md with completed topic
13. CHANGELOG      → Append entry with slug, topic, and reasoning
```

**IMPORTANT Changes:**

- ✅ **Always check roadmap first** - pre-analyzed keyword opportunities
- ✅ **Track topics covered** - prevent keyword cannibalization
- ✅ **Update tracking after publish** - keep checklist current

---

## Step -1: Research Keywords & Content Roadmap

### Check Long-Tail Keyword Roadmap FIRST

**CRITICAL**: Before researching keywords manually, read the long-tail keyword roadmap. This contains pre-analyzed keywords that our DR 18 can realistically rank for.

```bash
# Read the long-tail keyword roadmap
ROADMAP="docs/SEO/long-tail-keyword-roadmap.md"

if [ -f "$ROADMAP" ]; then
  echo "✅ Found long-tail keyword roadmap: $ROADMAP"

  # Show priority topics
  echo "=== PRIORITY 1: Platform-Specific (Immediate) ==="
  grep -A 10 "## Priority 1: Platform-Specific" "$ROADMAP" | head -15

  echo "=== PRIORITY 2: Format-Specific (Immediate) ==="
  grep -A 10 "## Priority 2: Format-Specific" "$ROADMAP" | head -15

  echo "=== PRIORITY 3: Use-Case Specific (This Month) ==="
  grep -A 10 "## Priority 3: Use-Case Specific" "$ROADMAP" | head -15

  echo "=== ALREADY COVERED (Don't Duplicate) ==="
  grep -A 30 "## Topics Already Covered" "$ROADMAP" | head -35
else
  echo "⚠️  No keyword roadmap found at $ROADMAP"
  echo "Please ensure the file exists before proceeding."
  exit 1
fi
```

### Keyword Priority Tiers (DR 18 Optimized)

**IMPORTANT**: We have DR 18 with 75 referring domains. We CANNOT rank for high-volume head terms (500K+ searches). Focus on:

| Tier           | Volume Range | Competition | Can We Rank?                | Priority  |
| -------------- | ------------ | ----------- | --------------------------- | --------- |
| **Long-tail**  | 300-2,000    | Low         | **YES** (DR 15-25 needed)   | **P1**    |
| **Mid-tail**   | 2,000-10,000 | Low-Med     | **MAYBE** (DR 25-35 needed) | **P2**    |
| **Head terms** | 50,000+      | High        | **NO** (DR 50+ needed)      | **AVOID** |

### Keyword Selection Rules

1. **DO target:**
   - Platform-specific: "midjourney upscaler", "stable diffusion upscaler"
   - Format-specific: "upscale heic", "upscale tiff", "avif upscale"
   - Use-case-specific: "youtube thumbnail upscaler", "etsy image upscaler"
   - Scale-specific: "upscale 8x", "upscale to 8k"
   - Question-based: "how to upscale without losing quality"

2. **DON'T target (yet):**
   - "image upscaler" (500K, DR 50+ needed)
   - "ai image enhancer" (500K, DR 50+ needed)
   - "photo quality enhancer" (500K, DR 50+ needed)
   - Any keyword with 50K+ volume until we reach DR 35+

### Track What's Been Written (Prevent Duplication)

```bash
# Create content tracking directory
mkdir -p docs/SEO/blog-content-tracking

# Create tracking file if it doesn't exist
if [ ! -f "docs/SEO/blog-content-tracking/topics-covered.md" ]; then
  cat > docs/SEO/blog-content-tracking/topics-covered.md << 'EOF'
# Blog Content Tracking - MyImageUpscaler

**Last Updated**: $(date +%Y-%m-%d)

## Topics Covered (Blog Posts Published)

| Date | Keyword/Topic | Blog Slug | Roadmap Segment | Status |
|------|---------------|-----------|-----------------|--------|
| YYYY-MM-DD | Example keyword | example-slug | Segment A | ✅ Published |

## Topics In Progress

| Started | Keyword/Topic | Target Slug | Roadmap Segment | Assignee |
|---------|---------------|-------------|-----------------|----------|
| YYYY-MM-DD | Example keyword | example-slug | Segment B | Claude |

## Topics Planned (From Roadmap)

| Priority | Keyword/Topic | Search Vol | Competition | Roadmap Segment | Est. Impact |
|----------|---------------|------------|-------------|-----------------|-------------|
| P1 | ... | 500 | Low | Segment A | +50 clicks/mo |
EOF
fi

# Display tracking status
cat docs/SEO/blog-content-tracking/topics-covered.md

# Check for conflicts
echo "=== DUPLICATION CHECK ==="
read -p "Enter your target keyword: " TARGET_KEYWORD
grep -i "$TARGET_KEYWORD" docs/SEO/blog-content-tracking/topics-covered.md && \
  echo "⚠️  WARNING: Similar topic may already be covered!" || \
  echo "✅ No conflicts found - safe to proceed"
```

### Select Topic from Roadmap

**Decision Matrix:**

| Source                            | Priority | When to Use                                    |
| --------------------------------- | -------- | ---------------------------------------------- |
| **Priority 1: Platform-Specific** | P1       | Platform upscaler pages need blog support      |
| **Priority 2: Format-Specific**   | P1       | Format pages (HEIC, TIFF, WebP) need content   |
| **Priority 3: Use-Case Specific** | P1       | Use case pages (logo, real estate, NFT)        |
| **Priority 4: Scale-Specific**    | P2       | Scale pages (8x, 16x, 4x sweet spot)           |
| **Priority 5: Free + Long-Tail**  | P2       | Free modifier keywords                         |
| **Priority 6: Question-Based**    | P2       | Featured snippet opportunities                 |
| **Priority 7: Comparison**        | P3       | Alternative/comparison posts                   |
| **Topics Already Covered**        | AVOID    | Check topics-covered.md to prevent duplication |

### Topic Selection Workflow

1. **Read** `docs/SEO/long-tail-keyword-roadmap.md`
2. **Check** `docs/SEO/blog-content-tracking/topics-covered.md` for duplicates
3. **Select** highest priority keyword NOT yet covered
4. **Verify** volume is 300-5,000 (our DR 18 range)
5. **Confirm** competition is "Low"
6. **Proceed** with blog post creation

---

## Step 0: Search Existing Images (ALWAYS FIRST)

**CRITICAL**: Before generating any new images, search for existing reusable images. This saves ~$0.05-0.12 and ~60-120s per image.

### Tag Vocabulary Reference

Use these standardized tags when searching and uploading. Each image should have 3-6 tags.

| Category          | Tags                                                                                                                                                        |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Theme**         | `before-after`, `ai-processing`, `workflow`, `print-result`, `comparison`, `workspace`, `tutorial`, `ecommerce`, `social-media`, `restoration`, `upscaling` |
| **Subject**       | `laptop`, `phone`, `printer`, `photo`, `screenshot`, `artwork`, `product-photo`, `infographic`, `diagram`                                                   |
| **Style**         | `photorealistic`, `clean`, `professional`, `split-screen`, `side-by-side`, `step-by-step`                                                                   |
| **Blog Category** | `guides`, `tips`, `comparisons`, `news`, `technical`                                                                                                        |
| **Image Type**    | `featured`, `inline`                                                                                                                                        |

### Search Commands

```bash
# Load environment
source scripts/load-env.sh
API_KEY=$(grep BLOG_API_KEY .env.api | cut -d'=' -f2)

# Search for featured images with before-after comparison theme
curl -s "http://localhost:3000/api/blog/images?tags=before-after,upscaling&image_type=featured&limit=5" \
  -H "x-api-key: $API_KEY" | jq '.data[] | {url, alt_text, tags, prompt}'

# Search for inline images showing AI processing
curl -s "http://localhost:3000/api/blog/images?tags=ai-processing,workflow&image_type=inline&limit=5" \
  -H "x-api-key: $API_KEY" | jq '.data[] | {url, alt_text, tags, prompt}'

# Search for print-related images
curl -s "http://localhost:3000/api/blog/images?tags=print-result,printer&limit=5" \
  -H "x-api-key: $API_KEY" | jq '.data[] | {url, alt_text, tags, prompt}'

# Search for ecommerce/product images
curl -s "http://localhost:3000/api/blog/images?tags=ecommerce,product-photo&limit=5" \
  -H "x-api-key: $API_KEY" | jq '.data[] | {url, alt_text, tags, prompt}'

# Browse all available images
curl -s "http://localhost:3000/api/blog/images?limit=20" \
  -H "x-api-key: $API_KEY" | jq '.data[] | {url, alt_text, tags, image_type}'
```

### Decision Logic

**When to reuse:**

- Image matches 2+ of your desired tags
- Image theme matches your post topic (e.g., `before-after` for comparison posts)
- Image type matches need (featured vs inline)

**When to generate new:**

- No images match your tags
- Existing images don't fit the specific context
- You need a unique visual for the post

### Example: Search-First Workflow

```bash
# 1. Search for a featured image for an upscaling guide
FEATURED_SEARCH=$(curl -s "http://localhost:3000/api/blog/images?tags=before-after,upscaling&image_type=featured&limit=3" \
  -H "x-api-key: $API_KEY")
FEATURED_COUNT=$(echo "$FEATURED_SEARCH" | jq '.data | length')

if [ "$FEATURED_COUNT" -gt 0 ]; then
  # Reuse the first matching image
  FEATURED_URL=$(echo "$FEATURED_SEARCH" | jq -r '.data[0].url')
  echo "Reusing existing featured image: $FEATURED_URL"
else
  echo "No suitable featured image found, will generate new one"
  # Continue to Step 1 to generate
fi

# 2. Search for inline images
INLINE_SEARCH=$(curl -s "http://localhost:3000/api/blog/images?tags=ai-processing,comparison&image_type=inline&limit=5" \
  -H "x-api-key: $API_KEY")
INLINE_COUNT=$(echo "$INLINE_SEARCH" | jq '.data | length')

if [ "$INLINE_COUNT" -ge 2 ]; then
  # Reuse existing inline images
  INLINE1_URL=$(echo "$INLINE_SEARCH" | jq -r '.data[0].url')
  INLINE2_URL=$(echo "$INLINE_SEARCH" | jq -r '.data[1].url')
  echo "Reusing inline images: $INLINE1_URL, $INLINE2_URL"
else
  echo "Not enough inline images found, will generate new ones"
  # Continue to Step 1 to generate
fi
```

---

## Step 1: Generate All Images with AI (ONLY IF NO SUITABLE MATCHES)

**CRITICAL**: Every blog post needs **1 featured image + 2-3 inline images** embedded in the markdown content.

```bash
# Load environment
source scripts/load-env.sh
API_KEY=$(grep BLOG_API_KEY .env.api | cut -d'=' -f2)

# Generate featured image (1200x630 - social sharing optimized)
yarn tsx .claude/skills/ai-image-generation/scripts/generate-ai-image.ts \
  "Modern laptop showing AI image upscaling interface, before and after comparison, professional setup, blue lighting, photorealistic" \
  ./featured.png \
  1200 630

# Generate inline image 1 (800x600 - content width)
yarn tsx .claude/skills/ai-image-generation/scripts/generate-ai-image.ts \
  "Split screen comparison: pixelated blurry photo on left, crystal clear enhanced photo on right, dramatic before after" \
  ./inline-1.png \
  800 600

# Generate inline image 2 (800x600)
yarn tsx .claude/skills/ai-image-generation/scripts/generate-ai-image.ts \
  "Step-by-step visual showing image upload to AI processing to enhanced output, clean infographic style" \
  ./inline-2.png \
  800 600

# Generate inline image 3 (800x600) - optional but recommended
yarn tsx .claude/skills/ai-image-generation/scripts/generate-ai-image.ts \
  "Photo printer producing sharp print from upscaled image, professional photography studio, warm lighting" \
  ./inline-3.png \
  800 600
```

See `/ai-image-generation` skill for prompt templates and best practices.

---

## Step 2: Upload All Images with Metadata

**CRITICAL**: Always include metadata when uploading images so they can be found and reused later.

```bash
# Upload featured image WITH METADATA
FEATURED=$(curl -s -X POST http://localhost:3000/api/blog/images/upload \
  -H "x-api-key: $API_KEY" \
  -F "file=@./featured.png" \
  -F "alt_text=AI image upscaling before and after comparison" \
  -F "tags=before-after,upscaling,ai-processing,featured,laptop" \
  -F "image_type=featured" \
  -F "description=Featured image showing AI upscaling interface with before after comparison" \
  -F "prompt=Modern laptop showing AI image upscaling interface, before and after comparison, professional setup, blue lighting, photorealistic")
FEATURED_URL=$(echo "$FEATURED" | jq -r '.data.url')

# Upload inline image 1 WITH METADATA
INLINE1=$(curl -s -X POST http://localhost:3000/api/blog/images/upload \
  -H "x-api-key: $API_KEY" \
  -F "file=@./inline-1.png" \
  -F "alt_text=Before and after image quality comparison" \
  -F "tags=before-after,comparison,split-screen,inline,photo" \
  -F "image_type=inline" \
  -F "description=Split screen comparison of pixelated blurry photo versus crystal clear enhanced photo" \
  -F "prompt=Split screen comparison: pixelated blurry photo on left, crystal clear enhanced photo on right, dramatic before after")
INLINE1_URL=$(echo "$INLINE1" | jq -r '.data.url')

# Upload inline image 2 WITH METADATA
INLINE2=$(curl -s -X POST http://localhost:3000/api/blog/images/upload \
  -H "x-api-key: $API_KEY" \
  -F "file=@./inline-2.png" \
  -F "alt_text=AI upscaling process workflow diagram" \
  -F "tags=ai-processing,workflow,step-by-step,inline,infographic" \
  -F "image_type=inline" \
  -F "description=Step-by-step visual showing image upload to AI processing to enhanced output" \
  -F "prompt=Step-by-step visual showing image upload to AI processing to enhanced output, clean infographic style")
INLINE2_URL=$(echo "$INLINE2" | jq -r '.data.url')

# Upload inline image 3 WITH METADATA
INLINE3=$(curl -s -X POST http://localhost:3000/api/blog/images/upload \
  -H "x-api-key: $API_KEY" \
  -F "file=@./inline-3.png" \
  -F "alt_text=High quality print from upscaled image" \
  -F "tags=print-result,printer,professional,inline,photo" \
  -F "image_type=inline" \
  -F "description=Photo printer producing sharp print from upscaled image in professional studio" \
  -F "prompt=Photo printer producing sharp print from upscaled image, professional photography studio, warm lighting")
INLINE3_URL=$(echo "$INLINE3" | jq -r '.data.url')

echo "Featured: $FEATURED_URL"
echo "Inline 1: $INLINE1_URL"
echo "Inline 2: $INLINE2_URL"
echo "Inline 3: $INLINE3_URL"
```

### Metadata Fields Reference

| Field         | Required    | Description                                     |
| ------------- | ----------- | ----------------------------------------------- |
| `file`        | Yes         | Image file (PNG, JPG, WebP)                     |
| `alt_text`    | Recommended | Alt text for accessibility and SEO              |
| `tags`        | Recommended | Comma-separated tags from vocabulary (3-6 tags) |
| `image_type`  | Recommended | `featured` or `inline`                          |
| `description` | Optional    | Brief description of image content              |
| `prompt`      | Optional    | Original AI prompt used to generate             |

**Response format:**

```json
{
  "success": true,
  "data": {
    "url": "https://xxx.supabase.co/storage/v1/object/public/blog-images/2026/01/timestamp-filename.webp",
    "key": "2026/01/timestamp-filename.webp",
    "filename": "2026/01/timestamp-filename.webp",
    "metadata_id": "uuid-of-metadata-record"
  }
}
```

---

## Step 3: Create Blog Post with Inline Images

### Three Kings Rule (MANDATORY — apply before writing any content)

Every post must inject the **exact target keyword** into the Three Kings before publishing. This is how new posts rank from day one instead of needing a refresh later.

| King                         | Field                          | Rule                                                                               |
| ---------------------------- | ------------------------------ | ---------------------------------------------------------------------------------- |
| **King 1 — Title Tag**       | `seo_title`                    | Keyword must appear, front-loaded. Max 60 chars.                                   |
| **King 2 — H1**              | First `#` heading in `content` | Keyword in the heading. Can be slightly reworded but must contain the core phrase. |
| **King 3 — First Paragraph** | First `<p>` after the H1       | Keyword in the **first sentence** naturally. Not stuffed.                          |

**Optional but high-impact:** slug and `seo_description` also contain the keyword.

Self-check before submitting the POST request:

- [ ] `seo_title` contains exact target keyword
- [ ] First `# Heading` in content contains target keyword
- [ ] First sentence after the H1 contains target keyword
- [ ] `seo_description` contains keyword + CTA (under 155 chars)

**Reference:** seo-content-3-kings-technique skill — for existing pages that missed this, run `/seo-content-3-kings-technique [domain]` to identify and fix them.

---

Include the inline image URLs directly in the markdown content using standard markdown syntax.

```bash
# Create draft post with inline images in content
curl -s -X POST http://localhost:3000/api/blog/posts \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "how-to-upscale-images-4x",
    "title": "How to Upscale Images 4x: AI Photo Enhancement Guide [2026]",
    "description": "Learn how to upscale images 4x quality using AI. Free online tool for photos, graphics, and artwork. No quality loss, instant results.",
    "content": "# How to Upscale Images 4x\n\nLow-res photos hurt your credibility...\n\n## The Problem with Low Resolution\n\nPixelated images look unprofessional...\n\n![Before and after image quality comparison]('"$INLINE1_URL"')\n\n## How AI Upscaling Works\n\nUnlike simple resizing, AI upscaling adds real detail...\n\n![AI upscaling process workflow]('"$INLINE2_URL"')\n\n## Perfect for Printing\n\nUpscaled images are ideal for large prints...\n\n![High quality print result]('"$INLINE3_URL"')\n\n## Conclusion\n\n[Start upscaling your images now](https://myimageupscaler.com) - free, no signup required.",
    "author": "MyImageUpscaler Team",
    "category": "Guides",
    "tags": ["upscale", "AI", "tutorial"],
    "seo_title": "How to Upscale Images 4x Quality Free - AI Photo Enhancer",
    "seo_description": "Upscale images 4x quality instantly with AI. Free online photo enhancer for prints, social media, and more. No signup required."
  }' | jq .
```

### Inline Image Markdown Syntax

```markdown
![Alt text describing the image](https://your-supabase-url.../image.webp)
```

**Placement Guidelines:**

- Place images **after** the section they illustrate
- Space images evenly throughout content (every 2-3 sections)
- Always include descriptive alt text for SEO and accessibility

---

## Step 3.5: Add Internal Links (REQUIRED)

**CRITICAL**: Every blog post must contain 2-3 contextual internal links. Prioritize pages that are already getting GSC impressions but need more clicks — internal links from the blog push them up.

### Step A: Check GSC for High-Value Pages to Support

Before picking pages to link to, check which existing pages have impressions but low CTR. These are the highest-leverage internal link targets.

```bash
# Run GSC analysis to find pages worth supporting
# Use the /gsc-analysis skill or check the latest report:
cat docs/SEO/reports/gsc-*.md 2>/dev/null | grep -A3 "impression" | head -40
```

**Target pages with:**

- 50+ impressions / month
- CTR < 5%
- Position 8-30 (close to page 1 — a link boost can push them over)

These benefit most from internal link juice. Prefer linking to them over arbitrary pSEO pages.

### Step B: Discover Relevant pSEO Pages to Link

Scan the pSEO data files to find pages that match the blog post topic, then cross-reference with the GSC high-impression pages above. Pages that appear in both lists are the highest-priority link targets. Available categories:

```bash
# List all available pSEO categories
ls app/seo/data/*.json

# Search for pages relevant to your topic keyword
# Replace KEYWORD with your topic (e.g., "background", "4k", "jpeg", "ecommerce")
node -e "
const fs = require('fs');
const files = ['tools','free','formats','scale','use-cases','guides','alternatives','compare'];
const keyword = 'KEYWORD';
files.forEach(f => {
  try {
    const data = JSON.parse(fs.readFileSync(\`app/seo/data/\${f}.json\`,'utf-8'));
    const matches = data.pages.filter(p =>
      p.slug.includes(keyword) ||
      (p.primaryKeyword && p.primaryKeyword.toLowerCase().includes(keyword)) ||
      (p.metaTitle && p.metaTitle.toLowerCase().includes(keyword))
    );
    if (matches.length) console.log(\`[\${f}]\`, matches.map(p => \`/\${f}/\${p.slug}\`).join(', '));
  } catch(e) {}
});
"
```

### Category → URL Pattern

| Category file       | URL prefix       | Good for posts about...                    |
| ------------------- | ---------------- | ------------------------------------------ |
| `scale.json`        | `/scale/`        | Resolution, 4K, upscaling, print size      |
| `free.json`         | `/free/`         | Free tools, no signup, trial, credits      |
| `formats.json`      | `/formats/`      | JPEG, PNG, WebP, AVIF, HEIC, file formats  |
| `use-cases.json`    | `/use-cases/`    | E-commerce, real estate, portraits, anime  |
| `tools.json`        | `/tools/`        | Specific AI tools (enhancer, upscaler, bg) |
| `alternatives.json` | `/alternatives/` | Tool comparisons, vs, alternatives         |
| `compare.json`      | `/compare/`      | Comparisons, head-to-head                  |
| `guides.json`       | `/guides/`       | How-to guides, tutorials                   |

### High-Value pSEO Pages to Link (Most Common)

| URL                                        | Target anchor text ideas                    |
| ------------------------------------------ | ------------------------------------------- |
| `/scale/upscale-to-4k`                     | "4K resolution", "upscale to 4K"            |
| `/scale/upscale-to-1080p`                  | "1920x1080", "HD resolution", "1080p"       |
| `/free/free-image-upscaler`                | "free image upscaler", "free upscaling"     |
| `/free/free-background-remover`            | "free background remover"                   |
| `/free`                                    | "free tools", "free credits"                |
| `/formats/upscale-jpeg-images`             | "JPEG images", "upscale JPG"                |
| `/formats/upscale-png-images`              | "PNG images"                                |
| `/formats/upscale-webp-images`             | "WebP images"                               |
| `/formats/upscale-avif-images`             | "AVIF images"                               |
| `/use-cases/ecommerce-product-photos`      | "product photos", "e-commerce photos"       |
| `/use-cases/old-photo-restoration`         | "photo restoration", "restore old photos"   |
| `/use-cases/real-estate-photo-enhancement` | "real estate photos"                        |
| `/use-cases/anime-image-upscaler`          | "anime upscaling", "illustration upscaling" |
| `/tools/ai-background-remover`             | "remove backgrounds", "background removal"  |
| `/tools/ai-photo-enhancer`                 | "photo enhancer", "enhance photo quality"   |
| `/alternatives`                            | "tool alternatives", "comparing tools"      |

### Rules for Adding Links

1. **GSC first** — prefer linking to pages with 50+ impressions and CTR < 5% (they need the boost most)
2. **Read the draft post content first** — understand what's in each paragraph
3. **Find 2-3 natural anchor opportunities** — where the linked page URL genuinely adds value for the reader
4. **Embed links in existing sentences** — never add a "Related Links" section or "See also" block
5. **Use descriptive anchor text** — the linked text should be a natural keyword phrase, not "click here"
6. **No zombie categories** — never link to `/ai-features/`
7. **Canonical BG removal links** — always link to `/tools/ai-background-remover` (not `/tools/remove-bg`)

### Example Link Insertions

```markdown
<!-- Original -->

AI upscalers can enlarge images to 4K resolution.

<!-- With link -->

AI upscalers can enlarge images to [4K resolution](/scale/upscale-to-4k).

<!-- Original -->

JPEG files can still be upscaled without losing quality.

<!-- With link -->

[JPEG files](/formats/upscale-jpeg-images) can still be upscaled without losing quality.

<!-- Original -->

For e-commerce sellers, product photo quality matters.

<!-- With link -->

For e-commerce sellers, [product photo quality](/use-cases/ecommerce-product-photos) matters.

<!-- Original -->

Start with our free tools if you're new.

<!-- With link -->

Start with our [free upscaling tools](/free) if you're new.
```

### Update the Post Content with Links

After identifying insertion points, PATCH the post with the updated content:

```bash
# After updating the markdown content with internal links, PATCH the post
curl -s -X PATCH http://localhost:3000/api/blog/posts/YOUR-SLUG \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "...updated content with internal pSEO links..."
  }' | jq .
```

---

## Step 4: Update Post with Featured Image

```bash
curl -s -X PATCH http://localhost:3000/api/blog/posts/how-to-upscale-images-4x \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "featured_image_url": "'"$FEATURED_URL"'",
    "featured_image_alt": "AI image upscaling comparison showing original vs upscaled result"
  }' | jq .
```

---

## Step 5: Publish Post

```bash
curl -s -X POST http://localhost:3000/api/blog/posts/how-to-upscale-images-4x/publish \
  -H "x-api-key: $API_KEY" | jq .
```

---

## Step 6: Verify

```bash
# Check API
curl -s http://localhost:3000/api/blog/posts/how-to-upscale-images-4x \
  -H "x-api-key: $API_KEY" | jq '{title, status, published_at}'

# Check frontend
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/blog/how-to-upscale-images-4x
```

---

## Step 7: Update Content Tracking (REQUIRED)

**CRITICAL**: After publishing, update the tracking file to prevent future duplication.

```bash
# Variables from your published post
PUBLISHED_DATE=$(date +%Y-%m-%d)
KEYWORD="your target keyword"  # e.g., "upscale image 4x"
BLOG_SLUG="your-blog-slug"     # e.g., "how-to-upscale-images-4x"
ROADMAP_SEGMENT="Segment B"    # From Step -1
ESTIMATED_IMPACT="+30 clicks/mo" # From roadmap

# Add to "Topics Covered" section
cat >> docs/SEO/blog-content-tracking/topics-covered.md << EOF

| $PUBLISHED_DATE | $KEYWORD | $BLOG_SLUG | $ROADMAP_SEGMENT | ✅ Published |
EOF

echo "✅ Tracking file updated!"
echo "File: docs/SEO/blog-content-tracking/topics-covered.md"
```

### Tracking File Maintenance

**Weekly**: Review and update the "Topics Planned" section from the latest keyword roadmap:

```bash
# Get latest roadmap
LATEST_ROADMAP=$(ls -t docs/SEO/keyword-strategy-roadmap-*.md | head -1)

# Extract top 10 uncovered opportunities
echo "Updating planned topics from roadmap..."

# Manual step: Copy Segment A and B opportunities from roadmap
# Add them to "Topics Planned" table if not already covered
```

---

## SEO Requirements

### Minimum Thresholds

| Field          | Requirement                              |
| -------------- | ---------------------------------------- |
| Title          | 5-200 chars                              |
| Description    | 20-500 chars                             |
| Slug           | 3-100 chars, lowercase with hyphens only |
| Content        | Min 100 chars                            |
| Featured Image | Recommended for better engagement        |

### Optimal Ranges

| Field         | Optimal                                |
| ------------- | -------------------------------------- |
| Title         | 50-70 chars, has brackets `[2026]`     |
| Description   | 150-160 chars, ends with CTA           |
| Slug          | 3-5 words, contains main keyword       |
| Content       | 1000+ words, 4+ H2s                    |
| Featured img  | 1 AI-generated (1200x630)              |
| Inline images | 2-3 AI-generated (800x600) in markdown |

---

## CTA (Call-to-Action) Requirements

> **🚨 HARD REQUIREMENT — DO NOT PUBLISH WITHOUT CTAs**
>
> Every blog post MUST have at least **2 BlogCTA component markers** embedded in the content.
> A post without CTAs gets impressions but zero clicks. This is the #1 reason posts fail to convert.

### The BlogCTA System (PRIMARY METHOD)

The blog renderer converts blockquote markers into fully-styled CTA components automatically. Use these markers in your markdown content:

| Marker               | Renders As                                 | When to Use                                           |
| -------------------- | ------------------------------------------ | ----------------------------------------------------- |
| `> [!CTA_TRY]`       | Inline banner with "Try Free" button       | After explaining a benefit or completing a section    |
| `> [!CTA_DEMO]`      | Feature highlights card with demo CTA      | Before FAQ or Conclusion — high-intent position       |
| `> [!CTA_PRICING]`   | Pricing-focused CTA                        | When discussing plans or paid features                |
| `> [!CTA_TOOL:slug]` | Tool-specific CTA (links to `/tools/slug`) | Posts about a specific tool (e.g. background remover) |

**How to write them in markdown:**

```markdown
## After this section I want a CTA

Some content explaining value...

> [!CTA_TRY]

## Next section continues here
```

```markdown
<!-- Tool-specific: links to /tools/transparent-background-maker -->

> [!CTA_TOOL:transparent-background-maker]

<!-- Tool-specific: links to /tools/ai-image-upscaler -->

> [!CTA_TOOL:ai-image-upscaler]
```

### Required CTA Placements (MANDATORY)

Every post MUST have ALL THREE of the following:

- [ ] **Mid-article CTA** — `> [!CTA_TRY]` after the first major value section (before the halfway point)
- [ ] **Pre-conclusion CTA** — `> [!CTA_DEMO]` immediately before `## Conclusion` or `## FAQ`
- [ ] **Description CTA** — Meta description must end with an action word ("try now", "try free", "instant results")

### Content Structure with CTAs (REQUIRED TEMPLATE)

```markdown
# H1 Title

Introduction paragraph...

## Section 1 — Explain the problem

Content...

## Section 2 — Show the value

Content...

> [!CTA_TRY]

## Section 3 — How it works / Step-by-step

Content...

![Inline image](url)

## Section 4 — Use cases / Tips

Content...

> [!CTA_DEMO]

## Conclusion

Summary sentence.

[Start upscaling your images for free](https://myimageupscaler.com) — no signup required.

---

## Frequently Asked Questions
```

### Tool-Specific Posts

If the post is about a specific tool (background remover, face restore, etc.), use `CTA_TOOL` instead of `CTA_TRY` for the mid-article CTA:

```markdown
> [!CTA_TOOL:transparent-background-maker]
> [!CTA_TOOL:ai-image-upscaler]
> [!CTA_TOOL:ai-face-restorer]
```

### Secondary: Inline Contextual Links

In addition to the component CTAs, embed 1-2 natural inline links in the body:

```markdown
[Try our AI upscaler](https://myimageupscaler.com) and see the difference instantly.
[Upload your photo free](https://myimageupscaler.com) — 4x enhancement in seconds.
[Start upscaling now](https://myimageupscaler.com) — no credit card required.
```

### Accurate Claims — DO NOT LIE

The free plan has limits. Always be accurate:

- ✅ "Try free — no account required" (guest access works)
- ✅ "Get 10 free credits on signup — no credit card"
- ✅ "No watermarks, no signup to try"
- ❌ "Unlimited free upscaling" — FALSE (10 credits on signup, no monthly refresh)
- ❌ "Free forever, no limits" — FALSE
- ❌ "Unlimited uploads" — FALSE

### Pre-Publish CTA Checklist

Before calling the publish endpoint, verify:

```bash
# Check that CTA markers exist in the content
echo "$POST_CONTENT" | grep -c "\[!CTA_" && echo "✅ CTA markers found" || echo "❌ BLOCKED: No CTA markers — do not publish"

# Should return at least 2
CTA_COUNT=$(echo "$POST_CONTENT" | grep -c "\[!CTA_")
[ "$CTA_COUNT" -ge 2 ] || { echo "❌ Need at least 2 CTAs, found $CTA_COUNT"; exit 1; }
```

---

## Categories & Tags

**Available Categories:**

- `Guides` - How-to tutorials and step-by-step instructions
- `Tips` - Quick tips and tricks
- `Comparisons` - Tool comparisons, before/after
- `News` - Industry news and updates
- `Technical` - Deep technical explanations

**Available Tags:**

- `upscale`, `AI`, `tutorial`, `photo`, `image`, `enhancement`, `resolution`, `prints`, `social-media`, `graphics`, `artwork`, `logo`, `product-photos`, `ecommerce`, `restoration`, `batch`, `free`, `online`

---

## Content Guidelines

### Title Format

Use this pattern: `[Keyword]: [Benefit] [Year]`

Examples:

- "How to Upscale Images for Print: Complete Guide [2026]"
- "AI Photo Enhancer: 5 Ways to Improve Image Quality [2026]"
- "Image Upscaling vs Resizing: What's the Difference? [2026]"

### Content Structure

```markdown
# H1 Title (matches page title)

Engaging introduction paragraph (3-4 sentences). Mention the problem and promise solution.

## Understanding the Concept

Explain the core topic. Use examples.

![Inline image 1 - illustrates the concept](https://supabase-url/inline-1.webp)

## Why It Matters

Benefits and use cases. Real-world applications.

## Step-by-Step Guide

Numbered steps with clear instructions.

![Inline image 2 - shows the process](https://supabase-url/inline-2.webp)

## Tips for Best Results

Actionable tips and recommendations.

## Common Mistakes to Avoid

What not to do, with explanations.

![Inline image 3 - shows results](https://supabase-url/inline-3.webp)

## Conclusion

Summary + [Primary CTA link](https://myimageupscaler.com).
```

**Image Placement Rules:**

- Place images **after** the section they illustrate
- Space 2-3 images evenly throughout (every 2-3 H2 sections)
- Never place images in introduction or conclusion

---

## Humanizing Content

### AI Patterns to AVOID

| Category            | Words to Avoid                                      |
| ------------------- | --------------------------------------------------- |
| **Overused**        | delve, tapestry, nuanced, multifaceted, landscape   |
| **Corporate**       | leverage, facilitate, streamline, optimize, utilize |
| **Filler**          | "It's important to note", "worth noting"            |
| **Hype**            | groundbreaking, revolutionary, game-changing        |
| **Throat-clearing** | "In today's world", "Here's the thing"              |

### Human Writing Techniques

```markdown
❌ AI: "Image upscaling represents a significant advancement in AI technology."
✅ Human: "I've tried dozens of upscalers. Most make your photos look like plastic."

❌ AI: "This solution offers numerous benefits for users."
✅ Human: "Here's what makes this different: it actually preserves details."

❌ AI: "The process facilitates enhanced image quality."
✅ Human: "Your photos get sharper. Period."
```

**Writing Rules:**

- First sentence must deliver value immediately
- Use active voice: "The tool sharpens photos" not "Photos are sharpened"
- Keep paragraphs short (2-4 sentences max)
- Mix sentence lengths (some 5 words, some 20+ words)
- Use first-person occasionally: "I tested this...", "Our team found..."

---

## Image Guidelines

### Image Requirements

| Image Type | Dimensions | Purpose                          |
| ---------- | ---------- | -------------------------------- |
| Featured   | 1200x630   | Social sharing, post header      |
| Inline     | 800x600    | Content illustrations (2-3 each) |

**All images must be:**

- AI-generated using `/ai-image-generation` skill
- Uploaded to Supabase Storage
- Include descriptive alt text for SEO/accessibility

### Prompt Templates by Topic

**For "How to upscale images" posts:**

```
Featured: "Modern laptop screen showing AI photo upscaling interface, before and after comparison, professional setup, blue lighting, photorealistic"
Inline 1: "Split screen: pixelated blurry photo on left, crystal clear enhanced photo on right, dramatic comparison"
Inline 2: "Step-by-step visual: image upload to AI processing to enhanced output, clean infographic style"
Inline 3: "Person examining sharp enlarged photo on screen, professional workspace, satisfied expression"
```

**For "Image resolution" posts:**

```
Featured: "Computer monitor showing pixelated vs sharp image comparison, professional photo editing workspace"
Inline 1: "Magnified pixel grid next to smooth high-res detail, educational comparison"
Inline 2: "Digital image being transformed from blocky to smooth, visualization of upscaling process"
```

**For "Print preparation" posts:**

```
Featured: "Photo printer producing high-quality print, professional photography studio"
Inline 1: "Side by side: small low-res image next to large crisp printed poster"
Inline 2: "Hands holding sharp printed photo, professional quality result"
```

---

## Environment Configuration

The `BLOG_API_KEY` is stored in `.env.api`:

```bash
# Development
BLOG_API_KEY=test-blog-api-key-xxx

# Load with:
source scripts/load-env.sh
API_KEY=$(grep BLOG_API_KEY .env.api | cut -d'=' -f2)
```

---

## Troubleshooting

### "A post with this slug already exists" (409)

Either delete the existing post or use a different slug:

```bash
# Delete existing
curl -s -X DELETE http://localhost:3000/api/blog/posts/[slug] \
  -H "x-api-key: $API_KEY"
```

### Image not showing on blog page

1. Check the URL is accessible
2. Verify `featured_image_url` is set correctly
3. Check browser console for 403/CORS errors

### Post not appearing on blog page

Only **published** posts appear. Drafts are only accessible via direct slug URL.

---

## Example: Complete Post Creation (Search-First Workflow)

```bash
# 0. Load environment
source scripts/load-env.sh
API_KEY=$(grep BLOG_API_KEY .env.api | cut -d'=' -f2)

# =========================================
# STEP 0: SEARCH FOR EXISTING IMAGES FIRST
# =========================================

# Search for featured image (before-after theme)
FEATURED_SEARCH=$(curl -s "http://localhost:3000/api/blog/images?tags=before-after,upscaling&image_type=featured&limit=3" \
  -H "x-api-key: $API_KEY")
FEATURED_COUNT=$(echo "$FEATURED_SEARCH" | jq '.data | length')

# Search for inline images (ai-processing theme)
INLINE_SEARCH=$(curl -s "http://localhost:3000/api/blog/images?tags=ai-processing,comparison&image_type=inline&limit=5" \
  -H "x-api-key: $API_KEY")
INLINE_COUNT=$(echo "$INLINE_SEARCH" | jq '.data | length')

# Decision: Reuse or generate
if [ "$FEATURED_COUNT" -gt 0 ] && [ "$INLINE_COUNT" -ge 2 ]; then
  echo "Found suitable existing images - reusing them"
  FEATURED_URL=$(echo "$FEATURED_SEARCH" | jq -r '.data[0].url')
  INLINE1_URL=$(echo "$INLINE_SEARCH" | jq -r '.data[0].url')
  INLINE2_URL=$(echo "$INLINE_SEARCH" | jq -r '.data[1].url')
else
  echo "No suitable images found - generating new ones"

  # =========================================
  # STEP 1: GENERATE IMAGES (only if needed)
  # =========================================
  yarn tsx .claude/skills/ai-image-generation/scripts/generate-ai-image.ts \
    "Modern laptop showing AI photo upscaling, before after comparison, blue lighting" \
    ./featured.png 1200 630

  yarn tsx .claude/skills/ai-image-generation/scripts/generate-ai-image.ts \
    "Split screen: pixelated photo left, crystal clear photo right, dramatic comparison" \
    ./inline-1.png 800 600

  yarn tsx .claude/skills/ai-image-generation/scripts/generate-ai-image.ts \
    "AI neural network processing image, visualization of enhancement process" \
    ./inline-2.png 800 600

  # =========================================
  # STEP 2: UPLOAD WITH METADATA
  # =========================================
  FEATURED_URL=$(curl -s -X POST http://localhost:3000/api/blog/images/upload \
    -H "x-api-key: $API_KEY" \
    -F "file=@./featured.png" \
    -F "alt_text=AI upscaling comparison" \
    -F "tags=before-after,upscaling,ai-processing,featured,laptop" \
    -F "image_type=featured" \
    -F "prompt=Modern laptop showing AI photo upscaling, before after comparison, blue lighting" | jq -r '.data.url')

  INLINE1_URL=$(curl -s -X POST http://localhost:3000/api/blog/images/upload \
    -H "x-api-key: $API_KEY" \
    -F "file=@./inline-1.png" \
    -F "alt_text=Before after comparison" \
    -F "tags=before-after,comparison,split-screen,inline,photo" \
    -F "image_type=inline" \
    -F "prompt=Split screen: pixelated photo left, crystal clear photo right, dramatic comparison" | jq -r '.data.url')

  INLINE2_URL=$(curl -s -X POST http://localhost:3000/api/blog/images/upload \
    -H "x-api-key: $API_KEY" \
    -F "file=@./inline-2.png" \
    -F "alt_text=AI processing visualization" \
    -F "tags=ai-processing,workflow,step-by-step,inline,infographic" \
    -F "image_type=inline" \
    -F "prompt=AI neural network processing image, visualization of enhancement process" | jq -r '.data.url')
fi

echo "Using images:"
echo "  Featured: $FEATURED_URL"
echo "  Inline 1: $INLINE1_URL"
echo "  Inline 2: $INLINE2_URL"

# =========================================
# STEP 3: CREATE DRAFT WITH INLINE IMAGES
# =========================================
curl -s -X POST http://localhost:3000/api/blog/posts \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "ai-image-upscaling-guide",
    "title": "AI Image Upscaling: Complete Guide to Better Photos [2026]",
    "description": "Learn how AI image upscaling works and can transform your low-res photos into print-quality images. Free online tool.",
    "content": "# AI Image Upscaling: The Complete Guide\n\nLow-resolution photos look unprofessional. AI upscaling changes that.\n\n## What Is AI Image Upscaling?\n\nTraditional upscaling just copies pixels. AI upscaling adds real detail.\n\n![Before and after comparison]('"$INLINE1_URL"')\n\n## How It Works\n\nNeural networks analyze patterns and generate new pixels.\n\n![AI processing visualization]('"$INLINE2_URL"')\n\n## Conclusion\n\n[Start upscaling your images now](https://myimageupscaler.com) - free, instant results.",
    "author": "MyImageUpscaler Team",
    "category": "Guides",
    "tags": ["upscale", "AI", "tutorial", "photo"],
    "seo_title": "AI Image Upscaling Guide - Free Photo Enhancer Tool",
    "seo_description": "Transform low-res photos into print-quality images with AI upscaling. Free online tool - instant results, no signup required."
  }' | jq .

# =========================================
# STEP 4: ADD FEATURED IMAGE
# =========================================
curl -s -X PATCH http://localhost:3000/api/blog/posts/ai-image-upscaling-guide \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "featured_image_url": "'"$FEATURED_URL"'",
    "featured_image_alt": "AI image upscaling before and after comparison"
  }' | jq .

# =========================================
# STEP 5: PUBLISH
# =========================================
curl -s -X POST http://localhost:3000/api/blog/posts/ai-image-upscaling-guide/publish \
  -H "x-api-key: $API_KEY" | jq .

# =========================================
# STEP 6: VERIFY
# =========================================
curl -s http://localhost:3000/blog/ai-image-upscaling-guide | grep -o "<title>.*</title>"
```

---

## Production Notes

- Posts are stored in Supabase `blog_posts` table
- Published posts are public, drafts are API-only
- Supabase Storage for featured images (auto-compressed to WebP)
- Reading time is auto-calculated from content
- `updated_at` is auto-updated on any change
- **IndexNow Integration**: Published posts are automatically submitted to IndexNow for faster search engine indexing

## Image Storage Details

- **Bucket:** `blog-images` (Supabase Storage)
- **Max input size:** 10MB (before compression)
- **Output format:** WebP (auto-converted)
- **Max dimensions:** 1920x1080 (auto-resized)
- **Compression:** 80% quality
- **Cache:** 1 year CDN cache
- **Path format:** `YYYY/MM/timestamp-filename.webp`

---

## Related Skills

- `/ai-image-generation` - Generate featured and inline images with AI
- `/blog-edit` - Edit existing blog posts
- `/internal-linking-optimizer` - Analyze and optimize internal link structure site-wide

## pSEO Sitemap Reference

To browse all available pSEO pages for linking, check the data files:

- `app/seo/data/tools.json` → `/tools/*` pages
- `app/seo/data/free.json` → `/free/*` pages
- `app/seo/data/formats.json` → `/formats/*` pages
- `app/seo/data/scale.json` → `/scale/*` pages
- `app/seo/data/use-cases.json` → `/use-cases/*` pages
- `app/seo/data/alternatives.json` → `/alternatives/*` pages
- `app/seo/data/compare.json` → `/compare/*` pages
- `app/seo/data/guides.json` → `/guides/*` pages
