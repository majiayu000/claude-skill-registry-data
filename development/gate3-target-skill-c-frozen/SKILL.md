---
name: repo-native-refactor
description: Audit and refactor completed or AI-assisted changes so they conform to a repository's existing semantics, architecture, domain language, prose style, and reliability contracts. Use after implementation for cleanup, rehabilitation, review preparation, or removal of AI slop; preserve behavior and avoid unrelated modernization.
metadata:
  version: "1.2.1"
---

# Repo-Native Refactor

Turn implemented code into the smallest defensible change that belongs naturally in its repository.

Prioritize, in order:

1. semantic integrity;
2. destructive false-positive avoidance;
3. correctness and security;
4. repository conformity;
5. maintainability;
6. reviewability;
7. finding coverage.

Repository-native authorship is a consequence of semantic and stylistic conformity, not a detector-evasion target. Do not manufacture variation, rewrite working code to appear human-authored, or optimize for a slop score.

This is a post-implementation audit and refactoring skill. It is not permission to redesign the repository.

## Choose the operating mode

Use **change-set cleanup** for a working tree, branch, commit range, feature, or bounded implementation checkpoint. Work diff-first and inspect surrounding code only to understand ownership, contracts, and relevant precedent.

Use **repository rehabilitation** only when the user requests codebase-wide cleanup or the authorized scope spans multiple domains. Read [repository rehabilitation](references/repository-rehabilitation.md), build a concise repository profile, and work in independently verifiable batches.

## Resolve evidence

When evidence conflicts, prefer:

1. the user's requirement and authorized scope;
2. repository instructions and documented architecture;
3. observable behavior and public or persisted contracts;
4. healthy code in the same owner, domain, and runtime boundary;
5. relevant tests, schemas, callers, dependencies, configuration, and history;
6. dominant local conventions;
7. language and framework idioms;
8. conservative defaults.

Treat conventions as `observed`, `likely`, `conflicting`, or `unknown`. Do not turn weak evidence into a rule, copy a newly introduced pattern merely because it is nearby, or preserve a known defect as precedent.

## Workflow

### 1. Establish scope and baseline

Before mutation, determine what is available and relevant:

- working-tree state and comparison base;
- changed, new, generated, vendored, or history-sensitive files;
- applicable repository instructions;
- intended verification commands and their current status;
- unrelated user changes that must remain untouched.

Separate pre-existing failures, failures in the implementation under review, and regressions introduced by this pass. Never claim a check ran when it did not.

### 2. Establish intent, ownership, and preservation

Identify the intended behavior, owning domain, important callers, and affected boundaries. Sample healthy sibling implementations when needed to learn how the repository handles the same kind of work.

Refactoring is behavior-preserving by default. Protect relevant APIs, formats, state transitions, validation, authorization, error semantics, transactions, retries, timeouts, idempotency, side-effect ordering, caches, resource lifecycles, and consumed output.

Use history when an irregular implementation or comment may encode compatibility or operational intent. If a defect requires observable change, classify and report it as an intentional behavioral correction rather than cleanup.

### 3. Inventory findings before rewriting

Inspect the authorized scope for repository divergence, domain erosion, misplaced ownership, reinvention, unreliable error behavior, type or schema drift, weak tests, operational risk, prose slop, and unrelated change noise.

Read [finding taxonomy](references/finding-taxonomy.md) when findings are numerous or ambiguous.

A suspicious pattern is a finding, not automatically a defect. For a material correction establish:

- the observed problem and concrete consequence;
- the correct owner;
- whether it is new or pre-existing;
- repository evidence;
- the smallest adequate correction;
- preserved behavior and available verification.

### 4. Classify risk and refactor

Use these risk bands:

- **R0 — mechanical:** established formatter or locally provable cleanup;
- **R1 — low structural:** local residue with straightforward verification;
- **R2 — contextual structural:** rename, movement, control-flow change, consolidation, or abstraction change;
- **R3 — semantic:** errors, fallbacks, retries, caching, serialization, transactions, async, or lifecycle;
- **R4 — critical boundary:** auth, permissions, payment, crypto, migrations, destructive persistence, or concurrency-critical behavior.

Read [semantic risk](references/semantic-risk.md) for R2+, uncertain classification, or bulk changes. Read [deterministic tooling](references/deterministic-tooling.md) before destructive dead-code or dependency removal, structural bulk rewrites, surprising analyzer findings, or new suppressions.

Resolve confirmed R0 and safe R1 residue first. Make R2 changes only with repository evidence and a concrete benefit. Never mass-rewrite R3 or R4 behavior. If evidence is insufficient, preserve the uncertain region, report it, and continue with safer work elsewhere.

Do not consolidate code merely because its syntax matches. Share implementations only when they have the same concept, owner, invariants, and reasons to change. Preserve abstractions that carry policy, dependency direction, compatibility, an external boundary, a test seam, or volatility isolation.

### 5. Audit code prose

Treat comments, docstrings, test descriptions, errors, logs, CLI output, and user-facing strings as distinct surfaces. Read [repository prose](references/repository-prose.md) when these surfaces are added, edited, suspicious, or material to the cleanup.

Prefer deletion over paraphrase when prose only narrates syntax or execution order. Preserve and tighten information about non-obvious constraints, invariants, compatibility, external behavior, security, or operational consequences. Treat observable wording as behavior until evidence shows otherwise.

Phrase matching may locate candidates but cannot decide removal. Do not invent rationale, tickets, incidents, owners, or production history.

### 6. Verify and review

Run the smallest repository-native checks that meaningfully constrain the change, expanding with semantic risk. When error, retry, timeout, transaction, async, or observability behavior is material, read [error and reliability boundaries](references/error-reliability.md). When tests change, are weak, or support R3/R4 work, read [testing integrity](references/testing-integrity.md).

Review the final diff as a skeptical maintainer. Every changed line must have a defensible reason. Confirm that:

- intended behavior and preservation contracts remain intact except for explicit corrections;
- terminology, ownership, architecture, prose, and tests fit relevant repository evidence;
- no analyzer result caused unjustified deletion or suppression;
- no tests were weakened and no sensitive artifact bypassed its normal workflow;
- no unrelated formatting, renaming, dependency churn, or modernization obscures the change;
- uncertain high-risk regions were preserved and reported;
- the result is bounded, explainable, and reversible where practical.

Remove changes that cannot survive this review.

## Hard stops

Do not force a material refactor where intent, ownership, public-contract consequences, migration semantics, error ownership, or concurrency behavior cannot be established. Do not choose between materially conflicting repository patterns without relevant evidence.

A local stop does not end the entire audit. Continue with safe work elsewhere.

## Completion report

Report concisely:

### Result

Use one: **Verified**, **Verified with caveats**, **Needs review**, or **Failed verification**.

### Changed

Summarize material corrections rather than every edit.

### Preserved intentionally

Mention suspicious-looking code or prose deliberately retained when it matters to review.

### Verification

State only checks actually run and their outcomes.

### Residual uncertainty

State unresolved findings or high-risk regions left unchanged. Never claim all AI slop has been eradicated.
