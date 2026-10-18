---
name: aid-update-kb
description: >
  Apply one targeted, human-confirmed change to the Knowledge Base. Use this skill when you
  know what changed and which part of the KB should reflect it, and you want that edit and
  nothing more. It works in its own worktree: it analyses how your instruction lands across
  the KB, turns that into a minimal scope plan with an explicit list of what it will not
  change, and pauses for your confirmation before any edit. Only the confirmed scope is
  applied, it is reviewed against the four-mandate panel, and it commits only after you
  approve a second time.
allowed-tools: Read Glob Grep Bash Shell Terminal Write Edit Agent
argument-hint: "<what changed / what to update in the KB>"
---

# Targeted KB Update

State machine: ANALYZE -> SCOPE -> CONFIRM -> APPLY -> REVIEW -> APPROVAL -> DONE (FIX loop inside REVIEW).

Analyzes how a prompt-driven instruction lands in the Knowledge Base,
confirms the correct understanding and the exact scope with the user BEFORE
any edit, then applies only that confirmed delta through the same
review/calibration gate as `/aid-discover`. One pass per run -- each
invocation drives the state machine to the next natural pause point.

**Optional, off-pipeline.** `/aid-update-kb` is NOT in the numbered
phase-to-skill pipeline; no phase gate references it. It is an on-demand
maintenance skill (like `/aid-housekeep` / `/aid-ask`).

**Run-state is transient.** Its run-state lives in a project-level file
under `.aid/.temp/` (`.aid/.temp/UPDATEKB_STATE_<ts>.md`, gitignored per
`.gitignore`, removed at DONE) -- inside the skill's own Pre-flight-created
worktree (AC-10), not the caller's tree. It does NOT write to any work
`STATE.md` for its own run-state. The KB it edits has its own
`.aid/knowledge/STATE.md` for review/approval history.

**Boundary: prompt-driven-targeted vs source-driven-global.** This skill
is the prompt-driven-targeted half of the KB freshness loop -- the user
supplies the scoping seed (the instruction) and ANALYZE + SCOPE turn it into
a minimal Scope Plan. The source-driven-global sweep is `aid-housekeep`'s
KB-DELTA job. Docs that are domain-adjacent but not named by the instruction
stay out of scope here (HL-5) and route to that sweep instead. The
non-overlap contract between the two (FR-33/FR-34) is drawn in f010; this
skill references that boundary but does not own it.

**Human-gated, twice (NFR-6/C4/AC13, HL-1).** Analysis and scope-planning
are automatic; the change to KB content cannot proceed to APPLY without an
explicit human `[1] Confirm` at CONFIRM (the root fix -- scope is vetoed
BEFORE any edit exists), and cannot proceed to DONE without a second explicit
human `[1] Approved` at APPROVAL. No auto-apply path exists at either gate.

**State machine -- each `/aid-update-kb` invocation drives the state machine
until it hits a natural pause point per
`.aid/runtime/templates/state-machine-chaining.md`.
Mechanical states auto-chain; only PAUSE-FOR-USER-ACTION and HALT stop the
run. Two human gates by design: CONFIRM guards scope/understanding BEFORE
any edit; APPROVAL guards the specific edits before commit -- but a gate
answered `[1]` inline is itself a CHAIN, not a pause (below).**

> ```
> aid-update-kb  > Pre-flight ISOLATE runs first, every invocation
>   [ ANALYZE ] -> [ SCOPE ] -> [ CONFIRM ] -> [ APPLY ] -> [ REVIEW ] -> [ APPROVAL ] -> [ DONE ]
>                                 ^ human gate                             ^ human gate
>                                 [1] chains inline; [2]/[3] pause/halt
> ```

CONFIRM and APPROVAL are the two human gates -- **inline decision points,
not out-of-chat pauses.** Per `state-machine-chaining.md`, a pause is only
legitimate when the user has to do work outside the chat; answering an
inline question is not that. Answering `[1]` (CONFIRM's `Confirm` / APPROVAL's
`Approved`) is a CHAIN: the run continues straight through to APPLY / DONE
within the same invocation (`state-confirm.md`'s and `state-approval.md`'s
own `[1]` Advance lines say so explicitly, and the Dispatch table below
agrees). Only the re-plan/cancel branches actually pause or halt: CONFIRM
`[2] Adjust` loops back to SCOPE (or ANALYZE if the understanding itself
changes) and PAUSES (a genuine re-plan needs a fresh clean-context SCOPE
dispatch, which is real out-of-chat-equivalent work, not just an answer);
CONFIRM `[3] Cancel` HALTs. APPROVAL `[2] Additional consideration`
re-scopes back to CONFIRM/SCOPE (never blindly back to APPLY) and PAUSES for
the same reason. REVIEW's FIX loop (REVIEW -> fix edits -> REVIEW) repeats
until `grade >= minimum_grade AND teach-back PASS AND act-back PASS`, bounded
to Confirmed Scope only (HL-7).

