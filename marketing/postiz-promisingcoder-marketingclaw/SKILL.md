---
name: postiz
description: "Publishing and scheduling social posts across connected networks (X, LinkedIn, Facebook, Instagram, etc.) via the self-hosted Postiz public API; listing integrations, uploading media, and checking the schedule queue."
homepage: https://docs.postiz.com/public-api/introduction
metadata:
  {
    "marketingclaw":
      {
        "emoji": "📣",
        "requires": { "bins": ["curl", "jq"], "env": ["POSTIZ_API_KEY", "POSTIZ_BASE_URL"] },
        "primaryEnv": "POSTIZ_API_KEY",
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "jq",
              "bins": ["jq"],
              "label": "Install jq (brew)",
            },
          ],
      },
  }
---

# Postiz Skill

Postiz is a self-hosted social media scheduler: one API, 20+ connected networks (X, LinkedIn,
Facebook, Instagram, TikTok, Threads, YouTube, Mastodon, Bluesky, Discord, Slack, and more),
with durable scheduling on the Postiz side (posts still fire even if this agent is offline).

## Approval-first rule

**Never publish or schedule a real post without explicit human approval of the draft content
and target time first.** Workflow is always: draft the copy → show it to the user (or the
approving agent) → get an explicit go-ahead → only then call `--now` or `--date`. Use
`--dry-run` (see below) to preview the exact payload before sending anything. Treat "schedule
this" from a human as approval for that one post; never chain into scheduling additional posts
without asking again.

## Setup

1. Self-host Postiz (or use the Postiz cloud) and sign in.
2. Settings → Developers → Public API → generate an API key.
3. Set environment variables:
   ```bash
   export POSTIZ_BASE_URL="https://your-postiz-instance.example.com"   # self-hosted backend URL
   # or: export POSTIZ_BASE_URL="https://api.postiz.com"               # Postiz cloud
   export POSTIZ_API_KEY="your-api-key"
   ```
4. Connect the social accounts you want to post to inside the Postiz UI (Postiz owns the
   OAuth flow per network) — this skill only reads/writes through the already-connected
   integrations.

All requests go to `${POSTIZ_BASE_URL}/public/v1/...` with header `Authorization: $POSTIZ_API_KEY`
(no `Bearer` prefix).

## List connected socials

```bash
curl -s "${POSTIZ_BASE_URL%/}/public/v1/integrations" \
  -H "Authorization: ${POSTIZ_API_KEY}" | jq '.[] | {id, name, identifier}'
```

Copy the `id` values you need — every post targets one or more integration ids.

## Upload media

```bash
curl -s -X POST "${POSTIZ_BASE_URL%/}/public/v1/upload" \
  -H "Authorization: ${POSTIZ_API_KEY}" \
  -F "file=@/path/to/image.jpg" | jq
# => { "id": "upload-id", "path": "https://.../image.jpg", ... }
```

Keep the returned `id` — it goes in a post's `image` array.

## Draft, preview, and post via the helper script

`scripts/postiz-post.sh` builds the nested `POST /public/v1/posts` payload so you don't hand-roll
the JSON. It never sends anything with `--dry-run`.

```bash
# Preview only — always do this first and show the output for approval
{baseDir}/scripts/postiz-post.sh \
  --integration "INTEGRATION_ID" --content "Launching our new feature today 🚀" \
  --platform x --date "2026-07-15T14:00:00Z" --dry-run

# After approval, schedule for real
{baseDir}/scripts/postiz-post.sh \
  --integration "INTEGRATION_ID" --content "Launching our new feature today 🚀" \
  --platform x --date "2026-07-15T14:00:00Z"

# Cross-post identical copy to two networks, with an image, publish immediately
{baseDir}/scripts/postiz-post.sh \
  --integration "X_INTEGRATION_ID" --integration "LINKEDIN_INTEGRATION_ID" \
  --content "We just shipped v2." \
  --image "UPLOAD_ID" --now
```

Run `{baseDir}/scripts/postiz-post.sh --help` for the full flag reference (per-platform content,
tags, short links).

## Raw API (when the helper doesn't cover it)

```bash
# Schedule directly
curl -s -X POST "${POSTIZ_BASE_URL%/}/public/v1/posts" \
  -H "Authorization: ${POSTIZ_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "schedule",
    "date": "2026-07-15T14:00:00Z",
    "shortLink": false,
    "tags": [],
    "posts": [
      {
        "integration": { "id": "INTEGRATION_ID" },
        "value": [ { "content": "Post text here", "image": [] } ],
        "settings": { "__type": "x" }
      }
    ]
  }' | jq
```

`type` is `"now"` to publish immediately or `"schedule"` with a `date` (ISO-8601 UTC) to queue it.
`settings.__type` carries provider-specific fields (per-platform settings like X thread mode or
LinkedIn document posts) — check `GET /public/v1/integrations` for each integration's provider
before adding advanced settings, and when in doubt omit `settings` beyond `__type`.

## Check the schedule queue

`GET /public/v1/posts` requires `startDate` and `endDate` (ISO-8601 UTC) query params and
returns `{ "posts": [ ... ] }`; each post's scheduled time is `publishDate`.

```bash
# startDate & endDate are required — this pulls a one-week window
curl -s "${POSTIZ_BASE_URL%/}/public/v1/posts?startDate=2026-07-13T00:00:00Z&endDate=2026-07-20T00:00:00Z" \
  -H "Authorization: ${POSTIZ_API_KEY}" | jq '.posts[] | {id, state, integration: .integration.id, publishDate}'
```

## Notes

- Rate limit: 90 requests/hour (100 on the cloud) for the create-post endpoint — batch multiple
  posts into a single `POST /public/v1/posts` call (multiple entries in `posts[]`) instead of
  looping requests when scheduling several at once.
- **Verify on first use**: the exact `settings` sub-schema is provider-specific and evolves with
  Postiz releases. Confirm current field names against `https://docs.postiz.com/public-api` (or
  `GET /public/v1/integrations` response shape) before relying on advanced per-platform settings;
  the `type`/`date`/`posts[].integration.id`/`posts[].value[].content` fields above are stable.
- Never echo `$POSTIZ_API_KEY` in logs or commit it to the repo.
