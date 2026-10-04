---
name: eos-week-review
description: Personal-life weekly review and next-week plan. Reads the past week's journal entries, milestones, mood check-ins, the system-generated wheel review, the previous weekly note, and the month / half-year / year notes, so the week is planned against the commitments it serves — overdue month items roll forward with their age, and a week target contradicting a revised year target is caught. Drafts the blank review section in the current weekly note, drafts a top-3-plus-supporting plan into next week's Focus section, and pushes the actionable items into the projects app as real tasks. Use when the user says "review this week and plan next week", "weekly review", "what did I do this week", or "plan next week" in a personal-life context. NOT an EmptyOS dev session log (use eos-session-wrapup) and NOT a per-track dev brief (use eos-session-resume).
---

# EmptyOS Week Review

Reflect on the past week (personal life, not EmptyOS dev work) and plan the next, then capture the plan as durable tasks in the projects app so it survives the conversation.

## When to use

- User says "review this week and plan next week", "weekly review", "what did I do this week"
- Sunday evening / Monday morning loop
- The blank `## Review` and Focus sections in the latest `{vault}/50_Journal/{year}/{year}-W{NN}.md` files are the visible symptom

Do **NOT** use this for EmptyOS dev session work — `/eos-session-wrapup` covers that. The line between them: dev-session = git-tracked codebase changes; week-review = the human's life.

## Pre-flight

This skill writes its plan as tasks through the daemon HTTP API, so the daemon must be reachable first:

- **Daemon up** — `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:9000/projects/` should print `200`. If not, ask the user to run `restart.bat` — never start/restart the daemon yourself (`.claude/rules/daemon-handling.md`).
- **Auth (private mode)** — read `auth_token` from `emptyos.toml` `[network]` and send `Authorization: Bearer <token>` on every request (`.claude/rules/environment.md`).
- **Non-ASCII task text** — POST via Python `urllib`, not `curl -d` (cp1252 mangles em-dash / CJK).

## Vocabulary

- **This week** — the week containing today's date, in ISO Mon-start (`datetime.date.today().isocalendar()`)
- **Last week** — `this_week - 1`
- **Weekly note path** — `{vault}/50_Journal/{year}/{year}-W{NN}.md`. Kevin's notes use Sun-start weeks (file says "May 10-16" but ISO W20 is May 11-17). Use the ISO week for the filename; trust the file's date-range header for the actual coverage.
- **Month note path** — `{vault}/50_Journal/{year}/{year}-{MM}.md` (e.g. `2026-08.md`). This is where every commitment carries its real 📅 date, grouped under life-area headings. When next week crosses a month boundary, read **both** month notes.
- **Half-year note** — `{vault}/50_Journal/{year}/{year}-H1.md` / `-H2.md`, linked from the month note's blockquote. Holds the gates and hard deadlines the month cascades from.
- **Year note** — `{vault}/50_Journal/{year}/{year}.md`. Holds the standing targets (exercise frequency, English hours, floor salary) and the quarterly focus. This is the layer that gets *revised*, so it is the authority when a week note disagrees with it.
- **The vertical chain** — year → half-year → month → week → day, wikilinked in both directions. A weekly plan drafted without reading up the chain is the failure mode this skill exists to prevent; see Step 2.

## Process

### Step 1 — Gather signal

Read these, in order, then synthesise. Don't synthesise from one source.

