---
name: triage
description: Use when the user runs /triage [hours] [account]. Pulls unread Outlook inbox mail from the last N hours (default 24) through the read-only Microsoft 365 claude.ai connector, separates the few items worth attention from routine noise, and renders a tight two-tier summary. Mark-read and move-to-folder run on the Graph write hooks (the connector cannot mutate mail). Multi-account aware via the `outlook_accounts.md` memory map.
purpose: Summarizes unread Outlook inbox mail from the last N hours into a two-tier brief.
user_invocable: true
stage: intake
---

# Triage

Cuts unread mail down to the few items that deserve a human eye. Everything else is collapsed into a tally.

## Arguments

- `hours` — optional integer, defaults to `24`. Window of `receivedDateTime` to fetch.
- `account` — optional friendly account name (e.g. `personal`, `work`). When omitted, the default account from `outlook_accounts.md` is used. When the memory has no entries, the bare `outlook` Bitwarden item is used (single-account compat).
- `--list-accounts` — special verb. When given (in any position), render the configured accounts from `outlook_accounts.md` and stop. No fetch, no classify, no offer. If the memory file is missing, render `(no accounts configured — single-account compat in effect)`.

## Workflow

### 1. Fetch unread mail

Mail is read through the **Microsoft 365 claude.ai connector**, not the Graph device-code hook. The connector authenticates itself against whichever Microsoft account was connected at claude.ai → Settings → Connectors for this session; there is no Bitwarden read token to resolve. The connector is **read-only** — it fetches here, but every mutation in step 4 still rides the Graph write hooks.

**Locate the connector's search tool.** It surfaces as `mcp__claude_ai_Microsoft_365__outlook_email_search` — a deferred tool, so load its schema first with ToolSearch (`select:mcp__claude_ai_Microsoft_365__outlook_email_search`, or search `outlook email` if the exact name differs on this account). If no Microsoft 365 mail tool is present in the session, the connector is not connected — tell the user to enable it at claude.ai → Settings → Connectors and stop. Do **not** fall back to `outlook-fetch.sh`.

**Resolve the account for state and writes only.** Read `outlook_accounts.md` from project memory — a table of `name → bitwarden item` entries with one marked default. The `account` arg (or the `default` entry) selects the classify/state namespace `<account>` and the Bitwarden item `<bw-item>` used **only** by the write offers in step 4; the connector — not this item — drives the fetch. With no memory file, use the legacy flat state path and the bare `outlook` item. The chosen account must be the same mailbox the session's connector is bound to: reads come from the connected mailbox, writes target `<bw-item>`, and if they differ the two point at different inboxes.

**Fetch.** Call `outlook_email_search` for inbox messages received within the last `<hours>` hours. Apply an unread filter if the tool exposes one; otherwise fetch the window and keep only unread using whatever read/unread field the tool returns. Each message should carry at least `subject`, sender name/address, and `receivedDateTime`; `id`, `importance`, `bodyPreview`, and `webLink` may or may not be present — the connector's field set is undocumented. Map what is present and degrade gracefully where a field is absent: a missing `importance` never trips the high-importance rule, a missing `webLink` drops the open-link offer, a missing Graph `id` disables the write offers (see step 4).

Fetch once. If the tool errors (not connected, scope denied, throttled), surface the message plainly and stop. Do not retry silently.

### 2. Classify each message

Two buckets only — **Worth a look** and **Routine**. Classify in two passes — user overrides first, then static rules.

**Pass 1 — user overrides.** Resolve the rules path: `~/.skadi/outlook/<account>/classify.json` when an account was resolved, else `~/.skadi/outlook/classify.json` (legacy). If the file exists, walk its rules. Schema:

```json
{
  "demote_to_routine": [{"from": "<addr>", "subject": "<substr>"}, ...],
  "promote_to_worth":  [{"from": "<addr>", "subject": "<substr>"}, ...]
}
```

`from` is required and matched case-insensitively (exact equality); `subject` is optional substring match (case-insensitive); when a rule has no `subject`, it matches any subject from that sender. Promote wins over demote when both match.

For each message:

- If a `promote_to_worth` rule matches, classify as **Worth a look** and skip pass 2.
- Else if a `demote_to_routine` rule matches, classify as **Routine** and skip pass 2.
- Else fall through to pass 2.

Ad-hoc verification of the verdict for a single message: `~/.claude/hooks/outlook-classify.sh "<from>" "<subject>" [account]` prints `worth`, `routine`, or `default`.

**Pass 2 — static rules.** Mark a message **Worth a look** when *any* of these hold:

- `importance == "high"`
- The sender domain is a monitoring or security service (Netdata, Sentry, PagerDuty, Datadog, Grafana, AWS Health, GitHub security alerts, Cloudflare alerts) **and** the subject suggests an open or escalated state (`Critical`, `Raised`, `Failure`, `Down`, `Breach`).
- The sender is a bank, payment provider, or government agency **and** the subject is not a routine receipt or statement (login from new device, suspicious activity, document required).
- The sender is a real human (free-text name, no `noreply`/`no-reply`/`notifications`/`updates` substring in the address) writing directly — not via a list.
- The subject explicitly asks the user for action by a date (`due`, `by Friday`, `before`, `action required`, `please respond`).

Everything else is **Routine**: newsletters, marketing, shipping/receipt notifications, social pings, recovered-state alerts, automated digests.

When in doubt between the two, prefer Routine — false negatives in this skill are recoverable (the message stays in the inbox); false positives drown the signal.

