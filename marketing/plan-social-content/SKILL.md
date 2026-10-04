---
name: plan-social-content
description: >
  Plan, write, and schedule a week of on-brand social media content for your business
  through the Marky API. Use this when you want a full week of posts produced and queued
  with one conversation: it mines real material from your own notes and updates, drafts in
  your voice, shows you everything for approval, then schedules across every platform you
  have connected. Always gets your approval before anything is scheduled. Uses the
  marky-api and schedule-posts skills to talk to Marky. Also triggers on "plan my week", "fill my queue", "what should I post this week", "post for me every day". For one-off posts, see schedule-posts; for ideas only, see suggest-topics.
---

# Plan Social Content

Plan the next week of your social media as a repeatable batch. The goal is consistent,
on-brand posts that get your message in front of the right people, without you sitting down
to write every one from scratch.

This skill **plans and produces, then schedules only after you approve.** Posting to your
live accounts is brand-facing, so you review the whole batch and say go before a single
post is queued. That approval gate is the most important step. Never skip it.

**Read the `marky-api` skill first** for your `mk_live_` key, the base URL, and the
endpoints. Use the `schedule-posts` skill for the actual create/schedule calls.

**Marky wants your feedback.** If anything breaks or is confusing while you run this
skill — and again once you finish a week's plan — send Marky a quick note with the
`submit_feedback` MCP tool. See the **"Marky wants your feedback"** section in the
`marky-api` skill for when and how.

## Where your data lives

Keep a small folder somewhere on your machine (you choose where, e.g.
`~/marky-content/`). The recipe is in this skill; your data lives in the folder so it
builds up over time:

- `writing-style.md` — your voice profile: tone, words you like and avoid, do's and
  don'ts. Read it before drafting. Update it whenever an edit reveals a lasting preference.
- `calendar.md` — a human-readable view of the week's plan.
- `material.md` — running notes of post-worthy moments worth turning into content (a
  customer win, a lesson learned, a new offering, a behind-the-scenes detail).

If the folder is empty on the first run, that is fine. Start a `writing-style.md` by asking
the user a few questions about their brand voice, and create the rest as you go.

## Stages

### Stage 1 — Gather real material

Good posts are grounded in something real, not generic filler. Before drafting, collect a
handful of concrete things worth saying. Pull from whatever the user actually has:

- Their `material.md` notes (the richest source over time).
- Recent wins, launches, lessons, or behind-the-scenes moments they describe to you.
- Their website or a recent blog post (you can pass a `website_url` to Marky's generator to
  pull in page context).
- Their connected platforms' recent performance —
  `GET /businesses/{id}/integrations/{integration_id}/stats` and
  `GET /businesses/{id}/integrations/{integration_id}/posts` show what has landed before.

**Judgment gate:** not every real thing is postable. Skip anything that would worry
customers, expose private details, or name a person or customer without their consent. Keep
it grounded and safe.

### Stage 2 — Learn what is working (optional, once you have history)

If the business has posted through Marky for a few weeks, look at the engagement before
planning. Pull per-post stats (`get_post_analytics`) and account stats
(`get_integration_stats`, `list_integration_posts`), and notice
patterns: which topics, formats, and platforms get the most reach and engagement. Lean the
next week toward what works, but keep some variety so you keep learning. If there is no
history yet, skip this and come back to it later.

### Stage 3 — Plan the week

Design about 6 posts for the week.

- **Learn from past boards first.** Read the last ~20 entries for this business in
  `~/.marky/feedback-log.jsonl` (see "The feedback log" in the `marky-api` skill): lean
  into approved topics/formats, drop anything repeatedly rejected, honor the comments.
- **Learn from the numbers too.** Read the business's `performance-learnings.md` (see
  "Performance learnings" in the `marky-api` skill) and let its data-backed lessons
  steer topic, format, and voice — they are measured on this audience and outrank
  generic best practices.
- **Anchor every post to something real** from Stage 1. A post that sounds like a human who
  was actually there beats a generic one every time.
- **Keep variety** across topics and formats (a tip, a story, a result, a question, a
  behind-the-scenes look) so the feed does not feel repetitive.
- **Lead with the value to the reader,** not the feature or the jargon. Say what they get.
- **Cover the platforms you have connected.** Check
  `GET /businesses/{id}/integrations` and plan to reach each `valid` one.
