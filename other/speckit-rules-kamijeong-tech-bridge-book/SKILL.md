---
name: "speckit-rules"
description: "Codex Spec Kit multi-agent workflow rules and safety invariants."
compatibility: "Requires Spec Kit artifacts under specs/ and Codex assets under .codex/agents and .agents/skills"
---

# Spec Kit Multi-Agent Rules

## Core Order

Default to gated behavior. For a full epic, run:

1. intake
2. slicing
3. scheduling
4. per-slice specify
5. clarify
6. checklist
7. plan
8. tasks
9. analyze
10. implementation only after approval or explicit automation mode
11. review
12. integration
13. token reporting
14. commit only when explicitly allowed
15. draft PR only when explicitly requested

## Execution Modes

- `plan-only`: run through analyze and token reporting; do not implement.
- `gated`: run through analyze and ask before implementation, commit, or PR.
- `auto-implement`: implement only low-risk slices after analyze passes; do not
  commit or open PRs unless explicitly permitted.
- `auto-commit`: validate, token-report, and commit only when explicit
  permission is present.
- `auto-pr`: implement, validate, token-report, commit, push, and create a draft
  PR only when explicitly requested.
- `auto-stack-pr`: implement validated slices as an ordered branch stack,
  validate, token-report, commit each slice separately, push with `gh stack`,
  and create stacked draft PRs only when explicitly requested.

`auto-commit` is an explicit permission flag, not a standalone mode. It may be
enabled for `gated` or `auto-implement` after review and validation pass, and
it authorizes the commit step inside an `auto-pr` or `auto-stack-pr` run.

## Slicing And Scheduling

Treat a request as a slicing candidate when it spans multiple independent
deliverables, shared contracts, or more than one implementation area, unless the
user or workflow explicitly overrides the decision.

The scheduler must choose one of:

- `single-spec`
- `sequential`
- `foundation-first-then-parallel`
- `parallel-safe`
- `stop-and-ask`

Choose `stop-and-ask` when dependency, conflict, or repository-state safety is
unclear.

## Stop Conditions

Stop on:

- CRITICAL analyze issues
- failed tests
- high-risk slices without explicit approval
- unrelated user changes before implementation, commit, or PR
- unclear base branch
- missing or unauthenticated GitHub CLI for PR mode
- missing `gh stack` extension for stacked PR mode
- protected publishing branches: `main`, `master`, `develop`
- explicitly configured blocking token budgets
- missing token-analyzer in automation modes without approval

## Issue Commentary

Always add a short issue comment before each phase and before any terminal
action such as commit, push, or PR creation. The comment should note the scope,
label change, and any gate result.

## Token Observability

Token analysis runs after every completed phase. Missing token data must be
reported. High token usage is not a quality gate unless explicit blocking
thresholds are configured.

## Path And Configuration Rules

Use project-local Codex paths:

- `.codex/agents/`
- `.agents/skills/`
- `AGENTS.md`
- `.specify/token-analysis/`

Preserve existing repository configuration unless a minimal update is necessary
for this workflow. Do not assume Claude Code paths.
