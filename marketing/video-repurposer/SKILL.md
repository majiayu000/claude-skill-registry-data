---
name: video-repurposer
description: Take a published YouTube video URL, extract clips per the social calendar's Clip Release Schedule, write platform-native captions with comment-to-DM CTAs, and publish to connected platforms (LinkedIn, Instagram, TikTok, Twitter/X, Facebook) via Zernio at the scheduled times.
allowed-tools: Read, Grep, Glob, Bash
area: Marketing
use_for: "Repurpose a YouTube video into platform-specific clips with captions for all connected platforms. Run after the weekly YouTube video is uploaded."
deps:
  mcp: ["Notion", "Slack", "Zernio (publishing)"]
  gateway: ["FiveAgents (logging)"]
  files: ["brand.md", "audience.md"]
  env: ["`${BRAND}_ZERNIO_LI`", "`${BRAND}_ZERNIO_IG`", "`${BRAND}_ZERNIO_TT`", "`${BRAND}_ZERNIO_TW`", "`${BRAND}_ZERNIO_FB`", "`${BRAND}_NOTION_DB`"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.19.0 | July 03, 2026 |

### Change Log

**v2.19.0** — July 03, 2026
- **Corrected the Zernio publish mechanics to the real MCP schema (fixes the v2.18.0 migration bug).** v2.18.0 wrongly repointed `late_presign_upload` → `media_generate_upload_link`, but that Zernio tool is a **browser-only** upload flow — PUTting to it silently fails. Clips now upload via `media_get_media_presigned_url(filename, content_type, size)` → PUT → public URL, `validate_media` before publish. `posts_create` corrected to the real signature: `content`, `platform` (single string), `account_id`, `media_urls` (string), `publish_now`/`schedule_minutes` — one call per platform (no `platforms[]`, no `platformSpecificData`); scheduling uses integer `schedule_minutes` via Python `datetime`.

**v2.18.0** — July 01, 2026
- **Zernio migrated to its own MCP (gateway v1.7.4).** Repointed `late_presign_upload` → `media_generate_upload_link` and `late_create_post` → `posts_create` to Zernio's native MCP tool names; dropped the `fiveagents_api_key` param from those calls (Zernio is now OAuth-connected, not gateway-routed); renamed `${BRAND}_LATE_*` env vars to `${BRAND}_ZERNIO_*` and internal `late_*` PublishLog fields to `zernio_*`.

**v2.14.0** — May 29, 2026
- New skill. Phase 4–5 of the YouTube-First content pipeline. Downloads the week's YouTube video via yt-dlp, reads the Clip Release Schedule from the Notion social calendar, extracts clips via ffmpeg, writes platform-native captions, and publishes to connected platforms via Zernio at the times specified in the schedule.

---

# SKILL.md — Video Repurposer

## Before Executing

Read `agents/link.md` and `brands/{brand}/brand.md` before starting. Load credentials from `.claude/settings.local.json`.

## Role

Take the week's published YouTube video, extract clips per the Clip Release Schedule in the social calendar, write platform-native captions, and publish each clip to the correct platform at the scheduled time.

---

## Step 0 — Load credentials + validate

```python
import os, json
from pathlib import Path

def load_credentials():
    search = Path(os.getcwd())
    for p in [search] + list(search.parents):
        settings_file = p / ".claude" / "settings.local.json"
        if settings_file.exists():
            data = json.loads(settings_file.read_text())
            for k, v in data.get("env", {}).items():
                if not os.environ.get(k):
                    os.environ[k] = v
            return True
    return False

load_credentials()
```

Get the YouTube video URL from the user or from this week's social calendar page in `${BRAND}_NOTION_DB`.

---

## Step 1 — Read the Clip Release Schedule from Notion

Fetch this week's social calendar page from `${BRAND}_NOTION_DB` (search for `SocialCalendar_[DDMon]-[DDMonYYYY]`). Read the Clip Release Schedule table:

- Clip #, Platform, Publish Day, Publish Time, Duration, Moment to Clip, Caption Angle, Hook Archetype, CTA

Only process clips for platforms where the matching env var is set (`${BRAND}_ZERNIO_LI`, `${BRAND}_ZERNIO_IG`, `${BRAND}_ZERNIO_TT`, `${BRAND}_ZERNIO_TW`, `${BRAND}_ZERNIO_FB`). Skip platforms with missing env vars and log the gap.

---

## Step 2 — Download video

```bash
python3 -m pip install yt-dlp --break-system-packages -q
python3 -m yt_dlp -o "tmp/{brand}/source_video.%(ext)s" "{youtube_url}"
```

---

## Step 3 — Extract clips

For each clip in the schedule:

```bash
pip install ffmpeg-python --break-system-packages -q
ffmpeg -i tmp/{brand}/source_video.mp4 -ss {start_time} -to {end_time} -c copy tmp/{brand}/clip_{n}_{platform}.mp4
```

If exact timestamps are not in the schedule, use the `Moment to Clip` description to identify the segment. Use Whisper transcription if needed:

```bash
python3 -m pip install openai-whisper --break-system-packages -q
python3 -m whisper tmp/{brand}/source_video.mp4 --output_dir tmp/{brand}/ --output_format srt
```

Match the described moment against the transcript to find the timestamp.

---

## Step 4 — Write captions

For each clip, the caption is already written in the Notion calendar Captions section. Read it verbatim. If absent, write a new caption using:
- Voice and tone from `brand.md`
- Caption angle and hook archetype from the Clip Release Schedule
- Comment-to-DM CTA from the schedule
- Platform-native format (length, hashtag count per platform guidelines)

---

## Step 5 — Publish via Zernio

The clip is a **local video file**, so upload it programmatically via `media_get_media_presigned_url` — **not** `media_generate_upload_link` (that returns a browser upload-page URL for a human; PUTting to it silently fails). Resolve account IDs via `accounts_list` at run start.

For each clip:
1. `media_get_media_presigned_url` (filename, content_type: `"video/mp4"`, size) → returns an upload URL (PUT target) + a public URL
2. Upload the clip via `requests.put` to that upload URL
3. `validate_media(url=public_url)` → confirm `valid: true`
4. `posts_create` (one call per platform): `content` (caption), `platform` (single string), `account_id`, `media_urls` (the public URL), and either `publish_now: true` or `schedule_minutes` (integer minutes from now, computed via Python `datetime`)

```python
# Platform account ID mapping (verify against accounts_list at run start)
platform_ids = {
    "LinkedIn": os.environ.get(f"{brand_upper}_ZERNIO_LI"),
    "Instagram": os.environ.get(f"{brand_upper}_ZERNIO_IG"),
    "TikTok": os.environ.get(f"{brand_upper}_ZERNIO_TT"),
    "Twitter/X": os.environ.get(f"{brand_upper}_ZERNIO_TW"),
    "Facebook": os.environ.get(f"{brand_upper}_ZERNIO_FB"),
}
```

Schedule each clip at the `Publish Time` from the Clip Release Schedule: convert the target time to UTC, then compute `schedule_minutes` as integer minutes from now via Python `datetime`. `posts_create` takes one `platform` + `account_id` per call (no `platforms[]` array) and has no `platformSpecificData` param.

---

## Step 6 — Update Notion + PublishLog

- Update each clip row in the Notion calendar page: `Status = Published`, add post URL
- Append to `outputs/{brand}/published/PublishLog_[DDMonYYYY].md` — **use the exact same columns as `social-publisher`** so `content-performance-analyst` can join on `Zernio ID`:

```markdown
| Date | Platform | Topic | Zernio ID | Post URL | Status | Published At |
|---|---|---|---|---|---|---|
| {date} | {platform} | {clip moment} | {zernio_id} | {url} | Published | {publish_time} |
```

---

## Step 7 — Slack notification

**Load `slack_send_message` via ToolSearch before calling.** DM `$SLACK_NOTIFY_USER`:

```
🎬 [{brand}] Video repurposed — {YouTube title}
• {N} clips published/scheduled
• {one line per connected platform: Platform: {publish_time}}
• Notion calendar updated
```

---

## Step 8 — Log to dashboard

```
fiveagents_log_run:
- skill: "video-repurposer"
- brand: {brand}
- status: success | partial | failed
- summary: "{N} clips published to {platforms} from: {YouTube title}"
- metrics: {
    "youtube_url": "{url}",
    "clips_published": N,
    "platforms": ["LinkedIn", "Instagram", ...],
    "publish_times": { "LinkedIn": "...", ... },
    "skipped_platforms": [] // any planned platform whose _ZERNIO_ env var is unset
  }
```

---

## Quality Checklist

- [ ] Credentials loaded
- [ ] Clip Release Schedule read from Notion calendar
- [ ] Only connected platforms published (missing env vars skipped + logged)
- [ ] Each clip extracted at the correct moment (timestamp or transcript match)
- [ ] Captions read from Notion or written platform-natively with comment-to-DM CTAs
- [ ] Clips scheduled at correct Publish Time from the schedule
- [ ] Notion clip rows updated to Published with post URL
- [ ] PublishLog written
- [ ] Slack notification sent
- [ ] Dashboard logged

---

## Part of the pipeline

**Phase 4–5 of the YouTube-First content loop.** Runs after the YouTube video is uploaded.

```
social-calendar (Clip Release Schedule) → video-repurposer (download → extract → publish) → PublishLog (feeds content-performance-analyst Phase 1)
```
