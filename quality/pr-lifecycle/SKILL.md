---
name: pr-lifecycle
description: "Reference document describing PR lifecycle: pre-flight gates (4 conditions), verification gate (5 conditions), body structure (from templates/pr-body.md), reviewer-suggestion algorithm (CODEOWNERS → file expertise → recent activity → workload balance), and finding-ledger merge prerequisite. Reference only (policy document; consumed by `/flow:pr` and `/flow:merge`)."
allowed-tools: Read
agent: general-purpose
disable-model-invocation: true
---

# PR Lifecycle

Policy reference for PR creation and the pre-merge finding-ledger gate; the runnable bash lives in `commands/pr.md` and `commands/merge.md`.

## Contract

Iron law: **no PR without verification — a PR body that cannot show test, lint, and runtime evidence is not ready.** Consumed by `/flow:pr` (Phase 1 pre-flight; Phase 4 verification gate, body assembly, push, create, reviewer suggestion at step 11) and by `/flow:merge` Phase 1 (finding-ledger check). Returns the policy those commands apply: four pre-flight conditions, five verification-gate conditions, the PR body section order, the reviewer cascade, and the two ledger rules that block a merge. Permitted skips: none — pre-flight conditions 1, 2, and 4 are hard errors; condition 3 is a warning that offers `/flow:commit`.

## Pre-Flight Gate (`/flow:pr` Phase 1)

| # | Condition | On failure |
|---|-----------|------------|
| 1 | Not on the default branch | Hard error — PRs come from feature branches |
| 2 | At least one commit ahead of the default branch | Hard error — empty PRs are noise |
| 3 | No uncommitted changes | Warning — offer `/flow:commit` first |
| 4 | No existing open PR for this branch | Hard error — update the existing PR |

## Verification Gate (`/flow:pr` Phase 4)

All five must hold before creation; otherwise stop:

1. All quality commands (lint, test, typecheck) pass — output captured for the PR body.
2. Self-review completed against the `code-quality-principles` checklist.
3. Change classification shows no out-of-context files.
4. Every acceptance criterion has a "Met" or "Interpreted" status with concrete evidence.
5. No P1 findings remain from code review.

"Get the PR up and fix it after", "the reviewer will catch it", "small change", and "CI will validate it" are not exemptions. The eight quality gates flow enforces are mapped in [`gate-configuration.md`](../../references/gate-configuration.md#quality-gates).

## PR Body

Generated from [`templates/pr-body.md`](../../templates/pr-body.md) plus review findings and the decision journal. Section order: Summary (2–3 sentences), Closes, Changes (grouped by area), Comprehension Report, Key Decisions (public journal entries; internal entries redacted), Requirements Adherence (criterion → status → `file:line` evidence), Review Findings (P1/P2/P3), Known cosmetic notes, Review Cycle History, Verification checklist, Verification Verdict, Files Changed. Reviewers skim Summary, Requirements Adherence, Verification in under thirty seconds.

## Reviewer Suggestion (`/flow:pr` Phase 4 step 11)

Priority cascade: (1) CODEOWNERS entries for paths in the diff; (2) file expertise — contributors to the same files in the last 30 days; (3) recent activity in adjacent areas; (4) workload balance — among equals, fewest outstanding review requests. Surface the top 2–3 with a one-line rationale each; the author decides.

## Push and Create

`git push -u origin <branch>` and `gh pr create` are Tier 2 (journal-and-proceed). Afterwards verify with `gh pr view --json number,url,state,title`, surface the URL, and suggest `/flow:review {number}`.

## Merge Prerequisite: Finding-Ledger Check (`/flow:merge` Phase 1)

PR comments carry `FLOW_REVIEW_CYCLE:{N} FINDINGS:[...]` and `FLOW_RESOLUTION_CYCLE:{N} RESOLVED:[...] ESCALATED:[...] DISPUTED:[...]` markers; the latest of each is parsed and compared (grammar and trust filter in [`finding-ledger-parser.md`](../../references/finding-ledger-parser.md)). The merge blocks when:

1. The `ESCALATED` array is non-empty — an escalated finding is unresolved.
2. Any ID in `FINDINGS` has no entry in `RESOLVED`.

To clear: run `/flow:address {pr_number}` until every finding appears in `RESOLVED` and `ESCALATED` is empty, then re-run `/flow:merge`. This is the "no incomplete shipments" boundary.

## Keeping Policy and Bash Aligned

Pre-flight: `commands/pr.md` Phase 1. Body assembly, push, create: Phase 4. Reviewer suggestion: Phase 4 step 11. Ledger gate: `commands/merge.md` Phase 1. A new check, section, or marker changes the command and this reference together.
