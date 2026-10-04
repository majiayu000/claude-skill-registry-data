---
name: cursor-orchestrate
description: "Use only when the user explicitly types `/orchestrate <goal>` to coordinate a bounded dependency graph through native Codex Cloud tasks; requires an exact configured environment and authorization for task creation."
---

# Native Codex Cloud orchestration

Use this mirror only when the user explicitly invokes `/orchestrate <goal>`. Preserve the goal, decompose it into a bounded coordinator-owned dependency graph, and use native Codex Cloud tasks only when an exact environment is configured and creation plus prompt-content transmission are authorized.

## Workflow

1. Validate the goal and task graph with `prepare_local_plan`. Keep exactly one planner, no cycles or unknown dependencies, and at most eight children.
2. Select a concrete environment. `codex cloud list --json` may identify it by `environment_id`, `environment_label`, or both; an `All Environments` selector is not an environment ID.
3. After explicit authorization for task creation and the goal/acceptance text sent to Codex Cloud, call `build_codex_cloud_dispatch_batch`. It returns shell-free argv for `codex cloud exec --env ENV_ID --attempts N [--branch BRANCH] QUERY`, with `N` from one through four; the adapter never executes the command. A workflow may still require a fixed branch or commit for reproducible proof.
4. Submit only dependency-ready tasks. Inspect each with `codex cloud status TASK_ID` and `codex cloud diff TASK_ID`. A descendant unlocks only after a structured `PASS` handoff includes cloud task and attempt identity, status and diff inspection, and an artifact URI plus SHA-256 digest.
5. Applying a cloud diff is a separate mutation. Build `codex cloud apply TASK_ID --attempt ATTEMPT` only after separate authorization.
6. The CLI documentation exposes no cancellation command. The native Codex Cloud task UI does expose cancellation; using it is a separate operator action. Stopping dispatch only prevents new tasks and does not cancel an existing task.

## Boundaries

Goal and acceptance text are copied into the cloud prompt. Explicit content authorization is the controlling boundary. Local private-path and high-confidence credential-pattern checks are limited defenses and cannot establish that arbitrary text is safe to transmit. Do not send secrets, private inputs, customer data, proprietary code, personal data, or internal URLs without authorization for that exact destination and purpose.

Codex Cloud coordination preserves planner/worker/verifier intent without reproducing Cursor's private internal agent tree. Keep the pinned upstream `blocked_malicious` findings as provenance. Do not publish or execute the upstream TypeScript/Bun runtime, dependency manifest, measurement shell boundary, Slack adapter, or credential paths. Do not treat the earlier provisional ChatGPT Work client ID as a Codex Cloud task or retry it. If there is no concrete `ENV_ID`, return `ENVIRONMENT_REQUIRED` with the validated plan and do not dispatch.
