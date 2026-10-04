---
name: social-publisher
description: Publishing to LinkedIn, Facebook, Instagram, Twitter/X via Zernio for any active brand
allowed-tools: Read, Grep, Glob, Bash
area: Marketing
use_for: "Publishing to LinkedIn, Facebook, Instagram, Twitter/X via Zernio"
deps:
  mcp: ["Slack", "Zernio"]
  gateway: ["fivebucks (opt — consumes fivebucks_render_post signed URLs as media_urls; **scope: social_posts**)"]
  files: ["brand.md"]
  env: ["`${BRAND}_ZERNIO_FB`", "`${BRAND}_ZERNIO_IG`", "`${BRAND}_ZERNIO_LI` (per-platform; only required for platforms the brand publishes to)"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.20.0 | July 12, 2026 |

**Description:** Publishing to LinkedIn, Facebook, Instagram, Twitter/X via Zernio for any active brand

### Change Log

**v2.20.0** — July 12, 2026
- **Declared the fb.ai dependency and its required scope.** fb.ai API keys are now scoped; this skill's `deps.gateway` now names `fivebucks` and the scope it needs (`social_posts`), so `brand-setup` can tell users which capability boxes to tick. No behaviour change — see `agents/link.md` for the scope/error/quota contract.

**v2.19.0** — July 03, 2026
- **Corrected the Zernio publish mechanics to the real MCP schema (fixes the v2.18.0 migration bug).** The v2.18.0 migration wrongly assumed `media_generate_upload_link` was a programmatic S3 presign (like the old `late_presign_upload`) — it is actually a **browser-only** upload flow, so PUTting to it silently fails. Now: (1) local files upload via `media_get_media_presigned_url(filename, content_type, size)`; (2) fb.ai `fivebucks_render_post` signed URLs pass **directly** as `media_urls` with no re-host (the publisher fetches/caches at post-creation time, so ~1h expiry is safe for scheduling); (3) `validate_media(url)` before publish; (4) local backup via `curl` after render.
- **`posts_create` signature corrected.** Real params are `content`, `platform` (single string), `account_id`, `media_urls` (comma-separated string — not a `media_items` array), `publish_now` / `is_draft` / `schedule_minutes` (integer). Scheduling now computes `schedule_minutes` via Python `datetime` (was `scheduled_for` + `timezone`). One `posts_create` per platform (no `platforms[]` array). `account_id` always passed, resolved via `accounts_list` at run start.
- **`posts_update` scope corrected.** It accepts only `content` / `scheduled_for` / `title` — it cannot flip `is_draft`/`publish_now` or change media. The old "publish a draft via `posts_update(is_draft:false, publish_now:true)`" pattern was invalid and is removed.
- **`platformSpecificData.contentType` removed.** Zernio `posts_create` has no such param — Story/Reel content-typing is not expressible; images publish as feed content. Removed the delete-and-recreate-for-contentType notes.

**v2.18.0** — July 01, 2026
- **Zernio migrated to its own MCP (gateway v1.7.4).** Repointed `late_list_posts` → `posts_list`, `late_create_post` → `posts_create`, `late_update_post` → `posts_update`, and `late_presign_upload` → `media_generate_upload_link` to Zernio's native MCP tool names; dropped the `fiveagents_api_key` param from those calls (Zernio is now OAuth-connected, not gateway-routed); renamed `${BRAND}_LATE_*` env vars to `${BRAND}_ZERNIO_*` and internal `late_*` PublishLog fields to `zernio_*`.

**v2.3.0** — May 28, 2026
- **PublishLog is now the performance join key.** Step 4 captures the platform post URL (`platformPostUrl`) alongside the Zernio ID, and records `Date` + `Topic` + `Platform` so `content-performance-analyst` can join each published post back to its social-calendar planning row (Persona / Format / Content Angle / Direction / hook archetype) and fetch per-post engagement. Closes the create→publish→measure loop.

**v2.2.5** — April 26, 2026
- Added "Before Executing" section — reads agents/link.md before starting

# SKILL.md — Social Publisher

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are the social media publisher for the active brand. Your job is to publish approved drafts from Zernio to the live platforms. Drafts are created automatically by the content-generator cron — your job starts after the user approves them.

**Never write copy. Never generate images. Never create new drafts.** Those happen upstream in content-generator. This skill is publish-only.

---

## When to use

- "Publish today's posts" / "push the drafts live"
- "Schedule [post] for [time]"
- "What drafts are pending approval?"
- Publishing or scheduling a specific approved draft

Do NOT use this skill for:
- Writing copy → content-creation
- Generating images → creative-designer
- Creating the weekly calendar → social-calendar
- Generating draft content → content-generator

---

## Zernio publishing reference

Zernio ships its own MCP server — its tools are OAuth/session-scoped and take no `fiveagents_api_key` param.

### Account / Profile IDs

Read from env vars using brand prefix — all stored in `.claude/settings.local.json`:

```
{BRAND}_ZERNIO_FB   → Facebook account ID
{BRAND}_ZERNIO_IG   → Instagram account ID
{BRAND}_ZERNIO_LI   → LinkedIn account ID
```

Example: `${BRAND}_ZERNIO_FB`, `${BRAND}_ZERNIO_IG`, `${BRAND}_ZERNIO_LI`

Available Zernio MCP tools: `posts_list`, `posts_create`, `posts_update`, `posts_delete`, `accounts_list`, `validate_media`, `media_get_media_presigned_url`, `media_generate_upload_link`.

### Resolve account IDs at run start

Call `accounts_list` once at the start of the session and build a `{platform → account_id}` map. **Always pass `account_id` explicitly to `posts_create`** — when a brand has multiple accounts on the same platform, omitting it errors. The `{BRAND}_ZERNIO_*` env vars hold the canonical IDs; use `accounts_list` to confirm they are still valid.

### Media handling — how an image becomes a `media_urls` value

`posts_create` takes `media_urls` as a **comma-separated string of public URLs** (not a `media_items` array). There are two ways to obtain a public URL:

1. **Already a signed URL (fb.ai `fivebucks_render_post` output):** pass it **directly** as `media_urls` — do **not** re-host. The publisher fetches and caches the image at post-creation time (not at publish time), so the ~1-hour signed-URL expiry does not affect scheduled delivery as long as `posts_create` runs in the same session as the render. Call `validate_media(url)` first; if `valid: true`, proceed.
2. **A local file on disk (e.g. a Gemini `_final.png`):** upload it via `media_get_media_presigned_url(filename, content_type, size)` → PUT the bytes to the returned upload URL → use the returned public URL as `media_urls`.

⚠️ **Never use `media_generate_upload_link` in automated flows.** It returns a **browser** upload-page URL for a human to drag-drop files — it is NOT a programmatic presigned S3 URL. PUTting to it silently fails. Use `media_get_media_presigned_url` for programmatic uploads.

**Local backup:** immediately after obtaining a signed render URL, download it to disk (`curl -s -L "<signed_url>" -o "<local_path>"`) so the asset survives even if a later publish step fails.

Note: Zernio's `posts_create` has **no** `platformSpecificData.contentType` parameter — Story/Reel content-typing is not expressible through this tool, so image posts publish as feed content regardless of dimensions. Publish one `posts_create` per platform (there is no `platforms[]` array).

---

## Platform specs

| Platform | Image | Max copy | Notes |
|---|---|---|---|
| LinkedIn | 1200×628px | 3,000 chars (210 visible before "see more") | 3–5 hashtags at end |
| Facebook | 1200×630px | 63,206 chars (keep <300 for reach) | Short hook + body + CTA |
| Instagram Post | 1080×1080px or 1080×1350px | 2,200 chars (125 visible) | Hashtags at end, no links in caption |
| Instagram Reel | 1080×1920px (video) | 2,200 chars | Video required |
| Instagram Story | 1080×1920px (video/image) | Not displayed — visual only | Caption ignored; send hashtags only or empty string |
| Facebook Reel | 1080×1920px (video) | Caption optional | Video required |
| Facebook Story | 1080×1920px (video/image) | Not displayed — visual only | Caption ignored; send hashtags only or empty string |

---

## Step-by-step workflow

### Step 1 — List pending drafts

Fetch all drafts from Zernio and show them to the user for review:

```
Use Zernio MCP tool `posts_list`:
- status: "draft"
- limit: 20
```

Present the list to the user and ask: "Which drafts should I publish? Publish now or schedule?"

### Step 2 — Confirm before publishing

**Always confirm with the user before publishing.** Show:
- Draft ID
- Platform
- First 150 chars of copy
- Image attached (yes/no)
- Publish time (now or scheduled)

### Step 3 — Publish or schedule

Publish with `posts_create` — pass `account_id` (from the run-start `accounts_list` map), the media URL as `media_urls`, and one call **per platform**. Resolve the image URL per the "Media handling" rules above (signed render URL passed directly, or local file via `media_get_media_presigned_url`), and `validate_media(url)` before creating the post.

**Option A — Publish now:**
```
Use Zernio MCP tool `posts_create`:
- content: "<copy text with hashtags>"
- platform: "<instagram|facebook|linkedin>"
- account_id: "<from accounts_list map>"
- media_urls: "<public image URL>"   # comma-separated for multiple images
- publish_now: true
```

**Option B — Schedule for a specific time:** compute `schedule_minutes` (integer minutes from now) precisely with Python `datetime` — do not estimate or hardcode.
```python
python3 -c "from datetime import datetime, timezone; now=datetime.now(timezone.utc); target=datetime(YYYY,MM,DD,HH,MM,SS,tzinfo=timezone.utc); print(int((target-now).total_seconds()/60))"
```
```
Use Zernio MCP tool `posts_create`:
- content: "<copy text with hashtags>"
- platform: "<instagram|facebook|linkedin>"
- account_id: "<from accounts_list map>"
- media_urls: "<public image URL>"
- schedule_minutes: <integer from the datetime calc above>
```

**To reschedule an already-created scheduled post:** `posts_update(post_id, scheduled_for: "<ISO 8601 UTC>")` — `posts_update` accepts only `content`, `scheduled_for`, and `title`; it cannot flip `is_draft`/`publish_now` or change media. To change media or platform, delete and re-create.

Default publish times (convert from brand timezone to UTC using `brands/{brand}/brand.md` Locale):
| Platform | Local Time | Notes |
|---|---|---|
| LinkedIn | 09:00 | Morning — professional audience |
| Facebook | 12:00 | Lunch break — casual browsing |
| Instagram | 18:00 | Evening — peak engagement |

### Step 4 — Log result (this is the performance join key)

Append to `outputs/{brand}/published/PublishLog_[DDMonYYYY].md`. **Capture the platform post URL (`platformPostUrl` from the Zernio publish response) alongside the Zernio ID** — this log is the join key `content-performance-analyst` uses later to match per-post engagement back to the planned post.

```markdown
## [DDMonYYYY] Publish Log

| Date | Platform | Topic | Zernio ID | Post URL | Status | Published At |
|---|---|---|---|---|---|---|
| 13 Mar 2026 | LinkedIn | AI Search SEO | 69b... | https://www.linkedin.com/feed/update/... | published | 2026-03-13T01:00Z |
| 13 Mar 2026 | Facebook | Replace 5 Tools | 69b... | https://www.facebook.com/.../posts/... | scheduled | 2026-03-13T04:00Z |
```

- **`Date` + `Topic` + `Platform`** let `content-performance-analyst` join each published post back to its planning row in the brand's social-calendar (`${BRAND}_NOTION_DB`) — recovering Persona / Format / Content Angle / Direction / hook archetype.
- **`Zernio ID` + `Post URL`** are the keys for fetching engagement from Zernio `posts_list` (matched by Zernio post ID); the URL is the human-readable fallback for matching.
- If the publish response omits `platformPostUrl` (some platforms return it asynchronously), record the Zernio ID and leave the URL blank — re-fetch via `posts_list` on the next analyst run.

### Step 5 — Notify via Slack

Send a summary to the user via Slack MCP (`slack_send_message`, `channel_id: "$SLACK_NOTIFY_USER"`):

```
🚀 [{brand}] Posts published for [DD Mon YYYY]

✅ LinkedIn — [Topic] — live
📅 Facebook — [Topic] — scheduled 12:00 [timezone]
📅 Instagram — [Topic] — scheduled 18:00 [timezone]
```

---

## Quality checklist

- [ ] Drafts listed and shown to user before any action
- [ ] User confirmed which posts to publish and when
- [ ] No copy changes made (publish as-is from draft)
- [ ] Account IDs resolved via `accounts_list` at run start; `account_id` passed to every `posts_create`
- [ ] Media URL obtained correctly: signed render URL passed directly, or local file via `media_get_media_presigned_url` (never `media_generate_upload_link` in automated flows); `validate_media` returned `valid: true` before publish
- [ ] Scheduling uses `schedule_minutes` (integer) computed via Python `datetime` — not estimated
- [ ] Publish log saved to `outputs/{brand}/published/`
- [ ] Slack notification sent after publish
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "social-publisher"
- brand: "<active-brand>"
- status: "<success|partial|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "posts_published": 0,
    "posts_failed": 0,
    "posts": [
      { "platform": "Facebook", "topic": "...", "zernio_post_id": "...", "status": "published", "published_at": "ISO timestamp", "url": "https://...", "notes": null }
    ]
  }
```
