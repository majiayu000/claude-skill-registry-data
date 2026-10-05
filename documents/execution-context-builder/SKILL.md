---
name: execution-context-builder
description: Synthesizes the chosen (or only) candidate flow into the canonical execution-context Markdown + JSON artifacts under .claude/clarifications/. Activates after flow-detector returns a single candidate, or after flow-selector confirms the user's choice. Never asks follow-up questions.
---

# Execution Context Builder

Take a `full_context` record and write the two canonical artifacts.

## Activation Triggers

This skill activates when:
- `flow-detector` returned exactly **one** candidate (skip selector, come straight here).
- `flow-selector` has resolved the user's pick (or synthesized one from "Other").

This skill never asks the user a question. If the input `full_context` has missing fields, fill them with conservative defaults (see "Field Defaults" below) and move on.

## Inputs

The skill receives:
- `task` — the original task description (string), and optionally a source ref (e.g., `ENG-123`).
- `full_context` — the chosen candidate's context record. Schema is defined in `references/execution-context.json`.

## Process

### 1. Resolve the slug

Generate a slug from the task title:
- Lowercase, replace non-alphanumeric runs with `-`, strip leading/trailing `-`.
- Truncate to **60 characters** max, on a word boundary.
- If the result is empty (no usable characters), fall back to `clarification-YYYYMMDD-HHMMSS` using the current local time.

Examples:
- `"Send message on sign-in"` → `send-message-on-sign-in`
- `"Migrate auth to Better Auth (Phase 2)"` → `migrate-auth-to-better-auth-phase-2`
- `"!!!"` → `clarification-20260427-143022`

### 2. Fill defaults

If any required field in `full_context` is missing, fill with these defaults:

| Field | Default |
|-------|---------|
| `trigger.timing` | `"after"` |
| `trigger.preconditions` | `[]` |
| `action.channel` | `"in-app"` |
| `flow.mode` | `"async"` |
| `flow.transport` | `null` |
| `failure_handling.strategy` | `"retry"` |
| `failure_handling.details` | `"3 attempts with exponential backoff, then log"` |
| `out_of_scope` | `[]` |

Defaults are not user-visible questions — silently apply them.

### 3. Build the JSON artifact

Read `references/execution-context.json`, populate it from `full_context`, add metadata:

```json
{
  "task": { "title": "<original task>", "source": "<ticket ref or null>", "slug": "<slug>" },
  "entity": "...",
  "trigger": { "event": "...", "timing": "...", "preconditions": [...] },
  "action": { "verb": "...", "channel": "...", "recipient": "..." },
  "flow": { "services": [...], "mode": "...", "transport": "..." },
  "failure_handling": { "strategy": "...", "details": "..." },
  "out_of_scope": [...],
  "metadata": {
    "created_at": "<ISO-8601>",
    "created_by": "clarify@0.1.0"
  }
}
```

Validate the result parses with a JSON parser before writing. If parsing fails, fix and retry; never write malformed JSON.

### 4. Build the Markdown artifact

Read `references/execution-context.md`, fill the template from the same `full_context`. Keep it human-readable — the developer is the primary reader.

### 5. Write both files

Path: `.claude/clarifications/<slug>.local.md` and `.local.json`.

- Create the `.claude/clarifications/` directory if it doesn't exist.
- If a file with the same slug already exists, **refuse to overwrite**. Print:
  > A clarification already exists at `.claude/clarifications/<slug>.local.md`.
  > Delete it first, or re-run `/clarify` with a different task title.
- Write atomically: write to a temp file, then rename. Prevents partial files on crash.

### 6. Optional cross-pack hooks (silent if absent)

After writing, if `.claude/failure-log.local.md` exists in the project, append a one-liner under "Pattern Mistakes":

```
- [<ISO-8601>] <slug> clarified — see .claude/clarifications/<slug>.local.md (kind: assumption-resolved)
```

If the failure-log file doesn't exist, skip silently. Do not create it.

### 7. Print the summary

```
✓ Execution context written:
  .claude/clarifications/<slug>.local.md
  .claude/clarifications/<slug>.local.json
```

Do not print the full content of either file. The developer opens the file to review.

## Field Reference

See `references/execution-context.md` and `references/execution-context.json` for the canonical templates.

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Ask the user to fill in missing fields | Apply the defaults table silently |
| Overwrite an existing artifact | Refuse and tell the user to delete it |
| Write the JSON without parsing it first | Validate, then write |
| Print the full Markdown to chat | Print only the file path; the developer opens it |
| Create `.claude/failure-log.local.md` if it's missing | Skip the cross-pack hook silently |

## Success Criteria

- [ ] Both `.local.md` and `.local.json` files are written.
- [ ] JSON parses cleanly with a strict parser.
- [ ] Markdown contains every required section: Task, Entity, Trigger, Action, Flow, Failure handling, Out of scope, Metadata.
- [ ] Slug matches the rules in step 1.
- [ ] No question was asked during execution-context generation.
- [ ] Optional failure-log append is silent when the file is absent.