- **Respect the brand profile and `writing-style.md` exactly.** Match the voice, and
  avoid anything on the brand's "don't" list.
- Write the week into `calendar.md` so it is easy to scan.

### Stage 4 — Ask for what only the user can give

Some posts need input only the user has: a photo, a screen recording, a short talking-head
clip, a specific number, a quote they want to use.

**Preferred: the capture studio** — a local browser page that records everything in one
sitting and saves files straight back to the agent (no Downloads-folder shuffle). It ships
at `${CLAUDE_PLUGIN_ROOT}/scripts/capture-studio.py` (cloned repo: `scripts/`); needs
`python3` — fall back to listing the asks in chat without it.

1. Write `tasks.json` to a temp dir: `{"title": "Clips for this week", "items": [{"id",
   "kind": "talking-head" | "screen" | "photo" | "screenshot", "title", "script"
   (teleprompter text for video kinds), "note"}, ...]}`.
2. Run `python3 .../capture-studio.py tasks.json` **in the background**; parse the
   `STUDIO_URL: http://127.0.0.1:PORT/` line.
3. AskUserQuestion with the URL (the blocking wait). The user records each item —
   talking-head gets a scrolling teleprompter of your script — and clicks Finish.
4. Read `captures.json` next to `tasks.json`: `captures` maps ids to files under
   `captures/`, plus per-item `notes` and `overall`. Upload each file via
   `POST /businesses/{id}/media` and attach to its post.

Numbers and quotes are still just questions — ask them in chat. If a post needs footage
the user cannot provide this week, swap it for one that needs nothing extra.

### Stage 5 — Produce the drafts

For each post:

- **Write the caption** in the brand's voice. Pull the business's brand profile first
  (`GET /businesses/{id}` — `tone`, `caption_writing_rules`, `caption_suffix`; see
  "Write like the business" in the `marky-api` skill) and layer `writing-style.md` on top.
- **Prepare media.** Reuse what the business already has before reaching for anything
  generic — `search_media_library` finds their own photos and videos by keyword. Upload new
  files with `create_media_upload` (PUT the bytes to the returned URL) or
  `upload_media_from_url` for media already online, and keep the returned URL.
- **Or design a diagram.** When a post announces, teaches, or compares something and no
  photo exists, a branded diagram image often beats stock. Use the `create-post-graphic` skill:
  it pulls the brand colors from the API, authors the diagram as HTML, renders a PNG, and
  uploads it.
- **Or let Marky write it.** For posts where the user just has a topic, use
  `POST /businesses/{id}/posts/generate` (brand voice, colors, and logo come from the
  business automatically), poll the job, and review the drafts.

#### Hooks — the first line earns everything else

The first line decides whether anyone reads the rest. Draft 2-3 candidate hooks per
post and pick the strongest. Named patterns that work, as a baseline palette:

1. **Contrarian** — "Most {industry} advice gets this backwards."
2. **Question** — a question the reader actually asks themselves.
3. **Story open** — drop into the middle of a real moment ("Tuesday, 6am, the oven died.").
4. **Stat** — one concrete number that surprises ("83% of our orders are regulars.").
5. **List preview** — "3 things we changed that doubled weekend traffic."
6. **Bold claim** — a strong statement you then earn in the body.
7. **Empathy** — name the reader's exact frustration in their words.
8. **Before/after** — the transformation in one line.
9. **Confession** — "We almost discontinued our best seller."

Anti-patterns to cut on sight: throat-clearing openers ("We wanted to share...",
"We're excited to announce..."), starting with the business name, a hashtag as the
first word, and generic-expert voice that could belong to any business in the
industry.

**Precedence:** these are a BASELINE. The user's brand profile
(`caption_writing_rules`, `tone`), their feedback log, and `performance-learnings.md`
always outrank this list — if their audience rewards plain announcements, or the user
has said they hate question hooks, follow them, not this palette. Tag the choice in
post `metadata` (`hook: question`) so `review-performance` can tell you which
patterns actually win for THIS audience.

Before presenting drafts, run every caption through the **humanize** skill's pattern check (score 90+; fix silently, don't show the math). The user's own caption_writing_rules still outrank it.