1. **The week's daily journals**: `{vault}/50_Journal/{year}/YYYY-MM-DD.md` for each day Mon→Sun. Filter out `PLAYWRIGHT-TEST-*` and bot breadcrumbs (`Growth Agent`, `🎙️ Generated a podcast`, `🏗️ Built site`, `✓ Applied rooms.write_note`, `🪞 System reflected`). Keep: `🎯` milestone bullets, mood entries with substantive text, anything with a `#tag` that isn't an automated app emit.
2. **The current weekly note's existing content** (`{vault}/50_Journal/{year}/{year}-W{NN}.md`): theme, focus tasks that were set, ## Review section (probably blank), ## Wheel Review (probably populated by the Sunday-9pm scheduler — `apps/public/standard/journal/reflection.py::scheduled_weekly_wheel_review`).
3. **Active life-area files**: glob `{vault}/20_Areas/{Career,Health,Finances,...}/*.md` modified in the past 7 days (`stat` mtime). Don't read all of them — just the ones that moved.
4. **Active life-project files**: same shape for `{vault}/10_Projects/{slug}/` directories. Visa, job-search, healing, immigration tend to be the durable ones.
5. **The previous weekly note's plan** (`{year}-W{NN-1}.md`): which items shipped, which slipped. Compare to actual reality, not just to the checkbox state (Kevin rarely ticks).
6. **The wheel-review narrative** if present in the current weekly note: it's the system's read of which dimensions got starved. Use it; don't re-derive.
7. **The month note** (`{year}-{MM}.md`) — read it in full, both this month and next month if next week straddles the boundary. This is the commitment source of truth: unchecked `- [ ] … 📅 YYYY-MM-DD` lines under each life-area heading, the `## Weekly Reviews` section where the month assigns each week a 重点, struck-through lines marking superseded work, and any `[UPDATED YYYY-MM-DD]` annotation that revised an earlier target.
8. **The half-year note** (`{year}-H2.md`) and **year note** (`{year}.md`) — skim for the standing targets and the hard gates. You need these to catch a week note planning against a number the year already revised.

Sources 7 and 8 are not optional and are not "extra context". They were absent from this list until 2026-08-18, and that single omission is the whole reason the skill kept producing plans that ignored overdue monthly commitments — see Step 2.

### Step 2 — Reconcile against the month

Before drafting anything, build a reconciliation table. This is the step that makes the vertical chain real; without it the weekly plan is drafted from last week's residue and whatever area files happened to move, which lets a dated monthly commitment sink with nothing noticing.

Produce four lists. Keep them in scratch, not in the vault — they feed Step 3's 未完成 and Step 4's Focus.

**1. Overdue** — every unchecked `- [ ]` line in the month note carrying a 📅 date **before today**. For each, record the days overdue and which life-area heading it sits under. Do not filter by importance yet; a three-day-late investment transfer and a nine-day-late certification phase both belong on the list.

**2. Landing next week** — every unchecked month-note item whose 📅 date falls inside next week's date range, plus the month note's own 重点 for that week from its `## Weekly Reviews` section. The month assigns the week a job; read it. If next week's assigned 重点 has no corresponding item in the plan you draft, that is a finding, not an oversight to smooth over.

**3. Drift** — any place the week layer and the month/year layer disagree:
- A **number** the year revised that the week still uses. Grep the year and month notes for `[UPDATED` annotations and compare each revised target against the current week note's metric line and Focus list. This has happened with a weekly-hours target revised *downward* in both the year and month notes, while a week note authored two weeks later still carried the old figure — including in its `___/Nh` review placeholder, which then measures against a target nothing else uses.
- A **task the month note already closed** — struck through (`~~…~~`) or annotated as superseded — that the week note still carries as live work. The recurring shape is a monitoring task ("check X weekly") for a process that has since completed: the month note strikes it, the weekly template keeps reproducing it.
- A **frequency or fixed slot** that degrades down the chain: year says 3x/week on fixed days, month says 3x, week names one weekday, and the calendar holds something else. Report the whole chain, not just the mismatched end.

**4. Needs a time block, not a task** — items that cannot be completed without an appointment or a booked slot: medical appointments, classes, consults, calls with a named person, anything with a third party's diary in it. Restating these as tasks is what lets them roll indefinitely; a task can be carried, a 2pm cannot.

> **Honesty limit.** EmptyOS cannot currently see the external calendars — `[apps.calendar]` subscribed-calendar import is dark (`calendar.feature.calendar-ics-import.enabled`, default false), so nothing in the vault knows whether a block was actually booked. Until that flag is on, treat list 4 as *unverifiable* and say so in Step 6 rather than implying it was checked. Do not infer a booking from a ticked task.

#### The roll limit

An item overdue by more than **14 days** must not simply roll a third time. Rolling it again is evidence the item's shape is wrong, not that the week was busy. Pick one, explicitly:

