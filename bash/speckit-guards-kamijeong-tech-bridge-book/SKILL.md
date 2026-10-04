---
name: "speckit-guards"
description: "Guard scripts for Codex Spec Kit multi-agent workflow safety and token observability."
compatibility: "Requires bash, git, jq when JSON validation is needed"
---

# Spec Kit Guards

Scripts live in `.agents/skills/speckit-guards/scripts/`.

## Scripts

- `guard-no-app-code-change.sh`: verifies read-only phases did not modify
  application code outside allowed workflow artifact paths.
- `guard-before-implement.sh`: blocks unsafe implementation when analyze, risk,
  tests, unrelated changes, or token-analyzer conditions fail.
- `guard-before-commit.sh`: blocks unsafe commits when validation fails,
  unrelated changes exist, secrets are suspected, or token-analyzer is missing
  for auto-commit without approval.
- `guard-before-pr.sh`: blocks unsafe PR creation on protected branches, missing
  GitHub CLI/authentication, unclear base branch, unrelated changes, or missing
  token-analyzer without approval.
- `guard-token-analyzer-available.sh`: detects token-analyzer by extension
  directory, scripts, or command references and recommends installation when
  missing.
- `validate-agent-definitions.sh`: rejects missing, malformed, incomplete, or
  mismatched `.codex/agents/*.toml` role definitions.
- `record-token-step.sh`: writes per-phase token step JSON.
- `generate-token-report.sh`: writes per-run summary, report, and quality notes.

## Read-Only Boundary

Token analysis and guard checks must not mutate product artifacts. The only
normal writes for token observability are under `.specify/token-analysis/`.

## Usage

Run guards before protected actions and record their output in the validation
evidence log for the active feature.
