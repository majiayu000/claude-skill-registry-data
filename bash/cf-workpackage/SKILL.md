---
name: cf-workpackage
version: 1.1.0
author: Ashay Kubal @ Qball Inc.
description: Manage workpackage lifecycle — view status, list, create, start, pause, track progress, validate, complete, or delete. Use when the user mentions workpackages, asks to start or pause work, wants progress updates, or needs to change workpackage state.
user-invocable: true
argument-hint: "[subcommand|help] [id] [options]"
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---

> **CLI Usage:** When unsure about a CLI's interface or flags, run it with `--help` first. Do NOT attempt to discover functionality by reading plugin source code — doing so leads to incorrect execution from assumptions made without context of the holistic flow.

# Workpackage Management

Manage the workpackage lifecycle: view status, list, create, start, pause, track progress, validate, complete, or delete workpackages.

## Plugin Root Resolution

CLI commands in this skill reference `$CLEAR_PLUGIN_ROOT` — a `.claude/settings.json` env var the shell expands. The SessionStart hook persists it, but settings env vars load at session **launch**, so on a brand-new consumer's **first session** (before its next restart) the variable is empty and `node "$CLEAR_PLUGIN_ROOT/build/..."` fails with `MODULE_NOT_FOUND`.

**First-session bootstrap** — if `$CLEAR_PLUGIN_ROOT` is empty, set it inline in the *same* Bash call as the CLI (each Bash call is a fresh shell, so a separate `export` would not carry over):

```bash
export CLEAR_PLUGIN_ROOT="${CLEAR_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}"
```

Prepend it to the CLI in one shell line: `export CLEAR_PLUGIN_ROOT="${CLEAR_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}"; <node "$CLEAR_PLUGIN_ROOT/build/..." command>`. `${CLAUDE_PLUGIN_ROOT}` resolves in this SKILL.md body to the actually-loaded plugin path; once the consumer restarts, `$CLEAR_PLUGIN_ROOT` is populated and the assignment is a harmless no-op. Reference files are left unchanged.

## When to Use This Skill

| Trigger | Examples |
|---------|---------|
| Active workpackage status | "What workpackage am I on?", "Current WP?" |
| List or show workpackages | "Show all workpackages", "What's in phase 2?" |
| Lifecycle actions | "Start WP-2.1", "Let's begin the next workpackage", "Pause this one" |
| Progress or validation | "Update progress to 80%", "Is this WP ready to complete?" |
| Complete or delete | "Mark this workpackage done", "Delete WP-1.3" |

**Not for:** Plan operations (`/cf-plan`), knowledge base (`/cf-knowledge`), session status (`/cf-status`).

---

## Command Reference

WP CLIs at `$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/`. Run with `--clear-dir=./.clear`. All WP CLIs derive `basePath` from `--clear-dir`; no separate flag is needed.

| Action | CLI Command |
|--------|-------------|
| Start workpackage | `lifecycle-cli start <id> [--force]` |
| Pause workpackage | `lifecycle-cli pause` |
| Complete workpackage | `lifecycle-cli complete [--force]` |
| Delete workpackage | `lifecycle-cli delete <id> --confirm` |
| Defer workpackage | `lifecycle-cli defer <id> [--reason="..."]` |
| Reorder workpackage | `lifecycle-cli reorder <id> --position=<N>` |
| View/set progress | `lifecycle-cli progress [--set <N>]` |
| Validate completion readiness | `lifecycle-cli validate` |
| Create workpackage | `create-cli --phase=<phase-id> --title="..."` |
| Update WP fields | `update-cli <wp-id> --status=<s> --description="..." [--*-file=<path>]` |
| Update deliverable | `update-cli <wp-id> deliverable <del-id> --status=<s> --weight=<n> --pattern=<glob>` |
| List workpackages | `status-cli list [--all] [--phase] [--status]` |
| Show workpackage details | `status-cli show <id>` |
| Active workpackage status | `status-cli` |
| Check dependencies + blockers | `deps-cli --workpackage=<id> [--check-deliverables]` |

