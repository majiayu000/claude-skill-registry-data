---
name: evaluation-preflight
description: Validate an Arena evaluation protocol before any costly or result-producing run.
argument-hint: "[issue-number-or-protocol]"
disable-model-invocation: true
---

Perform a read-only preflight for Arena evaluation $0. Do not start the evaluation.

Read `AGENTS.md` and the governing Issue/protocol, then verify only requirements that are actually specified, including as applicable:
- execution target and required merged revision
- clean-worktree requirement
- candidate and baseline identity
- seed set, game count, duplicate layout, and worker constraints
- artifact/output location and overwrite policy
- pre-execution lock or receipt requirements
- one-shot, rerun, or result-publication restrictions
- dependency/pin identity
- estimated runtime/cost when the protocol makes it decision-relevant

Treat application/protocol-level validation as authoritative. Claude Hooks are only operator-error guards and must not be treated as the research-integrity boundary.

Report `PASS`, `BLOCKED`, or `NOT APPLICABLE` for each relevant item and list any command the user should run next. Do not execute the result-producing command.
