---
name: multi-agent-pr-review
description: "Runs read-only parallel review of a PR, branch, commit, or diff across bugs, security, tests, maintainability, performance, and UI."
---

# Multi-Agent PR Review

Review a Git-backed change set with bounded read-only reviewers.

## Workflow

1. Resolve the exact base and head, or state that the current working tree is
   the target.
2. Read repository instructions and relevant changed files.
3. If subagent tools are available, dispatch independent read-only reviewers:
   security, runtime bugs, tests/flakiness, maintainability/architecture,
   performance, and UI/UX only when frontend files changed.
4. If subagents are unavailable, run the same categories sequentially.
5. Merge results with `subagent-result-merge`.

Default: keep the current selected model; multimodel and quorum are off.
The skill name and parallel reviewers do not activate different models or votes.
Same-model parallel reviewers remain available with the parent's selected model.
Use the task-scoped `/multimodel` and `/quorum` commands separately as specified
in [Explicit Activation](../../docs/cross-provider-review.md#explicit-activation).

## Cross-Provider Review

When `/multimodel` or `/quorum` is active, bind the same source snapshot,
reviewed artifacts and acceptance criteria before dispatch. Use the existing
worker result contract and a verified launcher; native subagent availability
does not establish an external provider route. Host-specific mappings and
credentials remain private. Apply `agent-squad` export and execution limits.

Only `/quorum` enables the fixed roster and voting decision policy in
[Worker Quorum](../../docs/worker-quorum.md): two-reviewer consensus or a
three-reviewer quorum. Reviewers draft independently before seeing peers'
results. Use distinct observed providers, exclude the change author from votes,
and keep unknown routes, abstentions and failed launches out of approvals.
An additional review is useful for material disagreement; small changes do not
need a model panel. Do not repeat all project checks in every reviewer.

Without `/quorum`, merge findings without votes or majority thresholds.
With `/quorum`, evaluate records using `scripts/worker-evidence.py quorum` and verify
the actual source and artifact roots. Confirmed critical counterexamples and
required failed checks block acceptance regardless of the approval count.
The helper validates evidence consistency; it does not authenticate a provider,
execute checks, establish isolation or authorize merging. The parent owns
reproduction of findings, integration validation and applying changes.

## Reviewer Contract

Each reviewer returns:

- finding
- severity
- evidence with file/line
- confidence
- suggested minimal fix
- validation gaps

## Rules

- Do not edit files.
- Do not report style-only issues unless they hide a real risk.
- Mark unverified concerns as uncertainty.
- Use `security-router` for deep security workflow when security findings are
  material.
