---
name: using-the-dashboard
description: "Use when you want to present an interactive board to the human user (status, options, NEEDs with A/B/C picks), or when you see a dashboard mention and wonder what is actually usable today. Carries the CLI surface, the write/read discipline, and the live-vs-coming honesty table."
---

# Using the Agent Dashboard

The Dashboard is an agent's way to put an **interactive board** in front of the
human user: typed widgets (status rows, cards, lists), optional HTML regions,
and **action-picks the user answers by clicking an option and optionally typing
nuance**. It replaces the "agent runs a TUI" pattern — it is out-of-band from
the messaging channel, so it never blocks messages and answers never scroll
away.

Dashboard writes (`dashboard set`, `dashboard answer`) are Pro. On a Free install a write is refused with an error
containing `not entitled`: stop writing the board for the session and keep the question in the message thread instead.
Reading and deleting stay free.

This is the COMMONS skill: role-agnostic surface + discipline. Role overlays
(`coordinator-dashboard-human-loop`, `brainstormer-dashboard-needs`) add the
role-specific loop on top. When an overlay and this skill conflict, the overlay
wins for role-specific behavior.

## 🔴 Honesty table — what is usable TODAY

Check this BEFORE you promise the human anything. Stale promises are worse
than no dashboard.

| Capability | Status |
|---|---|
| `dashboard.set/get/show/clear/delete` RPCs (daemon-side) | **LANDED** on trunk (merge `6c7539236f83`); usable only against daemons BUILT after that merge — verify your daemon's build before relying on the RPCs |
| `thrum dashboard` CLI (set/show/get/update/delete/clear/results) | **LANDED** on trunk (merge `108511a0`); usable only against a `thrum` binary BUILT after that merge — verify your CLI's build before relying on these commands |
| Web UI Dashboard tab (where the human SEES a board) | **SHIPPED** in v0.11.0-rc.1 (E3, merge `49712f87`) |
| Answer round-trip (user clicks → message + nudge to you) | **SHIPPED** in v0.11.0-rc.1 (E4, merge `ea95318a`) |

**Consequence, now that E2 has landed:** the `thrum dashboard ...` command
shapes below are runnable — but, per the E2 row above, only against a CLI
binary built after `108511a0`. Against an older binary, or if you're
calling the daemon directly, the raw RPCs (`dashboard.set` etc. over the
daemon socket) remain the fallback surface.

## The board model

A dashboard is ONE structured document per agent: an envelope
`{v, agent_id, title, updated_at, rev, widgets[]}`. Six widget types:
`section` (labeled grouping), `stat-row` (label/value pairs),
`card` (title + markdown body), `list` (ordered rows),
`action-pick` (question + options + optional text — the interactive control),
`html` (sanitized rich region, authored from a FILE).

Semantics that matter to you as an author:

- **Append-only + rev'd.** Every change appends a new snapshot; `rev` increments.
  Your `update` keeps a widget's position; `delete` removes it; `clear` wipes
  the board. Cleared/deleted content is **GONE** — the board is ephemeral, and
  the DURABLE record of any decision is the answer MESSAGES, not the board.
- **Widget cardinality (enforced):** action-pick ≤8, html ≤4, section ≤8,
  card ≤24, stat-row ≤12, list ≤4, total ≤64. Lists have NO row cap.
- **Answer path:** when the user answers an action-pick, you get a **nudge**
  and the answer lands as a thrum MESSAGE (payload type `dashboard.answer`,
  carrying `question_id`, the option `pick`, optional `text`). You read
  answers with `thrum dashboard results`.
- **Action-pick `status`** is `open` or `resolved`, set with `thrum dashboard update`, which takes the whole widget.
  `dashboard show` prints a pick as `RESOLVED` when its status is `resolved` and it has no answer, and as
  `ANSWERED (<pick>)` whenever an answer exists, whatever the status. `status` also drives
  `dashboard results --unanswered`, which leaves out answers whose pick is `resolved`. A card's `status` shows after its
  title, for example `(resolved)`.
- **User deletes are SILENT.** If a widget you posted disappears, the user
  dismissed it — you are NOT nudged. Notice it on your next `show`; do not
  repost it reflexively (the user saw it and removed it on purpose).
- **No dashboard yet is not an error.** `dashboard.get`/`dashboard.show`
  succeed with `found: false` and an empty envelope when nothing has been
  posted for you yet — do not treat that as a failure to recover from.
- **Concurrent writes are guarded by `expected_rev`, not merged.** If you pass `expected_rev` and it no longer matches
  the board's current `rev`, the write is rejected with
  `dashboard changed (rev %d, you expected %d) — re-read with dashboard show and resubmit`. Fix: re-fetch the current
  document and resubmit with the fresh `rev`. Omitting `expected_rev` skips the check entirely (last-writer-wins) — fine
  for your own solo edits, risky if something else writes the same board.

## CLI surface (runnable now, against a `thrum` binary built after `108511a0`)