---

## Pre-Flight Check

```bash
if [ ! -d ".clear" ]; then
  echo "Error: CLEAR not initialized. Run /cf-init first."; exit 1
fi
```

---

## Subcommand Table

| Subcommand | Type | Reference File | Intent Signals |
|------------|------|----------------|----------------|
| `list` | [R] | `references/list.md` | "list", "show all", "what workpackages" |
| `show` | [R] | `references/show.md` | "show", "details", "tell me about" |
| `progress` | [R] | `references/progress.md` | "progress", "how far", "percentage" |
| `validate` | [R] | `references/validate.md` | "validate", "check", "ready to complete?" |
| `deps` | [R] | `references/deps.md` | "dependencies", "what blocks", "blockers", "is this WP ready" |
| `help` | [R] | `references/help.md` | "help", "how do I", "usage" |
| `create` | [W] | `references/create.md` | "create", "add", "new workpackage" |
| `start` | [W] | `references/start.md` | "start", "begin", "activate", "let's work on" |
| `pause` | [W] | `references/pause.md` | "pause", "stop for now", "take a break" |
| `complete` | [W] | `references/complete.md` | "done", "finished", "complete", "mark complete" |
| `update` | [W] | `references/update.md` | "update", "change", "edit", "set status", "modify deliverable" |
| `defer` | [W] | `references/defer.md` | "defer", "postpone", "push back", "later" |
| `reorder` | [W] | `references/reorder.md` | "reorder", "move to position", "shift WP" |
| `delete` | [W] | `references/delete.md` | "delete", "remove", "archive" |

---

## Routing

Follow these steps **in order**. Track which step you reached — this determines whether confirmation is needed.

**Step 1 — Check `$ARGUMENTS` for an explicit subcommand.**
Check whether `$ARGUMENTS` literally starts with one of the subcommand keywords from the table above (e.g., `start`, `complete`, `list`). This is a string match, not intent inference.
- If YES: load `references/{subcommand}.md`, pass remaining arguments. **Done — skip steps 2-4.**
- If NO (empty, missing, or does not start with a table keyword): continue to step 2.

**Step 2 — Infer intent from the user's natural language message.**
`$ARGUMENTS` did not contain an explicit subcommand. Determine which subcommand best matches the user's intent from their message. Use the subcommand table's intent signals, the "When to Use" examples, and the conversation context.
- If you can identify a specific subcommand with reasonable confidence: continue to step 3.
- If the user's message is purely a status or overview inquiry with no action intent (e.g., "what's my current workpackage?"): load `references/default.md`. **Done.** Only use this exit if the message contains no entity identifiers (WP ID, phase name) and expresses no specific action intent.
- If you cannot determine intent with reasonable confidence: go to step 4.

**Step 3 — Confirm before write actions (NL-inferred only).**
You reached this step via intent inference (step 2), not explicit arguments (step 1).
- If the inferred subcommand is a **read** action ([R] in the table): load the reference file immediately.
- If the inferred subcommand is a **write** action ([W] in the table): **you MUST confirm before proceeding.** Ask: "I'll run **{subcommand}**{details}. Proceed?" where `{details}` includes the target identifier (e.g., " on WP-003"). For destructive actions (delete, complete), always include the target ID. Wait for the user's response. Only load the reference file after the user confirms.

**Step 4 — Ambiguity fallback.**
Ask the user: "I matched `/cf-workpackage` but I'm not sure which action you want. Did you mean: {top 2-3 candidates}?" Do NOT silently fall through to `default`.

---

## State Transitions

| From | To | Command |
|------|-----|---------|
| not_started | in_progress | `start` (deps satisfied) |
| not_started | archived | `delete` |
| in_progress | paused | `pause` |
| in_progress | complete | `complete` (validated) |
| paused | in_progress | `start` |
| paused | archived | `delete` |
| complete | archived | `delete` |

