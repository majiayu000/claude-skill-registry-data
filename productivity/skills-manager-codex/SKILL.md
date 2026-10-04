---
name: skills-manager
description: Manage Codex functions—skills, MCP servers, and skills-manager-defined plugins—as a unique-ownership catalog and project categories. Use when Codex needs to discover or adopt new user-level functions, group skills/MCPs into a plugin, recommend a minimal function set, create or edit categories, switch a project by linking skills and writing MCPs, inspect backups, validate or repair catalog drift, plan updates, retire, or restore functions.
---

# Skills Manager

Manage the complete function lifecycle through natural-language requests. Treat **function** as the common term for a skill, MCP, or skills-manager-defined plugin. An SM plugin is a managed bundle of skills/MCPs, not a Codex-native plugin.

Use `scripts/manager.py` as the deterministic layer. Users do not need command syntax: translate their intent, show the preview, explain the effect, obtain confirmation, then apply.

## Core contract

- Discover user-level skills only from `$CODEX_HOME/skills` or `~/.codex/skills`; discover user-level MCPs from `$CODEX_HOME/config.toml` or `~/.codex/config.toml`.
- Keep only the skills-manager package under `~/.codex/skills/skills-manager`; it must not contain runtime `config`, `code_*`, `retired`, or `backups` directories. Store all managed functions, configuration, retirement data, and backups under `$SKILLS_MANAGER_HOME` or the default `~/.codex/skills-manager-data`.
- Treat the package as stateless and portable. `setup` creates a new machine's data root from built-in defaults; every later catalog mutation targets that data root, never the package.
- Store each skill/MCP either independently or in exactly one SM plugin. Never register a plugin member as independent.
- Describe each plugin once as a concise aggregate of its member skills/MCPs; keep membership only in `plugins.json`.
- Let categories select independent skills, independent MCPs, and whole plugins. `All` is the non-duplicated active union; `None` is empty and the initial default.
- Switch projects through `<project>/.codex/skills/`, `<project>/.codex/config.toml`, and `<project>/.codex/skills-manager-state.toml`.
- Preserve unrelated project functions. Remove only entries proved SM-owned by project state; preserve same-target links and identical MCPs that existed before SM.
- Keep managed MCP definitions free of `enabled = false`; category presence controls activation.
- Do not update MCP definitions. Every managed MCP has `mcp:<id>: {"type":"none"}` in `updates.json`.
- Update an SM plugin through its member skills: keep one `plugin:<id>` update record covering every member skill, normally one repository/ref with mappings for all of them. Never duplicate those member skills as independent update records.

## Read only what the task needs

- Read [routing.md](references/routing.md) to translate natural language or recommend functions.
- Read [schema.md](references/schema.md) before changing storage, registration, categories, or project state.
- Read [workflows.md](references/workflows.md) before any mutation; it defines every operation and the backup policy.
- Read [repair.md](references/repair.md) only for conflicts, validation failures, drift, or unsupported permanent deletion.

## Mandatory execution protocol

1. Run `scan` and `validate`; batch ambiguities and conflicts.
2. Run the intended mutation without `--apply`. Explain physical moves, config changes, category rewrites, removals, preserved project entries, and conflicts.
3. Obtain confirmation immediately before the matching `--apply`. Never treat an earlier general approval as approval for a changed preview.
4. Ask for uncertain MCP purposes and exact plugin membership/names; do not infer them.
5. After applying, run `validate` and the relevant `scan`, `list`, `switch`, or `backup-status` check.
6. On adoption, register each MCP as `none`; ask for each independent skill's source. Before binding a plugin, confirm that all member skills have compatible sources, then consolidate them under the plugin.
7. Run `update-plan` and discuss every untracked independent skill or plugin. An empty `updates.json` means update maintenance is incomplete, not configured.

If the private data root is absent, preview `setup`, confirm its path, then run `setup --apply` before scanning.

## Backup invariant

Create backups before SM changes a user/project `config.toml`; adopt several MCPs in one backup transaction. Backups are append-only while their total size is at most 500 MB. If they exceed 500 MB, preview removal of top-level backup entries older than 30 days, ask the user explicitly, and delete only after confirmation. Never clean backups automatically or delete recent entries merely to fall below the threshold.