---

## Pre-flight

### Step 1: Confirm the prompt

Confirm a prompt was supplied. If `/aid-update-kb` is invoked with no
argument, print:

```
Usage: /aid-update-kb "<what changed / what to update in the KB>"
Example: /aid-update-kb "work-003 added the content-isolation cornerstone (AID:BEGIN/END boundary)"
```

Then exit without entering the state machine.

### Step 2: ISOLATE -- create and enter the skill's own worktree (FR-11, AC-10)

Before any state runs, self-isolate in the skill's OWN worktree -- mirroring
the isolation `/aid-fix` gets at its INTAKE, adapted to this off-pipeline
skill's timestamp-keyed identity. It allocates no `work-NNN`, so it does
**not** use `.aid/runtime/scripts/works/worktree-lifecycle.sh` or
`.aid/runtime/templates/work-initiation-gate.md` -- both hard-validate a
`^work-[0-9]+$` id and would reject an `aid/update-kb-<ts>` branch. This is
**plain git worktree mechanics**, entered via the **generic enter contract**
of `.aid/runtime/templates/worktree-lifecycle.md § Step 2` only.

**2a. Detect an already-live run (resume), before creating anything new:**

```bash
UPDATEKB_WT=""

# Rung A -- already inside a live update-kb worktree (same-session resume:
# a prior invocation's EnterWorktree already switched this session here).
# This rung only DETECTS the candidate + its stored Prompt -- it does NOT
# resolve UPDATEKB_WT by itself; the prompt-match rule right below decides.
RUNG_A_PROMPT=""
CUR_BRANCH="$(git symbolic-ref --short HEAD 2>/dev/null || true)"
case "$CUR_BRANCH" in
  aid/update-kb-*)
    SF=$(ls -1 .aid/.temp/UPDATEKB_STATE_*.md 2>/dev/null | sort | tail -1)
    if [ -n "$SF" ] && ! grep -q "^\*\*State:\*\* DONE" "$SF" 2>/dev/null; then
      RUNG_A_PROMPT="$(grep -m1 "^\*\*Prompt:\*\*" "$SF" 2>/dev/null | sed 's/^\*\*Prompt:\*\* *//')"
    fi
    ;;
esac

# Rung B -- live update-kb worktree(s) registered elsewhere (cross-session
# resume: a NEW chat/terminal, cwd back at the caller's own tree). This
# block only ENUMERATES live candidates -- it never picks one itself. Each
# `CANDIDATE:` line is a live (non-DONE) aid/update-kb-* worktree; the
# `**Prompt:**` line beneath it is that run's stored instruction, read
# verbatim from disk.
if [ -z "$UPDATEKB_WT" ]; then
  CUR_WT=""
  while IFS= read -r line; do
    case "$line" in
      "worktree "*) CUR_WT="${line#worktree }" ;;
      "branch refs/heads/aid/update-kb-"*)
        SF=$(ls -1 "$CUR_WT"/.aid/.temp/UPDATEKB_STATE_*.md 2>/dev/null | sort | tail -1)
        if [ -n "$SF" ] && ! grep -q "^\*\*State:\*\* DONE" "$SF" 2>/dev/null; then
          echo "CANDIDATE: $CUR_WT"
          grep -m1 "^\*\*Prompt:\*\*" "$SF" 2>/dev/null
        fi
        ;;
    esac
  done < <(git worktree list --porcelain 2>/dev/null)
fi
```

**Rung A prompt-match (HIGH finding fix -- no silent stale-run hijack, same
class the fix below already closes for Rung B).** Being physically inside a
live `aid/update-kb-*` worktree is not itself a resume decision -- it is
resolved the same way as every Rung B candidate: by comparing the stored
`**Prompt:**` against the *current* invocation's instruction.

