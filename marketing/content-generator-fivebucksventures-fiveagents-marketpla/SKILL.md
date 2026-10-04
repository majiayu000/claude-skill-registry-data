---
name: content-generator
description: Daily automated content production — generate copy and images from Notion Social Calendar, publish to Zernio API, update Notion, notify Slack. Runs daily on cron schedule.
allowed-tools: Read, Grep, Glob, Bash
area: Marketing
use_for: "Daily automated content production — generate copy and images from Notion Social Calendar, publish to Zernio API, update Notion, notify Slack"
deps:
  mcp: ["Notion", "Slack", "Zernio"]
  gateway: ["Gemini", "fivebucks (opt — fb.ai templates + media; falls back to Gemini + Pillow; **scope: social_posts**)"]
  files: ["brand.md", "audience.md", "product.md", "design-system/ (opt — local; or fb.ai brand kit via fivebucks_get_brand_kit; brand.md fallback)"]
  env: ["`${BRAND}_NOTION_DB`", "`${BRAND}_ZERNIO_FB/IG/LI`"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.0 | July 12, 2026 |

**Description:** Daily automated content production — generate copy and images from Notion Social Calendar, publish to Zernio API, update Notion, notify Slack

### Change Log

**v2.20.0** — July 12, 2026
- **Declared the fb.ai dependency and its required scope.** fb.ai API keys are now scoped; this skill's `deps.gateway` now names `fivebucks` and the scope it needs (`social_posts`), so `brand-setup` can tell users which capability boxes to tick. No behaviour change — see `agents/link.md` for the scope/error/quota contract.

**v2.19.0** — July 03, 2026
- **Corrected Zernio publish mechanics to the real MCP schema (fixes the v2.18.0 migration bug).** v2.18.0 wrongly repointed `late_presign_upload` → `media_generate_upload_link`, but that Zernio tool is a **browser-only** upload flow — PUTting to it silently fails. Now: **local files** (image-path `_final.png`, Step 5) upload via `media_get_media_presigned_url(filename, content_type, size)`; **fb.ai render signed URLs** (template-path §7) pass **directly** as `media_urls` with no re-host (the publisher fetches/caches at post-creation time, so ~1h expiry is safe within the run); `validate_media(url)` before publish; local `curl` backup after render.
- **`posts_create` signature corrected.** Real params: `content`, `platform` (single string), `account_id`, `media_urls` (comma-separated string — not a `media_items` array), `publish_now`/`is_draft`/`schedule_minutes`. One call per platform (no `platforms[]`). `account_id` always passed, resolved via `accounts_list`.
- **`platformSpecificData.contentType` removed** — no such param on Zernio `posts_create`; image-path posts publish as feed content. Removed the `ZERNIO_CONTENT_TYPE` mapping and the "always pass contentType" rule (Step 5).
- **Media-folder name-mismatch warning added (Step 4c-template §1).** When folders exist but none match the expected template-type names, surface a non-blocking Slack warning recommending a rename; continue with the all-folder pool.

**v2.18.0** — July 01, 2026
- **Zernio migrated to its own MCP (gateway v1.7.4).** Repointed `late_presign_upload` → `media_generate_upload_link` and `late_create_post` → `posts_create` to Zernio's native MCP tool names; dropped the `fiveagents_api_key` param from those calls (Zernio is now OAuth-connected, not gateway-routed); renamed `${BRAND}_LATE_*` env vars to `${BRAND}_ZERNIO_*` and internal `late_*` PublishLog/output fields to `zernio_*`.
- **Gemini image model ID updated (gateway v1.7.4).** `gemini_generate_image` model changed from the retired `gemini-3.1-flash-image-preview` to the GA default `gemini-3.1-flash-image` ("Nano Banana 2").

**v2.12.2** — June 08, 2026
- **Stale `_raw.png` reference removed.** Step 4g cleanup and Quality Checklist both referenced `_raw.png` as an intermediate file to delete — that filename is never created (Gemini backgrounds save to `brands/{brand}/backgrounds/`). Only `_with_text.png` is a real intermediate. Agents following the old instruction silently no-op'd on a non-existent file.
- **`TOOLS.md` dead reference removed.** Step 5 intro said "See TOOLS.md → 'Social Publishing' for account IDs" — that file does not exist; account IDs are documented inline in Step 5 itself.
- **Step 6 `old_str` now matches `"Processing"`.** Fix 2 (Step 5) writes `"Processing"` before `late_create_post`. The previous Step 6 `old_str` was still `"Planned"` — after Fix 2, the Notion row reads `"Processing"` so the Step 6 `update_content` call was silently no-op'ing and the row never reached `"Published"`.
- **Template-path carousel/single-image no longer refers to Step 5.** §7 said "pass `media_items` in `late_create_post` (Step 5)" — Step 5 has an "Image-path only" guard. Reference removed; note added that template-path posts don't proceed to Step 5.
- **`LATE_CONTENT_TYPE` dict now includes `"reel"` key.** Step 5 said "for Reels and Stories" but the dict had no Reel entry. Agents handling a calendar row with Format = `"Reel"` had no contentType to look up.
- **Step 4c routing table + decision logic: Reel row added.** The dimension table listed Reels but Step 4c had no routing entry — Reels fell through to the "Any | Post" catch-all. Now explicit: Reel → always Step 4c-image, 9:16 canvas, `contentType: "reel"`.
- **`add_text_overlay` comment corrected: `ratio ≥ 1.78` → `ratio ≥ 1.7`.** Comment and code disagreed on the Story/Reel detection threshold; code (`>= 1.7`) is authoritative.

**v2.12.1** — May 30, 2026
- **Media pool fallback made explicit.** Restructured the media pool build from a single dense paragraph into a numbered sub-step list so Claude reliably executes both fallback levels during runs: (1) exact folder-name match first, (2) all-folders pool if no exact match, (3) empty pool if no folders. Previously the fallback clauses were buried in prose and skipped in practice, causing posts to publish with no photos despite a media library folder being present.

# SKILL.md — Content Generator

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are a content production agent for the active brand. Your job is to generate copy and images for today's scheduled social media posts from the Notion Social Calendar, save all outputs, update Notion, and notify via Slack.

Runs daily Mon–Sun on cron schedule. Targets posts scheduled for **today** (in the brand's timezone from `brands/{brand}/brand.md` Locale section).

---

## Inputs

- **Social calendar**: Notion Social Media Calendar database — DB ID from env var `{BRAND}_NOTION_DB` (e.g. `FIVEBUCKS_NOTION_DB`)
- **Publishing**: Zernio API — publish immediately (`isDraft: false`, `publishNow: true`)
- **Brand context**: `brands/{brand}/brand.md`, `brands/{brand}/audience.md`, `brands/{brand}/product.md`
- **Mode**: `AUTO_PUBLISH=true` — publish immediately, do NOT save as draft

---

## Step 1 — Find today's posts in Notion

**Target date**: today in the brand's timezone (read from `brands/{brand}/brand.md` Locale section, e.g. `TZ=Asia/Jakarta date '+%d %b %Y'`)

### Find the active Social Calendar page

Use **Notion MCP** to read the calendar. Follow these steps:

> ⚠️ **Never run a bare workspace-wide `notion-search`** (e.g. searching `"SocialCalendar_"` with no `data_source_url` filter). It returns matches from every brand and other unrelated databases in the workspace, and content-generator will publish the wrong brand's content. The search MUST be scoped to the active brand's database.

**1a. Resolve the brand's database to a `collection://` URL, then search inside it:**

The available Notion MCP tools are `notion-fetch` and `notion-search`. Use this two-step pattern:

1. **Fetch the brand's DB to discover its collection URL:**
```
Use mcp__claude_ai_Notion__notion-fetch:
- id: "${BRAND}_NOTION_DB"   # the brand's DB ID from env var, e.g. FIVEBUCKS_NOTION_DB
```
Inspect the response and extract the `collection://` URL — typically returned as `data_sources[0].url` or under a `collection` field. Save it as `data_source_url`.

2. **Search inside that collection:**
```
Use mcp__claude_ai_Notion__notion-search:
- query: "SocialCalendar_"
- data_source_url: <data_source_url from step 1>
- query_type: "internal"
```

This restricts results to pages inside the brand's social calendar DB. From the results, pick the page whose title contains `SocialCalendar_` and whose date range covers today. Title format: `SocialCalendar_DDMon-DDMonYYYY` (e.g. `SocialCalendar_06Apr-11Apr2026`).

**Brand-header validation (mandatory before proceeding):** open the candidate page with `notion-fetch` and confirm the page's parent / database title matches `${BRAND}` — e.g. parent is "Fivebucks Social Media Calendar", not "NPC Office Social Media Calendar". If the brand header doesn't match, abort with a `failed` run log — do not publish content from another brand's calendar.

**Fallback (only if step 1 returns no `collection://` URL):**

If `notion-fetch` on the DB ID does not yield a usable `data_source_url`, fall back to a workspace-wide `notion-search` AND apply the brand-header validation strictly:

```
Use mcp__claude_ai_Notion__notion-search:
- query: "SocialCalendar_ ${BRAND}"   # include brand name to disambiguate
```

Filter every result by checking the page's parent database title contains the brand. Reject any result whose parent does not include the active brand. If no result passes the brand check, log `failed` and exit — never default to the first match.

**1b. Read the table from the chosen page:**

Use `mcp__claude_ai_Notion__notion-fetch` with the page ID to retrieve the page content. Locate the table block (or the page's child database, depending on how the calendar was structured) and extract its `table_row` children. If the table is nested as a child page rather than inline, fetch the child page first.

**1c. Parse rows into post objects:**

Each table row has cells in this order (column index):
`[0] Date`, `[1] Platform`, `[2] Format`, `[3] Topic`, `[4] Persona`, `[5] ContentAngle`, `[6] CTA`, `[7] Hashtags`, `[8] ImageBrief`, `[9] Direction`, `[10] Status`

`Direction` is set by `social-calendar` at planning time and tells content-generator which template variant to use:
- **Story format** (`meta-story`): one of `"A"` (Spotlight Dark, brand-led), `"B"` (Editorial Stat, single big claim), `"C"` (Cream Press, case studies / testimonials). Maps to the `_direction` override.
- **Carousel format** (`meta-carousel`): one of `"type-allnumbers"` (default), `"sticker-editorial"`, `"editorial-mixed"`, or whatever `coverVariant-bodyVariant` combination the brand's template supports.
- **Single-image formats** (`linkedin-post`, `meta-post`): `"A"` / `"B"` / `"C"` — maps to the un-prefixed `direction` override.
- **Formats with no matching fb.ai template**: leave blank — Direction does not apply.

If Direction is blank for a Story / Carousel / single-image post, default to `"A"` (story / single-image) or `"type-allnumbers"` (carousel) and log a warning — the calendar should have assigned one. There is no separate slide column: fb.ai selects the slide(s) from the direction override at render time (see Step 4c-template §6).

Skip the header row (index 0). Filter rows where:
- `Date` matches today's date (in brand timezone)
- `Status` == `"Planned"`

Save each row's block ID as `_row_id` — needed for Step 6 status update.

If no matching rows, log "No posts scheduled for [date]" and exit.

---

## Step 2 — Read brand context

Read before writing any copy:
- `brands/{brand}/brand.md` — voice, tone, approved phrases
- `brands/{brand}/audience.md` — persona pain points and triggers
- `brands/{brand}/product.md` — features, pricing, differentiators

Read before generating any image — **all optional, never block on missing folders:**
- **Brand visual identity for the Gemini-only image-path** — resolve the color/font source in this 3-tier order, feeding the Gemini prompt aesthetic:
  1. **fb.ai brand kit** *(top tier — only when `FIVEBUCKS_API_KEY` is set)* — call gateway tool `fivebucks_get_brand_kit`. If it returns non-null, use its color tokens (HEX) + typography as the authoritative source — resolve fields via the Brand kit field map in `agents/link.md` (secondary→`tokens.colors.accent`, text→`tokens.colors.dark`, fonts from `tokens.fonts.heading`/`body`; the kit has no separate `secondary` or font weight scale). Returns null when no kit is uploaded — fall through to tier 2.
  2. **brands/{brand}/design-system/** *(local folder — when the fb.ai kit is null or `FIVEBUCKS_API_KEY` is unset; the free baseline)* — Claude Design visual system (colors, fonts, components, spacing). When present, informs the Gemini-only image-path's prompt aesthetic.
  3. **brands/{brand}/brand.md** — the Colors and Voice & Tone sections plus the Google Font names captured in brand-setup Step 4. Universal fallback when neither of the above is available.
- **Social templates on fb.ai** — the brand's Claude-designed social templates live on fb.ai (uploaded via the dashboard in brand-setup Step 4c), **not on disk**. Discover them with the gateway tool `fivebucks_list_templates` (needs the brand's fb.ai key in the vault under service `fivebucks` — `FIVEBUCKS_API_KEY`). Each entry has an `id`, a `type` (`meta-carousel` | `meta-story` | `linkedin-post` | `meta-post`), `dimensions`, and a `manifest` (editable fields + image slots + slide IDs). Used by Step 4c-template; **cache the list for the whole run** (don't call per post).

If no matching fb.ai template exists for the post's format, fall back to the Gemini-only path (Step 4c-image) — sourcing colors/fonts via the same 3-tier order (fb.ai brand kit when the key is set → local `design-system/` → brand.md colors/voice). Never log a `failed` run for missing visual assets.

---

## Step 3 — Write copy for each post

For each post, generate:

1. **Hook** (first line) — must stop the scroll; persona-specific pain point
2. **Body** (2–4 short paragraphs) — one key insight per paragraph, no fluff
3. **CTA** — from the calendar's CTA field; match to campaign goal
4. **Hashtags** — use calendar hashtags; add 1–2 relevant extras if needed

### Copy format by platform
| Platform | Hook | Body | CTA | Total length |
|---|---|---|---|---|
| LinkedIn | Bold stat or provocative question | 3–4 paragraphs, professional tone | Text + link | ~1200 chars |
| Facebook | Relatable pain moment | 2–3 short paragraphs, conversational | Short CTA | ~800 chars |
| Instagram | 3–5 word hook only | Bullet points or very short copy | "Link in bio" | ~300 chars |

**For Stories**: caption text is NOT displayed (Stories are visual-only). Still write a production script for the `_copy.md` file, but send minimal text to Zernio (just hashtags or empty string).

### Naming convention for output files
```
outputs/{brand}/posts/[Platform]/[TopicSlug]_[DDMonYYYY]_copy.md
```
Examples:
- `outputs/{brand}/posts/LinkedIn/AISearchSEOFoundations_12Mar2026_copy.md`
- `outputs/{brand}/posts/Facebook/Replace5Tools_12Mar2026_copy.md`

**Always overwrite existing files** — never skip because a file already exists.

### Step 3b — Generate structured `_copy.json` for template-path posts

For posts that will render via the template-path (a matching fb.ai template exists for the post's format — see Step 4c), produce a structured copy artifact alongside `_copy.md`:

```
outputs/{brand}/posts/[Platform]/[TopicSlug]_[DDMonYYYY]_copy.json
```

The JSON's keys MUST match the template's **fb.ai manifest field keys** (`fivebucks_get_template` → `manifest.fields[].key`) — the canonical key set + per-key character budgets per type are documented in `content-creation/SKILL.md` ("template copy contracts"). Read those budgets before writing.

Map the post's hook/body/CTA (from Step 3) into the template's structure per type:

- **meta-carousel** (6 slides): Cover (`cover_eyebrow` + `cover_title` + `cover_sub`) → 4 sign slides (`s2_kicker`/`s2_title`/`s2_body` through `s5_*`, optional `s2_pullquote`, `s3_stat_value`/`s3_stat_label`, `s5_before`/`s5_after`) → CTA (`cta_eyebrow` + `cta_title` + `cta_sub` + `cta_button`).
- **meta-story** (6 slides): Hook (`s1_*`) → Problem (`s2_*` — eyebrow + headline + 3 pain bullets) → Solution (`s3_*`) → Proof (`s4_*` — 4 stats + quote + author) → Offer (`s5_*` — 4 bullets + pill) → CTA (`s6_*`). Set `_direction` (A/B/C).
- **linkedin-post** (1 slide): `eyebrow` + `headline` + `body` + `stat_value`/`stat_label` + `quote`/`attribution` + `cta_text` + `cta_button`. Set `direction` (A/B/C).
- **meta-post** (1 slide): `eyebrow` + `headline` + `body` + `quote`/`attribution` + `b1`…`b5` + `cta_text` + `cta_button`. Set `direction` (A/B/C).

If the post brief is too thin to fill all required keys, omit those keys — fb.ai seeds the template's defaults for any key you don't send — and log a warning to memory.

**Skip Step 3b for non-template posts** — any post where no matching fb.ai template exists. For those, only `_copy.md` is required; content-generator's image-path uses the headline + body from `_copy.md` directly via Pillow text overlay.

---

## Step 4 — Generate images

**Two image-production paths depending on Format and template availability — see Step 4c for the dispatcher.**
- **Template-path** (Carousel / Story / single-image Post on IG/FB/LinkedIn when a matching fb.ai template exists): fb.ai renders the slides server-side via `fivebucks_render_post`; no Gemini call, no Pillow overlay.
- **Image-path** (any post with no matching fb.ai template, or when the fb.ai render fails / quota is exhausted): Gemini generates the background fresh + Pillow stamps text and logo. Universal fallback — always available.

### Step 4a — Determine canvas dimensions

> **Template-path posts skip this step** — fb.ai renders each template at its own registered dimensions (e.g. 1080×1350 for 4:5 types, 1080×1920 for meta-story). The table below applies only to the **image-path** (Step 4c-image).

| Format | target_w | target_h |
|--------|----------|----------|
| LinkedIn Post | 1200 | 628 |
| Facebook Post | 1200 | 630 |
| Instagram Post (square) | 1080 | 1080 |
| Instagram Post (portrait) | 1080 | 1350 |
| Instagram Reel / Facebook Reel | 1080 | 1920 |
| Instagram Story / Facebook Story | 1080 | 1920 |

**Per-canvas insets — Story/Reel uses Meta safe zones only; Feed text uses asymmetric pad-derived values (larger sides); Feed logo uses uniform `pad // 2`.**

`pad = int(target_w * 0.06)` (~6% of canvas width). On 9:16 text and logo use the same Meta safe zones. On feed they diverge on **sides only** — text needs extra side clearance to survive IG profile-grid 4:5 recrop (~34 px side trim).

| Canvas | Element | Top | Bottom | Sides | Scrim fade |
|---|---|---|---|---|---|
| 9:16 Story/Reel (1080×1920) | text + logo | `int(target_h * 0.14)` (~269 px) | `int(target_h * 0.13)` (~250 px) | `int(target_w * 0.13)` (~140 px) | `0` |
| All feed formats (IG, FB, LinkedIn, X) | **text** | `pad // 2` (~32–36 px) | `pad // 2` | **`pad + pad // 2` (~96–108 px)** | `pad // 2` |
| All feed formats (IG, FB, LinkedIn, X) | logo | `pad // 2` | `pad // 2` | `pad // 2` | n/a |

**Annotations:**
- **Story/Reel (9:16) — Meta safe zones only.** Top 14% clears the Stories profile header; bottom 13% clears the Reels UI stack; sides 13% clear the Reels right-rail action buttons. `scrim_fade = 0` keeps the gradient flush to the safe-zone boundary with no transition padding (no `pad` anywhere in 9:16 geometry).
- **Feed text — asymmetric.** Top, bottom, and scrim_fade all `pad // 2` (~32–36 px). Sides `pad + pad // 2` (~96–108 px) — Instagram's profile-grid view recrops square feed posts to 4:5 portrait, trimming ~34 px per side; the extra side inset guarantees text survives that crop with visible breathing room. **Do not "simplify" feed text back to uniform `pad // 2`** — that regressed v2.4.8 hardening (see v2.5.2 changelog).
- **Feed logo — uniform `pad // 2`.** All four sides ~32–36 px. Logo is small relative to canvas, so the IG profile-grid crop doesn't impact it the way it impacts text; uniform pad-derived inset reads as intentional corner placement.
- **Gradient scrim direction depends on `text_position`.** Bottom-anchored text → scrim runs `scrim_top → target_h` (alpha 0→230, dark zone at bottom). Top-anchored text → scrim runs `0 → text_bottom + scrim_fade` (alpha 230→0, dark zone at top). The dark zone is always on the same end as the text.

### Step 4b — Day-of-week layout rotation

Determine the day-of-week for the post date, then apply:

| Day | text_align | text_position | logo_position |
|-----|------------|---------------|---------------|
| Mon | left | bottom | top-right |
| Tue | center | top | bottom-left |
| Wed | right | bottom | top-right |
| Thu | left | top | bottom-left |
| Fri | center | bottom | top-right |
| Sat | right | top | bottom-left |

**Text and logo are always on opposite vertical ends** — never on the same row. Mon/Wed/Fri = bottom text + top-right logo; Tue/Thu/Sat = top text + bottom-left logo. `text_align` cycles left → center → right across days.

⚠️ **The day-of-week rotation table applies only on the Gemini-only image-path (Step 4c-image).** On the template-path (Step 4c-template) all text, logo, kicker numerals, and CTA chrome are produced by the React template's render — Pillow text overlay and logo overlay are both skipped, and neither `text_align` nor `logo_position` rotation has any effect on template-path posts.

### Step 4c — Choose asset type: Image or Video

Check the post `Format` from the calendar. "A `<type>` template exists" means the cached `fivebucks_list_templates` result (Step 4c-template, step 1) includes an entry with that `type`.

| Platform | Format | Asset Type | Tool |
|---|---|---|---|
| FB/IG | Carousel | Static images | If a `meta-carousel` template exists on fb.ai → **Step 4c-template**. Else → **Step 4c-image** (Gemini background → text overlay → logo). |
| FB/IG | Story | Static image | If a `meta-story` template exists → **Step 4c-template**. Else → **Step 4c-image** (publish as Story). |
| FB/IG | Reel | 9:16 static image | **Step 4c-image** (Gemini background → text overlay → logo; `aspect_ratio: "9:16"`). No fb.ai template type exists for Reels, and Zernio `posts_create` cannot set a Reel content-type — the 9:16 image publishes as a feed post. |
| FB/IG | Post (single image) | Static image | If a `meta-post` template exists → **Step 4c-template**. Else → **Step 4c-image**. |
| LinkedIn | Post | Static image | If a `linkedin-post` template exists → **Step 4c-template**. Else → **Step 4c-image**. |
| Any | Post | Static image | **Step 4c-image** (no matching template) |

**Decision logic:**
1. Check the `Format` field from the Notion calendar.
2. If Format = `"Reel"` AND platform ∈ {Instagram, Facebook} → use **Step 4c-image** (9:16 canvas). No fb.ai template type exists for Reels, and Zernio `posts_create` cannot set a Reel content-type — the 9:16 image publishes as a feed post.
3. If Format = `"Carousel"` AND platform ∈ {Instagram, Facebook} AND a `meta-carousel` template exists → use **Step 4c-template**.
4. If Format = `"Story"` AND platform ∈ {Instagram, Facebook} AND a `meta-story` template exists → use **Step 4c-template**.
5. If Format = `"Post"` AND platform ∈ {Instagram, Facebook} AND a `meta-post` template exists → use **Step 4c-template**.
6. If Format = `"Post"` AND platform = LinkedIn AND a `linkedin-post` template exists → use **Step 4c-template**.
7. All other formats (or no matching template) → use **Step 4c-image** (Gemini-generated background + text overlay + logo).

### Step 4c-template — Render via fb.ai (`fivebucks_*`)

Use this path when a matching fb.ai template exists for the post's format (see Step 4c). Rendering is server-side on fb.ai — **no local Playwright, no Gemini-for-slots, no Zernio slot presign**. Templates render their own images and tint overlay natively; the skill just supplies copy (and optionally photos) and collects rendered PNGs.

**No Pillow text overlay, no Pillow logo overlay on this path.** The skill's jobs: pick the template by `type` → build copy `overrides` → create a post → render → re-host the PNGs on Zernio for publishing.

Requires the brand's fb.ai key in the vault under service `fivebucks` (`FIVEBUCKS_API_KEY`, brand-setup Step 7). Each render consumes **1.0 CONTENT_GENERATION quota** on fb.ai regardless of slide count.

**Steps:**

#### 1. List templates (cache for the run)

```
Use gateway MCP tool fivebucks_list_templates:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
```

Returns an array of templates, each with `id`, `name`, `type` (`meta-carousel` | `meta-story` | `linkedin-post` | `meta-post`), `dimensions`, and `manifest`. Build a `type → {id, manifest}` map and **cache it for the entire daily run** — don't call per post. If no template of the type this post needs exists, fall back to **Step 4c-image**.

Also at run start, build the **media pool** (cache alongside the template list — call once, not per post). Execute these sub-steps in order — do not skip the fallbacks:

1. **Call `fivebucks_list_media_folders` once** (cache the result alongside the template list):

   ```
   Use gateway MCP tool fivebucks_list_media_folders:
   - fiveagents_api_key: ${FIVEAGENTS_API_KEY}
   ```

2. **Match each returned folder to a template type by exact name (case-insensitive):**

   | Folder name | Template type |
   |---|---|
   | `LinkedIn Post` | `linkedin-post` |
   | `Meta Story` | `meta-story` |
   | `Meta Carousel` | `meta-carousel` |
   | `Meta Post` | `meta-post` |

3. **For each matched folder:** call `fivebucks_list_media_files` → store the file list as `media_pool[type]`.

4. **Fallback — no exact match:** if a template type has no folder with a matching name, combine **ALL** returned folders — call `fivebucks_list_media_files` for every folder and merge into a single list. Use that combined list as `media_pool[type]`. (Do not leave the type's pool empty just because its named folder is missing.) **When this fallback fires** (folders exist but none match the expected names `LinkedIn Post` / `Meta Story` / `Meta Carousel` / `Meta Post`), surface a non-blocking warning in the Slack notification recommending the user rename folders to the expected names so per-type photo injection works correctly. Do not fail — continue with the all-folder pool.

5. **Fallback — no folders at all:** if `fivebucks_list_media_folders` returns an empty list, set `media_pool` to empty. Photo injection is skipped for the entire run — this is normal, not an error.

6. **On any API error** from `fivebucks_list_media_folders`: skip silently, treat the pool as empty. Never fail or warn the run.

#### 2. Read the manifest

From the cached entry (or `fivebucks_get_template` for the freshest copy) read:
- `manifest.fields[]` — each `{ key, label, group, type, default, bound?, options? }`. **Skip** fields with `bound === false` (hardcoded — editing has no effect). For `type: 'select'` fields, send only a value from `options`. For `type: 'image'` slots, the value is `""` or `"media:{fileId}"`, with companion `{slot}_image_position` / `{slot}_image_fit` selects.
- `manifest.slides[]` — slide IDs. The render returns one PNG per slide, in slide order.
- `manifest.theme` — informational (the template bakes its own overlay: `dark` = 40% black, `light` = 50% white). Use it to pick photos that contrast.

#### 3. Build the `overrides` payload (copy → manifest field keys)

Flat key→value map. Send only fields you're changing; fb.ai seeds defaults for the rest. Use the per-type key sets in `content-creation/SKILL.md` (or the Step 3b `_copy.json`). Set direction:
- **meta-story**: `_direction` = `"A"` / `"B"` / `"C"` (default `"A"` — renders 6 slides). **Never `"all"`** (renders 18 slides and burns the same 1.0 quota at once).
- **linkedin-post / meta-post**: the un-prefixed `direction` = `"A"` / `"B"` / `"C"` (picks the single slide's layout).
- **meta-carousel**: `coverVariant` / `bodyVariant` from the post's Direction field (e.g. `"type-allnumbers"` → `coverVariant="type"`, `bodyVariant="allnumbers"`) if the manifest exposes them.

#### 4. Assign photos from the media pool

Use `media_pool[type]` built in Step 1. For this post's template type:

- **Pool non-empty** → inject photos into image slots:
  - `meta-carousel` / `meta-story` body slots `s2_image`…`s5_image`: cycle through the pool (up to 4 photos; reuse from the start if the pool has fewer than 4). Use a different photo per slot when possible.
  - `linkedin-post` / `meta-post`: assign one photo to `bg_image`.
  - For each assigned slot add companion overrides: `"<slot>_image_position": "center"` and `"<slot>_image_fit": "cover"`.
- **Pool empty** → leave all image slots empty — the template renders its own branded placeholder/gradient. Never fail or warn for an empty pool; this is the normal no-media fallback.

#### 5. Create the post

```
Use gateway MCP tool fivebucks_create_post:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- template_id: "<id from step 1>"
- name: "[Brand] [Platform] [Format] — [Topic] — [Date]"
- overrides: { ...copy + direction (+ image slots from step 4)... }
→ Returns the new post id
```

To adjust copy or add photos after creating, call `fivebucks_update_post` (post_id, overrides) — overrides merge.

#### 6. Render — fb.ai selects the slides from the Direction

**Omit `slide_ids` for every template type.** fb.ai filters direction-based templates by the post's direction override **server-side** and screenshots only the right slide(s). You set the direction in `overrides` (Step 3); `fivebucks_render_post` returns the correct PNGs in slide order. Don't pass `slide_ids` to choose a direction — that's fb.ai's job now (`slide_ids` remains only as an optional way to render a specific subset, which you never need here).

| Template `type` | Direction override (set in Step 3) | What fb.ai renders |
|---|---|---|
| `meta-story` | `_direction` = A/B/C | that direction's 6 slides (`all` = 18 — **never** use) |
| `meta-carousel` | `coverVariant`/`bodyVariant` (style) | all 6 slides |
| `linkedin-post` | `direction` = A/B/C | the 1 slide for that direction |
| `meta-post` | `direction` = A/B/C | the 1 slide for that direction |

```
Use gateway MCP tool fivebucks_render_post:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- post_id: "<id from step 5>"
- (omit slide_ids)
→ Returns 1-hour signed PNG URL(s), one per rendered slide, in slide order
```
meta-story renders the 6 slides of the `_direction` set (A/B/C — **never `all`**, which renders 18 slides and burns the same 1.0 quota). meta-carousel renders all 6. linkedin-post / meta-post each return the single slide matching `direction`. fb.ai resolves any `"media:{fileId}"` overrides server-side and the template renders the photo natively — nothing else to wire.

#### 7. Publish — Story vs other formats

Pass the `fivebucks_render_post` signed URLs **directly** to `posts_create` as `media_urls` — **do not re-host**. The publisher fetches and caches each image at post-creation time (not at publish time), so the ~1-hour signed-URL expiry is safe as long as `posts_create` runs in the same run as the render. `validate_media(url)` each URL first, and `curl` a local backup of each slide before publishing.

⚠️ **Do not use `media_generate_upload_link` here** — it is a browser-only upload flow (returns a human upload-page URL, not a programmatic presign) and PUTting to it silently fails. It was mis-used by the v2.18.0 migration. Resolve account IDs via `accounts_list` at run start.

`posts_create` real signature: `content`, `platform` (single string), `account_id`, `media_urls` (comma-separated string), `publish_now`/`is_draft`/`schedule_minutes`. There is no `platforms[]` array and no `platformSpecificData` — publish one `posts_create` per platform.

**`meta-story` (6 slides → 6 separate Story posts per platform):**

Post one slide at a time with a 1-second sleep between calls. After every ~5 consecutive FB story posts, sleep 5 seconds before the next call (Facebook rate-limits rapid sequential story submissions) and retry once on rejection.

```python
import time, subprocess

for i, signed_url in enumerate(render_urls, start=1):  # slide-1 through slide-6
    validate_media(url=signed_url)  # confirm valid: true before publishing
    # Local backup — preserves the asset even if a publish step later fails
    subprocess.run(["curl", "-s", "-L", signed_url,
                    "-o", f"outputs/{brand}/posts/Instagram/{slug}_story-slide-{i}_{date}.png"])

    for platform, account_id in [("facebook", ZERNIO_ACCOUNTS["facebook"]),
                                  ("instagram", ZERNIO_ACCOUNTS["instagram"])]:
        for attempt in range(2):
            result = posts_create(
                content=copy_text,
                platform=platform,
                account_id=account_id,
                media_urls=signed_url,          # signed URL passed directly — no re-host
                publish_now=True,
                is_draft=False,
            )
            if result.get("success") or attempt == 1:
                break
            time.sleep(5)  # FB rate-limit back-off before retry

    time.sleep(1)  # 1-second gap between slides
```

This produces 6 separate Story posts per platform — one per slide, in slide order.

**`meta-carousel` and single-image types (`linkedin-post`, `meta-post`) — publish directly:**

```python
media_urls = ",".join(render_urls)   # comma-separated string, in slide order (one URL for single-image types)
for signed_url in render_urls:
    validate_media(url=signed_url)
posts_create(
    content=copy_text,
    platform=platform_key,
    account_id=ZERNIO_ACCOUNTS[platform_key],
    media_urls=media_urls,   # carousel = comma-separated URLs; single-image = one URL
    publish_now=True,
    is_draft=False,
)
```

A carousel becomes a comma-separated `media_urls` string; single-image types are one URL. `curl` a local backup of each `signed_url` first. (Template-path posts do not proceed to Step 5 — that section is image-path only.)

**Skip Steps 4d, 4e, 4f, 4g** — no Pillow overlays, no local tmp files. Day-of-week `text_align` / `logo_position` rotations apply only to Step 4c-image.

**On quota / subscription error** (`fivebucks_render_post` returns 402/403 with a quota body): surface the upgrade message in the Slack notification, set the Notion status to `"Draft Ready"`, and fall back to **Step 4c-image** for this post.

**On other failure (5xx / timeout):**
- Log a Slack warning for this post: `"⚠️ [{brand}] fb.ai render failed for '{topic}' — falling back to Gemini-only path. Post marked Draft Ready."`
- Fall back to **Step 4c-image** (Gemini background → Pillow text overlay → Pillow logo overlay).
- Set Notion status to `"Draft Ready"` instead of `"Published"` so the user reviews the fallback before resending.
- Do NOT retry the render — render once and fall back.

### Step 4c-image — Generate image via Gemini

**Story full-frame guard (defensive — belt-and-suspenders):**

Before building the Gemini prompt, check whether the post is a Story and whether the `image_brief` already contains the full-frame composition instruction written by `social-calendar` v2.5.0+. If it does not (e.g. the calendar was authored by an older run), wrap it now:

```python
STORY_FULLFRAME_TEMPLATE = (
    "Photorealistic, full-bleed vertical portrait image for a 9:16 social media Story. "
    "{SCENE_DESCRIPTION}. The scene fills the ENTIRE frame from top to bottom — no empty areas, "
    "no plain backgrounds, no flat colour zones anywhere in the image. Rich environmental detail "
    "in the upper, middle, AND lower thirds of the frame. Cinematic lighting, editorial quality. "
    "Shot as if for a magazine cover in portrait orientation. "
    "Do not include any text, logos, or UI elements."
)

if post.format.lower() == "story" \
        and "fills the ENTIRE frame" not in post.image_brief:
    image_brief = STORY_FULLFRAME_TEMPLATE.format(SCENE_DESCRIPTION=post.image_brief)
else:
    image_brief = post.image_brief
```

Use `image_brief` (the potentially-wrapped version) as the Gemini prompt base from this point on — never `post.image_brief` directly.

Generate a fresh image for every post using Gemini:

```
Use gateway MCP tool `gemini_generate_image`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- prompt: Build from: brand visual style (from brand.md), post topic, mood, and image_brief (the wrapped version from the guard above). Example: "Professional clean desk workspace with laptop showing analytics dashboard, soft natural lighting, warm tones, no text, no people, bokeh background"
- aspect_ratio: match target canvas from Step 4a (e.g. "1:1" for IG square, "9:16" for Story/Reel, "191:100" for LinkedIn)
- model: "gemini-3.1-flash-image"

Result is auto-saved to a temp file. Use Python to locate, decode, and save to disk:
```python
import glob, json, base64, os
result_file = max(glob.glob('/sessions/*/mnt/.claude/projects/*/tool-results/mcp-*gemini_generate_image*.txt'), key=os.path.getmtime)
with open(result_file) as f:
    parsed = json.loads(json.load(f)[0]['text'])
with open('brands/{brand}/backgrounds/{descriptive_filename}.png', 'wb') as f:
    f.write(base64.b64decode(parsed['image_base64']))
```

**Prompt rules:**
- Always include "no text, no people" — text and logo are added in Steps 4d/4e
- Match the brand's visual style and color palette — **3-tier read order: (1) fb.ai brand kit via `fivebucks_get_brand_kit` when `FIVEBUCKS_API_KEY` is set; (2) `brands/{brand}/design-system/` when the kit is null or the key is unset; (3) `brands/{brand}/brand.md` Colors section as the universal fallback.** Extract the primary/accent/background HEX tokens from whichever source applied and inject them into the prompt as "warm tones around #ec4899 / muted slate around #0f172a" style guidance — when the fb.ai kit is the source, resolve roles via the Brand kit field map in `agents/link.md` (secondary→`tokens.colors.accent`, text→`tokens.colors.dark`; the kit has no separate `secondary` token). Same Visual consistency rule as `agents/link.md` — never hardcode from memory.
- Pillow text rendering in Step 4d uses `DejaVuSans-Bold` as a stable cross-platform rasterizer; the brand font names (fb.ai brand kit / design-system files) are for reference only (Canva / HTML mockups consume them, this image path does not). Colors on text are picked adaptively from the Gemini background, which is why getting the brand palette into the Gemini prompt at this step matters.
- Keep it clean and uncluttered — the text overlay needs readable space at the top or bottom (per the day-of-week `text_position` from Step 4b)

### Step 4d — Apply text overlay — USE PILLOW

Use Python Pillow to add gradient scrim + headline + subline. Do NOT use `image_add_text_overlay` gateway MCP tool.

```python
from PIL import Image, ImageDraw, ImageFont, ImageStat

def add_text_overlay(input_path, output_path, headline, subline, target_w, target_h,
                     text_align='center', text_position='bottom'):
    img = Image.open(input_path).convert('RGBA')
    # Resize + center-crop to target canvas
    r = img.width / img.height; tr = target_w / target_h
    if r > tr: nw = int(img.width * target_h / img.height); nh = target_h
    else: nw = target_w; nh = int(img.height * target_w / img.width)
    img = img.resize((nw, nh), Image.LANCZOS)
    img = img.crop(((nw-target_w)//2, (nh-target_h)//2, (nw-target_w)//2+target_w, (nh-target_h)//2+target_h))

    pad = int(target_w * 0.06)
    # Per-canvas insets — Story/Reel uses Meta safe zones only; Feed uses pad-derived only.
    # is_story_reel: True only for 9:16 (ratio ≥ 1.7). IG portrait 4:5 = 1.25 → feed treatment.
    # target_h > target_w is NOT sufficient: IG portrait (1080×1350) would wrongly get 9:16 safe zones.
    is_story_reel = (target_h / target_w) >= 1.7
    if is_story_reel:
        # Meta-spec safe zones (matches "central 1080x1420 of 1080x1920" rule)
        top_inset    = int(target_h * 0.14)   # Stories profile header clearance
        bottom_inset = int(target_h * 0.13)   # Reels UI stack clearance
        side_inset   = int(target_w * 0.13)   # Reels right-rail clearance
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

- `headline`: max 6–8 words, title case or all caps — use the post hook (NOT the topic name verbatim)
- `subline`: **always provide a subline** — never pass `""`. Use a short supporting line: brand tagline, key benefit, or CTA teaser (read from `brands/{brand}/brand.md`)
- `target_w`, `target_h`: canvas dimensions from Step 4a
- `text_align`: from day-of-week rotation (Step 4b) — `"left"`, `"center"`, or `"right"`
- `text_position`: from day-of-week rotation (Step 4b) — `"bottom"` (Mon/Wed/Fri) or `"top"` (Tue/Thu/Sat). Must match the day's row in the rotation table; logo is always placed on the opposite end (Step 4e).
- Text colors are chosen adaptively: the function samples the image brightness in the text zone before the scrim, then selects white + pink `#ec4899` (dark backgrounds) or near-black + dark-pink `#be185d` (light backgrounds).
- Save output as `_with_text.png`.

### Step 4e — Apply logo overlay — USE PILLOW

Use Python Pillow to composite the logo. Do NOT use `image_add_logo` gateway MCP tool.

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
    # Per-canvas logo insets — Story/Reel uses Meta safe zones; Feed uses uniform pad // 2.
    # Logo can sit at top OR bottom (selected by `position`); insets defined for both ends.
    pad = int(w * 0.06)                 # matches definition in add_text_overlay
    is_story_reel = (h / w) >= 1.7
    if is_story_reel:
        top_inset    = int(h * 0.14)   # Stories profile header clearance
        bottom_inset = int(h * 0.13)   # Reels UI stack clearance
        side_inset   = int(w * 0.13)   # Reels right-rail clearance
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

- Logo path: `brands/{brand}/logo.png`. Scale: 0.18.
- `position`: from day-of-week rotation (Step 4b) — `"top-right"` (Mon/Wed/Fri, paired with bottom text) or `"bottom-left"` (Tue/Thu/Sat, paired with top text). Logo and text always occupy opposite vertical ends; never both top or both bottom.
- Save as `_final.png`.

### Step 4f — Save final image

```
outputs/{brand}/posts/[Platform]/[TopicSlug]_[DDMonYYYY]_final.png
```

**Always overwrite** — never skip existing files.

### Step 4g — Cleanup

Only `_final.png` (or `_final.mp4`) should remain in the output folder. Delete any intermediate files (`_with_text.png`) for every post before moving to Step 5.

---

### Step 4h — Visual verification (MANDATORY before publishing)

For every `_final.png`, read the image file and visually inspect it before uploading to Zernio. Determine canvas type first: **9:16** = 1080×1920 (Story/Reel); **Feed** = all other formats.

**Text — position and inset (9:16 = Meta safe zones; feed = asymmetric pad-derived — larger sides):**
- [ ] Text block is at the **top OR bottom** matching `text_position` from Step 4b — never both ends, never mid-canvas
- [ ] Text alignment matches the day-of-week rotation: left (Mon/Thu), center (Tue/Fri), right (Wed/Sat)
- [ ] **9:16 (text at bottom — Mon/Wed/Fri):** bottom of text block is ~250 px (13%) from canvas bottom — clears Reels UI stack
- [ ] **9:16 (text at top — Tue/Thu/Sat):** top of text block is ~269 px (14%) from canvas top — clears Stories profile header
- [ ] **9:16:** text stays within ~140 px (13%) side margins — clears Reels right-rail
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

**If any check fails, fix before publishing:**

| Issue | Fix |
|---|---|
| **Text at wrong end of canvas** | Pass `text_position='top'` or `'bottom'` per Step 4b for the post's day-of-week; re-render |
| **Text too close to bottom edge (9:16)** | Verify `bottom_inset = int(target_h * 0.13)` (Meta-spec — Reels UI stack); re-render |
| **Text too close to top edge (9:16)** | Verify `top_inset = int(target_h * 0.14)` (Meta-spec — Stories profile header); re-render |
| **Text too close to sides (9:16)** | Verify `side_inset = int(target_w * 0.13)` (Meta-spec — Reels right-rail); re-render |
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
| Text overlaps logo | Text and logo must occupy opposite vertical ends per Step 4b. If overlapping despite correct positions (very long text on short canvas), reduce `hs` by 10% to shorten the text block. Re-render. |
| Logo at wrong end | Correct `position` per day-of-week rotation: `top-right` for Mon/Wed/Fri (paired with bottom text); `bottom-left` for Tue/Thu/Sat (paired with top text); re-render |
| Logo and text on same row | Verify Step 4b mapping: `text_position` and `logo_position` must always be on opposite vertical ends. Re-pull the rotation row for the post's day; re-render |
| Logo positioned wrong | Verify the `is_story_reel` branch in `add_logo`: 9:16 → `top_inset = int(h * 0.14)`, `bottom_inset = int(h * 0.13)`, `side_inset = int(w * 0.13)` (Meta); feed → all three = `pad // 2`; re-render |
| Logo clipped at edge | Reduce `scale` by 0.02 and re-render |
| Logo visually offset (unequal margins) | `add_logo` already crops transparent padding via `logo.crop(logo.getbbox())` before computing dimensions — verify the crop line is present at the top of the function; re-render |
| Logo aspect ratio looks distorted | Confirm `logo.crop(logo.getbbox())` runs BEFORE `logo_w`/`logo_h` are computed (cropping after the resize-target calc distorts aspect); re-render |
| Logo too small to read | Increase `scale` to 0.22 and re-render |
| Logo too large / dominates image | Reduce `scale` to 0.14 and re-render |
| Logo blends into background | Add white semi-transparent backing: `bg = Image.new('RGBA', (logo_w + pad, logo_h + pad), (255,255,255,160))`, paste at `(x - pad//2, y - pad//2)` before pasting logo |
| Logo over busy image area | Last-resort fallback only: switch to the opposite corner (e.g. `top-right` → `top-left`) on the same end. This overrides the day-of-week `logo_position`; use only when contrast cannot be salvaged via scrim alpha or backing. Re-render. |

Re-render until all checks pass. Only then proceed to Step 5.

---

## Step 5 — Publish to Zernio API

Upload the image and copy directly to Zernio API and publish immediately.

⚠️ **Image-path only: always upload `_final.png` from `outputs/{brand}/posts/[Platform]/`. Never upload the raw Gemini background from `brands/{brand}/backgrounds/` or the intermediate `_with_text.png`. Steps 4d–4g must be complete before this step runs.**

**Fix 2 — Before calling `posts_create`:** write Notion Status → `"Processing"` for this row (same `notion-update-page update_content` call as Step 6, matching `Planned` → `Processing`). This ensures a crash after publish but before the Step 6 `Published` write leaves the row in a non-`Planned` state — the next run's `Status == Planned` filter skips it entirely.

⚠️ **Zernio `posts_create` has no `platformSpecificData.contentType` param** — Story/Reel content-typing cannot be set through this tool, so image-path posts publish as feed content regardless of dimensions. (Story/Reel typing is only achievable on the template-path via fb.ai; the Gemini image-path publishes feed posts.)

For each post, use the Zernio MCP tools (OAuth/session-scoped — no `fiveagents_api_key`). The `_final.png` is a **local file**, so upload it programmatically via `media_get_media_presigned_url` — **not** `media_generate_upload_link` (that is a browser-only flow and PUTting to it silently fails):

```
1. Use `media_get_media_presigned_url`:
   - filename: "<filename>.png" (or .mp4 for video)
   - content_type: "image/png" (or "video/mp4")
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

3. `validate_media(url=public_url)` → confirm `valid: true`, then use `posts_create` (one call per platform):
   - content: <copy text with hashtags>
   - platform: "<facebook|instagram|linkedin>"   # single string, not an array
   - account_id: "<from accounts_list / ZERNIO_ACCOUNTS>"
   - media_urls: "<public_url>"                    # comma-separated string for multiple images
   - publish_now: true (or is_draft: true)
```

**Account IDs** — resolve via `accounts_list` at run start; the `{BRAND}_ZERNIO_*` env vars hold the canonical IDs:
```python
B = BRAND.upper()
ZERNIO_ACCOUNTS = {
    "facebook":  os.environ[f"{B}_ZERNIO_FB"],
    "instagram": os.environ[f"{B}_ZERNIO_IG"],
    "linkedin":  os.environ[f"{B}_ZERNIO_LI"],
}
```

**For each post:**
- `platform_key` = post platform lowercase ("facebook" | "instagram" | "linkedin")
- `account_id` = `ZERNIO_ACCOUNTS[platform_key]` — **always passed** (omitting it errors when a brand has multiple accounts on a platform)
- Call `posts_create` per platform with the public media URL and copy text.

**Do NOT store copy in Notion** — Zernio is the single source of truth.

---

## Step 6 — Update Social Calendar status in Notion

Set Status (cell index 10) based on what was actually done in Step 5:

| Step 5 action | Notion status |
|---|---|
| `publishNow: true` (live post) | `"Published"` |
| `isDraft: true` (saved as draft) | `"Draft Ready"` |

Use **Notion MCP** to update the row's Status cell.

The current Notion connector does not expose block-level updates, so individual `table_row` cells cannot be patched directly. Use `notion-update-page` with the `update_content` command to do a targeted search-and-replace on the calendar page's markdown table — find the row's previous status text and replace with the new one.

```
Use mcp__claude_ai_Notion__notion-update-page:
- page_id: <calendar_page_id from Step 1>
- command: "update_content"
- content_updates: [
    {
      "old_str": "| <Date> | <Platform> | <Format> | <Topic> | <Persona> | <ContentAngle> | <CTA> | <Hashtags> | <ImageBrief> | <Direction> | Processing |",
      "new_str": "| <Date> | <Platform> | <Format> | <Topic> | <Persona> | <ContentAngle> | <CTA> | <Hashtags> | <ImageBrief> | <Direction> | Published |"
    }
  ]
```

- If published live → new status = `"Published"`
- If saved as draft → new status = `"Draft Ready"`

The 11 columns in the table are: `[0] Date, [1] Platform, [2] Format, [3] Topic, [4] Persona, [5] ContentAngle, [6] CTA, [7] Hashtags, [8] ImageBrief, [9] Direction, [10] Status`. The `old_str` MUST match the row exactly as it appears in the page (whitespace and pipe characters preserved); reconstruct it from the values you parsed in Step 1c. Run one `update_content` operation per published post — or batch all updates into a single call by passing multiple entries in `content_updates`.

---

## Step 7 — Send Slack notification

**Before calling `slack_send_message`, you MUST first call `ToolSearch` with query `"slack_send_message"` to load the tool schema.** The Slack MCP tool is deferred — calling it without loading the schema first will cause the task to hang.

DM the user via **Slack MCP** (`slack_send_message`, `channel_id: "$SLACK_NOTIFY_USER"`):

```
[{brand}] Content ready for [DD Mon YYYY]

[Platform] — [Format] — [Topic]
  Copy: outputs/{brand}/posts/[Platform]/[Slug]_copy.md
  Image: outputs/{brand}/posts/[Platform]/[Slug]_final.png
  Published: [zernio_post_id]
  (or Saved as draft: [zernio_post_id])

Notion Social Calendar updated.

[⚠️ Media folders don't match expected names (LinkedIn Post / Meta Story / Meta Carousel / Meta Post) — using the all-folder pool. Rename them for per-type photo injection. — include this line only when the Step 4c-template §1 sub-step 4 fallback fired]
```

---

## Step 8 — Log to memory

Append a summary to `memory/YYYY-MM-DD.md`:

```markdown
## Content generation run — YYYY-MM-DDTHH:MM UTC (daily cron)
- Posts generated: N (for DD Mon YYYY)
- [Platform] "[Topic]" ([persona])
  - Copy: [path]
  - Image: [path]
  - Zernio draft id: [id]
- Images generated: N
- Social Calendar updated: yes/no
- Slack notified: yes/no
```

---

## Quality Checklist

- [ ] All "Planned" posts for today processed
- [ ] Copy matches persona voice and brand tone
- [ ] Hook is scroll-stopping; CTA is specific
- [ ] Brand visual source resolved in 3-tier order (informs Gemini prompt aesthetic): fb.ai brand kit (`fivebucks_get_brand_kit`, checked first when `FIVEBUCKS_API_KEY` set) → local `brands/{brand}/design-system/` (when present) → `brand.md` colors/voice; never blocked on a missing key or design-system
- [ ] Image dimensions are correct for platform/format
- [ ] Template-path used when a matching fb.ai template exists for the format; image-path used otherwise (no `failed` run for missing templates)
- [ ] **Template-path:** `fivebucks_list_templates` called once at run start and cached (not per-post)
- [ ] **Template-path:** media pool built — `fivebucks_list_media_folders` called once; exact-name match first (case-insensitive); if no match → ALL folders pooled for that type; if no folders → pool empty (not a failure)
- [ ] **Template-path:** `overrides` map copy → manifest field keys (skip `bound:false`, `select` values from `options`); direction set (`_direction` A/B/C for meta-story — never `all`; `direction` for single-image types)
- [ ] **Template-path:** `fivebucks_create_post` → `fivebucks_render_post`; signed render URLs passed **directly** as `media_urls` (no re-host; `validate_media` first; local `curl` backup); **Story (`meta-story`)**: posted one-per-slide via `posts_create` (one call per platform) with `is_draft=False` + `publish_now=True`; 1-second sleep between slides; 5-second sleep + one retry after ~5 consecutive FB posts (FB rate-limit); **Carousel/single-image**: signed URLs passed as a comma-separated `media_urls` string to a single `posts_create` per platform; Pillow overlays skipped (Steps 4d–4g)
- [ ] **Template-path:** `slide_ids` **omitted** for all types — fb.ai selects slides from the direction override (`_direction` for meta-story/meta-carousel, `direction` for single-image)
- [ ] **Template-path (failure):** quota/5xx falls back to Step 4c-image; Notion status set to `"Draft Ready"`; Slack warning logged
- [ ] **Image-path (Gemini-only):** Story/Reel full-frame guard applied — `image_brief` passed to Gemini contains `"fills the ENTIRE frame"` (either from `social-calendar` or wrapped by the guard)
- [ ] **Image-path (Gemini-only):** Pillow text overlay (Step 4d) AND logo overlay (Step 4e) BOTH applied — Gemini background has no logo
- [ ] **Image-path:** text overlay applied with correct day-of-week `text_align` (left Mon/Thu, center Tue/Fri, right Wed/Sat) AND `text_position` (bottom Mon/Wed/Fri, top Tue/Thu/Sat) per Step 4b
- [ ] **Image-path:** Logo at 0.18 scale with correct day-of-week `logo_position`
- [ ] Day-of-week rotation does NOT apply on template-path (template chrome is fixed)
- [ ] Final images saved to correct `outputs/{brand}/posts/[Platform]/` folder
- [ ] Intermediate files deleted — `_with_text.png` removed after `_final.png` confirmed
- [ ] **Image-path publish:** local `_final.png` uploaded via `media_get_media_presigned_url` (never `media_generate_upload_link`); `validate_media` passed; `posts_create` called per platform with `media_urls` string + `account_id` (resolved via `accounts_list`)
- [ ] Published to Zernio API with correct mode (`publish_now` or `is_draft`); scheduled posts use integer `schedule_minutes`
- [ ] Notion Social Calendar rows updated to "Published" (if published) or "Draft Ready" (if draft) — never hardcoded
- [ ] Slack notification sent with Zernio post IDs and correct status
- [ ] Memory logged
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "content-generator"
- brand: "<active-brand>"
- status: "<success|partial|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "images_generated": 0,
    "videos_generated": 0,
    "posts": [
      { "platform": "Facebook", "topic": "...", "persona": "...", "format": "<Post|Story|Carousel>", "asset_type": "image", "status": "Published", "zernio_post_id": "..." }
    ]
  }
```

**Status values:** `success` (all posts generated + published), `partial` (some posts failed), `failed` (skill errored).
