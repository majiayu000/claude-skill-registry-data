---
name: gz-tidy
persona: main-session
description: Use for repository hygiene; reports governance maintenance findings and regenerates surfaces with --fix.
category: agent-operations
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
model: haiku
metadata:
  skill-version: "1.3.1"
---

# gz tidy

## Overview

`gz tidy` prints a maintenance report and, with `--fix`, regenerates the
control surfaces. It deletes nothing. The handler is `tidy` in
`src/gzkit/commands/tidy.py`; the report has four sections:

- **Validation issues** from `validate_all` (`src/gzkit/validate.py`): the
  manifest, the ledger, every ADR and OBPI document the manifest lists
  against its schema, the control surfaces including sync parity (a
  generated file that differs from what sync would write), the instruction
  audit and the persona files. Each line prints the issue type and message,
  not the file.
- **Orphaned OBPIs**: ledger OBPIs whose parent ADR is absent from the
  ledger graph.
- **Settings vault**: printed when the snapshots of
  `.claude/settings.local.json` are drifted, absent or recoverable
  (`vault_status` in `src/gzkit/settings_vault.py`, GHI #1072). The message
  says what to do.
- **ADRs pending attestation**: every ADR in the ledger graph with no
  attestation event, pool ADRs included — an inventory, not a defect list,
  and never gating.

A finding in any of the first three sections is a policy breach: the run
prints `✗ Maintenance breaches found.` and exits 3 (GHI #1124). It exits 0 with
`✓ All checks passed. Project is tidy.` only when none of them has a finding,
and 1 when the project is not initialized or `--fix` is refused or fails
(below). Until GHI #1125 retires the `validate_all` fork, its `[header]` lines
alone keep the run at exit 3.

Flags:

- `--check` is the report-only mode: the parser refuses it together with
  `--fix` (exit 2). A bare run is also report-only unless `--fix` is given.
- `--fix`, after the report, runs the guarded sync `gz agent sync
  control-surfaces` uses: it refuses with exit 1, writing no mirror, when
  canonical skills fail the sync preflight (`refuse_on_sync_blockers`, GHI
  #1100); otherwise `sync_all` regenerates the surfaces and appends an
  `agent_sync_completed` ledger event, and the post-sync skill audit exits 1
  on a blocking parity error. It repairs control-surface drift only, never
  documents, orphans, the vault or attestations, and unlike `gz agent sync
  control-surfaces` it lists neither the updated paths nor stale mirror-only
  paths. After a successful sync the run re-validates, and the exit status
  judges that tree, so a drift the sync repaired no longer counts.
- `--dry-run` changes only `--fix`, to a single "would sync control
  surfaces" line with no path list. Alone it has no effect.

## Workflow

1. Run `uv run gz tidy > <file> 2>&1` and read the file; the report is long.
2. Act on each section:
   - `[surface] Generated surface is out of sync`: preview with
     `uv run gz agent sync control-surfaces --dry-run`, then sync with that
     command or `uv run gz tidy --fix`. Sync overwrites a hand edit to a
     generated file, so move any intended change into canon first.
   - `[header]` / `[frontmatter]` lines name no file, and raw-schema-check
     the historical OBPI corpus that `gz validate --documents` deliberately
     skips (GHI #500). Run `uv run gz validate --documents` and the
     version-aware `uv run gz validate --briefs` for findings that name the
     file, and act on those.
   - Orphaned OBPIs, a vault notice, and the pending-attestation list are
     reported for the operator; tidy repairs none of them.
3. Report what each section held, what was synced, and what remains open.

## Claude Surface Validation

In Claude Code, after the report:

1. **Hook health**: `.claude/hooks/*.py` and the hook wiring in
   `.claude/settings.json` are generated — the scripts by `setup_claude_hooks`
   in `src/gzkit/hooks/claude.py`, the settings by `sync_claude_settings` in
   `src/gzkit/sync_surfaces.py`, which keeps user-added phases and keys. A hand
   edit shows as a `[surface]` sync-parity issue. If a hook errored at session
   start, dispatch the `claude-code-guide` subagent with the failing hook and
   the error to diagnose it against current Claude Code documentation. The
   repair belongs in the generator and reaches the tree through sync; never
   edit the generated file.
2. **Instructions budget**: run `uv run gz validate --instructions-files-budget`.
   It is an explicit-tier scope, so neither `gz tidy` nor a bare `gz validate`
   runs it. The per-file budgets for `AGENTS.md`, `CLAUDE.md` and
   `.claude/rules/*.md` live in `data/instructions_files_budget.json`. Trim a
   file over budget with the `gz-context-diet` skill.
3. **Skill mirror parity**: run `uv run gz skill audit`. It checks canonical
   `.gzkit/skills/` and the Codex and Claude skill mirrors, each when its
   vendor is enabled in `.gzkit.json` § `vendors`
   (`audit_skills` in `src/gzkit/skills_audit.py`). `gz agent sync
   control-surfaces` clears mirror drift.

## Example

```bash
# Read-only report (identical to --check)
uv run gz tidy > tidy.log 2>&1

# Preview, then apply, the control-surface sync
uv run gz tidy --fix --dry-run
uv run gz tidy --fix

# Actionable, file-named document findings
uv run gz validate --documents
```

## Common Rationalizations

These thoughts mean STOP — you are about to leave drift in place:

| Thought | Reality |
|---------|---------|
| "Tidy exited 0, so the project is tidy" | Tidy exits 0 whatever it reports. Only the printed sections say what it found. |
| "`--check` is the safe mode" | `--check` does nothing a bare run does not; both are read-only. The choice is between reporting and `--fix`. |
| "`--fix` fixed everything tidy reported" | `--fix` only regenerates control surfaces. Document, orphan, vault and attestation findings stay until someone acts on them. |
| "The mirrors look fine — sync isn't needed" | A `[surface]` issue is the sync-parity check saying they are not. "Looks fine" is not a verification. |
| "CLAUDE.md is over budget but it's all useful content" | The budget in `data/instructions_files_budget.json` exists because adherence drops past it. Relocate the narrative through `gz-context-diet`. |
| "Hook errors at startup are pre-existing — not my problem" | Pre-existing failures are still failures. Diagnose, repair the generator, sync. |

## Red Flags

- Reading tidy's exit code instead of its output
- Hand-editing a file under `.claude/hooks/` or `.claude/settings.json` instead of its generator
- Acting on a `[header]` line from tidy without the file-named `gz validate` finding behind it
- An instructions file over its budget (`gz validate --instructions-files-budget`) with no relocation plan
- Hook errors observed but never resolved
- Skill mirrors not regenerated after a skill edit
