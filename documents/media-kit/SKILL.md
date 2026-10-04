---
name: media-kit
description: Build a speaker media kit — bio writing, photo prep, and page generation for event organizers. Use when preparing speaker bios, headshots, or a press/media page.
user-invocable: true
argument-hint: Optional path to existing headshot photo
metadata:
  version: "1.0.0"
---

# Media Kit Builder

Build a complete speaker media kit from scratch — bios, headshots, and a ready-to-publish page that event organizers can use directly.

## When to Use

- User wants to create a speaker media kit
- User is preparing for speaking engagements or conferences
- User needs professional bios at different lengths
- User needs headshots cropped and formatted for events
- User has a photo but doesn't know what sizes/formats organizers need

## What You'll Produce

1. **Bio variants** — one-liner, short (~50 words), medium (~100 words), long (~200 words)
2. **Photo assets** — headshot (square), headshot (wide), portrait, each with transparent background variant
3. **Media kit page** — HTML/framework page with copy buttons and download links
4. **Markdown kit** — plain text version for email/docs
5. **Downloadable zip** — all assets bundled for organizers

---

## Phase 1: Collect Information

Interview the user. Batch 2-3 questions per round. Don't proceed until you have enough to write bios.

### Round 1: Identity

- Full name (as it should appear on event materials)
- Current title and company
- Contact email for event organizers

### Round 2: Background

