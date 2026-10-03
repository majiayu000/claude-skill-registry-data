---
name: blog-writing
description: Write SEO-optimized blog posts for MyImageUpscaler. Use when creating new blog content, optimizing existing posts, or planning content strategy.
---

# Blog Writing Skill

## Changelog

**Before starting:** Read recent entries to understand what topics and angles have already been covered.

```bash
tail -60 .claude/skills/blog-changelog.md
```

**After finishing:** Append a brief entry.

```bash
cat >> .claude/skills/blog-changelog.md << 'EOF'

## YYYY-MM-DD

### Write: [slug or topic]
**Why:** [keyword opportunity / content gap]
**Changes:**
- `slug` — [topic summary, target keyword, word count]
EOF
```

---

## Quick Reference

### Directory Structure

```
content/blog/              # Blog posts (MDX format)
├── *.mdx                  # Individual posts
app/blog/
├── page.tsx               # Blog listing page
└── [slug]/page.tsx        # Individual post page
public/before-after/       # Before/after comparison images
├── girl-before.webp
├── girl-after.webp
├── bird-before.webp
└── bird-after.webp
```

## Blog Post Format

### Frontmatter (Required)

```yaml
---
title: "Post Title - Include Primary Keyword"
description: "150-160 chars. Include keyword and value prop. End with action."
date: "YYYY-MM-DD"
author: "MyImageUpscaler Team"
category: "Tutorials" | "Comparisons" | "E-commerce" | "Tips"
tags: ["tag1", "tag2", "tag3", "tag4"]
image: "/blog/images/post-cover.jpg"  # Optional: OG image
---
```

### Content Structure

1. **Hook** (1-2 paragraphs) - Identify problem, connect emotionally
2. **Context** - Why this matters, statistics if available
3. **Main Sections** (3-5) - H2 headers, actionable content
   - Add **contextual Unsplash image** after every 2-3 sections
4. **Callouts** - Tips, warnings, info boxes
5. **CTA** - Link to `/pricing`

**Visual rhythm:** Text → Image → Text → Table → Text → Image → CTA

## Writing Guidelines

### SEO Optimization

- **Title**: 50-60 chars, primary keyword near start
- **Description**: 150-160 chars, keyword + benefit + CTA
- **H1**: Match title or slight variation
- **H2s**: Include secondary keywords naturally
- **Intro**: Primary keyword in first 100 words
- **Internal links**: Link to `/pricing`, other blog posts

### Keyword Targeting

Reference `/docs/SEO/keywords.csv` for keyword research:

| Volume | Priority | Example                                         |
| ------ | -------- | ----------------------------------------------- |
| 500K+  | High     | "image upscaler", "ai photo enhancer"           |
| 50K+   | Medium   | "upscale image to 4k", "free image upscaler"    |
| 5K+    | Low      | "best ai upscaler", "photo resolution enhancer" |

### Content Components

#### Callout Types

```mdx
<Callout type="tip">Pro tip content here.</Callout>

<Callout type="info">Informational content here.</Callout>

<Callout type="warning">Warning or caution content here.</Callout>
```

#### Tables

```markdown
| Column 1 | Column 2 | Column 3 |
| -------- | -------- | -------- |
| Data 1   | Data 2   | Data 3   |
```

#### Code Blocks

```markdown
\`\`\`
Code or formula here
\`\`\`
```

#### Images

Reference images from `/public/` using absolute paths:

```markdown
![Alt text](/before-after/girl-before.webp)
```

For before/after comparisons:

```markdown
| Before                                              | After                                             |
| --------------------------------------------------- | ------------------------------------------------- |
| ![Before upscaling](/before-after/bird-before.webp) | ![After upscaling](/before-after/bird-after.webp) |
```

## Sourcing Images from Public APIs

Use free stock photo APIs to add relevant images to blog posts. **Every post should have 2-4 images** placed contextually throughout the content.

### Image Placement Strategy (REQUIRED)

**Minimum images per post: 3**

1. **Hero/OG Image** (frontmatter) - Eye-catching, represents the topic
2. **Mid-post image** (after 2nd or 3rd H2) - Illustrates a key concept
3. **Supporting image** (before conclusion) - Reinforces the message or shows results

**Contextual relevance rules:**

