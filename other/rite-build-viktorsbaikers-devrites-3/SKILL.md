---
name: rite-build
description: Build the next approved vertical slice with evidence. HITL one-slice default; AFK/autocomplete refill eligible isolated work under --parallel N, one global writer cap under Autocomplete.
argument-hint: "[--parallel N] [slice number or name]"
user-invocable: true
---

<!-- loads: {"always":["devrites-lib/reference/parallel-workspaces.md","devrites-lib/reference/standards/core.md","devrites-lib/reference/standards/code-navigation.md","devrites-lib/reference/standards/code-index.md","devrites-lib/reference/standards/agents.md","rite-build/reference/phase-contract.md","rite-build/reference/one-slice-cycle.md","rite-build/reference/wright-dispatch.md","rite-build/reference/checkpoint.md","rite-build/reference/spec-drift-guard.md","rite-build/reference/output.md","rite-build/reference/anti-patterns.md"],"rootOnly":["devrites-lib/reference/standards/code-index.md","devrites-lib/reference/parallel-workspaces.md","rite-build/reference/phase-contract.md","rite-build/reference/wright-dispatch.md","rite-build/reference/checkpoint.md","rite-build/reference/output.md","rite-build/reference/afk-discipline.md","rite-build/reference/checkpoint-protocol.md","rite-build/reference/parallel-batch.md","devrites-lib/reference/standards/afk-hitl.md","devrites-lib/reference/standards/workflow-artifacts.md"],"triggers":{"afk":["rite-build/reference/afk-discipline.md","devrites-lib/reference/standards/afk-hitl.md","rite-build/reference/checkpoint-protocol.md"],"applicability":["devrites-lib/reference/standards/repository-topology.md","devrites-lib/reference/standards/data-integrity.md","devrites-lib/reference/standards/integration-reliability.md"],"coding":["devrites-lib/reference/standards/coding-style.md"],"debug-recovery":["devrites-lib/reference/standards/debug-recovery.md"],"dod":["devrites-lib/reference/standards/definition-of-done.md"],"errors":["devrites-lib/reference/standards/error-handling.md"],"frontend":["rite-build/reference/frontend-trigger.md"],"parallel":["rite-build/reference/parallel-batch.md","devrites-lib/reference/parallel-workspaces.md"],"patterns":["devrites-lib/reference/standards/patterns.md"],"principles":["devrites-lib/reference/standards/principles.md"],"security":["devrites-lib/reference/standards/security.md"],"tdd":["rite-build/reference/tdd.md","devrites-lib/reference/standards/testing.md"],"workflow-artifacts":["devrites-lib/reference/standards/workflow-artifacts.md"]},"workspace":["brief.md","spec.md","state.md","decisions.md","assumptions.md","questions.md","decision-coverage.md","architecture.md","plan.md","tasks.md","traceability.md","eng-review.md","test-plan.md","gates.md","strategy.md"],"workspaceByRole":{"code-reviewer":["spec.md","plan.md","tasks.md","test-plan.md","architecture.md","decisions.md","state.md"],"doubt-reviewer":["spec.md","plan.md","tasks.md","state.md","decisions.md"],"slice-wright":["brief.md","spec.md","architecture.md","plan.md","tasks.md","test-plan.md","state.md","decisions.md","assumptions.md","questions.md"],"test-analyst":["spec.md","tasks.md","test-plan.md","state.md"]}} -->
> Read-set manifest: `devrites-engine context --skills-root .dsh/skills <slug> --phase build` bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.


# /rite-build: one verified slice