- **Shrink it** to the smallest first action that fits in 15 minutes, and roll only that. "Book back-pain appointment" becomes "find the clinic's number and put it in the note".
- **Block it** — convert it to a specific day and time, and say in Step 6 that it needs to reach the calendar by hand.
- **Kill it** in the month note with a one-line reason, struck through. A commitment that has survived three weeks of not mattering enough to start is allowed to be wrong.

Never carry an item forward silently for the third time. Name every roll in Step 6 with its age, and name anything you killed. A silently-truncated list reads as "everything is tracked" when it is not — the same discipline as `.claude/rules/audits.md`.

### Step 3 — Draft the review

Find the `## Review` section in the **current week's** weekly note (`this_week`). It usually has placeholders like:

```
**English Hours**: ___/7h | **Zumba**: ___/3
**完成:**
**未完成:**
**感想**:
```

Fill in. **Voice rule for the whole section:** this is Kevin's own weekly note — draft it as if Kevin wrote it (first person, never address him as "you"; same discipline as braindump's capture summary). Recognition test: each line should make him go "oh right, that."

**Always add the reach counter**, on the metric line beside English/Zumba:

```
**Sent to a human**: ___  (what / to whom / when — or "nothing")
```

One binary field: did anything this week reach an actual person outside the vault. A LinkedIn
post that went live, an outreach DM, a job application submitted, a referee approached, an
email to a recruiter. **Drafting it does not count. Publishing to your own blog does not
count.** The test is whether a named human could have seen it.

Why this row exists, and why it is not optional: the 2026-08-16 insights pass measured the
pattern the Q1 review first named as "the builder trap". Five separate tracks — outreach,
LinkedIn, job applications, CPEng, the August pipeline — had all failed at exactly the same
step, and every one of them was *prepared and never sent*. Nothing in the weekly template
asked the one question that separates those five failures from success, so the gap was
invisible for four months while everything upstream of it looked productive. A "nothing" here
is a legitimate and useful answer; leaving it blank is not. If it reads "nothing" two weeks
running, say so plainly in **感想** — that is the signal, not a footnote.

- **完成** — bullets with a leading emoji + (date), **one bullet per goal/work-stream, not per event**. Default to merging: fold related wins under the stream they served — two bullets about the same stream should almost never exist. Lead with the biggest unblock, not chronologically. Skip dev-work wins (those go to /eos-session-wrapup).
- **未完成** — bullets describing each gap. Be specific: which outreach didn't happen, which area got zero signal, which item from last week's Focus quietly rolled. Name the wheel-imbalance directly using the wheel review's words. **Every item on Step 2's overdue list belongs here with its age** — "<item> still open, N days past its <date> date" is the shape. An overdue monthly commitment that never appears in 未完成 is exactly how it stays invisible for another week; the review is the only place the month layer gets read back to the human.
- **感想** — 2–3 short paragraphs in Kevin's first-person voice. Honest, not performative. Don't summarise — interpret. What was the emotional shape of the week? Was the energy in the right place given Kevin's stated priorities (career pivot, visa wait, balanced life)?
- **Personal-life summary** — one short paragraph at the bottom linking forward to next week's note: `[[YYYY-WNN+1]]`. State the top-3 in one sentence.

### Step 4 — Draft the plan

Find the `## Focus` section in **next week's** weekly note (`this_week + 1`). Often pre-populated with a template. Add four blocks above the existing `本周目标` list:

```markdown
**Top 3 (do these even if everything else slips):**
- [ ] 🎯 ... 📅 YYYY-MM-DD  ⟵ serves [[{year}-{MM}]] <area>
- [ ] 🎯 ... 📅 YYYY-MM-DD  ⟵ serves [[{year}-H2]] <gate>
- [ ] 🎯 ... 📅 YYYY-MM-DD

**Rolled forward from [[{year}-{MM}]] (overdue at the month grain):**
- [ ] ... 📅 YYYY-MM-DD  ⟵ was 📅 YYYY-MM-DD, Nd late
- [ ] ... 📅 YYYY-MM-DD  ⟵ was 📅 YYYY-MM-DD, Nd late — needs a calendar block

**<category> — <one-line frame>:**
- [ ] ... 📅 YYYY-MM-DD
- [ ] ... 📅 YYYY-MM-DD

**Life-balance restock (counter the W{NN} wheel-imbalance):**
- [ ] Fill one Three-things per day 📅 YYYY-MM-DD
- [ ] One <thin-dimension> action 📅 YYYY-MM-DD
```

