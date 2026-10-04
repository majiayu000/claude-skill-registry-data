---
name: kelly-social
description: >-
  Social media command desk (Busabase App-in-Skill) for Kelly's Twitter/X,
  Facebook, and Instagram accounts (extensible to LinkedIn, YouTube, Threads,
  TikTok, Xiaohongshu), covering cross-platform monitoring and ECHO-based
  publishing. Use when the user invokes $kelly-social or /kelly-social, wants
  cross-platform account metrics and timelines, or needs a content calendar,
  draft review, engagement inbox, crisis playbook, share-of-voice, or
  pre-publish quality gate.
metadata:
  category: marketing
  tags:
    - risk:gated-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-social
    resources:
      - accounts
      - posts
      - sync-log
      - calendar
      - drafts
      - shorts
      - engagement
      - settings
    risk: gated-write

---

# Kelly Social

## Overview

Kelly Social is a Busabase Cloud App-in-Skill. Its canonical product surface
is the AirApp in Busabase, not a separate local-data product. The same Hono
source supports an explicitly requested local preview with OAuth connection
bootstrap. Use this skill as Kelly's social media command desk. It does two
jobs on the **ECHO** discipline — **E**xplore, **C**raft, **H**ost,
**O**bserve:

- **Monitor** (Observe): aggregate her Twitter/X, Facebook, and Instagram
  accounts (and later LinkedIn, YouTube, Threads, TikTok, Xiaohongshu) into
  one dashboard — per-platform KPI cards, a unified cross-platform timeline,
  account detail pages with follower trends, per-post engagement metrics, and
  share-of-voice vs competitors.
- **Publish** (Explore / Craft / Host): a review-and-approval workflow where
  the **agent drafts → the human approves → the skill publishes**. A content
  calendar, a post composer / draft queue, a short-video scripter, and an
  engagement (mentions/comments) reply inbox — all gated by a five-state
  review model and a pre-publish quality gate.

Collection is agent-driven, not API-first: most of these platforms have
hostile or expensive APIs, so the agent gathers the data through the method
configured per account and normalizes it into Busabase via
`scripts/ingest_snapshot.mjs`. **Real publishing and replying is skill-executed
out of band, only after a human approves** — the app records intent, it does
not post. Neither the AirApp nor any script in this skill calls a platform
API to publish, like, follow, or reply; that action happens separately,
performed by the agent (or a future dedicated publishing connector) once a
draft or reply is `approved`.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, update Busabase directly and give the user the clickable AirApp
URL. Start localhost only when local preview/debugging is explicitly
requested; it uses the same Busabase resources and never offers another data
provider. Use chat-only mode only when the user says "纯聊天", "chat only",
"不要打开 UI", or similar.

This skill is an implementation of the **App-in-Skill** pattern — a
Codex/agent skill paired with a small companion UI for review and approval.
See the spec paper:
<https://mr-kelly.github.io/research/app-in-skill-specification-for-pairing-agent-skills-with-a-local-companion-ui.pdf>.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-social-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and
product contracts, stop before the unavailable Busabase operation, and report
the exact missing dependency. Do not invent a second data backend.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Social overview"></td>
    <td width="50%"><img src="assets/screenshots/timeline.webp" alt="Kelly Social unified timeline"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Cross-platform KPI cards for X, Instagram, and Facebook with follower trends and top posts of the week.</td>
    <td><strong>Unified timeline</strong><br>Posts across all platforms in one stream with per-post likes, replies, reposts, and view counts.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/detail.webp" alt="Kelly social detail"></td>
    <td width="50%"><img src="assets/screenshots/accounts.webp" alt="Kelly social accounts"></td>
  </tr>
  <tr>
    <td><strong>Detail</strong><br>Single-post performance view with platform metrics, comments, reply drafts, and approval status.</td>
    <td><strong>Accounts</strong><br>Connected-account health board with platform status, audience totals, content cadence, and sync freshness.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/calendar.webp" alt="Kelly Social content calendar"></td>
    <td width="50%"><img src="assets/screenshots/compose.webp" alt="Kelly Social post composer"></td>
  </tr>
  <tr>
    <td><strong>Content calendar</strong><br>Scheduled posts across channels by theme pillar and date, with status and approvals.</td>
    <td><strong>Compose (publishing)</strong><br>Agent-drafted posts in a review queue with hooks, hashtags, and CTAs, behind a social-qa SHIP/FIX/BLOCK gate — one draft blocked for a banned claim.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/engagement.webp" alt="Kelly social engagement"></td>
  </tr>
  <tr>
    <td><strong>Engagement</strong><br>Mentions and comments inbox grouped by urgency, sentiment, owner, and reply-approval state.</td>
  </tr>
</table>

## Boundary

- The skill (agent side) may read the user's own social accounts and their
  public metrics, parse analytics exports the user downloaded, call an
  official API when the user configured one, normalize the data, validate
  schemas, draft posts/short-video scripts/replies for human review, and
  write to Busabase through `scripts/ingest_snapshot.mjs` (monitoring
  ingest) and the AirApp's compose/approval writes.
