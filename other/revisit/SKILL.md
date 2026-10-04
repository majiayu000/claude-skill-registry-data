---
name: revisit
description: >-
  Revisit dashboard — one scan of everything you parked to re-check later,
  across every skill's memory. Reads out/*/tracker.md and the other memory
  files skills leave behind (ideate PARK "revive when", verdict/scout
  revisit-when triggers, refactor WATCH candidates, learn spaced-repetition due
  dates, jobfit roles to re-check) and surfaces what's due now: date-based items
  past their date, trigger-based items whose condition may have fired. Renders
  one prioritized "due to re-check" list in chat — grouped by skill, most
  overdue first — quoting the exact tracker line and its revive trigger so you
  can act or defer. Strictly read-only: it never edits a tracker or fires the
  follow-up skill; it points, you decide. Use for "what do I need to revisit",
  "what's due to re-check", "anything parked worth reviving", "show my revisit
  queue" — e.g. "/revisit", "/revisit ideate".
---

# revisit — what you parked, now due

`/revisit` — scan every skill's memory for items due to re-check
`/revisit <skill>` — only that skill's tracker (e.g. `/revisit ideate`)

Skills that judge under uncertainty don't just decide — they record a **trigger
for revisiting the decision**: ideate PARKs an idea "revive when X", verdict
stamps "revisit-when", scout/refactor leave WATCH items, learn schedules the
next review by date. Scattered across `out/*/`, those triggers rot unseen. This
skill is the one place that gathers them and asks a single question: **what is
due to re-check right now?**

It is **strictly read-only** — the same contract as `daybrief`. It never edits a
tracker, never marks anything revived, never runs the follow-up skill. It
surfaces; you decide.

## Step 0 — Locate the memory

Today's date is `date +%F` (compute it; don't hardcode). Then find `out/` in the
current project.

- No `out/`, or no memory files under it → say so plainly and stop. Nothing to
  revisit is a valid, complete answer (keyless, graceful — never invent items).
- `/revisit <skill>` → restrict the scan to `out/<skill>/` only.

**Completion criterion:** the set of memory files to scan is fixed, or a clean
"nothing to revisit yet" is reported.

## Step 1 — Collect the revisit signals

Read each memory file and pull every line carrying a revisit signal. Known
shapes (don't limit to these — any "revive/revisit/recheck/due" marker counts):

| Source | Signal to pull |
|---|---|
| `out/ideate/tracker.md` | PARK rows with a **"Revive when …"** reason |
| `out/verdict/*.md` | **revisit-when** triggers on a past verdict |
| `out/scout/tracker.md` | **WATCH** items and their revive condition |
| `out/refactor/tracker.md` | **WATCH** candidates deferred to a trigger |
| `out/learn/*.md` | next-review **due dates** (spaced repetition) |
| `out/jobfit/tracker.md` | roles marked to re-check later |

Skip anything already resolved (SHIPPED, DONE, DROP, applied) — a DROP is not a
revisit. Capture for each item: source skill, the verbatim line, and its
trigger (a date, or a condition in prose).

**Completion criterion:** a flat list of open revisit items, each tagged with
source skill and its trigger.

## Step 2 — Classify each item

Sort every item into exactly one bucket:

- **DUE** — a date-based trigger whose date is **on or before today**, or a
  condition-based trigger that plausibly **has fired** given what you can see in
  the repo/trackers (state the evidence). When unsure whether a condition fired,
  mark **DUE** and say why it's worth a look — a false "check this" is cheaper
  than a missed revive.
- **NOT YET** — date still in the future, or condition clearly not met. Keep it,
  but below the fold, with the unmet trigger shown.

Don't fire or resolve anything — classification only.

**Completion criterion:** every item is DUE or NOT YET, each with a one-line
reason.

## Step 3 — Render the queue

One prioritized list in chat:

- **DUE first**, most overdue at the top (oldest date, or longest-standing
  condition). Group by source skill. For each: the quoted line, its trigger, why
  it's due, and the **next skill to run** if the user chooses to act (e.g.
  "→ `/ideate` to re-diverge", "→ `/verdict revisit <brief>`").
- **NOT YET** collapsed underneath as a short "watching" list — item + the
  trigger not yet met — so the user sees the horizon without noise.
- Nothing DUE → say so in one line; the watching list is still worth showing.

Never auto-run a follow-up. Naming the next skill is a suggestion the **user**
acts on — the read-only contract holds to the last line.

**Completion criterion:** a single grouped, prioritized queue in chat; every DUE
item names the skill that would act on it; nothing was written or triggered.