Rules:
- Top-3 must be **named verbs with specific objects**. Not "do career work". "Open Application-Tracker, log the two stalled applications' status, decide on a nudge" is correct shape — a verb, a named artifact, and a decision to reach. Use role descriptions rather than third parties' names in examples; this file ships in the public snapshot (see the note in Cross-references).
- **Each Top-3 item names the parent it serves** with a `⟵ serves [[…]]` trailer pointing at the month or half-year note plus the area or gate. A top-3 item that cannot name a parent is either genuinely new (fine — say so) or is filling the week with work the month never asked for (not fine). This trailer is the only place the upward edge gets written down, so it is what makes the chain auditable next week.
- **The rolled-forward block is drawn from Step 2's lists 1 and 2, and honours the roll limit.** Anything shrunk gets its shrunken form here; anything killed does not appear here at all and is struck through in the month note instead. Carry the original 📅 date in the trailer so the age keeps accumulating visibly — resetting the date hides the roll.
- **Items from Step 2's list 4 get the `needs a calendar block` trailer.** Do not silently convert a booking into a task.
- Every supporting bullet must have a 📅 date.
- The "Life-balance restock" block must respond to the actual wheel reading — if Physical was Empty, the action is a physical one. Don't paste a generic template. **When the wheel reports a dimension Empty, check Step 2's list 4 and the week's known fixed commitments before believing it**: the wheel scores journal signals and `healing` habits only (`apps/public/standard/journal/reflection.py::_today_dimension_signals`) and cannot see the calendar, so a recurring class reads as zero. Say "the wheel can't see X" rather than prescribing a restock for a dimension that was actually fed.
- **Fix the drift you found.** If Step 2's list 3 caught a stale number in the template's metric line (e.g. `___/7h` against a 5h target), correct it in next week's note and say so. If it caught a superseded task, drop it from the plan and note why. Leaving known drift in place because "the template is load-bearing" propagates it another week.
- Don't touch the existing template lines (`本周目标`, `重点任务`, `💼 Job Search`, `## Tasks`, etc.) — augment, don't replace. Kevin's weekly template is load-bearing across years. Correcting a target *number* inside a template line is not replacing the template; deleting the line is.

### Step 5 — Push tasks into the projects app

The weekly note is markdown — easy to skip, easy to forget. Real tasks live in the `projects` app. Pick the right project per bullet:

