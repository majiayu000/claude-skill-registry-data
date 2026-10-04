---
name: background-generator
description: Generate 20 background images per brand for Reel video production. Run manually or schedule externally.
allowed-tools: Read, Grep, Glob, Bash
area: Marketing
use_for: "Generate 20 background images per brand for Reel video production. Run manually or schedule externally"
deps:
  mcp: ["Notion"]
  gateway: ["Gemini", "fivebucks (opt — brand kit via fivebucks_get_brand_kit; **scope: social_posts**)"]
  files: ["brand.md", "design-system/ (opt — local; or fb.ai brand kit via fivebucks_get_brand_kit; brand.md fallback)"]
  env: ["`${BRAND}_NOTION_DB`"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.0 | July 12, 2026 |

**Description:** Generate 20 background images per brand for Reel video production. Run manually or schedule externally.

### Change Log

**v2.20.0** — July 12, 2026
- **Declared the fb.ai dependency and its required scope.** fb.ai API keys are now scoped; this skill's `deps.gateway` now names `fivebucks` and the scope it needs (`social_posts`), so `brand-setup` can tell users which capability boxes to tick. No behaviour change — see `agents/link.md` for the scope/error/quota contract.

**v2.18.0** — July 01, 2026
- **Gemini image model ID updated (gateway v1.7.4).** `gemini_generate_image` model changed from the retired `gemini-3.1-flash-image-preview` (Google 404'd all `-preview` image IDs on 2026-06-25) to the GA default `gemini-3.1-flash-image` ("Nano Banana 2").

**v2.8.0** — May 20, 2026
- Brand palette resolution is now a **3-tier lookup**: fb.ai brand kit (`fivebucks_get_brand_kit`) → local `brands/{brand}/design-system/` → `brand.md`, per the Brand kit field map in `agents/link.md`. Trimmed the duplicated design-system reading boilerplate (now centralized in link.md tier 2).

**v2.7.0** — May 20, 2026
- Dropped the "Claude Design shell collections" relationship note that referenced local `social-meta-*-template/` folders. Social-post templates now live on fb.ai (rendered via `fivebucks_*`); this skill's `backgrounds/` library remains an independent, general-purpose set for Reels + the Gemini fallback.

**v2.4.1** — May 12, 2026
- Step 2 — added explicit "Read brand visual identity FIRST" block. Probes `brands/{brand}/design-system/` (preferred) then `brand.md` Colors (fallback). Mirrors the Visual consistency rule in `agents/link.md`.
- Step 2 Prompt rules — every Gemini prompt now appends a brand-palette hint (HEX values phrased as ambient mood, e.g. "warm tones around #ec4899 with muted slate (#0f172a) shadows"). Backgrounds are now on-brand instead of generic stock-photo aesthetics. **Reason:** library was previously brand-agnostic (no color injection); content-generator's downstream Pillow overlay couldn't recover an off-brand background.
- Quality Checklist — two new entries enforce the design-system probe and the palette-hint injection.

# SKILL.md — Background Generator

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You generate 20 pre-stored background images per brand for use in Ken Burns Reel videos. These backgrounds are stored at `brands/{brand}/backgrounds/` and used as raw material for video production. Run manually when the library needs refreshing.

**Relationship to fb.ai social templates** — the brand's polished social-post templates live on fb.ai (installed via `brand-setup` Step 4c) and are rendered by `content-generator` / `creative-designer` via the `fivebucks_*` tools. The `backgrounds/` library this skill produces is a separate, general-purpose set used by Reel video production and as the Gemini fallback library. The two systems are independent — this skill does not touch fb.ai templates.

---

## When to use

- When the user asks to refresh or add backgrounds
- When the library feels repetitive (content-generator reusing same images)
- After adding a new brand

Do NOT use for:
- Generating post-specific images → content-generator handles that
- Generating video → content-generator or creative-designer

---

## Step 1 — Read upcoming social calendar briefs

Read the next 2 weeks of social calendar entries for the brand to get fresh `ImageBrief` values.

Use **Notion MCP** to query the calendar:

1. Resolve the brand's database to a `data_source_url` first, then search inside it for the latest `SocialCalendar_` pages:

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: "${BRAND}_NOTION_DB"
```

Inspect the response and extract the `collection://` URL (typically `data_sources[0].url`). Save as `data_source_url`.

```
Use mcp__claude_ai_Notion__notion-search:
- query: "SocialCalendar_"
- data_source_url: <data_source_url from above>
- query_type: "internal"
- page_size: 5
```

2. For each page whose date range covers the next 2 weeks, use `mcp__claude_ai_Notion__notion-fetch` with the page ID to retrieve the page content (returns full markdown including the calendar table). Parse the table rows from the returned markdown directly.

3. Parse each row — column order: `Date, Platform, Format, Topic, Persona, ContentAngle, CTA, Hashtags, ImageBrief, Status`. Filter for rows with Status = `"Planned"` and dates within the next 14 days.

Extract all unique `ImageBrief` values (column index 8). These are the prompts.

---

## Step 2 — Build prompt list (20 per brand)

**Read brand visual identity FIRST so every prompt is palette-aware. Resolve the source in this 3-tier order:**
1. **fb.ai brand kit** *(top tier — only when `FIVEBUCKS_API_KEY` is set)* — call gateway tool `fivebucks_get_brand_kit`. If it returns non-null, use its color tokens (primary / accent / background HEX) as the authoritative source — resolve fields via the Brand kit field map in `agents/link.md` (secondary→`tokens.colors.accent`, text→`tokens.colors.dark`; the kit has no separate `secondary` token). Returns null when no kit is uploaded — fall through to tier 2.
2. **brands/{brand}/design-system/** *(local folder — when the fb.ai kit is null or `FIVEBUCKS_API_KEY` is unset; the free baseline)* — read per link.md tier 2 for the brand HEX palette.
3. **brands/{brand}/brand.md** — Colors section. Universal fallback when neither of the above is available. Never block on a missing fb.ai key or design-system; brand.md is always available.

Same Visual consistency rule as `agents/link.md` — derive from the fb.ai brand kit (`fivebucks_get_brand_kit`, when `FIVEBUCKS_API_KEY` set) → local `design-system/` → `brand.md` (fallback), never hardcode brand colors from memory.

Take up to 20 unique ImageBriefs from Step 1. If fewer than 20, create variations of existing briefs by changing:
- Lighting (morning light, golden hour, dim ambient, bright studio)
- Setting (office, cafe, co-working, home office, outdoor)
- Composition (top-down flat lay, close-up, wide angle, aerial)

**Prompt rules:**
- Use the `ImageBrief` exactly as written in the calendar
- **Append a brand-palette hint to every prompt** using the HEX values from the brand-visual read above (fb.ai brand kit / local design-system/ when present, brand.md when fallback) — phrased as ambient mood, e.g. `", warm tones around #ec4899 with muted slate (#0f172a) shadows"` or `", rich teal accents (#0d9488) on a near-black background (#0a0a0a)"`. This keeps the library on-brand without baking literal HEX swatches into the image. Skip the hint only when the fb.ai kit, `design-system/`, AND the `brand.md` Colors section are all empty (rare — brand-setup writes brand.md Colors on every run).
- NEVER use the word "portrait" — Gemini generates actual portrait photos
- Every prompt must end with: "No text. No logos. No watermarks."

---

## Step 3 — Generate images

Create the backgrounds folder if it doesn't exist: `brands/{brand}/backgrounds/`

For each image:
```
Use gateway MCP tool `gemini_generate_image`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- prompt: "{ImageBrief}"
- aspect_ratio: "1:1" (default for background library; content-generator crops to target canvas at overlay time)
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

If user has selected a folder, save directly to `brands/{brand}/backgrounds/` — not a temp path.

Wait 6 seconds between calls (rate limit: ~10 requests per minute).

**Filename convention:** Use a descriptive slug based on the Topic or ImageBrief content. Examples:
- `finance_dashboard_laptop.png`
- `singapore_skyline_timelapse.png`
- `abstract_purple_silk.png`
- `cafe_laptop_notepad.png`

Filenames must be descriptive enough that the content-generator can pick the right background based on the post's Topic.

**Rate limit:** 6 seconds between image generation calls.

---

## Step 4 — Verify

Count the PNG files in `brands/{brand}/backgrounds/`. Must have at least 20 NEW images generated. Skip filenames that already exist — the library grows each month. If any failed, retry.

---

## Step 5 — Notify via Slack

DM the user via Slack MCP (`channel_id: "$SLACK_NOTIFY_USER"`):

```
🖼️ [{brand}] Monthly backgrounds refreshed

New images: 20
Total library: [count] images
Location: brands/{brand}/backgrounds/
```

---

## Quality Checklist

- [ ] 20 images per brand generated
- [ ] Filenames are descriptive (content-generator can pick by Topic)
- [ ] No "portrait" in any prompt
- [ ] All prompts end with "No text. No logos. No watermarks."
- [ ] Brand visual source resolved in 3-tier order at Step 2: fb.ai brand kit (`fivebucks_get_brand_kit`, checked first when `FIVEBUCKS_API_KEY` set) → local `brands/{brand}/design-system/` (when present) → `brand.md` Colors; never blocked on a missing key or design-system
- [ ] Every Gemini prompt carries a brand-palette hint (HEX values from fb.ai brand kit / design-system / brand.md, phrased as ambient mood) — library is on-brand
- [ ] 6-second delay between image generation calls
- [ ] Existing images NOT deleted (library grows)
- [ ] Slack notification sent
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "background-generator"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: { "date": "YYYY-MM-DD", "images_generated": 0, "total_library": 0 }
```
