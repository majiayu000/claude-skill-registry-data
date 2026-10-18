---
name: aid-housekeep
description: >
  Sweep the project back into a consistent state after work has landed. Use this skill when
  the Knowledge Base has drifted from the code, the generated summary is stale, or work-area
  artifacts have piled up. It runs three gated jobs in order: re-discovering KB docs that
  changed since the last approval, regenerating the visual summary if the KB moved, and
  clearing stale work-area artifacts. Forward-authored greenfield docs take the Conformance
  Lane, which flags design-versus-as-built divergence for you to reconcile and never
  overwrites the design itself. Each stage commits on its own branch and nothing is pushed;
  a stalled run resumes where it stopped. This is the source-driven global reconcile -- for
  a targeted, prompt-named delta use `/aid-update-kb`.
allowed-tools: Read Glob Grep Bash Shell Terminal Write Edit Agent
argument-hint: "[--cleanup-only] [--grade X] jump to cleanup stage, or set minimum summary grade"
---

# Knowledge Base Housekeeping

State machine: PREFLIGHT → KB-DELTA → SUMMARY-DELTA → CLEANUP → DONE.

Runs the three standard housekeeping jobs in a safe, fixed order, on a dedicated
`aid/housekeep-*` branch, with one commit per stage. Re-running after a stalled
gate resumes at the stalled stage — not job 1.

**Prerequisite:** A `.aid/` directory must exist (init has run). Not Plan Mode
(stages write). A git repository must be present and clean enough to branch.

**Absent from the mandatory pipeline flow.** `/aid-housekeep` is an optional,
on-demand skill (REQUIREMENTS.md FR6). It is NOT inserted into the phase-to-skill
pipeline mapping and no phase gate references it.

**State machine — each `/aid-housekeep` invocation drives the state machine until
it hits a natural pause point per
[`.aid/runtime/templates/state-machine-chaining.md`](../../aid/templates/state-machine-chaining.md).
Mechanical states auto-chain; only PAUSE-FOR-USER-ACTION and HALT stop the run.**

> ```
> aid-housekeep  ▸ one step per run
>   [ PREFLIGHT ] → [ KB-DELTA ] → [ SUMMARY-DELTA ] → [ CLEANUP ] → [ DONE ]
> ```

---

## Arguments

| Argument | Effect |
|----------|--------|
| *(none)* | Full gated sequence: `KB-DELTA → SUMMARY-DELTA → CLEANUP` (FR7 default). |
| `--cleanup-only` | Jump straight to CLEANUP, skipping KB and summary (AC10). Sets `**Mode:** cleanup-only`. KB/Summary stage rows are left `—` (a deliberate cleanup-only run does not violate C1 — REQUIREMENTS.md FR7). `--grade X` is ignored under `--cleanup-only` (SUMMARY-DELTA is bypassed). |
| `--grade X` | Pass-through to the SUMMARY-DELTA delegation to `/aid-summarize`. Format: `[A-F][-+]?` (e.g., `A`, `A-`, `B+`). Without this, resolved via `bash .aid/runtime/scripts/config/read-setting.sh --skill summary --key minimum_grade --default A`. Ignored when `--cleanup-only` is also given. |

> **`--fetch` / offline:** The online-first / permissioned-offline gate
> (REQUIREMENTS.md C2, AC3) is feature-002's concern. The skeleton does not parse
> a `--fetch` flag; it simply routes into KB-DELTA, whose body (feature-002)
> performs `git fetch origin` and the offline-permission prompt.

---

## Dispatch Protocol (L1+L2+L3 subagent visibility)

Every subagent dispatch in this skill MUST follow this protocol so the user
sees mid-wait progress instead of going silent for 10–25+ minutes. The full
protocol lives in two reference docs; this section is a checklist citing them.

**Before each dispatch:**

1. **Look up ETA** in `.aid/runtime/templates/rough-time-hints.md` for the
   subagent's operation class. Capture LOW–HIGH band.
2. **Read heartbeat config** via
   `bash .aid/runtime/scripts/config/read-setting.sh --path traceability.heartbeat_interval --default 1`
   (resolves from `.aid/settings.yml`; default 1; `0` = disabled).
3. **Pre-create heartbeat file** (always — unconditional):
   - Pre-create `.aid/.heartbeat/<agent-name>-<unix-ts>.txt`
   - Include `HEARTBEAT_FILE=<path>` + `HEARTBEAT_INTERVAL=Nm` in dispatch prompt with explicit instruction to update during long phases
   - SKIP only if `traceability.heartbeat_interval: 0` (user-explicit opt-out in `.aid/settings.yml`)
