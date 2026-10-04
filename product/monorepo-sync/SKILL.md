---
name: monorepo-sync
description: "Synchronize roadmaps, AGENTS.md, versions, and documentation across chainskills monorepo packages — use when updating version numbers, syncing roadmap status, or keeping documentation consistent"
model: haiku
allowed-tools: Read, Edit, Bash(pnpm :*), Bash(git :*), Grep, Glob
---

# Monorepo Sync — chainskills

Keeps all documentation and version metadata consistent across the `cli-mcp-core/` and `vscode-extension/` packages and the monorepo root.

## Files to Keep in Sync

| File | Purpose | Syncs With |
|------|---------|------------|
| `ROADMAP.md` (root) | Canonical roadmap — phases, changelog, decisions | — |
| `AGENTS.md` (root) | Monorepo index | `cli-mcp-core/AGENTS.md` + `vscode-extension/AGENTS.md` |
| `cli-mcp-core/package.json` | CLI version | `ROADMAP.md` changelog |
| `vscode-extension/package.json` | Extension version | `ROADMAP.md` changelog |

## Sync Protocol

### On Version Milestone Completion

1. **Mark phase complete** in canonical roadmap (`ROADMAP.md`):
   - Update phase status: `En cours` -> `Complete (YYYY-MM-DD)`
   - Add changelog entry with features list and metrics
   - Update "Phase suivante" section

2. **Update AGENTS.md files**:
   - Root `AGENTS.md`: update phase status in roadmap table
   - `cli-mcp-core/AGENTS.md`: same update
   - Check that agent/skill references are still valid

3. **Bump package versions** (if applicable):
   - `cli-mcp-core/package.json` -> `version` field
   - `vscode-extension/package.json` -> `version` field

### On New Agent/Skill/Instruction Added

1. Add entry to root `AGENTS.md` (agents table or skills table)
2. Add entry to relevant project AGENTS.md (`cli-mcp-core/AGENTS.md` or `vscode-extension/AGENTS.md`)
3. Verify `applyTo` patterns don't conflict with existing instructions

### On README Update

1. Update `cli-mcp-core/README.md` for CLI/Core changes
2. Update `vscode-extension/README.md` for extension changes
3. Update root `README.md` if monorepo-level changes

## Consistency Rules

- **No duplication**: Root AGENTS.md = index only. Project AGENTS.md = project details.
- **Single source of truth**: `ROADMAP.md` (root) — canonical roadmap for all packages.
- **Version parity**: Both package versions should bump together for cross-cutting changes.
- **Link integrity**: All markdown links in AGENTS.md files must resolve correctly.

## Anti-patterns

- Do not update canonical roadmap but not root roadmap
- Do not add agent to project AGENTS.md but not root AGENTS.md
- Do not allow different phase statuses between canonical and portfolio roadmaps
- Do not bump version in package.json but not in ROADMAP.md changelog
