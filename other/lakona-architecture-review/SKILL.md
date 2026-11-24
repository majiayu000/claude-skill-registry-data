---
name: lakona-architecture-review
description: Perform an explicitly requested, read-only Lakona architecture and framework-health review; honor any specified reduced scope.
metadata:
  internal: true
---

# Lakona Architecture Review

## Scope And Boundaries

Follow `CONTRIBUTING.md` and `docs/contributing/architecture-review.md`, reusing
unchanged material already read. Default to a full current-repository review;
an explicit path, commit range, or validation scenario overrides that default.
Read [scope.md](references/scope.md) when establishing or expanding the inventory
and selecting authorities. Preserve the explicit reduced scope.

The review is read-only. Preserve pre-existing changes. Write reports to
`.tmp/lakona-architecture-review-<yyyyMMdd-HHmmss>.md` and other scratch artifacts
to a review-specific directory under repository-root `.tmp/`. Only an explicit
request permits a tracked report under `docs/plans/`. Do not implement findings,
change versions, create branches or commits, or open PRs as part of the review.

## Review Passes

Assess all eight passes. For a full review, complete every pass; finding a strong
problem does not end another pass. For reduced scope, mark a pass not applicable
only with evidence that the scope cannot affect it. Read each applicable pass's
reference when beginning that pass, rather than loading all details up front.
Full coverage may not be replaced by sampling. Zero findings is valid.

| Pass | Read when executing |
| --- | --- |
| 1. Macro architecture | [macro-architecture.md](references/macro-architecture.md) |
| 2. Micro code smells | [micro-code-smells.md](references/micro-code-smells.md) |
| 3. Generated-project experience | [generated-projects.md](references/generated-projects.md) |
| 4. Performance and resource efficiency | [performance.md](references/performance.md) |
| 5. Reliability and recovery | [reliability.md](references/reliability.md) |
| 6. Contract evolution and determinism | [contract-evolution.md](references/contract-evolution.md) |
| 7. Operability and diagnosability | [operability.md](references/operability.md) |
| 8. Standards conformance | [standards-pass.md](references/standards-pass.md) |

## Verification Integrity

For every reliability, evolution, operability, or performance finding, state
whether the evidence is static, reproduced, measured, or blocked. Identify the
verification needed to accept or reject it:

- contract or lifecycle test
- fault injection
- deterministic concurrency test
- stress or soak test
- focused benchmark
- repository guard

Do not claim runtime impact, recovery correctness, absence of leaks, or
diagnostic sufficiency from static inspection alone. Conversely, do not discard
a concrete static risk merely because no harness exists; report the missing
verification as part of the finding.

## Coverage Integrity

Maintain a coverage ledger while reviewing. For the standards pass the
top-level areas are the checklist rule families. For each top-level area,
record:

- inventory count
- reviewed count
- excluded count and reasons
- relevant validation performed
- complete, not applicable, partial, or blocked status

Do not describe a report as full while any required pass or maintained area is
partial. If interrupted, save the partial Markdown report at its repository
root `.tmp/` path, label it `Status: Incomplete`, and continue from its ledger.
Never replace missing coverage with sampling or inference.

## Report And Completion

Read [reporting.md](references/reporting.md) when recording the first finding or
preparing the report. It defines finding evidence, IDs, recommendation strengths,
report structure, and discussion boundaries. The standards pass additionally
requires its baseline procedure and the existing standards checklist.

Return the absolute report path and a concise summary. Record final
`git status --porcelain` in the report. A complete report accounts for the whole
selected inventory and every pass; retain an incomplete report and resume from
its ledger when coverage is unfinished. Review findings alone never authorize
implementation.
