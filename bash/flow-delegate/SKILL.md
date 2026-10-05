---
name: flow-delegate
description: Delegate a bounded repository task to an allowlisted external coding CLI through the guarded Flow runner. Use for automatic provider selection or explicit Codex, OpenCode, Kimi, Gemini, or Kiro delegation that requires timeout handling and independent local review.
---

# Delegate Through Flow

Read [delegation](../../references/delegation.md), [safety](../../references/safety.md), and [collaboration](../../references/collaboration.md) before acting.

## Select

Accept `auto` or one explicit provider: `codex`, `opencode`, `kimi`, `gemini`, or `kiro`. For `auto`, select from the provider matrix in [delegation](../../references/delegation.md), announce the provider, mode, and reason, and use `read` only for analysis-only work.

Standalone delegation inherits no fleet authorization, so never add either fleet bypass vector: `--dangerously-bypass-approvals-and-sandbox` (Codex) or `--dangerously-skip-permissions` (Claude). An acknowledgement given for a fleet launch never covers a delegated run.

## Run

1. Inspect repository status, resolve `../../scripts/run-agent.sh` from this installed skill, check the selected binary, and determine its configured `timeout_s` without reading secret files.
2. Run the packaged preview and display both its exact expanded provider vector and confirmation token:

   ```text
   bash <packaged-run-agent.sh> --preview <provider> <read|write> <task>
   ```

3. Require explicit confirmation of that exact expanded vector. Treat the displayed token as bound to its provider, repository, mode, typed model, arguments, standardized prompt, and task; do not reuse it after any change.
4. Execute the identical packaged runner invocation without `--preview`, setting `FLOW_DELEGATION_CONFIRM_TOKEN` to the confirmed token. Execute only the packaged runner. Set the host execution timeout to at least `timeout_s + 60` seconds so the runner can report its own timeout first.
5. Report the runner exit code and captured output path. Do not treat a delegated summary as proof of completion.

## Review Independently

After every run, including failures, inspect Git status and the full unstaged and staged diff, inspect relevant untracked files, reconcile scope against the task, and run the relevant tests in the primary session. Return an independent `APPROVED`, `CAVEATS`, or `REJECTED` verdict with evidence and concerns.