Active caller takes precedence per [output.md](reference/output.md#caller-owned-continuation).
Standalone HITL stops; standalone AFK chains under green proof, caps and pause
rules. Every wright returns after one slice.
**HITL:** `/rite-build --parallel N` (2≤N≤10; N=1≡serial) follows
[`reference/parallel-batch.md`](reference/parallel-batch.md)
([`one-slice-cycle.md`](reference/one-slice-cycle.md)).

Root owns gates/bookkeeping; fresh
[`devrites-slice-wright`](../../agents/devrites-slice-wright.md) writes source/tests.
Workflow Artifacts use
[`workflow-artifacts.md`](../devrites-lib/reference/standards/workflow-artifacts.md)
(trigger `workflow-artifacts` — only when the plan declares them).
Execute [`reference/phase-contract.md`](reference/phase-contract.md)
([`one-slice-cycle.md`](reference/one-slice-cycle.md),
[`afk-discipline.md`](reference/afk-discipline.md)); dispatch uses
[`reference/wright-dispatch.md`](reference/wright-dispatch.md).
Every wright contract names the writer-safe checks the wright runs (syntax/type/lint,
unit and self-check suites, a narrow local smoke) and never forbids them; only
artifact-producing, consumptive, or full canonical gates stay root-owned, and a
`RUN: writer` gate adds `gates precheck` to them;
`dispatch open --contract` refuses a contract that breaks this. Prior contracts in `evidence.md` are not a template for this. **Failing case:** the
contract says "skip tests mid-flight; root runs them after return", and the wright
returns three unit failures that a 20 s `go test` would have caught in-round.

## Required rules

Read `.dsh/skills/devrites-lib/reference/standards/core.md` first. Load only triggered rules:
coding/error/testing/[`tdd.md`](reference/tdd.md)/patterns/DoD; binding
`.devrites/principles.md`; security; topology; data integrity; integration reliability.
Wright applies anti-slop; root verifies returns and never patches source. Refuse the rationalizations in
[`anti-patterns`](reference/anti-patterns.md).

## Invariants

- Standalone HITL default: serial on control (core.md #5). AFK/`--parallel N`
  uses [`parallel-batch.md`](reference/parallel-batch.md).
  Same-worktree multi-writer / root-emulated concurrency forbidden.
  Native-worktree pilot = single-slice isolation when `wright-dispatch.md`
  preflight + reconcile hold.
- Exact feature scope only (core.md #7); reject out-of-allowlist diffs
  (`devrites-engine check diff-scope <slug> --allow <contract-paths>`); record
  adjacent issues. An adjacent issue or non-obvious rationale bound to specific
  code anchors as a note — `devrites-engine note add <slug> <file> "<verbatim
  quote>" <title>` — so refactors regrade it instead of losing it
  ([`notes.md`](../devrites-lib/reference/workspace-artifact-schema.md#anchored-notes)).
- Re-prove affected behavior after edits (core.md #6); reuse observations only
  under [evidence validity](../devrites-lib/reference/candidate-integrity.md#evidence-validity).
- Unplanned dependency/design-system/gap/repair → Vet/Spec Drift Guard batch
  sweep: every contract-assumption violation recorded before one folded
  repair+vet. Ask only for licensing/cost/security/product or explicit
  architecture-policy decisions (core.md #8).
- Root never edits product source/tests (`.devrites/` + Workflow Artifact only;
  [agents.md](../devrites-lib/reference/standards/agents.md) source-writing
  boundary). Wright is sole product writer; extras in returned paths/`git diff
  --name-only` hard-stop via `check diff-scope`.
- Principles bind; irreversible conflict needs human exception or stop.
- Evidence beats confidence (core.md #6). Never weaken tests, skip TDD, widen
  writers, or self-approve. Drift →
  [`spec-drift-guard.md`](reference/spec-drift-guard.md); checkpoint →
  [`checkpoint.md`](reference/checkpoint.md).
- Async readiness waits during slice work follow
  [`debug-recovery.md`](../devrites-lib/reference/standards/debug-recovery.md)
  (bounded poll + last-signal artifact; no blind sleep as primary strategy).

## Workflow Artifact branch

<!-- workflow-artifact-adapter: {"module":"devrites-lib/reference/standards/workflow-artifacts.md","entry":"Vet-ready admitted bytes require root authorship outside product wright","action":"ROOT_TRANSACTION; root writes only admitted .devrites/** targets","return":"saved Build slice cursor; wright product allowlist unchanged"} -->
## `--parallel N` (opt-in)

Standalone HITL default/explicit `1` ≡ serial; AFK inherits cap. Under
Autocomplete, read and execute shared root-only
[`parallel-workspaces.md`](../devrites-lib/reference/parallel-workspaces.md)
(trigger `parallel`, including global cap 1): controller/source routing,
authorized pool, isolated first writer and continuous repair/re-Vet/refill.
Standalone Build remains local. `2`–`10` is a cap, not a quota; eligible
path-disjoint work refills after each landing
([`parallel-batch.md`](reference/parallel-batch.md#dynamic-selection-and-re-batching)).
Unattended runs (`/rite-autocomplete`, `.devrites/AFK` `max_parallel`) refill
inside the same run; HITL stops after each landing. This invocation's `--parallel N`
is the cap: leftover sentinel `max_parallel` is not consulted. Autocomplete with
that flag also writes or replaces only `max_parallel: N`. Non-integer/`N≤0`/`N>10` hard refuse.
Each sibling lands alone when its review + proof are green (`integrate --slice`):
one local `WIP(<slug>):` commit onto the control branch (never pushed). Do not
integrate a sibling because the wright returned. A red/gap sibling gets a bounded repair
round in its own worktree — never rebuilt from scratch while budget remains.
Post-writer inventory and affected rechecks follow `phase-contract.md` § Independent
Build review; fold accounts before one repair-all wright.
Plan-owned gaps still route through Spec Drift Guard
(batch sweep, one folded plan repair + one vet recheck inline); do not emit
a human `Fix`. Exhausted repair blocks and preserves everything;
`cleanup --force` salvages slice branches before removing worktrees —
human-gated to abandon a batch, orchestrator-emitted only as the salvage
step of an automatic frozen-lease re-batch.
AFK charges per landed sibling only. A retained lease resumes through its
controller; it blocks a competing Build root, not controller-owned source dispatch.
Details: `parallel-batch.md`.

## Execute and reply

Run every step in `reference/phase-contract.md`: readiness, one target, dispatch
or canonical transaction, return inspection, independent code/doubt/test analysis,
approved fail-on-red proof, record, and applicable accounting. Continue/reply via
[`reference/output.md`](reference/output.md) plus the shared
[`reply contract`](../devrites-lib/reference/reply-contract.md). Standalone AFK obeys remaining budget; Prove requires every slice built except a
[deferred slice](../rite-plan/reference/slicing.md#deferred-slice).

## Phase exit

**Complete when:** Independent Build review and fail-on-red proof are green,
`git diff --name-only` ⊆ allowlist, no open Critical/Important, `state.md` cursor
advances with recorded evidence, and the control-branch checkpoint has landed
per [`checkpoint.md`](reference/checkpoint.md).

**Failing case:** wright reports "done" but independent review or proof was
skipped, red, or followed by an uncommitted repair → slice incomplete; do not
advance cursor or commit on control.
