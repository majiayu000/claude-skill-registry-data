---
name: workspace-doctor
description: Diagnose local workspace readiness, generated catalog freshness, and common setup problems, then point to the right repo-native next command. Use when Codex needs to check project health, missing tools, Xcode or XcodeGen blockers, auth gaps, environment mismatches, broken install steps, or other practical issues that stop a user from building or running something.
---

# Workspace Doctor

Use this skill when the fastest path forward is to inspect the machine, the workspace, and the project setup before making deeper changes.

It is especially useful in this repo when the task touches:

- bundled macOS app workspaces under `apps/`
- `project.yml` plus XcodeGen flows
- local runner scripts in `skills/*/scripts/run_*.sh`
- ambiguous "why will this not build or run" reports where the blocker may be machine setup rather than code

## Quick Start

1. Run `bash scripts/workspace_doctor.sh` from the skill folder, or use `codex-goated doctor` from the repo root for the same audit path and catalog freshness check.
2. From the repo root, expect the inventory to prioritize `apps/skillbar` as the local manager hub, to show each tracked app workspace with its paired runner command set, and to print the app-to-skill overlap map plus runner command families.
3. Reproduce the problem with the smallest safe command that reveals the issue.
4. Check the local environment before blaming the code.
5. Explain blockers in plain language and prefer direct fixes over abstract advice.
6. Distinguish between missing tools, auth problems, dependency issues, and actual code errors.

## Workflow

### Diagnose First

- Inspect the current workspace layout, package manager files, and toolchain markers.
- Check versions, missing CLIs, missing secrets, and obvious environment mismatches.
- Check generated catalog freshness and the repo overlap map when the workspace includes this repo's skills and packs; stale metadata or hidden near-equivalents can both break discoverability even if the app still builds.
- Prefer targeted commands that confirm one hypothesis at a time.
- Start with `bash scripts/workspace_doctor.sh` or `codex-goated doctor` when you want a fast machine and repo inventory.
- When the target is a macOS app workspace, let the script tell you whether Xcode, XcodeGen, and the paired repo runner are available before you try a full build.

### Follow Repo-Native Entry Points

- If the workspace lives inside this repo, prefer the local runner script the doctor output names.
- For bundled app workspaces, the doctor output should surface the correct `run_*.sh` helper when one exists.
- If a bundled app has `project.yml` but no paired runner, treat that as a real gap and use the fallback `xcodegen` plus `xcodebuild` commands the doctor script prints.
- For repo-root checks, use the surfaced `bin/codex-goated`, `bin/codex-goated catalog check`, `scripts/audit-catalog.sh`, or overlap-map section instead of ad hoc equivalents.

### Fix Carefully

- Apply the smallest useful fix first.
- If a blocker is machine-specific, say so clearly.
- If the project has an existing script for doctor, build, test, or setup, use that before inventing a new flow.
- Separate "cannot run on this machine yet" from "code is actually broken."

### Required Deliverables

- A ranked diagnosis of the likely blocker.
- The exact command or change needed to unblock the next step.
- A note about whether the issue is machine, environment, dependency, or code related.
- The repo-native next command when the workspace already has a local doctor, build, test, or runner flow.

### Common Checks

- repo root markers such as `.git`, `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `project.yml`
- available CLIs such as `git`, `node`, `npm`, `pnpm`, `python3`, `pip`, `uv`, `cargo`, `go`, `docker`, `xcodebuild`, `xcodegen`, `swiftc`
- auth-sensitive CLIs only when relevant, such as `gh`
- project scripts such as `test`, `build`, `dev`, `doctor`, or custom setup commands
- repo-native app runners such as `skills/*/scripts/run_*.sh` when working inside this repository

### Editing Guidance

- Keep troubleshooting output concrete and ranked by likely cause.
- Avoid flooding the user with every possible issue if one root blocker explains the failure.
- Leave the workspace in a more runnable state than you found it.

## Resources

- `agents/openai.yaml`: UI metadata and default invocation prompt.
- `assets/`: branded icons for repo listings and skill chips.
- `scripts/workspace_doctor.sh`: repo-aware doctor script that checks workspace markers, toolchains, Xcode readiness, and local runner paths.
- `scripts/repo_launch_audit.py`: repo launch audit helper that powers the overlap map and runner-family summary.
- `../../bin/codex-goated`: repo-root command that exposes the same doctor flow as `codex-goated doctor`.
- `references/diagnostic-order.md`: preferred order for narrowing environment and setup issues.
