---
name: debug-team
description: Full-repo debugging team workflow. Use for 'org run debug', 'org run debug list', or 'org run debug "pasted bug"' requests.
---

# Debug Team

## When to use

- User says: `org run debug`
- User says: `org run debug list`
- User says: `org run debug "pasted bug"`

## Core rules

- Read `AGENTS.md` first.
- Obey `docs/company/lock-policy.md` and `docs/company/locks.md` before edits.
- Always update `docs/bugs.md` (and domain bug files if relevant).
- Prefer smallest coherent diff; no new deps without approval.
- Never add logs containing PII.

## Workflow

### 1) Triage (no code yet)

- Restate goal, non-goals, constraints, success metrics.
- Identify smallest shippable step.
- If the request is broad, pick one command to run first:
  - `npm run typecheck`
  - `npm run lint`
  - `npm test`
  - `npm run doctor`

### 2) Bug list updates

- Add new bugs to `docs/bugs.md` before coding.
- If the bug is domain-specific, mirror to:
  - `docs/bugs-ui.md`
  - `docs/bugs-api.md`
  - `docs/bugs-security.md`
  - `docs/bugs-ops.md`

### 3) Locking

- Claim file locks in `docs/company/locks.md` before edits.
- Use the smallest scope and shortest expiry.

### 4) Fix

- Implement minimal, safe changes.
- Prefer eliminating `undefined` optional props by omitting keys.
- Keep multi-tenant boundaries intact.
- After fixes, check with file owners for any functional concerns or behavior changes before finalizing.

### 5) Retest

- Re-run the originating command.
- Update bug status to `Fixed (pending retest)` or `Fixed` with evidence.

## Command-specific modes

### `org run debug`

- Run `npm run typecheck` first.
- Triage failures and propose owners.
- Ask before cross-domain fixes.

### `org run debug list`

- Run `npm run typecheck` (or the command referenced by the user).
- Convert output into bug entries with owner + evidence.
- Do not edit code unless explicitly approved.

### `org run debug "pasted bug"`

- Focus only on the pasted bug.
- Identify suspect file(s) and propose fix.
- Ask for approval before edits unless already granted.

## Output format

- Findings list (prioritized)
- Proposed next steps + owners
- Risks or rule bends (if any)
