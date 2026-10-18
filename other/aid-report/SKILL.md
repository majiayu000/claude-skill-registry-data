---
name: aid-report
description: >
  Analyse data or usage and return a verified insight report in one pass -- exploratory
  analysis, metrics, or an A/B result. Use this skill when you have data and need to know
  what it says, with the caveats stated rather than buried. It presents findings,
  conclusions both positive and negative, data-quality caveats, any conflicts with the
  reason for each, and the gaps; you decide what follows. The data itself, plus the
  Knowledge Base and project source for what the data means, are the authoritative
  grounding; external baselines are supplementary and cited with a URL and access date. It
  reads data read-only. For a durable dashboard rather than a one-off report, use
  `/aid-create-dashboard`.
allowed-tools: Read Glob Grep Bash Shell Terminal Write Edit Agent
argument-hint: "<subject> -- the data/usage to analyze (a dataset, logs, metrics, an A/B result)"
---

# Report (analyze now, resolve nothing)

`/aid-report` analyzes data/usage **now** and returns a **curated, verified insight
report**. Like `/aid-research` it resolves nothing -- it presents the picture and you
decide -- but its subject is *data* (a dataset, logs, telemetry, metrics, an A/B result)
rather than an open question.

- **Boundary:** `aid-report` = a **one-time** analysis + insight. A **durable, refreshable**
  BI view is `/aid-create-dashboard`, not this. If the user wants the analysis to recur,
  that's a printed handoff to `/aid-create-dashboard`.
- **Not a numbered pipeline phase**; does not route to `/aid-execute`.

State machine: **INTAKE -> ANALYZE -> VERIFY (loop) -> PRESENT [user resolves] -> HANDOFF?
-> DONE**. Print the `[State: NAME] -- {purpose}` entry line on each state.

---

## State: INTAKE

1. **Require a subject.** Empty argument -> ask one bootstrapping question ("What data
   should I analyze, and what question about it?") and wait.
2. **Pick the path:** **Fast** -- a clear data source + a clear analytical ask ("analyze
   the A/B results in `results.csv`", "error-rate breakdown from these logs") -> analyze
   now. **Guided** -- vague ("analyze our usage") -> scope *which data, which metrics, what
   question* first, then analyze.
3. **Classify complexity (model + effort):** simple (small dataset, one metric) ->
   `aid-researcher` at **sonnet / medium**; standard/complex (large data, A/B significance,
   deep telemetry) -> **opus / high**. Verifier tier >= producer tier.
4. **Consult the Work Initiation Gate, then allocate the work folder + STATE.** First run
   the gate (`.aid/runtime/templates/work-initiation-gate.md`):
   `bash .aid/runtime/scripts/works/enumerate-works.sh` (main tree + every git worktree).
   Empty -> allocate, no prompt. Works exist -> ask new-vs-continuation; on **continuation**
   route to the chosen work's resume door and STOP (allocate nothing); on **new work**:
   create and enter the worktree per the gate's `§ 3a` step 2
   (`worktree-lifecycle.sh create <work-id> <name>`, STOP on a non-zero exit or empty path,
   else enter the resolved path), **then** allocate (`pipeline.path: lite`, `initiator:
   aid-report`, `lifecycle: Running`, `active_skill: aid-report`; `phase` not driven), same
   as the other collapse skills.

**Advance:** ANALYZE.

---

## State: ANALYZE

Access the data **read-only** and dispatch **`aid-researcher`** (clean context, tiered) to
analyze + consolidate:

- **Data access:** files / logs / exports -> read directly (never mutate the source). A
  live DB / analytics / telemetry service -> **MCP-first connector**
  (`connectors/consumption-protocol.md`): scan `.aid/connectors/INDEX.md`, request the
  connection from the host MCP; no catalogued connector -> ask the user for the export.
  Optional, never blocks.
- **Two-tier grounding (enforced):** the **data** + KB/source (what a metric means) are
  authoritative; external baselines/benchmarks are supplementary, cited URL + date. A
  data-vs-KB-assumption contradiction is surfaced with its reason, never resolved.
- It writes `REPORT.md` into the work folder (see [Response shape](#response-shape)).

**Advance:** VERIFY.

---

## State: VERIFY

1. **Mechanical grounding check** (no dispatch): findings cite the data; external claims a
   URL+date; the **Caveats** and **Conflicts** sections exist.
2. **Adversarial verification** -- clean-context **`aid-reviewer`** checks `REPORT.md`:
   findings supported by the data; **no metric or A/B conclusion stated without its caveat**
   (sampling, significance, denominator, confounders); conflicts surfaced with reasons;
   conclusions not overstated into resolutions. Writes a review-quality ledger to
   `.aid/.temp/review-pending/<work>-verify.md`.
3. **Grade:** `bash .aid/runtime/scripts/grade.sh --explain <ledger>`. Not clean -> loop
   to ANALYZE. Circuit-breaker: 3 cycles -> IMPEDIMENT + `lifecycle: Blocked`.

**Advance:** PRESENT.

---

## State: PRESENT  (hard stop -- the user resolves)

Set `lifecycle: Paused-Awaiting-Input`. Present `REPORT.md` clearly: findings
(metrics/tables), conclusions (+/-), **caveats & data-quality gaps** (first-class),
conflicts with reasons, and gaps. Assert no resolution.

**Advance:** HANDOFF (optional) then DONE.

---

## State: HANDOFF  (optional; printed suggestions only)

Printed suggestions the user may act on: make it recurring (`/aid-create-dashboard`), record
a decision (`/aid-document-decision`), act on a conclusion (`/aid-create*` / `/aid-update*`),
or comment on a source ticket (`/aid-update-ticket comment [<connector>:]<ticket-id> <text>`).
Never auto-invoked; never a resolution.

**Advance:** DONE.

---

## State: DONE

Set `lifecycle: Completed`, `updated` now, append a `## Lifecycle History` row. Keep the
work folder (`REPORT.md`, the verify ledger) as the audit record.

---

## Response shape

`REPORT.md`, sections in order:

1. **Question / Scope** -- the analytical ask, as scoped.
2. **Data & method** -- what data, its source, and how it was analyzed.
3. **Findings** -- the metrics / tables / EDA output.
4. **Conclusions** -- positive *and* negative, each tied to a finding.
5. **Caveats & data-quality gaps** -- sampling, confounders, significance, missing data;
   `none` only if genuinely none.
6. **Conflicts & contradictions** -- data<->KB especially, each with its reason + citations;
   `none` if none.
7. **Sources** -- data source(s) + KB/`file:line` (authoritative) and external baselines
   `URL (accessed YYYY-MM-DD)` (supplementary), separated.

---

## Constraints

- **Resolves nothing**; presents findings/conclusions/caveats/conflicts/gaps.
- **Read-only on the data source**; never mutates it.
- **Two-tier grounding, enforced**; data<->KB conflicts surfaced with reasons.
- **Caveats are mandatory** -- a metric/A-B conclusion without its caveat fails VERIFY.
- **Clean context**; **verification always a sub-agent** (`aid-reviewer`).
- **Boundary:** durable/refreshable dashboards are `/aid-create-dashboard`, not this.
- **Tracking:** write STATE `lifecycle` at every transition.