- What did you do before your current role? (companies, roles, duration — but we won't use exact years in the bio)
- Education (degree, institution)
- Any notable affiliations (podcasts, open-source orgs, advisory roles)

### Round 3: Positioning

- In one sentence, what do you do now? (This becomes the core of every bio variant.)
- What are 2-3 current projects you want highlighted?
- What topics can you speak on? (List 3-5)

### Round 4: Links

- Personal website
- LinkedIn
- Twitter/X
- GitHub
- Any other relevant links (podcast, company site, project sites)

---

## Phase 2: Write Bios

Write all four variants and present them together for review. Each variant builds on the previous.

### Bio Principles

- **No year counts** — say "enterprise architecture background" not "12 years of enterprise architecture." Years date quickly and create update debt.
- **Name companies, not durations** — "at Informatica and Dun & Bradstreet" not "over a decade in data management"
- **Lead with current work** — what you're building now, not where you came from
- **Spell out abbreviations** — "Hong Kong" not "HK" in bios that organizers will copy verbatim
- **End with education** — it's credential, not headline

### One-liner (~20 words)

For speaker grids, name badges, social bios.

**Pattern:** `[Title], [Company]. [Core positioning statement].`

Example: *CTO & Founder, Digital Rain Technologies. Enterprise architecture background (Informatica, Dun & Bradstreet), now building systems that reason — across culture, operations, and enterprise governance.*

### Short (~50 words)

For event programs, conference apps.

**Pattern:** `[Full name] is the [title] of [company]. [Background]. [Current work]. [Notable affiliation]. [Education].`

### Medium (~100 words)

For panel introductions, press releases.

**Pattern:** `[Full name] is the [title] of [company], where [current work — expanded]. [Background with company names and scope].`

Second paragraph: `[Current projects with one-line descriptions]. [Affiliation]. [Education].`

### Long (~200 words)

For detailed press kits, conference bios.

**Pattern:** First paragraph from medium bio. Then one paragraph per notable project with concrete details. Close with affiliation and education.

### Review Checkpoint

Present all four bios. Ask user to review for:
- Factual accuracy
- Tone (too formal? too casual?)
- Anything missing or to remove

Iterate until approved.

---

## Phase 3: Photo Prep

This is where most people get stuck. Walk through each step.

### What Organizers Need

| Asset | Dimensions | Format | Use Case |
|-------|-----------|--------|----------|
| Headshot (square) | 800x800 | PNG | Avatars, thumbnails, small speaker grids |
| Headshot (wide) | 1170x1170 | PNG | Speaker grids, social media, event programs |
| Portrait | ~1200x1800 | JPEG | Event banners, press, print materials |
| All above + transparent | Same | PNG | Composite graphics, stage screens |

The difference between "square" and "wide" is zoom level, not aspect ratio:
- **Square**: tight face crop
- **Wide**: head and shoulders, more breathing room

### Step 1: Start from the best photo

Ask the user:
- Do you have a professional headshot? If so, what's the file path?
- If not, what's the best photo you have? (Even a phone photo works as a starting point.)

### Step 2: Crop variants

Use `sips` (macOS) for resizing and cropping:

```bash
# Resize to target dimensions (preserving aspect ratio)
sips --resampleWidth 800 input.png --out headshot_square.png

# Crop to exact square (centers the crop)
sips --cropToHeightWidth 800 800 headshot_square.png

# For wide variant (more context around face)
sips --resampleWidth 1170 input.png --out headshot_wide.png
sips --cropToHeightWidth 1170 1170 headshot_wide.png
```

If the source image needs manual framing guidance, tell the user:
- Face should be in the upper third
- Leave roughly equal space on each side of the head
- For "wide" variant, include shoulders

### Step 3: Fix rotation (if needed)

Photos from phones often have EXIF rotation metadata that displays correctly in Preview but not on the web. Fix with `sips`:

```bash
# Check current rotation
sips --getProperty orientation input.jpg

# Rotate to straighten (supports any degree value, not just 90/180/270)
# e.g. 4 degrees to fix a slight tilt
sips --rotate 4 input.jpg --out input_rotated.jpg
```

**White corner artifacts:** Small-degree rotations (like straightening a tilted photo by 4 degrees) fill the canvas corners with white triangles. Crop inward to remove them:

```bash
# Check dimensions after rotation
sips --getProperty pixelWidth --getProperty pixelHeight input_rotated.jpg

# Crop inward to remove white corners
# A 4-degree rotation on a 1410x2006 image needs ~100px trimmed per side
# 1410x2006 → crop to 1210x1806
sips --cropToHeightWidth 1806 1210 input_rotated.jpg --out input_fixed.jpg
```

The amount to crop depends on the rotation angle — larger angles need more trimming. Verify by reading the image file. White corners are easy to miss on white backgrounds but show up immediately on event slides, banners, and transparent composites.

### Step 4: Remove backgrounds

Install `rembg` if not available:

```bash
which rembg || pip install rembg
```

Generate transparent variants:

```bash
rembg i headshot_square.png headshot_square_transparent.png
rembg i headshot_wide.png headshot_wide_transparent.png
rembg i portrait.jpg portrait_transparent.png
```

`rembg` uses the U2-Net model locally — no upload to external services. First run downloads the model (~170MB).

If `rembg` is not available and user can't install it:
- macOS Preview: Open image > Markup toolbar > Instant Alpha (click background, delete)
- Last resort: remove.bg (uploads to external service)

### Step 5: Verify outputs

For each generated image:
1. Check dimensions with `sips --getProperty pixelWidth --getProperty pixelHeight [file]`
2. Read transparent versions to visually verify clean edges
3. Check file sizes are reasonable (under 2MB per image)

Present a summary table of all generated assets with dimensions and file sizes.

---

## Phase 4: Generate the Page

Ask the user what framework they're using:

### Option A: Next.js (App Router)

Generate:
- `app/media-kit/page.tsx` — full media kit page with copy buttons
- `app/media-kit/CopyButton.tsx` — client component for copying bios

The page should include:
- Download button for zip bundle
- Quick reference (name, title, company, contact, LinkedIn)
- All bio variants with copy-to-clipboard buttons
- Photo grid with thumbnails and download links
- Links section

### Option B: Static HTML

Generate a single `media-kit.html` with inline styles and vanilla JS copy buttons.

### Option C: Markdown only

Generate `media-kit.md` with all bios, photo table, and links. No page generation.

### In all cases, also generate:

- `media-kit.md` — plain text version for email/docs/LLMs
- Photo assets organized in a clear folder structure

---

## Phase 5: Bundle

### Naming Convention

Use a personal identifier (e.g. GitHub handle) in both the **zip filename** and the **top-level folder inside the zip** so recipients can distinguish it from other media kits:

- Zip file: `[handle]-media-kit.zip` (e.g. `augchan42-media-kit.zip`)
- Extracts to: `[handle]-media-kit/` (e.g. `augchan42-media-kit/`)

Never use a generic name like `media-kit.zip` — organizers juggle kits from many speakers.

### Create the zip

```bash
# Organize assets under the named folder, then zip it
zip -r [handle]-media-kit.zip [handle]-media-kit/
```

The folder should contain:

```
[handle]-media-kit/
├── media-kit.md
├── headshots/
│   ├── [name]_headshot_square.png
│   ├── [name]_headshot_square_transparent.png
│   ├── [name]_headshot_wide.png
│   └── [name]_headshot_wide_transparent.png
└── portraits/
    ├── [name]_portrait.jpeg
    └── [name]_portrait_transparent.png
```

Report final zip size.

---

## Phase 6: Quality Check

Before finishing, verify:

- [ ] All four bio variants are factually consistent
- [ ] No year counts in any bio
- [ ] All abbreviations spelled out
- [ ] Photo dimensions match the spec table
- [ ] Transparent versions have clean edges
- [ ] Copy buttons work (if page was generated)
- [ ] Download links point to correct files
- [ ] Zip contains all assets
- [ ] Markdown version matches page version

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using exact year counts ("12 years at...") | Use "background at [Company]" — years create update debt |
| Only providing one headshot size | Organizers need square (avatars) AND wide (speaker grids) |
| No transparent background versions | Event designers need these for composite graphics and stage screens |
| Abbreviations in bios ("HK", "SF") | Spell out — organizers copy these verbatim |
| Bios that start with background, not current work | Lead with what you're doing now |
| No plain text version | Many organizers work in email/docs, not your website |
| Inconsistent facts across bio lengths | Write shortest first, then expand — never contradict |