```bash
# Publish/replace whole widgets (upsert by widget id — targets update in place)
cat > /tmp/board.md <<'EOF'
{"title": "My board", "widgets": [ ... ]}
EOF
thrum dashboard set --doc-file /tmp/board.md
thrum dashboard set < /tmp/board.md   # stdin is the default when --doc-file is omitted

# HTML regions come from FILES ONLY — never inline (backticks in shell strings EXECUTE)
thrum dashboard set --html-file /tmp/panel.html --html-id my-panel

# Read
thrum dashboard show                 # compact outline: what's on the board, what's PENDING/ANSWERED
thrum dashboard get <widget-id>      # full widget JSON
thrum dashboard results              # user answers (after your nudge), newest N selected, displayed oldest-first
thrum dashboard results --unanswered # only questions with no answer yet

# Mutate
thrum dashboard update <widget-id> --doc-file /tmp/new-widget.json   # in place, keeps position
thrum dashboard delete <widget-id>
thrum dashboard clear                # wipe the whole board (content is GONE)
```

**Validation loop:** `set`/`update` either print `posted OK (rev N)` or fail
with one of three error shapes: a per-widget schema error naming the exact
widget id + field; a per-type cardinality error naming the widget TYPE + count
(e.g. "too many action-pick widgets: 9 (max 8)"); or the aggregate/total-cap
error, which names a CATEGORY TOKEN + count + max rather than a widget type
(e.g. "too many widgets (total_widgets): 65 (max 64)" — "total_widgets" is the
violation category, not a widget type: the per-type limits sum to 60 < 64, so
a doc breaching 64 always breaches some per-type limit too, and there is no
single offending widget type to name). On any of these: fix the file and
resubmit — do not recompute the whole board inside one invocation.

**Authoring rules with teeth:**

- Widget `id`s are load-bearing — stable across updates; `update`/`delete`
  and the answer join key off them (action-picks also carry `question_id`).
- Text fields render as MARKDOWN (no raw HTML — that is the `html` widget's
  job, sanitized). Keep compact fields single-line.
- HTML files: no script/style/iframe/event-handlers — the render side strips
  them, but author clean anyway.

## Widget schema

```json
{"title": "<board title>", "widgets": [
  {"id": "hdr",  "type": "stat-row", "stats": [{"label": "<label>", "value": "<value>"}]},
  {"id": "rows", "type": "list",     "title": "<list title>", "rows": [{"id": "r0", "text": "<one-line markdown>"}]},
  {"id": "note", "type": "card",     "title": "<card title>", "body": "<markdown>"},
  {"id": "grp",  "type": "section",  "label": "<section label>"},
  {"id": "ask",  "type": "action-pick", "question_id": "<stable question id>", "prompt": "<markdown question>",
   "options": [{"id": "a", "label": "<option A and its consequence>"}, {"id": "b", "label": "<option B>"}],
   "allow_text": true, "status": "open"}
]}
```

- `stat-row` takes `stats`, `list` takes `rows` (each row has its own `id`), `card` takes
  `title` + `body`, `section` takes `label`. Widget `id`s are the upsert key — keep them stable.
- `action-pick` requires `question_id`, `prompt`, a non-empty `options` list (each with `id` and
  `label`) and `allow_text`; `submit_label` is optional. `status` is optional: `open` or `resolved`.
- Write the document to a file; `thrum dashboard set --doc-file <f>`. Pass `--replace` when one
  generator owns the whole board.
- Regenerate the board from a script that prints one summary line, run from the agent's own
  session. A daemon-spawned monitor process is an unauthenticated caller (identity is
  kernel-verified per process) and cannot write the board, whatever environment it carries, so
  schedule the monitor as a reminder (`--schedule`, `--match`, `--notify-on-success`) and run
  the generator when the reminder arrives. The cron schedule is evaluated in the daemon's local
  time zone, not UTC.
  Load the `using-monitors` skill before you arm that reminder.

## The board is for the human reader, not an audit trail

- Show what the reader needs to decide or know; filter out coordinator mechanics.
- A "landed since deploy" list shows feature/fix branch landings only — no trunk-sync merges,
  pull merges, or artifact commits.
- An "orchestrators" view shows each orchestrator's open work, not liveness.
- When the owner asks for a change, change the generator, not the snapshot.

## When to reach for the dashboard (vs a nudge vs a message)

- **Dashboard:** state the human will consume VISUALLY and possibly answer
  interactively — rosters, queues of options, pipelines, NEEDs with discrete
  choices. Persistent board the human checks on their own rhythm.
- **Nudge:** something needs attention NOW and is small (one line). The
  dashboard does not pulse or blink; urgent + tiny = nudge.
- **Message:** conversation, anything needing prose back-and-forth, or anything
  the record must keep forever (decisions live in messages).

Anti-pattern: posting a board INSTEAD of answering a direct question. The
dashboard is a surface you maintain, not a replacement for talking.

## Refs to other skills

- `coordinator-dashboard-human-loop` — coordinator overlay: owning a board for
  the human, the human-loop mandate
- `brainstormer-dashboard-needs` — brainstormer/researcher overlay: authoring
  NEEDs as answerable action-picks
- `using-the-queue`, `using-thrum-state` — sibling agent-tied local surfaces