- If `$RUNG_A_PROMPT` is empty (Rung A found no live run at all -- the
  current branch doesn't match `aid/update-kb-*`, or its state file is
  `DONE`/absent), there is nothing to match here -- proceed to Rung B below;
  this is the ordinary case of a caller invoking the skill from their own
  tree.
- If `$RUNG_A_PROMPT` is set, compare it against the current invocation's
  instruction using the exact same normalized-exact-match rule the
  "Prompt-matched resume" section below defines (trim + collapse whitespace;
  never semantic/fuzzy):
  - **Match** -- this worktree IS this invocation's resume target. Set
    `UPDATEKB_WT="$(pwd -P)"` and skip Rung B, 2b, and the rest of this
    section entirely -- go straight to 2c.
  - **Mismatch** -- do NOT silently resume the session's current worktree
    for a different instruction. This is a harder stop than Rung B's
    "leave it untouched, start fresh elsewhere" -- the session is bodily
    *inside* the stale run right now, so silently starting a fresh worktree
    elsewhere while cwd stays here would be its own source of confusion.
    Print and STOP:

    ```
    [Pre-flight] ISOLATE: this session is already inside a paused
    /aid-update-kb run for a DIFFERENT instruction --
      Stored prompt:   <RUNG_A_PROMPT>
      This invocation: <the current invocation's instruction>
    Finish or cancel the paused run from inside this worktree (answer its
    pending gate, or run /aid-update-kb with the SAME instruction to
    resume it), or start this new instruction from a clean tree (a fresh
    terminal/session outside this worktree). STOP.
    ```

    Do not continue to Rung B, 2b, or 2c -- exit without entering the state
    machine.

**Prompt-matched resume (HIGH finding fix -- no silent stale-run hijack;
Rung B).** The block above only lists Rung B candidates (Rung A, if any, was
already resolved above); resuming one is a match decision, not a
first-match/last-match default. Compare each candidate's stored
`**Prompt:**` against the current invocation's instruction (exact match;
trimming leading/trailing whitespace and collapsing internal whitespace runs
is fine -- this is a text-equality check, never a semantic/fuzzy one):

- **Exactly one candidate matches** -- that run IS this invocation's resume
  target. Set `UPDATEKB_WT` to that candidate's worktree path.
- **No candidate matches** (including zero candidates found) -- this is a
  NEW run for a new instruction. Leave `UPDATEKB_WT` unset and continue to
  2b (fresh worktree). A live run for a *different* instruction is left
  completely untouched -- each distinct instruction gets its own isolated
  run; never repurpose someone else's paused run just because it is the
  only (or the most recent) one found.
- **More than one candidate matches the same instruction** (ambiguous --
  e.g. two duplicate invocations raced) -- do NOT silently pick one (no
  first-match/last-match default). Print the matching worktree paths and
  STOP:

  ```
  [Pre-flight] ISOLATE found more than one live run for this exact
  instruction -- ambiguous, cannot silently pick one:
    <matching worktree path 1>
    <matching worktree path 2> ...
  Resume one explicitly (cd into its worktree and re-run /aid-update-kb
  "<same instruction>" from there), or rephrase to a distinct instruction to
  start a fresh run. STOP.
  ```

  Do not continue to 2b or 2c until the user responds -- exit without
  entering the state machine.

If `$UPDATEKB_WT` resolved (either rung), that path IS the worktree to enter
-- skip 2b and go straight to 2c.

**2b. No live run found -- create a fresh worktree off `master`:**

```bash
TS="$(date +%Y%m%d%H%M)"
BRANCH="aid/update-kb-${TS}"
GCD="$(git rev-parse --git-common-dir 2>/dev/null)" || GCD=""
if [ -z "$GCD" ]; then
  echo "[Pre-flight] ISOLATE failed -- not a git repository. STOP."
  exit 1   # never fall back to the caller's own tree
fi
MAIN_ROOT="$(cd "$(dirname "$GCD")" && pwd -P)"
WT_ROOT="$(bash .aid/runtime/scripts/works/worktree-lifecycle.sh root)"
mkdir -p "$WT_ROOT"
UPDATEKB_WT="${WT_ROOT}/update-kb-${TS}"

if ! git worktree add "$UPDATEKB_WT" -b "$BRANCH" master >/dev/null 2>&1; then
  echo "[Pre-flight] ISOLATE failed -- 'git worktree add' could not create"
  echo "$UPDATEKB_WT on branch $BRANCH off master. STOP."
  exit 1   # fail-closed -- never run in the caller's tree/branch
fi
```

