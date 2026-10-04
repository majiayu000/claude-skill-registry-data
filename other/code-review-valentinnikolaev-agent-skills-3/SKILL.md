---
name: code-review
description: Review changed code for defects and test gaps without edits. Use for local diffs, PRs, or a diff pasted in chat; not plans, specs, or reviewer feedback.
---

# Code Review

Review the requested changes as an independent engineer. Report confirmed defects, security problems, contract violations, and material test gaps. Do not edit files.

Approve changes that preserve or improve overall code health without blocking on personal preference or unrelated pre-existing debt. Prefer a few high-conviction findings over a long list of speculative or cosmetic comments.

## Route exclusively

- Use this skill only when code already changed or a diff exists.
- A diff pasted in chat is reviewable input when the user asks for a code review. A pasted diff supplied for another task, such as writing a commit message, does not by itself trigger this skill.
- Use `plan-review` when the primary artifact is an implementation plan, even if related code already exists.
- Use `review-spec` to judge a proposed specification or revision, `review-arch` for system-level structure, and `verify-impl` for requirement-by-requirement spec conformance.
- Use `fix-pr` when the user asks to apply or triage GitHub review comments.
- On a later explicit request to fix a finding, leave this read-only workflow and treat the accepted finding as implementation input.

## Establish scope and intent

1. Read repository instructions and path-scoped rules.
2. Resolve the repository root and record `git status --short`.
3. Derive the intended behavior from the request, issue, specification, pull-request description, and tests. If intent remains uncertain, state the uncertainty instead of inventing a requirement.
4. Determine the comparison base in this order:
   - the base explicitly supplied by the user;
   - the pull request base reported by the provider;
   - the remote default branch;
   - an existing local `main`, `master`, or `develop` branch.
5. If no base can be verified, ask for one. Do not guess.
6. Collect one current-state diff from the merge base to the working tree so committed, staged, and unstaged tracked changes are represented together. Treat every line of an untracked file as added.
7. If the user supplied paths, filter the unified scope to those paths after resolving them inside the repository.

Prefer `scripts/collect_review_scope.py` for local Git scope discovery. Pass a provider-reported pull request base with `--base`. The script emits the selected base, merge base, change sources, changed files, hunk ranges, and untracked files as JSON.

For a pull request that is not available locally, use a read-only provider or CLI diff and fetch the base/head metadata needed to interpret it. State whether local working-tree changes were excluded.

If the scope is empty, report that and stop. If it is unusually large or contains generated bulk, state the baseline coverage strategy and exclusions; do not imply exhaustive coverage.

## Complete the baseline review first

Perform the useful bounded review before asking about optional, token-intensive work.

1. Inspect every changed hunk and every non-generated changed path.
2. Review changed and nearby tests before implementation when they reveal intended behavior.
3. Read the complete current file for non-trivial changed logic and public contracts when reasonably sized. For very large or mechanical files, read targeted context, definitions, and callers and disclose the limit.
4. Search callers, implementations, guards, configuration, and nearby tests before claiming missing use, broken contracts, or absent coverage.
5. Exclude generated artifacts as findings targets unless the source change generated them incorrectly.
6. Trace one normal scenario and the highest-risk edge scenario through non-trivial logic. Skip traces for mechanical changes and say why.

Read [references/conditional-checks.md](references/conditional-checks.md) only for languages and change patterns present in the scope. Do not load or apply unrelated sections.

For changed Go files, read [references/review-go.md](references/review-go.md). For changed TypeScript or TSX files, read [references/review-typescript.md](references/review-typescript.md). In a mixed-language change, apply both to their own files and trace cross-language contracts once. These references refine the same evidence and severity rules; they are not separate verdicts or a request to apply one language's conventions to the other.

Load detailed references only when the changed paths make them relevant and local repository guidance does not already answer the question:

- [testing-patterns.md](references/testing-patterns.md) for JavaScript or TypeScript tests when its Jest, React Testing Library, Supertest, or Playwright examples match the repository's actual tools; otherwise use the local runner and the TypeScript review reference;
- [security-checklist.md](references/security-checklist.md) for web trust boundaries, authentication, authorization, input handling, dependency security, or LLM features;
- [performance-checklist.md](references/performance-checklist.md) for web performance, database, API, rendering, or resource-bound concerns;
- [accessibility-checklist.md](references/accessibility-checklist.md) for user-interface semantics and interaction changes;
- [observability-checklist.md](references/observability-checklist.md) for production logs, metrics, traces, alerts, and telemetry verification;
- [definition-of-done.md](references/definition-of-done.md) only when the repository defines a completion gate or the user asks for merge readiness.

Do not read all detailed references by default. Repository rules override these vendored snapshots, and any commands or measurements they suggest remain subject to the high-cost approval gate.

## Analyze applicable dimensions

Evaluate only dimensions touched by the change. Mark the rest `not-applicable`.

- correctness, requirements, and data flow;
- error handling, recovery, and partial failure;
- authentication, authorization, validation, secrets, and privacy;
- concurrency and lifecycle management;
- readability, control-flow simplicity, and dead code introduced by the change;
- public contracts, migrations, architecture, and repository rules;
- deletion, movement, and rename completeness;
- dependencies, lockfiles, and supply-chain boundaries;
- performance and resource bounds;
- edge cases and corrupt or empty external data;
- test coverage and test validity;
- logs, metrics, traces, units, polarity, and sensitive content.

