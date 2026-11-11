---
name: pair-workflow-contract-phase
description: "Phase 0 of the delivery workflow: ensures the machine contract derived from a KB markdown template (verdict options, severities with explicit ranks, finding fields) is fresh — cache-by-hash via ensure-contract.mjs, regenerated only when the template changed — and returns it as the enum-locked return-value schema the reviewer is held to. Never modifies the template. Dispatched by the batch engine (pair-implement-batch)."
version: 0.1.0
author: Foomakers
---

# /pair-workflow-contract-phase — The Template Is the Truth, the Contract Is Its Cache

Derive the machine contract from the human template so the reviewer's structured output and the human-facing report can never drift apart.

## Arguments

| Argument    | Required | Description                                                                                             |
| ----------- | -------- | ------------------------------------------------------------------------------------------------------- |
| `$name`     | Yes      | Contract name (e.g. `code-review`).                                                                     |
| `$template` | Yes      | Path of the KB markdown template — the source of truth.                                                 |
| `$contract` | Yes      | Path of the `*.contract.json` artifact (git-ignored derived cache).                                     |
| `$skeleton` | Yes      | JSON: the loose return-value schema to tighten. Only the fields `$mirrors` names become `enum`s.        |
| `$mirrors`  | Yes      | Which schema fields mirror which template vocabulary, and the severity-rank rule.                        |

## Algorithm

**Headless execution (single owner: `.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/headless-stage-execution.md`)** — this stage runs headless: never leave a command in the background and never end your turn while a command runs (a push with a pre-push gate, a quality gate): use the maximum tool timeout, poll to completion in the same turn, and ALWAYS end with the stage's structured result — on partial progress `{ status: "failed", reason: "incomplete", detail, branch, outputHead }`.

> Since 4.0.1 (t9d-2, AC-06) this skill is invoked by the FIRST review dispatch of a run (`$contractSpec`), not by a generator-only dispatch: the same steps, the same cache-by-hash, returned as the review's `templateContract`.

1. Run `node "$SKILL_DIR/scripts/ensure-contract.mjs" check $template $contract` — where `$SKILL_DIR` is the directory this SKILL.md was loaded from; the script ships beside it ([scripts/ensure-contract.mjs](./scripts/ensure-contract.mjs)) — for ALL hash/cache/validation work; never hand-roll hashing or freshness logic.
2. `fresh` ⇒ return the cached contract file content unchanged with `status: cache-hit`.
3. Otherwise READ the template and generate the contract: take `$skeleton` and tighten ONLY the fields `$mirrors` names into `enum`s, leaving every other field untouched. Fill `vocabulary` (`verdictOptions`, `severities`, `findingFields`, …) from the template, AND the top-level `severityRanks`: every name in `vocabulary.severities`, spelled identically, mapped to an explicit unique integer, HIGHER = MORE SEVERE. Derive each rank from what the template SAYS the level means — a must-fix/merge-blocking level outranks an advisory one or a question — NEVER from the order the levels appear in: the consumer ignores array order, and a wrong rank silently converts a merge-blocking finding into an accepted one. If the levels carry no discernible relative severity, return `status: failed` rather than inventing an order.
4. Persist via `node "$SKILL_DIR/scripts/ensure-contract.mjs" write $template $contract <draft.json>` (it validates the draft and stamps the template hash); return `status: regenerated` plus the final contract content.
5. Never modify the template. If generation or validation fails after one retry, return `status: failed` with no contract.

## Output Format

`{ status: cache-hit | regenerated | failed, contract?: { $meta, vocabulary, severityRanks, schema } }`.
