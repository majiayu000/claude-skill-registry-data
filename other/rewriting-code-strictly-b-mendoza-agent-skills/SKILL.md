---
name: "rewriting-code-strictly"
description: "Rewrite existing Python, TypeScript/JavaScript, or Go code for strict static typing, boundary validation, and maintainable idioms while preserving behavior. Use when the user asks to harden code, remove unsafe escape hatches, add validation, or align with mypy, Pyright, tsc, go vet, or Staticcheck. Coordinates baseline mapping, strategy, approved implementation, and review through co-located subagents and just-in-time language references."
---

# Rewriting Code Strictly

Strict-rewrite orchestrator for behavior-preserving Python, TypeScript/JavaScript, or Go rewrites. Think, decide, and dispatch one subagent at a time; keep only status, decisions, validation verdicts, changed paths, risks, and material URLs.

## Inputs

| Input                     | Required | Example                                     |
| ------------------------- | -------- | ------------------------------------------- |
| `TARGET_CODE`             | Yes      | `src/api/users.py` or pasted code           |
| `LANGUAGE`                | No       | `python`, `typescript`, `go`                |
| `USER_GOAL`               | No       | `"make this strict and easier to maintain"` |
| `VALIDATION_COMMAND`      | No       | `mypy src/api/users.py`                     |
| `SCOPE_LIMITS`            | No       | `"do not add dependencies"`                 |
| `REFERENCE_NEED`          | No       | `"Pydantic strict mode"`                    |
| `EXTERNAL_FETCH_APPROVAL` | No       | `"approved for Pydantic docs only"`         |

Missing `TARGET_CODE` or unclear language → one focused question before dispatch.

## Output Contract

Handoff order: (1) original behavior, (2) weaknesses, (3) typing vs validation decisions, (4) files/code, (5) validation results, (6) references used or unavailable, (7) assumptions/risks, (8) gate evidence for `G_STRICT_STRATEGY_APPROVAL`, `G_MUTATION_SCOPE`, `G_IMPLEMENTATION_VALIDATION`, `G_STRICT_REVIEW_PASS`, `G_FINAL_HANDOFF_EVIDENCE`.

Stops (`NO_CHANGE`, `NEEDS_CLARIFICATION`, `BLOCKED`, `ERROR`): status, smallest reason, next decision, any validation already completed.

## State Machine Overview

Mermaid: [`flow-diagram.md`](./flow-diagram.md). Table: [`state-machine.md`](./state-machine.md).

| Group              | Result                                                         |
| ------------------ | -------------------------------------------------------------- |
| Intake gates       | Target, language, scope; derive `MUTATION_LIMITS`              |
| Baseline           | Mapper; `NO_CHANGE_CANDIDATE` continues (not a stop)           |
| Strategy           | Strategist; only `NO_CHANGE` stops before edits                |
| Gates + approval   | Check gates; `AskApproval` **resumes implement on approve**    |
| Implement / review | Mutate, review; ≤2 repairs re-enter implement                  |
| Terminals          | `PASS`, `NO_CHANGE`, `NEEDS_CLARIFICATION`, `BLOCKED`, `ERROR` |

## Pipeline Overview

| Phase     | States                                     | Execution                    | Output                    |
| --------- | ------------------------------------------ | ---------------------------- | ------------------------- |
| Intake    | `Intake`…`DeriveLimits`                    | Inline; personality          | Packet + limits           |
| Baseline  | `DispatchBaseline`/`RouteBaseline`         | `strict-baseline-mapper`     | `STRICT_BASELINE`         |
| Strategy  | `DispatchStrategy`/`RouteStrategy`         | Strategist + one playbook    | `STRICT_STRATEGY`         |
| Gates     | `CheckGates`/`GateExpansion`/`AskApproval` | Inline                       | Proceed, block, or resume |
| Implement | `DispatchImplement`/`RouteImplement`       | `strict-rewrite-implementer` | `STRICT_IMPLEMENTATION`   |
| Review    | `DispatchReview`…`GateFixCycles`           | Reviewer; repair → implement | `STRICT_REVIEW`           |
| Handoff   | `Handoff`→`TerminalPass`                   | Inline                       | Final response            |

## Subagent Registry

| Subagent                     | Path                                        | Purpose                                |
| ---------------------------- | ------------------------------------------- | -------------------------------------- |
| `strict-baseline-mapper`     | `./subagents/strict-baseline-mapper.md`     | Read-only baseline map                 |
| `strict-rewrite-strategist`  | `./subagents/strict-rewrite-strategist.md`  | Playbook, optional fetch, minimal plan |
| `strict-rewrite-implementer` | `./subagents/strict-rewrite-implementer.md` | Apply rewrite; run authorized checks   |
| `strict-rewrite-reviewer`    | `./subagents/strict-rewrite-reviewer.md`    | Independent review verdict             |

