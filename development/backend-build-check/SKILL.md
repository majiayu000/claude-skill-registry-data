---
name: backend-build-check
description: Ensure backend build readiness for Espresso Engineered. Use when backend code/config changes are made or when a feature/task is wrapping up to suggest running `npm run build:backend` (and tests only if requested).
---

# Backend Build Check

## Overview

Confirm the backend still builds cleanly after backend updates. Prompt to run the build when work is wrapping up.

## Workflow

1. Detect trigger: backend files changed or user indicates a task/feature is finishing.
2. Suggest running `npm run build:backend` from repo root.
3. If the user agrees, run the command and report pass/fail.
4. If it fails, summarize the top errors and ask how they want to proceed.

## Notes

Only run tests when explicitly asked. Respect sandbox/network constraints; if build requires escalation, request approval.
