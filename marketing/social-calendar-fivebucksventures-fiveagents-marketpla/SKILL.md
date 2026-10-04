---
name: social-calendar
description: Plan a weekly social media content calendar for any active brand — Static Mode (14 posts across LinkedIn, Facebook, Instagram) or YouTube-First Mode (one weekly video + platform clips), selected by brand.md Content Strategy. Runs weekly on Sunday cron schedule.
allowed-tools: Read, Grep, Glob, Bash, WebSearch
area: Marketing
use_for: "Plan a weekly social media content calendar — Static Mode (14 posts across LinkedIn, Facebook, Instagram) or YouTube-First Mode (one weekly video + platform clips), per brand.md Content Strategy. Runs weekly on Sunday cron schedule"
deps:
  mcp: ["Notion", "Slack"]
  gateway: ["FiveAgents (logging)", "fivebucks (opt — fb.ai template manifest via fivebucks_get_template; **scope: social_posts**)"]
  files: ["brand.md", "audience.md", "product.md", "competitors.md"]
  env: ["`${BRAND}_NOTION_DB`"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.0 | July 12, 2026 |

**Description:** Plan a weekly social media content calendar for any active brand — Static Mode (14 posts) or YouTube-First Mode (one weekly video + platform clips), selected by brand.md Content Strategy

### Change Log

**v2.20.0** — July 12, 2026
- **Declared the fb.ai dependency and its required scope.** fb.ai API keys are now scoped; this skill's `deps.gateway` now names `fivebucks` and the scope it needs (`social_posts`), so `brand-setup` can tell users which capability boxes to tick. No behaviour change — see `agents/link.md` for the scope/error/quota contract.

**v2.15.0** — June 09, 2026
- **Competitor video structure matching added (Step 2a Part 1b).** YouTube-First Mode now reads the `video_structure` JSON from trend_db (written by `trend-radar` Step 2c) and maps each structural element — credibility hook, pattern interruptor, framework, escalation, reflection, close — to the brand's own angle. The adapted structure is written as a Video Structure table in the calendar. Clips now have a `Source Section` column tracing each clip to a video section, preventing topic-mismatch bugs. Degrades gracefully when no video structure is available (plans from topic/angle as before).

**v2.14.0** — May 29, 2026
- **YouTube-First Mode added.** Step 1 now reads `brand.md` `## Content Strategy` (`Primary channel`, `Connected platforms`, `Clips per video`, `Cadence`) to pick the planning flow. New **Step 2a (YouTube-First Mode)** plans one weekly YouTube video + a per-platform **Clip Release Schedule** — publish day/time per clip, Twitter/X support, comment-to-DM CTAs — restricted to connected platforms; the schedule is the handoff to `video-repurposer` (Phase 4–5). The original 14-post flow is renamed **Step 2b (Static Mode)**. The quality checklist branches per mode. Brands without `## Content Strategy` default to Static.

**v2.12.0** — May 28, 2026
- **Planning now closes the learning loop.** Step 1b reads two new inputs before the market-research pass: (1) the latest **Performance Brief** from `content-performance-analyst` (`${BRAND}_PERFORMANCE_DB` / `outputs/{brand}/strategy/PerformanceBrief_*`) to bias the mix toward proven-winning formats/personas/hook archetypes/Directions, and (2) **`trend-radar`** candidate topics (`${BRAND}_TREND_DB`) for 2–3 timely/newsjacking slots. Step 2's Content Angle now names a **hook archetype** from `content-creation/hook-library.md` so production and performance analysis share one hook vocabulary.

**v2.11.1** — May 22, 2026
- **Metrics and checklist corrected.** Log payload: `calendar_status` fixed "Published" → "Planned"; post `format` fixed from hardcoded `"static"` → `"<Post|Story|Carousel>"`; `content_mix.type` fixed from `"static"` → content-type enum. Quality checklist: added Monday slot checks (LinkedIn Post / Facebook Post / Instagram Post) and Friday LinkedIn = Post. `deps.gateway` updated from `[]` to `["FiveAgents (logging)"]`.

# SKILL.md — Social Calendar

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

You are a senior social media strategist for the active brand. Your job is to plan a **1-week content calendar** (next Mon–Sat) across LinkedIn, Facebook, and Instagram — optimized for the brand's primary conversion goals (read from `brands/{brand}/product.md`).

Runs weekly on Sunday cron schedule. Output is a **planning table only** — topics, formats, angles, CTAs. The content-generator skill handles actual copy.

---

## Step 1 — Read Brand Context

Read these files before planning:
- `brands/{brand}/brand.md`
- `brands/{brand}/product.md`
- `brands/{brand}/audience.md`
- `brands/{brand}/competitors.md`

After reading brand context, check `brands/{brand}/brand.md` for `## Content Strategy`:
- Read `Primary channel` value: `youtube` or `static`
- Read `Connected platforms` — in YouTube-First Mode, only plan clips for the platforms listed here
- Read `Clips per video` — default clip count per platform in YouTube-First Mode
- Read `Cadence` — publishing rhythm
- If `## Content Strategy` is absent → default to `static` mode and note the gap

This single field drives which planning flow runs in Step 2.

---

## Step 1b — Read the learning loop, then research

**First, read what already worked and what's timely** (these bias the whole plan — read them before the market-research pass):

1. **Latest Performance Brief** — from `content-performance-analyst`. Read the newest `outputs/{brand}/strategy/PerformanceBrief_*.md` (or query `${BRAND}_PERFORMANCE_DB` if the file is absent). Use its "double down / stop-fix / next-calendar guidance" to bias the content mix toward winning **formats, personas, hook archetypes, and Directions**, and away from underperformers. If no Brief exists yet (first weeks), note it and proceed on market research alone.
2. **Trend Radar candidates** — query `${BRAND}_TREND_DB` for `Status="Candidate"` rows seen in the last 7 days (written by `trend-radar`). Earmark **2–3 timely/newsjacking slots** for the strongest, most relevant candidates; mark the ones you use `Status="Planned"`.

**Then run `/link-skills:research-strategy` for market context.** Focus the research on:

1. **Viral content formats** — what's getting high engagement on LinkedIn, Facebook, Instagram right now in the brand's niche? (e.g. carousel threads, short-form video, meme formats, hot takes, before/after)
2. **Trending topics** — what industry conversations, news, or pain points are blowing up this week?
3. **Competitor social content** — what did competitors post recently that got high engagement? What format/hook did they use?
4. **High-performing keywords** — from DataforSEO, what search terms are trending in the brand's space?

Read the research output from `outputs/{brand}/strategy/` after it completes.

**All three Step 1b signals — the Performance Brief (what worked), Trend Radar (what's timely), and this market research — MUST drive the content mix and topic selection in Step 2.** Do not default to a fixed content mix. Precedence: the Performance Brief first (your own measured results), then timely trend candidates, then market research.

---

## Step 2a — YouTube-First Mode

*Run this step only if `Primary channel: youtube` in `brand.md`. Otherwise skip to Step 2b.*

Plan one YouTube video for the upcoming week plus a clip release schedule for each connected platform. All content must be informed by Step 1b inputs: Performance Brief, Trend Radar candidates, and competitor research.

### Part 1 — YouTube Video Plan

| Field | Notes |
|---|---|
| Title | Hook-led, ≤60 chars — use proven title mechanics: specific outcome, time-pressure hook, or curiosity gap |
| Publish Day & Time | Mon or Tue evening, 6–9pm (brand timezone from `brand.md Locale`) |
| Format | `talking-head` / `screen-share` / `hybrid` |
| Target persona | One persona slug from `audience.md` |
| Trend Radar topic | Candidate from `${BRAND}_TREND_DB` it maps to — mark that row `Status=Planned` |
| Intro hook | First 30s — what the viewer will learn |
| Talking points | 3–5 key points (one line each) |
| CTA | Comment-to-DM format: "Comment '[keyword]' and I'll send you [specific resource]" — never generic subscribe asks |
| Est. length | 5–15 min |

### Part 1b — Apply Competitor Video Structure (when available)

If the Trend Radar candidate used for this video has a `video_structure` JSON in its Notion page body (written by `trend-radar` Step 2c), read it and use it to plan the video's internal structure.

**Procedure:**

1. **Fetch the trend_db page** for the candidate marked `Status=Planned` — use `mcp__claude_ai_Notion__notion-fetch` with the page ID.
2. **Parse the `video_structure` JSON** from the page body (inside a ```json code fence under the "Video Structure Analysis" heading).
3. **Map each structural element to the brand's own angle:**

| Competitor Element | Brand Adaptation Rule |
|---|---|
| `credibility_hook` | Replace the competitor's credential with the brand's own credibility anchor (from `brand.md` or brand context — e.g. corporate pedigree, specific experience, unique access). Never copy the competitor's claim. |
| `pattern_interruptor` | Keep the same technique (flash-forward, show-don't-tell, etc.) but apply it to the brand's content. If the competitor shows a finished product, the brand shows its finished product. |
| `framework` | Teach a framework relevant to the brand's expertise. If the competitor taught a 3-type taxonomy, the brand teaches its own taxonomy from its domain knowledge. |
| `build_with_escalation` | Match the escalation pattern (time-based, complexity-based, etc.) but with the brand's own build/journey. Preserve the same number of escalation steps. |
| `reflection_beat` | Add a personal/honest reflection from the brand's perspective — what the brand owner learned, what surprised them, what they'd change. |
| `close_cta` | Match the CTA mechanic (comment-to-DM, etc.) but with the brand's own resource/offer. |

4. **Write the adapted structure into the YouTube Video Plan** as a new table:

#### Video Structure (adapted from competitor)

| # | Section | Timestamp Target | Brand's Version | Technique |
|---|---|---|---|---|
| 1 | Credibility Hook | 0:00–0:30 | <brand's adapted hook> | <same technique, brand's credential> |
| 2 | Pattern Interruptor | 0:30–1:30 | <brand's adapted interruptor> | <same technique> |
| 3 | Framework | 1:30–3:00 | <brand's framework> | <same or adapted technique> |
| 4 | Build with Escalation | 3:00–<end-2min> | <brand's build steps> | <same escalation pattern> |
| 5 | Reflection Beat | near end | <brand's reflection> | <same technique> |
| 6 | Close / CTA | final 30s | <brand's CTA> | <same CTA mechanic> |

Also add a **Competitor Structure Applied** reference:

> Structure adapted from: [competitor channel] — "[video title]" ([source URL])
> Original hook technique: [technique] | Adapted: [brand's technique]

5. **Ensure clips are derived FROM the video structure.** Each clip in Part 2 must map to a specific section from the structure table above. Do not plan clips about topics unrelated to the video — every clip's "Moment to clip" must reference a section number (1–6) or a specific escalation step from section 4.

**If no `video_structure` is available** (trend-radar Step 2c was skipped, or the candidate is not a competitor-remix, or Chrome MCP was unavailable): plan the video using the current method (topic + angle + talking points from Step 1b research). Note in the calendar: "No competitor structure available — planned from topic/angle."

### Part 2 — Clip Release Schedule

For each platform listed under `Connected platforms` in `brand.md`, plan the number of clips specified under `Clips per video` (default 1–2 if unset). Do NOT plan clips for platforms not listed as connected.

| Clip # | Platform | Publish Day | Publish Time | Duration | Source Section | Moment to clip | Caption angle | Hook Archetype | CTA |
|---|---|---|---|---|---|---|---|---|---|

Where `Source Section` is the section number (1–6) or escalation step (e.g. "4a: Day 1") from the **Video Structure** table (Part 1b) that this clip is drawn from.

**Validation rule:** Every clip's `Source Section` must reference a valid section from the Video Structure table. If a clip cannot be traced to a video section, it must be removed or rewritten. This prevents clips about topics not covered in the video. *(When no `video_structure` was available and the video was planned from topic/angle, leave `Source Section` blank and note it.)*

**Scheduling rules** (read timezone from `brand.md Locale`):
- YouTube publishes first (Mon or Tue evening), clips roll out Tue–Fri — never before the YouTube video is live
- Never publish two clips on the same platform on the same day
- **LinkedIn:** Tue or Thu, 7:30–8:30am local time
- **Instagram Reels:** Wed 12pm or Thu 9am local time
- **TikTok:** Fri 9am local time
- **Twitter/X:** Thu 12pm local time
- **Facebook:** Wed or Thu, 1–3pm local time

**Clip guidelines per platform:**
- LinkedIn: 60–90s, professional insight or story angle
- Instagram: ≤60s Reels, hook in first 3s
- TikTok: ≤60s, fastest hook from the video
- Twitter/X: ≤30s, sharpest one-liner from the video
- Facebook: 60–90s, broader audience angle

### Part 3 — Captions

For each clip, write a platform-native caption. Read voice and tone from `brand.md`. Use comment-to-DM CTAs — never generic subscribe asks.

- **LinkedIn:** 150–300 words, professional + story-led, 3–5 hashtags
- **Instagram:** Hook in line 1 (≤125 chars before "more"), 80–150 words, 3–5 hashtags
- **TikTok:** ≤150 chars, casual, 3–5 hashtags
- **Twitter/X:** ≤280 chars (URLs = 23 chars), 2–3 hashtags
- **Facebook:** 100–200 words, conversational, 2–3 hashtags

All clips set to `Status = Planned` pending YouTube upload.

**Save to Notion** — same DB as static mode (`${BRAND}_NOTION_DB`); if the env var is unset (first-ever run for this brand), create the DB first via the **Step 3a** bootstrap, then persist its ID. Page title: `SocialCalendar_[DDMon]-[DDMonYYYY]`. Content: YouTube Video Plan table + Video Structure table (when Part 1b produced one) + Clip Release Schedule table + Captions section. The Video Structure table must be saved when present — `content-creation` Step 2b reads it back off this page to build the YouTube script skeleton.

After saving, skip Step 2b and proceed to Slack notification.

---

## Step 2b — Static Mode

*Run this step only if `Primary channel: static` in `brand.md` (or if `## Content Strategy` is absent). Otherwise this step was already handled by Step 2a.*

Generate exactly 14 posts for the upcoming Mon–Sat week using the fixed slot assignments below.

### Fixed Slot Assignments — do not deviate

| Day | Platform | Format |
|---|---|---|
| Monday | LinkedIn | Post |
| Monday | Facebook | Post |
| Monday | Instagram | Post |
| Tuesday | Facebook | Post |
| Tuesday | Instagram | Story |
| Wednesday | LinkedIn | Carousel |
| Wednesday | Instagram | Post |
| Thursday | Facebook | Post |
| Thursday | Instagram | Story |
| Friday | LinkedIn | Post |
| Friday | Facebook | Story |
| Friday | Instagram | Carousel |
| Saturday | Facebook | Post |
| Saturday | Instagram | Carousel |

### For each post output ONLY these fields (one row per post, no extra commentary):

| Field | Constraint |
|---|---|
| Date | DD Mon YYYY |
| Platform | LinkedIn / Facebook / Instagram |
| Format | From fixed slot table above. |
| Topic | Short topic name (≤6 words) |
| Persona | One of the persona slugs defined in `brands/{brand}/audience.md` — max 2× per persona per week. Examples: `content-mgr`, `seo-pro`, `sales-rep`, `agency-owner`, `solopreneur`, `growth-mktr` |
| Content Angle | Hook + key message (1 sentence, ≤20 words). Name the **hook archetype** it uses (from `skills/content-creation/hook-library.md`, e.g. `Contrarian Correction`, `Proof / Result`) so production and `content-performance-analyst` share one hook vocabulary. Favor archetypes the latest Performance Brief shows winning for this brand. |
| CTA | Specific action (≤8 words) |
| Hashtags | 3–5 hashtags |
| Image Brief | Scene description for image gen (1 sentence). End with: "No text. No logos. No watermarks." For Story posts the raw scene is automatically wrapped in the full-frame composition template (see "Story image_brief wrapping" below) before saving to Notion. |
| Direction | Template variant for the post — see "Direction selection" below. Required for any format with a matching fb.ai template (IG/FB Carousel, Story, IG/FB single-image, LinkedIn single-image); leave blank for formats with no matching fb.ai template. |
| Status | Planned |

### Direction selection — pick the template variant per post

The `Direction` field tells `content-generator` which template variant to render at production time. Direction is your responsibility (planning); content-generator just applies what you set.

**Rotate Direction for variety — don't let the audience get bored.** Pick by content type first (rules below), but when several posts of the same format/platform fit the same type, spread the Direction across `A`/`B`/`C` (and rotate the carousel `coverVariant-bodyVariant` combos) instead of repeating one. Aim for a varied mix across the week — avoid long runs of the same Direction in a single platform's feed.

**For Carousel posts** — combine the carousel template's two variant axes as `coverVariant-bodyVariant`:
- `type-allnumbers` — default. Big typographic cover, all sign slides have large kicker numerals (01/02/03/04). Good for educational carousels with strong listicle structure.
- `sticker-editorial` — Sticker-style cover (badge / playful), editorial body slides (less number-forward). Good for personality-led / opinion / hot-take content.
- `editorial-mixed` — Editorial cover (magazine), mixed body slide treatments. Good for story / case-study carousels where each slide has a different visual rhythm.

Pick by content type:
- Educational / how-to / "N signs of..." → `type-allnumbers`
- Hot take / opinion / personality → `sticker-editorial`
- Case study / customer story → `editorial-mixed`

**For Story posts** — pick one of the story template's three direction styles:
- `A` — Spotlight Dark. Brand-led campaigns: eyebrow → headline → divider pill, dark backgrounds, accent color leading. Good for product launches, brand campaigns, urgent CTAs.
- `B` — Editorial Stat. When a single big number is the story (oversized stat as hero). Good for ROI proof, benchmark posts, "X% faster" / "$Y saved" data points.
- `C` — Cream Press. Light, magazine-style. Good for case studies, testimonials, founder posts, customer stories.

Pick by content type:
- Brand campaign / launch / direct CTA → `A`
- Stat-driven proof / benchmark → `B`
- Case study / testimonial / founder voice → `C`

**For LinkedIn single-image posts** (`linkedin-post` template) — pick one of three directions:
- `A` — Hook Headline (text-led). Narrative / opinion posts.
- `B` — Stat Hero (one big number). Proof / results posts.
- `C` — Pull Quote (editorial). Testimonials, founder posts, press mentions.

**For IG/FB single-image posts** (`meta-post` template) — pick one of three directions:
- `A` — Hero Visual (full-bleed photo + headline). Brand campaigns, launches, scroll-stoppers.
- `B` — Quote Card (editorial). Testimonials, founder voice, press quotes.
- `C` — Listicle Teaser (3–5 bullets). Value-led / educational posts.

**For any format with no matching fb.ai template** — leave Direction blank.

If you assign a Direction the brand's template doesn't support, content-generator falls back to the template defaults and logs a warning — so before assigning, check the template's `manifest` (via `fivebucks_get_template`) for the `direction` / `coverVariant` / `bodyVariant` `options` the brand's template actually exposes.

### Direction reference — fb.ai handles slide selection server-side

fb.ai's renderer filters `linkedin-post` and `meta-post` by the post's `direction` (A/B/C) **server-side** and screenshots the one matching slide. So for these types just set **Direction** (above) — there is no separate slide column to fill, and `content-generator` no longer passes `slide_ids`. Same for `meta-story` (`_direction` → 6 slides) and `meta-carousel` (renders all 6). Slide selection is fb.ai's job; your job is picking the Direction.

### Content mix across 14 posts:

**Adapt the mix based on Step 1b research findings.** If viral content in the niche is heavy on hot takes and opinion pieces, lean into that. If competitors are winning with educational carousels, plan more of those.

Default mix (use ONLY if research is unavailable):
- Educational / How-to: 5 posts
- Social Proof / Results: 3 posts
- Product Spotlight: 3 posts
- Direct CTA: 2 posts
- Engagement / Opinion: 1 post

Research-driven adjustments:
- If a viral topic is relevant to the brand → dedicate 2-3 posts to ride the trend (different angles per platform)
- If competitor content is heavily educational → differentiate with more social proof or opinion content
- If a keyword is trending → build posts around that keyword's intent
- Always keep at least 2 Direct CTA posts per week (non-negotiable)

### Rotation rules:
- No persona more than 2× in the week
- Rotate across all personas defined in `brands/{brand}/audience.md` (e.g. `content-mgr`, `seo-pro`, `sales-rep`, `agency-owner`, `solopreneur`, `growth-mktr`)
- Direct CTAs at least 3 slots apart per platform
- No same topic twice
- **Instagram Story and Facebook Story must never fall on the same day.** The fixed slot table guarantees this (Tue IG, Thu IG, Fri FB — no pair shares a date). If a conflict is somehow detected, abort and report rather than moving fixed slots.

### Story image_brief wrapping

Before saving any post row to Notion, apply this transformation to `image_brief` for Story posts.

```python
STORY_TEMPLATE = (
    "Photorealistic, full-bleed vertical portrait image for a 9:16 social media Story. "
    "{SCENE_DESCRIPTION}. The scene fills the ENTIRE frame from top to bottom — no empty areas, "
    "no plain backgrounds, no flat colour zones anywhere in the image. Rich environmental detail "
    "in the upper, middle, AND lower thirds of the frame. Cinematic lighting, editorial quality. "
    "Shot as if for a magazine cover in portrait orientation. "
    "Do not include any text, logos, or UI elements."
)

if format.lower() == "story":
    image_brief = STORY_TEMPLATE.format(SCENE_DESCRIPTION=image_brief)
```

**Rules:**
- Apply AFTER writing the raw scene description (the inner `SCENE_DESCRIPTION`) — the template adds composition constraints, not content.
- The raw scene description must already end with "No text. No logos. No watermarks." — the template's final sentence supersedes it but the rule still guards earlier drafting.
- For LinkedIn posts and all Carousel posts (any aspect ratio), do NOT apply the template — pass `image_brief` verbatim.
- The wrapped string (not the raw scene) is what gets saved to Notion `Image Brief` and read verbatim by `content-generator`.

**Example:**

*Raw scene (before wrapping):*
> A glowing analogue clock face on a clean minimal background, concept of time and urgency. No text. No logos. No watermarks.

*Wrapped image_brief (saved to Notion):*
> Photorealistic, full-bleed vertical portrait image for a 9:16 social media Story. A glowing analogue clock face on a clean minimal background, concept of time and urgency. No text. No logos. No watermarks. The scene fills the ENTIRE frame from top to bottom — no empty areas, no plain backgrounds, no flat colour zones anywhere in the image. Rich environmental detail in the upper, middle, AND lower thirds of the frame. Cinematic lighting, editorial quality. Shot as if for a magazine cover in portrait orientation. Do not include any text, logos, or UI elements.

---

## Step 2c — Verify Format Rules Before Saving

*Static Mode only — skipped in YouTube-First Mode.*

Run this check on **every row** before proceeding to Step 3. Fix any failing row in place — do not save until all rows pass.

| Format | Platform | Direction required | Valid Direction values |
|---|---|---|---|
| LinkedIn Post | LinkedIn | ✅ Yes | `A` / `B` / `C` |
| LinkedIn Carousel | LinkedIn | ❌ No | *(blank)* |
| Meta Post (FB or IG) | Facebook / Instagram | ✅ Yes | `A` / `B` / `C` |
| Meta Story | Facebook / Instagram | ✅ Yes | `A` / `B` / `C` |
| Meta Carousel (FB or IG) | Facebook / Instagram | ✅ Yes | `type-allnumbers` / `sticker-editorial` / `editorial-mixed` |

**Golden rule: every row must have Direction populated unless it is `LinkedIn Carousel`.**

**Story conflict rule: Instagram Story and Facebook Story must not share the same date.** The fixed slot table guarantees this — if a conflict appears, abort and report; do not attempt to move fixed slots.

If any row fails, correct it before Step 3 — do not post a failing row as a known issue.

---

## Step 3 — Save to Notion

*Static Mode only — YouTube-First Mode already saved its calendar in Step 2a. (Step 3a's DB bootstrap below is shared: Step 2a reuses it on first runs.)*

Use **Notion MCP** to save the calendar to Notion. The calendar page must live **inside the brand's social-calendar database** so `content-generator` Step 1 can find it via `${BRAND}_NOTION_DB`.

Page title: `SocialCalendar_[DDMon]-[DDMonYYYY]`
e.g. `SocialCalendar_17Mar-22Mar2026`

### Step 3a — Ensure the brand's social-calendar DB exists (first-run only)

This step is primarily for the **first-ever calendar run** for a brand. On subsequent weekly runs, the env var is already set and the DB already exists — fetch and proceed.

Read `${BRAND}_NOTION_DB` from `.claude/settings.local.json` (e.g. `FIVEBUCKS_NOTION_DB`).

**Decision:**

```
IF env var is set:
  fetch the DB → if fetch succeeds → DB exists → DO NOT create. Skip to Step 3b.
  (only create if fetch returns 404 / not_found, meaning the DB was deleted)

IF env var is NOT set:
  → first-ever run for this brand → create the DB (instructions below).
```

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: "${BRAND}_NOTION_DB"
```

**If env var is set and fetch succeeds → skip to Step 3b. Do not create another DB.**

**Create only when env var is unset (or fetch returns not_found):**
```
Use mcp__claude_ai_Notion__notion-create-database:
- parent: { "type": "page_id", "page_id": "<brand_parent_page_or_workspace_root>" }
- title: "{Brand Name} Social Media Calendar"
- properties: {
    "Name":          { "title": {} },
    "Date Range":    { "rich_text": {} },
    "Status":        { "select": { "options": [
                        {"name": "Planned"},
                        {"name": "Published"},
                        {"name": "Archived"}
                      ] } },
    "Posts":         { "number": { "format": "number" } },
    "Created":       { "created_time": {} }
  }
```

If no brand parent page exists yet, `notion-search` for `"{Brand}"` first; if nothing is found, create a parent page with `notion-create-pages` titled `"{Brand Name}"` at the workspace root, then nest the DB under it.

After creation, **persist the new DB ID back to `.claude/settings.local.json`** under `env.{BRAND}_NOTION_DB`. Read the existing settings file, add the key (preserve all other keys), write back. This makes the DB discoverable by `content-generator` and by every future weekly social-calendar run.

Notify the user in chat (first-run only):
> Created new Notion DB **{Brand Name} Social Media Calendar** and saved its ID as `${BRAND}_NOTION_DB` in `.claude/settings.local.json`. Future runs will reuse this DB — no re-creation.

### Step 3b — Save local backup

Save local backup first: `outputs/{brand}/strategy/SocialCalendar_[DDMon]-[DDMonYYYY].md`

### Step 3c — Find or create this week's calendar page inside the brand DB

1. **Resolve the DB to a `data_source_url`** (needed for scoped search):
   ```
   Use mcp__claude_ai_Notion__notion-fetch:
   - id: "${BRAND}_NOTION_DB"
   ```
   Extract the `collection://` URL from the response — typically `data_sources[0].url`. Save as `data_source_url`.

2. **Check if the week's page already exists, scoped to the brand DB only:**
   ```
   Use mcp__claude_ai_Notion__notion-search:
   - query: "SocialCalendar_[DDMon]-[DDMonYYYY]"
   - data_source_url: <data_source_url from step 1>
   - query_type: "internal"
   ```
   ⚠️ Never run a bare workspace-wide `notion-search` for the page name — it can return another brand's calendar with the same week label. Always pass `data_source_url`.

3. **If no matching page → create it:**
   ```
   Use mcp__claude_ai_Notion__notion-create-pages:
   - parent: { "database_id": "${BRAND}_NOTION_DB" }
   - pages: [{
       "properties": { "Name": "SocialCalendar_[DDMon]-[DDMonYYYY]", "Status": "Planned", "Posts": 14 },
       "content": "<markdown of the calendar — heading + 11-column table + content mix + persona distribution>"
     }]
   ```
   The `content` field accepts markdown. Use a markdown table with **11 columns** — Date, Platform, Format, Topic, Persona, Content Angle, CTA, Hashtags, Image Brief, Direction, Status. The Notion connector converts markdown headings, tables, and paragraphs into the appropriate block types automatically.

4. **If the page already exists → update it in place:**
   ```
   Use mcp__claude_ai_Notion__notion-update-page:
   - page_id: <existing page id>
   - properties: { "Status": "Planned", "Posts": 14 }
   - replace_content: true
   - content: "<same markdown as step 3>"
   ```
   `replace_content: true` clears existing child blocks before appending the new content — avoids duplicate tables stacking up across re-runs.

5. Capture the returned page URL for the Slack notification.

**Brand-header sanity check before Slack:** the returned page's parent database title must contain the active brand. If somehow it doesn't (shouldn't happen given the DB-scoped flow), abort with a `failed` log — do not announce a calendar that landed in another brand's DB.

### Local backup file structure

```markdown
---
Date: YYYY-MM-DD
Skill Used: social-calendar
Brand: {brand}
Week: Mon DD Mon – Sat DD Mon YYYY
Status: Planned
Notion: {url}
---

# Social Calendar: [Mon DD Mon] – [Sat DD Mon YYYY]

| Date | Platform | Format | Topic | Persona | Content Angle | CTA | Hashtags | Image Brief | Direction | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 06 Apr 2026 | LinkedIn | Post | ... | ... | ... | ... | ... | ... | A | Planned |
| 06 Apr 2026 | Facebook | Post | ... | ... | ... | ... | ... | ... | B | Planned |
| 11 Apr 2026 | Instagram | Carousel | ... | ... | ... | ... | ... | ... | type-allnumbers | Planned |
... (14 data rows)

## Content Mix

| Type | Count | Posts |
|---|---|---|
| Educational / How-to | 5 | ... |
... (5 rows)

## Persona Distribution

| Persona | Count | Posts |
|---|---|---|
| content-mgr | 2 | ... |
... (6-7 rows)
```

---

## Notify via Slack

**Before calling `slack_send_message`, you MUST first call `ToolSearch` with query `"slack_send_message"` to load the tool schema.** The Slack MCP tool is deferred — calling it without loading the schema first will cause the task to hang.

DM the user via **Slack MCP** (`slack_send_message`, `channel_id: "$SLACK_NOTIFY_USER"`). Use the message that matches the mode you planned in:

**Static Mode:**
```
📅 [{brand}] Social Calendar Ready — Week of [DD Mon YYYY]
• 14 posts planned (Mon–Sat)
• Platforms: LinkedIn, Facebook, Instagram
• Mix: [x] edu / [x] proof / [x] product / [x] CTA / [x] engage
• Notion: [page URL]
```

**YouTube-First Mode:**
```
📅 [{brand}] Content Plan Ready — Week of [DD Mon YYYY]
• 1 YouTube video + [N] clips across [connected platforms]
• Video: [title]
• Notion: [page URL]
```

---

## Quality Checklist

- [ ] **Mode check:** read `brands/{brand}/brand.md` `## Content Strategy` before planning — YouTube-First Mode (Step 2a) if `Primary channel: youtube`, Static Mode (Step 2b) otherwise
- [ ] **YouTube-First:** YouTube Video Plan includes publish day/time; Clip Release Schedule includes publish day + time per clip for each connected platform only; comment-to-DM CTAs used; Trend Radar candidate marked Planned if used
- [ ] **Video structure applied** — if trend_db candidate had a `video_structure` JSON, the Video Structure table is present in the calendar with all 6 elements adapted for the brand
- [ ] **Credibility anchor is brand-appropriate** — the hook uses the brand's own credential (from `brand.md`), not the competitor's claim
- [ ] **Clips trace to video sections** — every clip's `Source Section` maps to a valid section in the Video Structure table; no orphan clips about unrelated topics
- [ ] **Competitor Structure Applied reference** — source attribution present with competitor channel, video title, and URL
- [ ] **Static:** Exactly 14 posts
- [ ] Formats match fixed slot table
- [ ] Monday LinkedIn = Post, Monday Facebook = Post, Monday Instagram = Post
- [ ] Tuesday Instagram = Story, Wednesday LinkedIn = Carousel
- [ ] Thursday Facebook = Post, Thursday Instagram = Story
- [ ] Friday Facebook = Story, Friday LinkedIn = Post, Friday Instagram = Carousel, Saturday Instagram = Carousel
- [ ] **Static:** Persona rotation applied — no persona used more than 2× across the 14 posts
- [ ] Content mix is research-driven (Step 1b) — if research was available, mix reflects findings; if research was unavailable, default mix used (5 edu / 3 proof / 3 product / 2 CTA / 1 engage); at minimum 2 Direct CTA posts present
- [ ] All raw scene descriptions (before wrapping) end with "No text. No logos. No watermarks."
- [ ] Story image briefs are wrapped in the full-frame composition template before saving to Notion — the saved `Image Brief` cell must contain "fills the ENTIRE frame"; LinkedIn and Carousel briefs are saved verbatim (no wrapping)
- [ ] **Step 2c verification passed (Static Mode)** — every row passed the format-rules table (Direction correct per format type; no row missing Direction except `LinkedIn Carousel`)
- [ ] **Direction rotated for variety** — same-format posts spread across `A`/`B`/`C` (and carousel `coverVariant-bodyVariant` combos); no long runs of the same Direction in one platform's feed
- [ ] **No same-day Stories** — Instagram Story and Facebook Story are on different dates
- [ ] Notion page URL logged to memory
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

**Mode-aware:** the payload below is the **Static Mode** shape. In **YouTube-First Mode**, set `mode: "youtube"`, drop `posts_planned` / `posts` / `content_mix` / `persona_distribution`, and instead log `videos_planned: 1`, `clips_planned: [N]`, and a `clips[]` array (platform / duration / caption angle); keep `calendar_status` + `notion_url`.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "social-calendar"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "mode": "static",
    "date": "YYYY-MM-DD",
    "week": "DD-DD Mon YYYY",
    "posts_planned": 14,
    "calendar_status": "Planned",
    "notion_url": "https://notion.so/...",
    "posts": [{ "date": "DD Mon", "platform": "LinkedIn", "topic": "...", "persona": "...", "format": "<Post|Story|Carousel>", "status": "Planned" }],
    "content_mix": [{ "type": "<Educational / How-to|Social Proof / Results|Product Spotlight|Direct CTA|Engagement / Opinion>", "count": 5, "percentage": 35.7 }],
    "persona_distribution": [{ "persona": "seo-pro", "count": 3 }]
  }
```
