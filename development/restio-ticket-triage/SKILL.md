---
name: restio-ticket-triage
description: "Handle Restio support tickets when the user provides a ticket ID like XX-### (e.g., 'YYYYY-##: TASK - ...'). Use this skill to fetch the ticket via the restio-support MCP, prepare git branches, summarize the ticket, and request confirmation before making any code changes."
---

# Restio Ticket Triage

## Overview
Fetch a Restio support ticket by ID, prepare a clean git branch, and provide a read-only analysis before any edits.

## Workflow

### 1) Parse ticket ID
- Accept inputs like `XX-###: TASK - ...` or `YYYYY-##`.
- Extract the leading ticket ID in the form `^[A-Z]{2,5}-\d+`.
- If no valid ID is found, ask the user to provide it.

### 2) Fetch ticket details (read-only)
- Use MCP `restio-support.get_case` with the extracted ID.
- Summarize the ticket: problem statement, reported behavior, environment, and acceptance criteria.

### 3) Research only
- Use `serena` to locate relevant code and tests.
- Identify likely touch points and risks.
- Do not modify files yet.

### 4) Ask for confirmation
- Present a concise summary of findings and a proposed plan.
- Ask the user to confirm before making any code changes.

### 5) Prepare git branches (after confirmation)
- Ask the user to confirm branch switching before executing git commands.
- If the repo has uncommitted changes, stop and ask the user before switching branches.
- Determine the primary dev branch:
  1. Prefer `develop` if it exists on `origin`.
  2. Else prefer `development` if it exists on `origin`.
  3. Else use the remote default from `origin/HEAD`.
  4. Else fall back to `main`, then `master`.
- Checkout that branch, pull latest (ff-only), then create/switch to a branch named exactly the ticket ID (e.g., `YYYYY-##`) unless already on it.
## Constraints
- Read-only until the user confirms.
- Do not spawn sub-agents unless explicitly authorized.
- Avoid destructive git commands; never reset or overwrite without approval.
