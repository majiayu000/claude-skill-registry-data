---
name: site-phase-4
description: Phase 4 of build-site — Doc research results + React project scaffold
allowed-tools: Read, Write, Edit, Bash
model: sonnet
effort: medium
context: fork
user-invocable: false
---

# Phase 4 — Docs + Scaffold

## Objective

Use doc research results from the orchestrator to scaffold a complete React project with correct dependencies, config files, downloaded images, and design tokens — ready for component implementation in Phase 5.

---

## Step 1 — Use doc research results

The orchestrator launched a research agent for the top libraries. Apply the pitfalls found.

For known pitfalls and version-specific issues:
> `Read: sites/_templates/package-libs.md` (section "Known Pitfalls" + "Lenis Parameters")

---

## Step 2 — Create directories

```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2
LEAD_ID="SLUG_DO_LEAD"
mkdir -p sites/$LEAD_ID/public/images/stock
mkdir -p sites/$LEAD_ID/src/{components/{layout,seo,ui,sections},pages,hooks,i18n,data,design-system}
mkdir -p sites/$LEAD_ID/screenshots
```

---

## Step 3 — Generate package.json

**Do NOT copy blindly.** Build package.json based on the Phase 3 creative concept.

For required dependencies, devDependencies, animation lib mapping, and conditional packages:
> `Read: sites/_templates/package-libs.md`

Key rules:
- If multi-page (Phase 2.6): add `react-router-dom`
- Always include Radix UI for accessible components
- Add `@fontsource/` packages from Phase 3 fonts
- Animation libs: derive ONLY from blueprint — if blueprint doesn't mention it, do NOT include it

---

## Step 4 — Install

```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2/sites/$LEAD_ID && npm install
```

---

## Step 5 — Generate config files

