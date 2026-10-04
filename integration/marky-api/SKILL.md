---
name: marky-api
description: >
  Reference for driving Marky (social media management) from an AI agent. Use this
  when you need to authenticate to the Marky API, find the base URL, look up the key
  endpoints (businesses, integrations, media, posts, generate, schedule, stats), or
  connect Marky's MCP server to Claude Code CLI, Cowork, or Codex. Read this
  first before calling the Marky API or using the plan-social-content or schedule-posts
  skills. Also triggers on "connect my agent to Marky", "is my Marky connection working".
---

# Marky API

Marky is an AI social media manager. This skill is the reference for talking to it from
an agent: how to authenticate, how to connect Marky's MCP server, and which tools to
reach for.

**The MCP is how agents drive Marky.** Connect it once (see the setup pointer below) and
your client gets a curated set of typed Marky tools natively — `list_businesses`,
`create_post`, `schedule_post`, `publish_post_now`, `create_media_upload`,
`submit_feedback`, ... — the live list your client shows after connecting is the source
of truth. When an MCP tool exists for an operation, **use the tool, not curl.**

The REST API shares the same auth and data and covers operations not yet exposed as MCP
tools (see "REST endpoints" below). Treat it as a stopgap, not a peer: if an agent
routinely needs REST for something, that is a gap in the MCP — report it with the
`submit_feedback` tool so Marky can add the missing tool, then use REST to finish the
job in the meantime.

Detail lives in `references/` next to this file — each section below says when to read
which. Load them as needed rather than all up front.

## Base URL and auth

```
Base URL:  https://api.mymarky.ai/api
Auth:      Authorization: Bearer mk_live_YOUR_KEY
```

Every request needs the Bearer header:

```bash
curl https://api.mymarky.ai/api/businesses \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

Error responses:

| Status | Meaning |
|--------|---------|
| `401` | Missing or invalid API key |
| `403` | Business does not belong to your org |
| `404` | Business or resource not found |
| `429` | Rate limit exceeded (check the `Retry-After` header) |

Rate limits: 100 requests per minute per org.

**Not connected yet?** Read `references/setup.md` — it covers connecting the MCP server
(`https://api.mymarky.ai/api/mcp`, streamable HTTP) to Claude Code, Cowork, Codex,
Cursor, or any other client. Interactive clients sign in with **OAuth** (browser consent,
no key to paste — Cowork/claude.ai custom connectors use this automatically); automation
(CI, scripts, headless agents) uses an `mk_live_` key, which setup.md also covers
creating and persisting in `MARKY_API_KEY`. In a Claude Code plugin install the MCP
server is already bundled and reads the `MARKY_API_KEY` env var; for OAuth instead,
register the server manually per setup.md.

## The shape: everything is scoped to a business

Almost every resource lives **under a business** (your workspace). The path always starts
with the business id:

```
/api/businesses/{business_id}/posts
/api/businesses/{business_id}/topics
/api/businesses/{business_id}/library
/api/businesses/{business_id}/integrations
...
```

So the first call you make is always `GET /businesses` to get your `business_id`, then you
slot that id into every path after it. Only a few org-level resources (`/keys`,
`/webhooks`, `/feedback`) sit outside a business.

### Pagination (list endpoints)

List endpoints (`GET /businesses`, `/posts`, `/topics`, ...) return **at most 20 items per
page** in a cursor-paginated envelope:

```json
{ "items": [ ... ], "next": "..." }
```

If `next` is non-null, there are more results. Pass `?limit=100` to get a bigger page, or
page through by passing it back as `?cursor=NEXT` until `next` is `null`. **This matters on the
very first call:** if your org has more than 20 workspaces, the one you want may not be on
page 1 of `GET /businesses` — use `?limit=100` (or page with the cursor) so you do not miss
it. Same for finding a specific post or topic in a long history.

## Opening the app for the user

When the user asks to *see* something (their scheduled posts, the calendar, the library),
open the right page in the Marky app instead of describing it. Workspace pages live under
`https://app.mymarky.ai/ws/{workspace}/...` — `{workspace}` accepts **the `business_id`
UUID** (the human-readable slug also works, but the API does not expose it, so use the id
you already have).

| To show the user... | Open |
| :--- | :--- |
| A single post | `https://app.mymarky.ai/post/{post_id}` |
| Scheduled posts | `https://app.mymarky.ai/ws/{business_id}/social-posts?tab=scheduled` |
| Drafts to review | `https://app.mymarky.ai/ws/{business_id}/social-posts/review` |
| The posting calendar | `https://app.mymarky.ai/ws/{business_id}/post-calendar` |
| The media/docs library | `https://app.mymarky.ai/ws/{business_id}/library` |
| Connect / reconnect social accounts | `https://app.mymarky.ai/ws/{business_id}/business/profile` |
| Business settings | `https://app.mymarky.ai/ws/{business_id}/business/settings` |

