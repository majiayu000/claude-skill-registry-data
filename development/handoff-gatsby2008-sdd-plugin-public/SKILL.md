---
name: handoff
description: Build a model-agnostic execution handoff pack from existing SDD artifacts. Exits without changes if required artifacts are missing.
argument-hint: "[slug]"
allowed-tools: Read, Write, Bash(git rev-parse:*), Bash(find .specwork:*), Bash(cat .specwork/_state/*), Bash(cat .specwork/_spec/*), Bash(cat .specwork/_plan/*), Bash(cat .specwork/_progress/*), Bash(mkdir:*), Bash(test:*), Bash(date:*), Bash(python3:*), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py:*)
---

# Handoff

Build a compact, model-agnostic execution pack that can be pasted into another coding agent such as Gemini, Copilot, Codex, or Claude.

`/sdd:handoff` must NOT analyze the repository, enrich the spec, generate a plan, or infer missing requirements.

It only packages existing pipeline artifacts.

---

## Core Rule

If the required artifacts are missing, exit cleanly and make no changes.

As a first step, confirm a pipeline exists here — abort with no writes if the exit code is non-zero:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py precheck
```

Do not attempt to recover by scanning the repo.
Do not ask the user to provide missing content inside this skill.
Do not create a partial handoff pack.

---

## No-Enrichment Rule

`/sdd:handoff` may curate, reorder, summarize, and mechanically derive execution sections from existing `.specwork` artifacts.

It must not introduce new business meaning, new implementation decisions, new file targets, new constraints, or new assumptions.

Every derived section must be traceable to one of:
- spec.md
- plan.md
- rules.json
- implementation-cache.json
- context.md
- escalations.md

If the information is not present in those artifacts, omit it.

The fixed boilerplate sections (`Execution Budget`, `Failure Handling`) are exempt — they are static text declared in this skill, not derived from artifacts.

---

## Required Artifacts

`/sdd:handoff` requires all of these:

```text
.specwork/_state/<slug>-state.json
.specwork/_state/<slug>-rules.json
.specwork/_spec/<slug>-spec.md
```

Optional artifacts (consumed when present):

```text
.specwork/_plan/<slug>-plan.md
.specwork/_progress/<slug>-context.md
.specwork/_progress/escalations.md
.specwork/_state/<slug>-implementation-cache.json
```

---

## Output

Creates:

```text
.specwork/_handoff/<slug>-execution-pack.md
```

Optional machine-readable summary:

```text
.specwork/_handoff/<slug>-execution-pack.json
```

---

## What It Does

| Step | Action |
|------|--------|
| 0 | Pipeline precondition — abort if `.specwork/` is missing or uninitialized via `gates.py precheck` |
| 1 | Resolve slug from argument or current branch |
| 2 | Check required artifacts |
| 3 | Abort if unresolved Open Questions exist in spec **or** plan |
| 4 | Load state, rules, spec, and optional plan/cache/context/escalations |
| 4.5 | Worktree freshness check — abort if plan Target Files diverge from current worktree state |
| 5 | Build execution pack (curated capsule) — includes behavioral change warning if signals detected |
| 6 | Build JSON summary |
| 7 | Print concise summary |

---

## Step 1 — Resolve Slug

If an explicit argument is provided, use it as `SLUG`.

Otherwise derive it from current branch:

```bash
git rev-parse --abbrev-ref HEAD
```

Rules:

```text
feature/IR-45        -> ir-45
feature/ir-45-fix    -> ir-45-fix
hotfix/foo           -> foo
```

Normalize to lowercase for file lookup.

---

## Step 2 — Required Artifact Check

Check for:

```text
STATE_FILE=".specwork/_state/${SLUG}-state.json"
RULES_FILE=".specwork/_state/${SLUG}-rules.json"
SPEC_FILE=".specwork/_spec/${SLUG}-spec.md"
```

If any are missing, print:

```text
No handoff generated.

Missing required artifacts:
  - <missing file>

Required:
  .specwork/_state/<slug>-state.json
  .specwork/_state/<slug>-rules.json
  .specwork/_spec/<slug>-spec.md

Run /sdd:start first.
```

Then exit with no writes.

Do not create `.specwork/_handoff/`.

---

## Step 3 — Open Questions Gate

Scan **only** the body of the `## Open Questions` section — from that heading to the next `## ` heading (or end-of-file) — in both the spec (always) and the plan (when present). Ignore checkboxes elsewhere in either file. This matches the gate used by `/sdd:implement`.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py check-oqs <slug>
```

If the exit code is non-zero, abort with no writes:

```text
No handoff generated.

Unresolved Open Questions detected — resolve them first, then re-run /sdd:handoff.
```

Do not write anything.

Rules:
- Spec Open Questions = business behavior ambiguity. Resolve in the spec.
- Plan Open Questions = discovery/implementation-path ambiguity. Resolve in the plan.
- Both gates are strict and additive — a single unresolved item in either file blocks handoff.
- If the plan file does not exist, only the spec is checked.

Reason:
The handoff pack is for execution only. Ambiguity must be resolved before another model receives the task.

---

## Step 4 — Load Artifacts

Load required:

```text
STATE_FILE
RULES_FILE
SPEC_FILE
```

Load optional artifacts if present:

```text
PLAN_FILE=".specwork/_plan/${SLUG}-plan.md"
CONTEXT_FILE=".specwork/_progress/${SLUG}-context.md"
ESCALATIONS_FILE=".specwork/_progress/escalations.md"
CACHE_FILE=".specwork/_state/${SLUG}-implementation-cache.json"
```

Do not load:
- full repository
- source files
- git diff
- README
- AGENTS.md
- service-rules.md

The handoff must use only existing pipeline artifacts.

---

## Step 4.5 — Worktree Freshness Check

Plans can drift from the worktree between `/sdd:plan` and `/sdd:handoff` — files marked `(new)` may have been created by an earlier implementation pass, or paths the plan referenced may have been deleted in the meantime. A pack generated against a stale plan misleads the executor.

Skip this step entirely when `plan.md` is absent — no Target Files to check.

When `plan.md` is present, parse its `## Target Files` table and validate each row against the worktree. This is a **bounded existence check** (`test -e <path>` per row), not a repository scan — paths come exclusively from the plan.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py worktree-freshness <slug>
```

When the script exits non-zero, surface its output to the user, **make no writes**, and stop — do not proceed to Step 5. This matches the same exit-clean pattern used by the Open Questions Gate (Step 3) and Required Artifacts Check (Step 2).

When the script exits 0, continue to Step 5.

---

## Step 5 — Build Execution Pack

Create:

```text
.specwork/_handoff/<slug>-execution-pack.md
```

The pack is a **curated execution capsule**, not a documentation export. Build it from existing artifacts using the structure below. The order matters — executors degrade on long preambles, so the dense summary goes first.

### Behavioral change signal detection

Before rendering the pack body, detect whether the spec or plan implies modifying existing behavior (not just adding new code). This drives a conditional `## Behavioral Change Warning` section near the top of the pack.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py behavioral-signals <slug>
```

If the script prints any lines, the pack must include the `## Behavioral Change Warning` section (template below) with the detected signals listed. Otherwise omit the section entirely — no header, no empty body.

```markdown
# Execution Pack: <slug>

> Generated by `/sdd:handoff`
> Purpose: model-agnostic implementation capsule

## Role

You are implementing an existing feature spec in an existing codebase.
Do not re-analyze the problem from scratch.
Do not infer missing business rules.
If something is ambiguous, stop and report Open Questions.

If the **Known Architecture Context** (existing-codebase patterns) appears to conflict with the **Spec** (intended behavior), the Spec wins. Existing patterns are background, not constraints.

## Execution Summary

**Goal**: <one sentence from spec `## Summary`>
**Primary class/service**: <first item from spec `## Implementation Context`, or `[UNKNOWN]`>
**Main behavior**:
<verbatim copy of spec `## Behavior` section, max ~10 lines>

## Behavioral Change Warning

<conditional section — render only when the behavioral change signal detection (Step 5 prelude) emitted at least one signal. Omit the entire section, header included, when no signals fired.>

⚠ This spec implies modifications to existing behavior, not a purely additive change. Detected signals:

<bulleted list of the signal labels emitted by the detection script>

Before implementing:
- Verify the current state of the affected code — what does it return / log / persist today?
- Compare against the spec's intended behavior — are there guards, transitions, or side effects to remove or change?
- Do not treat a change as additive just because it adds a new code path. If the new path replaces an existing one, the existing one must also be updated or removed.

When the difference between "additive" and "behavioral" is ambiguous, stop and surface it as an Open Question rather than guessing.

## Known Architecture Context

<built from implementation-cache.json; if the file is missing or all arrays empty, print: "No prior implementation context cached. This is the first run on this feature.">

**Repositories**: <comma-separated `repositories[]`>
**Primary classes**: <comma-separated `similar_classes[]`>
**Patterns**: <bulleted `patterns[]`>
**Related tests**: <bulleted `related_tests[]`>

## Target Files

<verbatim copy of the `## Target Files` table from `.specwork/_plan/<slug>-plan.md`. Omit the entire section (heading and all) if plan.md is missing or has no Target Files table.

The table is the source of truth for which files this feature is allowed to touch. Files marked `[UNVERIFIED]` were not confirmed during `/sdd:plan` discovery — the executor must verify before editing or stop and report.

If the executor confirms an additional file must change that is NOT in this table and is NOT in the plan's `## Out-of-Plan Files` list, treat it as a stop condition (see `## Stop Conditions`).>

## Expected Change Scope

<verbatim copy of spec `## Expected Change Scope` section>

## Safe Constraints

<verbatim copy of spec `## Safe Constraints` section>

## Service Rules

<bulleted list from rules.json: combine `global_rules[]` and `service_rules[]`>

## Execution Budget

- Avoid repository-wide scans.
- Avoid broad refactors.
- Prefer focused diffs.
- Escalate if the implementation expands beyond the Expected Change Scope.

## Failure Handling

- Retry direct implementation failures: max 2 attempts.
- Test setup failures: max 1 retry.
- Escalate infrastructure/environment failures immediately instead of retrying.
- Never rewrite unrelated infrastructure to make a test pass.

## Complexity Indicators

- **Concurrency concerns**: <yes/no — yes if spec contains "async", "concurrent", "thread", "race", "scheduled", "transactional"; otherwise no>
- **Integration scope**: <yes/no — yes if spec mentions endpoints, controllers, repositories, or external integrations; otherwise no>

## Plan

<full contents of `.specwork/_plan/<slug>-plan.md` with the `## Target Files` section stripped (already surfaced above). Omit the entire `## Plan` section (heading and all) if plan.md is missing.

Include: `## Approach`, `## Out-of-Plan Files`, `## Open Questions` (resolved by the Step 3 gate before reaching this point), `## Risks / Constraints`.>

## Spec

<full contents of `.specwork/_spec/<slug>-spec.md`, with the following sections stripped because they were already surfaced above:
- `## Behavior` (now in **Execution Summary → Main behavior**)
- `## Implementation Context` (now in **Execution Summary → Primary class/service** + **Known Architecture Context**)
- `## Expected Change Scope` (extracted verbatim above)
- `## Safe Constraints` (extracted verbatim above)
>

## Focused Context

<contents of `.specwork/_progress/<slug>-context.md` if present; omit section otherwise>

## Known Blockers / Escalations

<contents of `.specwork/_progress/escalations.md` if present; omit section otherwise.
Include the full file verbatim — it is already append-only and concise by construction.
This section warns the executor not to repeat the failed attempts listed.>

## Expected Response From Executor

Return:

1. Files changed (paths)
2. Summary of implementation (≤5 lines)
3. Tests added or updated
4. Tests executed and results
5. Assumptions made (if any)
6. Any unresolved questions or blockers

## Stop Conditions

Stop immediately if:

- Open Questions are discovered.
- Business behavior is ambiguous.
- A service rule conflicts with the requested behavior.
- The implementation needs to touch areas listed under `Avoid touching` in Expected Change Scope.
- An "Unsafe" operation from Safe Constraints would be required.
- Tests reveal behavior outside the requested scope.
- A file outside the `## Target Files` table (and not in the plan's `## Out-of-Plan Files`) appears to require changes.
```

---

## Step 6 — Build JSON Summary

Create:

```text
.specwork/_handoff/<slug>-execution-pack.json
```

Format:

```json
{
  "id": "<slug>",
  "state_file": ".specwork/_state/<slug>-state.json",
  "rules_file": ".specwork/_state/<slug>-rules.json",
  "spec_file": ".specwork/_spec/<slug>-spec.md",
  "plan_file": ".specwork/_plan/<slug>-plan.md",
  "context_file": ".specwork/_progress/<slug>-context.md",
  "escalations_file": ".specwork/_progress/escalations.md",
  "cache_file": ".specwork/_state/<slug>-implementation-cache.json",
  "execution_pack_file": ".specwork/_handoff/<slug>-execution-pack.md",
  "pack_size_bytes": 8421,
  "status": "ready",
  "open_questions_resolved": true,
  "sections_included": {
    "known_architecture_context": true,
    "target_files": true,
    "plan": true,
    "complexity_indicators": false,
    "behavioral_change_warning": false,
    "focused_context": false,
    "escalations": false
  },
  "behavioral_change_signals": [],
  "worktree_freshness": "ok",
  "extracted_sections": [
    "Behavior",
    "Implementation Context",
    "Expected Change Scope",
    "Safe Constraints",
    "Target Files"
  ]
}
```

Fill in `pack_size_bytes` from the byte length of the markdown pack on disk (e.g. `python3 -c "import os; print(os.path.getsize(p))"`).

`extracted_sections` lists which sections of the source artifacts were lifted into the upper structured sections of the pack (and therefore stripped from the embedded `## Spec` / `## Plan`). Only include section names that were actually present in the source — if the spec didn't have an `## Expected Change Scope` section, or plan.md didn't have a `## Target Files` table, do not list it here.

If optional files are missing:
- Use `null` for the path (e.g. `"plan_file": null`).
- Set the corresponding `sections_included` flag to `false`.

`behavioral_change_signals` contains the lines emitted by the Step 5 behavioral signal detector (empty array when no signals fired). When non-empty, `sections_included.behavioral_change_warning` must be `true`.

`worktree_freshness` is `"ok"` when Step 4.5 found no discrepancies (the only case where the pack is generated at all). It is reserved for future expansion — when Step 4.5 fails, the pack is not generated and no JSON file is written.

---

## Step 7 — Summary

Print:

```text
Handoff pack created.

Pack:
  .specwork/_handoff/<slug>-execution-pack.md

JSON:
  .specwork/_handoff/<slug>-execution-pack.json

Use this pack with Gemini, Copilot, Codex, or Claude as an implementation contract.
```

Do not print the full pack content.

---

## Hard Rules

- Do not scan the repository for new content. Bounded existence checks (`test -e`) against paths already named in `plan.md` Target Files are allowed — they are gates, not discovery.
- Do not enrich the spec — verbatim extraction from existing artifacts only.
- Do not generate implementation details.
- Do not resolve Open Questions.
- Do not create partial handoff output.
- Do not read AGENTS.md or the `.claude/rules/` files (or a legacy `service-rules.md`) directly —
  their rules are already captured in `rules.json`.
- Use only `.specwork` artifacts (plus bounded path checks from Step 4.5).
- Missing required artifacts means exit with no writes.
- `Execution Budget` and `Failure Handling` are fixed boilerplate — do not customize per feature.
- `Complexity Indicators` may flip yes/no flags based on simple keyword presence in the spec, but must not synthesize new content.
- `Behavioral Change Warning` content is fixed boilerplate; only the list of detected signals is filled in from the Step 5 detection script.
- `plan.md` is optional — when present, its `## Target Files` and body are embedded; when absent, the pack is built from spec alone (and Step 4.5 is skipped).
- Worktree freshness discrepancies are a gate — exit clean, no writes, surface the discrepancies and ask the user to re-run `/sdd:plan`.

---

## Related Skills

- `start` — creates the state, rules, source, and execution spec
- `implement` — implements inside the current pipeline
- `commit` — commits implementation
- `mr` — creates merge request description
