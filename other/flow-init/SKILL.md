---
name: flow-init
description: Initialize, inspect, resume, or migrate portable PWDEV Flow project state. Use when the user asks to set up PWDEV Flow, adopt an existing repository or legacy PWDEV Code workspace, resume its workflow, or diagnose its current state.
---

# Initialize PWDEV Flow

Read [workflow](../../references/workflow.md), [artifacts](../../references/artifacts.md), [migration](../../references/migration.md), and [safety](../../references/safety.md) before changing project state.

## Procedure

1. Inspect the repository without reading secrets:
   - locate `AGENTS.md` and read applicable instructions;
   - treat `CLAUDE.md` as optional compatibility context when present;
   - inspect manifests, source layout, tests, and recent Git history;
   - never open `.env`, credentials, tokens, private keys, or certificates.
2. Check for `.planning/flow/config.json`, `.planning/flow/state.md`, and the legacy `.planning/config.json`.
3. Route the request as `inspect`, `initialize`, or `migrate`:
   - if Flow state exists, do not overwrite it; summarize the active workflow, last gate, artifacts, and next valid action;
   - if legacy config exists and Flow config does not, report a migration candidate instead of initializing over it;
   - use `migrate` only when the user asks to adopt the legacy workspace.
4. For `migrate`:
   - resolve [migrate_legacy.py](../../scripts/migrate_legacy.py) from this installed plugin and run `plan` with the active repository root and `--runtime <your adapter>`;
   - present mappings, excluded field names, and conflicts without exposing excluded values;
   - stop for explicit approval before `apply`;
   - after approval, run `apply`, create missing Flow state/directories without overwriting existing paths, and inventory legacy artifacts in `.planning/flow/migration.md`;
   - do not copy or move legacy artifacts without a second approval for exact paths;
   - record `migrated` through the audit helper only when the migrated config enables audit.
5. If state does not exist and the user requested fresh initialization:
   - classify the repository as `greenfield` or `brownfield` from existing source and history;
   - create `.planning/flow/quick/` and `.planning/flow/reports/`;
   - create configuration and state using the exact schemas in [artifacts](../../references/artifacts.md);
   - set the artifact language from the user's current language unless explicitly configured otherwise;
   - record `runtime` as the adapter you are running as, `claude` or `codex`; it is metadata about who initialized the workspace and never makes the artifacts unreadable from the other runtime;
   - set `auto_commit` to `false`.
6. Report created, migrated, or discovered paths and recommend one next action.

## Constraints

- Preserve existing configuration fields that this version does not recognize.
- Preserve `.planning/config.json` byte-for-byte during migration.
- Do not add project dependencies, hooks, branches, commits, or remote configuration.
- Do not create or rewrite `AGENTS.md` unless the user separately requests it.
- Keep all initialization writes under `.planning/flow/`.

## Output

Return `MODE`, `STATUS`, repository classification, state path, configuration path, `MIGRATION` when applicable, and `NEXT`. Link every real local artifact with an absolute path in the final response.
