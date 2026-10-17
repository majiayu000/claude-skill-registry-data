---
name: review-correctness
description: Review code for bugs, incorrect state transitions, races, and failure handling, including closed-world branching, unknown external values, swallowed errors, masking defaults, invariants, deadlines, cancellation, and retry safety. Use for "review correctness", "review logic", "review defensive", "check exhaustiveness", "fail fast review", or "robustness review".
argument-hint: '[target] [--staged | --unpushed | --changed | --all]'
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Review Correctness

Check correct behavior under normal inputs, failures, and changing assumptions. Perform both passes below; a general bug scan does not replace the failure-path checklist.

Read `references/defensive-checklist.md` for examples, language-specific exhaustiveness mechanisms, and supporting sources when a finding needs them. Follow this skill's ownership and evidence rules when using those examples.

## Instructions

1. Resolve the scope. When called by `code-review`, use its supplied file list and diff scope without recomputing them. An explicit target selects those files or directories; otherwise use the Scope table.
2. Read applicable `AGENTS.md` / `CLAUDE.md` and the contracts and tests around the scoped code. Trace callers, dependencies, and observable results, including guards outside the diff.
3. Perform Pass 1 and Pass 2. When a change extends an enum, union, status set, or response type, search the repository for every consumer: switches, match arms, predicate chains, lookup maps, and membership tests. Include newly affected branches outside the initial file list.
4. Verify each finding's trigger, path, and consequence. Inspect guarantees from callers, types, framework configuration, and dependency defaults before claiming a check is missing. For a future-value finding, name the extension and show why it would take the wrong handler; distinguish this from an input already possible today.
5. Apply the ownership rules below, deduplicate findings with the same root cause, and report. Do this work yourself; do not dispatch sub-agents or launch other agent CLIs. If execution tools are unavailable, ask the parent for a specific verification and report any unresolved limitation.

**Read-only, including temporarily.** Do not edit the reviewed checkout. Run experiments only in a disposable copy, subject to the project's instructions. Do not create worktrees or change git state without authorization.

## Scope

| Flag | Scope | Method |
|------|-------|--------|
| (none) | Context-related code | Files from the current conversation context: any files the user has discussed, opened, or that you have read/edited in this session. If no conversation context exists, ask the user to specify files or use `--staged`/`--changed`/`--all`. |
| `--staged` | Staged changes | `git diff --cached --name-only` |
| `--unpushed` | Files changed across unpushed commits | `git diff --name-only $(git rev-list HEAD --not --remotes \| tail -1)^..HEAD` |
| `--changed` | Unstaged changes | `git diff --name-only` |
| `--all` | Full codebase | Enumerate source files |