| Bullet category | Project id |
|---|---|
| Career / outreach / job search | `job-search` |
| Visa / immigration | `visa-189` (or `visa-eb2` / `visa-canada` depending on theme) |
| Health / Zumba / diet / inner work | `54-day-safe-projects` if active, else `health` if it exists, else create a personal project for the quarter |
| Apartment / environment | `apartment-decoration` |
| Sydney networking | `job-search` (it's a career signal, not its own track yet) |

POST shape (Windows notes: cp1252 mangles em-dash via curl `-d`, use Python urllib for any
non-ASCII body — `feedback_curl_windows_utf8_bodies.md`; and use `127.0.0.1`, NOT `localhost`
— Python urllib resolves `localhost`→IPv6 `::1` while the daemon binds IPv4, so `localhost`
gives `WinError 10061 connection refused`):

```python
import urllib.request, json, tomllib
with open('emptyos.toml', 'rb') as f:
    TOKEN = tomllib.load(f)['network']['auth_token']
URL = 'http://127.0.0.1:9000/projects/api/projects/{project_id}/tasks/add'
body = json.dumps({'text': '...', 'due': 'YYYY-MM-DD'}).encode('utf-8')
req = urllib.request.Request(URL, data=body, method='POST',
    headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'})
urllib.request.urlopen(req, timeout=15)
```

Tag every task `#w{NN}` plus a category tag (`#top3`, `#career`, `#wellbeing`). Tag rolled-forward items `#rolled` as well — it makes the treadmill queryable, so "what has been rolling for a month" is one filter instead of a diff across weekly notes. The hub task panel filters by tag; the weekly note's `## Tasks` block uses an Obsidian Tasks query that pulls by due-date window.

If the daemon hiccups mid-POST (connection refused), retry with `time.sleep(1.5)` between calls — 8-task burst sometimes overruns whatever rate limit is in front of the projects app.

### Step 6 — Report

Tell the user (in chat):
1. Wins + gaps in 2–4 bullets each
2. Top-3 for next week, each as one sentence, each naming the parent it serves
3. **The reconciliation result** — how many month-level items are overdue and by how long; which ones rolled, which you shrank, which you killed and why; and anything on Step 2's list 4 that needs to reach the calendar by hand. Name every roll with its age. If the calendar ICS import is still dark, say plainly that bookings could not be verified.
4. Any **drift** you corrected (a stale target number, a superseded task) and any you found but left alone, with the reason.
5. How many tasks landed in which project
6. **The one EmptyOS gap you noticed** that this skill bumped against — feed it back so the skill (or its dependencies) keep improving. The skill exists because the gap was: "system has the signal, doesn't bridge to action." Notice the next narrowing of that gap.

Do NOT generate a `/eos-session-wrapup`-style devlog from this skill. The weekly note IS the log.

## Cross-references

- `apps/public/standard/journal/reflection.py::scheduled_weekly_wheel_review` — Sunday 9pm cron that writes the wheel narrative this skill reads (bound onto the spine at `journal/app.py`, per `.claude/rules/multi-module-apps.md`)
- `apps/public/standard/journal/reflection.py::_today_dimension_signals` — what the wheel actually counts: daily-journal signals plus `call_app('healing')` habits. It does **not** read the calendar, which is why a recurring class can show as a dimension Empty. Step 4 tells you to say so rather than prescribe against a false zero
- `apps/public/standard/calendar/ics.py` — the dark ICS ingest (`parse_ics`, SSRF-guarded `_fetch_ics`, cache, scheduled refresh). Enabling `calendar.feature.calendar-ics-import.enabled` plus `ics_feed_urls` in `[apps.calendar]` is what would let Step 2's list 4 be *verified* instead of merely flagged, and would let the wheel see committed time. Config only, no code
- `apps/public/standard/projects/app.py::add_task_to_project` / `POST /projects/api/projects/{id}/tasks/add` — task-write endpoint
- `apps/public/core/task/app.py` — read-side aggregator that surfaces tasks tagged `#w{NN}` on the hub
- `.claude/rules/time-dimension.md` — past → future → now is exactly what a weekly review does; this skill is its first concrete consumer
- `.claude/skills/eos-session-wrapup/SKILL.md` — sibling skill for dev-side reviews; do not conflate
- `.claude/skills/eos-session-resume/SKILL.md` — sibling skill for dev-side resume; do not conflate
- **This file ships publicly.** `release-public.py` builds the snapshot from `git archive HEAD` and drops files under `.claude/` only when they name held engineering tokens — this one names none, so it reaches the public repo. Keep worked examples in role terms (never a third party's name), and keep dates and case-specific figures out; describe the *shape* of a drift or a rollforward instead. `.eos-personal` is not a fallback here: it ships publicly too and carries no literal names, so adding one as a pattern would publish it.
- `vault-journal-planner` skill (user-level) — generic periodic-notes management; overlaps in surface (weekly notes) but not in goal. `vault-journal-planner` arranges notes; this skill *interprets* a week's signal and *records actions*. Prefer this skill for Sunday-evening / Monday-morning review-and-plan loops; prefer `vault-journal-planner` for "create a new monthly note from template" or "where's my Q3 review folder" shape requests.

## When NOT to use

- The user is mid-conversation about EmptyOS code → use `/eos-session-wrapup` instead
- The user wants a one-off mood reflection → write it directly into the daily journal, no full weekly process
- It's Wednesday → fine to run, but the wheel review the scheduler writes Sunday 9pm won't reflect the current week yet, so the signal will be partial; mention this in step 6. Step 2's reconciliation is unaffected — month-level dates don't care what day you read them on, and mid-week is arguably the better time to catch something already overdue.
