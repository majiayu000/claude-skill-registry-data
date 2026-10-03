---
name: review-pr
description: Reviews a pull request with independent parallel reviewers, verifies every finding, fixes the valid in-scope ones, and has an independent reviewer re-check the result. Use when invoked explicitly on a PR.
---

## Running in Codex

This is the Codex copy of this skill. Read the rest of it with these translations:

- Agents launched in parallel: spawn each one with `spawn_agent` before waiting on any, then collect the
  results with `wait_agent`. Tell every agent you spawn not to spawn agents of its own. If subagents are
  unavailable, run each lane yourself, one after another.
- "Your default model" and "your strongest model": spawn the agent with an `agent_type` whose role file in
  `~/.codex/agents/` sets `model` and `model_reasoning_effort`. An agent without a role runs on the
  session's model.
- A slash command such as `/name`: mention the skill as `$name`.
- This repository's hooks and `.claude/` paths are for Claude Code only, and nothing here installs a Codex
  hook. A loop runs one pass per invocation, saves its state and reports how to resume.
- `CLAUDE.md`: also read `AGENTS.md`, which is the file Codex loads.

# review-pr

Autonomously review this PR, verify every finding, fix valid in-scope issues, and independently re-review the result.

The task is the text given with this invocation.

---

## Establish the review target

Resolve the PR, base, head, merge base, description, applicable instructions, full diff, changed files, and relevant tests. Review the exact current head SHA. Record staged, unstaged, and untracked user work; never overwrite, stash, reset, stage, commit, or push unrelated changes.

Invoking this skill authorizes local review-and-fix work without asking after each finding. It does not authorize merge, release, deployment, destructive actions, or behavior/product decisions outside the PR's intent.

## Adaptive independent review

Scale to the diff:

- trivial: direct review or 1 specialist;
- modest: 2-3 reviewers;
- normal: 4-7 reviewers;
- broad, cross-system, or high-risk: 8-12+ reviewers.

Orthogonality and independence matter more than reaching a count. Launch independent reviewers concurrently in one dispatch and never permit nested agents. Give each reviewer the exact head SHA, diff, relevant context, and a non-overlapping lens.

Tiers: reviewers run on your default model; the pass that verifies each finding runs on your strongest model. Pin the model on every agent; an unpinned agent inherits whatever the session runs on.

For a normal PR, cover these seven lenses:

1. correctness and error paths;
2. security, privacy, and trust boundaries;
3. data integrity, migrations, idempotency, and transactional behavior;
4. architecture, API compatibility, and integration;
5. tests, failure reproduction, and regression risk;
6. concurrency, performance, and resource use;
7. maintainability, simplicity, operations, and observability.

Adaptive exceptions are required: omit genuinely irrelevant lenses, combine closely related lenses for small diffs, and add domain, accessibility, infrastructure, dependency, or compatibility specialists when the diff warrants them. A docs-only PR receives documentation accuracy, security/privacy disclosure, and link/example validation; it is not an early exit.

## Finding contract

Every candidate finding must include severity, file and line, violated invariant or requirement, concrete consequence, triggering conditions, evidence, confidence, and a minimal fix. Re-read the code and tests to classify it as `valid`, `invalid`, `obsolete`, or `needs decision`. Deduplicate by root cause. Do not fix bot or reviewer claims blindly.

Use this fix policy:

- critical/high: fix valid findings first;
- medium: fix when within PR intent and supported by evidence;
- low/nit: fix only when high-confidence, behavior-preserving, low-churn, and unlikely to conflict with user work.

Do not expand scope to satisfy style preference. Escalate only a genuine behavior/product/architecture decision that cannot be resolved from repository evidence.

## Autonomous fix loop

1. Publish the verified, severity-ranked report before edits.
2. Apply minimal fixes in severity order. Parallelize only non-overlapping fixes; integrate serially.
3. Run focused tests plus relevant lint, type-check, build, and repository checks.
4. Have an independent reviewer examine the new diff and verification evidence. The authoring lane cannot approve its own work.
5. Repeat for at most 3 total review/fix rounds. Stop earlier when no valid in-scope findings remain. If the same issue survives or evidence is inconclusive, report it without churning.

Never weaken tests, bypass hooks, or claim approval on behalf of a human or bot. A clean result means the independent review found no remaining valid in-scope issues on the final local head; it is not self-approval.

## Output

```text
## PR Review: [title] ([head SHA])
### Verdict: [CLEAN | FIXED | CHANGES REMAIN | NEEDS DECISION]
### Findings
- [severity] [file:line] [consequence, evidence, confidence, disposition]
### Fixes
- [file:line] [minimal change and finding addressed]
### Verification
- [command/check] — [result]
### Remaining risk
- [unresolved issue, decision, or none]
```
