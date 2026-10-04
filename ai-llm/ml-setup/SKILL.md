---
name: ml-setup
description: Sets up the BMad ML module in a project. Use when the user requests to 'install ML module', 'configure BMad ML', or 'setup BMad ML'.
---

# Module Setup

## Overview

Installs and configures BMad ML into a project. Module identity (name, code, version) comes from `./assets/module.yaml`. Collects user preferences and writes them to three files:

- **`{project-root}/_bmad/config.yaml`** — shared project config: core settings at root plus an `ml` section with module metadata and module-specific values. User-only keys (`user_name`, `communication_language`) are **never** written here.
- **`{project-root}/_bmad/config.user.yaml`** — personal settings intended to be gitignored: `user_name`, `communication_language`, and any module variable marked `user_setting: true` in `./assets/module.yaml`. These values live exclusively here.
- **`{project-root}/_bmad/.session/`** — subagent session state, ephemeral and gitignored
- **`{project-root}/_bmad/module-help.csv`** — registers module capabilities for the help system.

Both config scripts use an anti-zombie pattern — existing entries for this module are removed before writing fresh ones, so stale values never persist.

`{project-root}` is a **literal token** in config values — never substitute it with an actual path. It signals to the consuming LLM that the value is relative to the project root, not the skill root.

## On Activation

1. Read `./assets/module.yaml` for module metadata and variable definitions (the `code` field is the module identifier)
2. Check if `{project-root}/_bmad/config.yaml` exists — if a section matching the module's code (`ml`) is already present, inform the user this is an update
3. Check for per-module configuration at `{project-root}/_bmad/ml/config.yaml`. If it exists:
   - If `{project-root}/_bmad/config.yaml` does **not** yet have an `ml` section: this is a **fresh install**. Inform the user that installer config was detected and values will be consolidated into the new format.
   - If `{project-root}/_bmad/config.yaml` **already** has an `ml` section: this is a **legacy migration**. Inform the user that legacy per-module config was found alongside existing config, and legacy values will be used as fallback defaults.
   - In both cases, per-module config files and directories will be cleaned up after setup.

If the user provides arguments (e.g. `accept all defaults`, `--headless`, or inline values like `project name is AlphaModel, framework is jax`), map any provided values to config keys, use defaults for the rest, and skip interactive prompting. Still display the full confirmation summary at the end.

## Collect Configuration

Ask the user for values. Show defaults in brackets. Present all values together so the user can respond once with only the values they want to change (e.g. "change framework to jax, rest are fine"). Never tell the user to "press enter" or "leave blank" — in a chat interface they must type something to respond.

**Default priority** (highest wins): existing new config values > legacy config values > `./assets/module.yaml` defaults. When legacy configs exist, read them and use matching values as defaults instead of `module.yaml` defaults. Only keys that match the current schema are carried forward — changed or removed keys are ignored.

**Core config** (only if no core keys exist yet): `user_name` (default: BMad), `communication_language` and `document_output_language` (default: English — ask as a single language question, both keys get the same answer), `output_folder` (default: `{project-root}/_bmad-output`). Of these, `user_name` and `communication_language` are written exclusively to `config.user.yaml`. The rest go to `config.yaml` at root and are shared across all modules.

**Module config** — ask using each variable's `prompt` from `./assets/module.yaml`:

| Variable | Prompt | Default | Type |
|----------|--------|---------|------|
| `project_name` | What is your ML/AI project called? | `{directory_name}` | text |
| `ml_framework` | Primary ML framework? | pytorch | single-select: PyTorch, TensorFlow, JAX |
| `experiment_tracker` | Experiment tracking tool? | wandb | single-select: W&B, MLflow, TensorBoard, None |
| `planning_artifacts` | Where should planning artifacts be stored? | `{output_folder}/ml-planning` | path |
| `experiment_artifacts` | Where should experiment artifacts be stored? | `{output_folder}/experiments` | path |
| `project_knowledge` | Where should research and references be stored? | `docs/research` | path |

## Write Files

Write a temp JSON file with the collected answers structured as `{"core": {...}, "module": {...}}` (omit `core` if it already exists). Then run both scripts — they can run in parallel since they write to different files:

```bash
python3 ./scripts/merge-config.py --config-path "{project-root}/_bmad/config.yaml" --user-config-path "{project-root}/_bmad/config.user.yaml" --module-yaml ./assets/module.yaml --answers {temp-file} --legacy-dir "{project-root}/_bmad"
python3 ./scripts/merge-help-csv.py --target "{project-root}/_bmad/module-help.csv" --source ./assets/module-help.csv --legacy-dir "{project-root}/_bmad" --module-code ml
```

Both scripts output JSON to stdout with results. If either exits non-zero, surface the error and stop. The scripts automatically read legacy config values as fallback defaults, then delete the legacy files after a successful merge. Check `legacy_configs_deleted` and `legacy_csvs_deleted` in the output to confirm cleanup.

Run `./scripts/merge-config.py --help` or `./scripts/merge-help-csv.py --help` for full usage.

## Create Output Directories

After writing config, create any output directories that were configured. For filesystem operations only (such as creating directories), resolve the `{project-root}` token to the actual project root and create each path-type value from `config.yaml` that does not yet exist — this includes `output_folder`, `planning_artifacts`, `experiment_artifacts`, and `project_knowledge`. The paths stored in the config files must continue to use the literal `{project-root}` token; only the directories on disk should use the resolved paths. Use `mkdir -p` or equivalent to create the full path.

## Detect IDE Skills Directory

Before cleaning up legacy directories, detect which IDE skills directory the project uses. Check for the existence of these directories under `{project-root}`:

1. `.claude/skills/`
2. `.cursor/skills/`
3. `.opencode/skills/`

Use the first one found as `{active_skills_dir}`. If multiple exist, prefer the one that contains the module's skills. If none exist, skip the `--skills-dir` safety check in the cleanup step.

## Cleanup Legacy Directories

After both merge scripts complete successfully, remove the installer's package directories. Skills and agents in these directories are already installed at `{active_skills_dir}` — the `_bmad/` directory should only contain config files.

```bash
python3 ./scripts/cleanup-legacy.py --bmad-dir "{project-root}/_bmad" --module-code ml --skills-dir "{project-root}/{active_skills_dir}"
```

The script verifies that every skill in the legacy directories exists at `{active_skills_dir}` before removing anything. Directories without skills are removed directly. If the script exits non-zero, surface the error and stop. Missing directories (already cleaned by a prior run) are not errors — the script is idempotent.

Check `directories_removed` and `files_removed_count` in the JSON output for the confirmation step. Run `./scripts/cleanup-legacy.py --help` for full usage.

## Confirm

Use the script JSON output to display what was written — config values set (written to `config.yaml` at root for core, `ml` section for module values), user settings written to `config.user.yaml` (`user_keys` in result), help entries added, fresh install vs update. If legacy files were deleted, mention the migration. If legacy directories were removed, report the count and list. Then display the `module_greeting` from `./assets/module.yaml` to the user.

## IDE Project Instructions (Optional)

After confirming config, offer to create or append `{project-root}/AGENTS.md` using `./assets/agents-md-snippet.md`, resolving config tokens. OpenCode auto-loads `AGENTS.md` every session (falling back to `CLAUDE.md` if absent). If the target already contains a managed `bmad-ml` block, skip with a note that it is already configured.

## Outcome

Once the user's `user_name` and `communication_language` are known (from collected input, arguments, or existing config), use them consistently for the remainder of the session: address the user by their configured name and communicate in their configured `communication_language`.
