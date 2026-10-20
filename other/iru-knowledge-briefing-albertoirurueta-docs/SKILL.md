---
name: iru-knowledge-briefing
description: Summarize the most relevant agreements and pending tasks recorded in the `knowledge/` base (built
  by `iru-knowledge-process-inbox`) for a given subject. Accepts any mix of scoping context — a person (matched
  against `knowledge/people/*.md`), a meeting reference ("last meeting", a date, or a topic keyword matched
  against `knowledge/meetings/meeting-*/meeting.md`), and/or a plain-language subject/topic — and searches
  `knowledge/people`, `knowledge/meetings`, `knowledge/agreements`, and `knowledge/pending` for material that
  matches. Invoke as `/iru-knowledge-briefing` to be asked for the subject/context, or `/iru-knowledge-briefing
  <subject-or-context>` to skip straight to searching. Read-only — produces a conversational report only (which
  meetings/agreements/pending tasks matched, their status, and who was involved), never edits any file in
  `knowledge/`. Stops early if `knowledge/` doesn't exist yet (run `iru-knowledge-setup` and
  `iru-knowledge-process-inbox` first). Use whenever someone needs to catch up on "what's been agreed/is still
  open about X" or "what did we discuss with/about Y" without hand-reading every meeting file, instead of
  `iru-knowledge-complete` (which closes out one specific task) or `iru-knowledge-to-issue` (which files one).
model: sonnet
---

# Knowledge Briefing

Produce a short, grounded briefing on what's been agreed or is still pending about a given subject, by
searching the `knowledge/` base rather than requiring someone to read every meeting file by hand. This skill is
read-only research: its output is a report, not a file edit.

## Step 1 — Confirm the knowledge base exists

Check for `knowledge/` and at least one of `knowledge/meetings`, `knowledge/agreements`, `knowledge/pending`. If
`knowledge/` doesn't exist at all, tell the user to run `iru-knowledge-setup` first, then
`iru-knowledge-process-inbox` to populate it, and stop. If it exists but every one of `knowledge/meetings`,
`knowledge/agreements`, and `knowledge/pending` is empty, tell the user there's nothing to brief on yet and stop.

## Step 2 — Determine the subject and any scoping context

If the skill was invoked with an argument, treat its full text as both the subject and any scoping context
combined (e.g. "what did Jane agree to about the pricing API in the last meeting" names a person, a meeting
reference, and a topic all at once). Otherwise ask the user, in plain conversational text (open-ended, not a
fixed choice): what subject/topic they want briefed on, and — making clear both are optional — whether they want
it scoped to:

- **A specific person** — a name that should match a file in `knowledge/people/`.
- **A specific meeting** — "the last meeting", a date, or a topic/title that identifies one meeting directory in
  `knowledge/meetings/`.

A briefing needs at least a subject, a person, or a meeting reference to search against — if the user gives
none of the three, ask once more before proceeding; don't summarize the entire knowledge base unscoped.

## Step 3 — Resolve a named person

Skip this step if no person was named.

Derive the expected filename the same way `iru-knowledge-process-inbox` creates one: lowercase, hyphen-joined
first and last name (e.g. "Jane Doe" → `jane-doe.md`). Look for `knowledge/people/<name>.md`:

- **Found**: read it in full (their role and what they've contributed across meetings, per how
  `iru-knowledge-process-inbox`'s Step 7 maintains it).
- **Not found under the exact derived name**: list the filenames that do exist in `knowledge/people` and ask the
  user (via `AskUserQuestion`) to pick the intended one, or confirm there's no matching person — don't guess a
  close match silently.

Note this person's name for Step 5's search — every meeting/agreement/pending file that mentions them (by name,
or as a diarized speaker) is in scope.

## Step 4 — Resolve a named meeting

Skip this step if no meeting reference was given.

- **"Last meeting" / "most recent meeting" / "latest meeting"**: list `knowledge/meetings/` and pick the
  directory with the lexicographically greatest `<timestamp>` — the filesystem-safe ISO 8601 naming
  (`meeting-YYYY-MM-DDTHH-MM-SSZ`) sorts correctly as a plain string, no date parsing needed.
- **An explicit date or date range**: match the meeting directory/directories whose `<timestamp>` falls on/in it.
- **A topic or title fragment**: search every `meeting.md`'s Summary section for a match; if more than one
  plausibly matches, list them (timestamp + one-line summary) via `AskUserQuestion` and ask the user to pick.
- **No match at all**: tell the user plainly, list the meeting directories that do exist (timestamp + one-line
  summary of each), and ask whether to proceed unscoped by meeting (search everything, per Step 5) or stop.

Note the resolved meeting directory (or directories, for a date range) for Step 5 — only material from these
meetings, and the agreements/pending files they produced, is in scope.

## Step 5 — Search for relevant material

Search across whatever scope Steps 3-4 established (a specific person, a specific meeting/date range, both, or
neither — in which case the whole knowledge base is in scope), for the subject given in Step 2:

- **Meetings**: grep every in-scope `knowledge/meetings/meeting-*/meeting.md` (Summary and Full transcription)
  for the subject's keywords. A meeting matches if the subject appears in its content, or — when scoped to a
  person — if that person is named/speaking in it.
- **Agreements**: grep every `knowledge/agreements/agreement-*.md` for the subject's keywords, restricted to
  items from in-scope meetings if a meeting/date scope was given. Note each matching item's checkbox state
  (`[ ]` open, `[x]` done) — a briefing on "the last agreements about X" should surface both, not just open ones.
- **Pending**: grep every `knowledge/pending/pending-*.md` for the subject's keywords (this also catches a
  hand-created pending file with no matching agreement entry). Cross-reference each match against the
  agreements search above to avoid reporting the same item twice.
- **People**: if not already scoped to one person in Step 3, note any other person whose `knowledge/people/*.md`
  file discusses the subject — they may be worth mentioning as "also involved" in Step 6.

If nothing matches at all, tell the user plainly (state what was searched and with which scope) rather than
producing an empty or padded-out report, and stop.

If a very large number of items match, prioritize by recency (most recent meetings/agreements first) and by
whether an item is still open (`[ ]`) over already-done (`[x]`) — state explicitly how many older/less-relevant
matches were left out of the report rather than silently dropping them.

## Step 6 — Read the matched material in full

For every meeting that matched, read its `meeting.md` in full (not just the snippet that matched the grep) so
the briefing reflects real context, not an out-of-context keyword hit. Read every matched agreement/pending file
in full too — they're short, and reading them avoids misreporting a checkbox state or item number.

## Step 7 — Compose the briefing

Report directly in the conversation (no file written, unless the user separately asks for one), structured as:

- **Scope** — restate what was searched: the subject/topic, and any person/meeting scope from Steps 3-4 (or "no
  scope given — searched the full knowledge base" if neither applied).
- **Relevant meetings** — one line per matching meeting: date/timestamp, a one-line summary of what was discussed
  relevant to the subject, and who was involved (from diarization, if available).
- **Agreements** — grouped by status:
  - **Still open** — each item's text, its source meeting, and its pending task id (so the user can act on it
    directly with `iru-knowledge-complete <task-id>` or convert it with `iru-knowledge-to-issue <task-id>`).
  - **Already done** — each item's text and source meeting, briefly, so the briefing shows the subject's recent
    history even where nothing remains to act on.
- **People involved** — if Step 5 surfaced anyone beyond an explicitly-scoped person, name them with a one-line
  note of their involvement.
- If Step 5 truncated a long match list, say so here, with a count of what was left out.

Keep the whole briefing tight — a person reading it should come away knowing what was decided, what's still
open, and where to look (file paths) for more detail, not have to re-read the meetings themselves.