### vite.config.js

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
export default defineConfig({ plugins: [react(), tailwindcss()], server: { port: 5173 } })
```

### index.html (full SEO)

Include directly: optimized `<title>`, `<meta description>` 150-160 chars, Open Graph complete (og:title, og:description, og:image REAL, og:url, og:type, og:locale pt_BR), Twitter Card, canonical, hreflang pt-BR and en, favicon.

---

## Step 6 — Download ALL images AND videos AND build MANIFEST.json

**CRITICAL:** the goal of this step is not just downloading files. It is producing `sites/$LEAD_ID/public/images/MANIFEST.json` — the SEMANTIC source of truth that Phase 6 uses to map images to sections. Without MANIFEST.json, Phase 6 falls back to filename heuristics and 60%+ of images become orphans (verified in barbeariaancorador-v3 audit).

For the complete image analysis methodology (video filter, per-image analysis, coherence rules):
> `Read: sites/_templates/image-analysis-guide.md`

### A0) Priority user images (if provided by orchestrator)

If the orchestrator included URLs labeled "PRIORITY IMAGES" or "professional images":
1. Navigate with Playwright (`browser_navigate`) to each URL
2. Instagram post (`/p/`): extract og:image with `browser_evaluate`
3. Instagram Reel (`/reel/`): do NOT use og:image (play button overlay) — try carousel extraction or discard
4. Download with curl and validate
5. Place in the MOST prominent positions: Hero and About

### A) Real images from briefing (data_points category "images")

For each image URL, try in order:
1. **curl direct**: `curl -sfL -o sites/$LEAD_ID/public/images/DESCRIPTIVE-NAME.jpg "URL"`
2. **If curl failed or file < 5KB** (CDN/Instagram URLs expire): navigate with Playwright, extract og:image, download
3. **Validate**: file must be > 5KB. Under 5KB = thumbnail or error — discard and retry

Name descriptively: `portrait-dra-ariel.jpg`, `logo-usina.png`, `hamburguer-classico.jpg`.

**MANDATORY — analyze each image inline, AS SOON AS it is downloaded.** Never defer analysis to a batch step at the end. The download → analyze pair is atomic. Skipping the analyze half breaks Phase 6's semantic mapping.

For each newly downloaded image file:
1. Confirm file exists and > 5KB
2. **Read: sites/$LEAD_ID/public/images/{filename}** — Claude opens the image visually
3. Append a manifest entry to `sites/$LEAD_ID/public/images/MANIFEST.json` with the schema below (Step 6.5). Do NOT proceed to the next download until this entry is written.

This inline pattern is REQUIRED by the user. Batch-after-download has been tried and fails because the agent forgets which images it already processed when iterating dozens of files.

### A1) Brand logo (MANDATORY)

The actual brand logo (PNG/SVG/WebP) must be downloaded if available. Profile pictures from Instagram are NOT a substitute. Try in order:

1. Check `data_points` from enrich-phase-6 for `tipo: "logo"` → download to `public/images/brand-logo.png`
2. If only `tipo: "profile_pic"` exists AND it visually IS the logo (single emblem on solid background, not a person photo), use it as fallback → save as `brand-logo.png`
3. WebSearch: `"{brand_name}" logo png` and `"{brand_name}" logo svg site:instagram.com OR site:twitter.com` — if a clean version surfaces, download it
4. Mark `logo_real_present: true|false` in the MANIFEST.json from Step 6.5

### A2) Videos from enrich-phase-6 (with poster-frame analysis)

If `data/enrichment/{slug}/videos/` exists with reel_*.mp4 files, copy them to the build AND analyze each one inline.

**For each video, the analysis loop is:**

1. Copy MP4 to `sites/$LEAD_ID/public/videos/{filename}`
2. Extract poster frame (1.5s into the video) via ffmpeg:
   ```bash
   ffmpeg -y -i sites/$LEAD_ID/public/videos/{file}.mp4 -ss 00:00:01.5 -vframes 1 -q:v 2 sites/$LEAD_ID/public/images/poster-{file}.jpg
   ```
3. **Read: sites/$LEAD_ID/public/images/poster-{file}.jpg** — Claude opens the still frame visually
4. **Read: data/enrichment/{slug}/captions.json** (if exists) — find the caption matching this reel's shortcode
5. Compose a manifest entry combining what you SEE in the poster + what the caption SAYS:
   ```json
   {
     "file": "videos/reel_ABC123.mp4",
     "poster_file": "images/poster-reel_ABC123.jpg",
     "content_type": "video_reel",
     "subjects": [...what is visually in the poster...],
     "caption_excerpt": "...first 200 chars of Instagram caption...",
     "duration_seconds": 12,
     "quality_assessment": "1080p, sharp, well-lit, professional|amateur",
     "tone": "warm|cool|neutral",
     "shows_action": true,
     "shows_people": true,
     "people_count": 2,
     "fingerprint_summary": "1-2 sentence description of what the video shows AND what the caption says",
     "recommended_sections": ["s1_background", "s3_demo"],
     "do_not_use_for": ["formal portrait section"],
     "is_safe_for_autoplay_loop": true
   }
   ```
6. Append entry to MANIFEST.json
7. Move to next video — never batch

```bash
mkdir -p sites/$LEAD_ID/public/videos
SLUG=$(echo "$LEAD_ID" | sed 's/-v[0-9]*$//')
ENRICH_VID="data/enrichment/$SLUG/videos"
[ -d "$ENRICH_VID" ] && ls "$ENRICH_VID"/reel_*.mp4 2>/dev/null | head -5 | xargs -I {} cp {} sites/$LEAD_ID/public/videos/
ls sites/$LEAD_ID/public/videos/ 2>/dev/null
```

After copying, run the per-video analyze loop above for EACH file. Do NOT skip videos that look low-quality at first glance — let the manifest record the quality assessment, and Phase 6 decides whether to use the video or only its poster.

### B) Stock images from Phase 3.4

```bash
curl -sL -o sites/$LEAD_ID/public/images/stock/NAME.jpg "URL"
```

Only for backgrounds/textures/atmosphere. NEVER for people, locations, products, or team.

### C) Additional images during build (Phase 6)

Use image MCPs: `mcp__stock-images`, `mcp__mcp-pexels`, `mcp__pixabay`, `mcp__freepik`.
Rule: "could this image deceive the visitor?" If yes, do NOT use.

---

## Step 6.5 — `public/images/MANIFEST.json` (the contract for Phase 6)

By the time you reach this step, MANIFEST.json should ALREADY exist (built incrementally inline during downloads in Step 6 A0/A/A2). This step is the FINAL validation + schema completion.

### Schema (REQUIRED for every image and video entry)

```json
{
  "version": 1,
  "lead_id": "{lead_id}",
  "generated_at": "ISO8601",
  "vision_analyzer": "claude-via-read-tool",
  "logo_real_present": true,
  "total_images": N,
  "total_videos": M,
  "entries": [
    {
      "file": "portrait-bruno.jpg",
      "kind": "image",
      "size_kb": 142,
      "dimensions": "1080x1080",
      "content_type": "portrait",
      "subjects": ["barber", "man", "shop interior background"],
      "people_count": 1,
      "tone": "warm",
      "lighting": "natural window light",
      "color_palette": ["#3a2515", "#a08050"],
      "is_logo_or_brand_mark": false,
      "looks_professional": true,
      "looks_staged_or_candid": "candid",
      "quality_assessment": "high — sharp focus, good exposure, framed for use",
      "fingerprint_summary": "Bruno Sucata in his barbershop, looking at camera, warm afternoon light",
      "recommended_sections": ["s2"],
      "do_not_use_for": ["s4 community", "s3 process — no action shown"]
    },
    {
      "file": "videos/reel_ABC123.mp4",
      "poster_file": "images/poster-reel_ABC123.jpg",
      "kind": "video",
      "duration_seconds": 12,
      "content_type": "video_reel",
      "shows_action": true,
      "people_count": 2,
      "caption_excerpt": "Hoje o Tyson decidiu ajudar...",
      "quality_assessment": "1080p, sharp, ambient sound, professional handheld",
      "tone": "warm",
      "fingerprint_summary": "Bruno cutting a client's hair while the dog Tyson sits on his lap, slow-motion",
      "recommended_sections": ["s3_process_demo"],
      "do_not_use_for": ["s5 contact"],
      "is_safe_for_autoplay_loop": true
    }
  ]
}
```

### Mandatory fields per entry

- `file` (basename, relative to `public/images/` for images or `public/videos/` for videos)
- `kind`: `"image"` | `"video"`
- `content_type`: one of: `interior_atmospheric | portrait | process_at_work | community_group | product | texture | logo | exterior | video_reel | other`
- `subjects`: array of nouns describing what is actually in the frame
- `people_count`: 0+
- `tone`: `warm | cool | neutral | mixed`
- `quality_assessment`: 1-2 sentences on resolution, sharpness, lighting, professional/amateur — the user explicitly requested this
- `fingerprint_summary`: 1-2 plain sentences on what the image/video actually shows (not what it's named)
- `recommended_sections`: array of slugs `s1` through `s5` (or `s1_background`, `s3_demo`, etc. for sub-roles)
- `do_not_use_for`: array of contexts where this asset is wrong

### Rules

- Tagging is based on what Claude SEES via the Read tool, not on filename guesses. A `logo-bruno.jpg` that visually shows a man's face is `content_type: "portrait"`, NOT `"logo"`.
- The `quality_assessment` field is REQUIRED — the user explicitly requested it. Sites must reject low-quality assets at Phase 6 if a higher-quality alternative exists.
- For images that came from `enrich-phase-6` with vision tags already, REUSE the tags but VERIFY by re-Reading the file (the file may have been transformed during copy or the original tagging may be stale).
- For images analyzed in Phase 4 (legacy lead with no enrichment manifest), ALWAYS Read each one — do not trust the filename.

---

## Step 7 — Generate tokens.css + index.css

### tokens.css

Generate with hex colors and fonts from Phase 3 design system.

### index.css

```css
@import "tailwindcss";
@import "./design-system/tokens.css";
/* Tailwind v4 already includes Preflight. Do NOT use * { margin:0; padding:0 } */
*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: auto; }
body { font-family: var(--font-body); color: var(--color-text-primary); background: var(--color-background); -webkit-font-smoothing: antialiased; }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; } }
```

---

## Verification

List to the user: each image downloaded, what it contains, where it will be used, and which were discarded (with reason).

---

## Exit Gate (blocking)

```bash
.claude/scripts/gate-images.sh $LEAD_ID
.claude/scripts/gate-image-manifest.sh $LEAD_ID
```

If `gate-images.sh` fails: go back to Step 6 (download). CDN images (Instagram/scontent) can expire — if curl fails, use Playwright to re-capture.

If `gate-image-manifest.sh` fails: MANIFEST.json is missing or invalid — go back to Step 6.5 and generate it. The manifest is the contract for Phase 6 image-to-section semantic mapping. Without it, Phase 6 will produce a build with orphan images and section/image mismatches.

---

## Constraints

| Constraint | Enforced by |
|---|---|
| Animation libs only from blueprint | Phase 3 blueprint review |
| No `* { padding: 0 }` with Tailwind v4 | gate-quality-loop.sh (Phase 7) |
| Images > 5KB each | gate-images.sh |
| At least 1 real client image | gate-images.sh |
| Video thumbnails discarded | Image analysis guide (manual) |
| Image-section coherence | Image analysis guide (manual) |
| Lenis params from concept (not default) | package-libs.md rules |

---

## Exit Criteria

- [ ] `sites/$LEAD_ID/node_modules/.package-lock.json` exists
- [ ] Images downloaded in `sites/$LEAD_ID/public/images/` (gate passed)
- [ ] Videos copied to `sites/$LEAD_ID/public/videos/` if enrichment had reels
- [ ] `sites/$LEAD_ID/public/images/MANIFEST.json` exists with valid entries (gate-image-manifest passed)
- [ ] Brand logo file present at `public/images/brand-logo.*` OR MANIFEST.json declares `logo_real_available: false`
- [ ] `tokens.css`, `index.css`, `vite.config.js`, `index.html` generated
- [ ] Each image visually analyzed via Read tool (NOT filename heuristic)
- [ ] gate-images.sh exited 0
- [ ] gate-image-manifest.sh exited 0
