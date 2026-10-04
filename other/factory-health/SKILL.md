---
name: factory-health
description: "Weekly health check for the multi-channel content factory. Reads the append-only run logs in ./runs/, the open PR list on the fork, and the LinkedIn unshipped register, then reports which channels have gone dark, which are starved, and where work is piling up at the human gate. Catches the failure mode where a routine is broken or was never created and its silent exits look identical to normal no-op runs. Use when the user says /factory-health, 'is the factory healthy', 'check the channels', 'which channels are dark', 'why is X not posting', or when invoked by the weekly Factory Health routine. Always trigger this skill for factory health questions."
trigger: /factory-health
---

# /factory-health

Reports whether the content factory is actually running. Read-only. **This skill never generates content, never opens a PR, and never writes to a channel folder.** Its only side effect is an optional row in its own report history.

## Why this exists

Channel agents exit quietly when there is nothing to do, so a healthy no-op and a dead routine produce the same observable: nothing. X and Instagram were dark for seven weeks under exactly that cover. This check makes silence legible.

## Inputs

| Source | What it gives |
|---|---|
| `./runs/<channel>.md` | Last run date, last `produced` date, recent outcome pattern |
| `gh pr list --repo altaf-shaikh-cs/content-factory --state open` | Work waiting at the human review gate |
| `./linkedin-posts/TODO.md` → `## Ready to ship` | Finished LinkedIn posts never published |
| `./linkedin-posts/performance/tracker.md` → `## Unshipped register` | Same, cross-checked |
| Each channel's `TODO.md` Queue section | Whether the channel is starved of ideas |

Channels to check: `linkedin`, `x`, `instagram`, `blog`.

---

## Step 1 — Per-channel status

For each channel, parse its `runs/<channel>.md` table. Ignore rows with outcome `seeded`; they are backfill, not agent activity.

Compute:
- `last_run` = date of the newest row of any outcome
- `last_produced` = date of the newest row with outcome `produced`
- `recent` = the outcomes of the last 7 rows, in order

Assign exactly one status, first match wins:

| Status | Condition | Read |
|---|---|---|
| `DARK` | Channel has a routine AND `last_run` is more than **2 days** ago | The routine is broken, disabled, or was never created |
| `FAILING` | 2 or more of the last 3 rows are `error` | The routine fires but the run does not complete |
| `GATED` | `last_run` is current AND the last 3 rows are all `blocked` | Working as designed, but a gate is holding it. Act on the gate, not the agent |
| `STARVED` | `last_run` is current AND no `produced` in **14 days** AND recent rows are `skipped` | Alive but out of input. Check the queue and `inspiration-inbox/` |
| `HEALTHY` | Anything else | |

**There is no blog exemption.** Blog has a cloud routine — `Daily Blog Post Creator`, cron `30 13 * * *` UTC = 7:00 PM IST — so it is subject to `DARK` exactly like every other channel. The exemption that used to sit here assumed blog had no routine, which was never true; it was simply missing from `CLAUDE.md`'s table until 2026-09-08. Never report blog as `NO ROUTINE`.

**Channels that are off on purpose.** X (`trig_01TcT5YBCou7ZVapPN527Lzp`) and Instagram (`trig_01GrhrDA2vPYEyDkvuCUBRvi`) are `enabled:false` by the owner's deliberate decision of 2026-06-29, confirmed 2026-09-07. Their last runs SUCCEEDED. They will keep computing as `DARK` here, and that is expected rather than an incident — report the status, then say **off by decision, not broken**, so the reader does not go debugging a routine that is simply switched off. Do not suggest `setup-channel-routine` for either: it cannot delete a routine and would create a duplicate.

**Warm-up rule (important, and it expires).** A channel whose log contains **zero agent-written rows** has not yet had a chance to write one. Report it as `UNCONFIRMED` rather than `DARK`, and say what its last known activity was from git and the PR list. Otherwise the very first health check flags every channel as dark purely because the heartbeat is younger than the channels are.

