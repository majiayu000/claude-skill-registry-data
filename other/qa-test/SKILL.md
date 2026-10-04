---
name: qa-test
description: "Verify a feature against its acceptance criteria on the actual implementation and record reproducible evidence."
metadata:
  category: Quality
---

# Qa Test

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Resolve the issue or feature, repository, branch/worktree, and exact revision. Inspect the existing working tree before checkout operations; preserve unrelated or uncommitted changes. Test the intended feature revision rather than silently using the default branch.
2. Read acceptance criteria and relevant discussion. Build a test plan covering each criterion with happy-path, edge, and negative scenarios. Include preconditions, inputs, steps, and expected results.
3. Discover build and execution commands from the repository. Match the environment to the product: CLI commands, API requests, browser interactions, desktop workflows, or device tests. Physical hardware is required only when the behavior or project policy requires it. Record simulator or test-environment limitations.
4. Execute the plan against the real feature. Record observed results and mark each scenario pass, fail, blocked, or not run. An unavailable environment is not a pass. Gather screenshots for meaningful UI evidence, or logs, responses, and assertions for non-UI behavior.
5. Keep implementation code unchanged during verification. Record defects with reproducible steps, expected/actual behavior, and severity; hand fixes back to development. Keep test data/setup changes bounded and report them.
6. Save a traceable report with the revision, environment, scenario results, and evidence. Post or upload it only when authorized, using an existing destination appropriate to the project rather than creating a special branch by default.
7. If authorized, update a configured board only after a clean pass of required criteria and an unchanged tested revision. Use its actual QA/acceptance state and verify the update. Otherwise report the next step without mutating the board.

## Deliverable

Return criterion coverage, verdict, tested SHA, environment, evidence, defects, and limitations. QA does not provide human acceptance, merge a PR, or close an issue by itself.
