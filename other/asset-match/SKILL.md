---
name: asset-match
description: Audit where images are needed across the project (heroes, covers, cards, OG images) vs what's available in public/images/. Reports matches, mismatches, missing assets, and broken references. Connects to asset generation skills for creating missing images.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Match available images to image slots across the project: $ARGUMENTS

$ARGUMENTS should include:
- Optionally: a scope to audit (`all`, `heroes`, `courses`, `books`, `pathways`, `portals`, `pages`, `og`, `cards`)
- Optionally: a specific page or component path to check
- Optionally: `--fix` to generate NB2 prompts for missing assets
- Empty — audit all image slots across the entire project

## Image Inventory

### Directory Structure
All local images live under `public/`:

| Directory | Purpose | Naming Convention |
|-----------|---------|-------------------|
| `public/images/art/` | General art, abstract hero art | `art-{description}.webp` |
| `public/images/art/hero-sections/` | Page hero background art | `art-abstract-{description}.webp` |
| `public/images/art/hero-sections/pathways/` | Pathway-specific hero art | `art-pathway-{slug}.webp` |
| `public/images/art/courses/` | Course covers & hero art | `course-{slug}-cover-{breakpoint}.webp`, `art-course-{slug}.webp` |
| `public/images/art/portals/` | Portal/theme imagery & icons | `art-portal-{slug}.webp`, `portal-{slug}-icon-2x.webp` |
| `public/images/art/mdna/` | mDNA concept art | `art-abstract-{description}.webp` |
| `public/images/art/textures/` | Background textures | `art-texture-{description}.webp` |
| `public/images/books/` | Book cover images | `book-{slug}.webp` + responsive variants |
| `public/images/orgs/` | Organization logos | `image-{org}-logo.webp` + responsive variants |
| `public/images/logo/` | Platform logos & signatures | `logo-{variant}.{webp,png}` |
| `public/marks/` | Brand marks | `brand-{name}.{webp,svg}` |
| `public/placeholders/` | Placeholder/fallback images | various |
| `public/images/generated/` | AI-generated assets (NB2) | `{type}/{slug}-{n}.png` |

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

### 1. Tenant Config (`src/lib/config/tenant.config.ts`)
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
grep -n 'imageUrl\|coverImage\|heroImage\|backgroundImage' src/lib/config/tenant.config.ts

# Dynamic image props in components
grep -rn 'imageUrl\|coverImage\|heroImage\|thumbnailUrl\|avatarUrl' src/components/ --include='*.tsx'
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

---

### MATCHED (no action needed)
| Slot | Image Path | Notes |
|------|-----------|-------|
| Home hero BG | /images/art/hero-sections/art-abstract-communal-figures-loosely-circling-a-centra.webp | 16:9, warm tones, on-brand |
| AI Lab hero | /images/art/ai-lab.webp | Matches lab theme |
| ... | ... | ... |

---

### MISSING / NEEDS GENERATION

#### 1. [Slot Name] — [Page/Component]
- **Current state**: [NO_IMAGE / PLACEHOLDER / MISSING_FILE]
- **What's needed**: [description of ideal image]
- **Suggested type**: hero / cover / thumbnail / portrait
- **Suggested aspect ratio**: 16:9 / 3:4 / 1:1
- **Best existing reference**: [path to closest existing image, if any]
- **Recommended skill**: `/asset-generate` | `/asset-hero-portrait` | `/asset-headshot` | `/asset-series`
- **NB2 Prompt** (if `--fix` flag):
  > [Ready-to-use prompt following the Brief Method from /asset-generate]

#### 2. [Next slot...]
...

---

### MISSING RESPONSIVE VARIANTS

| Base Image | Missing Variants |
|-----------|-----------------|
| `/images/art/courses/art-course-metanoia-shaping-potter.webp` | mobile, tablet, desktop, 2x |
| ... | ... |

---

### BROKEN REFERENCES
| File | Line | Reference | Issue |
|------|------|-----------|-------|
| src/app/(public)/page.tsx | 76 | /images/art/courses/course-forgotten-ways-cover-desktop.webp | OK |
| ... | ... | ... | ... |

---

### RECOMMENDATIONS

1. **Quick wins** — Images that exist but aren't being used where they should be
2. **Batch generation** — Groups of similar missing assets that can use `/asset-series`
3. **Priority gaps** — High-visibility slots (home hero, course covers) without proper images

### Generation Plan
For missing assets, the recommended approach:
1. Use `/asset-series` for batches of similar assets (e.g., all missing course covers)
2. Use `/asset-hero-portrait` for author-featuring hero images
3. Use `/asset-generate` for individual standalone assets
4. Use `/asset-headshot` for avatar/profile photos
5. Run `/asset-brand-check` on all generated assets before publishing
```

## Scope Filters

When `$ARGUMENTS` specifies a scope, only audit that subset:

- **`heroes`** — Hero components + hero background images + tenant hero config
- **`courses`** — Course cover images (DB + config + components)
- **`books`** — Book cover images (DB + local files)
- **`pathways`** — Pathway cover images, hero images, portal cards
- **`portals`** — Theme/portal card images in tenant config
- **`pages`** — Static image references in page files (`src/app/(public)/`)
- **`og`** — Open Graph / social card images
- **`cards`** — Card component image props and their data sources

## Connecting to Generation Skills

When missing assets are identified, recommend the right generation skill based on the slot type:

| Slot Type | Recommended Skill | Why |
|-----------|------------------|-----|
| Page hero background | `/asset-generate` (type: hero) | Abstract art, no person needed |
| Author hero portrait | `/asset-hero-portrait` | Needs existing photo as input |
| Course cover | `/asset-generate` (type: cover-course) | Thematic art for course topic |
| Book cover | `/asset-generate` (type: cover-book) | 3:4 book cover art |
| Profile avatar | `/asset-headshot` | Needs existing photo as input |
| Multiple similar covers | `/asset-series` | Batch with visual continuity |
| OG / social cards | `/asset-text-overlay` | Needs text rendered on image |
| Product mockup | `/asset-product-shot` | Book or course material shot |

When using `--fix`, generate ready-to-use NB2 prompts following the Brief Method from `/asset-generate`, incorporating brand context (warm earth tones, charcoal textures, scholarly/missional mood).

## DB Audit (Optional — requires Supabase access)

If Supabase is accessible, check for empty image columns on active records:

```sql
-- Courses without cover images
SELECT id, title, slug FROM courses WHERE cover_image_url IS NULL AND status = 'published';

-- Books without covers
SELECT id, title, slug FROM books WHERE cover_image_url IS NULL;

-- Pathways without hero images
SELECT id, title, slug FROM pathways WHERE cover_image IS NULL;

-- Videos without thumbnails
SELECT id, title FROM videos WHERE thumbnail_url IS NULL;
```

Report these as `DB_EMPTY` entries with recommendations to either:
1. Upload existing local images to Supabase storage and update the DB
2. Generate new assets and upload them