- The AirApp reads and writes Busabase records only. It must never initiate
  platform requests, post, like, follow, delete, or mutate any remote
  system. Publishing and replying happen **only after a human approves in
  the review queue**, and the real platform action is performed by the skill
  out of band — never by the app, and never automatically. `publish_post` /
  `send_reply` only write `status: "done"` (and, for a post, the intended
  `scheduled_for`) onto the record — a recorded approval + intent, not a
  network call.
- Collect only the user's own accounts plus the public metrics attached to
  their own posts. Never scrape other people's private data, DMs, or
  non-public profiles.
- Respect login sessions the user owns: reuse an existing authenticated
  browser session; never ask for, capture, or store passwords, cookies, or
  session tokens anywhere (not in Busabase records, ingest payloads, or
  chat).
- Respect platform terms of service: prefer official analytics exports and
  user-owned sessions, throttle politely (small page counts, pauses between
  navigations, stop on rate-limit signals), and never bypass anti-bot walls.
- The skill must never create fake engagement: no automated likes, follows,
  comments, reposts, or engagement pods. Normal Kelly Social operation is
  read-mostly aggregation plus human-gated drafting.
- Treat all account data as personal. Never commit Busabase credentials or
  real account tokens.

## Busabase Resources

Eight Bases under one application Folder (`kelly-social`), declared in
`content/kelly-social-app/app/js/config.js` and the generated template sidecars under `content/`:

- `accounts`: connected social accounts — platform, handle, collection
  method, rolled-up metrics (JSON), follower series (JSON), traffic sources
  (JSON), and sync freshness. A non-`ok` `status` (with `notes` explaining
  why) is the only source of monitoring warnings — there is no separate
  warnings store.
- `posts`: collected posts across every connected account, with per-post
  engagement metrics (JSON) and a stored `engagement-rate`.
- `sync-log`: append-only history of collection runs per account, written
  only by `scripts/ingest_snapshot.mjs`.
- `calendar`: the content calendar — scheduled posts across channels by
  theme pillar and date, optionally linked to a `drafts` row.
- `drafts`: the post composer / draft review queue. The social-qa quality
  gate is **recomputed live** from each draft's own copy on every read (see
  `content/kelly-social-app/app/js/social-model.js`'s `evaluateGate()`) — it is never trusted as
  stale stored state, and a `BLOCK` verdict always forces the effective
  `status` to `blocked` regardless of what is stored.
- `shorts`: short-video scripts (Reels / Shorts / TikTok / Douyin) with a
  shot list (JSON), same five-state review model.
- `engagement`: incoming mentions/comments with an agent-drafted reply,
  approval-gated.
- `settings`: one row per `kind` — `kelly-social-crisis` (the crisis
  playbook) and `kelly-social-share-of-voice`.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/social-schema.md` for
exact field shapes. Monitoring rollups (`metrics`), the derived `warnings`
list, and every draft's quality gate are computed client-side on every read
— never stored.

## First Run And Onboarding

On invocation, check whether the `accounts` Base has any rows. If it is
empty, guide setup before collecting real accounts: ask, turn by turn, which
platforms the user is on, the handle and display name per account, and the
collection method per account — `browser_agent` (agent browses with the
user's own logged-in session), `manual_export` (user downloads the
platform's analytics export and tells the skill where it is), or `api` (user
has an official API token; ask only for the env var name that holds it). Ask
for non-secret details only. Never ask the user to paste secret values into
chat; secrets belong only in the trusted ingest process's own environment.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-social-app dev` only when local preview/debugging is explicitly
requested.

Required app views — monitoring (Observe):

- `#/overview`: social command desk. Per-platform KPI cards (followers, following, posts, impressions, engagement rate, profile visits) with 7d/28d deltas and platform badges, a cross-platform followers trend summary with inline SVG sparklines, top posts this week, **share-of-voice vs competitors**, and collection freshness per account (last sync + method).
- `#/timeline`: unified reverse-chronological timeline across all platforms. Each row shows platform badge, account, timestamp, text preview, media indicator, and per-post metrics (likes, replies/comments, reposts/shares, views/impressions). Platform badge chips filter the list.
- `#/timeline/<post_id>`: Post Detail. Full text, metrics breakdown, engagement rate, permalink, and agent notes.
- `#/accounts`: account inventory. Handle, platform, display name, followers, growth deltas, engagement rate, last sync, and collection method.
- `#/accounts/<account_id>`: Account Detail. Profile summary, follower trend rendered as an inline SVG sparkline (no chart library), top posts, traffic sources when available, and sync history with warnings.
- `#/settings`: sanitized setup summary. Account handles, platforms, collection methods, data provider, and onboarding state. Never expose secret values.

Required app views — publishing desk (Explore / Craft / Host):