When an integration's `status` is not `valid` (or a platform the user wants is missing),
send them to the **business profile** page — that's where social accounts are connected
and reconnected. It is NOT under business settings.

Do not invent page paths (there is no `/calendar` at the root, for example) — anything not
in this table, link `https://app.mymarky.ai` and let the user navigate.

## Marky wants your feedback — please send it

Marky is built to be driven by AI agents, and the team relies on agents like you to report
how it goes. There is a first-class channel for exactly this: the **`submit_feedback` MCP
tool**. **Treat sending feedback as part of the job, not an afterthought.** It is low-cost
(one tool call), it never blocks your work, and it is how Marky finds and fixes the rough
edges agents hit.

`submit_feedback` (org-level, not under a business; over REST it is `POST /feedback`).
Typed fields:

| Field | Required | Value |
| :--- | :--- | :--- |
| `type` | yes | `"bug"`, `"feature"`, or `"feedback"` |
| `message` | yes | Plain-language report, 1–5000 chars. |
| `context` | no | Object: `page_url`, `error_details`, `environment`, plus any extra keys you want (the object is stored as-is). |

Returns `201` with `{ "id": "...", "status": "received" }`. Tip: send an `Idempotency-Key`
header so a retry never files a duplicate.

**When to send feedback — three triggers:**

1. **IMMEDIATELY on any bug or friction** — a call failed, an error was confusing, a tool
   did something unexpected, a workflow was harder than it should be. File it as
   `type: "bug"` with exactly what broke (the call you made and the error you got), the
   moment it happens, before you work around it.
2. **AFTER running a skill / completing a workflow** — a quick note on how it went, as
   `type: "feedback"`. Did it work end to end? What was confusing or slower than expected?
3. **PERIODICALLY on use cases + satisfaction** — every so often, tell the team what you
   are using Marky for and how satisfied you are. `type: "feature"` for something missing,
   `type: "feedback"` for a satisfaction check-in.

Example `submit_feedback` call (the shape is the same for all three — vary `type` and
`message`):

```json
{
  "type": "bug",
  "message": "schedule_post returned 422 \"scheduled_publish_time must be in the future\" even though I sent a UTC time 2 hours ahead. Had to retry with an explicit Z suffix.",
  "context": {
    "environment": "claude-code",
    "error_details": "schedule_post -> 422 validation_error"
  }
}
```

Non-MCP scripts can send the same body over REST as `POST /feedback` with the
`mk_live_...` key. Other Marky skills point back here — this is the one place that
documents how to give feedback.

## Session start + where state lives

Skills are amnesiac — every session starts fresh — but you have two durable stores. Use this **one rule** for anything worth remembering:

**Marky-first, memory-fallback.** If the thing has a home in the Marky business profile — a brand color, font, tone/Profile, caption rule, imagery preference, logo, CTA, tagline — persist it **there** with `update_business` (read-merge-write, confirm the wording). The product itself reads those fields, so it never goes stale inside one agent's head. If there is **no** field in Marky for it — an agent-only preference like a preferred TTS voice, "no code in my videos", the user's default business, or "stop asking me for feedback" — save it as a **local memory** instead. Everything else runs on sensible defaults; you only remember a *deviation* from a default. (There is no `user.toml` — this rule replaced it.)

At session start the plugin's SessionStart hook injects a `brand-cache.md` snapshot to orient you; before your first authored content, refresh with one `get_business` call. Your **default business** and any **muted prompts** live in memory — read them from there. If you don't know which business yet, ask once and remember the choice; a stale id 404s on first use, so re-pick and re-remember.

### Feedback — event-driven
Submit feedback the moment you hit a real bug or friction (the three triggers in "Marky wants your feedback" above) — this is always on. Separately, at a natural pause roughly every couple of weeks, you *may* ask once with **AskUserQuestion** whether they want to share quick feedback: **Yes** → collect it and `POST /api/feedback` (or the `submit_feedback` tool); **No** → skip; **Don't ask again** → save a memory and never ask again. No stored timers — if a memory says the user muted it, don't ask.

### Contribution nudge — opportunistic
If the user has locally built or substantially edited a genuinely generic, reusable skill, you *may* offer once (**AskUserQuestion**) to contribute it to the community repo `Marky-Team/marky-skills-community` — read `references/contribution-nudge.md` and follow it. Never nudge on a skill carrying private prompts or client data, and never open a PR without an explicit yes **and** the user reviewing the sanitized diff. "Don't ask again" → save a memory.

