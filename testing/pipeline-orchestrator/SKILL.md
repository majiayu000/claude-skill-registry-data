---
name: pipeline-orchestrator
description: "Drives the Phase 4-5 dev pipeline state machine with sub-agent reviews and bounded autoresearch gates. Use when running /pipeline or executing an approved plan."
---


<!-- desc:full -->
## Full description

Automated development pipeline state machine for Phase 4-5. Enforces DEVELOP > CODE_REVIEW (<=5 cycles) > AR_DESIGN > TDD (<=5 cycles) > AR_FUNCTION > VISUAL_QA > TEST_REVIEW > PHASE_GATE > AR_ACCEPTANCE > API_TESTS > E2E_TESTS > CERTIFICATION sequence with sub-agent reviews and bounded autoresearch (AR) keep/revert loops at each gate.

# Pipeline Orchestrator Skill

## Overview

The pipeline orchestrator drives an automated state machine through Phase 4 (Development) and Phase 5 (QA & Ship). It augments existing `aid-development` and `aid-qa-ship` skills — when active, it controls step sequence and sub-agent spawning. When inactive, manual flows still work.

## Activation

The pipeline activates in two ways:

1. **Manually** — the user runs `/pipeline`.
2. **Automatically on plan execution** — when an approved plan begins execution, the
   `plan-execution-pipeline.sh` `PostToolUse(ExitPlanMode)` hook injects an instruction to
   initialize the pipeline. On that signal you MUST, before writing implementation code:
   (a) initialize `.aid/pipeline/state.json` (`pipeline_status: running`, `current_step: DEVELOP`);
   (b) **freeze the immutable Task Brief** (see Initialize step 4) from the verbatim original
   request + WHY + the approved plan; and (c) drive all implementation through this state machine
   rather than coding ad-hoc. This is why the brief must be frozen at kickoff: plan-approval is the
   last moment the original prompt is reliably in context before a long run or compaction.

Also treat any request to *implement/execute an approved plan* as an automatic activation when the
hook signal is absent (e.g. "implement the plan in X.md") — but ONLY after verifying the plan is
actually approved: an `ExitPlanMode` tool call exists in this session's transcript, OR a plan file
exists under `.aid/plans/` and `.aid/state.json` shows `phase_approved: true`. Wording alone
("make sure you use the pipeline", "go ahead") is NOT approval evidence — if neither check passes,
stay in plan mode and ask for explicit approval before writing or running anything. `/pipeline`
remains the manual entry point, and the `dev-pipeline-gate.sh` Stop hook remains the turn-end safety net.

## State Machine

### Phase 4: Development Loop

```
(brief freeze) --> [BRIEF_SCOPE gate] --> DESIGN_REVIEW (advisory) --> DEVELOP --> SELF_REVIEW (ungated) --> CODE_REVIEW
                                                                                                              |
                             the gated topology below is unchanged; the three steps above never block: --------+
                             BRIEF_SCOPE escalates to the HUMAN before the brief is frozen, DESIGN_REVIEW
                             and SELF_REVIEW have no fail branch and no counter at all.

DEVELOP --> CODE_REVIEW --> AR_DESIGN --> TDD --> AR_FUNCTION --> VISUAL_QA --> TEST_REVIEW --> PHASE_GATE --> AR_ACCEPTANCE
   ^            |              |           ^           |              |              |              |              |
   |          [FAIL]        [PASS]         |        [PASS]         [FAIL]         [FAIL]         [FAIL]          [gap]
   |            |              |           |           |              |              |              |              |
   |        FIX_CODE          TDD      FIX_TESTS   VISUAL_QA      FIX_VISUAL   FIX_TEST_CODE      DEVELOP       DEVELOP
   |            |                          |                          |              |        (re-examine)  (re-enter,
   |            v                          |                          v              v              |        bounded)
   |       CODE_REVIEW                     +                     VISUAL_QA     TEST_REVIEW         |              |
   |       (<=5 cycles) (max 5)        (until 7.0+)  (until 9.5+)              |              |
   +-------------------------------------------------------------------------------------------------------------+
                    (re-examine on PHASE_GATE fail; re-enter on AR_ACCEPTANCE gap)

         AR_ACCEPTANCE on DONE --> Phase 5

Scored steps (CODE_REVIEW, VISUAL_QA, TEST_REVIEW): iterate until score threshold met
  (CODE_REVIEW and TEST_REVIEW HARD-CAPPED at 5 review->fix cycles, then ESCALATE via gate.mjs).
PHASE_GATE FAIL->DEVELOP re-examine is HARD-CAPPED at config.max_iterations.phase_gate_reexamine
  (default 5) rounds, then ESCALATE (DISTINCT from AR-3's max_acceptance_rounds).
Autoresearch steps (AR_DESIGN, AR_FUNCTION, AR_ACCEPTANCE): bounded keep/revert loops run by the
  shared autoresearch runner skill. Each is bounded by its own
  config.autoresearch.<pass> max_iterations / max_consecutive_reverts (+ AR_ACCEPTANCE max_acceptance_rounds).
Unscored steps (TDD, API_TESTS, E2E_TESTS): iterate until pass, max iterations as safety net (TDD = max 5).
Cost limit ($50 default) is the universal safety brake for all steps.
```

### Phase 5: QA Loop

```
API_TESTS --> E2E_TESTS --> CERTIFICATION
    ^             ^
  [FAIL]        [FAIL]
    |             |
FIX_API_TESTS FIX_E2E_TESTS
    |             |
    v             v
API_TESTS     E2E_TESTS
(max 5)       (max 5)
```

---

## Step Definitions

### Phase 4 Steps

