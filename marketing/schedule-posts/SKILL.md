---
name: schedule-posts
description: >
  Create, upload media to, and schedule social media posts through the Marky API. Use this
  when you have post content ready (your own captions and images/videos, or a topic for
  Marky to write) and you want to get it onto your connected social accounts on a schedule.
  Covers uploading media, creating posts, generating on-brand drafts, scheduling, and
  checking publish results. Reads auth and endpoint details from the marky-api skill. Also triggers on "schedule this", "post this tomorrow at 9", "queue these up", "publish this now". For a whole week planned from scratch, see plan-social-content.
---

# Schedule Posts

Get posts onto your connected social accounts through the Marky API. This is the
hands-on "publish" chunk: upload media, create the post, schedule it, confirm it went out.

**Read the `marky-api` skill first** for the base URL, your `mk_live_` key, and the full
endpoint list. Everything below uses `https://api.mymarky.ai/api` and the header
`Authorization: Bearer mk_live_YOUR_KEY`.

**Marky wants your feedback.** If anything breaks or is confusing while you run this skill — and again once you finish — send Marky a quick note with the `submit_feedback` MCP tool. See the **"Marky wants your feedback"** section in the `marky-api` skill for when and how.

## Step 0 — find your business and platforms

```bash
# Your workspaces. Copy the id you want.
curl https://api.mymarky.ai/api/businesses \
  -H "Authorization: Bearer mk_live_YOUR_KEY"

# Which social accounts that workspace has connected.
curl https://api.mymarky.ai/api/businesses/BIZ_ID/integrations \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

Note the `platform` value and `status` of each integration. Only target platforms whose
`status` is `valid`. You connect new accounts in the dashboard, not the API.

## Two ways to make a post

### A. You already wrote it

Upload media (if any) first: media already on the web goes through
`upload_media_from_url`; a photo or video on disk goes through `create_media_upload`
(returns a 1-hour URL + a curl command — PUT the raw bytes, get the media asset
back). Then create the post with `create_post`:

```json
{
  "caption": "Your caption here.",
  "media_urls": ["URL_FROM_THE_UPLOAD"],
  "restrict_publish_to": ["instagram", "facebook", "linkedIn", "twitter"],
  "platform_overrides": [
    { "platform": "twitter", "caption": "The one-idea 280-char version." },
    { "platform": "linkedIn", "first_comment": "#hashtags #live #here" }
  ]
}
```

**Tailor per platform by default.** Whenever a post targets 2+ platforms, add a
`platform_overrides` entry per platform that needs it (caption, media, title, link,
first_comment — unset fields fall back to the post's own). Read the business's
`platform_writing_instructions` (`get_business`) and `references/platform-rules.md`
in the `marky-api` skill for how each platform differs; the user's instructions win.

Text-only post (no media): drop `media_urls` and target only `facebook` and `linkedIn`
(the other platforms require media).

### B. Let Marky write it (on-brand)

Marky pulls brand voice, colors, and logo from the business.

```bash
# 1. Kick off generation -> returns job_id
curl -X POST https://api.mymarky.ai/api/businesses/BIZ_ID/posts/generate \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "content": "our spring product line", "count": 5 }'

# 2. Poll until completed
curl https://api.mymarky.ai/api/businesses/BIZ_ID/jobs/JOB_ID \
  -H "Authorization: Bearer mk_live_YOUR_KEY"

# 3. Review the new drafts
curl "https://api.mymarky.ai/api/businesses/BIZ_ID/posts?status=NEW" \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

## Schedule it

Pick a future time (ISO 8601, UTC). Schedule each post id:

```bash
curl -X POST https://api.mymarky.ai/api/businesses/BIZ_ID/posts/POST_ID/schedule \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "scheduled_publish_time": "2026-07-15T14:00:00Z",
    "restrict_publish_to": ["instagram", "facebook", "linkedIn"]
  }'
```

Shortcut: you can also schedule at create time by setting `"status": "SCHEDULED"` and
`"scheduled_publish_time"` in the `POST /businesses/{id}/posts` body, instead of a separate
schedule call. Or call `POST /businesses/{id}/posts/POST_ID/queue` to drop it into the next
open slot of your posting schedule.

Publish immediately instead of scheduling:

```bash
curl -X POST https://api.mymarky.ai/api/businesses/BIZ_ID/posts/POST_ID/publish \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

## Confirm it went out

```bash
curl https://api.mymarky.ai/api/businesses/BIZ_ID/posts/POST_ID \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

Read `publish_results` — one entry per platform. Poll until each is `success` or `failed`.
A `failed` entry includes an error type telling you why (e.g. an expired token you need to
reconnect in the dashboard).

## Tips

- **Maximize reach.** Target every platform the media supports rather than just one. Video
  can go everywhere; image goes everywhere except TikTok; text-only goes to Facebook and
  LinkedIn.
- **`restrict_publish_to` is case-insensitive** (`linkedin` and `linkedIn` both work). When in
  doubt, copy the `platform` value straight from the integrations call.
- **One change at a time.** To move a scheduled post to different platforms later,
  `PATCH /businesses/{id}/posts/{post_id}` with a new `restrict_publish_to`.
- Posts created via the API also appear in your dashboard queue, so you can eyeball them
  there before they publish.