**Fail-closed (FR-11 / AC-10).** A worktree that cannot be created or
resolved is a hard STOP, not a degrade. `/aid-update-kb` never proceeds to
ANALYZE (or any other state) in the caller's own working tree or branch.
**Advance (on either failure above):** HALT -- print the diagnostic already
echoed by the failing block and exit; do not enter the state machine.

**2c. Enter it (agent action, per `worktree-lifecycle.md § Step 2`):**

- **claude-code:** invoke the **`EnterWorktree`** tool with `$UPDATEKB_WT`.
- **Any other profile:** operate with `$UPDATEKB_WT` as the working
  directory for every subsequent file operation in this run, and print
  `Working in worktree: $UPDATEKB_WT`.

From this point on, every state, the run-state file, the `aid/update-kb-<ts>`
branch, and every commit this run makes live **inside `$UPDATEKB_WT`** --
isolated from whatever the caller's own tree/branch was (HL-8's filesystem/
branch half; clean-context dispatch at ANALYZE/SCOPE, below, is the
conversation half). This worktree's branch is what ANALYZE's Step 0 records
as `**Branch:**` in the run-state file -- DONE never creates a separate
branch, it only ever commits on this one.

**Advance:** CHAIN -> ANALYZE (State Detection, below, resolves the state to
resume inside the entered worktree).

---

## Dispatch Protocol (L1+L2+L3 subagent visibility)

Every subagent dispatch in this skill MUST follow this protocol so the user
sees mid-wait progress instead of going silent for 10-25+ minutes. The full
protocol lives in two reference docs; this section is a checklist citing them.

**Before each dispatch:**

1. **Look up ETA** in `.aid/runtime/templates/rough-time-hints.md` for the
   subagent's operation class. Capture LOW-HIGH band.
2. **Read heartbeat config** via
   `bash .aid/runtime/scripts/config/read-setting.sh --path traceability.heartbeat_interval --default 1`
   (resolves from `.aid/settings.yml`; default 1; `0` = disabled).
3. **Pre-create heartbeat file** (always -- unconditional):
   - Pre-create `.aid/.heartbeat/<agent-name>-<unix-ts>.txt`
   - Include `HEARTBEAT_FILE=<path>` + `HEARTBEAT_INTERVAL=Nm` in dispatch prompt
   - SKIP only if `traceability.heartbeat_interval: 0` (user-explicit opt-out)
4. **Arm 3 L2 timers as SEPARATE background dispatches** (always -- even for short
   ETAs use minimums 60s/120s/180s; never gate on ETA). Each timer is its OWN
   `Bash(..., run_in_background=true)` call.
   Intervals are capped at 270 s / 540 s / 810 s, and a further 270 s timer is re-armed on
   each fire while the sub-agent still runs -- every fire refreshes the orchestrator's 5-minute
   prompt-cache TTL; a silent gap over 5 minutes re-writes the whole context at full price.

**References:**

- `.aid/runtime/templates/long-wait-protocol.md` -- full L2 spec
- `.aid/runtime/templates/subagent-heartbeat-protocol.md` -- full L3 spec
- `.aid/runtime/templates/rough-time-hints.md` -- current measured ETAs

---

## State Detection

State detection reads the files on disk, every run. Nothing remembered from an
earlier run or from this conversation counts as state, because the files may
have changed since.

Resolve `<STATE_FILE>` to the project-level update-kb run-state file under
`.aid/.temp/` (inside the worktree Pre-flight entered). The file is
transient (gitignored, never committed/pushed) and is named
`UPDATEKB_STATE_<YYYYMMDDHHMM>.md`; the DONE state removes it (and any stale
siblings) at the end of a run.

```bash
mkdir -p .aid/.temp
STATE_FILE=$(ls -1 .aid/.temp/UPDATEKB_STATE_*.md 2>/dev/null | sort | tail -1)
if [ -n "$STATE_FILE" ] && \
   grep -q "^\*\*State:\*\* DONE" "$STATE_FILE" 2>/dev/null; then
    STATE_FILE=""   # a leftover DONE file is stale -- start fresh
fi
[ -z "$STATE_FILE" ] && \
    STATE_FILE=".aid/.temp/UPDATEKB_STATE_$(date +%Y%m%d%H%M).md"
```

