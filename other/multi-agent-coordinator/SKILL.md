---
name: multi-agent-coordinator
description: Coordinate multiple AI agents, subagents, or separate Codex threads on complex tasks. Use when a user explicitly asks for multi-agent collaboration, parallel agent work, delegation, independent reviewers, parallel research, parallel codebase exploration, split implementation across disjoint modules, or using multiple conversations to solve one task. Also use when work already has separable research, review, validation, or implementation tracks that can proceed independently. Do not use for tiny, tightly coupled, or direct-answer tasks where coordination overhead would dominate.
---

# Multi Agent Coordinator

## Overview

Use this skill to act as the lead coordinator for tasks that benefit from multiple independent reasoning or execution tracks. Treat extra agents or threads as bounded contributors; keep final accountability, integration, and user communication in the lead agent.

## Coordination Modes

Prefer the lightest mode that materially improves the outcome:

- **Single-agent sequential**: Use when the task is small, highly coupled, or unclear.
- **Subagents**: Use when the environment exposes subagent tools and the user or host policy allows delegation.
- **Separate threads**: Use when the user asks for multiple conversations, isolated workspaces, long-running branches, or independent follow-up tracks.
- **Manual parallel tracks**: Use when no agent or thread tools are available; split the work internally and execute tracks one by one while preserving the same ownership and review rules.

Obey the host environment's tool permissions. Do not create agents, threads, branches, or worktrees unless the active tool instructions allow it.

## Fit Check

Coordinate multiple agents only when at least one condition is true:

- The task has independent research, exploration, review, or validation tracks.
- The implementation can be split by disjoint files, modules, services, or documents.
- The user explicitly asks for parallel agents, multiple reviewers, separate conversations, or agent collaboration.
- A second independent pass is likely to catch real defects, security issues, missing tests, or flawed assumptions.

Avoid multi-agent coordination when:

- The next step is blocked on a single fact the lead agent can quickly determine.
- The task requires tight, iterative edits to the same file or interface.
- The overhead of task packaging, waiting, and integration exceeds the work saved.
- The user asked only for a direct answer, a tiny edit, or a one-command action.

## Workflow

1. **Frame the objective**: Restate the final deliverable, constraints, repository or artifact scope, and success criteria.
2. **Identify the critical path**: Decide what the lead agent must do locally right now.
3. **Split independent tracks**: Assign only tasks that can progress without blocking the lead's immediate next step.
4. **Choose ownership**: Give each agent or thread one clear responsibility and, for code changes, a disjoint write scope.
5. **Delegate with a task packet**: Include objective, context, allowed files, forbidden actions, expected output, and validation requirements.
6. **Continue local work**: Do non-overlapping work while delegated tasks run.
7. **Collect results**: Wait only when the next critical-path action needs a result.
8. **Review before integration**: Treat agent outputs as proposals. Inspect diffs, claims, commands, and test results.
9. **Merge deliberately**: Resolve conflicts in favor of the user request, repository conventions, and verified behavior.
10. **Validate end to end**: Run the smallest sufficient tests or checks after integration.
11. **Close the loop**: Report what each track contributed, what was integrated, what was rejected, and any residual risk.

## Delegation Rules

Use concise, concrete task packets. Never ask a worker to "figure everything out" when it can be given a narrow scope.

Every delegated task should specify:

- **Goal**: The exact question to answer or change to make.
- **Scope**: Files, modules, URLs, documents, or APIs in bounds.
- **Non-goals**: Things the delegate must not modify or decide.
- **Context**: Only the facts needed for the task.
- **Preflight**: For editing tasks, inspect and report relevant dirty files or overlapping ownership before making changes.
- **Output format**: Bullets, patch summary, file paths changed, findings with severity, or test logs.
- **Validation**: Commands to run or evidence to collect.
- **Coordination warning**: State that other agents may be working in parallel and user changes must not be reverted.

For detailed patterns, read `references/delegation-patterns.md`.

For reusable prompt packets, read `references/prompt-templates.md`.

## Integration Rules

Keep the lead agent responsible for final correctness.

- Inspect any code or document changes before accepting them.
- Prefer one integrated final answer over forwarding multiple raw agent reports.
- Preserve user changes and unrelated work.
- Do not let one delegate overwrite another delegate's ownership area without explicit review.
- Re-run tests after integration, even if delegates already ran focused checks.
- If delegates disagree, compare evidence first, then decide or ask the user only if the decision is product-level or irreversible.

For conflict handling and acceptance criteria, read `references/merge-and-conflict-policy.md`.

## Output Contract

When multi-agent coordination was used, final responses should include:

- The coordination shape used, such as `2 explorers + 1 local implementation`.
- The material result from each track.
- The integrated outcome.
- Verification performed.
- Any delegated output that was rejected or left unresolved.

Keep the final answer concise. Do not expose unnecessary internal prompting details unless the user asks.