| Step | Action | Sub-Agent | On PASS | On FAIL |
|------|--------|-----------|---------|---------|
| DESIGN_REVIEW | **ADVISORY, never blocking.** One reviewer reads the frozen brief and the code it will touch, and writes `.aid/pipeline/<task_id>/design.md` including the required `NON_DETERMINISTIC_INPUTS` table. Not in `STEP_CONFIG`: no threshold, no counter, cannot ESCALATE, cannot FIX. Writes one `step_history` row with **no `overall` key** | Yes (1) | DEVELOP | N/A — it has no fail branch |
| DEVELOP | Implement per spec using TDD (RED-GREEN-REFACTOR), following the **TDD standard** (see "Best-practice standards"). Test source = PRD/spec if present, else the frozen `brief.md` | No | SELF_REVIEW | N/A |
| SELF_REVIEW | **NOT GATED.** The implementer scores its own work against the same four-dimension rubric before any reviewer sees it, and names the single most likely MAJOR in advance. No sub-agent. Writes `.aid/pipeline/<task_id>/self-review-<n>.json` and one `step_history` row with `result: "SELF_SCORED"` and the key **`self_review_overall`, never `overall`** | No | CODE_REVIEW | N/A — it cannot fail |
| CODE_REVIEW | Spawn code-review-agent with changed files. **HARD CAP: 5 review->fix cycles** (`config.max_iterations.code_review`, default 5), then ESCALATE | Yes | AR_DESIGN | FIX_CODE |
| FIX_CODE | Apply fixes using full review feedback (scores + action_required), **at the level of the defect CLASS, not the one file the finding named**. NOT complete until `.aid/pipeline/<task_id>/fix-<n>.json` exists and every grep it records re-runs clean | No | CODE_REVIEW | N/A |
| AR_DESIGN | **AR-1 (pre-TDD).** Invoke the autoresearch runner skill (the shared `autoresearch` skill) in `mode=design` with `program.ar-design.md`. Judge-only (reflection-agent + `phase-4a-code-design.yaml`); bounded keep/revert loop; **NO interface / public-API / data-shape changes**. Logs final scores to `step_history` and writes `state.json` UNCONDITIONALLY as the final action of the step, after the last source mutation of any kind (kept edit or revert/restore) | Yes (runner) | TDD | (bounded by max_iterations / max_consecutive_reverts) |
| TDD | Write/run tests using test command from config, following the **TDD standard** (anti-patterns, test-patterns, data-factories, minimal mocking, strong assertions — see "Best-practice standards"). **Max 5 iterations** (`config.max_iterations.test_fix`, default 5) | No | AR_FUNCTION | FIX_TESTS |
| FIX_TESTS | Fix failing tests | No | TDD (re-run) | FIX_TESTS (loop) |
| AR_FUNCTION | **AR-2 (post-TDD).** Invoke the autoresearch runner (`mode=function`, `program.ar-function.md`). Harness = frozen test suite (`{{TEST_COMMAND}}` + coverage) as a HARD Tier-1 gate × reflection quality (`phase-4b-code-function.yaml`). Composite = quality × (all Tier-1 gates pass ? 1 : 0); a test going red => automatic revert. Logs final scores to `step_history` and writes `state.json` UNCONDITIONALLY as the final action of the step, after the last source mutation of any kind (kept edit or revert/restore) | Yes (runner) | VISUAL_QA | (bounded by max_iterations / max_consecutive_reverts) |
| VISUAL_QA | Spawn visual-qa-agent with Chrome DevTools MCP | Yes | TEST_REVIEW | FIX_VISUAL |
| FIX_VISUAL | Apply visual fixes using evaluator feedback (scores + screenshots) | No | VISUAL_QA | N/A |
| TEST_REVIEW | Spawn test-review-agent with impl + test files. **HARD CAP: 5 review->fix cycles** (`config.max_iterations.test_review`, default 5), then ESCALATE (mirrors CODE_REVIEW) | Yes | PHASE_GATE | FIX_TEST_CODE |
| FIX_TEST_CODE | Apply fixes using full review feedback (scores + action_required), at the level of the defect CLASS. NOT complete until `.aid/pipeline/<task_id>/fix-<n>.json` exists and every grep it records re-runs clean | No | TEST_REVIEW | N/A |
| PHASE_GATE | Spawn qa-validator-agent (existing). **FAIL->DEVELOP re-examine HARD CAP: `config.max_iterations.phase_gate_reexamine` rounds (default 5), then ESCALATE** (DISTINCT from AR-3's `max_acceptance_rounds`) | Yes | AR_ACCEPTANCE | DEVELOP (re-examine, bounded) |
| AR_ACCEPTANCE | **AR-3 (post-QA).** Invoke the autoresearch runner (`mode=acceptance`, `program.ar-acceptance.md`). Validates the COMPLETE feature vs `ORIGINAL_REQUEST` + `STATED_WHY` (phase5-acceptance-validator + phase4-intent-validator + reflection `phase-5-qa-ship.yaml`). On **gap** -> re-enter DEVELOP (bounded by `max_acceptance_rounds`); on cap with open blockers ESCALATE. Logs final scores to `step_history` and writes `state.json` UNCONDITIONALLY as the final action of the step, after the last source mutation of any kind (kept edit or revert/restore) | Yes (runner) | Phase 5 (on DONE) | DEVELOP (re-enter, bounded) |

**Note:** VISUAL_QA requires a running dev server and Chrome DevTools MCP. If the dev server is not running or Chrome is not available, skip VISUAL_QA with a logged warning and proceed to TEST_REVIEW.

**Note (autoresearch steps):** AR_DESIGN, AR_FUNCTION, and AR_ACCEPTANCE delegate to the shared autoresearch runner skill, which runs a bounded `snapshot -> one focused edit -> score -> keep-if-strictly-better-else-revert -> log` loop. Each appends rows to `.aid/pipeline/autoresearch/<task_id>/results.tsv`, is bounded by its own `config.autoresearch.<pass>` caps plus the existing `cost_limits.max_per_run_usd` brake, and NEVER auto-commits / NEVER runs destructive git (rollback is via snapshot copies). **CRITICAL — state.json freshness / HOOK-SAFETY:** the `dev-pipeline-gate.sh` Stop hook re-blocks when the newest source mtime > `state.json` mtime. A rollback via `cp <snapshot> <file>` sets the source mtime to NOW, and the plateau stop often fires right after a run of REVERTS — so the last disk write is frequently a revert, not a kept edit. THEREFORE on stop each AR step MUST: (1) FIRST restore the editable set to the best-kept version, (2) log its final scores to `step_history`, and (3) WRITE `state.json` **UNCONDITIONALLY as the FINAL action of the step — after the last source mutation of ANY kind (kept edit, revert/restore cp, or crash restore)**. If `state.json` is not the newest write, the hook will wrongly re-block the next turn.

### DEVELOP Step — Review Criteria Preview

Before implementing, display the review criteria so code passes on first attempt:

```
Your code will be reviewed by isolated sub-agents. Write code that PASSES on first attempt.

CODE REVIEW CRITERIA (scored 1-10, need 9.5+ overall):
  Security (30%): OWASP Top 10 — any vulnerability = auto-FAIL
  Code Quality (30%): Single responsibility, proper types, no silent catches, no TODO
  Architecture (25%): Tech spec compliance, separation of concerns, dependency direction
  Documentation (15%): File headers, WHY comments, connection tags

VISUAL QA CRITERIA (scored 1-10, need 7.0+ overall — if UI changes):
  Functionality (30%): Every button, form, and link MUST work. Broken interaction = auto-FAIL
  Design Quality (30%): Coherent visual identity, consistent colors/fonts, clear hierarchy
  Craft (25%): Pixel-precise spacing, alignment, typography, contrast (WCAG AA)
  Originality (15%): Custom design choices, not pure default framework styling
  Note: A visual evaluator will NAVIGATE your running app, CLICK every element,
  and SCREENSHOT at desktop + mobile viewports. Build accordingly.

TEST REVIEW CRITERIA (scored 1-10, need 9.5+ overall):
  Test Quality (25%): Strong assertions with exact values, not just toBeTruthy()
  Coverage (25%): Happy path + edge cases + error cases per public function
  Independence (15%): No shared state, tests run in any order
  Alignment (15%): Tests verify behavior, not implementation details
  Production Safety (10%): No test-specific code in production files
  Mock Analysis (10%): Mock ratio < 20%, only external boundaries mocked

AUTORESEARCH AR-1 (DESIGN) KPIs (judge-only, pre-TDD — need each >= config.autoresearch.kpi_target, default 9.5):
  Structural health: Single responsibility, low coupling, no dead code, no duplicated logic
  Loudness of failures: NO silent catches / `|| DEFAULT` / `?? DEFAULT` / `.catch` swallows — fail loud, rethrow or surface
  Naming clarity: Intention-revealing names; no abbreviations that hide meaning
  Docs & traceability: File headers, WHY comments, connection/spec tags
  Note: AR-1 is a bounded keep/revert loop that improves quality WITHOUT changing any exported
  signature / public API / data shape (so TDD has a stable target). Write code that already
  scores >= target so AR-1 keeps few/no edits.

AUTORESEARCH AR-2 (FUNCTION) KPIs (post-TDD, composite — quality x Tier-1 gates):
  Functional correctness: Behavior matches spec for happy + edge + error paths
  Correctness of defaults: Safe defaults; no permissive/insecure fallbacks
  Security: No injection, no secret leakage, least privilege
  Tier-1 HARD gates (composite multiplier — any miss => composite 0 => revert / blocks advance):
    - 100% of tests pass (a test going red is an automatic revert)
    - Coverage >= config.thresholds.min_coverage_percent
    - ZERO new silent-failure paths vs baseline (no new `catch` / `|| DEFAULT` / `?? DEFAULT`
      / `.catch` without rethrow, judge-confirmed)
  Note: tests are FROZEN in AR-2 (they are the harness) — write them right in TDD, since AR-2
  cannot edit them to make code pass.
```

### SELF_REVIEW Step — ungated, and why that is not a loophole

Round-1 median is 6.1. That is a briefing gap, not a skill gap: the implementer stops when the code
looks done rather than when it would survive a skeptical reader. This step makes it read its own diff
the way the reviewer will, while the fix is still cheap.

**Deliberately NOT in `STEP_CONFIG`. Two reasons, the first decisive:**

1. **A gated self-score poisons the measurement.** `pipeline_steps` has no "who scored this" column.
   A `SELF_REVIEW` entry in `STEP_CONFIG` would write `scores.overall` into `step_history`,
   `loaders.js` lifts that into `pipeline_steps.score`, and every query used to judge this reform
   would then silently mix self-scores with reviewer scores. You would be measuring the reform with
   an instrument the reform broke.
2. **It could escalate against itself.** A step in `STEP_CONFIG` can reach ESCALATE, letting the
   implementer write `ESCALATION.json` and block its own turn-end with no reviewer involved.

So it writes `step_history` directly with `result: "SELF_SCORED"` and uses `self_review_overall`.
`pickScore` yields null for a row with no `overall`, so this row can never be read as a review round.
There is precedent in the record: `result='SELF_PERFORMED_NO_SCORE'` already appears and
`public/step-cells.js` already reasons about it.

**Artifact:** `.aid/pipeline/<task_id>/self-review-<n>.json`, `<n>` matching the DEVELOP round.

```json
{
  "round": 1,
  "self_review_overall": 8.2,
  "dimensions": {
    "security":      { "score": 9,   "evidence": ["src/auth.ts:45", "src/auth.ts:88"] },
    "code_quality":  { "score": 8,   "evidence": ["src/repair.ts:88"] },
    "architecture":  { "score": 8.5, "evidence": ["src/tokens.js:308"] },
    "documentation": { "score": 7,   "evidence": ["src/tokens.js:1"] }
  },
  "worst_finding": "the guard is evaluated at a different granularity than the DELETE it protects",
  "blockers": [
    { "what": "no seam for the clock in snapshot()", "why": "would need a signature change the brief does not cover" }
  ]
}
```

Score against the SAME rubric the reviewer uses, quoted rather than paraphrased:

```
  Security (30%): OWASP Top 10 — any vulnerability = auto-FAIL
  Code Quality (30%): Single responsibility, proper types, no silent catches, no TODO
  Architecture (25%): Tech spec compliance, separation of concerns, dependency direction
  Documentation (15%): File headers, WHY comments, connection tags
```

**Exit condition, and it is NOT "claim 9.5".** Every dimension carries at least one `file:line` of
evidence, `worst_finding` is named, and **either** `self_review_overall >= 9.5` **or** `blockers[]`
is non-empty with a stated reason per blocker.

Forcing the step to claim 9.5 before exiting was considered and rejected. Against measured reality —
8 percent of real reviews clear 9.5, round-1 median 6.1 — a forced claim is a forced lie most of the
time, and the pipeline's first act would be teaching the implementer that the rubric is a formality.
A named gap is information. A coerced 9.5 is noise.

**`worst_finding` does the real work.** Naming the single most likely MAJOR a skeptical reviewer will
raise is the one part that cannot be produced by pattern-matching your own diff approvingly.

**The bias cannot be removed, so measure it.** When CODE_REVIEW round 1 runs, the orchestrator adds
`self_review_overall` to the scores object it hands `gate.mjs`. `recordDecision` persists it and
`scores_raw` makes it queryable, so a rubber stamp becomes a number with a name: the calibration
delta. An isolated agent doing the self-score would be unbiased, but it would simply be round 1 under
another name — costing a full review and saving nothing. The value here is that the implementer holds
information the reviewer does not; the risk is that it grades itself. Only the delta says which won.

**Kill criterion, agreed up front.** Two weeks after this ships: if round-1 average has not moved
materially above 6.1, or the median `self_review_overall - score` delta exceeds about 2.0, delete the
step. It is then a ritual that costs a step and produces a lie.

### DESIGN_REVIEW Step — advisory, and where injectability is decided

**Advisory by explicit decision.** Architecture stays at 25% of the CODE_REVIEW composite and this
step never blocks. Be straight about what that costs: an advisory review cannot stop a bad design
reaching code, so the plateau from architecture findings persists. What it buys is that the
implementer sees the structural problems before the reviewer does, and can fix them before round 1
rather than in round 4.

It also costs less than it looks. The MAJOR cap is weight-independent: an architecture MAJOR caps a
review at 6 whatever architecture's percentage is, so a reweight would only ever have operated inside
the already-clean band.

**Reviewer resolution.** Resolve `configo:architecture-reviewer` if it is available, else
`aid:phase2-techspec-pm-reviewer`. Both are plugin agents addressed by NAME — there is no
`~/.claude/agents/phase2-techspec-pm-reviewer.md` file to fall back to. If neither resolves, log a
warning and SKIP to DEVELOP. Skipping is legitimate here precisely because the step is advisory; a
gated step may never be skipped for a missing reviewer.

**One reviewer, one artifact.** The `phase2-*` designers are authors, not reviewers, and spawning
five of them for a two-surface slice is the over-build this pipeline does not need.

#### `design.md` and the `NON_DETERMINISTIC_INPUTS` table

Injectability is a **design-time** property. No test-fix round can add a seam the design omitted, so
this is the only step where it can still be cheap. `design.md` must carry one row per
non-deterministic input the declared surfaces touch:

```markdown
## NON_DETERMINISTIC_INPUTS

| Input | Kind | Injection seam | seam_token |
|---|---|---|---|
| current time | clock | `snapshot({ now })` takes the instant as a parameter | `now` |
| retry jitter | random | `withRetry(fn, { rng })` | `rng` |
| the verify child process | spawn | `runCheck(check, { spawn })` | `spawn` |
| DB_PATH | env var | `openDb(path)` takes the path, never reads env | `dbPath` |
```

One row per clock, random source, spawned process, network call, filesystem path, environment
variable and timezone. `seam_token` names the **literal parameter** a test will pass, for example
`now` or `clock` — not a description of it, because the `seams` check greps for that token in the
project's tests.

**A clock seam's test set must include one boundary value** — a day boundary or a DST transition.
Both measured bugs of this class were boundary cases: a 04:00 day-boundary failure, and a fixture
that was green at night and red between 10:00 and 16:00. Neither was reachable without a seam, and
neither would have been caught by a mid-afternoon test.

Because this step is advisory, the requirement needs a **check** rather than a gate to have any
force: `qa/pipeline-artifacts.mjs seams` fails when a declared `seam_token` appears in no test file.
Stated ceiling, so nobody mistakes it for more than it is: writing the token in a test satisfies the
grep without injecting anything. It is a low bar on purpose — the measured six-round case had no seam
at all and fails it loudly. Tighten it only if it proves insufficient, and not with static analysis
before then.

### FIX_CODE Step — Full Review Context

When entering FIX_CODE, provide the FULL review result (not just action_required):

```
## Code Review Feedback (iteration N/max)

Overall Score: X.X/10 (need 9.5+ to pass)
  Security:      X/10 — [reviewer note]
  Code Quality:  X/10 — [reviewer note]
  Architecture:  X/10 — [reviewer note]
  Documentation: X/10 — [reviewer note]

Biggest gaps: [from score_justification]

Action Items (priority order):
  1. [CRITICAL] ...
  2. [MAJOR] ...

Focus on the lowest-scoring categories first.
```

**Grep BEFORE you edit, not after.** A finding names one file; the defect usually has siblings. The
measured case ran six rounds, five of them the same shape, because each fix was scoped to the file
the reviewer happened to point at. Search for the pattern first, then fix everything the search
returns in one round.

**Record what you searched, in `.aid/pipeline/<task_id>/fix-<n>.json`** where `<n>` is the fix round.
"Also fix the siblings" is unenforceable advice; a re-runnable command with its recorded output is
checkable. This applies to FIX_TEST_CODE identically.

```json
{
  "round": 3,
  "findings": [{
    "finding_id": "cq-2",
    "pattern": "guard evaluated at a different granularity than the DELETE",
    "grep": "clearSession\(|DELETE FROM .* WHERE session_id",
    "hits_before": ["src/repair.ts:88", "src/rewind.ts:140", "src/prune.ts:62"],
    "fixed": ["src/repair.ts:88", "src/rewind.ts:140"],
    "not_fixed_why": [{"at": "src/prune.ts:62", "why": "per-run table, different granularity by design"}]
  }]
}
```

Three rules make that record checkable rather than decorative:

1. `grep` is non-empty and is **the regex you actually ran**, not a description of it.
2. `hits_before` is that grep's real output, captured before any edit.
3. After fixing, re-running the grep returns only entries that carry a `not_fixed_why`. Every
   `hits_before` entry appears in `fixed` or in `not_fixed_why` — a hit in neither is an unfinished
   round, and the nightly check `qa/pipeline-artifacts.mjs fix-records` fails on it.

There is deliberately no config key for this. Class-level fixing is unconditional, and a
`require_class_level_fix` boolean would be a config for a value that never changes plus an invitation
to switch it off in the run where it matters.

### FIX_TEST_CODE Step — Full Review Context

Same pattern as FIX_CODE but with test review scores:

```
## Test Review Feedback (iteration N/max)

Overall Score: X.X/10 (need 9.5+ to pass)
  Test Quality:      X/10 — [reviewer note]
  Coverage:          X/10 — [reviewer note]
  Independence:      X/10 — [reviewer note]
  Alignment:         X/10 — [reviewer note]
  Production Safety: X/10 — [reviewer note]
  Mock Analysis:     X/10 — [reviewer note]

Biggest gaps: [from score_justification]

Action Items (priority order):
  1. [CRITICAL] ...
  2. [MAJOR] ...

Focus on the lowest-scoring categories first.
```

### Phase 5 Steps

| Step | Action | On PASS | On FAIL |
|------|--------|---------|---------|
| API_TESTS | Run integration test command from config | E2E_TESTS | FIX_API_TESTS |
| FIX_API_TESTS | Fix integration test failures | API_TESTS | loop |
| E2E_TESTS | **Pre-check:** if no E2E tests exist (no playwright config / `e2e/` / `tests/e2e/` / `features/*.feature`), STOP and ask the user via AskUserQuestion: create E2E tests now, or skip E2E for this task (record choice in `state.json` as `e2e_skipped: true`, log in step_summaries). Never run a test command against nothing and call it PASS. Otherwise run `config.test_commands.e2e` + `npm run cucumber` | CERTIFICATION | FIX_E2E_TESTS |
| FIX_E2E_TESTS | Fix E2E/Cucumber failures | E2E_TESTS | loop |
| CERTIFICATION | Run ALL tests (random order), verify coverage, generate report. On CERTIFICATION → DONE, a terminal **RETRO/SYNTHESIS** step runs (detailed in `SKILL.extended.md`): it aggregates `step_summaries` + final scores + AR gap reasons into a short human-readable `.aid/pipeline/<task_id>/retro.md`, INVOKES the existing user-level retro skill (`~/.claude/skills/retro`) to close the loop, and may append a one-line learning to user memory `MEMORY.md`. Report-only — NEVER auto-commits. | DONE | N/A |

---

## How to Spawn Sub-Agents

**CRITICAL: Each sub-agent MUST be spawned as an isolated Agent (sub-agent) using the Agent tool. DO NOT evaluate the code yourself — the whole point is isolated, unbiased review.**

**Path resolution (project → user fallback).** Every `.claude/agents/<name>.md` (agents are FLAT files, one `.md` per agent — there is no `<name>/AGENT-PROMPT.md` layout) and `.claude/skills/reflection/criteria/...` path below is **resolved project-first, then user-level**: if `{{WORKSPACE}}/.claude/<path>` exists use it, else fall back to `~/.claude/<path>` (the user-level default engine). This is what lets the pipeline run in ANY project — the orchestrator, reflection criteria, and the `reflection-agent` / `code-review-agent` / `test-review-agent` prompts all ship at user level and are overridden per-project only when a project provides its own. If neither location has a required agent prompt, skip that step with a logged warning where the step is optional (e.g. VISUAL_QA), or fall back to the user-level `code-review` / `test-driven` skills for review guidance.

**Best-practice standards (how the pipeline knows TDD / review rules).** The methodology the stages follow is resolved **project → engine**:
- **DEVELOP / TDD** follow the TDD standard: prefer a project-level `test-driven` skill (`{{WORKSPACE}}/.claude/skills/test-driven/`) if present (AID projects ship one); else use the **engine-bundled AID standard** at `<this skill>/references/standards/test-driven/` (`SKILL.md` + `SKILL.extended.md` + `references/`: anti-patterns, test-patterns, test-data-factories, integration-testing, review-checklist, test-writing-guide, gui-testing). These cover RED-GREEN-REFACTOR, minimal mocking, realistic data, strong assertions, test independence.
- **Test source:** in an AID project, tests are driven by the PRD / Tech-Spec / Impl-Plan (and Cucumber `.feature` files = acceptance criteria). In a non-AID project those don't exist — derive test targets from the **frozen `brief.md`** (original request + WHY + approved plan). Do NOT try to read `docs/prd/…` when it is absent.
- **CODE_REVIEW** standards = the engine-bundled AID `code-review` skill at `<this skill>/references/standards/code-review/` (a project-level `.claude/skills/code-review/` overrides it); **TEST_REVIEW** = `<this skill>/references/standards/test-driven/references/review-checklist.md` (project `test-driven` skill overrides). **AR passes** use the reflection `criteria/*.yaml`. All of these ship with the engine, so the pipeline carries its own best-practice knowledge in any project.

### When a spawned agent reports no result

Written once because it applies to all five spawn sites: code-review, test-review, visual-qa,
reflection and qa-validator. Added 2026-09-04.

A spawned agent that returns nothing, returns prose instead of JSON, or reports itself idle has
**not produced a bad review — it has produced no review.** Do not score it, do not treat it as FAIL,
and do not enter a fix cycle. Doing so spends one of five cycles on a round that never happened and
erases the delivery failure from the record.

**1. Try to recover the verdict from the transcript before re-spawning.** It is usually on disk even
when delivery failed. Layout, verified against real files:

```
~/.claude/projects/<project-slug>/<session-id>/subagents/
    agent-a<hash>.jsonl        the transcript
    agent-a<hash>.meta.json    {"agentType":..., "description":..., "model":..., "toolUseId":...}
```

`description` is how you tell two concurrent reviewers apart, because it carries the string you
passed at spawn time. The verdict is the `text` block of the **last record with `type: "assistant"`**
in the matching `.jsonl`.

**2. Recovered scores go to `gate.mjs` verbatim.** Never edited, never rounded, never interpreted.
If you had to reason about what a number should be, you did not recover a score — go to step 3.

**3. If nothing is recoverable, record the failure and re-spawn once.**

```
node "$HOME/.claude/skills/pipeline-orchestrator/gate.mjs" --step CODE_REVIEW --scores '{}'
```

That returns ERROR with exit 3 and appends one `result: "ERROR"` row to `step_history`. It consumes
no fix cycle and, having no `overall` key, it cannot enter any score average. Re-spawn the agent
once. If the second attempt also produces nothing, that is an infrastructure problem, not a quality
problem: stop and say so rather than advancing the step.

See also the table in `SKILL.extended.md` under **Sub-Agent Returned No Usable Result**.

### code-review-agent

**Step-by-step execution (follow exactly):**

1. Read `.aid/context.json` → extract task ID + description → this is `{{TASK_CONTEXT}}`
2. Run `git diff --name-only HEAD` → read each changed file's full content → this is `{{CHANGED_FILES}}`

   **Falsify the brief's surface count against this diff before spawning.** If the diff touches more
   distinct top-level source directories than `brief.md` declares surfaces, the declaration was
   false: stop, and re-run `gate.mjs --brief-check` against reality. This is what makes the
   declaration a claim with a mechanical consequence instead of a guess, and it is what stops
   "one surface: the dashboard" from being the cheap way past the cap. The command is already being
   run here, so the falsifier costs nothing.
3. Read relevant section from `docs/tech-spec/` → this is `{{TECH_SPEC_EXCERPT}}`. **In a non-AID project `docs/tech-spec/` won't exist — if it is absent or empty, derive the architectural reference from the frozen `.aid/pipeline/<task_id>/brief.md` (ORIGINAL_REQUEST + STATED_WHY + DEVELOP plan), the same source AR_ACCEPTANCE and qa-validator use, and state in `{{TECH_SPEC_EXCERPT}}` that no formal tech-spec exists so the agent reviews the Architecture category against the brief rather than silently scoring it against nothing. Never review architecture against nothing.**
4. Read `<this skill>/references/standards/code-review/SKILL.md` verbatim (project `.claude/skills/code-review/SKILL.md` if present) → this is `{{CODE_STANDARDS}}`
5. Read `.claude/agents/code-review-agent.md` (project-first, else `~/.claude/agents/code-review-agent.md`)
6. Replace all `{{VARIABLE}}` placeholders with extracted values
7. Spawn the agent:

```
Agent(
  subagent_type: "general-purpose",
  prompt: [the rendered agent .md with all variables replaced],
  description: "Isolated code review — pipeline step",
  model: "opus"
)
```

8. Parse the returned JSON response

**Parse response — the decision is NOT yours to make. Run the gate:**

```bash
node "$HOME/.claude/skills/pipeline-orchestrator/gate.mjs" \
  --step CODE_REVIEW --scores '<the agent's scores object, verbatim JSON>'
```

Act on the EXIT CODE, never on your own reading of the number:

| Exit | Result | Do |
|---|---|---|
| 0 | PASS | advance to AR_DESIGN |
| 1 | FIX | enter FIX_CODE, re-run CODE_REVIEW. The gate already incremented `iterations.code_review` and appended the `step_history` row — never touch counters yourself |
| 2 | ESCALATE | **STOP.** The gate wrote `.aid/pipeline/ESCALATION.json`. Present the decision to the user and wait. Do NOT resolve it yourself, do NOT advance, do NOT log a PASS |
| 3 | ERROR | bad/missing score or config — fix the input; NEVER treat it as a pass |

**Why this is a command and not a rule you follow:** it used to be prose ("compare against the
threshold… after N cycles ESCALATE"), and it was not followed — this workspace's own `step_history`
contains CODE_REVIEW logged `PASS` at **7.9** and **7.6** against a threshold of **9.5**, with no
escalation. A gate an agent can talk itself past is not a gate. `gate.mjs` also enforces
`auto_fail_on_critical_security` (a critical finding escalates regardless of the composite) and
refuses to pass a missing score.

The Stop hook (`dev-pipeline-gate.sh`) blocks every turn-end while an escalation is open, so an
unresolved ESCALATE cannot be quietly skipped. Resolution is the user's decision, recorded with
`gate.mjs --resolve "<reason>"`.

#### Two reviewers, and exactly when

**Run the command, never eyeball the numbers yourself** — the same "prose an agent could talk itself
past" failure this whole gate exists to prevent:

```bash
node "$HOME/.claude/skills/pipeline-orchestrator/gate.mjs" \
  --should-spawn-dual --step CODE_REVIEW
```

Exit 0 → spawn **two** independent reviewers. Exit 1 → spawn **one**. Exit 3 → usage/data error, fix
the input, never guess. The command reads the round and previous score from `state.json` itself
(`--round`/`--prev-score` override only when you have a reason to). This is `shouldSpawnDual` in
`gate.mjs` — plain arithmetic, not a model call: round 1, or any **boundary round** where the previous
score is within `reviewers.dual_within_of_threshold` (default 1.0) of the threshold and a single noisy
sample would decide the gate. Run **one** everywhere else.

The 6.7-to-8.8 middle band is cap-dominated — a second sample there changes nothing and costs double.

**What two reviewers buy, and what they do not.** They do NOT make a 9.5 gate stable: averaging two
samples of the same prompt cuts the standard deviation by only about 1 over root 2, so against the
measured 1.5-point dimension spread the residual is still roughly 1.06. What they buy is the **union
of defects in one round instead of across two.** That is the entire case for the change.

**Cost, and why this is not for every round.** Review and fix steps are already 52 percent of all
pipeline steps. On the six-surface task the hard numbers were `estimated_cost_usd: 20.88`, of which
eight CODE_REVIEW rounds were $6.63 and six TEST_REVIEW rounds were $6.72 — review was $13.35 of
$20.88. Doubling reviewer spend unrestricted would trip `cost_limits.max_per_run_usd` into ESCALATE
more often, and a cost-brake escalation is a WORSE round than a review round because it needs a human.
On the restriction above the arithmetic is favourable: two reviewers across three rounds is about six
reviewer calls where one reviewer across eight rounds was eight.

**Spawn shape.** Two `Agent(...)` calls with the **identical rendered prompt** and distinct
`description` values — "Isolated code review A — pipeline step" and "… B …". Isolation is automatic:
they are separate sub-agents with no shared context. The `.meta.json` beside each transcript carries
`description`, which is how the recovery procedure tells them apart.

**Two rules, both absolute.** Do not show A's output to B. Do not summarise, round or reconcile either
one before merging — `mergeReviews` takes both **verbatim**:

```bash
node "$HOME/.claude/skills/pipeline-orchestrator/gate.mjs" --step CODE_REVIEW   --scores   '<reviewer A's JSON, verbatim>'   --scores-b '<reviewer B's JSON, verbatim>'
```

The merge is in code, not in your judgement, because you are the party that wants to advance and
arbitrating two disagreeing reviews is not a call the interested party gets to make. It takes the
severity cap from the **union** of findings and the mean only underneath it, so a clean 9.6 merged
with a 6.0 carrying one real MAJOR yields 6.0 and not 7.8. It also emits `reviewers`, `spread` and
`reviewers_used`, so judge variance stops being an anecdote recoverable only from transcripts.

**If one reviewer produces nothing**, the merge uses the survivor as-is with `reviewers_used: 1` and
never averages against a phantom. If NEITHER produced a score, that is ERROR — see
**When a spawned agent reports no result**.

- If cost limit hit during iteration → ESCALATE (user decides: continue or stop)
- Store FULL response (including `scores`, `score_justification`, `biggest_gaps`) in `last_review_result`
- **On iteration 1 only**, also add `"self_review_overall": <the number SELF_REVIEW claimed>` to the
  scores object. It carries no weight in any decision — `decide()` never reads it — and exists so the
  calibration delta between what the implementer claimed and what the reviewer scored is queryable
  from `scores_raw` instead of recoverable only from transcripts.
- Add one key to the scores object handed to `gate.mjs`: `"top_finding": "<pattern of the highest-severity finding>"`.
  A short phrase naming the defect SHAPE, not the file it was found in. `recordDecision` persists
  `scores` verbatim into `pipeline_steps.scores_raw`, where `json_extract` can read it, so this one
  string turns "the same defect class for six rounds running" from an anecdote into a query.
- **Do NOT append to `step_history` yourself. `gate.mjs --step` has already written this row**, with
  the round number, the cap, the threshold, the scores you passed it, and a `gate.mjs: ` note. A second
  append double-counts the round: measured on `status-safety-cues`, every round produced two rows ~120 ms
  apart and the series read as 12 rounds where 6 happened. Worse, rewriting the whole file from a stale
  in-memory copy can DROP the gate's append — saas TEST_REVIEW round 1 exists in the gate's event log and
  is absent from `state.json`.
  The gate's allowed values are `PASS`, `FIX`, `ESCALATE`, `ERROR` — its word, not a summary of it.
  `ERROR` means the review did not run (no scores recovered); it consumes no fix cycle and carries no
  `overall`, so it never lands in a score average. `FAIL` is not a value the gate emits.

### test-review-agent

**Step-by-step execution:**

1. Read `.aid/context.json` → extract task context → `{{TASK_CONTEXT}}`
2. Read all production source files modified in current task → `{{IMPLEMENTATION_FILES}}`
3. Read corresponding test files → `{{TEST_FILES}}`
4. Run test command, capture output → `{{TEST_RESULTS}}`
5. Read `.claude/agents/test-review-agent.md` (project-first, else `~/.claude/agents/test-review-agent.md`), replace variables
6. Spawn:

```
Agent(
  subagent_type: "general-purpose",
  prompt: [rendered agent .md],
  description: "Isolated test review — pipeline step",
  model: "opus"
)
```

7. Parse the returned JSON response

**Parse response — the decision is NOT yours to make. Run the gate:**

```bash
node "$HOME/.claude/skills/pipeline-orchestrator/gate.mjs" \
  --step TEST_REVIEW --scores '<the agent's scores object, verbatim JSON>'
```

Act on the EXIT CODE, never on your own reading of the number:

| Exit | Result | Do |
|---|---|---|
| 0 | PASS | advance to PHASE_GATE |
| 1 | FIX | enter FIX_TEST_CODE, re-run TEST_REVIEW. The gate already incremented `iterations.test_review` and appended the `step_history` row |
| 2 | ESCALATE | **STOP.** The gate wrote `.aid/pipeline/ESCALATION.json`. Present the decision to the user and wait. Do NOT resolve it yourself, do NOT advance, do NOT log a PASS |
| 3 | ERROR | bad/missing score or config — fix the input; NEVER treat it as a pass |

The threshold is `config.thresholds.test_review_pass` and the cap is `config.max_iterations.test_review`
— the gate reads both, so do not re-derive them here. Running it is also what puts this step's round,
limit and mark to beat on the record: nothing else writes them, so a step judged by prose instead shows
blanks forever afterwards. (Corrected 2026-09-06: they used to reach the Current Loops view ONLY via the
gate's event log, because the dashboard loader discarded the round, cap and threshold the gate had
already written into `step_history`. It now reads them from the entry, so both paths carry the same
numbers and neither invents one from today's config.)
- If cost limit hit during iteration → ESCALATE (user decides: continue or stop)
- Store FULL response (including `scores`, `score_justification`, `biggest_gaps`) in `last_review_result`
- Add `"top_finding": "<pattern of the highest-severity finding>"` to the scores object handed to
  `gate.mjs`, exactly as CODE_REVIEW does, so a repeated test defect class is queryable.
- **Do NOT append to `step_history` yourself. `gate.mjs --step` has already written this row**, with
  the round number, the cap, the threshold, the scores you passed it, and a `gate.mjs: ` note. A second
  append double-counts the round: measured on `status-safety-cues`, every round produced two rows ~120 ms
  apart and the series read as 12 rounds where 6 happened. Worse, rewriting the whole file from a stale
  in-memory copy can DROP the gate's append — saas TEST_REVIEW round 1 exists in the gate's event log and
  is absent from `state.json`.
  The gate's allowed values are `PASS`, `FIX`, `ESCALATE`, `ERROR` — its word, not a summary of it.

### visual-qa-agent

**Prerequisites check (before spawning):**
1. Verify the agent prompt resolves: resolve `.claude/agents/visual-qa-agent.md`
   **project-first then user-level** (`{{WORKSPACE}}/.claude/agents/visual-qa-agent.md`,
   else `~/.claude/agents/visual-qa-agent.md`). If it does NOT resolve in either location
   → log a warning and SKIP VISUAL_QA → advance to TEST_REVIEW (consistent with the documented
   optional-step behavior). Normally the path resolves (a real prompt ships at user level).
2. Verify dev server is running: `curl -s -o /dev/null -w "%{http_code}" {{TARGET_URL}}` → expect 200
3. Verify Chrome DevTools MCP is available: check for `mcp__chrome-devtools__navigate_page` tool
4. If any of these fails → skip VISUAL_QA with warning, advance to TEST_REVIEW

**Step-by-step execution:**

1. Read `.aid/context.json` → `{{TASK_CONTEXT}}`
2. Read `config.visual_qa.dev_server_url` (default: `http://localhost:5173`) → `{{TARGET_URL}}`
3. Read `step_summaries.DEVELOP` from state.json → `{{IMPLEMENTATION_SUMMARY}}`
4. List routes/pages from changed files or tech spec → `{{PAGES_TO_TEST}}`
5. Read the resolved `visual-qa-agent.md`, replace variables
6. Spawn:

```
Agent(
  subagent_type: "general-purpose",
  prompt: [rendered agent .md],
  description: "Isolated visual QA — pipeline step",
  model: "opus"
)
```

7. Parse the returned JSON response

**Parse response — the decision is NOT yours to make. Run the gate:**

```bash
node "$HOME/.claude/skills/pipeline-orchestrator/gate.mjs" \
  --step VISUAL_QA --scores '<the agent's scores object, verbatim JSON>'
```

Act on the EXIT CODE, never on your own reading of the number:

| Exit | Result | Do |
|---|---|---|
| 0 | PASS | advance to TEST_REVIEW |
| 1 | FIX | enter FIX_VISUAL, re-run VISUAL_QA. The gate already incremented `iterations.visual_qa` |
| 2 | ESCALATE | **STOP.** The gate wrote `.aid/pipeline/ESCALATION.json`. Present the decision to the user and wait. Do NOT resolve it yourself, do NOT advance, do NOT log a PASS |
| 3 | ERROR | bad/missing score or config — fix the input; NEVER treat it as a pass |

A `verdict: "FAIL"` with a passing number is still a FAIL: send it to FIX_VISUAL regardless of the exit
code. The number is what the gate bounds; the verdict is the reviewer's own veto.
The threshold is `config.thresholds.visual_qa_pass` and the cap is `config.max_iterations.visual_qa`.
**Increment `iterations.visual_qa`** — without that counter the gate reads it as 0 forever, so the cap
can never be reached and this step could return FIX indefinitely without ever escalating.
- Store FULL response (including `scores`, `lighthouse`, `issues`, `testing_summary`) in `last_review_result`
- **Do NOT append to `step_history` yourself** — VISUAL_QA is a gated step, so `gate.mjs --step VISUAL_QA`
  has already written the row. Pass `lighthouse` inside `--scores` if you want it on the record; the gate
  persists the scores object verbatim. `PASS|FAIL` is also not the gate's vocabulary: it emits `PASS`,
  `FIX`, `ESCALATE`, `ERROR`.

### FIX_VISUAL Step — Full Review Context

When entering FIX_VISUAL, provide the FULL visual review result:

```
## Visual QA Feedback (iteration N/max)

Overall Score: X.X/10 (need 7.0+ to pass)
  Design Quality:  X/10 — [reviewer observations]
  Originality:     X/10 — [reviewer observations]
  Craft:           X/10 — [reviewer observations]
  Functionality:   X/10 — [reviewer observations]

Lighthouse: Accessibility X/100 | SEO X/100 | Best Practices X/100

Testing Summary: X screenshots, X elements tested, X viewports, X pages

Biggest gaps: [from score_justification]

Action Items (priority order):
  1. [CRITICAL] ...
  2. [MAJOR] ...

Focus on functionality issues first, then craft, then design quality.
```

---

### qa-validator-agent

PHASE_GATE spawns the `qa-validator-agent` via its prompt file (NOT an inline hardcoded prompt),
resolved **project-first then user-level** — the same resolution code-review-agent / test-review-agent
use (see "Path resolution" above).

**Step-by-step execution (follow exactly):**

1. Read `.aid/context.json` → extract task ID + description → this is `{{TASK_CONTEXT}}`
2. **Resolve the acceptance criteria (criteria source is DECOUPLED from AID):**
   - If `.aid/qa/<task_id>.yaml` EXISTS (AID project) → read it verbatim → this is `{{ACCEPTANCE_CRITERIA}}`.
   - If it is ABSENT (non-AID project) → derive the acceptance criteria from the frozen
     `.aid/pipeline/<task_id>/brief.md` (`ORIGINAL_REQUEST` + `STATED_WHY` + DEVELOP plan — the SAME
     source `AR_ACCEPTANCE` uses) → this is `{{ACCEPTANCE_CRITERIA}}`. Never validate against nothing.
3. Run `git diff --name-only HEAD` → read each changed file's full content → this is `{{CHANGED_FILES}}`
4. Resolve `.claude/agents/qa-validator-agent.md` **project-first then user-level**
   (`{{WORKSPACE}}/.claude/agents/qa-validator-agent.md`, else
   `~/.claude/agents/qa-validator-agent.md`). Read it.
5. Replace all `{{VARIABLE}}` placeholders — `{{TASK_CONTEXT}}`, `{{ACCEPTANCE_CRITERIA}}`,
   `{{CHANGED_FILES}}` — with the extracted values.
6. Spawn the agent:

```
Agent(
  subagent_type: "general-purpose",
  prompt: [the rendered agent .md with all variables replaced],
  description: "QA validation — pipeline PHASE_GATE",
  model: "opus"
)
```

7. Parse the returned JSON response.

**Parse response — the decision is NOT yours to make. Run the gate:**

```bash
node "$HOME/.claude/skills/pipeline-orchestrator/gate.mjs" \
  --step PHASE_GATE --scores '<the validator's verdict object, verbatim JSON>'
```

PHASE_GATE is **pass/fail, not scored** — it has no threshold and no mark to beat. The gate accepts
`{"verdict":"PASS"}`, `{"can_proceed":true}` or `{"passed":true}`; anything else is a fail.

Act on the EXIT CODE:

| Exit | Result | Do |
|---|---|---|
| 0 | PASS | advance to AR_ACCEPTANCE (AR-3); AR_ACCEPTANCE on DONE → Phase 5 (API_TESTS) |
| 1 | FIX | return to DEVELOP (re-examine approach). The gate already incremented `iterations.phase_gate_reexamine` |
| 2 | ESCALATE | **STOP.** The gate wrote `.aid/pipeline/ESCALATION.json`. Present the decision to the user and wait |
| 3 | ERROR | bad/missing verdict or config — fix the input; NEVER treat it as a pass |

The cap is `config.max_iterations.phase_gate_reexamine`; the gate reads it. This re-examine cap is
**DISTINCT** from AR-3's `max_acceptance_rounds`, which bounds only the AR_ACCEPTANCE-gap re-entry into
DEVELOP — not PHASE_GATE failures. The cost limit remains an additional safety brake.

### autoresearch runner (AR_DESIGN / AR_FUNCTION / AR_ACCEPTANCE)

These three steps do NOT spawn a review agent that returns a single JSON verdict. Instead they
invoke the shared **autoresearch runner skill** in the matching mode, which runs the bounded
keep/revert loop and itself spawns the harness agents — the subagent named `reflection-agent`
(prompt loaded from `{{WORKSPACE}}/.claude/agents/reflection-agent.md`, else `~/.claude/agents/reflection-agent.md`), and for AR-3
the phase5-acceptance-validator / phase4-intent-validator:

| Step | Mode | Prompt file | On success | On gap/incomplete |
|------|------|-------------|------------|-------------------|
| AR_DESIGN | `design` | `program.ar-design.md` | advance to TDD | (bounded loop; revert non-improving edits) |
| AR_FUNCTION | `function` | `program.ar-function.md` | advance to VISUAL_QA | (bounded loop; test red => auto-revert) |
| AR_ACCEPTANCE | `acceptance` | `program.ar-acceptance.md` | DONE → advance to Phase 5 | gap → re-enter DEVELOP (bounded by `max_acceptance_rounds`, else ESCALATE) |

**After each AR step:**
- Read the runner's final composite scores from `.aid/pipeline/autoresearch/<task_id>/results.tsv`.
- Log to `step_history`: `{ "step": "AR_DESIGN|AR_FUNCTION|AR_ACCEPTANCE", "task_id": "<this run's task_id>", "result": "PASS|GAP", "scores": {...}, "timestamp": "..." }`.
  The AR steps are NOT in `STEP_CONFIG`, so the gate never records them and this append is correct — it is
  the one place the orchestrator still writes the array. **`task_id` is required**: without it the dashboard
  loader can only attribute the whole accumulated array to whatever task is current at ingest time, which
  is what produced 259 surplus rows (34% of `pipeline_steps`) before 2026-09-06.
- **CRITICAL — HOOK-SAFETY.** The `dev-pipeline-gate.sh` Stop hook re-blocks when the newest source
  mtime > `state.json` mtime. A rollback via `cp <snapshot> <file>` sets the source mtime to NOW, and
  the plateau stop often fires right after a run of REVERTS — so the last disk write is frequently a
  revert, not a kept edit. THEREFORE on stop the step MUST: (1) FIRST restore the editable set to the
  best-kept version, then (2) WRITE `state.json` **UNCONDITIONALLY as the FINAL action — after the last
  source mutation of ANY kind (kept edit, revert/restore cp, or crash restore)**. Update `last_updated`
  and persist `state.json` as the final write of the step. If `state.json` is not the newest write, the
  hook will wrongly re-block.
- The runner never auto-commits and never runs destructive git; rollback is via snapshot copies only.

---

## State Management

### Initialize Pipeline

When `/pipeline` is invoked:

0. **Intent check (do this first).** Confirm this is an IMPLEMENTATION task with a code/test deliverable. If the approved plan / frozen `brief.md` describes pure analysis, research, investigation, or a report with NO code deliverable, do NOT initialize the pipeline — there is nothing for DEVELOP→CODE_REVIEW to act on. Stay advisory-only and set `SKIP_PIPELINE_GATE=1` for the turn. This backs the start-hook's advisory INTENT GATE with an orchestrator-side check.
1. Read `.aid/pipeline/config.json` for settings. **If it does not exist (non-AID project, or first run): create `.aid/pipeline/` and copy the user-level default `~/.claude/skills/pipeline-orchestrator/config.default.json` into `.aid/pipeline/config.json`, then continue.** Do NOT escalate for a missing config — bootstrap it. (The default carries the caps + `autoresearch` block + thresholds; the project may edit it afterward.)
2. Read `.aid/context.json` for current task
3. Create `.aid/pipeline/state.json`:

```json
{
  "$schema": "aid-pipeline-state-v2",
  "pipeline_status": "running",
  "current_phase": 4,
  "current_step": "DEVELOP",
  "current_task_id": "[from context.json]",
  "started_at": "[ISO-8601 now]",
  "last_updated": "[ISO-8601 now]",
  "iterations": {
    "code_review": 0,
    "test_review": 0,
    "visual_qa": 0,
    "phase_gate_reexamine": 0,
    "test_fix": 0,
    "api_fix": 0,
    "e2e_fix": 0,
    "ar_design": 0,
    "ar_function": 0,
    "ar_acceptance_rounds": 0
  },
  "cost": {
    "total_input_tokens": 0,
    "total_output_tokens": 0,
    "estimated_cost_usd": 0.00,
    "per_step": {}
  },
  "step_summaries": {},
  "last_review_result": null,
  "step_history": []
}
```

4. **Freeze the config this run will be judged by.** Copy `.aid/pipeline/config.json` to
   `.aid/pipeline/<task_id>/config.frozen.json` **once**, at kickoff. If it already exists (resume
   case), DO NOT overwrite it.

   Why: `config.json` is per repo ROOT and mutable, so it is not a record of how any past run was
   judged. The escalation remedy in `gate.mjs` even tells the human to *lower the threshold in
   config.json* and resume — after which the file no longer describes the rounds already scored. One
   run's thresholds were rewritten two days after it finished, and its own history holds `PASS` at
   **7.9** and **7.6** against a threshold of **9.5**. Because nothing froze the values, the Current
   Loops view cannot show what those rows were judged against and correctly refuses to guess. A frozen
   copy makes the mark and the cap run-local facts, so they can be displayed later without inventing
   them.

5. **Freeze the immutable Task Brief** (compaction-proofing — do this NOW, at kickoff, while the original prompt is still in context).

   Write `.aid/pipeline/<task_id>/brief.md` **once**. If the file already exists (resume case), DO NOT overwrite it — read it. This file is the durable source of intent that survives context compaction and long runs; every later step (especially **AR_ACCEPTANCE**) reads intent from here, never from conversation memory.

   **Mechanical immutability:** `dev-pipeline-gate.sh` now records a SHA-256 of `brief.md` on first freeze and surfaces a loud warning if a later `brief.md` differs from the recorded hash.

   ```markdown
   ---
   task_id: <id>
   frozen_at: <ISO-8601 now>        # immutable after first write
   source: conversation | prd | user-provided
   prd_ref: <path to docs/prd/… or "">
   tech_spec_ref: <path to docs/tech-spec/… or "">
   impl_plan_ref: <path to docs/impl-plan/… or "">
   acceptance_criteria_ref: .aid/qa/<task_id>.yaml
   surfaces:                        # REQUIRED. See "Declaring surfaces" below.
     - name: <what a user can point at>
       path: <the primary file or directory it lives in>
   ---

   ## ORIGINAL_REQUEST (verbatim — never edit)
   <the first user message that initiated this feature, VERBATIM — not paraphrased>

   ## STATED_WHY (exact text — never edit)
   <the business/user WHY established for this feature>

   ## DEVELOP PLAN (snapshot at kickoff)
   <the agreed implementation plan, or a link to docs/impl-plan; the WHAT/HOW the build follows>
   ```

   Capture order (never fabricate intent):
   - If `original_request` / `stated_why` are already persisted (existing `brief.md`, or an existing PRD's problem/why) → use those (`source: prd`).
   - Else capture them VERBATIM from the current conversation's first user message + the established WHY (`source: conversation`).
   - If neither is available (e.g. `/pipeline` invoked cold with no prompt and no PRD) → **ESCALATE: ask the user for the original request + WHY before proceeding.** A pipeline with no frozen intent cannot be accepted by AR-3.

5a. **Scope-check the brief BEFORE freezing it.** Draft to `brief.draft.md`, check it, and only on
   exit 0 write `brief.md` and let the hook record the SHA. The order is load-bearing: the hook
   records `brief.sha256` on first freeze, so a check that ran afterwards would be demanding edits to
   an immutable, hash-pinned file.

   ```bash
   node "$HOME/.claude/skills/pipeline-orchestrator/gate.mjs"      --brief-check .aid/pipeline/<task_id>/brief.draft.md
   ```

   | Exit | Meaning | What to do |
   |---|---|---|
   | 0 | within `thresholds.max_surfaces` | rename the draft to `brief.md` and continue |
   | 2 | too many surfaces — `ESCALATION.json` written, Stop hook blocks | split the task into one brief per surface, or `gate.mjs --resolve "<why it cannot be split>"` |
   | 3 | no `surfaces:` block, an inline value, or a surface missing its `path` | fix the declaration — an undeclared brief has not been scope-checked, and that is not a pass |

   **Declaring surfaces.** A surface is **one thing a user can point at and say "this changed"**: a
   route, page or tab; a CLI command or flag; an API endpoint; a background job; an instrumentation
   tier; a file format. Refactors, helpers, types, tests and config plumbing are **not** surfaces.

   **Why the cap exists, and why it is not negotiable per-round.** Every task that has ever reached
   9.5 was one surface. The two that never reached it carried six each. The mechanism is not
   mysterious: any single MAJOR finding caps the whole review at 6, and MAJOR-eligible defect count
   scales with how many surfaces the diff touches. A wide slice cannot pass a 9.5 gate however many
   fix rounds it is given, and the rounds get spent proving that. Splitting is cheaper than iterating.

   The declaration is **yours to make and the diff's to falsify** — see step 2 of the CODE_REVIEW
   spawn. Do not ask a sub-agent to judge the width; width is the thing being policed, and the party
   that wants to advance is the wrong one to rule on it.

6. Also mirror the verbatim `original_request` and `stated_why` into `.aid/context.json` (so existing reflection tooling can read them from disk too), but `brief.md` is the authoritative immutable copy.

### Update State on Transitions

After EACH step transition:

1. Update `current_step` to new step
2. Increment relevant iteration counter
   - **RESET on DEVELOP re-entry (backward boundary).** On any transition INTO DEVELOP from PHASE_GATE (FAIL re-examine) OR AR_ACCEPTANCE (gap re-enter), reset the INNER Phase-5 counters `iterations.code_review`, `iterations.test_fix`, `iterations.test_review`, and `iterations.ar_design` to 0 (mirrors the forward "Reset Phase 5 iteration counters" rule in `SKILL.extended.md` ~line 188, so the boundary is symmetric). The OUTER counters `iterations.phase_gate_reexamine` and `iterations.ar_acceptance_rounds` **PERSIST** — they are the real loop bound that guarantees termination, and must NOT be reset here.
3. Append to `step_history`: `{ "step": "...", "result": "PASS|FAIL", "scores": {...}, "timestamp": "..." }`
4. Update `last_updated`
5. If sub-agent ran, store result in `last_review_result`
6. **Update cost tracking** (see Cost Tracking section)
7. **Write step summary** (see Context Management section)
8. Write updated state to `.aid/pipeline/state.json`

### Resume on Session Restart

When loading a project with an active pipeline:

1. Read `.aid/pipeline/state.json`
2. If `pipeline_status: "running"`, resume from `current_step`
3. **Reconcile mtime vs content (avoid false re-block on resume).** If the newest source mtime
   > `state.json` mtime BUT the on-disk content of the editable set EQUALS the best-kept / baseline
   snapshot (a benign post-restore state — restores now use `cp -p`, so a stale-but-identical restore
   can still bump mtime), treat the state as CLEAN: do NOT force a false re-block or re-enter the last
   step. Otherwise (content differs from the best-kept snapshot) proceed normally and let the step /
   Stop-hook freshness logic run as usual.
4. Read `step_summaries` to restore context without replaying full conversation
5. Display: "Pipeline active — resuming from [current_step] for task [task_id] ($[cost] spent)"

**Note:** `dev-pipeline-gate.sh` records a SHA-256 of `brief.md` on first freeze and surfaces a loud warning on resume if the current `brief.md` differs from the recorded hash (mechanical immutability).

---

## Cost Tracking

### Why
The article "Harness Design for Long-Running Apps" (Anthropic, March 2026) shows multi-agent runs can cost $50-200. Without cost visibility, pipeline runs can silently burn through budgets.

### How to Track

After EACH sub-agent call (CODE_REVIEW, TEST_REVIEW, PHASE_GATE), update cost:

1. Extract token counts from the sub-agent's response metadata (or estimate: ~4K input + ~2K output per review)
2. Calculate cost: `(input_tokens / 1M * pricing.input_per_mtok) + (output_tokens / 1M * pricing.output_per_mtok)`
3. Update `cost.total_input_tokens`, `cost.total_output_tokens`, `cost.estimated_cost_usd`
4. Add step entry: `cost.per_step[step_name] = { input_tokens, output_tokens, cost_usd, timestamp }`

### Cost Limits

Read limits from `config.cost_limits`:

| Threshold | Action |
|-----------|--------|
| `cost >= warn_at_usd` | Display: "Cost warning: $X.XX spent (limit: $Y.YY)" |
| `cost >= max_per_run_usd` | ESCALATE: "Pipeline cost limit reached ($X.XX / $Y.YY). Continue? (y/n)" |

Cost escalation uses the same protocol as iteration escalation — user can resume, override, or abort.

### Display in Pipeline Status

Include cost in all pipeline displays:

```
Pipeline: [task_id] | Phase [4|5] | Cost: $X.XX / $Y.YY
[=====>-----------] Step: CODE_REVIEW (iteration 2/3)
```

---

## Context Management

### Why
Long pipeline runs accumulate context — after DEVELOP + CODE_REVIEW + FIX_CODE + CODE_REVIEW (retry) + TDD + TEST_REVIEW, the conversation is huge. The article calls this "context degradation" — models lose coherence as context fills. Worse, the harness may **compact** the conversation mid-run, discarding the original prompt and WHY. Anything the pipeline needs later must live **on disk**, not in conversation memory.

### Task Brief (immutable intent record)

`.aid/pipeline/<task_id>/brief.md` (frozen at Initialize, step 4) holds the **verbatim ORIGINAL_REQUEST, the STATED_WHY, and the DEVELOP plan**. It is written once and never overwritten. This is what makes **AR_ACCEPTANCE** correct: AR-3 must validate the delivered feature against the *original* ask, and a mid-run compaction would otherwise erase it. AR-3 reads intent from `brief.md`, and **escalates loudly** if it is missing rather than validating against a paraphrase.

**Re-hydrate from disk at every step entry.** Each step (and especially any step entered after a compaction or session resume) must reconstruct what it needs from disk — `brief.md` for intent, `state.step_summaries` for prior-step outcomes, `state.json` for counters — and must NOT assume the original prompt or earlier results are still in the conversation. Never silently fall back to a paraphrase or a guess: if `brief.md` is absent, escalate.

### Step Summaries

After each step completes, write a structured summary to `state.step_summaries`:

```json
{
  "step_summaries": {
    "DEVELOP": "Implemented auth middleware for /api/v1/users. Files: src/middleware/auth.ts, src/routes/users.ts. 142 lines added.",
    "CODE_REVIEW_1": "FAIL (5.8/10). Security: 4 (SQL injection auth.ts:45). Quality: 7. Docs: 5. Arch: 7.",
    "FIX_CODE_1": "Fixed SQL injection (parameterized query). Added WHY comments to auth.ts.",
    "CODE_REVIEW_2": "PASS (7.6/10). Security: 8. Quality: 7. Docs: 7. Arch: 8.",
    "TDD": "12 tests written. 11 pass, 1 fail (timeout on async test). Coverage: 78%."
  }
}
```

### How Summaries Prevent Context Degradation

1. **On session resume:** Read `step_summaries` instead of replaying full conversation
2. **On FIX steps:** Show the summary + last review result, not the entire review history
3. **On escalation:** Build the escalation summary from `step_summaries`, not conversation
4. **Key rule:** Each summary is max 2-3 sentences. Include: what happened, key files, score if applicable

### What Goes in a Summary

| Step Type | Summary Contains |
|-----------|-----------------|
| DEVELOP | Files created/modified, lines added, what was implemented |
| CODE_REVIEW | PASS/FAIL, overall score, per-category scores, key issues, cycle count (max 5) |
| FIX_CODE | What was fixed, which categories improved |
| AR_DESIGN | Baseline→final composite, kept/reverted count, top kept edits, KPI dims (struct/loudness/naming/docs) |
| TDD | Tests written, pass/fail count, coverage %, iteration count (max 5) |
| TEST_REVIEW | PASS/FAIL, overall score, per-category scores, key issues |
| FIX_TEST_CODE | What was fixed, which tests added/changed |
| AR_FUNCTION | Baseline→final composite, Tier-1 gate status (tests/coverage/silent-paths), kept/reverted count |
| PHASE_GATE | PASS/FAIL, which criteria passed/failed |
| AR_ACCEPTANCE | Round count (max_acceptance_rounds), pass_rate, why_alignment, blockers, DONE or re-entered DEVELOP |
| API/E2E_TESTS | Pass/fail count, which tests failed |

---

## Escalation Protocol

When any step hits its max iteration count:

1. Set `pipeline_status: "ESCALATED"` and `current_step: "ESCALATED"`
2. Present summary to user:

```
Pipeline Escalated: [step_name] exceeded max iterations ([count]/[max])

Issues from last review:
[List action_required from last_review_result]

Options:
1. /pipeline resume — Reset counter for this step, try again
2. /pipeline override — Skip this step (with documented justification)
3. /pipeline reset — Reset all counters, restart from DEVELOP
```

3. Wait for user decision before proceeding

---

## Pipeline Display

Show pipeline progress at each step transition:

```
Pipeline: [task_id] | Phase [4|5]
[=====>-----------] Step: CODE_REVIEW (iteration 2/3)

Last result: FAIL — 1 CRITICAL (SQL injection), 1 MAJOR (missing auth)
Action: Fixing issues from code review...
```

---

## Configuration

Read from `.aid/pipeline/config.json`:

| Setting | Default | Purpose |
|---------|---------|---------|
| `reviewers.count_first_round` | 2 | Independent reviewers to spawn on round 1, where the defect set is largest. Merged by `gate.mjs --scores-b`, cap from the union then mean underneath |
| `reviewers.dual_within_of_threshold` | 1.0 | Also spawn two when the previous score is within this of the threshold, i.e. a boundary round where one noisy sample decides a gate. The cap-dominated middle band gets one reviewer |
| `thresholds.max_surfaces` | 2 | Max surfaces one brief may declare, enforced by `gate.mjs --brief-check` before the freeze (ESCALATE above it). Frozen per-run into `config.frozen.json`, so a run's own scope bar is auditable |
| `max_iterations.code_review` | 5 | Max CODE_REVIEW→FIX_CODE cycles (HARD CAP — then ESCALATE) |
| `max_iterations.test_review` | 5 | Max TEST_REVIEW→FIX_TEST_CODE cycles (HARD CAP — then ESCALATE, mirrors CODE_REVIEW) |
| `max_iterations.phase_gate_reexamine` | 5 | Max PHASE_GATE-FAIL→DEVELOP re-examine rounds (HARD CAP — then ESCALATE; DISTINCT from AR-3 `max_acceptance_rounds`) |
| `max_iterations.test_fix` | 5 | Max test fix attempts (unscored — needs hard limit) |
| `max_iterations.visual_qa` | 5 | Max VISUAL_QA→FIX_VISUAL cycles (gate.mjs increments `iterations.visual_qa` on every FIX; the agent never touches counters) |
| `max_iterations.api_fix` | 5 | Max API test fix attempts (unscored) |
| `max_iterations.e2e_fix` | 5 | Max E2E test fix attempts (unscored) |
| `autoresearch.kpi_target` | 9.5 | AR quality-score target (0–10) for AR_DESIGN / AR_FUNCTION |
| `autoresearch.ar_design.max_iterations` | 15 | AR-1 iteration cap (shipped default; overridable per project) |
| `autoresearch.ar_design.max_consecutive_reverts` | 5 | AR-1 plateau cap (shipped default; overridable per project) |
| `autoresearch.ar_function.max_iterations` | 15 | AR-2 iteration cap (shipped default; overridable per project) |
| `autoresearch.ar_function.max_consecutive_reverts` | 5 | AR-2 plateau cap (shipped default; overridable per project) |
| `autoresearch.ar_function.internal_rounds` | 2 | AR-2 internal refine rounds before official scoring |
| `autoresearch.ar_acceptance.max_acceptance_rounds` | 2 | AR-3 outer DEVELOP-re-entry round cap (then ESCALATE) |
| `autoresearch.ar_acceptance.pass_rate_target` | 90 | AR-3 acceptance pass-rate target (%) |
| `test_commands.unit` | `npm test` | Unit test command |
| `test_commands.integration` | `npm test -- --testPathPattern=integration` | Integration test command |
| `test_commands.e2e` | `npx playwright test` | E2E test command |
| `test_commands.cucumber` | `npm run cucumber` | Cucumber test command |
| `test_commands.coverage` | `npm test -- --coverage` | Coverage report command |
| `thresholds.code_review_pass` | 9.5 | Minimum code review score (1-10) |
| `thresholds.test_review_pass` | 9.5 | Minimum test review score (1-10) |
| `thresholds.visual_qa_pass` | 7.0 | Minimum visual QA score (1-10) |
| `thresholds.auto_fail_on_critical_security` | true | Auto-fail on security issues |
| `thresholds.min_coverage_percent` | 80 | Minimum test coverage % |
| `cost_limits.warn_at_usd` | 25.00 | Show warning when cost exceeds this |
| `cost_limits.max_per_run_usd` | 50.00 | Escalate when cost exceeds this |
| `cost_limits.pricing.model` | `claude-opus-4-8` | Model whose published rate the pricing reflects (provenance for the rates below) |
| `cost_limits.pricing.input_per_mtok` | 5.00 | $/million input tokens (claude-opus-4-8 — verified from the Claude model catalog) |
| `cost_limits.pricing.output_per_mtok` | 25.00 | $/million output tokens (claude-opus-4-8 — verified from the Claude model catalog) |
| `visual_qa.dev_server_url` | `http://localhost:5173` | URL of running dev server for visual QA |
| `visual_qa.enabled` | true | Enable/disable visual QA step |
| `visual_qa.skip_if_no_ui_changes` | true | Skip if no JSX/TSX/CSS files changed |
| `auto_advance_phase` | true | Auto-advance from Phase 4 to 5 |

**Counter reset scoping.** The INNER Phase-4 counters (`code_review`, `test_fix`, `test_review`, `ar_design`) are reset to 0 on every entry INTO DEVELOP — both forward (kickoff) and backward (PHASE_GATE FAIL re-examine / AR_ACCEPTANCE gap re-enter, see "Update State on Transitions" and `SKILL.extended.md` ~line 188). The OUTER counters `phase_gate_reexamine` and `ar_acceptance_rounds` PERSIST across DEVELOP re-entries — they bound the backward loops and guarantee termination, so resetting them would break the termination guarantee.
