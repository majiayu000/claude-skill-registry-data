---
name: mutation-testing
description: Configure a bounded mutation-testing campaign or analyze surviving mutants when explicitly requested. Use to assess whether tests detect changed behavior, classify equivalent mutants, or improve assertions from mutation results. Not triggered by ordinary testing, coverage, or refactoring requests; analysis-only requests do not authorize running a campaign.
disable-model-invocation: true
license: CC-BY-SA-4.0
---

# Mutation Testing

Change behavior deliberately to learn what the tests actually detect. A campaign tests the suite, not the safety of the original program. Adapted from Trail of Bits; see [source and changes](UPSTREAM.md).

## Establish scope

Distinguish setup, execution, result analysis, and test improvement. Start a campaign only when the user explicitly requested mutation execution; otherwise stay with the requested analysis or configuration.

Inspect the code, existing mutation configuration, test commands, and installed tool version. Reuse the project’s tool; otherwise choose a suitable option under its dependency policy. Examples include mutmut, Stryker, cargo-mutants, PIT, and mewt/muton. Confirm support and flags through installed help or current primary documentation rather than assuming a shared CLI.

Choose a small, high-value source target. Exclude tests, dependencies, generated code, and unrelated changes. Measure a passing unmutated baseline against the exact source snapshot and selected tests before interpreting mutant outcomes. A failing or unstable baseline blocks trustworthy scoring, not useful diagnosis.

## Run safely and within budget

Use a disposable snapshot or tool-provided isolation whose behavior you have verified. Include relevant uncommitted and untracked source inputs; a worktree at HEAD alone does not capture the current dirty tree. Never mutate a shared checkout, stash others’ work, or reset it to clean up.

Isolate test data, caches, databases, ports, and external effects where needed. Set runtime and concurrency bounds before execution. Estimate cost from baseline and mutant counts, including compilation overhead; label estimates as estimates. Start with a pilot and expand within the authorized budget, not an automatic whole-repository campaign.

Keep configuration, selected targets, exclusions, tool versions, commands, source identity, and results. Stop task-owned processes at the budget boundary, preserve partial evidence, and report incomplete scope. Do not purge saved campaigns or introduce a CI threshold without authorization.

## Interpret before improving

Inspect surviving mutations with their original code and relevant tests. Classify each examined result as killed, survived, demonstrably equivalent, uncovered, invalid/build error, timeout, or unresolved according to the actual tool’s semantics. Do not count every nonzero exit as a kill or silently fold inconclusive outcomes into a score.

Use [result interpretation](references/results.md) to distinguish real gaps from equivalence and infrastructure problems. A survivor is not automatically an original-program bug. Prioritize by the behavior’s importance, not only operator severity or aggregate score.

When authorized to improve tests, add the smallest meaningful assertion or input that distinguishes the mutant. Verify the test passes against the original and fails against that specific mutation. Restore the isolated original, rerun relevant checks, and verify the shared source was not modified by the campaign.

Report scope, exact counts and denominator definitions, exclusions, representative evidence, unresolved cases, and completed checks. A high kill rate does not prove suite adequacy; a partial campaign does not cover the whole repository.
