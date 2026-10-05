---
name: agent-reviewer
description: Review agent-generated changes against project rules. Use when asked for a review, before opening a PR, after large Codex edits, or when checking diffs for correctness, security, architecture, tests, docs drift, dependencies, migrations, and release risk.
---

# Agent Reviewer

## Purpose

Perform a findings-first review of agent-generated changes and prioritize risks over style commentary.

## Inspect First

- git diff, changed files, tests, docs, manifests, migrations, schemas, CI config, and relevant project rules
- `AGENTS.md`, architecture boundaries, test strategy, security baseline, dependency policy, and release checklist

## Procedure

1. Build a diff inventory.
   - Use `scripts/review_diff_inventory.py` when helpful.
   - Identify changed behavior, public contracts, dependencies, migrations, env vars, and docs.

2. Review by priority.
   - P0: correctness, security, data loss, broken release.
   - P1: architecture violations, missing tests, incompatible migrations.
   - P2: maintainability, docs drift, dependency risk.
   - P3: style or low-risk polish.
   - For UI diffs, check that icon-only controls expose accessible names and that browser tests can target important actions by role/name.
   - For OpenSpec-backed work, check implementation against proposal, delta specs, design, and tasks.
   - For shadcn/ui diffs, check component ownership, `components.json` aliases, accessibility, and local customization preservation.
   - For TDD work, check failing reproduction and green validation evidence.
   - For nested `AGENTS.md`, check local files do not contradict or duplicate root instructions.
   - For control-loop artifacts, check feature-state evidence, session handoff updates, initialization readiness, termination evidence, sprint contract coverage, and promoted review feedback.
   - For risky changes, check that `$pre-edit-investigation-gate` evidence exists before implementation.
   - For browser-facing changes, check click-path and Playwright evidence through `$click-path-and-browser-qa`.
   - For dependency, external API, framework, MCP, or security choices, check `$research-first-change` evidence.
   - For broad or risky reviews, use `$subagent-review-orchestrator` to generate explicit reviewer, security, docs, browser QA, or trajectory auditor subagents.
   - If task-trace artifacts exist, check `$trajectory-risk-supervisor` output for skipped evidence or suspicious transitions.

3. Produce findings first.
   - Include file and line references when available.
   - Avoid nitpicks unless requested.
   - Include open questions only when they affect correctness.

4. Recommend validation.
   - Name exact tests and scripts that should be run.
   - Route recurring findings to `review-feedback-promoter` instead of repeating the same review comment.
   - Use `project-local-skill-generator` to create `project-review-protocol` when review docs and promoted feedback should be triggerable in the repo.

## Validation

- Confirm every finding is grounded in a diff, file, command, or documented rule.
- Confirm severity is justified.
- Confirm review output leads with findings.
- For UI changes, confirm accessibility and browser workflow risks were considered.

## Completion Criteria

- The user has a prioritized review that can be acted on directly.
- No broad unsupported claims or generic style-only review.
