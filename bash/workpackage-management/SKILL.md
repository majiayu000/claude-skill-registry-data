---
name: workpackage-management
description: "Use when performing workpackage actions: start, pause, complete, delete, defer, reorder, update progress, or check dependencies. Not for reading WP history or definitions."
user-invocable: false
allowed-tools: Read, Bash, Glob
version: 2.0.0
author: Ashay Kubal @ Qball Inc.
tags: workpackage, lifecycle, progress, dependencies
---

> **CLI Usage:** When unsure about a CLI's interface or flags, run it with `--help` first. Do NOT attempt to discover functionality by reading plugin source code — doing so leads to incorrect execution from assumptions made without context of the holistic flow.

# Workpackage Management Skill

This skill manages workpackage lifecycle operations in the CLEAR framework. All `.clear/` mutations
are routed through CLI scripts — **never use Write or Edit on `.clear/` paths directly**.

## Plugin Root Resolution

CLI commands in this skill reference `$CLEAR_PLUGIN_ROOT` — a `.claude/settings.json` env var the shell expands. The SessionStart hook persists it, but settings env vars load at session **launch**, so on a brand-new consumer's **first session** (before its next restart) the variable is empty and `node "$CLEAR_PLUGIN_ROOT/build/..."` fails with `MODULE_NOT_FOUND`.

**First-session bootstrap** — if `$CLEAR_PLUGIN_ROOT` is empty, set it inline in the *same* Bash call as the CLI (each Bash call is a fresh shell, so a separate `export` would not carry over):

```bash
export CLEAR_PLUGIN_ROOT="${CLEAR_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}"
```

Prepend it to the CLI in one shell line: `export CLEAR_PLUGIN_ROOT="${CLEAR_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}"; <node "$CLEAR_PLUGIN_ROOT/build/..." command>`. `${CLAUDE_PLUGIN_ROOT}` resolves in this SKILL.md body to the actually-loaded plugin path; once the consumer restarts, `$CLEAR_PLUGIN_ROOT` is populated and the assignment is a harmless no-op. Reference files are left unchanged.

## When to Use

### TAKE ACTION (run CLI commands) when user says:
- "start workpackage P1.3" / "begin working on P1.3"
- "pause this workpackage"
- "complete this workpackage" / "mark P1.2 as done"
- "delete workpackage P1.3"
- "defer P1.3" / "defer this workpackage"
- "reorder P1.3 to position 2"
- "update progress on this workpackage" / "set progress to 75"
- "check dependencies for P1.4"

### JUST READ FILES (no CLI) when user asks:
- "what workpackages exist?" → Read `.clear/workpackages/registry.yaml`
- "what's in workpackage P1.2?" → Read `.clear/workpackages/P1.2.yaml`
- "what's the status of all workpackages?" → Read registry
- "what did we complete in P1.1?" → Read the workpackage file

## DO NOT Use For

- Questions about workpackage history or reading raw workpackage documents — just read the file directly.
- Plan-level operations (creating plans, checking blockers, milestone updates) — use the `plan-management` skill.

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
| Create workpackage | `create-cli --phase=<phase-id> --title="..." [--from-stdin]` |
| Update WP fields | `update-cli <wp-id> --status=<s> --description="..." [--acceptance-criteria-file=...] [--deliverables-file=...]` |
| Update deliverable | `update-cli <wp-id> deliverable <del-id> --status=<s> --weight=<n> --pattern=<glob>` |
| List workpackages | `status-cli list [--all] [--phase] [--status]` |
| Show WP details | `status-cli show <wp-id>` |
| Active WP status | `status-cli` |
| Check dependencies + blockers | `deps-cli --workpackage=<id> [--check-deliverables]` |

---

## CLI Reference

All lifecycle operations use `lifecycle-cli.js`. All progress operations use `progress-cli.js`.

**Common flags** (passed automatically by the `/cf-workpackage` command):
- `--cwd=<project-dir>` — project root
- `--session-id=<id>` — current session ID
- `--session-number=<num>` — current session number

**CLI base path**:
```
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/lifecycle-cli.js"
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/progress-cli.js"
```

---

## Lifecycle Operations

### Start a Workpackage

**User says**: "start workpackage P1.3", "begin P1.3"

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/lifecycle-cli.js" \
  start <id> [--force] \
  --cwd="$PROJECT_DIR" --session-id="$SESSION_ID" --session-number="$SESSION_NUMBER"
