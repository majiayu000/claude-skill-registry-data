---
name: parrallello
description: "Use when running big work as parallel fronts. Parrallello — autonomous parallel execution engine: single-writer fronts, blocks of up to 3 rounds of FRESH builders + an ADVERSARIAL critic that approves only on numeric gates, a lead that does not read code and changes method when something recurs, and ONE-PASS agents that pre-stage future waves. Verified quality on few tokens. ALWAYS use when the owner says 'parrallello' / 'parallello' / 'paralello', 'engines + critic', 'builder and critic', 'until the critic approves', 'parallel fronts', 'blocks of rounds', 'Sample Project', 'pre-stage the waves', or asks for big, multi-front, autonomous work (hours to days) — web engines, Blender/3D scenes, data pipelines, refactors, apps — with measurable targets. The owner invoking the skill = explicit authorisation for Workflow and background agents."
version: 1.0.0
ported: 1.0.0
author: "the owner (ported from his Claude Code skills library)"
license: MIT
metadata:
  hermes:
    tags: [owner-library, orchestration, parallel, critic, gates]
    related_skills: [fable-orchestrator, spec-driven]
---
> Ported from the owner's skills library (port 1.0.0; the source hash and
> what it needs are in `manifest.json` next to this file). Paths written `{skill_dir}/…` are this skill's own
> folder, `{skills_root}/<name>/…` a sibling icloneOS skill, `{agent_home}/…` the agent's home. Runs on macos, linux only. Needs `git` on PATH, `python3` on PATH, `node` on PATH, `bash` on PATH. Not ported (the owner's own records — notes, logs, examples, project data — never ship): #1, `references/lessons.md`, `references/measured.md`, `references/scenarios.md`, `tools/gpu_lock.py`, `tools/status.py`.
> In this copy the owner's own folder and project names are written `sample project` (in the case and joiner they had); the control plane is `CONTROL/` and its local half `CONTROL/local.nosync/` (neutral folder names, in prose and code alike).

# Parrallello

**Idea.** Big work is split into **fronts**. Each front has files of its own (single writer) and numeric targets.

- **Rounds.** Each front runs in **blocks of up to 3 rounds**. In a round, 1–2 **fresh builders** (≤ 60 calls, ≤ 120 k of
  context) work on tickets. Then an **independent adversarial critic** tries to REFUTE that the front meets its targets.
  - The critic measures with **automatic gates**, adds new gates and returns tickets.
  - Approval = 0 majors, 0 mediums and every gate PASS.
- **Lead (you).** Does not read code. Launches background workflows, reacts to 3 events and analyses between blocks. When an item
  recurs, changes method.
- **Prep.** Future work that does not collide with the fronts in flight is pre-staged by **one-pass agents**.
- **Machine.** Long work (renders, builds, measurements) runs in the background at **0 tokens**.

Proven on the Sample Project (2026-10-04/05): 3 fronts in parallel, plus prep and an integration rehearsal, at ≈ 1.7–1.9 % of the Max week per
round. The old method, with long agents of 300+ calls, spent 3.8 %/round.

> References (read only the one the step asks for):
> - `references/lead-protocol.md`: end of block, analysis, anomalies, budget.
> - `references/lessons.md`: traps already paid for (read ONCE before the first "go" of a new project).
> - `references/plan-template.md`: the PLAN to write per project.
> - `references/scenarios.md`: what a "gate" is and where the lock is in each project type.
> - `references/measured.md`: measured numbers.
> - `examples/sample-project.md`: the real run.

---

## 0. When to use

| use | do not use |
|---|---|
| ≥ 2 fronts or ≥ 3 rounds expected; hours to days of work | a 1–3 file task, a question, a one-off fix → plain Agent or inline |
| **measurable** targets (tests, image metrics, fps/ms, IoU, counts, schema) | pure taste with no criterion → first define the yardstick with the owner |
| the machine has long work (render, build, bench) | read/research only → normal "Understand" workflow |

**Authorisation.** When the owner invokes the skill ("parrallello", "go — run …"), that is the opt-in for Workflow and for background
agents. Everything else follows CLAUDE.md: do not ask for confirmation of obvious decisions.

## 1. Roles