| Post Topic            | Image Ideas                                          | Unsplash Search Terms                                     |
| --------------------- | ---------------------------------------------------- | --------------------------------------------------------- |
| Old photo restoration | Vintage photos, family albums, old cameras           | "vintage photographs", "old family photos", "photo album" |
| Social media          | Phone with apps, content creation, influencer        | "social media phone", "instagram", "content creator"      |
| E-commerce            | Product photography, online shopping, packaging      | "product photography", "ecommerce", "online store"        |
| Printing              | Printer, photo prints, frames                        | "photo printing", "framed photos", "print shop"           |
| General upscaling     | High-res landscapes, detailed textures, before/after | "high resolution", "detailed photo", "sharp image"        |

**In-content image format:**

```markdown
## Section About Scanning Old Photos

When scanning vintage photographs, resolution matters more than you might think.

![Stack of vintage family photographs on wooden desk](https://images.unsplash.com/photo-1516981879613-9f5da904015f?w=800&q=80)

The key is to capture as much detail as possible from the original...
```

**Image placement rules:**

- Place images **after** introducing a concept, not before
- Use images to **break up long text** sections (every 300-400 words)
- Match image mood to section content (technical sections → clean/minimal images)
- Avoid generic stock photos—choose images that add meaning

### Unsplash API

**Source URL Pattern:**

```
https://unsplash.com/photos/{photo-id}
```

**Direct Image URL (for downloading):**

```
https://images.unsplash.com/photo-{id}?w=1200&q=80
```

**How to find images:**

