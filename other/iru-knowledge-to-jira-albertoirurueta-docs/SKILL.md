---
name: iru-knowledge-to-jira
description: Convert one or more pending/not-completed agreements from the `knowledge/` base (built by
  `iru-knowledge-process-inbox`) into a Jira ticket. Asks the user which agreement(s) to convert, accepting a
  pending task id (`<timestamp>-<n>`), a `knowledge/pending/pending-*.md` filename, a `knowledge/agreements/
  agreement-*.md` filename/id (with an item number if it has more than one open item), or a plain natural-language
  description — searching `knowledge/pending` and `knowledge/agreements` by content when given the latter. Once an
  agreement is resolved, gathers additional context from its meeting's full transcription and attachments (via
  `knowledge/meetings/meeting-<timestamp>/`) and from the current codebase (via the `iru-explore` skill), then
  hands the synthesized purpose to the `iru-create-jira-ticket` skill to draft and file the ticket — passing the
  meeting transcription and attachments along too, either as an actual attachment (uploaded via Jira MCP tools'
  native attachment support, or embedded/described per that skill's own fallback if none is connected) or, when
  the file is already committed and pushed in this repository, as a link to it instead of duplicating its
  content. Invoke as `/iru-knowledge-to-jira` to be asked which agreement(s) to convert, or `/iru-knowledge-to-jira
  <id-filename-or-description>` to skip straight to resolving that one. Stops early if `knowledge/` doesn't exist
  yet (run `iru-knowledge-setup` and `iru-knowledge-process-inbox` first) or if no Jira MCP tool is connected —
  there is no CLI fallback the way GitHub has `gh`; use `iru-knowledge-to-issue` instead when the work should be
  tracked on GitHub. Does not mark the source agreement complete — filing a ticket means the work is now tracked,
  not done; it instead appends the created ticket's key/URL back onto the pending file (and a note on the
  agreement item) so a re-run doesn't file a duplicate, leaving `iru-knowledge-complete` as the step that later
  closes it out for real. Use whenever a meeting agreement or action item needs to become actionable Jira-ticket
  work instead of staying a markdown checkbox nobody triages.
model: sonnet
---

# Knowledge to Jira

Turn a pending or not-yet-completed agreement recorded in `knowledge/` into a well-formed Jira ticket — grounded
in the meeting that produced it and, where useful, the current codebase — using `iru-create-jira-ticket` to
actually draft and file it. This skill's own job is resolving *which* agreement, gathering *why it matters*, and
handing that off; drafting and filing stays `iru-create-jira-ticket`'s job so the two skills don't drift apart.

This is the Jira equivalent of `iru-knowledge-to-issue` — same shape, but sourced through Jira MCP tools instead
of `gh`, and with Jira's native attachment endpoint instead of GitHub's release-asset workaround.

## Step 1 — Confirm prerequisites

Two things must both hold before doing any real work:

- **`knowledge/` exists and has content**: check for `knowledge/pending` and `knowledge/agreements`. If
  `knowledge/` doesn't exist at all, tell the user to run `iru-knowledge-setup` first, then
  `iru-knowledge-process-inbox` to populate it from meeting transcriptions, and stop. If it exists but both
  `knowledge/pending` and `knowledge/agreements` are empty, tell the user there's nothing to convert yet and stop.
- **A Jira MCP tool is connected**: search with `ToolSearch` (a query like "jira issue" or "jira ticket"). Note
  which capabilities are actually available (creating issues, fetching by key, **uploading an attachment to an
  existing issue**) — the attachment capability specifically drives Step 7's link-vs-attach decision. If none are
  found, tell the user plainly that this environment has no Jira connection and this skill has no fallback for
  filing one without it — the same limitation `iru-create-jira-ticket` itself has — and suggest
  `iru-knowledge-to-issue` instead if the work should be tracked on GitHub. Stop.

## Step 2 — Determine which agreement(s) to convert

If the skill was invoked with an argument, treat it as the identifier (or natural-language description) to
resolve in Step 3. Otherwise ask the user, in plain conversational text (this is open-ended, not a fixed choice),
which pending or not-completed agreement(s) they want turned into a Jira ticket. Make clear any of these forms
works:

- A pending task id (`<timestamp>-<n>`) or its filename (`pending-<timestamp>-<n>.md`).
- An agreement file's id/filename (`agreement-<timestamp>.md`) — plus which item number, if that file has more
  than one still-open item.
