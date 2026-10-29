---
name: build-pipeline
description: "The stage machine from a task number to a shipped task: intake, draw, design (precut.py), build, the leak reader and judge together, ship, then the next task at once. Owns pipeline.json, the stage gates, effort per role, the commit points, returned tasks (routed to /fix-determinism and /fix-rubric), freeze.py, status.py, re-rooting and retirement. Invoked by /build, the two fix commands, and when resuming a build in flight."
---

# Build pipeline

Every gate is a script's exit status or a thread's verdict; no thread runs before the free gates pass.
One session carries a build end to end in its main thread at max effort. Spawned agents exist only where
isolation is the point (the leak reader and the judge must not have seen the design) and run at medium.
There is no solver round: stump power is argued on paper (`precut.py`), checked by the leak reader and the
judge's Gate F, and measured by the portal.

## The stages

| # | Stage | Skills | Gate to leave the stage |
|---|---|---|---|
| 0 | intake | `fingerprint` (`recent`, `coverage`) | `taskNN` from `status.py next <handle>` (the earliest backlog wave) or as handed out; `status.py taskNN` read for a new number (the seed's header and Situation only); `pipeline.json` with `status` `DRAWING` (or the rework's stage) |
| 1 | draw | `guide-to-prompt`, `stumping`, `fingerprint` (`mechanisms`, `check`, `register`, `names`) | card at PASS or answered WARN, **the 10/10 rules answered first** (`stump_class` analytical, the analyst test naming the easy route's wrong answer), both layers named, people drawn, the stump unique; **default path ending on a wrong answer, stump sentence, data-native sentence**. Commit `DRAWN (taskNN)` |
| 2 | design | `stumping` (screen, fork table, 3 to 5 rungs), `determinism-check` (closure), `supplemental-stumping`, `guide-to-prompt` | **`precut.py taskNN` exit 0** (runs `voice-check.py`) |
| 3 | build | `dataset-generation`, `determinism-check`, `submission-writeup`, `golden-realism`, `reduce-house-fixes`, `leak-check`, `fingerprint` | generator green, every fork asserted, the three-rules block (`dataset-generation` §7.1) green; `verify`; two byte-identical builds; input gates; `metadata.json`; `figures_check.py` exit 0; realism sweep; house-fix register; `leak.py` not LEAK; `guard.py surface` clean and `heart` not BLOCK |
| 4 | check | `leak-check` (reader), `determinism-check` (judge) | both spawned in one message, in the background. Reader: no decisive-step sentence, no helping file, quoted sentences execute to the golden, no main-call fork. Judge: APPROVE. Every finding fixed in the generator in one pass, stage 3 gates re-run; FIX_NOW re-judged once; the reader re-runs only if a document or the prompt changed. SEND_BACK: re-root |
| 5 | ship | `fingerprint`, `reduce-house-fixes` | pre-ship check in the design note, the 10/10 rules re-read against the built pack (the decisive step still analytical, the mess still only Layer 1); `target.zip` from the final rebuild; card current; ledger row `SHIPPED, delivered MM-DD, pending review`; `status` `SHIPPED`; commit `SHIPPED (taskNN): <the call>` with the zip and `golden/` force-added; the author handed the bundle and the stump, leak and judge lines. **Then the next task** |
| 6 | portal | the author | the author's portal list rewrites the ledger's portal record: APPROVED is `SHIPPED_APPROVED`, PENDING_REVIEW stays `SHIPPED`, a shipped build missing from the list is `FAILED_TO_STUMP` and joins the backlog; a determinism or rubric return is routed (Returned tasks) |

Back to design: a reader finding a decisive-step sentence or a main-call fork; a FIX_NOW that moves the
decisive path; a portal return where the call landed.

## Effort per role

| Role | Where | Effort |
|---|---|---|
| The build session (design, build, every repair) | `/build`, `/fix-determinism`, `/fix-rubric` | max, set in the command |
| Leak reader | stage 4, `/leak-check` | medium (`general-purpose`, `model: sonnet`, `effort: medium` on the call) |
| `determinism-judge` and its thread | stage 4, `/fix-determinism` | medium (agent definition) |
| `clone-auditor` and its adjudicators | `/clone-check` only | medium (agent definition) |
| `/approve` | author sign-off | medium |

## Running the stages

- **One thread.** Design and build are one hand; a repair runs where the context already is. Spawn a fresh
  agent for a repair only when the session is near its context limit, briefed with `pipeline.json`, the
  design note and the finding, never a resumed finished agent.
- **Stage 4 spawns the reader and the judge together** (same pack, neither changes it). While they run, update
  the card and write the pre-ship check. Collect both reports, fix everything in one generator pass, rebuild,
  and relay nothing structural until both are in: a fork, a decoy or a re-root called on one report alone
  costs the build a wasted pass. Where they disagree on what a shipped sentence licenses, the judge
  recomputed and the reader did not, so the judge settles it (task190: the reader read a band bound as the
  definition of the graded figure and the judge, cold on the same pack, found the estimand filed and the
  method open; task194: the reader's narrative said regression to the mean and the judge's arithmetic showed
  the structure sound). A reader finding is evidence of what a solver sees, which is Gate F, not Gate C.
  re-run the free gates, then re-judge only on FIX_NOW and re-read only if a document or the prompt changed.
- **The free gates come first, always:** nothing with a token cost runs on a pack the scripts have not passed.
- **No author checkpoints.** The draw is shown in ten lines and the build carries on; the author can stop or
  redraw at any point, and `/approve` remains for a manual sign-off.
- **Stage 0 reads no more than it needs.** `status.py taskNN` prints the seed's header and Situation; the
  rest of a seed is decoy-era design and is not read. The pitfall is re-found from the data.

## Commits

Commit only at a status change: `DRAWN`, `SHIPPED`, `RESHIPPED`, `PAUSED`, `RETIRED` (`CLAUDE.md`, Git). Each
commit stages its paths by name: the task folder, `.claude/skills/fingerprint/cards/taskNN.json`, the ledger
row, and at ship `git add -f taskNN/target.zip taskNN/golden/`. Then `git pull --rebase origin main` and push.
Nothing is committed between those points; a session that stops mid-stage writes `pipeline.json` with a
`resume` line and commits `PAUSED`. A blocker is never a reason to stop: the session that meets it removes it
(a redraw, a re-root into another domain and dataset, a generator fix) and carries the build on (`CLAUDE.md`,
A stuck build is unblocked, never parked).

## Returned tasks

**Every return reships on the regular checks only** (`CLAUDE.md`, the STOP block): the fix in the generator,
the free gates, the determinism judge, the leak check (`leak.py` and the one leak reader) and the clone check
(`guard.py heart` and `surface`). No solver, scored reader or probe is run, before the fix or after it.

A portal result comes back in one of three shapes, and each has its own repair. Every repair keeps every free
gate (generator checks, `verify`, byte-identical rebuilds, `leak.py`, `guard.py validate` and `heart`,
`voice-check.py` at `.claude/skills/guide-to-prompt/references/voice-check.py`, `figures_check.py`,
`precut.py`) and proves its scope with `freeze.py`.

- **Determinism block failed** (the judges found a fork, a competing defensible answer or a figure that does
  not recompute): `/fix-determinism`. The fork is closed in the record so the literal execution is the golden;
  the main call, the stump, the ladder and every graded figure are frozen.
- **Call held, rubric at or over 70:** `/fix-rubric`. The ask layer is reworked against the responses' paths;
  the main recommendation side is frozen, because touching it can turn a passed verdict into a failed one.
- **Call landed:** back to stage 2 with this session as designer. Read the response against the default path
  and rungs; it left the ladder after the last rung it shows:
  - walked the default path to the golden: redesign the decisive step, never add a rung above it;
  - never saw the rung, yet landed: discriminator dominance failed, fix the magnitudes;
  - saw the rung and declined it: file the selection criterion, never the method;
  - executed the rung as a work order: it was announced; the leak sweeps and readability screen find where;
  - missed only on a misread field or misapplied rule: a lower rung, not the stump; redesign.

Each attempt gets a `## Tried and rejected` line. A repair re-cuts `target.zip`, appends to `returned`, sets
`status` `SHIPPED`, commits `RESHIPPED (taskNN)`, and counts as a loop against the architecture.

**Failed to stump.** A shipped build the portal list leaves out is `FAILED_TO_STUMP`: it goes into the
backlog as a rework (redesign when the portal solved it, re-root when the architecture is spent),
and `/build taskNN` picks it up from its `pipeline.json` when its wave comes round.

**The 10/10 gate on every rework, before any resume** (`CLAUDE.md`, first section). The card carries
`stump_class: analytical`, `analyst_test` and `domain_test`, with no official or validated decoy flag; the
note's `## Three rules` passes `precut.py`, `Not semantics:` and `Not rule application:` included. A design
whose decisive step is a plant, a withheld rule, a field reading or an executed procedure is re-rooted at
stage 1, never resumed. `status.py next` prints what a rework still owes.

## `freeze.py` and `status.py`

- **Pick the mode whose contract matches the repair's scope, and if none matches, say so rather than
  manufacturing a pass.** `--mode determinism` appends any changed Deliverable Answers block to its
  findings unconditionally, on the premise that a determinism repair moves no graded figure, and `--allow`
  reaches only `figures.json` keys. So a determinism finding whose fix changes an asking sentence's unit or
  an ask's figures cannot be proved by that mode: task196's judge required the walk restated in index units
  and ask 1's grain pinned, both of which move block 4, so with all 25 ordered keys allowed exactly one
  finding remained and it was the ordered change itself. The control there is `--mode rubric`, which proved
  the Final Recommendation and Critical Components numbers, every main-call `figures.json` value, the stump
  sentence, the card's stump and driver, the ladder, the default path and the prompt's call sentence all
  unchanged while 18 ask figures moved, plus a fresh `snapshot` taken at the repair's end so that nothing
  moves from there to the judge. Editing `freeze.py` or retaking the snapshot to clear a mode the repair
  was always going to fail manufactures a pass on the author's own control: record both commands and both
  outputs instead, and let the author pick the mode.
- `freeze.py snapshot taskNN` before the first edit of a fix; `freeze.py check taskNN --mode determinism` or
  `--mode rubric` after the rebuild. It freezes the Final Recommendation and Critical Components numbers,
  the figures.json keys carrying them, the stump sentence, the card's stump and driver, the design note's
  ladder and default path, and the prompt's call sentence; in determinism mode also every Deliverable Answers
  number. Exit 1 lists what moved; a move the author accepts is named with `--allow` and its reason written
  in the design note.
- `status.py` prints every backlog wave with each task's status (`--handle <name>` for one file, `--all`
  for every folder and the portal record); `status.py next <handle>` the next task to start from the earliest
  wave; `status.py wave <handle>` the next six open lane numbers as a wave row; `status.py taskNN` the seed.