**Resume detection:**

| # | Disk condition (read run-state file) | Resume target |
|---|--------------------------------------|---------------|
| 1 | No run-state file (fresh run, just isolated by Pre-flight) | ANALYZE |
| 2 | `**State:** ANALYZE` present | ANALYZE |
| 3 | `**State:** SCOPE` present | SCOPE |
| 4 | `**State:** CONFIRM` present | CONFIRM |
| 5 | `**State:** APPLY` present | APPLY |
| 6 | `**State:** REVIEW` or `**State:** FIX` present | REVIEW |
| 7 | `**State:** APPROVAL` present | APPROVAL |
| 8 | `**State:** DONE` present | report "nothing to resume" -- HALT |

If row 8 is reached, print:

```
/aid-update-kb: nothing to resume -- the last run completed (DONE) and the
run-state file was removed. To start a new update, run:
  /aid-update-kb "<what changed / what to update in the KB>"
```

Then HALT.

### Run-state schema

The run-state file accumulates these fields as the run progresses (all
`**Field:**` markdown, read/written by exact-string match -- never
reformatted between states):

| Field | Written by | Meaning |
|---|---|---|
| `**State:**` | every state | current state name (drives resume, table above) |
| `**Prompt:**` | ANALYZE (Step 0, first entry only) | the user's instruction, verbatim |
| `**Started:**` | ANALYZE (Step 0) | ISO-8601 run-start timestamp |
| `**Branch:**` | ANALYZE (Step 0, recording Pre-flight's worktree branch) | the `aid/update-kb-<ts>` branch this run's worktree lives on |
| `**Understanding:**` | ANALYZE | plain restatement of what the instruction asks |
| `**Impact Findings:**` | ANALYZE | per-location table: KB location, current statement, Relation, Confidence |
| `**Contradictions & open questions:**` | ANALYZE | HL-3/HL-4 items CONFIRM must ask, never silently resolved |
| `**Escalation:**` | ANALYZE (ungroundable-concept PAUSE only) | the term + Q&A pointer when ANALYZE cannot ground a concept |
| `**Scope Plan:**` | SCOPE (replaces the legacy `Change Plan`) | the minimal (doc, change-type, description, Traces-to, Kind) table |
| `**Not-Changing:**` | SCOPE | docs considered but excluded, with reasons (HL-5) |
| `**Confirm Questions:**` | SCOPE | the questions CONFIRM presents |
| `**Confirmed:**` | CONFIRM (`[1]` only) | `yes` -- the HL-1 gate; APPLY is unreachable without it |
| `**Confirmed At:**` | CONFIRM (`[1]`) | ISO-8601 confirmation timestamp |
| `**Confirmed Scope:**` | CONFIRM (`[1]`) | the frozen doc set -- the scope contract for APPLY/REVIEW |
| `**Pre-APPLY baseline:**` | CONFIRM (`[1]`) | git HEAD (or `clean`) captured before APPLY's first edit -- REVIEW's scope-diff guard and any re-scope revert both diff against this |
| `**Adjustments:**` | CONFIRM (`[1]`/`[2]`) | free text, or the user's answers folded in, or `--`; read by SCOPE/ANALYZE Step 1 as the authorized re-plan input on a loop-back (HL-8/AC-9) |
| `**Edited Docs:**` | APPLY | the docs actually edited (unchanged field name from today) |
| `**APPLY Completed:**` | APPLY | ISO-8601 timestamp |
| `**Scope-diff:**` | REVIEW (Step 4, every outcome -- 4(a) incomplete-APPLY, 4(b) HARD FAIL, 4(c) PASS, 4(d) below-gate) | this pass's disk-derived scope-fidelity verdict; read back by APPROVAL Step 1 for its summary banner |
| `**Review Grade:**` / `**Review Teach-back:**` / `**Review Act-back:**` / `**Review Completed:**` | REVIEW | unchanged from today |
| `**User Approved:**` / `**Approved At:**` | APPROVAL | unchanged from today |
| `**Consideration:**` | APPROVAL (`[2]`, Step 3) | free-text summary of the user's re-scope consideration (`Q{N} -- <one-line summary>`); read by SCOPE Step 1 as an authorized re-plan input, the same way `**Adjustments:**` is (HL-8/AC-9) |

`**Change Plan:**` no longer exists anywhere in this schema -- SCOPE's
`**Scope Plan:**` replaces it.

**State-entry banners.** At the start of each state, print the matching banner:

**ANALYZE:**
```
[State: ANALYZE] -- Building the Impact Map: how and where the instruction lands in the KB.
aid-update-kb  > you are here
  [* ANALYZE ] -> [ SCOPE ] -> [ CONFIRM ] -> [ APPLY ] -> [ REVIEW ] -> [ APPROVAL ] -> [ DONE ]
```

**SCOPE:**
```
[State: SCOPE] -- Turning the Impact Map into the minimal Scope Plan + Not-Changing list.
aid-update-kb  > you are here
  [+ ANALYZE ] -> [* SCOPE ] -> [ CONFIRM ] -> [ APPLY ] -> [ REVIEW ] -> [ APPROVAL ] -> [ DONE ]
```

**CONFIRM:**
```
[State: CONFIRM] -- Human gate: confirm understanding + scope before any edit.
aid-update-kb  > you are here
  [+ ANALYZE ] -> [+ SCOPE ] -> [* CONFIRM ] -> [ APPLY ] -> [ REVIEW ] -> [ APPROVAL ] -> [ DONE ]
```

**APPLY:**
```
[State: APPLY] -- Applying only the Confirmed Scope's targeted summary+pointer edits.
aid-update-kb  > you are here
  [+ ANALYZE ] -> [+ SCOPE ] -> [+ CONFIRM ] -> [* APPLY ] -> [ REVIEW ] -> [ APPROVAL ] -> [ DONE ]
```

**REVIEW:**
```
[State: REVIEW] -- Scope-diff guard, then grading the changed KB docs through f005's four-mandate panel.
aid-update-kb  > you are here
  [+ ANALYZE ] -> [+ SCOPE ] -> [+ CONFIRM ] -> [+ APPLY ] -> [* REVIEW ] -> [ APPROVAL ] -> [ DONE ]
```

**APPROVAL:**
```
[State: APPROVAL] -- Human gate: confirm the approved changes before committing.
aid-update-kb  > you are here
  [+ ANALYZE ] -> [+ SCOPE ] -> [+ CONFIRM ] -> [+ APPLY ] -> [+ REVIEW ] -> [* APPROVAL ] -> [ DONE ]
```

**DONE:**
```
[State: DONE] -- Restamp approved_at_commit:, commit, and clean run-state.
aid-update-kb  > you are here
  [+ ANALYZE ] -> [+ SCOPE ] -> [+ CONFIRM ] -> [+ APPLY ] -> [+ REVIEW ] -> [+ APPROVAL ] -> [* DONE ]
```

---

## Dispatch

| State | Detail | Worker | Advance |
|-------|--------|--------|---------|
| ANALYZE | `references/state-analyze.md` | `aid-researcher` (clean-context dispatch, HL-8/AC-9) | CHAIN -> SCOPE (or PAUSE-FOR-USER-ACTION if a concept is un-groundable -- Q&A escalation to `.aid/knowledge/STATE.md`) |
| SCOPE | `references/state-scope.md` | `aid-architect` (clean-context dispatch, HL-8/AC-9) | CHAIN -> CONFIRM (or HALT if the Scope Plan is empty -- "no update needed") |
| CONFIRM | `references/state-confirm.md` | inline (human gate) | `[1]` CHAIN -> APPLY; `[2]` PAUSE-FOR-USER-ACTION -> SCOPE/ANALYZE; `[3]` HALT |
| APPLY | `references/state-apply.md` | inline (Edit) or `aid-architect`/`aid-researcher` for the owning doc-set | CHAIN -> REVIEW |
| REVIEW | `references/state-review.md` (REUSES f005's panel scoped to the changed docs; scope-diff guard runs first) | `aid-reviewer` panel (f005) | 4 outcomes (`state-review.md § Step 4`): incomplete APPLY -> CHAIN -> APPLY; out-of-scope disk edit -> PAUSE-FOR-USER-ACTION -> CONFIRM; grade/teach-back/act-back/TRACE-1 below gate (scope-diff already PASS) -> CHAIN -> FIX; READY -> CHAIN -> APPROVAL |
| APPROVAL | `references/state-approval.md` | inline | `[1] Approved` -> CHAIN -> DONE; `[2] Additional consideration` -> PAUSE-FOR-USER-ACTION -> re-scope (CONFIRM/SCOPE) |
| DONE | `references/state-done.md` | inline | HALT (restamp `approved_at_commit:`, commit on the Pre-flight worktree's `aid/update-kb-<ts>` branch, clean run-state) |

> **FIX loop.** Once the scope-diff guard has already PASSED, only grade /
> teach-back / act-back / `[TRACE-1]` findings route to the FIX cycle
> (REVIEW -> fix edits -> REVIEW) until `grade >= minimum_grade AND
> teach-back PASS AND act-back PASS` -- FIX edits stay within Confirmed Scope
> (HL-7). Scope-diff outcomes never reach this loop: an incomplete APPLY (a
> Confirmed-Scope doc not yet edited) chains straight back to APPLY, and an
> out-of-scope disk edit escalates to the user
> (PAUSE-FOR-USER-ACTION -> CONFIRM) instead of expanding scope -- see
> `references/state-review.md § Step 4` for the full 4-outcome routing.
> The minimum grade resolves via:
> `bash .aid/runtime/scripts/config/read-setting.sh --skill update-kb --key minimum_grade --default A`

> **Clean-context dispatch (ANALYZE/SCOPE, HL-8/AC-9).** Both dispatches
> receive ONLY the verbatim `/aid-update-kb` instruction (the `**Prompt:**`
> field from run-state), plus -- **if this is a re-plan loop-back** (CONFIRM
> `[2] Adjust`, APPROVAL `[2]`, or REVIEW 4(b) "accept") -- the run-state's
> recorded `**Adjustments:**`/`**Consideration:**` field: the user's
> explicit gate-time re-plan guidance, given AT the gate as part of the
> instruction dialogue -- part of THIS run's own instruction+confirmation
> dialogue. This is **authorized, first-class scoping input**, distinct
> from the FORBIDDEN source below. Both dispatches also get KB/codebase
> read access (`.aid/knowledge/`, `INDEX.md`, the repo) -- never the
> ambient session transcript, never anything from a previous or unrelated
> conversation or instruction that is absent from the instruction/recorded
> field. The orchestrator MUST NOT enrich either dispatch prompt with
> anything beyond those. Content that lives only in a previous or
> unrelated conversation -- anything outside this run's own dialogue -- and
> not in the instruction, a recorded Adjustments/Consideration field, or
> groundable KB/code evidence has no valid `Traces-to` and can never enter
> the Scope Plan (AC-9). See `state-scope.md § Step 1` / `state-analyze.md
> § Step 1` for how the recorded field is actually wired into the dispatch
> prompt on a loop-back.

> **REVIEW reuse (f005).** The REVIEW state does not redefine the review gate
> -- it invokes f005's four-mandate panel (`aid-reviewer` Correctness,
> Anatomy-incl-altitude, Teach-back, Act-back) with `{{ARTIFACTS}}` scoped to
> the **disk-derived** edited-doc set from `references/state-review.md`'s
> Step 0a scope-diff guard (`git status --porcelain` / `git diff` against the
> `**Pre-APPLY baseline:**`) -- NEVER APPLY's self-reported
> `**Edited Docs:**` -- and `<scope>` = `update-kb`. The merged ledger is
> written to `.aid/.temp/review-pending/update-kb.md`. Grade and teach-back
> are evaluated via the unchanged `grade.sh`.

> **DONE (commit convention).** Work happens on the `aid/update-kb-<ts>`
> branch the Pre-flight ISOLATE step already created and entered -- DONE
> creates **no** separate branch of its own (there is no "ensure branch"
> step); it only commits on the one the whole run has been living on since
> Pre-flight. The skill never pushes -- and never to `master` -- the human
> pushes / opens the PR after CI is green. `approved_at_commit:` is
> restamped in DONE (after the human gate), never in APPLY -- so a doc that
> is edited-but-not-yet-approved is correctly `suspect` to f007, never
> falsely current.

On state entry, print `[State: NAME]` + the "you are here" banner from State
Detection above. When a state completes, route by its `**Advance:**` type per
`.aid/runtime/templates/state-machine-chaining.md`:

- **CHAIN** -> begin the next state's reference doc within the same invocation; no exit.
- **PAUSE-FOR-USER-ACTION** -> print the pause reason + resume command and exit.
- **HALT** -> print the closing summary and exit.

> **State-machine chaining:** Each `/aid-update-kb` invocation drives the state
> machine until it hits a natural pause point per
> `.aid/runtime/templates/state-machine-chaining.md`. Mechanical states
> auto-chain; only PAUSE-FOR-USER-ACTION and HALT stop the run.

---

## Hard limits (HL-1..HL-8)

Owner-confirmed limits every state above cites. `/aid-update-kb` never ships a
change that violates one of these.

- **HL-1 No apply without confirmation.** No KB edit before the user
  confirms scope + understanding at CONFIRM. Enforced by: CONFIRM is a PAUSE
  gate; APPLY is unreachable without `**Confirmed:** yes` in run-state.
- **HL-2 Limit to the scope of the instruction.** The Scope Plan is a subset
  of what the instruction explicitly requests plus *necessary closure* (e.g.
  a coined term's glossary entry) -- and closure is surfaced at CONFIRM,
  never silent. Enforced by: SCOPE's `Traces-to` + `Kind` columns; CONFIRM's
  presentation of closure items.
- **HL-3 No assumptions -- surface, don't act.** ANALYZE may form hypotheses
  (`LIKELY`/`UNCERTAIN`) but anything not `CONFIRMED`-from-instruction is
  routed to CONFIRM as a question; never applied silently. Enforced by:
  ANALYZE's Confidence column + Contradictions/open-questions; CONFIRM's
  question list.
- **HL-4 Flag, don't resolve, contradictions.** Instruction-vs-KB conflicts
  are raised to the user; the skill never silently "corrects" either side.
  Enforced by: ANALYZE's Relation column (`CONTRADICTS`/`MISMATCH`); CONFIRM.
- **HL-5 No opportunistic edits.** Docs that merely share a domain/tag, or
  are `suspect` per freshness but unnamed by the instruction, are out of
  scope (-> `aid-housekeep`). Enforced by: ANALYZE (no tag-overlap candidate
  net; freshness advisory only); SCOPE's Not-Changing list.
- **HL-6 New files require explicit confirmation.** Allowed, never a silent
  side effect. Enforced by: SCOPE's `new-file` Kind tag; CONFIRM; APPLY
  (the actual creation mechanics -- `state-apply.md § Step 2b`'s "New file"
  branch, the only place a `Kind: new-file` row's doc is ever created, via
  `Write`, following the f001 schema).
- **HL-7 Grade-chasing may not expand scope.** The REVIEW FIX loop and
  DONE's closure re-check may only edit within Confirmed Scope; out-of-scope
  needs escalate to the user. Enforced by: REVIEW's FIX-loop constraint;
  DONE's closure-shortfall escalation.
- **HL-8 The instruction plus this run's own confirmation dialogue are the
  only scope seeds; prior or unrelated conversation is not a source.**
  Scope and content are grounded solely in: the verbatim `/aid-update-kb`
  instruction; the user's own gate-time responses recorded within this
  run's CONFIRM/APPROVAL/REVIEW-4(b) confirmation dialogue (the run-state's
  `**Adjustments:**`/`**Consideration:**` field -- the skill's OWN
  instruction+confirmation work-dialogue, **authorized first-class scoping input**,
  not the forbidden source below); and KB/codebase evidence. Content
  originating from a previous or unrelated conversation or instruction --
  anything NOT part of this KB-update's own dialogue -- is never a source
  of scope or content; that ban is unweakened and exactly as strict as
  before this carve-out (that, not the gate's own recorded answer, is what
  this limit forbids). **The clean line:** inside this
  skill-run's own instruction + confirmation dialogue = in-scope; anything from outside it = banned.
  Enforced by: (a) Pre-flight's worktree
  isolation (the filesystem/branch plane); (b) clean-context dispatch at
  ANALYZE/SCOPE (the sub-agent receives only the verbatim instruction + the
  recorded Adjustments/Consideration field, if any + KB/code pointers,
  never the ambient session transcript or any previous/unrelated
  conversation -- the orchestrator must not enrich the dispatch with
  anything beyond those; the conversation plane; see `state-scope.md
  § Step 1` / `state-analyze.md § Step 1` for the wired channel); (c) every
  Scope Plan item's `Traces-to` cites the instruction text, a recorded
  Adjustment/Consideration, or a KB/code location, never "the session" or
  prior/unrelated discussion.
