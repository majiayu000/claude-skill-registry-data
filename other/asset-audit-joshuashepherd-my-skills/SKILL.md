---
name: asset-audit
description: Audit image assets across the project to find missing, broken, or mismatched images — trigger phrases include "audit images", "find missing images", "check image slots", "which images are missing", or "image inventory".
---

Match available images to image slots across the project: $ARGUMENTS

$ARGUMENTS should include:
- Optionally: a scope to audit (`all`, `heroes`, `courses`, `books`, `pathways`, `portals`, `pages`, `og`, `cards`)
- Optionally: a specific page or component path to check
- Optionally: `--fix` to generate Gemini prompts for missing assets
- Empty — audit all image slots across the entire project

## Image Inventory

### Directory Structure
All local images live under `public/`:

| Directory | Purpose | Naming Convention |
|-----------|---------|-------------------|
| `{{IMAGES_DIR}}/art/` | General art, abstract hero art | `art-{description}.webp` |
| `{{IMAGES_DIR}}/art/hero-sections/` | Page hero background art | `art-abstract-{description}.webp` |
| `{{IMAGES_DIR}}/art/hero-sections/pathways/` | Pathway-specific hero art | `art-pathway-{slug}.webp` |
| `{{IMAGES_DIR}}/art/courses/` | Course covers & hero art | `course-{slug}-cover-{breakpoint}.webp`, `art-course-{slug}.webp` |
| `{{IMAGES_DIR}}/art/portals/` | Portal/theme imagery & icons | `art-portal-{slug}.webp`, `portal-{slug}-icon-2x.webp` |
| `{{IMAGES_DIR}}/art/mdna/` | mDNA concept art | `art-abstract-{description}.webp` |
| `{{IMAGES_DIR}}/art/textures/` | Background textures | `art-texture-{description}.webp` |
| `{{IMAGES_DIR}}/books/` | Book cover images | `book-{slug}.webp` + responsive variants |
| `{{IMAGES_DIR}}/orgs/` | Organization logos | `image-{org}-logo.webp` + responsive variants |
| `{{IMAGES_DIR}}/logo/` | Platform logos & signatures | `logo-{variant}.{webp,png}` |
| `public/marks/` | Brand marks | `brand-{name}.{webp,svg}` |
| `public/placeholders/` | Placeholder/fallback images | various |
| `{{OUTPUT_DIR}}/` | AI-generated assets (Gemini) | `{type}/{slug}-{n}.png` |

### Responsive Variants Pattern
Many images have breakpoint variants:
- `{slug}.webp` — base/default
- `{slug}-mobile.webp` — < 768px
- `{slug}-tablet.webp` — 768–1279px
- `{slug}-desktop.webp` — >= 1280px
- `{slug}-2x.webp` — high-DPI / retina

### Remote Storage
Some images resolve via Supabase storage URLs. The `resolveStorageUrl()` utility maps DB `cover_image_url` fields to full Supabase URLs. Check both local paths and DB-stored URLs.

## Image Slots — Where Images Are Needed

### 1. Tenant Config (`{{CONFIG_PATH}}`)
The central config defines image references that cascade across the platform:

| Config Path | Type | Description |
|-------------|------|-------------|
| `logo.imageUrl` | Logo | Platform signature/logo |
| `themes[].coverImage` | Cover | Theme/pathway portal art |
| `hero.backgroundImageUrl` | Hero BG | Home page hero background |
| `courses.items[].imageUrl` | Cover | Course card cover images |
| `email.logoUrl` | Logo | Email template logo |

### 2. Hero Components
| Component | Props | Fallback |
|-----------|-------|----------|
| `HeroSectionVariant` | `backgroundImageUrl`, `imageUrl` | Supabase storage pathway art |
| `PathwayHero` | `heroImage` | None (conditionally rendered) |
| `PathwayMapHero` | `content.heroImage` | None |
| `PathwayGlossaryHero` | `content.heroImage` | None |
| `AILabHero` | Hardcoded `/images/art/ai-lab.webp` | None |

### 3. Content Cards
| Component | Image Prop | Fallback |
|-----------|-----------|----------|
| `ArtCard` | `imageUrl` (required) | None |
| `PortalCard` | `imageUrl` (optional) | None shown |
| `ResourceCard` | `imageUrl` (optional) | None shown |
| `ContentDarkCard` | `item.imageUrl` | None shown |
| `ContentLibraryCard` | `item.imageUrl` | None shown |
| `TrendingBooksCarousel` | `item.imageUrl` | None shown |

