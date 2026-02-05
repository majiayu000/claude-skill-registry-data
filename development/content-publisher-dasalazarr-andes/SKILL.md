---
name: content-publisher
description: Handles the publication workflow for AndesRC blog articles. Creates markdown files, triggers builds, submits to Google Search Console, and initiates promotion. Use as the final step in the content pipeline.
metadata:
  author: AndesRC
  version: "1.0"
---

# Content Publisher

## Purpose
Execute the final publication workflow: file creation, build verification, search engine submission, and social promotion.

## Publication Workflow

### Step 1: File Creation

**Directory Structure:**
```
src/features/blog/content/
├── en/
│   └── {slug}.md
└── es/
    └── {slug}.md
```

**Filename Convention:**
- Use the `slug` from frontmatter
- Lowercase, hyphen-separated
- Example: `plan-10k-principiantes.md`

### Step 2: Asset Preparation

**Cover Image:**
- Format: WebP (with JPG fallback)
- Dimensions: 1200x630 (16:9 ratio, OG-optimized)
- Size: <150KB
- Location: `public/images/blog/{slug}/cover.webp`

**Inline Images (if any):**
- Location: `public/images/blog/{slug}/`
- Alt text: Include keyword naturally

### Step 3: Build Verification

```bash
# Run local build to verify no errors
npm run build

# Check for:
# - Markdown parsing errors
# - Missing images
# - Broken internal links
```

### Step 4: Deploy

```bash
# Commit and push to trigger Netlify deploy
git add .
git commit -m "blog: add {slug} article"
git push origin main
```

### Step 5: Search Engine Submission

**Google Search Console:**
1. Go to GSC → URL Inspection
2. Enter the new article URL
3. Request indexing

**Sitemap:**
- Verify `sitemap.xml` includes new URL (auto-generated on build)

### Step 6: Social Promotion

**Prepare snippets for:**

**Twitter/X:**
```
🏃 Nuevo artículo: [Título]

[Hook de 1 línea]

[Link]

#running #runners #correr
```

**LinkedIn:**
```
[Título del artículo]

[Párrafo de contexto - por qué es relevante]

Lee más: [Link]
```

**WhatsApp Status:**
- Use cover image
- Short caption: "[Título] - ¡Nuevo en el blog!"

### Step 7: Monitoring Setup

**Add to tracking:**
- [ ] Google Analytics goal/event for the page
- [ ] GSC performance tracking
- [ ] CTA click tracking

## Quality Checklist

### Pre-Publish
- [ ] Frontmatter complete and valid
- [ ] Cover image optimized and in place
- [ ] All internal links work
- [ ] Schema.org markup validated (schema.org validator)
- [ ] Spelling/grammar checked
- [ ] Preview on mobile

### Post-Publish
- [ ] URL accessible and rendering correctly
- [ ] GSC indexing requested
- [ ] Social posts scheduled/published
- [ ] Added to internal tracking sheet

## Output

A published, indexed, and promoted article with:
1. Live URL on andesrunners.com
2. GSC indexing requested
3. Social promotion initiated
4. Performance tracking enabled