### 3. Render the report

The header carries the account name when one was resolved from memory. Legacy single-account runs (no memory file) omit the account suffix.

```
Triage — N unread, last <hours>h, account <account>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ Worth a look (M)
  <YYYY-MM-DD HH:MM>  <sender name, ≤24 chars>  <subject, ≤60 chars>
  ...

· Routine (N - M)
  newsletters: X · marketing: X · receipts: X · alerts (recovered): X · social: X · other: X
```

The Routine line is a single-line tally by sub-category — assign each routine message to one of the labels shown. Omit a label whose count is zero. If the breakdown is uninteresting (everything in one bucket), collapse to `Routine (N - M) — all <label>`.

If `M == 0`, render only the header and the Routine tally; add `✓ Nothing pressing.` underneath.

If `N == 0`, render:

```
Triage — inbox is quiet (last <hours>h).
```

### 4. Offer the next step

After the report, render up to two offers — one per pending action, on its own line.

**Worth a look offer** (when M > 0): name the most important item, paste its `webLink` on its own line, then ask `open · demote (subject) · demote (sender) · skip?`. One verb per yes. When the connector did not surface a `webLink`, omit the link line and the `open` verb — the demote/skip verbs still stand.

All state paths below resolve per-account when an account was resolved from memory: `~/.skadi/outlook/<account>/...`. With no memory file, fall back to the legacy flat path `~/.skadi/outlook/...`. Hook calls receive `<account> <bw-item>` as their trailing args (or no args for the legacy path).

- **open** — the user opens the link by hand; the skill does nothing further.
- **demote (subject)** — append `{"from": "<sender>", "subject": "<subject>"}` to `classify.json`'s `demote_to_routine` array. Future mail with this subject from this sender classifies as Routine. Create the file (mode 600) if absent; preserve other rules.
- **demote (sender)** — append `{"from": "<sender>"}` (no subject) to `demote_to_routine`. All future mail from this sender classifies as Routine.
- **skip** — do nothing.

**Routine offer** (when N - M > 0): both `mark read` and `move to folders` act through the Graph write hooks, which target each message by its Graph `id`. The connector is read-only and its `id` field is undocumented — so this offer stands only when `outlook_email_search` returned a usable Graph message `id` for the routine batch. If it did not, skip the write offer with a one-line note: `(mark-read / move unavailable — connector surfaced no Graph message id)`. Otherwise ask `mark read · move to folders · skip?`. One verb per yes; to do both, two yeses.

- **mark read** — pipe each routine message's `id` to `~/.claude/hooks/outlook-mark-read.sh <account> <bw-item>`, one per line. The hook prints `read: <id>` per success and `failed: <id> <code>` on stderr per failure. Render a one-line tally of marked vs failed.
- **move to folders** — for each sub-category present in the Routine batch:
  1. Read `folders.json` — a `{ "<sub-category>": "<folder-id>", ... }` map. If the sub-category has an entry, use it.
  2. If missing, run `~/.claude/hooks/outlook-folders.sh <account> <bw-item>` to list folders, present them with their `displayName`, and ask the user either to pick an existing folder or to create a new one by name. To create: call `~/.claude/hooks/outlook-folder-create.sh <name> <account> <bw-item>` — the hook returns the new folder's id on stdout. On answer (pick or create), append the choice to the map and persist it (create the file if absent, with mode 600).
  3. Pipe the sub-category's IDs to `~/.claude/hooks/outlook-move.sh <folder-id> <account> <bw-item>`, one per line.

  Render a one-line tally per sub-category: `<sub-category> → <folder> (M moved, K failed)`. If a sub-category has no mapping and the user declines to set one, leave those mails in place — the rest still move.
- **skip** — do nothing.

If both M == 0 and N == 0, the inbox is quiet — render the §3 quiet-inbox line and stop.

### 5. Stamp the run

Record the run timestamp so `/preflight` knows triage was done today:

```bash
~/.claude/hooks/triage-mark-run.sh
```

Run this after rendering the report, regardless of which branch step 4 took.

## Migration to multi-account

When `outlook_accounts.md` is introduced for the first time on a machine that already carries single-account state, move the legacy flat state once into the default account's subdir:

```bash
DEFAULT=personal      # match the entry marked `default` in outlook_accounts.md
mkdir -p "$HOME/.skadi/outlook/$DEFAULT"
mv "$HOME/.skadi/outlook/tokens.json"    "$HOME/.skadi/outlook/$DEFAULT/" 2>/dev/null
mv "$HOME/.skadi/outlook/classify.json"  "$HOME/.skadi/outlook/$DEFAULT/" 2>/dev/null
mv "$HOME/.skadi/outlook/folders.json"   "$HOME/.skadi/outlook/$DEFAULT/" 2>/dev/null
```

After the move, `/triage` reads state from the per-account path. Reads for a new account (e.g. `work`) come through the connector and need no sign-in; the Graph device-code dance fires only on that account's first write action (mark-read, move, or folder-create). Either way, the account's state is born under `~/.skadi/outlook/<account>/`.

## Rules

- Never reveal the body content of a message in the report — the subject and sender are enough. The user can open the `webLink` if curious.
- Never bulk-archive or mark-as-read on the user's behalf without an explicit yes for that batch.
- Fetch once through the connector's `outlook_email_search` — one fetch, one report. `outlook-fetch.sh` is retired from this path; the connector reads, the Graph write hooks mutate.
- If `hours` is non-numeric or absent, default to `24` without prompting.
