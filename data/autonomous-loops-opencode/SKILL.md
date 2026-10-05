---
name: autonomous-loops-opencode
description: Design bounded OpenCode CLI loops and multi-stage pipelines with explicit artifacts, stop conditions, time/cost budgets, permissions, validation gates, and recovery. Use for repeat-until-pass, batch pipeline, CI audit, or Turkish intents such as “OpenCode döngüsü”, “otonom ama sınırlı çalış”, “başarana kadar dene”, “çok aşamalı pipeline”. Do not use for unbounded autonomy, ambiguous goals, credentials, payments, publishing, or irreversible external actions.
---

# Safe OpenCode Autonomous Loops

Use OpenCode's installed CLI and current provider configuration. Do not hard-code a provider or model, and do not change either automatically.

## Choose the smallest pattern

- **Sequential pipeline:** independent `opencode run` calls exchange files or commits.
- **Bounded iteration:** one task repeats until a measurable test passes or a fixed iteration/time budget expires.
- **Parallel DAG:** only independent nodes run together; every node owns disjoint files or is read-only.
- **CI gate:** a noninteractive audit or validation job produces a report and exit status; deployment remains separate.

Avoid autonomous execution for ambiguous goals, irreversible operations, secrets, production writes, payments, publishing, or work that requires human judgment at every step.

## Required loop contract

Before execution define:

```yaml
goal: measurable outcome
workspace: exact repository or directory
inputs: source files and immutable constraints
allowed_changes: bounded paths and actions
forbidden_actions: push, publish, deploy, delete, spend, external message, provider/model change
artifact: file, patch, test result, or report passed to the next stage
validation: deterministic command or rubric
stop_when: success condition
budget: maximum iterations, elapsed time, and optional cost ceiling
on_failure: preserve evidence, stop, and report
```

## Execution rules

1. Verify the installed OpenCode CLI syntax with `opencode --help` and the current official documentation; flags can change.
   If the executable is unavailable in the active environment, stop and report that fact instead of inventing commands.
2. Use the project's current working tree and instructions. Never discard unrelated changes.
3. Keep every prompt self-contained and pass state through explicit artifacts, not assumed conversation memory.
4. Use noninteractive execution only when supported by the installed CLI. Quote paths and secrets safely; pass credentials through approved environment/config mechanisms, never prompt text.
5. Set a finite retry/iteration/time budget. "Until perfect" and infinite loops are invalid stop conditions.
6. Require a fresh validation step before accepting a generated change. A loop must not edit its own acceptance test merely to pass.
7. Serialize steps that share files, package manifests, databases, git state, or external services.
8. Stop on permission requests, repeated identical failure, unexpected scope expansion, missing evidence, or budget exhaustion.
9. Do not commit, push, open a PR, deploy, publish, or message anyone unless the user separately authorized that external action.

## Recovery

Capture the command, iteration, inputs, changed files, validation output, and last known-good state. Resume only from verified artifacts; do not replay successful external actions. Prefer a reversible patch or isolated worktree for high-risk loops.

## Completion report

Return the loop contract, commands run, iterations used, artifacts, validation evidence, stopped/skipped actions, and rollback path. A loop is successful only when its predefined acceptance criterion passes within budget.
