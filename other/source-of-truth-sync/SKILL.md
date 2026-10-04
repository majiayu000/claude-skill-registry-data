---
name: source-of-truth-sync
description: >
  MANDATORY after editing any contract-paired source file (state machine, schema, routes,
  websocket, milestones, CLAUDE.md, docs/contracts/). Automatically triggered by the
  contract-edit-guard hook. Updates all corresponding contract docs and CLAUDE.md sections
  to maintain source-of-truth alignment. Must complete before continuing other work.
---

# Source of Truth Sync

You have just edited a source file that has contract documents and/or CLAUDE.md sections that must stay in sync. Follow this procedure to update them all.

## Step 1: Identify What Changed

Read the git diff to see exactly what source files were modified:

```bash
git diff --name-only
git diff --name-only --cached
```

Cross-reference against this contract map to identify which docs need updating:

| Source File | Contract Doc | CLAUDE.md Section |
|---|---|---|
| `server/src/taskStateMachine.js` | `docs/contracts/task-state-machine.md` | `STATE_MACHINE` |
| `server/src/db/schema.js` | `docs/contracts/database-schema.md` | `DB_SCHEMA` |
| `server/src/routes/tasks.js` | `docs/contracts/api-endpoints.md` | `API_ENDPOINTS` |
| `server/src/routes/projects.js` | `docs/contracts/api-endpoints.md` | `API_ENDPOINTS` |
| `server/src/routes/documents.js` | `docs/contracts/api-endpoints.md` | `API_ENDPOINTS` |
| `server/src/routes/activity.js` | `docs/contracts/api-endpoints.md` | `API_ENDPOINTS` |
| `server/src/ws.js` | `docs/contracts/websocket-events.md` | `WEBSOCKET_EVENTS` |
| `server/src/events.js` | `docs/contracts/websocket-events.md` | `WEBSOCKET_EVENTS` |
| `server/src/milestoneSync.js` | *(none)* | `MILESTONE_SYSTEM` |
| `server/src/templates/milestoneTasks.js` | *(none)* | `MILESTONE_SYSTEM` |
| `client/src/utils/taskTransitions.js` | `docs/contracts/task-state-machine.md` | `STATE_MACHINE` |
| `client/src/components/layout/PhaseBar.jsx` | *(none)* | `PHASE_SYSTEM` |

## Step 2: Read the Source (Current State)

For each modified source file, read it and extract the current implementation details:
- States, transitions, guards (state machine)
- Column names, types, constraints (schema)
- Endpoints, methods, body fields, responses (routes)
- Event names, payloads, triggers (websocket)
- Auto-transition rules (milestones)

## Step 3: Update Contract Docs

For each contract doc that needs updating:

1. Read the current contract doc
2. Compare against the source implementation from Step 2
3. Update the contract doc to match the source exactly
4. Preserve the document's existing structure and formatting style

**Rules for contract docs:**
- The source code is the authority. Docs describe what the code does.
- Use exact names from the code (field names, event names, status values).
- Do not add aspirational content (things the code should do but doesn't yet).
- Do not remove sections that are still accurate.

## Step 4: Update CLAUDE.md

For each CLAUDE.md section that needs updating:

1. Read the current CLAUDE.md section
2. Compare against the source implementation from Step 2
3. Update the section to match the source exactly
4. Keep the YAML/JSON format consistent with the rest of CLAUDE.md

**Rules for CLAUDE.md:**
- CLAUDE.md is a compressed reference. Keep it concise.
- Use the same code-block format as existing sections.
- Do not expand sections unnecessarily — token budget matters.
- Cross-check: if you update STATE_MACHINE, verify SAFE_MODIFICATIONS and DEBUG_CHECKLIST still reference the correct file paths and field names.

## Step 5: Cross-Check Related Sections

Some changes cascade. After updating, verify these cross-references:

- If states changed: check `SAFE_MODIFICATIONS.add_status` steps
- If API endpoints changed: check `FILE_MAP` references and `DEBUG_CHECKLIST.api_404`
- If WS events changed: check `SAFE_MODIFICATIONS.add_ws_event` steps and `DEBUG_CHECKLIST.ui_not_updating`
- If schema changed: check `ANTI_PATTERNS` examples still use valid field names
- If phases changed: check `PHASE_SYSTEM` and `MILESTONE_SYSTEM` consistency

## Step 6: Verify

After all updates:

1. Run `npm test --prefix server` — confirm tests still pass
2. Run `npm run lint --prefix client` — confirm no lint errors
3. Re-read each updated doc and CLAUDE.md section one more time to confirm accuracy
4. Report what was updated

## Output

Summarize:
```
SYNC COMPLETE
  Source files changed: [list]
  Contract docs updated: [list]
  CLAUDE.md sections updated: [list]
  Tests: PASS/FAIL
  Lint: PASS/FAIL
```
