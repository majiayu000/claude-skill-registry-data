---
name: speckit-review-pr
description: Perform a comprehensive 4-pass code review of a pull request. Use this
  command whenever the user asks to review a PR, do a code review, check a pull request,
  or says "/speckit-review-pr". Also trigger when the user says things like "review
  my changes", "look at this PR", "give me feedback on this PR", or "what do you think
  of this PR". If a PR number is provided use it; otherwise default to the PR for
  the current branch.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: review:commands/pr.md
---

# PR Review

You are an expert code reviewer. Perform a thorough, multi-pass review and synthesize the results into a final report.

**Claude Code note:** If you're using Claude Code and need the PR number, review scope, or missing repo context, use the `AskUserQuestion` tool before proceeding.

## Step 1: Gather context

```bash
gh pr view $PR_NUMBER --json title,body,headRefName,baseRefName,additions,deletions,changedFiles
git log --oneline -10
git diff $(git merge-base HEAD main) --stat
```

If no PR number was given, detect it from the current branch:
```bash
gh pr view --json number,title,body,headRefName,baseRefName,additions,deletions,changedFiles
```

Also check for project conventions:
- Read `CLAUDE.md` if it exists
- Read `CONTRIBUTING.md` if it exists

## Step 2: Four sequential reviews

Work through each review fully before moving to the next. Use `gh pr diff` or `git diff` to read changed files.

> **Ignore** the `graphify-out/` directory in all review passes — exclude it from diffs, file reads, and issue reporting.

### Review 1 — Architecture & API Design
Focus: API contract changes, backward compatibility, architectural consistency, design decisions.

Examine:
- Public interfaces, exported types, handler/controller signatures
- Whether new patterns are consistent with existing ones
- Whether there's a simpler design that achieves the same goal
- Breaking changes or subtle contract shifts

### Review 2 — Implementation Quality & Data Flow
Focus: Correctness, error handling, data flow, edge cases, language best practices.

Examine:
- Logic correctness and edge case handling
- Parameter propagation end-to-end (trace data from input to output)
- Error handling completeness (are errors surfaced or swallowed?)
- Type safety and null/undefined handling
- Dead code, redundant logic, or missing cleanup

### Review 3 — Testing, Performance & Security
Focus: Test coverage, performance, security vulnerabilities, scalability.

Examine:
- Test files — do they cover the changed behaviour and edge cases?
- Are there untested code paths introduced by this PR?
- Performance implications (N+1 queries, unbounded loops, large allocations)
- Security concerns (injection, auth gaps, sensitive data exposure, input validation)
- Resource cleanup (connections, file handles, goroutines, etc.)

### Review 4 — Simplicity
Focus: over-engineering, reinvented standard-library behavior, speculative abstractions, dead flexibility, unnecessary indirection, and code that can be made smaller without losing clarity.

If the `ponytail:ponytail-review` skill (from the `DietrichGebert/ponytail` marketplace) is available locally — i.e. it appears in the host's available-skills list — invoke it via the Skill tool with `skill: "ponytail:ponytail-review"` against the current PR diff. Treat its findings as first-class review findings and include them under the `Simplicity` section in the final report.

Detection rules:
- Only invoke `ponytail:ponytail-review` if it is explicitly listed as an available/user-invocable skill in this session. Do **not** guess the name or attempt to install it.
- If the skill is not available, perform this pass manually using the same focus areas. Do not warn the user, and do not block the review.
- If the user has installed the marketplace and wants ponytail enabled but it isn't showing up, point them at the marketplace: `DietrichGebert/ponytail`.

## Step 3: Synthesize

Combine findings from all four reviews into a single report using the format below. Be specific — every issue should include a `file:line` reference where possible. Omit sections that have nothing to report.

---

## Output format

```
# PR #[number]: [title]

## Overview
[2–3 sentences: what this PR does and why it matters]

## Strengths
[Bullet list of things done well — be genuine, not perfunctory]

## Issues

### 🔴 Critical — must fix before merge
[Issues that introduce bugs, security vulnerabilities, or break contracts]

### 🟡 High — strongly recommended
[Significant quality or correctness concerns]

### 🔵 Medium — worth addressing
[Code quality, missing tests, performance concerns]

### ⚪ Low — optional polish
[Style, naming, minor improvements]

## Detailed findings

### Architecture & API Design
[Review 1 findings with file:line references]

### Implementation Quality
[Review 2 findings with file:line references]

### Testing & Security
[Review 3 findings with file:line references]

### Simplicity
[Review 4 findings with file:line references]

## Recommendation
**[Approve | Approve with conditions | Request changes]**
[One paragraph explaining the reasoning]
```

## Notes

- Use `TodoWrite` (or the host's task-tracking tool) to track your progress through the four review phases.
- Prioritise impact over completeness — a short list of real issues beats a long list of nitpicks.
- If the PR is large, focus each review pass on the files most relevant to that pass's concern rather than reading every file in every pass.
- Reference `CLAUDE.md` patterns when flagging deviations from project conventions.

## Archiving Convention

When a feature is fully implemented, verified, and the PR has merged, archive the entire planning folder rather than individual files.

Preferred archive location:
- `specs/archive/YYYY-MM-DD-{feature-slug}/`

This convention applies to merged PRs that originated from a `/speckit-specify` feature; ad-hoc PRs without a planning folder need no archive step.