---
name: daybrief
description: >-
  Morning work briefing — "what does my day look like, in one scan?" Gathers
  today's calendar and emails needing attention (via connected Google MCP tools
  when available), recent git activity and unfinished work across your local
  repos, your open tasks (TODO file / assigned GitHub issues), and a quick radar
  check on topics you track — all in parallel — and renders one compact,
  prioritized brief in chat, carrying over unfinished focus items from
  yesterday's saved brief. Every source is optional and
  degrades gracefully; strictly read-only (never sends email, never touches the
  calendar, never pushes). Use at the start of a workday or when the user asks
  "what's on today", "morning brief", "daybrief", "catch me up", "what should I
  focus on today". For deep research on one topic use pulse instead.
---

# daybrief — morning work briefing

`/daybrief [plain-language steering, e.g. "skip email", "just repos", "save it"]`

Answer one question in one scan: **what needs my attention today, in what
order?** Pull every source in parallel, compress hard, and lead with the
priorities — not the raw data. Target: the user reads it in under two minutes.

## Step 0 — Config

Look for `daybrief-config.md` in the current working directory. It defines:

```markdown
# daybrief config
## Repos            # absolute paths, or workspace roots to scan one level deep
- /home/hop/code
## Tasks            # optional: where your todos live (any/all of these)
- file: TODO.md     # a local markdown todo file (path relative to a repo or absolute)
- github: assigned  # issues assigned to you, via `gh` if authenticated
## Radar topics     # 2–4 topics to check for movement
- claude code
- postgres
## Preferences
- timezone: Asia/Ho_Chi_Minh
- email: on        # on / off
- calendar: on     # on / off
- save: off        # on = also write brief to out/daybrief/ (enables carry-over)
```

If missing, **don't block**: run with what's inferable (current repo, no radar
topics). Then, **after** delivering the brief, offer to create the config via a
short interview — ask (in one compact question set, prefilled with what you
learned this run): which repos/workspace roots to watch, 2–4 radar topics, where
todos live (file path / GitHub / none), email & calendar on/off, and whether to
save briefs (`save: on` enables carry-over). Confirm the timezone from the
system rather than asking. Write `daybrief-config.md` from the answers and
remind that it's gitignored. If the user declines, don't ask again on later
runs — just note "no config" in the footer. Honor one-off steering from the
arguments over the config.

## Step 1 — Gather all sources in parallel

Launch everything concurrently. Each source is independent and optional — if
its tools aren't connected or it errors, mark it "unavailable" in the brief
footer and move on. Never let one dead source stall the brief.

With five optional sources it's easy to silently drop one. Track this
checklist through the run — the brief isn't done until every box is ✓ or a
conscious ✗ with the reason shown in the footer (a skip is a decision, not an
oversight):

```
- [ ] calendar  - [ ] email  - [ ] repos  - [ ] tasks  - [ ] radar
- [ ] carry-over judged (if save: on)  - [ ] Focus = top 3, each with a "when"
```

### Calendar (Google Calendar MCP, if connected)

- Load the tools via ToolSearch (e.g. `+calendar list events`) only if
  available; otherwise skip.
- Today's events in the user's timezone: time, title, attendees count, video
  link. Flag: the next event and minutes until it, overlaps, meetings with no
  agenda/description (prep risk), and the largest free block (deep-work slot).

### Email (Gmail MCP, if connected)

- Load via ToolSearch (e.g. `+gmail search threads`) only if available.
- Search unread + recent important (last ~48h). Bucket into: **needs reply**
  (direct questions/requests to the user), **FYI worth knowing**, and count the
  rest as noise (report the number only). Quote nothing sensitive at length —
  one line per thread, sender + ask.

### Repos (local git — always available)

- For each configured repo/workspace root (`Bash`, read-only commands only):
  commits since yesterday morning (`git log --since`), dirty working trees
  (`git status --short`), unpushed branches (`git log @{u}..` where an upstream
  exists), and — if `gh` is authenticated — open PRs awaiting the user's review
  or with fresh comments.
- Surface **unfinished work first**: dirty trees and unpushed commits are
  today's loose ends.

### Tasks (local file and/or GitHub — if configured)