## `pipeline.json`

The one state file in a task folder: where the build is, never why.

```json
{"task": "task108", "status": "BUILD",
 "domain": "...", "objective": "forecasting",
 "stage": 3, "stage_name": "build", "updated": "2026-10-11",
 "stump": "the stump sentence",
 "architecture": 1, "loops": 0,
 "precut": {"exit": 0, "date": ""},
 "leak": {"leak_py": "", "reader": ""},
 "duplicate_check": {"heart": "", "nearest": ""},
 "judge": {"verdict": "", "disposition": "", "report": ""},
 "returned": [{"date": "", "portal": "", "repair": "determinism | rubric | design", "commit": ""}],
 "resume": "", "approved": null, "delivered": null, "portal": null,
 "portal_id": "", "portal_status": "APPROVED | PENDING_REVIEW", "portal_status_date": ""}
```

`status` is one of `DRAWING`, `DESIGN`, `BUILD`, `SHIPPED` (submitted, pending review), `SHIPPED_APPROVED` (the
portal approved it), `RETURNED`, `FAILED_TO_STUMP` (back in a backlog wave), `PAUSED` (the session ended
mid-stage; never a waiting state), `RETIRED`. Older files may
carry `solver_rounds`, `branch` and old stage numbers: history; `status.py` infers their status from
`stage_name`. `/approve` sets `approved`.