- `#/calendar`: content calendar. Scheduled posts across channels with theme pillars, dates, publish status, and links to the linked draft when one exists.
- `#/compose`: post composer / draft approval queue. Agent-drafted posts (hook + body + hashtags + CTA + target channels) as review items, each carrying its live social-qa gate result. Human edits/approves/blocks. Workflow chips filter by the five review states (`needs_review | changes_requested | approved | done | blocked`). An approved, gate-passing draft exposes a **Publish** action.
- `#/shorts`: short-video scripter for Reels / Shorts / TikTok / Douyin. Shot lists (visual + voiceover + duration + on-screen text) plus caption and hashtags, reviewed on the same five-state model.
- `#/engagement`: engagement inbox. Incoming mentions/comments with agent-drafted replies (approval-gated). Approve to expose a **Send reply** action.
- `#/crisis`: crisis playbook. A small incident-response checklist (triage, spokesperson, pause-publishing, holding statement, review) plus a live incident-status toggle (calm / watch / active) and a publishing-pause switch.

The quality gate (⛩ `social-qa`, in `content/kelly-social-app/app/js/social-model.js`): every draft is scored 0–100 (SQS) across brand voice, disclosure, and banned claims, producing a **SHIP / FIX / BLOCK** verdict. A BLOCK forces the draft to `blocked` and disables approve/publish until it is revised.

A human verdict (`review_draft` / `review_short` / `review_engagement`)
writes the new `status` and `review-note` directly onto the record through
`busabase-sdk`. `publish_post` requires a prior `approved` status and a
non-`BLOCK` gate, then writes `status: "done"` plus `scheduled-for` — the
recorded intent, never a real publish. `send_reply` requires a prior
`approved` status, then writes `status: "done"`. `crisis_toggle` updates the
`kelly-social-crisis` settings row. From a standalone local preview the write
merges immediately (trusted operator); from the deployed AirApp it creates a
pending ChangeRequest for the trusted process to merge.

Demo mode:

- `?demo=1` opens a deterministic mock dashboard for documentation and screenshots.
- `?demo=overview`, `?demo=timeline`, `?demo=accounts`, `?demo=detail`, `?demo=calendar`, `?demo=compose`, `?demo=shorts`, `?demo=engagement`, and `?demo=crisis` select named mock scenes.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.
- Demo mode never reads or writes Busabase.

UI language: support English and Chinese chrome with `Auto` default. Keep handles, post text, and imported data in their original language.

## Collection Workflow

Read `references/social-schema.md` before editing the app, scripts, or an
ingest payload.

1. Detect mode. Default to App UI (AirApp-first).
2. If the `accounts` Base is empty, enter onboarding.
3. If the user asks to refresh data, propose a collection scope first: which accounts, date window, and method per account.
4. Collect per account according to its `collection` value:
   - `browser_agent`: use a browser automation skill available in the session (for example a Stagehand/Playwright `browser` skill) with the user's own logged-in session. Read the user's profile page and their own posts' public/analytics metrics. Throttle politely: few pages, pauses between navigations, stop and report on rate-limit or captcha signals. Never enter credentials, never store cookies.
   - `manual_export`: ask the user for the platform's analytics export (e.g. Meta Business Suite CSV, X analytics CSV, TikTok/YouTube studio export), parse it locally, and note the export date. Warn when an export is older than 7 days.
   - `api`: call the official API with the token from the configured env var, read-only scopes only.
5. Normalize the collected data into the payload shape documented in `references/social-schema.md`, write it to a temp file, then run `node scripts/ingest_snapshot.mjs <payload.json> --apply`. This is the single write path for monitoring data: it validates, merges by stable ids (`account_id`, `post_id`), appends per-account `sync-log` entries, and never touches the ECHO publishing-desk Bases (`calendar`/`drafts`/`shorts`/`engagement`/`settings`).
6. Give Kelly the AirApp URL (or local preview URL) to review the fresh dashboard.
7. Surface collection problems (stale exports, missing metrics, rate limits) by setting the affected account's `status` to `warning`/`error` with an explanatory `notes` string in the ingest payload's `warnings[]` — the app derives the visible warning from that, rather than guessing numbers.

Platform vocabulary normalization: map replies/comments onto `replies`, reposts/shares onto `reposts`, and views/impressions/plays onto `views`. Preserve provenance: `platform`, `provider_post_id`, `permalink`, and original handles. Deduplicate by stable ids (`post_id`, `account_id`) so repeated collections are idempotent.

## Safety Defaults

- Treat posting, liking, following, deleting, and any other remote mutation as out of scope; if the user asks, require explicit approval and a separate, clearly-scoped plan.
- Only collect the user's own accounts and public metrics; skip anything requiring someone else's login or private data.
- Never store passwords, cookies, tokens, or session material in Busabase, ingest payloads, or chat. `scripts/ingest_snapshot.mjs` reads secrets only from its own process environment (`BUSABASE_API_KEY` and any platform token env vars the agent uses out of band).
- Throttle politely and back off on rate-limit or anti-bot signals; a stale dashboard beats a banned account.
- Keep collected data minimal and use stable ids so repeated ingests are idempotent.
- If numbers between a platform's UI and an export disagree, do not invent corrections. Mark the account `warning` and explain the mismatch in `notes`.
