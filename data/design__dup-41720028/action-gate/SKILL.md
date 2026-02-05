---
name: action-gate
description: Decide and take action when blockers appear. Use when tools are missing, installs are required, or the user expects proactive execution to complete the task.
---

# Action Gate

## Overview
Weigh cost, risk, and necessity, then act to unblock work with minimal back-and-forth.

## Workflow
1. Identify the blocker (missing tool, permission, or dependency).
2. Decide if it is required to complete the requested work.
3. If required and low risk, propose the exact install/run command and proceed when allowed.
4. If required but risky, explain the risk and ask for confirmation.
5. If not required, skip and continue with a fallback.

## Decision Rules
- Required to deliver the request -> act by default.
- Optional or high-risk -> ask before acting.
- Prefer minimal installs (single tool) and reversible changes.

## Portability Rules
- Detect OS and package manager before installing (Linux: apt/dnf/yum/pacman, macOS: brew, Windows: choco/scoop).
- If no install permissions or network access, ask for manual install or alternate environment.
- Prefer local, user-scoped installs when possible (e.g., `pip install --user`, `npm install -g` only if permitted).
- For Node CLIs, prefer `npx <tool>` when global install is blocked; document any global install used.

## Output Rules
- State why the action is required or optional.
- Provide the exact command(s) to run.
- Note any side effects or rollback steps.

## Acceptance Criteria
- Decision is explicit (act / ask / skip) with rationale.
- Actions are minimal and unblock the task.