### Library file storage
Library files (notes, briefs, knowledge-base docs) live in the user's Marky account via the `manage-library` skill — the default. If a user explicitly wants them on local disk instead, remember that as a memory and read/write under `~/.marky/fs/<business_id>/` (`/knowledge-base/services.md` → `~/.marky/fs/<business_id>/knowledge-base/services.md`).

### Low queue
By default, if the posting queue will run dry within ~3 days, mention it once and offer to top up — in the Claude Code plugin a SessionStart hook does this automatically (`GET /queue/summary`, cached 6h). If the user says "stop reminding me about my queue" (or gives a different day threshold), save a memory and honor it.

**How hooks find the business (they can't read your memory).** SessionStart hooks are plain shell scripts, outside the model loop — they have no access to your memory. The one durable fact they need, the active business id, lives in `~/.marky/brand-cache.md` (its first line, `business_id: <id>`), which the brand-cache hook rewrites on every `get_business`/`update_business`. So there are two views of the same fact: **you** read the default business from memory; **hooks** read it from `brand-cache.md`. That file — not a `user.toml` — is the machine-readable source for anything a hook must persist across sessions.
## The MCP tools (the curated set)

The MCP does **not** mirror the whole REST API. It exposes a **curated set of typed
tools** — the high-value content actions an autonomous agent actually needs. Everything
else stays **REST-only** (still fully usable over REST, just not as an MCP tool). This is a
deliberate allowlist on the server, so an agent holding a content key can't nuke a
workspace, leak keys, or get lost in low-value per-item CRUD.

The curated tools below are the stable core. Rather than trust this list to stay perfectly
in sync, **read the live tool list your MCP client shows after connecting** — that is the
source of truth. If you need an operation that is not exposed as a tool, tell Marky with
`submit_feedback` (missing tools get added), then call it over REST as a stopgap (see
"REST endpoints" below).

| Tool | What it does |
| :--- | :--- |
| `list_businesses` | List your workspaces. Grab the `id` you want as `business_id`. |
| `create_business` | Create a new workspace. |
| `update_business` | Set the brand profile (tone, palettes, fonts, logo) and merge-patch `platform_writing_instructions`. |
| `get_business` | Read one business's full brand profile by id, incl. `platform_writing_instructions`. |
| `list_posts` | List a business's posts (filter by status, incl. the review verdicts `LIKED`/`REJECTED`). |
| `create_post` | Create one post yourself (caption + platforms + media + per-platform `platform_overrides` — see `references/platform-rules.md`). |
| `update_post` | Edit a post (caption, `restrict_publish_to`, media) or move it through the TEAM review workflow: `status: NEW` tells the user's team it's ready for review (shows on the app's review page); `LIKED`/`REJECTED` record their verdict. Marky never gates publishing on these. Only valid between the three review states. |
| `list_post_comments` | Read the team's review comments on a post (the same thread the app's review page shows). |
| `create_post_comment` | Leave a review comment on a post. |
| `resolve_post_comment` | Mark a review comment resolved (or reopen it). |
| `get_post` | Read one post by id, including its `publish_results`. |
| `schedule_post` | Schedule a post for a future time. |
| `queue_post` | Drop a post into the next open posting-schedule slot. |
| `publish_post_now` | Publish a post immediately. |
| `get_post_analytics` | Engagement stats for one Marky post. |
| `get_posting_schedule` | Read the weekly recurring time slots. |
| `update_posting_schedule` | Set the weekly recurring time slots. |
| `list_topics` | List content topics. |
| `create_topic` | Add a content topic. |
| `list_categories` | List content categories. |
| `list_connected_social_accounts` | List connected social accounts (read `platform` + `status`). |
| `get_integration_stats` | Account-level audience stats (followers, growth) for one connected account. |
| `list_integration_posts` | Posts published on one platform with engagement — includes posts made outside Marky. |
| `get_external_post_stats` | Engagement for one post that was published outside Marky. |
| `search_media_library` | Keyword-search the business's media library (reuse the user's own photos/videos). |
| `list_queued_posts` | Which posts sit in which upcoming schedule slot (the lineup, not just the recurring slots). Paginated (items under `items`, follow the `next` cursor). |
| `get_queue_summary` | How full the daily queue is + when it runs dry: `queued_count`, `next_estimated_publish_time`, `last_estimated_publish_time`. One cheap call before deciding to top up — no need to page the full queue. |
| `list_google_reviews` | Read your Google Business reviews. |
| `create_media_upload` | THE upload path when the file is on a disk you can shell to (a code-exec sandbox, the user's machine) and has no public URL. Returns a 1-hour `upload_url` + a ready-to-run curl command; PUT the raw bytes there and the response is the created media asset (its `original_url` feeds `media_urls`/`logo_url`). Re-PUTting the same bytes safely returns the same asset. On hosted Claude clients, run the curl in the code-execution sandbox (the user may need to allow `api.mymarky.ai` under Settings → Capabilities → Code execution → Additional allowed domains). |
| `submit_feedback` | Send a bug report, feature request, or general feedback to the Marky team. |
| `generate_draft_posts` | **DEPRECATED — prefer `create_post`.** Have Marky generate on-brand draft posts from a brief / website / idea. Returns a job id; poll `get_job_status` until `completed`. Use this ONLY when the user explicitly asks Marky to write/design the content for them — it spends credits and counts against the org's monthly post quota. By default, author your own caption and push it in with `create_post`. |
| `get_job_status` | Poll a `generate_draft_posts` job until `completed` / `failed`. |

**Deliberately NOT tools** — these stay off the MCP on purpose, so do not wait for them:
the design/template flow, and the destructive/config ops (API-key create/list/revoke,
webhooks, `delete_business`, `delete_post`). (Marky-side generation IS a tool now —
`generate_draft_posts` above — but it's **deprecated**: author your own posts with
`create_post` and only reach for generation when the user explicitly asks Marky to generate.)

**Not yet MCP tools (REST stopgap)** — remaining gaps Marky is closing. If one matters
to your workflow, say so via `submit_feedback`; meanwhile reach them over REST:
multipart media upload (same 50 MB cap as the base64 tool, but no base64 inflation) and
per-item topic / category / library / file / folder GET-DELETE-UPDATE.

## REST endpoints

The calls you will make most, all relative to the base URL and nested under
`/businesses/{business_id}`:

- **Posts** — `POST /posts` (create: `caption` required, plus `restrict_publish_to`,
  `media_urls`, `status`, `link` (clickable on Facebook / Google Business /
  Pinterest — set it whenever the post has a destination), and `metadata` — see
  "Tag every post" below),
  `GET /posts?status=NEW` (list, filter by status),
  `GET|PATCH|DELETE /posts/{post_id}` (one post — GET includes `publish_results`),
  `POST /posts/{post_id}/schedule` (`scheduled_publish_time`, ISO 8601, future),
  `POST /posts/{post_id}/queue` (next open schedule slot),
  `POST /posts/{post_id}/publish` (now).
- **Generate** — `POST /posts/generate` (Marky writes on-brand drafts; returns a
  `job_id`), then poll `GET /jobs/{job_id}` until `completed` and list the new
  `status=NEW` drafts.
- **Media** — `POST /media` (multipart, field `file`, ≤50 MB; returns `original_url` to
  pass in `media_urls`).
- **Integrations** — `GET /integrations` (connected accounts; read `platform` + `status`,
  target only `valid` ones). Accounts are connected in the dashboard, never via API.
- **Stats** — `GET /posts/{post_id}/stats`, plus per-integration account/post stats.
- **Businesses** — `GET /businesses` (org-level list), `GET|PATCH /businesses/{id}`
  (the PATCH is also how you set the brand profile — flat fields like `tone`,
  `caption_writing_rules`, `palettes`; there is no separate brand endpoint).
- **Topics & schedule** — `GET|POST /topics`, `GET|PUT /posting-schedule`,
  `GET /queue` (paginated), `GET /queue/summary` (count + next/last estimated
  publish times — the cheap "when does my queue run dry?" call).

**Everything else** — library / folders / files, reviews, templates, designs, categories,
webhooks, API keys, full request/response shapes and field lists for the calls above —
is in `references/rest-endpoints.md`. Read it when you need a resource not listed here
or the exact fields of one that is.

## Brand voice and memory

Marky agents get better with use because four stores carry what was learned. The duties
are summarized here; `references/brand-memory.md` has the full protocol — file formats,
cache maintenance, examples, escalation rules. **Read it before your first
content-creation work of a session.**

### Write like the business — pull the brand profile before drafting

Whenever YOU are about to write social content yourself (captions, hooks, hashtags,
anything user-facing), first read the brand profile (`get_business` /
`GET /businesses/{id}`) and apply it: match `tone`, obey every line of
`caption_writing_rules`, append `caption_suffix`, respect `imagery_preferences`. Once per
session per business — don't draft from a generic voice and fix it later. A cached
snapshot (`~/.marky/brand-cache.md`) is injected by the plugin's SessionStart hook to
orient you, but it can be stale: before your first authored content of a session, make
one fresh `get_business` call. Cache format and maintenance rules are in the reference.

### Learn the user's style — persist critiques into the brand profile

When the user critiques generated content ("too many emojis", "stop saying
'game-changer'"), fix the content in front of you AND persist the lasting preference —
following the **Marky-first, memory-fallback** rule above. Most style critique has a home
in the brand profile (`tone`, `caption_writing_rules`, `imagery_preferences`) → write it
there with `update_business` (merge, don't clobber, confirm first). A lasting preference
with no brand-profile field (e.g. a preferred TTS voice, a format rule like "always
vertical") → save it as a local memory. One-off instructions are not lasting preferences.
Style critique never goes to `POST /feedback`.

### The feedback log — taste memory across sessions

`~/.marky/feedback-log.jsonl` records what the user actually approved, rejected, and
edited on review boards. Two duties for every creation skill: **append a line after
every board** (feedback verbatim + an `items` map), and **scan the last ~20 entries for
this business before you generate** — lean into what won, drop what got rejected. When
the same preference shows up ~3+ times, escalate it into the brand profile. Entry format
and escalation detail are in the reference.

### Performance learnings — what the NUMBERS taught us

`performance-learnings.md` (a per-business file: the Marky library file
`/performance-learnings.md` by default, or `~/.marky/fs/<business_id>/performance-learnings.md`
if the user opted into local library storage)
holds dated, data-backed lessons from real engagement — what the AUDIENCE rewarded, as
opposed to what the user chose. **Read it before drafting any batch** (it outranks
generic best practices — it was measured on this audience). **Offer to append** when a
performance review shows a real pattern — show the exact lines, write only on a yes.
User-taste statements go to the brand profile, not here. Format in the reference.

## Tag every post you create — `metadata`

When YOU create a post, always set `metadata` with the dimensions that describe it —
this is how future performance reviews learn what works instead of eyeballing. Posts
take up to 50 string key/value pairs (key <=40 chars, value <=500 chars), returned
verbatim on every read; Marky never interprets them. Use the shared vocabulary so cuts
line up across posts:

| Key | Values (extend as needed) |
| :--- | :--- |
| `media_type` | `text` \| `photo` \| `graphic` (designed brand card) \| `diagram` (flows/charts/steps) \| `carousel` \| `animated-video` \| `talking-head` \| `screen-demo` |
| `format` | `data-take` \| `how-to` \| `hot-take` \| `product-demo` \| `customer-outcome` \| `build-in-public` |
| `hook` | `number` \| `question` \| `bold-claim` \| `story-open` |
| `topic` | freeform slug, e.g. `automate-with-ai`, `social-tips` |
| `created_by` | the skill that made it, e.g. `create-post-video`, `plan-social-content` |

Add any keys of your own — Marky stores them verbatim. When reviewing performance
(`review-performance`), pull posts + stats and group by these keys: that's the whole
point of tagging.

## Platform name reference

`restrict_publish_to` is **case-insensitive**, so `linkedin` and `linkedIn` both work. The
integration `platform` field returns these canonical strings:

| Platform | String |
| :--- | :--- |
| Facebook | `facebook` |
| Instagram | `instagram` |
| Instagram Story | `instagramStory` |
| LinkedIn | `linkedIn` |
| TikTok | `tiktok` |

These five are the common targets. The `restrict_publish_to` enum also accepts `twitter`,
`linkedInProfile`, `pinterest`, `googleBusiness`, and `youtube` — but only target a platform
that shows up as a `valid` integration on the business.

Media rules of thumb:
- **Video** posts can target all platforms.
- **Image** posts target all except TikTok.
- **Text-only** posts target only `facebook` and `linkedIn` (Instagram, TikTok, and
  Stories all require media).

Always read `GET /businesses/{id}/integrations` first and only target platforms whose
`status` is `valid`.

## Before you start

- **Connect your social accounts in the dashboard first.** This is a one-time step at
  [app.mymarky.ai](https://app.mymarky.ai). The API sees connected accounts but cannot add
  new ones.
- Find your `business_id` with `GET /businesses` (or from the dashboard URL —
  workspace pages are `app.mymarky.ai/ws/{workspace}/...`, and a UUID in that slot is
  the business_id).
- Posts you create via the API show up in your normal Marky queue — review them at
  `app.mymarky.ai/ws/{business_id}/social-posts?tab=scheduled` (see "Opening the app
  for the user" above).