## Auto-Promotion (PostToolUse Hook)

Deliverables auto-promote based on file writes that match the deliverable's `--pattern` glob (or description-extracted file references) — you do NOT need to call `update-cli` manually in the normal flow:

- First matching write on a `not_started` deliverable → promotes to `in_progress`
- Subsequent matching write when the description-extracted file is present on disk → promotes to `complete`

A deliverable match is the canonical "in-scope" signal: when a write matches a deliverable, the WP's `scope.in_scope` is not checked. Scope warnings are emitted only for files that do NOT match any deliverable AND fall outside a pattern-shaped `scope.in_scope` (natural-language scope items are treated as descriptive and not enforced).

**Revert command** (for stub-then-iterate workflows where a stub triggered premature `complete`):

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/update-cli.js" \
  <wp-id> deliverable <del-id> --status=in_progress --cwd="$PROJECT_DIR"
```

Run this after writing a placeholder that the hook marked complete, before fleshing it out.

## Display IDs vs System IDs

The CLIs accept both forms; the CLI internally resolves display ID → systemId before mutation.

- **Display IDs** are user-facing, derived from phase + position. Format: `P<phase>.<position>` (e.g., `P1.3`, `P6.1`) for numbered phases, or `WP-<plan>.<position>` / `WP-<plan>-<suffix>` (e.g., `WP-AUTH.1`, `WP-AUTH-spike`) for plan-driven WPs. They CHANGE when WPs are reordered. Prefer in user-visible output and prompts.
- **System IDs** are internal stable slugs. Format: `wp-<8-char-hex>` (e.g., `wp-03cbf224`). They NEVER change once assigned. Stored in: WP YAML `systemId` field, registry.yaml `systemId` field + filename, and audit log rows. You'll encounter systemIds in CLI error messages, log file references, and registry-backfill operations.
- **When to use which** — Pass the display ID when invoking CLIs by hand or scripting against user input. Use the systemId when scripting against registry data or correlating with audit logs (where only systemIds appear). Either works at the CLI boundary.

## Error Codes

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | Invalid usage / missing arguments |
| 2 | Workpackage not found |
| 3 | Invalid state transition |
| 4 | Blocked by dependencies |
| 5 | Validation failed |

## Related Commands

`/cf-plan`, `/cf-status`, `/cf-knowledge`, `/cf-debug`

---

## Weight Conventions

Each deliverable in a workpackage carries a `weight` field used by progress calculation. The CLI surface (`update-cli deliverable <id> --weight=<n>`) accepts any non-negative integer — there is no upper cap because `calculateProgress` is ratio-based, so the magnitude itself is cosmetic.

For consistency across the codebase, **use weights that sum to 100 within each workpackage**. This matches the dominant convention already in use:

- `workflow.md`: 35 / 30 / 15 / 20
- `feature-brief.md`: 40 / 30 / 20 / 10
- 30+ test fixtures: 100 / 50 / 35 / 30 / 90 (single-deliverable WPs use 100)

### Caveats

- **Mixed-weight WP, one deliverable at weight 0**: that deliverable contributes nothing to progress regardless of its status.
- **All deliverables at weight 0**: activates the legacy equal-contribution path — every deliverable counts the same. This is supported for backward compatibility but should not be the deliberate choice for new WPs.
- **Any positive integer scale works mathematically** (e.g., 1 / 2 / 1 / 1 sums to 5 and is ratio-equivalent to 20 / 40 / 20 / 20). However, mixing scales across WPs makes registry-level inspection harder. Prefer percentage-summing-to-100.

When using `update-cli deliverable <id> --weight=<n>` to correct a weight, validate the post-update sum against the WP's original convention before completing.

---

## Completion Checklist

- [ ] Pre-flight check passed
- [ ] Correct subcommand reference loaded
- [ ] Command executed successfully
- [ ] Output displayed to user
