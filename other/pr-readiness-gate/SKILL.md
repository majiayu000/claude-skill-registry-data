---
name: pr-readiness-gate
description: Record mode-aware PR readiness, requiring human confirmation for normal task and Gauntlet promotion PRs while preserving the scoped Goal and approved Gauntlet-progress publication paths.
engines: [AGNOSTIC]
---

## When to use
Use when implementation and local verification are complete and the next likely action is pushing a branch or opening/updating a pull request. Select the explicit Goal or Gauntlet-progress interface only when that mode's durable authorization already applies.

## Output
- readiness report path
- validation summary and current branch state
- explicit user prompt for normal task and Gauntlet promotion publication, or a durable automatic-publication record for an authorized Goal task or Gauntlet work unit

## Notes
- Normal task PRs and Gauntlet promotion PRs are hard human gates: do not push, create or update a PR, or open a draft PR until the user explicitly confirms readiness after implementation. No Gauntlet PR may ever enable auto-merge, auto-rebase, auto-squash, or merge-queue entry; later human confirmation does not authorize it, and retained automation history invalidates the evidence.
- A general implementation request is not publication approval. Ask again at completion unless an explicit Goal flow or approved Gauntlet contract supplies the applicable scoped authorization.
- Goal task PRs may publish after `--goal` records successful readiness. Approved Gauntlet work-unit and remediation PRs may publish only from the exact checkpoint emitted by `--gauntlet-progress`; this authorization never includes merging, merge approval, auto-merge, or final promotion.
- Run the applicable readiness interface before any `gh`, `github` CLI/wrapper, GitHub MCP/connector, or publishing skill that could create or update a PR.
- Once the applicable gate authorizes publication and the PR is available, choose GitHub PR tools in this order: local `gh` first, an available `github` CLI executable or repository-provided GitHub CLI wrapper second, and GitHub MCP/app connector tools only when both CLI options are unavailable or unsuitable.
- Start post-PR QA immediately after the PR is confirmed available, regardless of which authorized publication path created it.
- For checkpointed ordinary tasks, run `commands/validate-task-checkpoint.sh <task> --phase complete` and review its scope/limitations before preparing readiness. Changed HEADs, declared files, or pending external writes require reconciliation and affected verification. This check is additional evidence, never a replacement for readiness authorization or Gauntlet's canonical validators.

## Command
../commands/pr-readiness-check.sh [task_or_issue_ref] [validation_summary_file]
../commands/pr-readiness-check.sh --goal [task_or_issue_ref] [validation_summary_file]
../commands/pr-readiness-check.sh --gauntlet-progress <gauntlet_ref> <item_id> [validation_summary_file]
../commands/pr-readiness-check.sh --gauntlet <gauntlet_ref> [validation_summary_file]
