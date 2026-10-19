---
name: gwaihir
description: Use when the user runs /gwaihir [channel] [hours]. Gathers Outlook mail and Microsoft Teams messages into one read-only "what needs me?" brief — the communications analog of /palantír. Surfaces the few items worth a look (mail) and the threads that want a reply (Teams); never acts. Renders whichever source answers and footer-notes a silent one (Teams stays dormant until tenant consent). Actions stay with /triage and /vor.
purpose: Gathers Outlook mail and Teams messages into one read-only brief of what needs attention.
user_invocable: true
stage: intake
composes: triage:companion, vor:companion
---

# Gwaihir — the Windlord's Brief

Gwaihir bears word in from afar. It gathers what arrived in Outlook mail and
Microsoft Teams, lays the few items that need a human eye before you in one
view, and points to `/triage` and `/vor` for the acting. **It reads and
surfaces. It never acts.**

## Arguments

`/gwaihir [channel] [hours]` — order-independent, both optional.

- `mail` → mail channel only.
- `teams` → Teams channel only.
- A bare integer → the mail lookback window in hours (default `24`). Mirrors
  `/triage`. Ignored when scope is `teams` — Teams has no window; its poller
  reads the delta since its last cursor.
- No args → both channels, 24h mail window.

If the integer is non-numeric or absent, default to `24` without prompting.

Examples:

- `/gwaihir` — both channels, 24h mail window
- `/gwaihir mail 48` — mail only, 48h
- `/gwaihir teams` — Teams only
- `/gwaihir 6` — both channels, last 6h of mail

## Workflow

### 1. Mail  *(skip when scope is `teams`)*

Read through the **Microsoft 365 claude.ai connector**, exactly as `/triage`
does — the connector is read-only and drives the fetch.

Locate `mcp__claude_ai_Microsoft_365__outlook_email_search` (a deferred tool;
load its schema with ToolSearch first — `select:mcp__claude_ai_Microsoft_365__outlook_email_search`,
or search `outlook email` if the exact name differs). **If no Microsoft 365 mail
tool is present in the session**, the connector is not connected — set the mail
source unavailable with reason `connector not connected — enable it at
claude.ai → Settings → Connectors` and do nothing further for mail. Do **not**
fall back to `outlook-fetch.sh`.

Fetch inbox messages received within the last `hours`, unread only. Each message
carries at least `subject`, sender name/address, `receivedDateTime`; degrade
gracefully where a field is absent (a missing `importance` never trips the
high-importance rule).

Classify each message, keeping only **Worth a look**; the rest become a single
`routineMail` count. **Classification is `/triage` §2's — reference it, do not
restate it:**

- **User overrides** — `~/.claude/hooks/outlook-classify.sh "<from>" "<subject>"`
  prints `worth`, `routine`, or `default`. Honor `worth`/`routine` directly.
- **Residual `default`** — judge by the Worth-a-look heuristic named in
  `/triage` §2 (high importance; open/escalated monitoring alerts; bank/gov
  non-routine; a real human writing directly; explicit action-by-date). When in
  doubt, prefer routine.

The account is the default from `outlook_accounts.md` (legacy single-account
compat when the memory file is absent). Gwaihir does not expose account
selection.

### 2. Teams  *(skip when scope is `mail`)*

Run the poller and read its exit code first:

    ~/.claude/hooks/vor-teams-poll.sh

- `2` — dormant (no `sources.txt`, or no `vor-graph-token`). Set the Teams
  source unavailable with reason `dormant — tenant consent pending`.
- `3` — a tool (`jq`/`curl`) is missing. Set unavailable, reason
  `missing tool: <name>`.
- `4` — Graph denied or errored. Set unavailable, reason
  `consent for Chat.Read/ChannelMessage.Read.All not yet granted`.
- `0` — proceed. Stdout is a JSON array of normalized messages
  (`{id, sender, text, thread, timestamp, mentionsMe}`); an empty array means
  nothing new (no surfaced threads, `routineTeams = 0`).

Organize as `/vor` does: group by `thread`. Surface, in order, threads where
`mentionsMe` is true (`kind = mention`), then threads asking a direct question
(`kind = question`); collapse the rest into a `routineTeams` count. Drop pure
noise (joins, reactions, automated notices).

**Do not draft replies.** Name the threads that want one; the footer points to
`/vor` for the drafting. There is no send path here and you must not construct
one.

### 3. Render

One combined brief. A half that answered renders its section; a half set
unavailable is replaced by a footer note naming the gap. A half outside the
chosen scope is neither queried nor noted.

    Gwaihir — N mail · M threads need you
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📧 Mail — Worth a look (N)
      <YYYY-MM-DD HH:MM>  <sender, ≤24 chars>  <subject, ≤60 chars>
      ...
    💬 Teams — Need a reply (M)
      <thread, ≤24 chars>  <@you: | Q:> <text, ≤60 chars>
      ...
    · Routine: mail K · teams J
    ───────────────────────────────────
      for mail actions: /triage    for Teams drafts: /vor

- Header counts `N`/`M` are the surfaced totals only (worth-a-look /
  needs-reply). Drop a channel's clause from the header when that channel is
  unavailable or out of scope.
- A Teams row is prefixed `@you:` when `kind = mention`, `Q:` when
  `kind = question`.
- The Routine line is a single per-channel tally; omit a channel whose routine
  count is zero or that was unavailable. If both channels have zero routine,
  omit the line.
- Mail rows sorted newest-first; Teams threads ordered mention-first, then
  question.

**Footer notes** — one line per silent source, beneath the brief:

- `Mail: connector not connected — enable it at claude.ai → Settings → Connectors`
- `Teams: <reason>` — the reason string from step 2 (e.g. `dormant — tenant
  consent pending`).

**Both silent (or both empty), when both were in scope:** render only

    Gwaihir — nothing to look through.

with any source-gap footer notes beneath it, so the user knows *why* it is empty
(dormant vs. genuinely quiet).

## Read-only guarantee

Gwaihir issues only read-shaped calls: the connector's `outlook_email_search`,
the `vor-teams-poll.sh` GET poller, and the `outlook-classify.sh` lookup. It has
no mark-read, no move, no post, no draft-send, and no run-stamp. Never add one —
mutation is out of scope; the acting verbs live in `/triage` and `/vor`.

## Rules

- Read-only — orchestrates existing read primitives; never mutates mail, posts
  to Teams, or stamps a run.
- Never reveal a mail message's body — subject and sender suffice.
- Classification is `/triage` §2's single source of truth — reference it, never
  copy it here.
- No Teams drafting — name the threads that want a reply; `/vor` composes.
- Default Outlook account only — for another mailbox, run `/triage <account>`.
- Fetch each source once — one poll, one connector search, one brief.
