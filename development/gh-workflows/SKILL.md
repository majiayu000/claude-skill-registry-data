---
name: gh-workflows
description: Manage GitHub Actions workflows with the gh CLI (list, run, cancel, monitor).
---

## When to Use
Use this skill whenever you need to inspect, trigger, or stop GitHub Actions workflows. It wraps `gh workflow` and `gh run` commands so you can keep CI pipelines healthy without leaving the terminal.

## Prerequisites
1. `gh` CLI authenticated with `gh auth login --scopes repo,workflow`. Confirm via `gh auth status`.
2. `jq` available to pretty-print JSON results.
3. Environment:
   - `GITHUB_REPOSITORY` (owner/name). Ask for it if missing.
   - `GITHUB_TOKEN` (gh uses it automatically once authenticated).
   - `DEFAULT_BRANCH` (fallback for manual dispatches; default to `main`).

## Common Parameters
- `--repo "$GITHUB_REPOSITORY"` is required for every command.
- `--json ... --jq '.'` returns machine-friendly payloads.
- When scripts provide `workflow` names, accept either filename (`deploy.yml`) or workflow ID.

## Procedures

### List Workflows (`/workflows-list`)
1. Run: `gh workflow list --repo "$GITHUB_REPOSITORY" --limit ${LIMIT:-20} --json id,name,path,state`.
2. Use `jq` to format the response.
3. Summarize key fields: name, path, state, and id so downstream commands can use them.

### List Workflow Runs (`/workflows-runs`)
1. Require a workflow identifier.
2. Optional filters:
   - Branch: `--branch ${BRANCH}` (omit if empty).
   - Status: `--status ${STATUS:-all}`.
3. Command:
   ```bash
   gh run list --repo "$GITHUB_REPOSITORY" \
     --workflow "$WORKFLOW" \
     ${BRANCH:+--branch "$BRANCH"} \
     --status ${STATUS:-all} \
     --limit ${LIMIT:-20} \
     --json databaseId,workflowName,displayTitle,headBranch,status,conclusion,createdAt
   ```
4. Pipe to `jq '.'` and surface the most recent run id for convenience.

### View a Workflow Run (`/workflows-view`)
1. Accept a `run_id` (numeric or URL) and optional `--log` flag.
2. Command:
   ```bash
   gh run view "$RUN_ID" --repo "$GITHUB_REPOSITORY" \
     --json databaseId,workflowName,displayTitle,event,headBranch,status,conclusion,logsUrl,htmlUrl
   ```
3. Share the JSON and hyperlink to `logsUrl`/`htmlUrl` for quick navigation.

### Cancel a Run (`/workflows-cancel`)
1. Confirm the run is in `in_progress` or `queued` state (use `gh run view`).
2. Command sequence:
   ```bash
   gh run cancel "$RUN_ID" --repo "$GITHUB_REPOSITORY"
   gh run watch "$RUN_ID" --repo "$GITHUB_REPOSITORY" --exit-status || true
   ```
3. Report the final status (cancelled/completed). If already finished, note that cancellation was skipped.

### Trigger a Workflow (`/workflows-trigger`)
1. Require workflow file/ID plus ref/branch.
2. Compose inputs:
   ```bash
   EXTRA_INPUTS=${INPUTS_JSON:+--inputs "$INPUTS_JSON"}
   gh workflow run "$WORKFLOW" --repo "$GITHUB_REPOSITORY" --ref "${REF:-${BRANCH:-$DEFAULT_BRANCH}}" $EXTRA_INPUTS
   ```
3. Capture the run id from gh output and share it for monitoring.

### Monitor a Run (`/workflows-monitor`)
1. Command: `gh run watch "$RUN_ID" --repo "$GITHUB_REPOSITORY" --exit-status`.
2. Stream output back. At completion, annotate whether the run concluded with success, failure, or cancellation.

## Safety Checks
- Never cancel or rerun workflows outside the configured repo.
- If a command fails due to missing repo/ref, prompt the user for the missing data before retrying.
- Treat manual dispatch inputs carefully—validate JSON before passing `--inputs`.