| role | who | does | never does |
|---|---|---|---|
| **Lead** | you, main session | plan, startup, workflows, commits, analysis between blocks, fixes ≤ 30 lines, method decisions, report | read big files, read agent transcripts, long progress messages |
| **Builder** | fresh agent per round and per file owner | ≤ 2–3 tickets (most severe first); snapshot before editing; `--quick` while iterating and `--full` once at the end; handoff note ≤ 15 lines | edit outside its list, commit, kill other people's processes, continue past the ceiling |
| **Critic** | fresh agent, `effort: high` | runs `--full` itself (performance inside the lock), probes what the gates do not see, puts each new probe into the gate script (dated), ≤ 3 contact sheets, JSON verdict and ≤ 8 tickets | edit the front's files; approve with majors, mediums or failing gates |
| **One pass** | fresh agent, no critic | pre-stages future waves: gate, baseline and tickets, plus the code that does not collide; integration rehearsals in *staging* | touch files of fronts in flight or live data the gates measure |
| **Machine** | `bgjob.py` | renders, builds, benches and caches in the background; the agent waits with `wait --max 540` | — |

## 2. Layout in the project (the *control plane*)

```
<root>/CONTROL/
  SAMPLE_PROJECT.md                 the plan (references/plan-template.md)
  sampleproject/<F>_critic_r<N>.json   verdicts (versioned)
  run/                       versioned
    RULES.md  tools/  workflows/  tickets/<F>_b<k>.json  baseline/<F>.json  state.json  costs.json
  local.nosync/                local (*.nosync/ stays in .gitignore)
    logs/ jobs/ scratch/<F>_<owner>_r<N>/ snap/<F>/r<N>_pre/ handoff/<F>_<owner>_r<N>.md gates/<F>_r<N>.json stage/
```

Install: `bash {skill_dir}/install.sh "<root>"`. Copies the tools, RULES.md and the workflow templates, creates the folders and
ensures `*.nosync/` is in `.gitignore`. It is idempotent: it never overwrites a file that has already been adapted.

## 3. Runbook — from request to finish

**A. Plan (inline, cheap, before spending).**
1. Scout: structure, existing tests, what is already approved, where the big files are.
2. Write `CONTROL/SAMPLE_PROJECT.md` from `references/plan-template.md`:
   - fronts, with file owners that do not overlap;
   - numeric targets for each front;
   - waves and dependencies;
   - progress-bar weights;
   - expected rounds and ceiling (3 blocks = 9 rounds).
3. Split fronts **by files, not by theme**. Two agents never edit the same file in the same wave.

**B. Startup.**
1. `get_usage` (§9).
2. `caffeinate -ims -t 604800` under nohup, with the pid saved; never wrap Python inside caffeinate.
3. `git status`; commit "checkpoint before the Sample Project"; `git tag pre-P-<date>`; push.
4. `install.sh`.