## Resuming

Read `handoffs/<handle>.md` if it names the task, then `pipeline.json` (`status`, `stage`, `resume`) and
`## Tried and rejected`; re-check that stage's gate before new work. No `pipeline.json` with a finished
submission is stage 3 complete. A portal result means Returned tasks. A `PAUSED` build is taken before any new
number, and `status.py next` names it first.

## Re-root and retirement

An architecture is **spent** when the judge returns SEND_BACK, a FIX_NOW fails its second pass, its third
portal return fails, or `precut.py` fails twice on the default path (re-root before any data is cut). A
hardening deepens Layer 2 or Layer 1 and never plants; if only a plant would hold, the architecture is spent.

**Re-root:** a new draw at stage 1 in the same objective and number, `architecture` incremented, `loops`
reset, the old card's lineage saying spent and why, one line in `## Tried and rejected`, committed `DRAWN`.
A re-root follows a spent architecture in the same session; when the domain or the seed's world is what keeps
failing, the new draw moves to another client domain and dataset. A slot whose third architecture is spent is
re-rooted again without a checkpoint; it is **retired** only on the user's word: a `## Retired` section in the
design note, `status` `RETIRED`, every card kept, committed `RETIRED`.

## Throughput

How many builds run at once is the user's call, not a per-person quota: no task belongs to anybody and any
build can be worked by whoever the user asks. The default is two in flight, a re-root counted as one, so that
while one waits on stage 4 the other proceeds; the user may ask for more, and then more run.
**The moment a build ships or retires, start the next task in the backlog** (`status.py next`, `/build`).
Waves are six tasks to ship, worked in order; when one is fully shipped, `status.py wave "<objective>"` cuts
the next from that objective's range and it is added to a backlog file in that `SHIPPED` commit.
