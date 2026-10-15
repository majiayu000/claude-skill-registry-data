---
name: "che-social-ui-designer"
description: "V4 — Backend-neutral design pipeline with 4 modes: (A) Social Media, (B) UI/UX Feature, (C) Design System, (D) Logo & Branding. Mandatory SPEC approval gate, staged execution ≤5 stages, visual review per stage. Supports capability-selected OpenPencil, Figma or spec-only execution. Trigger: /che-design, /che-figma."
---

# Che — Social UI Designer (Orchestrator) v4.0

> **SHARED REFERENCES (CANONICAL — DO NOT DUPLICATE body):**
> - **Formatting + verbosity ≤500w**: engineering-contracts §18 (subheadings ## / ###, bullets ≤2 lines, bold keywords)
> - **Hard-won session lessons** (offline composition / template text nodes / unique colors validation): §3 below
> - **Design tokens + Tailwind**: engineering-contracts skill (DS section)
> - **Image source fallback waterfall**: §3 item #1 (Real Unsplash > text_to_image endpoint > headless G(search))
> - **SVG vector quality gates**: §12 logo/branding

This is the **top-level orchestrator skill** for che design. The workflow is backend-neutral.
Backend selection MUST follow `references/DESIGN_BACKEND_CONTRACT.md`.
OpenPencil-specific instructions apply ONLY when backend=`openpencil`.
Figma execution follows `references/backends/FIGMA.md` when backend=`figma`.
Never select a backend only because the runtime is Trae or Codex.
Backend default fallback = local `mcp_open-pencil` (equivalent to Figma desktop, without auth/limits).

### Design source bootstrap

Before the design SPEC gate, capture optional `source_ref` and `requested_backend`, then resolve the complete `design_source` object through `references/DESIGN_BACKEND_CONTRACT.md`. Classification precedes capability validation. Do not call either backend while `effective_backend=none`.

If routing fails closed, report `source_kind`, `capability_status`, and `reason` plus the supported input forms. Stop before design execution. Never convert a Figma source to OpenPencil or an OpenPencil source to Figma.

### Runtime bootstrap

Before creating any durable design artifact:

```bash
python3 -m che_core.designer bootstrap "$WORKTREE_ROOT" "$SESSION_ID" "<mode>" "<slug>"
```

Create `$CHE_DESIGN_DIR` only after the bound-worktree/session preflight passes.
**4 mutually exclusive modes** (choose 1 at start via `AskUserQuestion`):
- **MODE A → Social Media Posts**: 1:1 posts / 9:16 stories + professional copy.
- **MODE B → UI/UX Feature**: wireframes → hi-fi → dev-spec (React/Tailwind 4).
- **MODE C → Design System**: Tailwind 4 tokens ↔ OpenPencil variables + atomic components.
- **MODE D → Logo & Branding**: deep brand discovery → brand briefing → logo concepts → vector refinement → full brandbook (SVG mandatory).

---

## 🔴 0. NON-NEGOTIABLE GATES (execute IN ORDER — failure = STOP)

### GATE -1 (HARD — DOES NOT pass WITHOUT APPROVAL) → WRITE + ITERATE MANDATORY UI/POST SPEC
> **Hard rule:** *No pixels are drawn, no images downloaded, no stages executed until the user explicitly responds "I approve the spec" to a structured document.*
>
> 2 rounds of spec adjustment still ambiguous → offer defaults in 1 line (§7 fail-fast).

#### 0.1 Write complete spec (use §9 TEMPLATE below as base)
Spec must have **ALL** these fields filled, per piece/screen:

When a design source was supplied, include a `Design Source` section with `source_ref`, `source_kind`, `requested_backend`, `effective_backend`, `capability_status`, and the fail-closed `reason` when present. Add Figma file key/page/node or OpenPencil identifiers only when the active driver exposes them.

| Field (per piece) | Example description (MODE A Post 1:1) |
|---|---|
| **ID / Piece Name** | `C1-COVER`, `C2-MENU` |
| **Piece Goal** | Initial hook, profile traffic |
| **Verbatim Copy (not a single char can change)** | Headline / Subline / Body / CTA (max wordcount per line) |
| **Hex Palette (exact, per piece)** | bg=#FFF7ED | headline=#C2410C | cta=#EA580C | text=#292524 |
| **Base dimension + export scale** | 1080×1080 → scale 2 = 2160×2160 PNG |
| **Layout grid (absolute or relative positions)** | Photo 360×360 x=696 y=540 bottom-right corner; Text block x=72 y=72 w=936 padding=24 |
| **Image (fallback cascade per §3.1)** | (1) Unsplash ID `photo-1586444248902-2f64eddc13df` / (2) stock prompt / (3) text_to_image prompt |
| **Visual aesthetics (per element)** | Photo: radius=28 / white stroke=6 / shadow=4 8 blur14 alpha40; Dark overlay #1C1917 alpha=35% IF photo is warm + white text |
| **Typography (weight/size/leading)** | Headline: Inter Black 72/76; CTA: Inter SemiBold 48/52 |
| **Mandatory WCAG Contrast** | Headline over bg min 4.5:1 body / 3:1 large (explain overlay if needed) |
| **Layer stacking order (INDEX low → high)** | 0=photo → 1=overlay (if any) → 2=headline/subline → 3=CTA button → NEVER photo over text |
| **Expected output** | `FINAL-C1-COVER@2x.png` 2160×2160 |

Extra fields for **MODE B UI screens**: persona, job story, 3 core behaviors max, responsive breakpoints (mobile 375 / tablet 768 / desktop 1280).
Extra fields for **MODE C Design System**: tokens origin (Tailwind 4 config / from scratch), mandatory dark mode, components list (Button/Card/Input/Textarea/Badge/Avatar/Alert/Toggle/Switch/Radio/Checkbox/Select — default 12).
Extra fields for **MODE D Logo & Branding (100% fill MANDATORY)**:
| MODE D Field | Mandatory description |
|---|---|
| **Brand name + slogan (if any)** | Wordmark VERBATIM text; optional slogan. |
| **Core idea / brand positioning** | 1-2 sentences "Brand X is for Y who want Z". |
| **Sector + target audience (min persona)** | E.g.: "Artisanal bakery UK, 25-55 audience, upper-middle class". |
| **Primary palette (brand hex colors)** | 2-5 hex colors (primary / secondary / accent / neutrals). If not defined → discover. |
| **Wordmark + body typography** | Wordmark family (Display) + Body (e.g. Playfair Display Bold 72 / Inter 400). |
| **Brand voice (brand voice doc) + 3 example phrases** | Tone (friendly / premium / minimalist / young / serious) + 3 written communication examples. |
| **References (up to 5)** | (a) Similar site/brand URLs; (b) Attached existing logos; (c) Visual themes/styles (e.g. "Nordic minimalist", "artisanal kraft paper"). |
| **Logo style (choose up to 3)** | Wordmark-only / Lettermark (initials monogram) / Pictorial mark (icon) / Combination mark (icon+word) / Emblem (seal). |
| **Final brandbook info architecture** | Cover → Logos → Palette → Typography → Mockup applications → Do/Don't (min 6 sections). |
| **Mandatory logo variants** | Primary (horizontal full) / Secondary (stacked / vert.) / Monochrome black / Monochrome white / Icon only / Favicon 64×64. ≥6 variants. |
| **MANDATORY SVG deliverable (HARD GATE)** | All variants must be standalone SVG, NO embedded bitmaps, < 128KB, `0 0 1024 1024` default viewBox. |

#### 0.2 Write spec to disk and ask for explicit approval
- Save spec at: `$CHE_DESIGN_DIR/spec.md`
- Show spec to user **formatted for diagonal reading** (tables, bold, bullets).
- Single approval question (mandatory):
  > **"I approve this spec as it is — you may execute (Yes / No, adjust these X points)"**
- If NO → adjust only the listed points; re-present; repeat.

---

### GATE 0: Choose mode A/B/C/D (if user did not specify)
If user request already indicates mode → direct. Otherwise stop and ask via `AskUserQuestion` (4 options: A Social / B UI-UX / C Design System / **D Logo & Branding**).

### GATE 0.1 → EXCLUSIVE MODE D: MANDATORY Deep Discovery Questions
If mode = **D (Logo & Branding)**, BEFORE writing spec §0.1, run **5 question batches** (batch by batch, wait for responses per batch):

| Batch D | MANDATORY Questions (max 5 per batch) |
|---|---|
| **Batch D1 — Identity** | 1. Full brand name (verbatim, exact case)? 2. Is there a slogan? If so, verbatim. 3. When was the brand born? Short story to tell? 4. Exact sector/industry? 5. Region/country of operation? |
| **Batch D2 — Positioning** | 1. What problem does the brand solve? 1 sentence. 2. Who is the ideal customer (persona, 3 characteristics). 3. Who are the 3-5 main direct competitors. 4. Single differentiator against competitors. 5. 3 adjectives describing brand personality (e.g. welcoming, premium, young). |
| **Batch D3 — Style & Aesthetics (up to 5 each)** | 1. 3-5 **reference brand/site URLs** (love / hate). 2. 3-5 reference visual themes/styles: minimalist / brutalist / artisanal / luxury / retro / modern / organic / tech etc. 3. Do you have old logos, sketches, drawings, existing moodboards to attach? 4. Colors associated with the brand (or colors to AVOID). 5. Favorite typography (or family you hate). |
| **Batch D4 — Voice & Communication** | 1. Tone of voice in 1 sentence (e.g. "accessible specialist", "friend who explains well", "discreet luxury"). 2. 3 EXAMPLE phrases of how brand speaks to customer (greeting, thank you, CTA). 3. Forbidden phrases / NEVER say. 4. Emoji use allowed? (Yes / No / Moderately). 5. Primary language and other operational languages. |
| **Batch D5 — Applications & Restrictions** | 1. Top 5 places logo will appear (Instagram profile / business card / shop front / t-shirt / site header / packaging...). 2. What the logo CANNOT have (e.g. "no generic bread icon", "no gradients"). 3. Do you have a defined palette/typography? (Yes → share / No → build from scratch). 4. Mandatory logo variants? (favicon, horizontal stacked, black, white, initials monogram). 5. Final delivery formats? (SVG mandatory default + PNG 1x/2x + vector PDF / .ico Favicon / wordmark font?). |

**Batch D fail-fast (if 2 batches still ambiguous)**: ask once: "Default: minimalist, neutral earthy tones, Inter + Playfair, 3 concepts, 6 variants. Proceed like this and refine per stage? (Yes / No — list adjustments)".

### GATE 1: Save path + brandbook
- **Design directory**: `CHE_DESIGN_DIR="$CHE_DESIGN_ROOT/<mode>-<slug>-YYYYMMDD"`. Source representation is backend-specific.
- **Brandbook (3 short bullets)**: hex palette / typography (Inter default) / copy tone of voice ("Professional accessible" default).
- Initialize/open design source using the active driver. OpenPencil can create local source; Figma registers metadata in `$CHE_DESIGN_DIR/figma-source.md`.

---

## 🧯 3. HARD-WON LESSONS (CANONICAL — mandatory fallback in THIS ORDER)
> *Never deviate from this order. It cost 4 hours + 14 bugs to discover this in production.*

### 3.1 Real PHOTO source cascade (ensure unique colors > 25,000)
1. **PRIORITY 1 — Real Unsplash photo URLs (GUARANTEED)**:
   ```
   https://images.unsplash.com/photo-<ID>?auto=format&fit=crop&w=1024&h=1024&q=90
   ```
   Mandatory headers: `User-Agent: Mozilla/5.0` + `Accept: image/webp,image/jpeg,*/*`. **DO NOT use source.unsplash.com (deprecated → HTML 403)**. Validate magic bytes `ffd8ff` (JPEG) or `89504e47` (PNG), size > 80KB — otherwise fall back.
2. **PRIORITY 2 — text_to_image endpoint (check for placeholder)**:
   ```
   https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=<ENCODED>&image_size=square_hd|portrait_16_9
   ```
   **MANDATORY VALIDATION**: photo MD5 ≠ others' MD5; unique colors > 25,000; NO `The image is generating` or `refresh page` substring in raw bytes. If fail → go to 3.
3. **PRIORITY 3 — open-pencil `stock_photo` MCP**: apply directly to a `create_shape(RECTANGLE 360×360 leaf)` via JSON array requests (query + orientation=square). Useful if OpenPencil desktop GUI is open (headless might not download — if fail → go to 4).
4. **PRIORITY 4 — PILLOW/IMAGEMAGICK offline fallback**: 100% guaranteed offline compositor (paste downloaded photo from 1 or 2 over rendered canvas base PNG with texts + fills). **This fallback NEVER FAILS**.

### 3.2 TEXT nodes in OpenPencil v0.8.4 — STRUCTURE ONLY RUNS WITH BUILT-IN TEMPLATE
- **PROHIBITED to create `TEXT` manually via `create_shape` or `I(null,{type:text,...})`**: node becomes width=height=0, without internal layout/font runs in Rust engine → **INVISIBLE / clipped / flat TEXT**.
- **MANDATORY CANONICAL METHOD**: `use-template knowledge-card-square` (1080×1080, 31 nodes per card) → generates full text/run/font store correctly. Then overwrite only copies/fills/fonts via MCP `set_text` + `set_font`.
- ALWAYS save via `save_document(filePath)` after changing text (saves internal stores in .op — otherwise different SHA256 and text disappears on desktop).

### 3.3 OFFLINE VISUAL validation (WITHOUT OPENING DESKTOP GUI) — unique colors
Python **definitive** heuristic (run on any exported PNG, validate per piece):
| Unique colors range | Meaning | Action |
|---|---|---|
| **< 2,000** | Flat / nothing rendered | Reproduce stage |
| **2,000 — 8,000** | Text + fills OK, NO PHOTOS | If stage expected photo → fallback 3.1.4 (Pillow) |
| **> 25,000** | REAL PHOTOGRAPHY rendered (natural gradients, pixel data) | ✅ PASS |

Run Python snippet in §10 after EACH stage export.

### 3.4 MANDATORY Stacking order (photos NEVER overlap text!)
Per frame (card/screen):
- **INDEX 0 → (PHOTO)**: always background, BEHIND everything.
- **INDEX 1 → (dark OVERLAY if WCAG requires, 30-40% alpha)**: only **if** photo is bright/warm AND text is white. Same radius as photo.
- **INDEX 2..N-1 → (Headline/Subline/Body TEXTS)**: always on top of photo + overlay.
- **LAST INDEX child → (CTA button)**: always highest layer, ensures click/tap target.

### 3.5 Image nodes in OpenPencil headless LIMIT
- `batch_design operations G(slot_id, "search", prompt)` creates child node in slot, but **headless CLI DOES NOT download stock photo** (no backend integration in headless runtime).
- Photo ONLY renders when opening .op in desktop GUI (it downloads on load). **If delivery requires FAST PNG without opening GUI → mandatory to fall back to Pillow 3.1.4 offline composition**.

---

## 📐 1. MODE A — Social Media Creatives (Execution BY STAGES + REVISOR PER STAGE)
Goal: Deliver N creatives (default 4 Feed 1:1) with 100% verbatim copies, palette, layout grid, photos, aesthetics, @2x export, **all aligned with approved §GATE -1 spec**.

### 1.0 Hard precondition: Spec APPROVED by user (§GATE -1)
- Copy approved spec to: `$CHE_DESIGN_DIR/spec.APPROVED.md` (SHA256 saved for revisor comparison).

### Stage flow (≤4 total stages, 1 stage executes at a time)
**BY STAGE → (a) Executor Agent (designer) executes; (b) Visual Revisor Agent validates against spec; (c) If pass → next stage; (d) If reject ≤2 times → stage rework; >2 times → back to spec adjustment.**

| Stage | Action (Executor Agent) | Visual Revisor Validation |
|---|---|---|
| **STAGE 1 — Photo Assets** | Download 1 photo per piece via §3.1 cascade; save in `/assets/<piece>.png`; center crop 1024×1024; unsharp 0.8 110% | (1) 4 PNG files exist; (2) Each unique colors >25,000; (3) Different MD5s (no repeated placeholder); (4) Unsplash query / text_to_image prompt matches piece theme in spec. |
| **STAGE 2 — Canvas Structure + Verbatim Texts** | 1 `knowledge-card-square` template per piece (TEXT nodes OK); name layers semantically (`C1-Headline`, `C2-CTA-Buy`); set 100% verbatim copies from spec (char-by-char, none changed); set spec fonts; set spec palette hex fills | Export @1x and validate: (1) Unique colors 2k-8k (text/fills OK); (2) Copies identical to spec (text hash); (3) Hex palette matches spec (`analyze_colors`); (4) Layers have no "Rectangle12" (all semantic); (5) WCAG AA contrast. |
| **STAGE 3 — Photo Slots + Visual Aesthetics** | Create 360×360 slot rect per piece at EXACT x/y from spec; apply photo asset (or §3.1.4 Pillow fallback if headless not rendering). Apply radius, white stroke, shadow, dark overlay (all EXACT spec values). **Stacking order INDEX 0 (photo) → INDEX 1 (overlay) → texts always above.** | Export @1x: (1) EXACT x/y position from spec (diff ≤2px); (2) exact radius + stroke + shadow (pixel check via edge mask); (3) Dark overlay ONLY if spec requested; (4) Photo NEVER covers headline/CTA (stacking); (5) Unique colors >25,000 ON ALL PIECES (photo embedded). |
| **STAGE 4 — Final @2x Export + Final QA Gate** | Export each piece scale=2 format=PNG; save_document source `.op` + `.openpencil` identical SHA; group in `/exports/` with exact spec names; run §4 gates on ALL outputs | All §4 gates pass; deliverables listed; spec vs output checklist complete. |

---

## 🖥 2. MODE B — UI/UX Feature Design (same Spec → Stages + Revisor structure)
Goal: Wireframes → Hi-Fi → Dev-Spec (React/Tailwind 4 pasteable output).

| Stage | Executor Action | Revisor Validates |
|---|---|---|
| **SPEC GATE-1** | Write complete spec: persona / job story / 3 core behaviors / 2-3 screens / breakpoints / dark mode / tokens / palette / reuse components | User approved spec → `APPROVED.md` saved. |
| **STAGE B1** | Low-fi wireframes (boxes + labels only; NO fills/photos). Max 3 screens. | Structure aligned with spec; correct labels; no fill/gradient. |
| **STAGE B2** | Design tokens collection (OpenPencil variables): 8 color / 6 radius / 8 spacing / 3 typography; bind layers to variables (NO raw hex). | All layers bound to vars; no raw hex in system elements; collection created with 2 modes if dark mode. |
| **STAGE B3** | High-fi: fills via vars; exact fonts + sizes; radius + effects; hero photo via §3.1 cascade; components (Button/Card) → `create_component`. | Variables bound; palette 100% from spec; photo >25k unique colors; WCAG AA; components created. |
| **STAGE B4** | Export dev-spec: `design_to_tokens(tailwind)` + PNG 2× screens + SVG components + 15-line `dev-spec.md` (1 for components / tokens / breakpoints). | Pasteable tailwind output; 2× 2560×1440 screen PNGs; SVG components with variables; 15-line dev-spec. |

---

## 🎨 3. MODE C — Design System (Tailwind 4 ↔ OpenPencil variables)
Goal: Extract Tailwind tokens → create variables + 12 atomic components × 4 variants (primary/secondary/ghost/destructive) + export 3 formats (tailwind / CSS / DTCG JSON).

| Stage | Executor Action | Revisor Validates |
|---|---|---|
| **SPEC GATE-1** | Spec: token origin (Tailwind config / from scratch) / mandatory dark mode / 12 default components; approve. | Approved spec saved. |
| **STAGE C1** | Create 2-mode collection (Light/Dark) → ~60 semantic vars (color/radius/spacing/typography/shadow/opacity). ALWAYS bind via semantic (never raw hex). | 60+ vars created; 2 modes if dark; no raw hex layers; semantic naming (color/brand/50, semantic/bg/primary). |
| **STAGE C2** | 12 atomic components: Button (5 variants + 3 sizes + disabled) / Card / Input+Textarea (focus ring) + Badge/Avatar/Alert/Toggle/Checkbox/Radio/Select/Modal-header. 4 variants each; SECTION group per component → `create_component`. | 48 variants total; padding/radius bound to vars; focus state via stroke+effects; components created (not just frames). |
| **STAGE C3** | `design_to_tokens` 3 formats (tailwind/CSS/JSON) → save to `/tokens/` | 3 token files; tailwind output pasted in `packages/ui/tailwind.config` if Flockr exists. |

---

## 🏷 4. MODE D — Logo & Branding (MANDATORY SVG + Brandbook)
Goal: Deep brand discovery → validated briefing → 3 logo concepts (low-fidelity sketch in OpenPencil) → vector refinement of 1 concept → **standalone SVG per variant** (HARD) → final brandbook with palette/typography/applications + brand voice.

### MODE D HARD Preconditions (fail = STOP):
1. **5 discovery question batches GATE 0.1 answered.**
2. **MODE D spec (§GATE -1 extra D fields) 100% filled and APPROVED by user → saved in `spec.APPROVED.md`.**
3. **At least 2 references (URL / attached logos / themes) provided.**

### MODE D Stage Flow (≤5 total stages; each stage validates with user BEFORE next):
**Each stage ALWAYS in this order → (a) Executor creates; (b) Visual Revisor validates against spec; (c) User confirms PASS / requests adjustments ≤3 bullets; (d) If user approved → next stage.**

| MODE D Stage | Action (Designer Executor Agent) | Visual Revisor Validation before showing user | MANDATORY User Checkpoint |
|---|---|---|---|
| **D0 — Validated Brand Briefing** | Write `brandbook/00-briefing.md`: name, slogan, positioning, persona, competitors, differentiator, 5 personality adjectives, brand voice + 3 example phrases, top 5 applications, prohibited restrictions. | (1) All D1-D5 discovery fields appear in briefing; (2) 3 brand voice phrases written; (3) ≤2 references per URL/attachment listed. | ✅ User signs off: "Briefing correct — generate concepts" (Yes / No adjustments X) |
| **D1 — 3 Low-Fidelity Concepts** | In OpenPencil, 3 side-by-side 1024×1024 artboards (CONCEPT-A / B / C). Each: **boxes + labels** (no final aesthetics): wordmark position / icon position / initials / general horizontal or stacked proportion. Basic shapes + text labels only. | (1) 3 concepts exist; (2) No bitmap / gradient / aesthetic fill; (3) Each concept has different proportion / style (e.g. A = horizontal wordmark only; B = vertical icon+word; C = circular monogram). | ✅ User chooses 1 concept to refine (can say "hybrid A top + B body"). ≤1 hybrid allowed. |
| **D2 — Vector Refinement of Chosen Concept** | In OpenPencil, on 1 artboard: build **pure vectors** (BOOLEAN union/subtract/intersect — NO raster, NO bitmaps) for: (a) wordmark (type converted to paths if display); (b) icon / symbol / monogram; (c) primary horizontal full combination. Apply spec hex palette; apply exact wordmark typography; adjust visual kerning. | (1) **ALL nodes are vectors** (check SVG export — no `<image>`, no base64); (2) Exact hex palette from spec (`analyze_colors`); (3) Linked typography; (4) Initial SVG export < 256KB; (5) Proportions aligned with chosen D1 concept. | ✅ User validates vector stroke / kerning / colors. |
| **D3 — 6 Variants + SVG Export (HARD GATE)** | Create **≥6 mandatory logo variants**: (1) Primary horizontal full (wordmark + side icon); (2) Secondary stacked vertical (wordmark below icon); (3) Lettermark / initials monogram square; (4) Pictorial icon-only; (5) Monochrome black (1 fill color); (6) Monochrome white (1 reverse color). **Export ALL 6 individually as pure vector standalone SVG.** Validate via §12.1 snippet before advancing. Optional extra: 64×64 SVG favicon. | (1) **6 SVG files in `/vectors/`**; (2) **Each SVG: zero `<image>` tags / zero base64 (regex validation)**; (3) Each SVG `viewBox="0 0 1024 1024"` (or correct proportion); (4) Each size < 128KB; (5) 2 monochrome variants (black + white) 100% 1 color; (6) Standalone SVG opens in browser without errors (XML parse validation). | ✅ User validates final 6 variants. Requests final color / spacing adjustments (≤3 bullets). |
| **D4 — Full Final Brandbook + Mockup Applications** | (a) Assemble 6-section min brandbook structure: `01-cover.md`, `02-logos-variants.md` (all 6 SVGs embedded), `03-palette.md` (color names + hex + uses: primary / secondary / text / bg), `04-typography.md` (Display wordmark + Body + weights + line heights + examples), `05-applications.md` (≥3 real mockups: IG profile 1:1 / business card / 1280×640 site header — generate mockup PNGs on separate canvas), `06-do-and-dont.md` (3 DO + 3 DON'T: e.g. DO leave 0.5× "X" height clear space / DON'T place on low-contrast photos). (b) Export 2× PNG of all SVGs to `/exports/logo-*@2x.png`. | (1) 6 brandbook sections in markdown + assets; (2) 3 PNG mockups created (≥2560 wide); (3) DO/DON'T has at least 3 each; (4) ALL already validated SVGs remain in `/vectors/`; (5) Consistent brand voice in brandbook text. | ✅ User approves final brandbook. |

---

### MODE D user validation flow per stage (HARD — NO skipping):
1. Executor finishes stage → saves files.
2. Revisor issues PASS/REWORK ≤3 bullets.
3. If REWORK → executor fixes deviations only.
4. If Revisor PASS → **raise single question to user**: `"Stage D<N> complete. Approve to advance to D<N+1>? (Yes / No — adjustments: [1,2,3 points])"`.
5. If NO → adjust listed points only; re-submit for approval. **Do not advance to next stage without explicit user Yes.**

---

## ✅ 4. QUALITY GATES (HARD FAIL if not passed → fix before delivery)
All gates 1-7 apply to **ANY MODE** and **every final stage**. Gates D1-D5 are **MODE D exclusive (HARD)**:

> **Simplicity Bias (engineering-contracts §1):** propose the simplest design. Defer variants, edge-case polish and extras no current spec demands — record them as deferred, do not build them in this iteration.

### Global gates (all modes)
1. **WCAG AA CONTRAST**: Body text ≥ 4.5:1; large text ≥ 3:1. Check with `analyze_colors` MCP if in doubt. Dark overlay mandatory if white text + bright photo.
2. **VALIDATED IMAGES**: (a) `unique colors > 25,000` (§3.3) PER PIECE expecting photo; (b) NO endpoint placeholder (check bytes + MD5); (c) Photo theme matches piece.
3. **ALWAYS EXPORT SCALE 2 (2×)**: Feed 2160×2160; Stories 2160×3840; Desktop screens ≥2560 wide.
4. **NO GARBAGE LAYER NAMES**: NO "Rectangle 12", "Text 4". Always: `<Piece>-<Role>` (e.g. `C1-Headline-Hero`, `CTA-Buy-Ticket`).
5. **MANDATORY OFFLINE FALLBACK IF HEADLESS STAGE 3 PHOTOS FAIL**: Run Pillow §3.1.4 offline compositor (paste downloaded photo asset over rendered text base PNG) — this is the final gate to deliver **guaranteed** photo.
6. **CLEAN STORAGE PATHS**: durable outputs in `$CHE_DESIGN_DIR`; assets in `$CHE_DESIGN_DIR/assets/`; exports in `$CHE_DESIGN_DIR/exports/`.
7. **SPEC CHECKSUM**: Final output **MUST** correspond to `spec.APPROVED.md`. Revisor compares item by item (palette / verbatim copies / layout / dimension).

### MODE D exclusive gates (Logo & Branding) — HARD fail
8. **D1: PURE SVG (NO BITMAPS)**: No logo variant may contain inline `<image>` tags, base64 bitmaps, `<foreignObject>`, or embedded raster data. Validate via regex in each SVG file. If photo needed → separate PNG, NOT inside logo SVG.
9. **D2: MINIMUM 6 MANDATORY VARIANTS**: Primary horizontal + Secondary stacked + Monochrome black + Monochrome white + Icon only + Initials Monogram/Lettermark. ≥6 files in `/vectors/` at end of D3.
10. **D3: SMALL, STANDALONE SVG, CORRECT VIEWBOX**: Each SVG ≤128KB; `viewBox` (e.g. `0 0 1024 1024` square OR natural width:height proportion); NO external dependencies (remote linked fonts, URLs); opens in any modern browser without errors. Validate §12.1 snippet.
11. **D4: 1-COLOR MONOCHROME**: black (`#000000` or spec dark) AND white (`#FFFFFF`) variants MUST have 100% paths in ONLY 1 fill. No gradient, no rasterized shadow. Test: open SVG in text editor → replace fill → only 1 color changes.
12. **D5: MINIMUM 6-SECTION BRANDBOOK**: 00-briefing / 02-logos-variants / 03-palette / 04-typography / 05-applications-mockups (≥3) / 06-do-and-dont (≥3 DO / ≥3 DON'T). PNG mockups ≥2560px each.
13. **D6: CANONICAL SVG NOMENCLATURE**: `logo-primary.svg`, `logo-stacked.svg`, `logo-monochrome-black.svg`, `logo-monochrome-white.svg`, `logo-icon.svg`, `logo-monogram-<INITIALS>.svg`. No spaces / special characters.
14. **D7: DOCUMENTED CLEAR SPACE & MIN SIZE**: Brandbook 02-logos-variants must have table: minimum clear-space (e.g. "0.5× wordmark X-height") and minimum size for print / digital (e.g. "≥48px digital height").

---

## 👀 5. SPECIALIST VISUAL REVISOR AGENT (role and criteria)
Invoked **AFTER EACH STAGE** (before next). Role = visual QA + spec compliance.

### 5.1 Per-stage revision protocol
```
Input:
  - SPEC_APPROVED_PATH (file saved after approval)
  - STAGE_ID (1/2/3/4)
  - STAGE OUTPUT_FILES (PNG / .op / json path list)
  - ENGINEERING_CONTRACTS §18 verbosity
Output:
  [PASS] → 1 sentence "Aligned with spec in all gates. Next stage released."
  [REWORK] → ≤3 bullets of ONLY the deviations (e.g. "C3 radius=24 but spec asks 28"; "C2 unique colors = 3,200 (expected >25k photo)")
```

### 5.2 Limits
- ≤ 2 REWORK rounds per stage; **>2 REWORK rounds = STOP and back to spec adjustment** (specification problem).
- Revisor NEVER modifies files; only issues PASS / REWORK with ≤3 deviations list.
- Offline visual validation: always run unique colors snippet (§3.3) + `analyze_colors` for contrast before deciding.

---

## 🚦 7. FAIL-FAST RULES (all modes)
- **2 adjustment rounds in Gate-1 Spec still ambiguous** → 1 question: "Want defaults and go? A) Yes / B) I will detail more".
- **2 stage copy/layout adjustment rounds DO NOT pass revisor** → back to Gate-1 Spec.
- **Placeholder photos 3x in cascade** → skip directly to §3.1.4 Pillow offline fallback (guaranteed).

---

## 📝 6. OUTPUT SHAPE §18 (all responses ≤500w)
```
### 📍 Status <1 sentence>
### 🧩 Key Changes (≤3 bullets)
  • **<Label>**: ≤2 lines.
### 🔗 Refs (≤5 links)
  • [<filename>](file:///absolute/path)
### ❓ Deep-dive
Do you want to deep-dive into **<ONE SINGLE THING>**? (Yes / No)
```

---

## 📁 8. PATH NOMENCLATURE
```
$CHE_DESIGN_DIR/
  ├── spec.md                  # Spec draft (iteration)
  ├── spec.APPROVED.md         # SHA256 spec locked after approval (GATE-1)
  ├── assets/
  │   ├── C1-hero.png          # 1024×1024 images (>25k unique colors)
  │   └── C2-flatlay.png
  ├── exports/
  │   ├── FINAL-<piece>@2x.png # 2160×2160 / 2160×3840 outputs (A/B modes)
  │   └── logo-primary@2x.png  # (MODE D only) 2× PNG of each SVG variant
  ├── vectors/ (MANDATORY for MODE D only)
  │   ├── logo-primary.svg
  │   ├── logo-stacked.svg
  │   ├── logo-monochrome-black.svg
  │   ├── logo-monochrome-white.svg
  │   ├── logo-icon.svg
  │   └── logo-monogram-<INITIALS>.svg
  ├── brandbook/ (MODE D only)
  │   ├── 00-briefing.md
  │   ├── 01-cover.md
  │   ├── 02-logos-variants.md (all SVG embedded)
  │   ├── 03-palette.md
  │   ├── 04-typography.md
  │   ├── 05-applications.md
  │   └── 06-do-and-dont.md
  ├── tokens/ (MODE C only)
  │   ├── tokens.tailwind.txt / tokens.css / tokens.json
  │   └── dev-spec.md (MODE B only, ≤15 lines)
```

Backend source artifacts are conditional: backend=`openpencil` stores `source.pen` plus the identical `source.openpencil` copy; backend=`figma` stores only `figma-source.md` metadata. backend=`spec-only` creates neither source artifact.

---

## 🗂 9. FULL SPEC TEMPLATE (MODE A MasterPan Instagram 4 posts 1:1 example)
> *Copy this template, fill 100% fields, present, wait for explicit "Yes, I approve spec" approval before any execution.*

```
# SPEC — MasterPan Bakery Instagram Carousel (4 posts 1:1 1080×1080)
## Meta
- Campaign goal: Present MasterPan as an artisanal bakery.
- Tone of voice: Cozy, artisanal, classic, warm.
- Global palette (all cards): #FFF7ED bg-stone-50 | #C2410C headline-orange-700 | #EA580C cta-orange-600 | #292524 text-stone-800 | #FFFFFF stroke-white
- Global typography: Inter (Black 72 headlines, Bold 40 subline, SemiBold 48 CTA)
- Export per card: 1080 base → scale 2 → 2160×2160 final PNG.

---
## Per Piece (4x)
| Field | C1-COVER | C2-MENU | C3-PROCESS | C4-VISIT |
|---|---|---|---|---|
| **Goal** | Hero hook: "Who we are" | 3 iconic breads | Wood oven = authenticity | Location + Visit CTA |
| **Headline (verbatim)** | *MasterPan* | *Our Breads* | *Wood-Fired Oven Baked* | *Come Visit Us* |
| **Subline (verbatim)** | Artisanal Bakery | Classics. Warm. Always fresh | Since 1998, with patience and embers | 123 Flower Street • Center |
| **Body bullets** | 1. Long natural fermentation; 2. Organic ingredients | 1. Warm French bread 7am; 2. Cheese bread; 3. Butter croissant | 1. Refractory bricks; 2. Baked daily 5am | 1. Tue-Sun 7am-7pm; 2. WhatsApp Delivery; 3. Free Wifi |
| **CTA button text** | View Menu → | Order Now → | View Process → | Get Directions → |
| **Photo pos (x,y) 360×360** | (696, 540) bottom-right | (696, 88) top-right | (696, 540) bottom-right | (696, 88) top-right |
| **Unsplash ID / prompt** | photo-1586444248902 (golden hero sourdough warm light) | photo-1549931319 (flat lay 3 breads parchment) | photo-1556909114 (wood oven embers bricks) | photo-1555507036 (bakery facade yellow awning morning) |
| **Photo radius | stroke | shadow** | 28 / 6 white / 4 8 blur14 alpha40 | same as C1 | same as C1 | same as C1 |
| **Dark overlay?** | No | No | **YES #1C1917 alpha 35%** (white text) | No |
| **Stacking order (0→N)** | 0=photo → 1=texts → last=CTA | 0=photo → 1=texts → last=CTA | 0=photo → 1=overlay → 2=white texts → last=CTA | 0=photo → 1=texts → last=CTA |
| **Final output name** | FINAL-WITH-REAL-PHOTO_C1-COVER@2x.png | FINAL-WITH-REAL-PHOTO_C2-MENU@2x.png | FINAL-WITH-REAL-PHOTO_C3-PROCESS@2x.png | FINAL-WITH-REAL-PHOTO_C4-VISIT@2x.png |

---
## WCAG Gate (per piece)
- C1: Orange text over bg-stone-50 → 5.2:1 ✅
- C2: same as C1
- C3: White text over oven photo + 35% overlay → ≥4.5:1 via overlay
- C4: same as C1
```

---

## 🗂 9.1 FULL SPEC TEMPLATE — MODE D (Logo & Branding)
> **MODE D EXCLUSIVE.** Copy this template, fill 100% fields after running 5 discovery batches D1-D5, present to user, wait for EXPLICIT APPROVAL "Yes, I approve MODE D spec" before any vector is drawn.

```
# SPEC MODE D — Logo & Branding <BRAND-NAME> (YYYY-MM-DD)
## D0 — Identity and Positioning
- Brand name (VERBATIM exact case):
- Slogan (if any, VERBATIM):
- Short story / brand origin (1-2 sentences):
- Exact sector / industry:
- Region / country of operation:
- Problem solved (1 sentence):
- Ideal customer (persona: 3 characteristics):
- 3-5 direct competitors + site URLs:
- 1 unique differentiator vs competitors:
- 5 brand personality adjectives:
- Brand voice (1 sentence tone):
  - 3 EXAMPLE phrases of brand-customer talk:
  - FORBIDDEN phrases / NEVER say:
  - Emojis allowed? (Yes / No / Moderately)
  - Primary language + other languages:

## D1 — Aesthetics, References and Restrictions
### MANDATORY References (at least 2 from one category):
- (a) 3-5 reference brand/site URLs (love):
- (b) 3-5 reference brand/site URLs (hate):
- (c) Old logos / sketches / moodboards attached (list paths):
- (d) Reference visual themes/styles (e.g. "Nordic minimalist", "brutalist", "luxury", "artisanal kraft"):
### Colors:
- DEFINED hex palette (if already have): primary=#XXXXXX | secondary=#XXXXXX | accent=#XXXXXX | neutrals=#XXXXXX,#XXXXXX,#XXXXXX
- FORBIDDEN colors NEVER USE:
### Typography:
- Wordmark (Display) family already defined? (Yes → which / No → choose in D2)
- Body family already defined? (Yes → which / No)
- FORBIDDEN typographic families we hate:
### Logo style(s) (choose up to 3):
- [ ] Wordmark-only
- [ ] Lettermark / initials monogram
- [ ] Pictorial mark (abstract icon / illustration)
- [ ] Combination mark (icon + horizontal word)
- [ ] Emblem / seal (circular, rectangular)
### Top 5 places logo will appear (define proportions and min-size):
1. E.g. Instagram profile 320×320
2. E.g. business card 85×55mm (300dpi)
3. E.g. site header 1280×640 (256px max height)
4. E.g. packaging front
5. E.g. screen printing t-shirt
### WHAT LOGO CANNOT HAVE (explicit restrictions):
- Restriction 1 (e.g. "no generic bread icon"):
- Restriction 2 (e.g. "no gradient, flat color only"):
- Restriction 3:

## D2 — Mandatory variants + brandbook architecture
### MANDATORY logo variants (≥6):
1. Primary horizontal full (wordmark + side icon)
2. Secondary stacked vertical (wordmark below icon)
3. Monochrome black (1 single fill color, no gradient)
4. Monochrome white (1 single fill color, reverse)
5. Icon / pictorial mark only (square)
6. Lettermark / initials monogram (square)
7. (optional) Favicon 64×64 SVG
### Final SVG filenames (HARD gate D6):
- `vectors/logo-primary.svg`
- `vectors/logo-stacked.svg`
- `vectors/logo-monochrome-black.svg`
- `vectors/logo-monochrome-white.svg`
- `vectors/logo-icon.svg`
- `vectors/logo-monogram-<INITIALS>.svg`
### Brandbook (min 6 sections):
1. Cover (brand name + slogan + primary logo + date)
2. Logos and variants (all 6 SVGs + clear-space + min-size table)
3. Color palette (names + hex + uses: primary / secondary / text / background)
4. Typography (Display wordmark + Body + weights + line-height + examples)
5. Real applications (≥3 mockups 2× PNG: IG profile / card / site header)
6. DO and DON'T (≥3 DO + ≥3 DON'T, each with short explanation)

## D3 — Final SVG gates (HARD — failure = STOP):
- Each SVG ≤ 128KB
- Each SVG: ZERO `<image>`, ZERO base64, ZERO `<foreignObject>`, ZERO external links
- viewBox (square: `0 0 1024 1024` or natural proportion e.g. `0 0 1536 512` for horizontal)
- Monochrome black and white: 100% single fill (check via fill= grep 1 single non-transparent color)
- All SVGs valid XML parse (Python xml.etree.ElementTree)

---
## Sign-off
**Approver (user):** _________________________ Date: ________
Expected response to continue: "I approve the MODE D spec. You may execute stages D0 → D4."
```

---

## 🛠 10. CANONICAL SNIPPETS (copy directly)
### 10.1 Python unique colors validation (run PER PIECE after export)
```python
import struct,zlib,os,hashlib
def validate_png(p:str, min_colors=25000, photo_expected=True)->tuple[bool,str]:
    with open(p,'rb') as f: d=f.read()
    is_png = d[:8].hex()=='89504e470d0a1a0a'
    placeholder = b'The image is generating' in d or b'refresh page' in d
    i=8; idat=b''; w=h=ct=0
    while i<len(d):
        L=struct.unpack('>I',d[i:i+4])[0]; ctt=d[i+4:i+8].decode('latin1'); cd=d[i+8:i+8+L]
        if ctt=='IHDR': w,h,_,ct,_,_,_=struct.unpack('>IIBBBBB',cd)
        if ctt=='IDAT': idat+=cd
        i+=12+L
    bpp={0:1,2:3,3:1,4:2,6:4}[ct]; stride=w*bpp+1
    try:
        raw=zlib.decompress(idat); seen=set()
        for ln in range(h):
            s=ln*stride+1; buf=raw[s:s+(stride-1)]
            for pi in range(0,len(buf)-bpp+1,bpp):
                seen.add(tuple(buf[pi:pi+bpp]))
                if len(seen)>600000: break
            if len(seen)>600000: break
        uc=len(seen)
    except:
        uc=0
    md5=hashlib.md5(d).hexdigest()[:12]; sz=os.path.getsize(p)//1024
    ok=True; reasons=[]
    if not is_png: ok=False; reasons.append('not_png')
    if placeholder: ok=False; reasons.append('placeholder_endpoint')
    if photo_expected and uc<min_colors: ok=False; reasons.append(f'low_colors(<{min_colors}):{uc}')
    return ok, f"{os.path.basename(p):42s} {w}x{h} {sz:>4d}KB uc={uc:>6d} md5={md5} {'OK' if ok else 'FAIL:'+','.join(reasons)}"
```

### 10.2 Pillow composition offline fallback (3.1.4 — paste photo over text base PNG)
```python
from PIL import Image, ImageDraw, ImageFilter, ImageOps
def compose_photo_onto_base(base_png:str, foto_png:str, out_png:str, *,
                             x:int,y:int,FW:int,FH:int, radius:int,
                             border_px:int, shadow_alpha:int=96,
                             dark_overlay_rgba:tuple[int,int,int,int]|None=None):
    base = Image.open(base_png).convert("RGBA")
    foto = ImageOps.fit(Image.open(foto_png).convert("RGBA"),(FW,FH),Image.LANCZOS,centering=(.5,.5))
    # Photo clip radius
    mask = Image.new("L",(FW,FH),0); ImageDraw.Draw(mask).rounded_rectangle((0,0,FW,FH),radius=radius,fill=255)
    foto.putalpha(mask)
    # Frame
    MS = (FW+border_px*2, FH+border_px*2); MR = radius + border_px//2 + 2
    frame = Image.new("RGBA", MS, (0,0,0,0)); ImageDraw.Draw(frame).rounded_rectangle((0,0,*MS),radius=MR,fill=(255,255,255,255))
    # Shadow
    SPAD=14*3; SZ=(MS[0]+SPAD*2, MS[1]+SPAD*2)
    shadow=Image.new("RGBA",SZ,(0,0,0,0)); ImageDraw.Draw(shadow).rounded_rectangle((SPAD,SPAD,SPAD+MS[0],SPAD+MS[1]),radius=MR,fill=(0,0,0,shadow_alpha))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=14))
    # Paste
    out = base.copy()
    out.alpha_composite(shadow,(x-border_px-SPAD+4, y-border_px-SPAD+8))
    out.alpha_composite(frame,(x-border_px, y-border_px))
    out.alpha_composite(foto,(x,y))
    if dark_overlay_rgba:
        ov=Image.new("RGBA",(FW,FH),(0,0,0,0)); ImageDraw.Draw(ov).rounded_rectangle((0,0,FW,FH),radius=radius,fill=dark_overlay_rgba)
        out.alpha_composite(ov,(x,y))
    out.save(out_png,"PNG",optimize=True)
```

### 10.3 MODE D — Pure vector SVG validation (run PER VARIANT after export D3)
```python
import os,re,xml.etree.ElementTree as ET
def validate_svg_logo(path:str,min_variants:int=6)->tuple[bool,str]:
    if not os.path.exists(path):
        return False,f"{os.path.basename(path):48s} MISSING"
    with open(path,'rb') as f: raw=f.read(); sz=os.path.getsize(path)//1024
    try:
        root=ET.fromstring(raw)
        tag=lambda x: x.split('}')[-1] if '}' in x else x
        # D1: no image / foreignObject / base64 data URI
        forbidden_tags={'image','foreignObject','use'}
        bad_tags=[e.tag for e in root.iter() if tag(e.tag) in forbidden_tags]
        has_b64=b'data:image' in raw or b'base64' in raw
        # D3: viewBox exists
        vb=root.attrib.get('viewBox','')
        # Monochrome check heuristic: count unique fill hex
        fills=set(re.findall(r'fill\s*=\s*["\'](#[0-9a-fA-F]{3,8})["\']',raw.decode('utf-8','ignore')))
        mono_ok = len(fills)<=2  # ≤2 non-transparent colors (1 fill + maybe same stroke)
        xml_ok = True
    except ET.ParseError as e:
        return False,f"{os.path.basename(path):48s} sz={sz:>3d}KB XML_INVALID: {str(e)[:40]}"
    ok=True; r=[]
    if sz>128: ok=False; r.append(f'oversize({sz}KB>128KB)')
    if bad_tags: ok=False; r.append('bad_tags:'+','.join(tag(x) for x in bad_tags[:3]))
    if has_b64: ok=False; r.append('b64_or_datauri')
    if not vb: ok=False; r.append('no_viewBox')
    return ok,f"{os.path.basename(path):48s} sz={sz:>3d}KB fills={len(fills)} vb={bool(vb)} mono~{mono_ok} {'OK' if ok else 'FAIL:'+','.join(r)}"
```

### 10.4 MODE D — 2× PNG Export of all SVGs (via cairosvg OR Pillow fallback)
```python
def rasterize_svgs_to_png2x(vectors_dir:str, exports_dir:str, scale:int=2):
    import subprocess, pathlib
    V=pathlib.Path(vectors_dir); E=pathlib.Path(exports_dir); E.mkdir(parents=True,exist_ok=True)
    for svg in V.glob('*.svg'):
        out=E/f"{svg.stem}@{scale}x.png"
        # Try cairosvg first, else rsvg-convert, else ImageMagick convert
        for cmd in (["cairosvg",str(svg),"-o",str(out),f"--scale={scale}"],
                    ["rsvg-convert","-o",str(out),"-w",str(2048),str(svg)],
                    ["convert","-density",str(144*scale),str(svg),str(out)]):
            try:
                if subprocess.run(cmd,capture_output=True,timeout=30).returncode==0: break
            except FileNotFoundError: continue
```

---

## 🧩 11. DESIGN BACKEND SELECTION
Canonical contract: `references/DESIGN_BACKEND_CONTRACT.md`.
Available drivers:
- `openpencil` → `references/backends/OPENPENCIL.md`
- `figma` → `references/backends/FIGMA.md`
- `spec-only` → SPEC/dev-spec only; STOP before pixel execution

Selection is capability-based, not IDE-based.
User explicit backend choice has precedence when that capability exists.
If the requested backend capability is unavailable, FAIL CLOSED instead of silently switching design engines.

---

## 🧰 12. MODE D — SVG Logo Reference (boolean vector & clean-up)
### 12.1 Pure vector & booleans (HARD for logo)
1. **WORDMARK**: if display/script, ideally convert outlines to paths via OpenPencil `boolean_union` BEFORE SVG export (ensures render without installed font dependency).
2. **SYMBOL/MONOGRAM**: ALWAYS build with primitives (rect / circle / bezier path) → then `boolean_union/subtract/intersect` for single contour. Avoid 12 overlapping layers generating artifacts.
3. **MANDATORY CLEAN-UP BEFORE SVG EXPORT**: remove empty / invisible / duplicate layers; flatten unnecessary groups. Final layer names: `wordmark` / `icon` / `monogram` / `bg`.

### 12.2 WCAG & contrast rules in logo
- Primary variant: logo contrast against light background (white / spec bg) ≥ 3:1 for readability in 48px+ header.
- Monochrome white variant: ALWAYS test against palette dark #111827.
- Minimum clear-space documented in 02-logos-variants brandbook: **0.5× wordmark X-height on ALL sides of logo bounding box.**
