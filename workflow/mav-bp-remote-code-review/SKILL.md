---
name: mav-bp-remote-code-review
description: Mandatory remote code review on every pull request. Defines the contract for a GitHub Actions workflow that runs the agent-code-reviewer in CI when a PR is opened, synchronized, or reopened. Used as a dependency by do-issue-solo and do-epic to enforce the review gate, and by do-maverick-alignment to audit the workflow's presence.
user-invocable: false
disable-model-invocation: true
---

# Remote Code Review (Optional CI Gate)

Maverick runs PR code review locally by default — `agent-code-reviewer` is dispatched as a subagent during `do-issue-solo` Phase 9 (and equivalent in `do-issue-guided` / `do-epic`) and produces the binary PASS/FAIL verdict that the auto-merge path trusts. The local agent's verdict is the gate.

This skill describes an **optional** GitHub Actions workflow that re-runs the same agent in CI. Adding it to a project gives you an independent CI-side check on every PR, at the cost of paid Anthropic API tokens for each run and a bit of setup. It is not required, and `do-init` does not scaffold it — projects that want it adopt it deliberately.

## When to Add the Remote Gate

The remote workflow is worth the setup and the per-PR API spend when one or more of these apply:

- **Multi-machine / fleet operation.** When `do-epic` dispatches a wave of stories across worktrees in parallel, a single worktree's local review can fail to fire (process crash, network blip, agent skipped). A CI gate guarantees the merge cannot complete without a review having run somewhere, regardless of what happened on any one worker.
- **Untrusted dev environments.** If contributors run their own local sessions in environments you don't control (shared infra, varied tooling, contractors), a CI-side review is the only review you can rely on.
- **Audit / regulatory needs.** Some teams need a verifiable status check on every PR — a record outside any one developer's session that an AI reviewer was invoked and what verdict it returned. The workflow's `Code Review` check on the PR is that record.

For solo / single-machine use, the local agent runs in the same session that opens the PR. Skipping it requires deliberately ignoring its output. A CI re-run mostly duplicates work the local agent already did — and bills against `ANTHROPIC_API_KEY` for the privilege.

## The Contract (When You Adopt It)

A repository that opts in is compliant iff it ships a GitHub Actions workflow that:

1. **Triggers on PR lifecycle events:** at minimum `pull_request: types: [opened, synchronize, reopened]`. Workflows that only run on `push` do not satisfy this contract — re-opened PRs, force-pushes, and base-branch retargets must each re-trigger the review.
2. **Carries the marker comment** `# maverick:code-review` on its own line, anywhere in the file. The marker is the convention that lets `do-maverick-alignment` identify which workflow file plays the code-review role without parsing GitHub Actions semantics.
3. **Invokes the agent-code-reviewer contract** — i.e., produces a structured PASS/FAIL verdict and posts it on the PR. The supported invocation is Anthropic's `anthropics/claude-code-action`; teams using their own Maverick worker pipeline or a custom integration are free to substitute as long as the verdict semantics match.

The shipped reference template `code-review.yml` (alongside this `SKILL.md`) is a drop-in starting point that satisfies the contract.

## Adopting the Reference Workflow

The fastest path is to copy the shipped template into the project:

```bash
cp "${CLAUDE_PLUGIN_ROOT}/skills/mav-bp-remote-code-review/code-review.yml" .github/workflows/
```

Then, in the repo's GitHub settings:

- **Set the `ANTHROPIC_API_KEY` repository (or organization) secret** so the action can authenticate to Anthropic. An org-level secret scoped to selected repositories is the lowest-friction option if Maverick will run across multiple projects.
- **Optionally make the workflow a required status check** on the protected branch so PRs cannot merge until it returns green. Without this branch-protection rule the workflow runs but does not block merge — that may or may not be what you want.

Edit `code-review.yml` to match the project's secret naming and any environment quirks, commit on a feature branch, and open a PR. The workflow itself will run on its own PR — a useful smoke test that the marker is present and the action invocation works.

## Detection Heuristic

When auditing, look for any file under `.github/workflows/` that:

- contains the literal string `# maverick:code-review` on a line of its own (after stripping leading whitespace)
- AND has a `pull_request:` trigger block (presence is sufficient — full validation of the trigger types is out of scope; the marker carries the team's intent)

Either condition alone is not enough. The marker without a `pull_request:` trigger means a misplaced or in-progress workflow; a `pull_request:` trigger without the marker is some other PR workflow (lint, tests, etc.) and is not the code-review gate.

## Audit Behaviour

`do-maverick-alignment` reports the workflow's presence as informational, not a compliance failure:

- **Workflow present and well-formed** → PASS, with a note that a CI gate is in place.
- **Workflow absent** → INFO, noting that the local agent review is the gate by default and pointing to this skill if the project wants the optional CI gate.
- **Workflow present but malformed** (marker without `pull_request:` trigger, or vice versa) → WARN, since the team's intent is unclear.

<!-- maverick-plugin-version: 4.0.2-dev -->
