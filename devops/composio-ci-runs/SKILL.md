---
name: composio-ci-runs
description: Use when Codex needs to run CI/CD or cross-service automations through the Composio MCP server.
---

# Composio CI Runs

## Purpose
Drive multi-service workflows (deploy previews, QA notifications, release toggles) using the Composio-hosted MCP server defined under `servers/composio`.

## Setup Checklist
1. Export `COMPOSIO_ENDPOINT` + `COMPOSIO_API_KEY` and update `mcp.json` with the websocket transport.
2. Map pipelines (e.g., `deploy-preview`, `promote-prod`) inside the Composio dashboard and document their inputs in `servers/composio/README.md`.
3. Confirm each connector account (GitHub, Slack, Vercel, etc.) has least-privilege scopes before triggering live runs.

## Workflow
1. **Plan** – outline prerequisites (tests pass, approvals granted) and choose the pipeline or action ID to invoke.
2. **Trigger** – call `runPipeline`/`invokeAction` with structured payloads and include an idempotency key when rerunning.
3. **Monitor** – poll `getRun` for status; fetch logs when state is `failed` or `warning` and summarize them.
4. **Close out** – after success, post a short confirmation back to the requester; if failure repeats after one retry, halt and request human review.

## Notes
- Record every automation invocation in the related pull request or issue so humans can audit history.
- Keep secrets out of payloads—Composio resolves connector credentials internally.
- This skill often pairs with `github-operations` (to prep PRs) and `playwright-automation` (for smoke tests); coordinate order explicitly in the plan.
