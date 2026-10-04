---
name: creative-designer
description: Visual design and asset creation — social media graphics, HTML/CSS mockups, image generation, text overlays and branding for any active brand
allowed-tools: Read, Grep, Glob, Bash, WebSearch, WebFetch
area: Marketing
use_for: "Visual design and asset creation — social media graphics, HTML/CSS mockups, image generation, text overlays and branding"
deps:
  mcp: ["Zernio"]
  gateway: ["Gemini", "fivebucks (opt — fb.ai templates + media library; falls back to Gemini + Pillow; **scope: social_posts**)"]
  files: ["brand.md", "audience.md", "design-system/ (opt — local; or fb.ai brand kit via fivebucks_get_brand_kit; brand.md fallback)"]
  env: []
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.0 | July 12, 2026 |

**Description:** Visual design and asset creation — social media graphics, HTML/CSS mockups, image generation, text overlays and branding for any active brand

### Change Log

**v2.20.0** — July 12, 2026
- **Declared the fb.ai dependency and its required scope.** fb.ai API keys are now scoped; this skill's `deps.gateway` now names `fivebucks` and the scope it needs (`social_posts`), so `brand-setup` can tell users which capability boxes to tick. No behaviour change — see `agents/link.md` for the scope/error/quota contract.

**v2.19.0** — July 03, 2026
- **Corrected Zernio publish mechanics to the real MCP schema (fixes the v2.18.0 migration bug).** v2.18.0 wrongly repointed `late_presign_upload` → `media_generate_upload_link`, but that Zernio tool is a **browser-only** upload flow — PUTting to it silently fails. Now: **fb.ai render signed URLs** (Step 4a template-path) pass **directly** as `media_urls` with no re-host (`validate_media` first, local `curl` backup); **local Gemini `_final.png`** (Step 4 upload) uploads via `media_get_media_presigned_url(filename, content_type, size)`.
- **`posts_create` signature corrected.** Real params: `content`, `platform` (single string), `account_id`, `media_urls` (comma-separated string — not a `media_items` array), `publish_now`/`is_draft`/`schedule_minutes`. One call per platform (no `platforms[]`, no `platformSpecificData.contentType`). `account_id` always passed, resolved via `accounts_list`.
- **`bg_image` / image-slot format documented (Step 4a).** Image-slot overrides (`bg_image`, `s2_image`…`s5_image`) must be `"media:{fileId}"` from `fivebucks_list_media_files`, never a raw URL — parity with content-generator.
- **Batch execution order added (Step 4a).** Multiple template-path posts run in three batched phases — all `fivebucks_create_post`, then all `fivebucks_render_post`, then all `posts_create` — never interleaved per post. Scoped to the template-path; the Gemini fallback stays strictly sequential.

**v2.18.0** — July 01, 2026
- **Zernio migrated to its own MCP (gateway v1.7.4).** Repointed `late_presign_upload` → `media_generate_upload_link` and `late_create_post` → `posts_create` to Zernio's native MCP tool names; dropped the `fiveagents_api_key` param from those calls (Zernio is now OAuth-connected, not gateway-routed); renamed internal `late_*` output fields (`late_uploaded`, `late_uploads`) to `zernio_*`.
- **Gemini image model ID updated (gateway v1.7.4).** `gemini_generate_image` model changed from the retired `gemini-3.1-flash-image-preview` to the GA default `gemini-3.1-flash-image` ("Nano Banana 2").

**v2.12.2** — June 08, 2026
- **`add_text_overlay` comment corrected: `ratio ≥ 1.78` → `ratio ≥ 1.7`.** Comment and code disagreed on the Story detection threshold; code (`>= 1.7`) is authoritative.
- **Rate limit rule now mentions `late_create_post`.** Steps 1 and 3 said "upload `_final.png` to Zernio" — the upload presigns to S3/CDN but the social post isn't live until `late_create_post`. Agents following the old rule would upload silently and never publish.
- **Step 4 upload code: `final_image.png` → `_final.png`.** The Python snippet used `'path/to/final_image.png'` while the ⚠️ guard above it said "always upload `_final.png`".
- **Step 4 `late_create_post` snippet expanded.** Previously only showed `media_items`. Now includes `content`, `platforms` (with `platformSpecificData.contentType` — required for Stories), `publish_now`, and `is_draft`.

**v2.12.1** — May 30, 2026
- **Media pool fallback made explicit (parity with content-generator v2.12.1).** Restructured the Step 1 media pool build from a single dense paragraph into a numbered sub-step list with bold-labelled fallbacks so both levels are reliably executed: (1) exact folder-name match first, (2) all-folders pool if no exact match, (3) empty pool if no folders. Matches content-generator's structure exactly.

# Creative Designer Skill

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are a visual art director for the active brand. Your job is to design on-brand marketing assets using HTML/CSS, produce detailed design specifications, and create visual mockups for web, email, and social contexts. All designs must follow the active brand's system (colors, typography, aesthetic — from `brands/{brand}/brand.md`) and serve a specific persona and campaign goal.

---

## When to use

Use this skill when the task involves:
- Designing HTML/CSS landing pages or sections
- Creating email template layouts
- Producing visual ad mockups (static)
- Designing social media graphics (LinkedIn banners, Twitter cards)
- Building comparison tables or feature highlight layouts
- Generating design specifications for a developer to implement
- Creating branded document templates (reports, one-pagers)

Do NOT use this skill for:
- Writing copy to go inside the design → use content-creation first
- Building full campaign strategy → use research-strategy first
- Creating presentation slide decks → use campaign-presenter
- Analyzing campaign performance → use data-analysis

---

## Inputs required

Before starting, confirm these inputs with the user:

| Input | Required | Notes |
|-------|----------|-------|
| Asset type | Yes | Landing page, email, ad, social graphic, one-pager, etc. |
| Target persona | Yes | Reference brands/{brand}/audience.md |
| Campaign / purpose | Yes | What this asset is for |
| Key message / headline | Yes | Get from content-creation or user |
| Dimensions / format | Optional | Defaults listed in design constraints below |
| Output type | Optional | HTML/CSS code, design spec, or visual mockup description |

---

## Design constraints

### Brand system — resolve the visual source in a 3-tier order

The brand's visual identity (colors, typography, components) is sourced in this 3-tier order. **Resolve it before applying colors, typography, layout, or component styles** — never block.