`UNCONFIRMED` is not a free pass. Escalate to `DARK` anyway when the independent evidence is already damning: no output of any kind for more than 14 days, or zero PRs ever opened for that channel. That is a conclusion drawn from git and `gh`, not from an empty log, and it holds on its own.

**Use `gh pr list --state all`, never `--state open`.** `--state open` cannot see a merged PR, so a channel whose PRs were all merged reads as having opened none. That exact mistake put "zero PRs ever" into `CLAUDE.md` for X and Instagram on 2026-08-15 and pointed three weeks of diagnosis at "the routine was never created" when the routines existed, had worked, and had been switched off. "Never produced" and "produced, then stopped" are different findings and only `--state all` can tell them apart.

The warm-up rule stops applying to a channel the moment it writes its first real row. LinkedIn and blog have both written many; X and Instagram have written none and cannot, because their routines are `enabled:false`. So this section will not expire on its own — **delete it when X and Instagram are re-enabled and each has written one real row**, not before.

A `DARK` channel is the highest-severity finding this check produces. Never soften it, and always print the routines URL next to it.

---

## Step 2 — Review gate

```bash
gh pr list --repo altaf-shaikh-cs/content-factory --state open \
  --json number,title,createdAt,headRefName
```

Flag any PR open more than **3 days**. This is the bottleneck that generation cannot fix: the factory produced, and the content is sitting in review.

If 3 or more PRs are open at once, say so as its own line. That is a queue forming, not a backlog of one.

---

## Step 3 — Ship gate

Count the entries under `## Ready to ship` in `./linkedin-posts/TODO.md`, cross-checked against the `## Unshipped register` in `./linkedin-posts/performance/tracker.md`. Take the union, deduplicated by post-folder name.

Report the count and whether it is at or above the ship-gate threshold of **3** (see `linkedin-growth-agent` Step 0.5). At or above the threshold, LinkedIn generation is deliberately blocked, and the fix is to publish, not to debug.

---

## Step 4 — Report

Lead with the verdict. This output usually arrives as a push notification, so the first two lines have to carry it alone.

```
FACTORY HEALTH — <YYYY-MM-DD>
<N> dark · <N> starved · <N> healthy · <N> PRs waiting

DARK
  x           last run <date> (<N>d ago) · last produced <date>
              7 ideas queued · off by decision, not broken (enabled:false)
              → https://claude.ai/code/routines
  instagram   last run <date> (<N>d ago) · last produced <date>
              → https://claude.ai/code/routines

STARVED
  blog        alive, queue empty since <date>

HEALTHY
  linkedin    last produced <date> · 4 unshipped, ship gate ARMED

REVIEW GATE
  #36  content: linkedin - claude-code-auto-mode-classifier   4d open
  #35  content: blog — five-rung-ai-automation-ladder         4d open

NEXT ACTION
  <the single highest-leverage thing, one line>
```

Omit any section with no entries. Never pad the report to look complete.

### Picking the next action

One line, and it must be the highest-leverage item, in this order:

1. Any `DARK` channel → verify or recreate that routine
2. Ship gate armed → publish the named post today
3. PRs open more than 3 days → review and merge
4. `STARVED` channels → refill via `inspiration-inbox/` and `/sync-inspiration`, or a derived cross-idea
5. All healthy → say so in one line and stop

---

## Shared rules

- Read-only across the whole repo. Never write to `raw-ideas/`, any channel folder, or any `TODO.md`
- Never open a PR, never push a branch
- Do not generate content, even if a channel is starved and the fix looks obvious. Report it and let the channel agent do its job
- If `runs/` does not exist yet, say so, point at `runs/README.md`, and fall back to `git log -1 --format=%ad -- <channel-dir>` per channel with an explicit note that git history is a weaker signal because it cannot see runs that produced nothing
- Never claim a channel is healthy on the strength of a `seeded` row