1. Search on [unsplash.com](https://unsplash.com) for relevant terms
2. Find a suitable image and copy the photo ID from URL
3. Download using the direct URL pattern above
4. Save to `/public/blog/images/{post-slug}/`

**Example workflow:**

```bash
# Create directory for post images
mkdir -p public/blog/images/restore-old-photos

# Download image (use curl or wget)
curl -o public/blog/images/restore-old-photos/vintage-camera.jpg \
  "https://images.unsplash.com/photo-1542567455-cd733f23fbb1?w=1200&q=80"
```

**Attribution:** Unsplash images are free to use without attribution, but credit is appreciated:

```markdown
![Vintage camera on wooden table](/blog/images/restore-old-photos/vintage-camera.jpg)
_Photo by [Photographer Name](https://unsplash.com/@username) on Unsplash_
```

### Other Free Image Sources

| Source       | URL           | License                       | Best For               |
| ------------ | ------------- | ----------------------------- | ---------------------- |
| Unsplash     | unsplash.com  | Free, no attribution required | High-quality photos    |
| Pexels       | pexels.com    | Free, no attribution required | Lifestyle, business    |
| Pixabay      | pixabay.com   | Free, no attribution required | Illustrations, vectors |
| Lorem Picsum | picsum.photos | Free placeholder              | Development/testing    |

### Image Guidelines for Blog Posts

1. **Download and host locally** - Don't hotlink to external URLs
2. **Optimize file size** - Use WebP format, max 200KB per image
3. **Consistent dimensions** - 1200x630 for hero images (OG compatible)
4. **Descriptive filenames** - `vintage-photo-album.webp` not `img123.webp`
5. **Alt text required** - Describe the image for accessibility and SEO

### Directory Structure for Blog Images

```
public/blog/images/
├── {post-slug}/           # Per-post image folder
│   ├── hero.webp          # Main/OG image
│   ├── step-1.webp        # Tutorial steps
│   └── comparison.webp    # Before/after
└── shared/                # Reusable across posts
    ├── upscaler-ui.webp
    └── quality-comparison.webp
```

### Quick Unsplash Image URLs (Copy-Paste Ready)

Use these directly in markdown with `?w=800&q=80` for in-content images:

```markdown
# Photography & Cameras

![Vintage camera](https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&q=80)
![DSLR camera close-up](https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&q=80)

# Old Photos & Nostalgia

![Vintage photo album](https://images.unsplash.com/photo-1516981879613-9f5da904015f?w=800&q=80)
![Old photographs](https://images.unsplash.com/photo-1504805572947-34fad45aed93?w=800&q=80)

# Social Media & Mobile

![Phone with social apps](https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=800&q=80)
![Content creator setup](https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=800&q=80)

# E-commerce & Products

![Product photography setup](https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80)
![Online shopping](https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&q=80)

# Printing & Frames

![Photo prints spread out](https://images.unsplash.com/photo-1598539912560-e1a1fdc7b8c5?w=800&q=80)
![Framed photos on wall](https://images.unsplash.com/photo-1513519245088-0e12902e35a6?w=800&q=80)

# Quality & Detail

![High-res landscape](https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80)
![Detailed texture](https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80)
```

### Unsplash Search Tips

| Need                 | Search Terms                        |
| -------------------- | ----------------------------------- |
| Hero images          | Add "minimal", "clean background"   |
| Technical content    | Add "workspace", "desk setup"       |
| Before/after concept | "transformation", "comparison"      |
| Action shots         | "working on", "editing", "creating" |

### Quick Image Download Script

```bash
# Function to download and optimize Unsplash image
download_blog_image() {
  local photo_id=$1
  local output_path=$2
  curl -sL "https://images.unsplash.com/photo-${photo_id}?w=1200&q=80" -o "${output_path}"
}

# Usage
download_blog_image "1542567455-cd733f23fbb1" "public/blog/images/my-post/hero.jpg"
```

## Category Guidelines

### Tutorials

- Step-by-step instructions
- Clear numbered steps
- Expected outcomes
- Troubleshooting tips
- Tags: ["tutorials", "how-to", specific topic]

### Comparisons

- Objective criteria
- Tables for easy scanning
- Clear winner recommendation
- Tags: ["comparison", "reviews", tool names]

### E-commerce

- Business-focused benefits
- ROI calculations
- Platform-specific tips (Amazon, Shopify, eBay)
- Tags: ["e-commerce", "product photography", platform names]

### Tips

- Quick, actionable advice
- Bullet points preferred
- Visual examples
- Tags: ["tips", "quick tips", specific topic]

## Product Mentions

### Natural Integration

- Mention myimageupscaler.com benefits organically
- Highlight differentiators:
  - Text/logo preservation (unique strength)
  - No watermarks on output
  - Fast processing (30-60 seconds)
  - E-commerce optimization
  - 10 free credits

### CTAs (Call-to-Action) - CRITICAL FOR ACQUISITION

Strategic CTA placement is essential for converting readers into users. Every blog post MUST include multiple CTAs.

**IMPORTANT: Link Destinations**

- **There is NO `/upscaler` page** - this route does not exist!
- CTAs link to `/?signup=1` (homepage with signup prompt)
- Pricing links go to `/pricing`
- Tool-specific links go to `/tools/{slug}`

#### CTA Types

Use blockquote-style markers to insert standardized CTAs:

| Marker               | Type          | Best Use Case                                                       |
| -------------------- | ------------- | ------------------------------------------------------------------- |
| `> [!CTA_TRY]`       | Try It        | Mid-article, after explaining a concept                             |
| `> [!CTA_DEMO]`      | Demo          | After before/after comparisons or visual examples                   |
| `> [!CTA_PRICING]`   | Pricing       | Near end, for value-conscious readers                               |
| `> [!CTA_TOOL:slug]` | Tool-specific | Link to specific tool page (e.g., `> [!CTA_TOOL:upscale-image-2x]`) |

#### CTA Placement Strategy (REQUIRED)

**Minimum CTAs per post: 2**

| Placement                    | When                                         | CTA Type         |
| ---------------------------- | -------------------------------------------- | ---------------- |
| After Hook (25% mark)        | Reader is engaged, understanding the problem | `[!CTA_TRY]`     |
| Mid-article (50% mark)       | After key insight or before/after demo       | `[!CTA_DEMO]`    |
| Before Conclusion (75% mark) | Reader has learned, ready to act             | `[!CTA_PRICING]` |

**Example placement in article structure:**

```markdown
## Introduction / Hook

(Problem statement, emotional connection)

## Why This Matters

(Context, statistics)

> [!CTA_TRY]

## Main Section 1

(First key insight)

## Main Section 2

(Tutorial steps or comparison)

> [!CTA_DEMO]

## Main Section 3

(Advanced tips)

## Conclusion

> [!CTA_PRICING]
```

#### CTA Best Practices

1. **Place after value**: Never put a CTA before explaining the benefit
2. **Match context**: Use `[!CTA_DEMO]` after showing visual results
3. **Don't over-CTA**: Maximum 3 in-content CTAs (plus bottom page CTA)
4. **Natural flow**: CTA should feel like a helpful suggestion, not interruption

#### Legacy CTA (Text-only)

For subtle inline CTAs within paragraphs, use markdown links:

```markdown
Ready to enhance your images? [Try myimageupscaler.com free](/pricing) — 10 credits, no credit card required.
```

## Legal Guidelines (CRITICAL)

### Never Do

- **No fabricated benchmarks** - Never invent test scores, performance metrics, or comparison data
- **No false competitor claims** - Never make claims about competitor products you cannot prove
- **No fake reviews/testimonials** - Never create fictional user experiences or quotes
- **No made-up statistics** - Never invent market data, percentages, or research findings

### Safe Content Types

1. **Educational content** - Explain concepts, techniques, how things work
2. **First-party showcases** - Before/after examples using YOUR tool with real images
3. **Use-case guides** - Practical tutorials for specific workflows (e-commerce, printing, etc.)
4. **General advice** - Tips that apply regardless of tool used
5. **Verified facts only** - Only cite statistics from reputable, linkable sources

### If Mentioning Competitors

- Only state **verifiable public facts** (pricing from their website, features they list)
- Use phrases like "at time of writing" for pricing/features that may change
- Never claim their quality is worse without actual documented evidence
- Prefer generic category references ("many online tools") over naming competitors

### Safe Comparison Approaches

- Compare YOUR tool's results (before/after) without mentioning competitors
- Compare approaches/methods generically (e.g., "browser-based vs desktop software")
- Link to third-party reviews if you need comparison data
- Use open-source tools (Waifu2x, Real-ESRGAN) for technical comparisons - less legal risk

## Validation Checklist

Before publishing:

**SEO & Metadata**

- [ ] Title is 50-60 characters with primary keyword
- [ ] Description is 150-160 characters with CTA
- [ ] Date is in YYYY-MM-DD format
- [ ] Category matches allowed values
- [ ] 3-5 relevant tags included
- [ ] Primary keyword in first 100 words

**Content & Links**

- [ ] 2+ internal links to /pricing, /?signup=1, or other blog posts
- [ ] NO links to /upscaler (this page does not exist!)
- [ ] Callouts used for tips/warnings

**Images**

- [ ] 3+ images: hero (frontmatter) + 2 mid-content Unsplash images
- [ ] Images are contextually relevant to surrounding content
- [ ] No broken image paths

**CTAs (Critical for Acquisition)**

- [ ] Minimum 2 in-content CTAs using `> [!CTA_*]` markers
- [ ] First CTA placed after hook/context section (25% mark)
- [ ] Second CTA placed mid-article after key insight (50% mark)
- [ ] CTAs placed AFTER providing value, not before
- [ ] CTA types match content context (DEMO after visuals, TRY after concepts)

**Final**

- [ ] `yarn verify` passes

## Existing Posts Reference

| Slug                                          | Topic                      | Category    | Keywords Covered                           |
| --------------------------------------------- | -------------------------- | ----------- | ------------------------------------------ |
| ai-image-enhancement-ecommerce-guide          | E-commerce AI enhancement  | E-commerce  | AI enhancement, product photos, conversion |
| best-free-image-upscalers-comparison          | Free tool comparison       | Comparisons | free upscaler, comparison, reviews         |
| how-to-upscale-images-without-losing-quality  | Quality upscaling tutorial | Tutorials   | upscale, quality, AI upscaling             |
| keep-text-sharp-when-upscaling-product-photos | Text preservation          | Tutorials   | text preservation, product labels          |

## Topic Ideas (Uncovered Keywords)

High-priority topics not yet covered:

1. **Old Photo Restoration** - "restore old photos ai", "old photo enhancer"
2. **Social Media Optimization** - "instagram image size", "facebook photo dimensions"
3. **Print Preparation** - "image resolution for printing", "DPI for print"
4. **Batch Processing** - "bulk image upscaler", "batch photo enhancement"
5. **Format Conversion** - "png vs jpg quality", "best image format"
6. **Wallpaper/4K Content** - "upscale to 4k", "wallpaper upscaler"
7. **Photo Enlargement** - "enlarge photo without blur", "photo enlarger"

## File Naming Convention

```
kebab-case-with-primary-keyword.mdx

Examples:
✅ restore-old-photos-ai-enhancement.mdx
✅ social-media-image-sizes-2024.mdx
❌ OldPhotoRestore.mdx (wrong case)
❌ photo_restore.mdx (underscores)
```
