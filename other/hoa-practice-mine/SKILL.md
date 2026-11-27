---
name: hoa-practice-mine
description: >-
  Mine local Claude Code, OMP, and Codex session history and project memory stores
  for reusable operational guardrails and unknown unknowns using two-level pruning,
  multi-head `/v1/decisions` probes, residual active learning, and raw-line verification.
  Explicit invocation only. Use hoa-practice-retro for periodic cross-repo retros
  and rubric-tune for iterative rubric refinement.
disable-model-invocation: true
metadata:
  revision: "3"
  areas: "self-management,software-development"
  targets: "runtime-agnostic"
  summary: "mine local session history and memory stores for reusable guardrails and unknown unknowns using a decision model"
  summary_zh: "用 Decision Model 低成本挖掘本地会话与记忆中的可复用护栏和未知盲区"
  kind: "entry"
---

# hoa-practice-mine

Extract reusable operational guardrails, hidden failure modes, and workflow rules
from local Claude Code, OMP, and Codex session history without linear full-text
rereads, closed-set Softmax blind spots, or prompt calibration drift.

## Gates

- **Domain and secret isolation before model calls.** Classify project directories
  before reading transcripts. Physically skip out-of-scope or corporate checkouts
  and mixed scratch directories. Use `--allow-regex` / `--deny-regex` in mixed
  stores; omit them only when all checkouts under the supplied roots are in scope.
  Deny matches take precedence.
- **Redact locally.** Strip credentials, bearer tokens, private endpoints, and
  agent-workflow prompt-injection boilerplate frames before sending any state to a
  decision endpoint. Apply this to extracted spans, memories, and the rules
  baseline. Never forward the unredacted evidence from `hoa history show`.
- **Read-only stores and gitignored scratch.** Never mutate source stores, WAL
  files, or repositories during mining. Put intermediates, ledgers, and any cursor
  in an outside-worktree state directory or one confirmed by `git check-ignore`.
- **Advisory probabilities, primary-agent proof.** Probabilities rank and route;
  they never prove a root cause or authorize an edit. Verify every surviving
  candidate against raw session lines or read-only SQLite ordinals and live
  repository files before proposing changes.
- **Gold-anchor monotonicity.** Never adopt a revised rubric (`v2+`) unless
  `anchor-check` passes for the endpoint: zero false negatives and a worst-case
  positive-vs-negative margin at least as wide as the baseline on the locked
  anchor set (`>= 8` positives + `>= 8` negatives).

## Workflow

1. **Extract** redacted L0 session skeletons and L1 causal spans from only the
   selected roots. Account for coverage in `extract-manifest.json`; add memories
   only when they are in scope.
2. **Prune at L0.** Score whole-session skeletons and retain pivot spans from
   surviving sessions. Keep model refusals and request failures eligible; do not
   count them as clean. Audit the top 5–8 pruned sessions near the boundary.
3. **Scan and reflect at L1.** Score the surviving spans with orthogonal heads.
   Use bundled `l1-v2` directly once its anchor check has passed for the endpoint;
   use `l1-v1` first only when iterating on a custom taxonomy. Inspect residuals,
   preserve the anchors, and apply the [stopping criterion](references/methodology.md#stopping-criterion).
4. **Reconcile at L3.** Compare strong non-routine survivors (and included memories)
   against live rules. Separate `target_gap`, `route_to_sibling_repo`, and
   `already_covered`, then verify every surviving gap in its source and live repo.

## What to read and when

Read the runbook for the stage you are about to execute. For a resumed run, load
only that stage and the references its inputs require. All examples use `hoa`;
its invocation options are in the extraction runbook.

| When to read | Reference |
|---|---|
| Before extracting, resuming from a history cursor, or setting up the CLI for any stage | [Extract](references/extract.md) |
| When using a selected history source; skip adapters for sources not in scope | [Claude Code](references/sources/claude-code.md), [OMP](references/sources/omp.md), [Codex](references/sources/codex.md) |
| Before scoring skeletons, selecting pivots, or auditing pruned sessions | [L0 pruning](references/l0-pruning.md) |
| Before scoring L1 spans, inspecting residuals, or checking a rubric revision | [L1 residuals](references/l1-residuals.md) |
| Before novelty scoring, verifying evidence, or producing the report | [L3 reconciliation](references/l3-reconciliation.md) |
| Before configuring or changing the decision endpoint | [Endpoint settings](references/endpoint-configuration.md) and [configuration lookup](references/configuration.md) |
| When interpreting probes, residual formulas, or when to stop refining | [Methodology](references/methodology.md) |
| Only if a CLI command fails | [Troubleshooting](references/troubleshooting.md) |
| When checking explicit-only invocation on Codex | [Codex policy](agents/openai.yaml) |

## Report

For each verified finding, report
`evidence locator -> concrete harm -> live coverage -> minimal fix -> canonical owner`.
Use physical source lines, SQLite history `rollout_ordinal` values, or SQLite
memory row identifiers, as applicable.
Keep unverified model suggestions out of the verified findings.