Read a subagent only when dispatching it.

## Progressive Loading Map

Load only what the current decision needs. Paths here are relative to this `SKILL.md`; later files use their own relative paths.

| Need                         | Load                                                            |
| ---------------------------- | --------------------------------------------------------------- |
| Posture                      | `./references/personality.md`                                   |
| Python / TS/JS / Go defaults | matching `./references/*-playbook.md`                           |
| External URL map             | `./references/external-sources.md` (orchestrator or strategist) |
| Examples                     | `./references/orchestration-examples.md`                        |
| State machine                | `./flow-diagram.md`, `./state-machine.md`                       |
| Subagent contract            | `./subagents/<name>.md` at dispatch                             |

One playbook after language is known. Playbooks do not chain-load `external-sources.md`; the map and strategist own that hop. Pass package-root-relative paths at dispatch; subagents may use `../references/...`.

Fetch URLs only with `REFERENCE_NEED`, `EXTERNAL_FETCH_APPROVAL`, or project-local required evidence. Unavailable URL → local evidence + risk, or `NEEDS_CLARIFICATION`. Network is optional for normal runs.

## Default Mutation Limits

Derive in `DeriveLimits`. Unless `SCOPE_LIMITS` expands them: write only in `TARGET_CODE` and direct compilation/typing/import/test consequences; preserve behavior, public contracts, deps, settings, unrelated work; no new deps, broad cleanup, public API, private config, generated artifacts, or repo tooling without approval; repairs stay on reviewer-named fixes inside limits. Out-of-limits need → clarify or expand before editing. Reports include mutation-boundary evidence.

## Critical Output Gates

| Gate                          | Evidence                                                |
| ----------------------------- | ------------------------------------------------------- |
| `G_STRICT_STRATEGY_APPROVAL`  | Status, non-goals, approval items, validation plan      |
| `G_MUTATION_SCOPE`            | Limits, planned/actual paths, expansions                |
| `G_IMPLEMENTATION_VALIDATION` | Commands, results, unavailable/unapproved notes         |
| `G_STRICT_REVIEW_PASS`        | `STRICT_REVIEW: PASS` or blocked findings after repairs |
| `G_FINAL_HANDOFF_EVIDENCE`    | Gate verdicts, files, validation, references, risks     |

## Core Decision Rule

Static types for stable internals; runtime validation at trust boundaries; convert boundary data to typed internals before deeper use; keep escape hatches local and justified. Project settings outrank playbook defaults when stricter.

## Execution Steps

Advance [`state-machine.md`](./state-machine.md):

1. **Intake → `DeriveLimits`.** Load personality; derive limits. Ask* resumes prior gate when answered; unattended → `TerminalNeedsClarification`.
2. **`DispatchBaseline`.** Route `PASS | NO_CHANGE_CANDIDATE | NEEDS_CLARIFICATION | ERROR`. `PASS` and `NO_CHANGE_CANDIDATE` both continue to strategy.
3. **`DispatchStrategy`.** Route `PASS | NO_CHANGE | NEEDS_CLARIFICATION | ERROR`. `NO_CHANGE` → `TerminalNoChange` without edits.
4. **`CheckGates` → `GateExpansion` → optional `AskApproval`.** On expansion need, ask once. **Approve → `DispatchImplement`.** Decline → `TerminalBlocked`. No reply → `TerminalNeedsClarification`. Missing validation command → continue with implementer warning evidence.
5. **`DispatchImplement`.** Route `PASS | PASS_WITH_WARNINGS | BLOCKED | ERROR`; check scope and validation gates; then review or terminal.
6. **`DispatchReview`.** `PASS` → handoff. `FAIL` with fixes and `repair_counter` under 2 → re-enter **`DispatchImplement`**. Else `TerminalBlocked`.
7. **`Handoff` → `TerminalPass`** with Output Contract and final gate evidence.

## Validation Loop Summary

`map → plan → gate/approve → change/check → review → targeted fix → re-check`. Implementer owns authorized checks; reviewer covers drift checks may miss.

## Example

`TARGET_CODE=src/payments/webhook.ts`, remove unsafe `any`, validate webhook, `REFERENCE_NEED` for Zod. Mapper finds TS + untrusted body. Strategist loads typescript playbook and, only if needed, `external-sources.md` + approved Zod URL. No expansion → implement → review → handoff. See `./references/orchestration-examples.md` for approval resume, no-change, and unavailable-reference round-trips.