```

- `<id>` — workpackage display ID (e.g., `P1.3`) or system ID
- `--force` — start even if dependencies are not satisfied
- The CLI validates dependencies, updates registry status, and sets the active workpackage

**Present to user**: Confirmation of start, list of deliverables and acceptance criteria.

### Pause a Workpackage

**User says**: "pause this workpackage", "pause current work"

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/lifecycle-cli.js" \
  pause \
  --cwd="$PROJECT_DIR" --session-id="$SESSION_ID" --session-number="$SESSION_NUMBER"
```

- Pauses the currently active workpackage (no ID needed)

**Present to user**: Confirmation of pause.

### Complete a Workpackage

**User says**: "complete this workpackage", "mark P1.2 as done"

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/lifecycle-cli.js" \
  complete [--force] \
  --cwd="$PROJECT_DIR" --session-id="$SESSION_ID" --session-number="$SESSION_NUMBER"
```

- Completes the currently active workpackage
- `--force` — complete even if not all deliverables are marked done
- The CLI verifies deliverables, updates status in registry, and identifies newly unblocked WPs

**Present to user**: Completion confirmation, list of unblocked workpackages.

### Delete a Workpackage

**User says**: "delete workpackage P1.3", "remove P1.3"

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/lifecycle-cli.js" \
  delete <id> --confirm \
  --cwd="$PROJECT_DIR" --session-id="$SESSION_ID" --session-number="$SESSION_NUMBER"
```

- `<id>` — workpackage display ID or system ID
- `--confirm` (or `-y`) — required to confirm deletion
- Without `--confirm`, the CLI returns a warning and does not delete

**Present to user**: Deletion confirmation or warning if `--confirm` was omitted.

### Defer a Workpackage

**User says**: "defer P1.3", "defer this workpackage", "postpone P1.3"

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/lifecycle-cli.js" \
  defer <id> [--reason=<reason>] \
  --cwd="$PROJECT_DIR" --session-id="$SESSION_ID" --session-number="$SESSION_NUMBER"
```

- `<id>` — workpackage display ID or system ID
- `--reason=<reason>` — optional reason for deferral
- The CLI updates the WP status to deferred and propagates changes to master-plan.yaml

**Present to user**: Deferral confirmation with reason (if provided).

### Reorder a Workpackage

**User says**: "reorder P1.3 to position 2", "move P1.3 to slot 1"

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/lifecycle-cli.js" \
  reorder <id> --position=<N> \
  --cwd="$PROJECT_DIR" --session-id="$SESSION_ID" --session-number="$SESSION_NUMBER"
```

- `<id>` — workpackage display ID or system ID
- `--position=<N>` — required, 1-based target position within the phase
- The CLI resolves display IDs, reorders within the phase, and propagates display ID changes to master-plan.yaml

**Present to user**: Reorder confirmation with old and new positions.

---

## Progress Operations

### Update Progress

**User says**: "update progress", "set progress to 75"

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/progress-cli.js" \
  progress [--set <N>] \
  --cwd="$PROJECT_DIR"
```

- Without `--set`: reports current progress percentage and remaining deliverables
- `--set <N>`: sets progress to N% for the active workpackage

**Present to user**: New progress percentage and remaining deliverables.

### Validate Workpackage

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/progress-cli.js" \
  validate \
  --cwd="$PROJECT_DIR"
```

- Validates the active workpackage structure and state

---

## Update Operations

`update-cli` is the comprehensive mutation surface for an existing workpackage. Two modes:

### WP-level fields

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/update-cli.js" \
  <wp-id> \
  --status=<status> \
  --description="<text>" \
  --acceptance-criteria-file=<path.json> \
  --deliverables-file=<path.json> \
  --verification-file=<path.json> \
  --notes-file=<path.json> \
  --in-scope-file=<path.json> \
  --out-of-scope-file=<path.json> \
  --upstream-file=<path.json> \
  --downstream-file=<path.json> \
  --cwd="$PROJECT_DIR" --session-id="$SESSION_ID" --session-number="$SESSION_NUMBER"