- A plain description of the agreement in their own words (e.g. "the one about adding retry logic to the client").

They may name more than one in the same answer (a list, or "these two: ... and ..."). Process each one through
Steps 3-9 below, one at a time, so a problem resolving or filing one doesn't block the others.

## Step 3 — Resolve the identifier to a concrete agreement item

For the current identifier:

- **Pending task id or filename**: look for `knowledge/pending/pending-<id>.md` directly.
- **Agreement id/filename, with an item number**: open `knowledge/agreements/agreement-<timestamp>.md` and locate
  that numbered item.
- **Agreement id/filename, no item number given**: open the file; if it has exactly one item that's still
  unchecked (`[ ]`), use that one. If it has more than one open item, list them via `AskUserQuestion` and ask
  which one they meant.
- **Natural-language description**: search the content of every file in `knowledge/pending` and
  `knowledge/agreements` for a match (`grep`-style keyword search, not just filename matching). If exactly one
  file/item matches clearly, use it. If several plausibly match, present short excerpts of each via
  `AskUserQuestion` and ask the user to pick. If none match at all, list the task ids/filenames that do exist
  (derived from the actual files present, the same fallback `iru-knowledge-complete` uses) so the user can pick
  one directly instead of guessing.

Once resolved, read the pending file (if one exists) for its agreement/meeting references, then open the matching
numbered item in its `knowledge/agreements/agreement-<timestamp>.md` file. Record: the task id (if any), the
agreement file path and item number, the item's own text verbatim, and the meeting reference (if the pending file
states one — see `iru-knowledge-process-inbox`'s Step 9 for the format it writes).

- **Item is already checked off (`[x]`) and no pending file exists for it**: this agreement is already marked
  complete. Tell the user plainly and ask via `AskUserQuestion` whether they still want a ticket filed anyway
  (e.g. for a regression or follow-up work) or want to skip this one — don't silently file a ticket for finished
  work.
- **Pending file already has a `- Jira ticket: ...` line** (see Step 9): a ticket was already filed for this
  agreement in an earlier run. Tell the user and ask via `AskUserQuestion` whether to open a second ticket anyway
  or skip this one — don't file a silent duplicate.

## Step 4 — Gather context: the meeting transcription and attachments

If the resolved item has a meeting reference, read `knowledge/meetings/meeting-<timestamp>/meeting.md` in full
(its Summary and Full transcription sections) and list every other file alongside it in that same meeting
directory (attachments carried over by `iru-knowledge-process-inbox`'s Step 6) — `Read` each one that's readable
(text, PDF, image) for context, same as `iru-create-jira-ticket`'s own file-reading step.

Since one meeting can cover several topics/agreements, pick out specifically the parts of the summary/
transcription that relate to *this* agreement item — not the whole meeting — as the core "why it matters" and
"what was actually decided" material for the ticket.

If the resolved item has no meeting reference (e.g. a hand-created pending/agreement file), note that plainly and
rely on Step 5 alone for grounding.

## Step 5 — Gather context: the codebase

Run `Skill({skill: "iru-explore"})` with no ticket argument — there's no Jira ticket yet, so this is a general
orientation pass, not one scoped to a ticket. Skip re-running it if general exploration already happened earlier
in this same conversation and looks reasonably current.

Using the agreement item's own text (plus whatever Step 4 surfaced) as keywords, search the codebase (`grep`, or
the `Explore` agent for a broader sweep) for the specific classes/files/modules this agreement would actually
touch — the same targeting `iru-explore` applies when it's given a real ticket, done here by hand since this
skill has no ticket to hand it yet. This is what makes the ticket's eventual Context/Acceptance-criteria sections
concrete instead of vague, and it's reused as-is by `iru-create-jira-ticket`'s own Step 2 in Step 8 below.

## Step 6 — Synthesize and confirm the purpose

Combine the agreement item's own text, Step 4's meeting context, and Step 5's codebase findings into a short
purpose statement: what problem this solves or capability it adds, why it matters (grounded in what was actually
discussed/decided), and any acceptance criteria the agreement text or meeting discussion implies.

Show this synthesized purpose to the user via `AskUserQuestion` before handing it off:

- **File it as-is** (recommended once it reads accurately).
- **Let me adjust it first** — take their correction and re-synthesize.
- **Skip this one** — move on to the next identifier from Step 2, if any, without filing anything.

## Step 7 — Prepare attachments: link vs. actual attachment

For every file gathered in Step 4 (the meeting's transcription source and its other attachments) plus the
resolved pending/agreement markdown files themselves, decide how each should reach the ticket:

- **Already tracked and pushed** (check with `git ls-files --error-unmatch <path>`, then confirm the commit that
  added/last-touched it is reachable from the pushed branch, e.g. `git log origin/<branch> -- <path>` returns a
  match): prefer a **link** to the file's stable location in the hosted repository (e.g.
  `https://github.com/<owner>/<repo>/blob/<branch>/<path>`, or the equivalent for whatever host `iru-explore`
  recorded) over re-uploading its content — the file already lives durably in the repo and may keep changing
  there.
- **Not tracked, or tracked but only committed locally (not yet pushed)**: treat it as a local file to actually
  attach — hand its path to `iru-create-jira-ticket`'s Step 4 in Step 8 below, which uploads it via Jira MCP
  tools' native attachment support if one is connected (confirmed in Step 1), or falls back to embedding/
  describing it otherwise.

Always include the meeting's full transcription file one way or the other — it's normally the single most
useful piece of context for whoever picks up the resulting ticket.

## Step 8 — File the ticket via `iru-create-jira-ticket`

Run `Skill({skill: "iru-create-jira-ticket", args: "<Step 6's confirmed purpose statement>"})`. As its own steps
run in this same turn:

- **Step 1 (Jira MCP tooling)**: already confirmed in this skill's Step 1 — it should pass through immediately.
- **Step 2 (explore)**: reuses Step 5's exploration from this skill instead of repeating it.
- **Step 3 (purpose)**: answer immediately with Step 6's confirmed purpose statement, already given as the
  argument; if it still asks a clarifying follow-up, answer from Step 4/5's gathered context rather than bouncing
  the question back to the user — only actually ask the user if the gathered context genuinely doesn't cover it.
- **Step 4 (additional context)**: supply, as "attached files/documents", every file Step 7 marked for actual
  attachment (with its local path); supply, as "URLs", every file Step 7 marked as already linkable. Don't
  fabricate related tickets — only mention one if the user names it, and don't supply an epic unless the user
  named one.
- **Step 4's delegation to `iru-jira-custom-context`**: let it run as normal — this skill gathers meeting/codebase
  context, not organization-specific Jira fields, so it has nothing extra to pre-answer here.
- **Steps 5-8 (due date/importance, project/issue type, draft, confirm+create)**: let these proceed on their own
  terms — due date/importance/project/issue-type are judgment calls that skill already knows how to make or ask
  about; don't pre-empt them. If the user declines to create the ticket at the draft-confirmation step, treat
  this identifier as skipped (not an error) and continue to the next one from Step 2, if any.

Capture the created ticket's key and URL from that skill's own Step 9 report, if it created one. If any file
failed to upload (per that skill's own Step 8 error handling), note it for Step 10's report.

## Step 9 — Record the ticket back into the knowledge base

If Step 8 actually created a ticket, append a line noting it — without checking off or otherwise altering
anything else:

- To the pending file (if one exists for this item): add `- Jira ticket: <key> (<url>)` after its existing
  `Agreement:`/`Meeting:` lines.
- Near the matching numbered item in its `knowledge/agreements/agreement-<timestamp>.md` file: add a short
  trailing note, e.g. `1. [ ] <original text> _(tracked in <key>)_` — leave the checkbox itself unchecked; filing
  the ticket means the work is now tracked elsewhere, not that it's done.

This is what Step 3's duplicate-detection check looks for on a re-run. Do not run `iru-knowledge-complete` here —
that stays a separate, deliberate step for once the work behind the ticket is actually finished.

If Step 8 was skipped or declined for this identifier, skip this step for it too — there's nothing to record.

## Step 10 — Report

Per identifier processed: which pending/agreement item it resolved to, whether a meeting/attachments and/or
codebase context were found and used, the created ticket's key and URL (or that filing was skipped/declined, and
why), any file that failed to attach, and confirmation that the knowledge base was annotated with the ticket
link. Remind the user that the agreement itself stays open until they run `iru-knowledge-complete` once the
linked ticket's work is actually done.