### Stage 6 — Approve, then schedule (hard gate)

1. Present the full batch to the user. **Preferred: the review board** (a local browser
   page — much faster than approving a wall of chat text). It ships with the plugin at
   `${CLAUDE_PLUGIN_ROOT}/scripts/review-board.py` (for a cloned repo: `scripts/` at the
   repo root). Needs `python3`; if that's missing or the server fails, fall back to
   presenting the batch in chat.

   1. Write `items.json` to a temp dir: `{"title": "This week's posts", "items": [{"id",
      "caption", "media_url", "meta": "Mon 9am - instagram, linkedIn"}, ...]}`.
   2. Run `python3 .../review-board.py items.json` **in the background**, and parse the
      `BOARD_URL: http://127.0.0.1:PORT/` line from its output.
   3. Use AskUserQuestion with the board URL so the user can open it. The board IS the
      chooser — AskUserQuestion is just the blocking wait; don't also ask per-post
      questions in it.
   4. When the user answers, read `feedback.json` next to `items.json`:
      `decisions` (approved/rejected per post id), `edits` (captions the user rewrote
      in place — use their version verbatim), `comments`, and `overall`. If there's no
      feedback file, treat their AskUserQuestion text as the feedback.
      **Learn from the edits and rules:**
      - Diff each edit against your draft — what they changed IS the preference
        (shortened it, cut the emoji, unhyped the verbs). Apply the pattern to the
        rest of the batch, not just the edited post.
      - Any comment phrased as a rule ("never ...", "always ...", "stop ...") is an
        explicit lasting preference: persist it to the brand profile
        (`caption_writing_rules` via `update_business`) NOW, with the user's wording —
        don't wait for it to recur. Confirm the field text, then write.
   
   5. **Persist it**: append the feedback to `~/.marky/feedback-log.jsonl` with
      `context: "weekly-posts"` — see "The feedback log" in the `marky-api` skill. This
      is how next week's batch starts smarter than this one.
2. **Stop and get explicit approval.** Do not schedule anything until the user says go
   (Submit on the board with at least one approved post counts). Rejected posts don't get
   scheduled; apply per-post comments as edits and re-show anything that changed.
   Apply their edits. If an edit reveals a lasting voice preference, write it into
   `writing-style.md` AND persist it to the business's brand profile (`tone` /
   `caption_writing_rules` via `PATCH /businesses/{id}` or `update_business`) so Marky's
   own generator learns it too — see "Learn the user's style" in the `marky-api` skill.
3. On approval, create each post WITH `metadata` tags (`media_type`, `format`, `hook`,
   `topic`, `created_by: "plan-social-content"` — see "Tag every post" in the marky-api
   skill); these power next month's what-worked review. Then schedule through Marky
   (see the `schedule-posts` skill). Spread the posts
   across the week — for example one per day at a consistent time. Use
   `POST /businesses/{id}/posts/{post_id}/schedule` with a future `scheduled_publish_time`,
   and maximize `restrict_publish_to` to every platform the media supports.
4. Update `calendar.md` with the scheduled times.

### Stage 7 — Confirm

After the scheduled times pass, check `GET /businesses/{id}/posts/{post_id}` and read `publish_results`. Every
platform entry should be `success`. If one is `failed`, tell the user why (often an account
that needs reconnecting in the dashboard) so they can fix it.

## Maximize reach

When you schedule, target every platform the media supports rather than just one:

- **Video** -> all connected platforms.
- **Image** -> all except TikTok.
- **Text-only** -> Facebook and LinkedIn (the others require media).

One caption rarely fits every platform. Read `references/platform-rules.md` (in the
`marky-api` skill) for the hard limits and per-platform style baseline, then tailor
with `platform_overrides` on every multi-platform post — X gets a compressed one-idea
version, LinkedIn moves hashtags to `first_comment`, Pinterest gets a keyword-rich
`title`. Read the business's `platform_writing_instructions` (on `get_business`)
first; the user's own platform preferences always win over the baseline.

## Cadence

Run this weekly. Most of the user's time goes into Stage 4 (gathering their photos/clips)
and Stage 6 (approving the batch). Revisit Stage 2 (learning from results) about once a
month, once enough posts have published to show a pattern. The approval gate stays manual
every time.