- `file:` entries — read the todo file(s) and pull **open** items only (unchecked
  boxes / non-struck lines), top ~5 by position. Read-only; never reorder or
  check anything off.
- `github: assigned` — if `gh` is authenticated: `gh issue list --assignee @me
  --state open` across the configured repos (plus `gh search issues` for the rest),
  top ~5 by recency. Skip silently if `gh` is missing/unauthenticated.
- These feed the Focus ranking (Step 2) — an explicit task list beats inference
  from git activity.

### Radar (keyless web — if topics configured)

- One Explore sub-agent for all topics together: HN Algolia last-24h search per
  topic + one web search pass. Return only items with real traction (points/
  comments) — **max 2–3 items total across all topics**, each one line + link.
  This is a glance, not a pulse; suggest `/pulse <topic>` if something is hot.

## Step 2 — Synthesize: priorities first

**Carry-over (if `save: on`):** before ranking, read the most recent brief in
`out/daybrief/`. For each of its Focus items, judge from today's evidence whether it
happened — commits/pushes touching it, the PR merged, the meeting past — and
sort into **done** vs **carried over**. Carried-over items start near the top of
today's ranking (unfinished yesterday-priorities outrank new shiny things), and
the brief reports the follow-through score ("yesterday: 2/3 done"). When
judgment is uncertain, mark it "status unclear" — never claim something was done
without evidence. Skip silently if there is no previous brief.

From all sources, derive **Top 3 focus items** for today. Ranking instinct:

1. Items carried over from yesterday's Focus (unless overtaken by events)
2. Hard deadlines/meetings needing prep that is not done
3. Loose ends blocking others (unpushed work, PRs awaiting the user, unreplied
   direct asks) and explicit open tasks (from the Tasks source)
4. The most important deep-work task, matched to the largest free block

Everything else is detail below the fold.

## Step 3 — Render the brief (chat-first)

Compact, scannable, in chat — this is the product. Skeleton:

```markdown
# Daybrief — <weekday> <YYYY-MM-DD>

## Focus today                (yesterday: 2/3 done — omit note if no carry-over data)
1. <item — why it's #1, and when to do it (e.g. "in the 9–11 free block")>
2. <item (carried from <date>)>
3. ...

## Calendar        (omit section if empty/unavailable)
- 10:00–10:30 <event> — <flag if no agenda / prep needed>
- Free block: 13:00–16:00 → deep work
## Inbox           (needs-reply first; omit if unavailable)
- <sender>: <one-line ask> → reply today?
- FYI: <one-liners> · <N> other unread (noise)
## Repos
- <repo>: <n> uncommitted files · branch <x> 2 commits unpushed
- PR #<n> awaiting your review (<repo>)
## Tasks           (omit if not configured)
- <top open todos / assigned issues, one line each>
## Radar           (omit if no topics)
- <topic>: <headline> (<engagement>) [link]

Sources: calendar ✓ · email ✓ · repos ✓ · tasks ✓/— · radar ✓/— <note any unavailable>
```

**Pre-render check:** read only the brief's opening block and its closing
pre-Sources lines — together they must say what matters most and what to do
next. If they don't, reshape the brief; don't bolt a second summary on top.

If the user runs daybrief manually on consecutive days, suggest once — never
nag — scheduling it each morning with `save: on` (cron or /schedule).

Dates/times from real commands (`date`), never guessed. If config `save: on`
(or the user asks), also write `out/daybrief/<YYYY-MM-DD>.md` — no HTML for this
skill; a daybrief is ephemeral by design. Ensure `out/daybrief/` and
`daybrief-config.md` are gitignored (personal data).

## Guardrails

- **Read-only, always.** No sending, replying, labeling, archiving, RSVP-ing,
  committing, or pushing — even if asked mid-brief; finish the brief first,
  then treat any action as a separate, explicit request.
- **Degrade gracefully.** A missing source is one footer note, not a failure.
- **Compress hard.** One line per item; counts instead of lists for noise. If
  the brief doesn't fit on one screen, it's too long.
- **Privacy.** Email/calendar contents stay in chat and local files only;
  saved briefs are gitignored. Never include message bodies at length.
- **Fast.** All sources in parallel; if a source hangs, drop it and note it.
  The brief should land in a couple of minutes, not ten.