4. **Arm 3 L2 timers as SEPARATE background dispatches** (always — even for short ETAs use minimums 60s/120s/180s; never gate on ETA). Each timer is its OWN `Bash(..., run_in_background=true)` call:
   - Call A: `sleep <min(LOW/2, 270) in s> && echo "... <agent> still running (Xm elapsed of ~LOW–HIGH)"` — own background dispatch
   - Call B: `sleep <min(LOW, 540) in s> && echo "... <agent> at estimated time (LOWm elapsed)"` — own background dispatch
   - Call C: `sleep <min(1.5×LOW, 810) in s> && echo "⚠️ <agent> EXCEEDED estimate (1.5×LOWm elapsed); consider checking on it or cancelling"` — own background dispatch
   - **Keep-warm re-arm:** when the last timer fires and the sub-agent is still running, arm one more `sleep 270 && echo "... <agent> still running (Xm elapsed)"` (own background dispatch), and again on each fire, until the completion notification arrives. Every fire is a request that re-reads the cached context and refreshes its 5-minute prompt-cache TTL; a silent gap over 5 minutes re-writes the whole context at full price.
   - ⚠️ **DO NOT chain timers with `&` inside a single wrapper Bash call.** If you do, the wrapper exits when the last `&` is queued, orphaning the sleeps — their stdout is silently lost and you'll never see the timer fire. Each timer needs its own `run_in_background: true` task so the harness can track and notify on completion.

**During dispatch:**

- **On L2 timer fire:** surface the timer output. If heartbeat file exists,
  also read it and append `[from heartbeat] state: <state> · progress: <progress>
  · activity: <activity>` to the narration.

**On completion / failure:**

- **Success:** emit `✓ <agent> done in <actual>` with measured time. When the dispatch is
  for a real `task-NNN`, append a `dispatch_log` entry to that task's own state (full
  path: its `STATE.yml`; flat path: `tasks_lifecycle.task-NNN.dispatch_log`) with
  fields `date`/`agent`/`eta_band`/`actual`/`outcome` -- the work-level Calibration
  Log / Dispatches views are derived at read time from these entries
  (`work-state-template.yml`); there is no work-level section to write. When the
  dispatch is NOT task-scoped (a housekeep-internal
  cycle, not a `task-NNN`), there is no persisted target at all -- the console
  narration above is the sole record. Mandatory wherever a target exists (never
  optional, never "if tracked"). Delete heartbeat file.
- **Failure:** emit `✗ <agent> FAILED after <elapsed> (reason: <one-line>)`.
  Decide whether to re-dispatch, fall back, or surface to user. Delete
  heartbeat file.

**References:**

- `.aid/runtime/templates/long-wait-protocol.md` — full L2 spec
- `.aid/runtime/templates/subagent-heartbeat-protocol.md` — full L3 spec
- `.aid/runtime/templates/rough-time-hints.md` — current measured ETAs
- `aid-*` agent definitions, `## Heartbeat protocol` section — subagent-side contract

---

## State Detection

State detection reads the files on disk, every run. Nothing remembered from an
earlier run or from this conversation counts as state, because the files may
have changed since.

Resolve `<STATE_FILE>` to the **project-level housekeep run-state file** under
`.aid/.temp/` — `/aid-housekeep` is project maintenance, so its run-state does NOT
live in any work-area `STATE.yml`. The file is transient (gitignored, never
committed/pushed) and is named `HOUSEKEEP_STATE_<YYYYMMDDHHMM>.md`; the DONE state
removes it (and any stale siblings) at the end of a run.

```bash
mkdir -p .aid/.temp
# Reuse the most recent in-progress run-state file; otherwise start a fresh one.
STATE_FILE=$(ls -1 .aid/.temp/HOUSEKEEP_STATE_*.md 2>/dev/null | sort | tail -1)
if [ -n "$STATE_FILE" ] && \
   [ "$(bash .aid/runtime/scripts/housekeep/housekeep-state.sh --state "$STATE_FILE" --read --field State)" = "DONE" ]; then
    STATE_FILE=""   # a leftover DONE file is stale (DONE-cleanup missed it) — start fresh
fi
[ -z "$STATE_FILE" ] && STATE_FILE=".aid/.temp/HOUSEKEEP_STATE_$(date +%Y%m%d%H%M).md"
```

Then resolve the resume target from the `## Housekeep Status` block:

```bash
bash .aid/runtime/scripts/housekeep/housekeep-state.sh --state "$STATE_FILE" --resume
```

(On a fresh run `$STATE_FILE` does not exist yet; `housekeep-state.sh` creates it on
the first `--write`, and `--resume`/`--read` treat an absent file as "no section".)

**Argument pre-check (before resume detection):**

1. If `--cleanup-only` was passed → set `**Mode:** cleanup-only` via
   `bash .aid/runtime/scripts/housekeep/housekeep-state.sh --state <STATE_FILE> --write --field "Mode" --value "cleanup-only"`.
   Route PREFLIGHT → CLEANUP directly (row 2 of the resume table). Any `--grade X` value is
   noted but ignored (SUMMARY-DELTA is bypassed in cleanup-only mode).
2. If `--grade X` was passed (without `--cleanup-only`) → validate format `[A-F][-+]?`; if
   invalid, exit non-zero with:
   ```
   ⚠️  --grade value must be a letter A–F with optional +/- suffix (e.g., A, A-, B+).
       Got: <value>
   ```
   If valid, store the grade value for pass-through to SUMMARY-DELTA.
3. Any other unrecognized flag → exit non-zero with:
   ```
   ⚠️  Unknown argument: <flag>
       Usage: /aid-housekeep [--cleanup-only] [--grade X]
   ```