1. **fb.ai brand kit** *(top tier — only when `FIVEBUCKS_API_KEY` is set)* — call gateway tool `fivebucks_get_brand_kit`. If it returns non-null, use its color tokens (HEX) + typography as the authoritative source — resolve fields via the Brand kit field map in `agents/link.md` (secondary→`tokens.colors.accent`, text→`tokens.colors.dark`, fonts from `tokens.fonts.heading`/`body`; the kit gives font families only — the font weight scale comes only from the local `design-system/`). Returns null when no kit is uploaded — fall through to tier 2.
2. **brands/{brand}/design-system/** *(local folder — when the fb.ai kit is null or `FIVEBUCKS_API_KEY` is unset; the free baseline)* — the Claude Design system optionally installed in `brand-setup` Step 4b. Read per link.md tier 2 (HEX color tokens + typography incl. weight/size scale); for this skill, also extract component styles (buttons, cards, headers, badges) and the spacing scale (gaps, padding, border-radius).
3. **brands/{brand}/brand.md** — voice/tone, approved phrases, Do/Don't rules — and (when neither of the above is available) canonical colors and the Google Font name identified during brand-setup Step 4. Universal fallback.

If neither the fb.ai brand kit nor `brands/{brand}/design-system/` is available, **continue** — derive colors and fonts from `brand.md` and proceed. You may suggest the user run `/link-skills:brand-setup` Step 4b for tighter brand consistency, but it is not a hard block.

Never hardcode colors or fonts from memory. Always derive them from the fb.ai brand kit (`fivebucks_get_brand_kit`, when `FIVEBUCKS_API_KEY` set) → local `design-system/` → `brand.md` (fallback). If the source you used (fb.ai brand kit or design-system) disagrees with `brand.md` on colors/fonts, that source wins and `brand.md` should be updated to match.

### Optional fb.ai social templates

Up to four optional Claude Design templates may exist for a brand, hosted on **fb.ai** (installed via brand-setup Step 4c, discovered via the gateway `fivebucks_list_templates` tool — needs `FIVEBUCKS_API_KEY`):

| Template `type` | Used for | Fallback if missing |
|---|---|---|
| `meta-carousel` (4:5) | IG + FB carousel posts (Cover + 4 value slides + CTA) | Gemini + Pillow text/logo overlay using fb.ai brand kit / design-system / brand.md colors |
| `meta-story` (9:16) | IG + FB Stories (Hook→…→CTA, directions A/B/C) | Same Gemini + Pillow fallback |
| `linkedin-post` (4:5) | LinkedIn single-image feed posts (directions A/B/C) | Same Gemini + Pillow fallback |
| `meta-post` (4:5) | IG + FB single-image feed posts (directions A/B/C) | Same Gemini + Pillow fallback |

fb.ai renders each template server-side and returns signed PNG URLs — no local Playwright, no local template files. See "Render via template" in Step 4a. If no matching template exists (or `FIVEBUCKS_API_KEY` is unset), fall through to Step 4b's Gemini-only pipeline — never block.

### Standard asset dimensions (platform-fixed — same across all brands)
| Asset | Dimensions | Notes |
|-------|-----------|-------|
| Landing page hero | Full width × 600-800px height | |
| Email header | 600px wide × 200px height | |
| LinkedIn banner | 1584px × 396px | |
| LinkedIn post image | 1200px × 628px | Landscape — highest CTR for B2B feed |
| Facebook post image | 1200px × 630px | Landscape for link posts |
| Facebook Story | 1080px × 1920px | 9:16 vertical — same as Instagram Story |
| Instagram post (square) | 1080px × 1080px | Standard feed |
| Instagram post (portrait) | 1080px × 1350px | More feed real estate, better reach |
| Instagram Story | 1080px × 1920px | 9:16 vertical |
| Twitter/X card | 1200px × 628px | |
| Google display ad (leaderboard) | 728px × 90px | |
| Google display ad (rectangle) | 300px × 250px | |

### Layout rules (same across all brands)
- Max content width: 1200px centered
- Section padding: 64px vertical (desktop), 40px (mobile)
- Card padding: 24-32px
- Border radius: 8-12px for cards, 6px for buttons
- Use subtle box shadows: `0 1px 3px rgba(0,0,0,0.1)`
- White space is a feature — never overcrowd sections
- **Inset rule — Story = Meta safe zones only; Feed text = asymmetric (larger sides); Feed logo = uniform `pad // 2`:**
  - **9:16 Story** (text and logo both): top = `int(h * 0.14)` (~269 px on 1920) — Stories profile header; bottom = `int(h * 0.13)` (~250 px) — Meta bottom safe zone; sides = `int(w * 0.13)` (~140 px) — Meta side safe zone. Scrim fade = 0 (no `pad` anywhere in 9:16 geometry).
  - **Feed posts (IG, FB, LinkedIn, X) — TEXT:** top = bottom = scrim_fade = `pad // 2` (~32–36 px); sides = `pad + pad // 2` (~96–108 px). Sides are intentionally larger — Instagram's profile-grid view recrops square feed posts to 4:5 portrait, trimming ~34 px per side; the extra side inset guarantees text survives the crop with visible breathing room. **Do not "simplify" to uniform `pad // 2`** — that regressed v2.4.8 hardening (see v2.5.2 changelog).
  - **Feed posts (IG, FB, LinkedIn, X) — LOGO:** top = bottom = sides = `pad // 2` (~32–36 px). Logo is small relative to canvas, so the IG profile-grid crop doesn't impact it; uniform pad-derived inset reads as intentional corner placement. Text and logo diverge on sides by design.
- **Text and logo always on opposite vertical ends** — never on the same row. Mon/Wed/Fri = bottom text + top-right logo; Tue/Thu/Sat = top text + bottom-left logo. Day-of-week rotation lives in content-generator Step 4b.
- **Gradient scrim direction depends on `text_position`:** bottom-anchored text → scrim runs `scrim_top → target_h` (alpha 0→230). Top-anchored text → scrim runs `0 → text_bottom + scrim_fade` (alpha 230→0). The dark zone is always on the same end as the text.

---

## Step-by-step workflow

### Step 1: Read brand and content context
- **Brand visual identity** — resolve in 3-tier order (authoritative for colors, fonts, components, spacing):
  1. **fb.ai brand kit** — call `fivebucks_get_brand_kit` when `FIVEBUCKS_API_KEY` is set; if non-null, use its color tokens (HEX) + typography — resolve fields via the Brand kit field map in `agents/link.md` (secondary→`tokens.colors.accent`, text→`tokens.colors.dark`, fonts from `tokens.fonts.heading`/`body`; the kit has no separate `secondary` or font weight scale). Returns null when no kit is uploaded — fall through to tier 2.
  2. **brands/{brand}/design-system/** — Claude Design visual system; read when the fb.ai kit is null or the key is unset.
  3. **brands/{brand}/brand.md** — canonical colors and Google Font name as the universal fallback when neither of the above is available.
- **brands/{brand}/brand.md** — Voice, tone, approved phrases, Do/Don't rules (always read for these, regardless of the visual source above)
- **skills/creative-designer/style-guide.md** — Generic fallback rules (use only when the fb.ai brand kit, design-system/, and brand.md are all silent on a topic)
- Confirm the headline and key message (from content-creation or user input)
- Call `fivebucks_list_templates` once (cache for the run) and note which template `type`s exist on fb.ai: `meta-carousel`, `meta-story`, `linkedin-post`, `meta-post`. (Skip if `FIVEBUCKS_API_KEY` is unset → image-path only.)
- **Build the media pool** (once per run, cache alongside the template list — call once, not per asset; only when `FIVEBUCKS_API_KEY` is set and a template match exists). Mirrors content-generator Step 1c exactly. Execute these sub-steps in order — do not skip the fallbacks:

  1. **Call `fivebucks_list_media_folders` once** (cache the result alongside the template list).

  2. **Match each returned folder to a template type by exact name (case-insensitive):**

     | Folder name | Template type |
     |---|---|
     | `LinkedIn Post` | `linkedin-post` |
     | `Meta Story` | `meta-story` |
     | `Meta Carousel` | `meta-carousel` |
     | `Meta Post` | `meta-post` |

  3. **For each matched folder:** call `fivebucks_list_media_files` → store the file list as `media_pool[type]`.

  4. **Fallback — no exact match:** if a template type has no folder with a matching name, combine **ALL** returned folders — call `fivebucks_list_media_files` for every folder and merge into a single list. Use that combined list as `media_pool[type]`. (Do not leave the type's pool empty just because its named folder is missing.)

  5. **Fallback — no folders at all:** if `fivebucks_list_media_folders` returns an empty list, set `media_pool` to empty. Photo injection is skipped — image slots left empty; this is normal, not an error.

  6. **On any API error** from `fivebucks_list_media_folders`: skip silently, treat the pool as empty. Never fail or warn the run.

### Step 2: Define the layout structure
Sketch the component hierarchy before writing code:
- What sections does this asset need? (hero, features, social proof, CTA, footer)
- What is the visual hierarchy? (What should the eye land on first?)
- What components are needed? (cards, comparison table, icon grid, testimonial block, etc.)

### Step 3: Apply brand system
- Assign brand colors to each component role (primary, secondary, background, text)
- Apply typography scale consistently
- Ensure white space and padding follow layout rules

### Step 4: Build the asset
For HTML/CSS output:
- Write semantic HTML5 with inline or embedded CSS
- Ensure responsive layout (mobile-first where relevant)
- Use flexbox or grid for layout
- Do not rely on external CSS libraries unless the user specifies Tailwind CSS

For design spec output:
- Describe each section with: dimensions, colors (hex), font sizes, spacing, and component type
- Include copy placeholders clearly marked

### Step 4a: Render via fb.ai template if available

Before falling through to Gemini-only image generation (Step 4b — the universal fallback), branch on asset type. "A `<type>` template exists" = it appeared in the cached `fivebucks_list_templates` result (Step 1).

**Decision tree:**

```
asset_type == "carousel" AND platform in {instagram, facebook} AND a meta-carousel template exists → render via template
asset_type == "story" AND platform in {instagram, facebook} AND a meta-story template exists → render via template
asset_type == "post" AND platform in {instagram, facebook} AND a meta-post template exists → render via template
asset_type == "post" AND platform == linkedin AND a linkedin-post template exists → render via template
all other cases (banners, ads, mockups, no matching template) → fall through to Step 4b (Gemini + Pillow text + Pillow logo)
```

**Render via fb.ai (`fivebucks_*`). No local Playwright, no Pillow on this path.** The template lives on fb.ai (installed via brand-setup Step 4c). **For the canonical implementation see `content-generator/SKILL.md` Step 4c-template** — both skills follow the same procedure:

1. `fivebucks_list_templates` (cached) → pick the template whose `type` matches; read its `manifest` (fields + image slots + slides). If none, fall through to Step 4b.
2. Build `overrides` from the post copy (manifest field keys; skip `bound:false`, `select` values from `options`). Set direction: `_direction` (A/B/C) for meta-story; un-prefixed `direction` (A/B/C) for linkedin-post / meta-post; `coverVariant` / `bodyVariant` for meta-carousel if present.
3. Inject photos from the media pool built at run start. Priority: (1) user-provided photo if supplied in the session — always preferred; (2) `media_pool[type]` — for `linkedin-post` / `meta-post` assign one photo to `bg_image`; for `meta-carousel` / `meta-story` cycle through the pool for body slots `s2_image`…`s5_image` (up to 4; reuse from start if pool has fewer than 4); add companion overrides `{slot}_image_position: "center"` and `{slot}_image_fit: "cover"` for each assigned slot — every image-slot value (`bg_image` and `s2_image`…`s5_image`) must be formatted as `"media:{fileId}"` using the `fileId` returned by `fivebucks_list_media_files`, never a raw URL; (3) if pool empty and no user photo, leave all image slots empty — the template renders its own branded placeholder. Never fail or warn for an empty pool.
4. `fivebucks_create_post(template_id, name, overrides)` → `fivebucks_render_post(post_id)` → 1-hour signed PNG URLs. **Omit `slide_ids` for every type** — fb.ai selects the slide(s) from the direction override server-side: `meta-story` `_direction` (A/B/C) → that direction's 6 slides; `meta-carousel` → all 6; `linkedin-post` / `meta-post` `direction` (A/B/C) → the single matching slide. Never use `_direction: all` (renders 18 and burns the same 1.0 quota). See content-generator Step 4c-template §6 for the canonical rule.
5. **Publish output — split by template type.** Pass `fivebucks_render_post` signed URLs **directly** to `posts_create` as `media_urls` — do **not** re-host. The publisher fetches and caches each image at post-creation time, so the ~1h signed-URL expiry is safe within the run. `validate_media(url)` each URL first, and `curl -s -L "<signed_url>" -o "<local_path>"` a local backup. **Never use `media_generate_upload_link`** — it is a browser-only upload flow and PUTting to it silently fails. Resolve account IDs via `accounts_list` at run start. `posts_create` signature: `content`, `platform` (single string), `account_id`, `media_urls` (comma-separated string), `publish_now`/`is_draft`/`schedule_minutes` — one call per platform (no `platforms[]`, no `platformSpecificData`).
   - **`meta-story`**: `fivebucks_render_post` returns 6 signed PNG URLs (slide-1 through slide-6). Post one slide at a time = 6 separate posts per platform; sleep 1 second between slides; sleep 5 seconds + retry once after ~5 consecutive FB posts (Facebook rate-limits rapid sequential posts). See `content-generator/SKILL.md` Step 4c-template §7 for the canonical implementation.
   - **`meta-carousel` / single-image types** (`linkedin-post`, `meta-post`): call `posts_create` once per platform with the signed URLs joined into a comma-separated `media_urls` string (carousel = multiple URLs; single-image = one).
   - Skip Steps 4d/4e (Pillow overlays — fb.ai render includes all chrome).
6. On quota / 5xx error: fall through to Step 4b (Gemini + Pillow fallback).

After the template-path completes (bullet 5 handles validation and publishing), skip directly to the next section — do NOT proceed to Step 4b or the "Upload to Zernio" step below; those apply only to the Gemini-only fallback path.

**Batch execution order (multiple template-path posts in one run).** When producing several template-path assets at once, run the fb.ai calls in three phases, batched — never interleaved per post:

1. **Phase 1:** call `fivebucks_create_post` for ALL posts (one per post, in parallel).
2. **Phase 2:** call `fivebucks_render_post` for ALL created posts (in parallel).
3. **Phase 3:** call `posts_create` (publish) for ALL rendered posts (in parallel).

This applies only to the template-path (fb.ai render is server-side and not subject to the Gemini image API rate limit). The Gemini + Pillow fallback (Step 4b) still runs strictly one image at a time — see its rate-limit rule.

**The Gemini + Pillow fallback in Step 4b remains the universal path** for: banners, ads, mockups, any post with no matching fb.ai template (or when `FIVEBUCKS_API_KEY` is unset), and any failure (quota / 5xx) on the template-path. That fallback path applies the Pillow text overlay AND Pillow logo overlay (both inside Step 4b) — both required since the Gemini-generated background has no copy and no logo. The day-of-week `text_align`, `text_position`, and `logo_position` rotations apply only on this Step 4b path.

---

### Step 4b: Generate images via Gemini API

**Core principle: Visual = emotion. Text = punchline.**
The image must stop the scroll and evoke a feeling *before* the viewer reads a single word. Text overlays sharpen the message — they never explain what the image already shows.

Use **Gemini image generation** for assets that need real imagery — scenes, people, environments, data visualizations. Do NOT use Gemini for pure typographic/text-only graphics (use HTML/CSS for those instead).

**Story full-frame guard — apply BEFORE building the Gemini prompt:**

For Story assets (9:16, 1080×1920), the generated image must fill the entire canvas — no flat-colour void in the lower half. If the image prompt/brief does not already contain `"fills the ENTIRE frame"`, wrap it now:

```python
STORY_FULLFRAME_TEMPLATE = (
    "Photorealistic, full-bleed vertical portrait image for a 9:16 social media Story. "
    "{SCENE_DESCRIPTION}. The scene fills the ENTIRE frame from top to bottom — no empty areas, "
    "no plain backgrounds, no flat colour zones anywhere in the image. Rich environmental detail "
    "in the upper, middle, AND lower thirds of the frame. Cinematic lighting, editorial quality. "
    "Shot as if for a magazine cover in portrait orientation. "
    "Do not include any text, logos, or UI elements."
)

# Use canvas ratio as the primary signal — works whether asset_type is set or not.
# 9:16 = 1.778; IG portrait 4:5 = 1.25 (feed treatment, no wrap needed).
_asset_label = (asset_type or "").lower() if 'asset_type' in dir() else ""
is_story = _asset_label == "story" or (target_h / target_w) >= 1.7
if is_story and "fills the ENTIRE frame" not in image_prompt:
    image_prompt = STORY_FULLFRAME_TEMPLATE.format(SCENE_DESCRIPTION=image_prompt)
```

Use `image_prompt` (the potentially-wrapped version) as the `prompt` argument to `gemini_generate_image`.

```
Use gateway MCP tool `gemini_generate_image`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- prompt: "<your image prompt>"
- aspect_ratio: match target canvas (e.g. "1:1" for IG square, "9:16" for Story, "191:100" for LinkedIn)
- model: "gemini-3.1-flash-image"

Tool returns JSON text: { "image_base64": "...", "mime_type": "...", "description": "..." }
Result is auto-saved to a temp file. Use Python to locate and decode it:

```python
import glob, json, base64, os
result_file = max(glob.glob('/sessions/*/mnt/.claude/projects/*/tool-results/mcp-*gemini_generate_image*.txt'), key=os.path.getmtime)
with open(result_file) as f:
    parsed = json.loads(json.load(f)[0]['text'])
with open('outputs/{brand}/posts/{Platform}/tmp_image.png', 'wb') as f:
    f.write(base64.b64decode(parsed['image_base64']))
```

If user has selected a folder, save directly to `outputs/{brand}/posts/{Platform}/` — not a temp path.
```

If the tool returns a rate limit error, wait 60 seconds and retry once.

**IMPORTANT — Never use Nano Banana / `continue_editing` for text overlays.**

Use **Python Pillow** for all text overlay and logo compositing (see Steps 2 and 3 below). Do NOT use `image_add_text_overlay` or `image_add_logo` gateway MCP tools — they require passing large base64 strings through context, which exceeds Cowork limits.

**5 proven image patterns (adapt messaging to active brand):**

| Pattern | Visual | Text punchline |
|---------|--------|----------------|
| **Pain Moment** | Frustrated person, multiple screens, overwhelm | "You don't need more tools. You need one that does it all." |
| **Before/After** | Split: chaos left, clean dashboard right | "From this → to this. One platform." |
| **Bold Stat** | One huge number, almost nothing else | "Your next customer is already in here." |
| **Social Proof** | Real person quote + result metric overlay | Let the quote speak |
| **Aha Insight** | Chart or trend showing AI search taking over | "Is your business invisible to AI?" |

**When to use each pattern:**
- Pain Moment → awareness campaigns, cold audience, top of funnel
- Before/After → consideration, retargeting, mid-funnel
- Bold Stat → trust-building, LinkedIn, B2B decision makers
- Social Proof → bottom of funnel, conversion campaigns
- Aha Insight → thought leadership, LinkedIn, SEO/marketing personas

**Platform visual strategy:**
| Platform | Best pattern | Text density on image | Why |
|---|---|---|---|
| LinkedIn | Bold Stat, Aha Insight, Pain Moment | Medium — headline + brand mark | B2B audience reads; credibility-first |
| Facebook | Pain Moment, Before/After | Medium — benefit + proof element | Thumb-stop visual; emotion-led |
| Instagram | Bold Stat, Pain Moment | Low — 3–5 words max | Visual-first feed; text kills reach |

**Image prompt guidelines:**
- Lead with the **scene/feeling**, not the brand: "Frustrated professional at desk..." not "[brand] ad..."
- Specify **cinematic, photorealistic, editorial photography style** for people/scenes
- Specify **abstract, data visualization, geometric** for non-people visuals
- Include **lighting/mood**: "dimly lit, blue screen glow, night" or "bright, clean, modern office"
- **Inject the brand palette into the prompt** using the colors extracted at Step 1 — fb.ai brand kit HEX tokens (when `FIVEBUCKS_API_KEY` set) → local `design-system/` HEX tokens when present → `brand.md` Colors section when fallback. Phrase as ambient mood: "warm tones around #ec4899 / muted slate around #0f172a" or "rich teal accents (#0d9488) on a near-black background (#0a0a0a)". This is how Gemini matches the brand without ever putting the literal HEX swatches into the image. Never hardcode brand colors from memory — same Visual consistency rule as `agents/link.md`.
- **No text, no logos, no brand name in the image** — text and logo are composited after using gateway tools
- Always end prompt with: **"No text in the image. No logos. No watermarks."**
- Do NOT use `continue_editing` for text — use Python Pillow (Step 2) instead

> **About fonts on the Pillow path:** the text overlay uses `DejaVuSans-Bold` as a stable cross-platform rasterizer regardless of brand. The brand font names (fb.ai brand kit / design-system) are for Canva, HTML mockups, and any path that can actually load arbitrary fonts. The Pillow path matches the brand via *colors* (adaptive sampling on the Gemini background) — getting the brand palette into the Gemini prompt is what makes the final composite feel on-brand.

**Example prompts by pattern:**

*Pain Moment:*
> "Photorealistic editorial photo: frustrated young professional at cluttered desk, multiple monitors showing different SaaS dashboards, hands on head in stress, dimly lit room with blue screen glow, sticky notes everywhere, cinematic shallow depth of field, dramatic moody lighting. No text in the image. No logos. No watermarks."

*Aha Insight:*
> "Abstract data visualization: upward trending graph splitting into two paths — traditional Google search and AI chat interfaces (represented as glowing nodes), dark navy background, purple and pink gradient lines, clean minimal style. No text in the image. No logos. No watermarks."

*Bold Stat:*
> "Dramatic close-up of a glowing purple number '275M' floating in dark space, abstract particle field background in purple and pink tones, cinematic lighting, square format. No text other than the number. No logos. No watermarks."

**Rate limit rule — ALWAYS follow this sequence when generating multiple images:**
1. Generate image 1 → apply text overlay → apply logo → save `_final.png` to `outputs/` → upload `_final.png` to Zernio → call `posts_create` to publish (never upload the raw Gemini background)
2. Wait ~15 seconds before next generation (API allows 10 IPM; 15s is a safe buffer)
3. Generate image 2 → apply text overlay → apply logo → save `_final.png` → upload `_final.png` to Zernio → call `posts_create` to publish
4. Repeat

Never generate multiple images in parallel or back-to-back. One at a time with a short pause. If a 429 RESOURCE_EXHAUSTED error occurs, wait 60 seconds and retry once.

**Full pipeline — run ALL steps in order for every image:**

**Step 1 — Generate image:**
```
gemini_generate_image → result auto-saved to temp file → Python decodes to PNG on disk
```
See instructions above for the Python decode snippet. Save the PNG to `outputs/{brand}/posts/{Platform}/` immediately.

**Step 2 — Text overlay (gradient scrim + headline + subline) — USE PILLOW:**

```python
from PIL import Image, ImageDraw, ImageFont, ImageStat

def add_text_overlay(input_path, output_path, headline, subline, target_w, target_h,
                     text_align='center', text_position='bottom'):
    img = Image.open(input_path).convert('RGBA')
    # Scale and center-crop to exact canvas
    r = img.width / img.height; tr = target_w / target_h
    if r > tr: nw = int(img.width * target_h / img.height); nh = target_h
    else: nw = target_w; nh = int(img.height * target_w / img.width)
    img = img.resize((nw, nh), Image.LANCZOS)
    img = img.crop(((nw-target_w)//2, (nh-target_h)//2, (nw-target_w)//2+target_w, (nh-target_h)//2+target_h))

    pad = int(target_w * 0.06)
    # Per-canvas insets — Story uses Meta safe zones only; Feed uses pad-derived only.
    # is_story: True only for 9:16 (ratio ≥ 1.7). IG portrait 4:5 = 1.25 → feed treatment.
    # target_h > target_w is NOT sufficient: IG portrait (1080×1350) would wrongly get 9:16 safe zones.
    is_story = (target_h / target_w) >= 1.7
    if is_story:
        # Meta-spec safe zones (matches "central 1080x1420 of 1080x1920" rule)
        top_inset    = int(target_h * 0.14)   # Stories profile header clearance
        bottom_inset = int(target_h * 0.13)   # Meta bottom safe zone
        side_inset   = int(target_w * 0.13)   # Meta side safe zone
        scrim_fade   = 0                       # no extra pad transition past text edge
    else:
        # Feed — asymmetric: top/bottom/scrim_fade = pad // 2; sides = pad + pad // 2.
        # Sides need extra room: IG profile-grid view recrops square feed posts to 4:5,
        # trimming ~34 px per side. pad // 2 (~32 px) gets entirely consumed by that crop.
        # Logo (add_logo) stays at uniform pad // 2 — text and logo diverge on sides by design.
        # Do NOT "simplify" sides back to pad // 2 — that regressed v2.4.8 hardening (see v2.5.2).
        top_inset    = pad // 2
        bottom_inset = pad // 2
        side_inset   = pad + pad // 2          # ~9% of width; survives IG profile-grid crop
        scrim_fade   = pad // 2               # gradient transition past the text edge

    hs = max(36, int(target_w * 0.048))
    ss2 = max(22, int(target_w * 0.026))
    try:
        fh = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', hs)
        fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', ss2)
    except:
        fh = fs = ImageFont.load_default()

    # Pixel-width-aware wrapping — no character-count heuristic.
    # Uses a throwaway draw context for measurement; avail_w is exact canvas space.
    _tmp = Image.new('RGBA', (target_w, target_h))
    draw_tmp = ImageDraw.Draw(_tmp)
    avail_w = target_w - 2 * side_inset

    def wrap_to_fit(text, font, max_w, draw):
        """Wrap text word-by-word so no rendered line exceeds max_w pixels."""
        words = text.split()
        lines = []
        current = ""
        for word in words:
            test = (current + " " + word).strip()
            if draw.textbbox((0, 0), test, font=font)[2] <= max_w:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines or [text]

    h_lines = wrap_to_fit(headline, fh, avail_w, draw_tmp)
    s_lines = wrap_to_fit(subline,  fs, avail_w, draw_tmp)

    # Measure total text block height
    line_gap = int(hs * 0.3)
    block_h = len(h_lines) * (hs + line_gap) + int(hs * 0.5) + len(s_lines) * (ss2 + line_gap)

    # Anchor text + scrim based on text_position. Scrim runs from the canvas edge (on text side)
    # past the text by `scrim_fade`, so the gradient fades into the un-darkened image.
    if text_position == 'bottom':
        text_bottom  = target_h - bottom_inset
        text_y       = text_bottom - block_h
        scrim_top    = text_y - scrim_fade
        scrim_bottom = target_h
    else:  # 'top'
        text_y       = top_inset
        text_bottom  = text_y + block_h
        scrim_top    = 0
        scrim_bottom = text_bottom + scrim_fade

    # Geometric invariants — crash loudly on regression instead of shipping a silently-wrong image.
    assert text_y >= 0, \
        f"text overflows canvas top — block_h={block_h} too large for available space; reduce headline/subline length or font size"
    assert text_bottom <= target_h, \
        f"text overflows canvas bottom — block_h={block_h} too large for available space; reduce headline/subline length or font size"
    if text_position == 'bottom':
        assert text_y + block_h == target_h - bottom_inset, \
            f"text bottom must equal target_h - bottom_inset (got {text_y + block_h}, expected {target_h - bottom_inset})"
        assert scrim_top + scrim_fade == text_y, \
            f"scrim must have exactly `scrim_fade` above text (scrim_top={scrim_top}, text_y={text_y}, scrim_fade={scrim_fade})"
        assert scrim_bottom == target_h, \
            f"gradient must run to canvas bottom for bottom-anchored text (scrim_bottom={scrim_bottom}, target_h={target_h})"
    else:  # 'top'
        assert text_y == top_inset, \
            f"text top must equal top_inset (got text_y={text_y}, expected {top_inset})"
        assert scrim_top == 0, \
            f"gradient must start at canvas top for top-anchored text (scrim_top={scrim_top})"
        assert scrim_bottom - scrim_fade == text_bottom, \
            f"scrim must have exactly `scrim_fade` below text (scrim_bottom={scrim_bottom}, text_bottom={text_bottom}, scrim_fade={scrim_fade})"

    # Sample the underlying image in the actual text zone BEFORE the scrim is applied.
    sample = img.convert('RGB').crop((
        side_inset, max(0, text_y),
        target_w - side_inset, min(target_h, text_bottom)
    ))
    bg_brightness = ImageStat.Stat(sample.convert('L')).mean[0]
    # The heavier scrim (max alpha 230/255) darkens this zone to ~40% of the original brightness on average.
    # Choose text colors based on the estimated post-scrim brightness.
    if bg_brightness * 0.40 < 85:   # dark result → light text
        headline_color = (255, 255, 255, 255)   # white
        subline_color  = (236, 72, 153, 255)    # pink #ec4899
    else:                            # light result → dark text
        headline_color = (15, 15, 15, 255)      # near-black
        subline_color  = (185, 28, 96, 255)     # dark pink #be185d

    # Gradient direction depends on which end the text is on:
    #   text at bottom → alpha 0 at scrim_top, 230 at scrim_bottom (dark zone is bottom)
    #   text at top    → alpha 230 at scrim_top, 0 at scrim_bottom (dark zone is top)
    scrim = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))
    ds = ImageDraw.Draw(scrim)
    span = max(1, scrim_bottom - scrim_top)
    for y in range(scrim_top, scrim_bottom):
        if text_position == 'bottom':
            alpha = int(230 * (y - scrim_top) / span)
        else:  # top
            alpha = int(230 * (scrim_bottom - y) / span)
        ds.line([(0, y), (target_w, y)], fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(img, scrim)
    draw = ImageDraw.Draw(img)

    def get_x(lw):
        if text_align == 'left':  return side_inset
        if text_align == 'right': return target_w - lw - side_inset
        return (target_w - lw) // 2  # center

    # Draw headline lines
    for line in h_lines:
        bbox = draw.textbbox((0, 0), line, font=fh)
        lw = bbox[2] - bbox[0]
        draw.text((get_x(lw), text_y), line, font=fh, fill=headline_color)
        text_y += hs + line_gap

    text_y += int(hs * 0.3)  # gap between headline and subline

    # Draw subline lines
    for line in s_lines:
        bbox = draw.textbbox((0, 0), line, font=fs)
        lw = bbox[2] - bbox[0]
        draw.text((get_x(lw), text_y), line, font=fs, fill=subline_color)
        text_y += ss2 + line_gap

    img.convert('RGB').save(output_path, 'PNG', optimize=True)
```

Font: DejaVuSans-Bold for headline, DejaVuSans for subline.
Text colors are chosen adaptively by sampling the image brightness in the text zone before the scrim is applied:
- **Dark background** (estimated post-scrim brightness < 85): white headline `#ffffff` + pink subline `#ec4899`
- **Light background** (estimated post-scrim brightness ≥ 85): near-black headline `#0f0f0f` + dark-pink subline `#be185d`

`text_align` (left/center/right) and `text_position` (top/bottom) both come from the day-of-week rotation. On 9:16 canvases Meta safe zones (14% top / 13% bottom / 13% sides) position the text and the gradient meets the text edge with no transition padding. On feed canvases the inset is **asymmetric**: top + bottom + scrim_fade are `pad // 2` (~3% of width, ~32–36 px), but sides are `pad + pad // 2` (~9% of width, ~96–108 px) so the text survives Instagram's profile-grid 4:5 recrop (~34 px side trim). `pad // 2` of gradient fade extends past the text edge into the un-darkened image. The dark end of the scrim always sits on the same end as the text — bottom-anchored text → gradient hits `target_h`; top-anchored text → gradient starts at y=0.

| Format | target_w | target_h |
|--------|----------|----------|
| LinkedIn Post | 1200 | 628 |
| Facebook Post | 1200 | 630 |
| Instagram Post (square) | 1080 | 1080 |
| Instagram Post (portrait) | 1080 | 1350 |
| Instagram / Facebook Story | 1080 | 1920 |

**Day-of-week layout rotation** (text and logo always on opposite vertical ends):
| Day | text_align | text_position | logo_position |
|-----|------------|---------------|---------------|
| Mon | left | bottom | top-right |
| Tue | center | top | bottom-left |
| Wed | right | bottom | top-right |
| Thu | left | top | bottom-left |
| Fri | center | bottom | top-right |
| Sat | right | top | bottom-left |

**Step 3 — Logo overlay (brand mark) — USE PILLOW:**

```python
from PIL import Image

def add_logo(image_path, output_path, logo_path, position='top-right', scale=0.18):
    img = Image.open(image_path).convert('RGBA')
    logo = Image.open(logo_path).convert('RGBA')
    logo = logo.crop(logo.getbbox())                # strip transparent padding BEFORE dimension calc
    cropped_w, cropped_h = logo.size                # capture for aspect-ratio assertion
    assert cropped_w > 0 and cropped_h > 0, \
        f"cropped logo has zero dimension ({cropped_w}x{cropped_h}); check logo file integrity"
    w, h = img.size
    logo_w = int(w * scale)
    logo_h = int(logo.height * logo_w / logo.width)  # aspect ratio preserved from cropped logo
    # Geometric invariant — fail loudly if anyone reorders the crop/resize and distorts the mark.
    assert abs((logo_w / logo_h) - (cropped_w / cropped_h)) / (cropped_w / cropped_h) < 0.01, \
        f"logo resize distorts aspect ratio — logo.crop(getbbox()) must run BEFORE logo_w/logo_h " \
        f"(cropped {cropped_w}/{cropped_h}={cropped_w/cropped_h:.3f}, resize {logo_w}/{logo_h}={logo_w/logo_h:.3f})"
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
    # Per-canvas logo insets — Story uses Meta safe zones; Feed uses uniform pad // 2.
    # Logo can sit at top OR bottom (selected by `position`); insets defined for both ends.
    pad = int(w * 0.06)                 # matches definition in add_text_overlay
    is_story = (h / w) >= 1.7
    if is_story:
        top_inset    = int(h * 0.14)   # Stories profile header clearance
        bottom_inset = int(h * 0.13)   # Meta bottom safe zone
        side_inset   = int(w * 0.13)   # Meta side safe zone
    else:
        top_inset    = pad // 2
        bottom_inset = pad // 2
        side_inset   = pad // 2
    top_y    = top_inset
    bottom_y = h - logo_h - bottom_inset
    positions = {
        'top-right':    (w - logo_w - side_inset, top_y),
        'top-left':     (side_inset, top_y),
        'bottom-right': (w - logo_w - side_inset, bottom_y),
        'bottom-left':  (side_inset, bottom_y),
    }
    x, y = positions[position]
    img.paste(logo, (x, y), logo)
    img.convert('RGB').save(output_path, 'PNG', optimize=True)
```

Logo path: `brands/{brand}/logo.png`. Scale: 0.18. `position` from day-of-week rotation — `"top-right"` (Mon/Wed/Fri, paired with bottom text) or `"bottom-left"` (Tue/Thu/Sat, paired with top text). Logo and text always occupy opposite vertical ends; never both top, never both bottom.
This is the standard final step for ALL social images.

**Step 3b — Visual verification (MANDATORY before uploading to Zernio):**

Read the final image and visually inspect it. Check every item below. Determine canvas type first: **9:16** = 1080×1920 (Story); **Feed** = all other formats.

**Text — position and inset (9:16 = Meta safe zones; feed = asymmetric pad-derived — larger sides):**
- [ ] Text block is at the **top OR bottom** matching `text_position` from the day-of-week rotation — never both ends, never mid-canvas
- [ ] Text alignment matches the day-of-week rotation: left (Mon/Thu), center (Tue/Fri), right (Wed/Sat)
- [ ] **9:16 (text at bottom — Mon/Wed/Fri):** bottom of text block is ~250 px (13%) from canvas bottom — Meta bottom safe zone
- [ ] **9:16 (text at top — Tue/Thu/Sat):** top of text block is ~269 px (14%) from canvas top — clears Stories profile header
- [ ] **9:16:** text stays within ~140 px (13%) side margins — Meta side safe zone
- [ ] **Feed:** text has `pad // 2` (~32–36 px) inset on top + bottom, and `pad + pad // 2` (~96–108 px) inset on sides — sides intentionally larger to survive IG profile-grid 4:5 recrop (~34 px side trim)
- [ ] **Gradient scrim reaches the canvas edge on the text side** — bottom-anchored text → scrim hits `target_h`; top-anchored text → scrim starts at y=0

**Text — legibility and color:**
- [ ] Headline is fully visible — no characters clipped at left, right, or bottom
- [ ] Subline is fully visible — not cut off
- [ ] Text color scheme is correct for the background: **dark zone** → white headline + pink `#ec4899` subline; **light zone** → near-black headline + dark-pink `#be185d` subline
- [ ] Scrim gradient provides enough contrast — text is clearly readable against the background

**Logo — position (always opposite end from text):**
- [ ] Logo position matches the day-of-week rotation: top-right (Mon/Wed/Fri, paired with bottom text); bottom-left (Tue/Thu/Sat, paired with top text)
- [ ] Logo and text occupy **separate vertical ends** — never both top, never both bottom
- [ ] **9:16:** logo top = `int(h * 0.14)` (~269 px), logo bottom = `h - logo_h - int(h * 0.13)` (~250 px from bottom), logo sides = `int(w * 0.13)` (~140 px) — Meta safe zones
- [ ] **Feed:** logo top + bottom + side = `pad // 2` (~32–36 px) — uniform pad-derived margin
- [ ] Logo is fully visible — not clipped by any edge
- [ ] Logo has sufficient contrast against the background behind it
- [ ] Logo corner margin looks visually balanced — top/bottom gap ≈ side gap

**Overall composition:**
- [ ] Text and logo occupy opposite vertical ends per the day-of-week rotation — they do not overlap and are visually separated
- [ ] The image looks intentional and on-brand — not accidental or broken

**If any check fails, fix before uploading:**

| Issue | Fix |
|---|---|
| **Text at wrong end of canvas** | Pass `text_position='top'` or `'bottom'` per the day-of-week rotation; re-render |
| **Text too close to bottom edge (9:16)** | Verify `bottom_inset = int(target_h * 0.13)` (Meta bottom safe zone); re-render |
| **Text too close to top edge (9:16)** | Verify `top_inset = int(target_h * 0.14)` (Meta-spec — Stories profile header); re-render |
| **Text too close to sides (9:16)** | Verify `side_inset = int(target_w * 0.13)` (Meta side safe zone); re-render |
| **Gradient has visible gap at canvas edge** | Bottom text → `scrim_bottom == target_h`; top text → `scrim_top == 0`. Gradient must reach the canvas edge on the text side; re-render |
| **Feed text top/bottom not at `pad // 2`** | Confirm feed branch sets `top_inset = bottom_inset = scrim_fade = pad // 2`; re-render |
| **Feed text sides too tight / clipped in IG profile grid** | Confirm feed branch sets `side_inset = pad + pad // 2` (~96–108 px). Do NOT "simplify" to `pad // 2` — that gets consumed by IG's profile-grid 4:5 recrop (~34 px side trim). See v2.5.2 changelog. Re-render. |
| Wrong text alignment for the day | Check day-of-week and pass correct `text_align` (`'left'`/`'center'`/`'right'`) to `add_text_overlay`; re-render |
| Wrong text color scheme | Adjust the brightness multiplier in `add_text_overlay` (change `0.40` up/down to shift the threshold); re-render |
| Subline illegible against busy or light bg | Increase scrim max-alpha — change `230` to `245` in the gradient loop; re-render |
| Headline clipped at sides | Increase `side_inset` by 20 px and re-render |
| Headline clipped at top/bottom of canvas (block too tall for canvas) | Reduce `hs` by 10% and re-render — happens when `block_h > target_h - top_inset - bottom_inset` (the available space between insets), pushing `text_y` negative or `text_bottom` past `target_h` |
| Subline cut off | Reduce `ss2` by 10% and re-render |
| Low text contrast (scrim too light) | Increase scrim opacity — change `230` to `245` in the gradient alpha and re-render |
| Text overlaps logo | Text and logo must occupy opposite vertical ends per the day-of-week rotation. If overlapping despite correct positions (very long text on short canvas), reduce `hs` by 10% to shorten the text block. Re-render. |
| Logo at wrong end | Correct `position` per day-of-week rotation: `top-right` for Mon/Wed/Fri (paired with bottom text); `bottom-left` for Tue/Thu/Sat (paired with top text); re-render |
| Logo and text on same row | Verify the rotation mapping: `text_position` and `logo_position` must always be on opposite vertical ends; re-render |
| Logo positioned wrong | Verify the `is_story` branch in `add_logo`: 9:16 → `top_inset = int(h * 0.14)`, `bottom_inset = int(h * 0.13)`, `side_inset = int(w * 0.13)` (Meta); feed → all three = `pad // 2`; re-render |
| Logo clipped at edge | Reduce `scale` by 0.02 and re-render |
| Logo visually offset (unequal margins) | `add_logo` already crops transparent padding via `logo.crop(logo.getbbox())` before computing dimensions — verify the crop line is present at the top of the function; re-render |
| Logo aspect ratio looks distorted | Confirm `logo.crop(logo.getbbox())` runs BEFORE `logo_w`/`logo_h` are computed (cropping after the resize-target calc distorts aspect); re-render |
| Logo too small to read | Increase `scale` to 0.22 and re-render |
| Logo too large / dominates image | Reduce `scale` to 0.14 and re-render |
| Logo blends into background | Add white semi-transparent backing: `bg = Image.new('RGBA', (logo_w + pad, logo_h + pad), (255,255,255,160))`, paste at `(x - pad//2, y - pad//2)` before pasting logo |
| Logo over busy image area | Switch to opposite corner (e.g. `top-right` → `top-left`) where background is calmer; re-render |

Re-render until all checks pass. Only then proceed to upload.

**Step 4 — Upload to Zernio (for social posts):**

⚠️ **Always upload `_final.png`. Steps 2 (text overlay) and 3 (logo overlay) must both complete before uploading. Never upload the raw Gemini background or `_with_text.png`.**

The `_final.png` is a **local file**, so upload it programmatically via `media_get_media_presigned_url` — **not** `media_generate_upload_link` (that is a browser-only upload flow and PUTting to it silently fails). Resolve account IDs via `accounts_list` at run start.
```
1. Use Zernio MCP tool `media_get_media_presigned_url`:
   - filename: "SocialPost_11Mar2026.png"
   - content_type: "image/png"
   - size: <file size in bytes>
   → Returns an upload URL (PUT target) + a public URL

2. Use Python requests to upload the file to the presigned URL:
```python
import requests, os
path = 'path/to/_final.png'
presign = media_get_media_presigned_url(filename=os.path.basename(path),
                                        content_type="image/png",
                                        size=os.path.getsize(path))
with open(path, 'rb') as f:
    requests.put(presign["uploadUrl"], data=f, headers={'Content-Type': 'image/png'})
public_url = presign["publicUrl"]
```

3. `validate_media(url=public_url)` → confirm `valid: true`, then use Zernio MCP tool `posts_create` (one call per platform):
   - content: <copy text with hashtags>
   - platform: "<instagram|facebook|linkedin>"   # single string, not an array
   - account_id: "<ZERNIO_ACCOUNTS[platform] / from accounts_list>"
   - media_urls: "<public_url>"                    # comma-separated string for multiple images
   - publish_now: true
   - is_draft: false
```
> Zernio `posts_create` has no `platformSpecificData.contentType` param — Story/Reel content-typing is not expressible on this Gemini image-path; the post publishes as feed content.

**Standard asset sizes and Zernio platform destinations:**
| Format | Canvas | Zernio `platforms` |
|--------|--------|-----------------|
| LinkedIn Post | 1200×628 | `linkedin` |
| Facebook Post | 1200×630 | `facebook` |
| Instagram Post (square) | 1080×1080 | `instagram` |
| Instagram Post (portrait) | 1080×1350 | `instagram` |
| Story (9:16) | 1080×1920 | `instagram` |

**Always save Story to `outputs/{brand}/posts/Instagram/` — naming: append `_Story`.**
e.g. `SocialPost_PainMoment_Story_11Mar2026.png`

Place generated images into the asset HTML using `<img>` tags or reference them in the design spec.

---

## Output format

**Save location — local workspace:**
```
outputs/{brand}/posts/[Platform]/     ← social images
outputs/{brand}/strategy/             ← design specs / HTML mockups
```

**Folder by asset type:**
| Asset Type | Local Folder | Upload to Zernio? |
|---|---|---|
| LinkedIn graphic | `outputs/{brand}/posts/LinkedIn/` | Yes — upload via presign, use `publicUrl` in post |
| Facebook graphic | `outputs/{brand}/posts/Facebook/` | Yes |
| Instagram graphic | `outputs/{brand}/posts/Instagram/` | Yes (required for Instagram) |
| Twitter/X card | `outputs/{brand}/posts/Twitter/` | Yes |
| Banner / display ad | `outputs/{brand}/strategy/` | No — local only |
| HTML/CSS mockup | `outputs/{brand}/strategy/` | No — local only |

**Naming convention:**
```
[AssetType]_[DDMonYYYY].png           ← generated images
[AssetType]_[DDMonYYYY]_spec.md       ← Design spec / HTML mockup
```

Examples:
- `SocialPost_10Mar2026.png`
- `HeroImage_10Mar2026.png`
- `AdCreative_10Mar2026.png`
- `LandingPage_10Mar2026_spec.md`

**Output metadata (for spec files):**
```markdown
---
Date: YYYY-MM-DD
Skill Used: creative-designer
Asset Type: [landing-page | email | ad | social-graphic | one-pager]
Persona: [Persona name]
Campaign: [Campaign name]
Dimensions: [e.g., 1200px × 628px]
Output Format: HTML/CSS | Design Spec
Status: Draft | Final
---
```

---

## Quality checklist

Before finalizing any design output:

**Brand compliance:**
- [ ] Brand visual source resolved in 3-tier order: fb.ai brand kit (`fivebucks_get_brand_kit`, checked first when `FIVEBUCKS_API_KEY` set) → local `brands/{brand}/design-system/` (when present) → `brand.md`; never blocked on a missing key or design-system
- [ ] Colors, fonts, and component styles match the fb.ai brand kit / design-system (when present) or brand.md (when fallback) — never hardcoded
- [ ] Primary brand color used for CTAs and key headings
- [ ] Accent color used sparingly — not dominant
- [ ] No off-brand colors used
- [ ] Typography follows the fb.ai brand kit / design-system font stack OR brand.md Google Fonts (whichever applied)
- [ ] For IG/FB/LinkedIn template formats: if a matching fb.ai template `type` exists (`fivebucks_list_templates`), template-path used (`fivebucks_create_post` → `fivebucks_render_post` → signed URLs passed **directly** as `media_urls`, no re-host, `validate_media` first + local `curl` backup → **Story**: posted one-per-slide per platform, 1-second sleep between slides, 5-second sleep + retry after ~5 consecutive FB posts; **Carousel/single-image**: one `posts_create` per platform with comma-separated `media_urls`); else Gemini-only fallback (Step 4b) documented
- [ ] Template-path: `fivebucks_list_templates` called once and cached; `overrides` built from manifest field keys; direction set per type (`_direction` for meta-story; `direction` for single-image; `coverVariant`/`bodyVariant` for meta-carousel)
- [ ] Template-path: `slide_ids` **omitted** for all types — fb.ai selects slides from the direction override (`_direction` for meta-story/meta-carousel, `direction` for single-image)
- [ ] Template-path: media pool built — `fivebucks_list_media_folders` called once; exact-name match first (case-insensitive); if no match → ALL folders pooled for that type; if no folders → pool empty (not a failure)
- [ ] Template-path: user-provided photo takes precedence over media pool; pool photo used if no user photo; image slots left empty if pool also empty
- [ ] Template-path: Pillow text overlay AND Pillow logo overlay BOTH skipped — gateway render includes all chrome
- [ ] Gemini-only fallback path (Step 4b): Story/Reel full-frame guard applied — `image_prompt` passed to Gemini contains `"fills the ENTIRE frame"` for every 9:16 asset
- [ ] Gemini-only fallback path (Step 4b): Pillow text overlay AND Pillow logo overlay (both inside Step 4b) BOTH applied — Gemini background has no copy and no logo
- [ ] Day-of-week `text_align`, `text_position`, and `logo_position` rotations applied only on the Gemini-only fallback path; not used on template-path

**Layout quality:**
- [ ] Visual hierarchy is clear (headline → subheadline → body → CTA)
- [ ] Adequate white space between sections
- [ ] CTA button is prominent and uses correct brand style
- [ ] Content width respects max 1200px

**Content accuracy:**
- [ ] Copy inside the design matches approved content (no placeholder text in finals)
- [ ] No invented features, pricing, or claims
- [ ] CTA matches the campaign goal

**Technical (for HTML/CSS output):**
- [ ] HTML is valid and semantic
- [ ] No broken links or missing assets
- [ ] Responsive behavior considered for key breakpoints
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "creative-designer"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "assets": [
      {
        "type": "social-image",
        "platform": "Facebook",
        "dimensions": "1200x630",
        "tool": "gemini",
        "avatar": false,
        "file": "<filename>",
        "zernio_uploaded": true
      }
    ],
      "zernio_uploads": 0
  }
```