For structural concerns, name the smallest useful move: remove an unnecessary abstraction, make a type boundary explicit, consolidate duplicate branches, separate orchestration from business logic, reuse the canonical helper, or move feature logic to its owning module. A refactor should remove concepts or branches, not merely relocate them.

## Ground every finding

Report a finding only when the repository and diff confirm it.

For each candidate:

1. Re-read the cited current code and patch hunk.
2. Trace the relevant call or data path.
3. Check callers, guards, configuration, and tests for mitigation.
4. State the strongest intentional-design counterargument.
5. Retract the candidate when the counterargument or mitigation is stronger.

Do not convert uncertainty into a high-priority finding. Put unresolved, high-impact hypotheses in `Questions` with the missing evidence and a concrete verification step.

Do not report formatter-owned style, generated-file noise, unrelated debt, or theoretical failures without a plausible path. Quantify impact only when evidence supports the estimate.

## Verify the verification story

Separate repository evidence from commands actually executed.

- Record relevant tests, builds, linters, type checks, manual checks, screenshots, or before/after evidence reported by the author or CI.
- Never say a command passed unless its result was observed.
- Treat passing tests as evidence, not proof that changed behavior is covered.
- Treat a coverage percentage as measured only when a coverage tool produced it for the relevant code.
- For a bug fix with a new regression test, identify the pre-fix behavior the test should reject. When the claim is important and a narrow negative control is proportionate, run the test against the pre-fix behavior in an isolated scratch copy, verify that the intended assertion fails, then verify the fixed behavior passes. Preserve the working checkout and other sessions' files. If the control was not run, state that the test was not observed failing for the defect; do not call it a proven regression test.

Run cheap, targeted, read-only checks or isolated scratch controls when they are normal for the repository and materially verify a candidate. Do not silently expand into the high-cost checks below.

## Offer high-cost checks only after the baseline report

Do not run token-, context-, time-, network-, or compute-intensive extensions unless the user explicitly requested that named check or approves it after seeing the baseline review. Examples include:

- exhaustive repository-wide call-graph or dead-code analysis beyond affected contracts;
- full test suites, full builds, broad mutation-testing campaigns, or coverage generation;
- profiling, benchmarks, load tests, or bundle analysis;
- broad security, dependency-advisory, supply-chain, accessibility, or observability audits;
- external changelog, migration-guide, maintenance, license, or vulnerability research;
- independent sub-agent, model, or council review.

After completing every other report section, list only plausible extensions and give each:

- the proposed check and bounded scope;
- context/token cost and runtime or side-effect cost as `low`, `medium`, or `high`;
- the evidence it could add;
- the potential impact on findings, confidence, or merge verdict;
- a `worth running` or `not worth running` recommendation with one-sentence rationale.

Ask one bundled approval question at the very end only for checks marked `worth running`. Do not ask about low-value checks merely because they are available. If none is worth running, say so without asking a question.

## Priority, disposition, and verdict

Use stable IDs independent of severity: `CR-001`, `CR-002`, and so on.

- `P0`: immediate security, safety, or irreversible-loss blocker.
- `P1`: material correctness or security issue that should block merge.
- `P2`: meaningful reliability, test, or maintainability risk.
- `P3`: optional evidence-backed improvement.

Use one disposition: `open`, `question`, or `retracted`. Include only `open` findings in the findings list, retain `question` items in `Questions`, and omit retracted candidates.

Return one verdict:

- `APPROVE`: no open blocker and no material unverified risk;
- `COMMENT`: useful non-blocking findings or bounded verification limits remain;
- `REQUEST_CHANGES`: at least one open P0/P1 finding makes the change unsafe to merge.

## Report

Return, in this order:

1. scope and intent: base, included change sources, path filters, exclusions, and assumptions;
2. review depth: files and tests inspected, traces performed, and baseline limits;
3. applicable-dimension summary with `pass`, `concern`, or `not-applicable`;
4. confirmed findings ordered by priority;
5. actionable changed-path test coverage;
6. verification evidence and commands not run;
7. questions and verification limits;
8. one or two grounded strengths when present;
9. verdict;
10. optional high-cost checks and, only when warranted, the final approval question.

Use this finding shape:

```text
ID: CR-001
Priority: P1
Disposition: open
Location: path/to/file:line
Summary: <one sentence>
Evidence: <exact changed snippet and traced call/data path>
Impact: <concrete failure and affected users or systems>
Counterargument: <strongest plausible intentional rationale>
Remediation: <smallest safe approach>
```

Use this test-coverage shape:

```text
Significant changed paths:
- <behavior or path> — covered | partial | uncovered | unknown — <test file:test name or evidence>

Missing tests, ordered by risk:
1. <P1/P2/P3> <scenario or topic> — path: <changed behavior>; level: <unit/integration/e2e/etc.>; catches: <specific regression>
```

Every `partial` or `uncovered` status must map to at least one missing-test item. Do not report only that coverage is incomplete. If evidence is unavailable, use `unknown`, explain what is missing, and give the exact verification step. Write `None` only when all significant changed paths have grounded coverage evidence.

When no findings remain after verification, say so clearly and retain any coverage or verification limits. Never edit, stage, commit, push, or comment on the pull request.