**Resume detection (the six-row re-entry table):**

| # | Disk condition (read `## Housekeep Status`) | Resume target |
|---|---------------------------------------------|---------------|
| 1 | No `## Housekeep Status` section (fresh run), no `--cleanup-only` | PREFLIGHT → KB-DELTA |
| 2 | No section, `--cleanup-only` flag | PREFLIGHT → CLEANUP (Mode=cleanup-only) |
| 3 | `**KB Stage:**` is `stalled` / `running` / `—` | resume at **KB-DELTA** |
| 4 | `**KB Stage:**` passed/skipped AND `**Summary Stage:**` stalled/running/`—` | resume at **SUMMARY-DELTA** |
| 5 | KB + Summary passed/skipped AND `**Cleanup Stage:**` not passed | resume at **CLEANUP** |
| 6 | All three passed/skipped AND `**State:** DONE` | report "nothing to resume" (NFR2 idempotent no-op) |

If row 6 is reached, print:
```
✅ /aid-housekeep: nothing to resume — the last run completed successfully (DONE).
   The run-state file under .aid/.temp/HOUSEKEEP_STATE_*.md is cleaned at DONE, so a
   fresh /aid-housekeep simply starts a new run. (Row 6 is reached only if a stale
   DONE file lingered; deleting .aid/.temp/HOUSEKEEP_STATE_*.md also resets it.)
```
Then HALT.

**State-entry banner.** At the start of each state, print the matching banner:

**PREFLIGHT:**
```
[State: PREFLIGHT] — Verifying prerequisites: .aid/ exists, not Plan Mode, git repo present.
aid-housekeep  ▸ you are here
  [● PREFLIGHT ] → [ KB-DELTA ] → [ SUMMARY-DELTA ] → [ CLEANUP ] → [ DONE ]
```

**KB-DELTA:**
```
[State: KB-DELTA] — Detecting KB delta since last approval; dispatching targeted re-discovery.
aid-housekeep  ▸ you are here
  [✓ PREFLIGHT ] → [● KB-DELTA ] → [ SUMMARY-DELTA ] → [ CLEANUP ] → [ DONE ]
```

**SUMMARY-DELTA:**
```
[State: SUMMARY-DELTA] — Checking whether the visual summary needs regeneration.
aid-housekeep  ▸ you are here
  [✓ PREFLIGHT ] → [✓ KB-DELTA ] → [● SUMMARY-DELTA ] → [ CLEANUP ] → [ DONE ]
```

**CLEANUP:**
```
[State: CLEANUP] — Sweeping stale work-area artifacts.
aid-housekeep  ▸ you are here
  [✓ PREFLIGHT ] → [✓ KB-DELTA ] → [✓ SUMMARY-DELTA ] → [● CLEANUP ] → [ DONE ]
```

**DONE:**
```
[State: DONE] — Housekeeping complete.
aid-housekeep  ▸ you are here
  [✓ PREFLIGHT ] → [✓ KB-DELTA ] → [✓ SUMMARY-DELTA ] → [✓ CLEANUP ] → [● DONE ]
```

---

## Dispatch

| State | Detail | Worker | Advance |
|-------|--------|--------|---------|
| PREFLIGHT | `references/state-preflight.md` | inline | CHAIN → KB-DELTA (or CLEANUP if Mode=cleanup-only) |
| KB-DELTA | `references/state-kb-delta.md` | `aid-architect` (feat-002 dispatches sub-agents via `/aid-discover`) | CHAIN → SUMMARY-DELTA / PAUSE-FOR-USER-ACTION if stalled |
| SUMMARY-DELTA | `references/state-summary-delta.md` | inline (delegates to `/aid-summarize`) | CHAIN → CLEANUP / PAUSE-FOR-USER-ACTION if stalled |
| CLEANUP | `references/state-cleanup.md` | inline | CHAIN → DONE |
| DONE | `references/state-done.md` | inline | HALT |

> **KB-DELTA sub-agent dispatch (feature-002).** The `aid-architect` Worker for
> KB-DELTA detects delta since the last KB approval, scopes/confirms the affected
> documents, and dispatches targeted re-discovery via `/aid-discover`. The
> `## Dispatch Protocol (L1+L2+L3)` block above applies to all sub-agent dispatches
> within KB-DELTA. The full dispatch protocol is documented inside
> `references/state-kb-delta.md` (authored by task-004 / feature-002).

On state entry, print `[State: NAME]` + the "you are here" map from State Detection above.
When a state completes, route by its `**Advance:**` type (per [`state-machine-chaining.md`](../../aid/templates/state-machine-chaining.md)):
- **CHAIN** → begin the next state's reference doc within the same invocation; no exit.
- **PAUSE-FOR-USER-ACTION** → print the pause reason + resume command and exit.
- **HALT** → print the closing summary and exit.

> **State-machine chaining:** Each `/aid-housekeep` invocation drives the state
> machine until it hits a natural pause point per
> `.aid/runtime/templates/state-machine-chaining.md`. Mechanical and inline-question
> states auto-chain; only PAUSE-FOR-USER-ACTION / HALT stop the run.