```

- `<wp-id>` — workpackage display ID (e.g., `WP-AUTH.1`, `P1.3`) or system ID
- `--status=<s>` — one of `not_started`, `in_progress`, `paused`, `blocked`, `complete`, `deferred`, `archived`
- Array fields each accept either `--<field>=<json>` (inline JSON) OR `--<field>-file=<path>` (path to JSON file). Use file variant for non-trivial content.
- `--force` — allows status transitions normally rejected (e.g., complete → not_started)

### Per-deliverable fields

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/update-cli.js" \
  <wp-id> deliverable <del-id> \
  --status=<s> \
  --description="<text>" \
  --weight=<n> \
  --pattern=<glob> \
  --cwd="$PROJECT_DIR" --session-id="$SESSION_ID" --session-number="$SESSION_NUMBER"
```

- `<del-id>` — deliverable ID within the WP (from the WP YAML's `deliverables[].id`)
- `--status=<s>` — deliverable-level: `not_started`, `in_progress`, `complete`
- `--weight=<n>` — non-negative integer (see Weight Conventions below)
- `--pattern=<glob>` — filename glob that auto-matches the deliverable for hook-driven progress (see Auto-Promotion below)

### Important Behavioral Notes

**Audit log gating** — Audit log entries (`workpackage/update`) are emitted only when BOTH `--session-id` AND `--session-number` are passed. The production hook chain forwards these from `.clear/state/session.json` automatically; direct CLI users supply them explicitly. If either is absent, the update succeeds but no audit row is written.

**YAML comment loss** — `update-cli` writes via `yaml.dump` round-trip, which does NOT preserve comments in the WP YAML. If a WP YAML has hand-authored comments that matter, hand-edit it (after pausing CLI mutations) rather than running update-cli.

**Atomic write** — Schema validation runs pre-write; on validation failure the YAML is left unchanged. Writes are atomic (temp file + rename).

### Auto-Promotion (PostToolUse Hook)

The PostToolUse hook auto-promotes deliverables based on file writes that match the deliverable's `--pattern` glob (or description-extracted file references):

- First matching write on a `not_started` deliverable → promotes to `in_progress`
- Subsequent matching write when the description-extracted file is present on disk → promotes to `complete`

This is the intended success path: as you write the files a deliverable describes, the deliverable progresses automatically. No explicit `update-cli` call needed in normal flow.

**Revert command** (for stub-then-iterate workflows where a stub file triggered premature completion):

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/update-cli.js" \
  <wp-id> deliverable <del-id> --status=in_progress --cwd="$PROJECT_DIR"
```

Run this after writing a placeholder/stub that the hook marked complete, before fleshing it out.

---

## Read-Only Operations

These operations are best served via `status-cli` for formatted output. Direct file reads of `.clear/workpackages/` are a fallback if the CLI is unavailable or for ad-hoc YAML inspection.

### Active Workpackage Status

**User says**: "what workpackage am I on?", "current WP?"

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/status-cli.js" \
  --clear-dir=./.clear
```

(No subcommand — defaults to active WP status.)

### List Workpackages

**User says**: "what workpackages exist?", "show all WPs"

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/status-cli.js" \
  list [--all] [--phase] [--status] \
  --clear-dir=./.clear
```

- `--all` / `-a` — include completed workpackages
- `--phase` / `-p` — group output by phase
- `--status` / `-s` — group output by status

Fallback: read `.clear/workpackages/registry.yaml` directly.

### View Workpackage Details

**User says**: "what's in P1.2?", "show workpackage P1.2"

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/status-cli.js" \
  show <wp-id> --clear-dir=./.clear
```

Fallback: read `.clear/workpackages/<id>.yaml` directly.

### Check Dependencies

**User says**: "check dependencies for P1.4", "what blocks P1.4"

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/deps-cli.js" \
  --workpackage=<wp-id> [--check-deliverables] \
  --clear-dir=./.clear
```

- `--workpackage=<id>` — required; WP to check
- `--check-deliverables` — also validate that upstream deliverables exist on disk

Returns the list of blocking dependencies + readiness verdict. Fallback (manual): read `.clear/workpackages/<id>.yaml` for upstream IDs, then read each upstream's status from registry.yaml.

---

## Workpackage Structure

Location: `.clear/workpackages/wp-<systemId>.yaml` (filename uses the system ID, not the display ID)

```yaml
id: P4.1                                    # display ID (user-facing, position-derived)
systemId: wp-03cbf224                       # internal slug (stable, used in filename)
position: 1                                 # 1-based position within phase
phase: ph-24415d90                          # parent phase systemId
title: Design System and Color Tokens
status: complete                            # not_started | in_progress | paused | blocked | complete | deferred | archived
type: feature                               # feature | spike | bug | refactor | doc
priority: medium                            # low | medium | high
description: >-
  CSS custom property design token system with vibrant color palette,
  typography, spacing, theme provider, and dev preview route
scope:
  in_scope: []
  out_of_scope: []
dependencies:
  upstream: []                              # array of WP systemIds this WP needs first
  downstream: []                            # array of WP systemIds blocked by this WP
deliverables:
  - id: deliverable-1
    pattern: ''                             # filename glob for hook-driven auto-promotion
    weight: 0                               # see Weight Conventions
    status: not_started                     # not_started | in_progress | complete
    description: 'src/renderer/styles/tokens.css — complete CSS token set'
  - id: deliverable-2
    pattern: ''
    weight: 0
    status: not_started
    description: 'src/renderer/styles/global.css — global reset and base styles'
```

## Registry Structure

Location: `.clear/workpackages/registry.yaml`

The registry indexes all workpackages with their resolved display IDs, statuses, and system IDs. Dependencies live on the individual WP YAMLs (`dependencies.upstream` / `dependencies.downstream`), NOT on the registry rows.

```yaml
version: '1.0'
lastUpdated: '2026-05-11'
workpackages:
  - id: P5.1
    systemId: wp-647a5f25
    position: 1
    phase: ph-24415d8f
    title: Filter, Search, and Sort
    status: complete
    file: wp-647a5f25.yaml
    progress: 0
  - id: P5.2
    systemId: wp-289ede2c
    position: 2
    phase: ph-24415d8f
    title: Export and Import
    status: complete
    file: wp-289ede2c.yaml
    progress: 0
  - id: P6.1
    systemId: wp-669b0123
    position: 1
    phase: ph-24415d8e
    title: Visual Dashboard View
    status: not_started
    file: wp-669b0123.yaml
```

Note: this describes the **CLEAR-managed WP YAMLs** at `.clear/workpackages/`. The **dev/plan WP YAMLs** at `plans/**/workpackages/*.yaml` are author-edited specification documents with a different shape (`acceptance_criteria`, `verification`, `notes`, `closure_summary`, etc.) and are not registry input.

## Progress Calculation

Progress is calculated from deliverables:

```
progress = Σ(deliverable.weight × deliverable.completion) / 100
```

### Weight Conventions

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

## Automatic Hook Integrations

| Script | Triggered By | What It Does |
|--------|--------------|--------------|
| `workpackage-load.sh` | SessionStart hook | Loads active workpackage, validates dependencies |
| `workpackage-progress.sh` | UserPromptSubmit hook | Tracks deliverable completion |
| `workpackage-deps.sh` | On demand | Validates dependency graph |

---

## Important Rules

1. **Never use Write or Edit on `.clear/` paths.** The PreToolUse guard blocks these. All mutations go through CLIs which use `fs.writeFileSync` (invisible to the guard).
2. **Parse CLI JSON output** to confirm `"status": "success"` before reporting to the user.
3. **Display IDs vs System IDs** — The CLIs accept both forms; the CLI internally resolves display ID → systemId before mutation.
   - **Display IDs** are user-facing, derived from phase + position. Format: `P<phase>.<position>` (e.g., `P1.3`, `P6.1`) for numbered phases, or `WP-<plan>.<position>` / `WP-<plan>-<suffix>` (e.g., `WP-AUTH.1`, `WP-AUTH-spike`) for plan-driven WPs. They CHANGE when WPs are reordered. Prefer in user-visible output, prompts, and Command Reference examples.
   - **System IDs** are internal stable slugs. Format: `wp-<8-char-hex>` (e.g., `wp-03cbf224`, `wp-647a5f25`). They NEVER change once assigned. Stored in: WP YAML `systemId` field, registry.yaml `systemId` field, registry.yaml `workpackages[].file` (the YAML filename uses the systemId — `wp-03cbf224.yaml`), and error messages / audit log rows. You'll encounter systemIds in CLI error messages, audit log entries, log file references, and registry-backfill operations.
   - **When to use which** — Pass the display ID when invoking CLIs by hand or scripting against user input. Use the systemId when scripting against registry data or correlating with audit logs (where only systemIds appear). Either works at the CLI boundary.