**C. P0 — setup** (`templates/workflows/setup.js`). 1 tools agent (self-test of each tool + the project's suites) and,
in parallel, **1 gate writer per front**:
- the gate script `--quick` (< 5 min) and `--full`;
- the `--full` baseline on the current code;
- `tickets/<F>_b1.json` (≤ 8, grouped by owner, most severe first, each one closing on a gate id).

Then: commit and `progress.py --set P0 status=approved`.

**D. Waves.**
- One `templates/workflows/block.js` per front, all in parallel. Launch with `Workflow({scriptPath, args})` (§6).
- The args carry the tickets in **lean** form (`id, owner, severity, gate`), plus `ticketsFile` with the full text. That way the
  lead does not rewrite long tickets.

**E. Lead loop — react to only 3 events.**
1. **Workflow finished** → `references/lead-protocol.md` §1–2.
2. **30-min pulse** (background Bash: `sleep 1800; python3 CONTROL/run/tools/status.py`) → act only on an anomaly (§3 of the protocol) and
   re-arm the pulse.
3. **Usage limit** → §9.

`get_usage` runs every 2 h and at every end of block. Each wake-up with nothing new = one short line or none.

**F. Between blocks** (`lead-protocol.md` §2):
1. `verdict_digest.py <F> --last 3` and the handoff notes.
2. Classify each open item: recurring → **change method**; regression → bisect and revert; miscalibrated gate →
   recalibrate with proof; ticket too big → split.
3. Make the fixes ≤ 30 lines.
4. Write `tickets/<F>_b<k+1>.json`, the section "Block k+1 — lead decision" in the front's contract, and the `leadNote`, which binds
   the critic too.
5. Commit and relaunch.

**G. Pre-stage (optional, recommended).** While wave N runs:
- `templates/workflows/prep.js` gives one pass per future front: gate, baseline and tickets, plus the conflict-free code.
- the same `prep.js`, with rehearsal jobs, rehearses the assembly and the final export **in staging**, and prepares the release (licences,
  secrets, notes, photos).

The wave opens and starts immediately.

**H. Finish** (final front approved):
1. `git tag v1.0` and a release with photos (≤ 2 MB each).
2. Update the plan and the README; the project memory keeps the state and the cost lessons.
3. Stop caffeinate (only our pid) and cancel the pulse.
4. Report **≤ 10 lines**, one per front: rounds, score, minors left and cost in % of the week.

## 4. The agent rules (`templates/RULES.md`, goes into EVERY prompt)

1. Fresh agent per task: ceiling of 60 calls and 120 k of context. On reaching the ceiling, write the handoff note and stop.
2. Never read big files whole: `codemap.py` first, then `sed -n` of the functions to change and `grep -n` to locate.
3. No output > 30 lines in context: `q.sh <cmd>` keeps the full log and shows the exit code and the last 15 lines. Big
   JSON goes through `jq` or python.
4. Long work = 0 tokens: `bgjob.py start/wait --max 540`. Never poll logs. **Before finishing, wait for or kill your
   OWN jobs**: orphan jobs double the critic's measurement.
5. Numbers first, eyes last: automatic gates decide; images only at the end and in ≤ 3 contact sheets (≤ 1600 px).
6. Iterate small: ≤ 480 px, only the affected tiles, `--quick`; full size and the full set once at the end.
7. Files, not chat: JSON tickets, notes ≤ 15 lines, JSON verdicts. Nobody reads another agent's transcript.
8. Measure once, reuse always: every new critic measurement goes into the gate script, dated. Caches are deterministic and
   keyed; manifest before cleaning.
9. Single writer per file; own scratch; shared tools only in `CONTROL/run/tools/`.
10. Snapshot before editing (`cp` to `snap/<F>/r<N>_pre/`).
11. Performance only in an exclusive window: `gpu_lock.py acquire --who X --max 900`, measure, `release`; never more than 15 min. Headless
    Chrome with its own profile, closed via CDP `Browser.close`.
12. Outputs for machines (JSON, numbers, paths). The human report belongs to the lead alone.

And the owner's rules: never commit or push (that is the lead), never credentials, never kill other sessions' processes, downloads only
CC0/CC BY/CC BY-SA/PD with credit, the root only by the given path.

## 5. Gates (the heart of quality)

- **Contract.**
  - `--quick` (iteration subset, < 5 min) and `--full`.
  - Output `RESULT_JSON {"pass":bool,"items":[{"id","value","target","pass"}]}` and a line `SUMMARY n/m PASS`.
  - Stable, hierarchical ids (`T.<hero>.<metric>.<view>`), with `--only <glob>`.
  - The critic saves the result to `local.nosync/gates/<F>_r<N>.json`, for `verdict_digest`.
- **The metric code is a frozen copy.** Builders do not edit it: the target does not move under them.
- **The critic adds gates every round**, for every thing it saw with its eyes or probed. The item count grows
  (373 → 449 is normal) and the yardstick only gets stricter.
- **Anti-cheat.** When a fix "passes" the gate without solving the thing (e.g. moving the tick so the version counter does not change), the
  critic creates a gate that measures the real thing (e.g. frames drawn in 10 s).
- **Anti-empty.** Gates measured on rejected or blank frames FAIL. A harness that silently drops items is a defect
  (compare the item count with the previous round).
- **Recalibrate only with proof**, recorded in the contract, with a date:
  - insufficient resolution (the feature is 1.5 px in the tile) → bigger tile;
  - noise (±25 % between runs) → median of 3 inside the lock;
  - wrong denominator (pixels outside the reference's framing) → `ok` mask;
  - clock assertions under contention → run inside the lock; an unstable item closes only with 2 full runs in a row;
  - the reference photo fails its own gate → the target becomes "≥ 0.9 × the reference".

## 6. Launching the workflows (scripts in `CONTROL/run/workflows/`)

`Workflow({ scriptPath: "<root>/CONTROL/run/workflows/block.js", args })`. The block args:

| arg | what |
|---|---|
| `root`, `front`, `label` | absolute root, front id (P1…), progress-bar label |
| `roundStart` | 1st round of this block (continues the front's numbering) |
| `owners` | `{owner: [files/globs]}`: each builder's edit list (single writer) |
| `gatesCmd` | gate script command, without `--quick`/`--full` |
| `contract`, `targets` | where the front's contract and targets are (the agent reads only the cited sections) |
| `prevVerdict` | path of the last verdict or `"none"` |
| `tickets` | lean list `[{id, owner, severity, gate}]`; `ticketsFile` = full text |
| `maxPerOwner` | tickets per builder per round (2–3; most severe first) |
| `leadNote` | lead decisions (method, recalibrations, widened lists). Binds builders AND critic |
| `criticFirst` | `true` when the 1st round is the critic alone on the code already done |
| `frontFrom`/`frontTo` | % of the front for the progress bar (block 1: 0→60; block 2: 60→85; block 3: 85→99) |
| `rulesFile` | defaults to `CONTROL/run/RULES.md` |

- The next tickets and each agent's result are in the workflow's **`journal.jsonl`** (last `result` with
  `approved` and `tickets`). The task's output file is not always pure JSON.
- Editing the script while workflows are running does not affect them, because each one loaded the script at startup.
- Size: 2 builders + 1 critic × 3 rounds = 9 agents per block.

## 7. Communication with the owner

- The owner wants it **short**: after "go", silence, except for a real blocker (login, credit, disk, paused front) in one line, or the
  final report.
- If the harness demands a line, state only the situation: front/round, % of the week and anomaly fixed.
- Direct question → direct answer. Estimate = hours along the critical path (remaining rounds × measured h/round) plus the worst
  case. Revise it when a front turns out to be slow.
- Request for "more agents" → say honestly where the bottleneck is (machine time, lock, single writer) and pre-stage only what
  does not collide (§3 G).

## 8. Parallelism — how much and where

- Per front: **≤ 2 builders per round**, with disjoint files. Split a front into two owners by file when a
  builder has ≥ 5 tickets or the foundation item stays undone for 2 rounds.
- Across fronts: as many as the waves allow without shared files (3 fronts + prep + rehearsal ran well).
- **The real bottleneck is the machine.** The render slots (6) and the exclusive measurement lock: a performance-heavy web front once
  held the lock ~50 % of the time and delayed the Blender fronts. More agents do not speed up a front whose `--full` takes 1 h of rendering.
- One-pass agents: ≤ 1 heavy job each, no lock, renders ≤ 480 px.

## 9. Budget and pace

- `get_usage`:
  - `Weekly · all models` ≥ 92 % → do not launch new blocks and let the running ones finish (wait mode until the reset);
  - 5 h window ≥ 95 % → same;
  - extra credit ≥ 90 % of the ceiling → pause at the end of the round and tell the owner in one line.
- Per block: `cost_mark.py "<F> b<k>" <weekly%> <extra€>`. If a block spends > 9 % of the week, the next one goes with ≤ 4 tickets and
  a ceiling of 40 calls.
- Measured: P0 (4 agents) ≈ 2 %; a 3-round block ≈ 1.1–1.3 M subagent tokens (≈ 180 k/agent, ~60 calls) and 6–9 h of
  wall clock; 3 fronts in parallel ≈ 1.5–2 % of the week per hour. Detail in `references/measured.md`.

## 10. Startup checklist (copy into the internal response, not to the owner)

- [ ] PLAN with fronts, disjoint owners, numeric targets, waves and weights
- [ ] usage OK · caffeinate alive · checkpoint + tag + push
- [ ] install.sh · P0 (tools + gates + baselines + b1 tickets) · commit
- [ ] wave 1 launched (1 block per front) · pulse armed · prep of the next waves launched if there is conflict-free work
- [ ] project memory: "Sample Project in progress", with the root and the workflow ids