`--unpushed` derives its range from `git rev-list HEAD --not --remotes` (oldest unpushed commit's parent → HEAD). If nothing is unpushed, or there is no remote/upstream (or the range walks back to the root commit) so it can't be determined reliably, stop and ask the user to pick another scope.

## Pass 1: Normal behavior and state transitions

- Trace the intended behavior from inputs to observable output. Check predicates, arithmetic, units, ordering, indexes, off-by-one errors, empty collections, null/undefined values, and boundary inputs.
- Check state transitions and multi-step operations: prerequisites enforced before side effects, partial writes, rollback or recovery, and whether reported success means the work actually completed.
- Trace races and ordering: check-then-act, concurrent updates, state assumed unchanged across an await, stale results applied after newer ones, and duplicate execution.
- Verify each calculation's invariants (non-empty or sorted input, exactly one match, valid balances). Do not demand a local assertion when callers or types already guarantee the condition.
- Follow return values and errors across callers. Check ignored results, short writes, affected-row counts, and unawaited work whose completion is required.

## Pass 2: Failure paths and changing assumptions

### Exhaustiveness

- Flag a final `else`, `default`, or wildcard that handles one specific known case by elimination, including negated predicates such as `status != cancelled` meaning active.
- Check lookup maps with fallbacks that disguise a missing handler. Check parallel case lists for a missing or inconsistent case; structural duplication alone belongs to design reviewers.
- Preserve compile-time exhaustiveness where the language supports it. Use the language's own mechanism; do not demand a TypeScript helper in a language with native exhaustive matching.
- An open-domain fallback is valid when it is intentionally correct for future values. A required wildcard for an extensible external type is not itself a defect. Ask what behavior it performs.

### Unknown external values

- Trace API, DB, config, message, and user-input decoding through consumers. Unknown values must be deliberately rejected, represented, or handled, rather than silently coerced into a known case.
- Judge rejection versus tolerance against the actual contract. Rejecting unknown input is not automatically a bug, and adding an unknown variant is not always required.
- Check whether one malformed or unsupported item should fail a whole batch or be isolated. Neither skipping nor continuing is automatically safe: check atomicity, data loss, and how the failure reaches the caller or operator.
- Assertions that disappear in the supported runtime/build configuration must not be the only validation of external input.

### Silent failure and misleading defenses

- Empty catches, broad catches that absorb errors the handler cannot recover from, and log-and-continue paths that leave incomplete state.
- Plausible defaults (`0`, empty strings/collections, default enum values) that conceal a missing required value or broken upstream contract.
- Retries or fallbacks that conceal persistent failure with no usable error signal.
- Guards that silently skip required work, catches that convert failure to success, and fallbacks that continue with corrupt state. Harmless redundant checks alone belong to design review.
- Contradictory validation that rejects valid input, or validation after an irreversible side effect. Validation placement without a behavioral defect belongs to design/architecture.

### Completion, cancellation, and retry safety

- Operations that can hang beyond their caller's deadline: network, IPC, database, subprocess, or blocking waits. Inspect inherited deadlines, library defaults, and intended lifetime before recommending a local timeout.
- Retries that never terminate, ignore cancellation, or repeat a non-idempotent effect after an ambiguous result. Check whether a timeout leaves background work running or a late result can still change state.
- Locks, transactions, files, and temporary state whose error/cancellation cleanup is required for correct behavior. Check release, rollback, and recovery on every relevant path.
- Non-terminating loops, recursion, and pagination, including repeated cursors. Capacity limits for large but terminating work belong to performance or security review.

## Ownership boundaries

Assign the finding by its demonstrated consequence, not by the syntax of the fix. A concrete behavioral bug remains reportable even if a type or architecture change is the best repair. Do not suppress it merely because another reviewer could also discover it; the parent deduplicates shared root causes.

| Concern without a demonstrated behavioral defect | Primary reviewer |
|---|---|
| Invalid field combinations, weak domain types, error-type/API modeling | Language review for representation; `review-interfaces` for public contracts |
| Repeated validation, duplicated case tables, redundant guards | `review-cleancode`; `review-architecture` for placement across modules |
| Retry amplification across layers, backoff/jitter policy, failure isolation and cascading failures | `review-architecture` |
| Growing caches, buffers, queues, large reads, missing pagination, accumulated connections/listeners | `review-perf` |
| Attacker-controlled exhaustion, injection, authn/authz, security validation | `review-security` |
| Hidden shared state, effect placement, mutation of caller-owned data | `review-functional`; trace concrete race/order failures here |
| Missing tests or weak assertions | `test --review`; lack of a test alone is not a correctness finding |
| Version-specific library contracts and required API setup | `review-library-use`; use its documented conventions as evidence when tracing behavior |

For diff scopes, report defects introduced or exposed by the change, including newly affected consumers outside the diff. For explicit whole-file or whole-repo audits, review all selected behavior.

## Output

When called by `code-review`, follow its mode-specific finding and scoring instructions: comprehensive mode uses independent scorers, while quick mode uses the integrated reviewer’s self-verification. Standalone, group findings as Critical, Should Fix, or Nice to Have according to concrete consequences, reachability, and scope. Do not assign a severity floor to exhaustiveness/timeouts or a ceiling to misleading guards.

Each finding includes:

- `file:line`, the problem, and its consequence.
- **Trigger:** the specific input, state, interleaving, failure, or future extension, with the path and relevant guarantees checked.
- **Fix:** a concise repair that preserves the intended contract.

Finish with coverage: behaviors traced, related callers/tests inspected, checks run, and unresolved limitations. If nothing survives verification, say `No actionable findings.` and give the coverage statement.

## Examples

**Ordinary logic:** `review-correctness --staged` finds a loop indexing one past the last element on a one-item input. Report the input and failing access, with the bound correction.

**Future extension:** a payment-kind branch handles PayPal in an unnamed final `else`. Name the future kind that would be refunded through PayPal; recommend explicit known cases and the language's exhaustiveness mechanism. An intentional generic display fallback is fine.

**New value, old consumer:** the diff adds `PAUSED`; a repository search finds `if status != CANCELLED: charge()`. Report the newly reachable charge of a paused subscription even though the consumer is outside the diff.

**Ambiguous retry:** a payment succeeds remotely but its response times out; the retry creates another payment. Trace the missing idempotency protection and duplicate charge. Separately, a cache that grows with each successful request belongs to performance.

**No defect:** all inputs are parsed at the boundary, branches are exhaustive, and operations inherit an enforced deadline. Do not request extra private-function validation, wildcard branches, or redundant timeout arguments.

## Troubleshooting

### Every else or default looks suspicious

Limit the exhaustiveness check to named cases where the fallback means one particular case. Test whether the same behavior would be correct for a future value, and respect intentionally open domains.

### A timeout, assertion, or cleanup is not visible locally

Trace callers, scope owners, runtime configuration, and library guarantees. Absence in this function is not evidence that protection is missing. Report uncertainty if the guarantee cannot be established.

### A finding fits several reviewers

Describe one root cause and its concrete consequence. Keep behavioral analysis here; leave a representation-only, capacity-only, or structural recommendation to its owner. The parent combines duplicate reports rather than counting them as independent defects.