### 4. Course Images
| Component | Image Source | Notes |
|-----------|------------|-------|
| `CourseOverviewContent` | `course.coverImageUrl` via `resolveStorageUrl()` | DB-stored |
| `CourseSalesLandingContent` | `coverImageUrl`, `section.imageUrl` | Props |
| Home page course cards | Hardcoded array in `page.tsx` | 3 course cover images |

### 5. Database Image Columns
These tables have image URL columns that should have values:

| Table | Column | Purpose |
|-------|--------|---------|
| `articles` | `author_avatar_url` | Article author photo |
| `profiles` | `avatar_url` | User avatar |
| `organizations` | `background_image_url`, `signature_image_url` | Org branding |
| `courses` | `cover_image_url` | Course card/hero cover |
| `course_lessons` | `cover_image_url` | Lesson cover |
| `pathways` | `cover_image`, `cover_image_fallback` | Pathway card/hero |
| `pathway_sections` | `featured_image_url` | Section feature image |
| `pathway_testimonials` | `testimonial_image_url` | Testimonial photo |
| `books` | `cover_image_url` | Book cover |
| `videos` | `thumbnail_url` | Video thumbnail |
| `video_series` | `cover_image_url` | Series cover |
| `podcast_episodes` | `thumbnail_url` | Episode thumbnail |
| `podcast_series` | `thumbnail_url` | Series cover |
| `assessments` | `cover_image_url` | Assessment cover |
| `certificates` | `certificate_image_url` | Certificate bg |

## Audit Process

### Step 1 — Inventory Available Images
Scan all image directories and build a catalog:

```bash
# List all available images with paths
find public/ -type f \( -name "*.webp" -o -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.svg" -o -name "*.avif" \) | sort
```

Categorize each image by:
- **Type**: hero, cover, icon, logo, texture, portrait, book, org
- **Subject**: what concept/entity it represents (course slug, pathway slug, etc.)
- **Variants**: which breakpoints exist (mobile, tablet, desktop, 2x)

### Step 2 — Scan Image References
Find every place the codebase references an image:

```bash
# Static references in TSX/TS
grep -rn '/images/\|/marks/\|/placeholders/' src/ --include='*.tsx' --include='*.ts'

# Tenant config image references
grep -n 'imageUrl\|coverImage\|heroImage\|backgroundImage' {{CONFIG_PATH}}

# Dynamic image props in components
grep -rn 'imageUrl\|coverImage\|heroImage\|thumbnailUrl\|avatarUrl' {{COMPONENTS_DIR}}/ --include='*.tsx'
```

### Step 3 — Cross-Reference & Report
For each image slot, determine its status:

| Status | Meaning |
|--------|---------|
| MATCHED | An appropriate image exists and is correctly referenced |
| WRONG_FIT | An image is referenced but doesn't match the slot's needs (wrong aspect, wrong subject) |
| PLACEHOLDER | Using a fallback/generic image where a specific one should exist |
| MISSING_FILE | Code references a file path that doesn't exist on disk |
| MISSING_VARIANTS | Base image exists but responsive variants are missing |
| NO_IMAGE | Slot exists but no image is assigned at all |
| DB_EMPTY | Database column for image URL is null/empty for active records |

### Step 4 — Generate Match Report

## Output Format

```
## Image Asset Audit Report

### Summary
| Status | Count |
|--------|-------|
| MATCHED | X |
| WRONG_FIT | X |
| PLACEHOLDER | X |
| MISSING_FILE | X |
| MISSING_VARIANTS | X |
| NO_IMAGE | X |
| DB_EMPTY | X |


### MISSING / NEEDS GENERATION

#### 1. [Slot Name] — [Page/Component]
- **Current state**: [NO_IMAGE / PLACEHOLDER / MISSING_FILE]
- **What's needed**: [description of ideal image]
- **Suggested type**: hero / cover / thumbnail / portrait
- **Suggested aspect ratio**: 16:9 / 3:4 / 1:1
- **Best existing reference**: [path to closest existing image, if any]
- **Recommended skill**: `/asset-generate` | `/asset-hero-portrait` | `/asset-headshot` | `/asset-series`
- **Gemini Prompt** (if `--fix` flag):
  > [Ready-to-use prompt following the Brief Method from /asset-generate]

#### 2. [Next slot...]
...


### BROKEN REFERENCES
| File | Line | Reference | Issue |
|------|------|-----------|-------|
| src/app/(public)/page.tsx | 76 | /images/art/courses/course-{{course-slug}}-cover-desktop.webp | OK |
| ... | ... | ... | ... |

