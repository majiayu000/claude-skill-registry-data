---
name: migrate-skills-between-libraries
description: Use when moving skills between library workspaces or upgrading from a personal library to a team library. Export from one workspace, import into another.
category: workflow
version: 4.1.0
---

# Migrate Skills Between Libraries

## Goal

Move skills from one library workspace to another without losing metadata, breaking dependencies, or duplicating entries.

## Guardrails

- Always use `--dry-run` before any mutating command in the target workspace.
- Always use `--list` to inspect the source library before importing.
- Always use `--format json` for structured output when scripting migrations.
- Never import skills without checking for name collisions in the target workspace first.
- Always run `build-docs` in the target workspace after migration.

## Workflow

### Export: Identify skills to migrate from the source library

1. List all skills in the source workspace.

```bash
cd /path/to/source-library
npx ai-agent-skills list --format json --fields name,tier,workArea,collections
```

2. For house copies, note the skill folder paths. For upstream picks, note the installSource.

### Import: Add skills to the target workspace

3. For house copies, use `vendor` to copy the skill folder into the target:

```bash
cd /path/to/target-library
npx ai-agent-skills vendor /path/to/source-library --skill <name> --area <workArea> --branch <branch> --why "Migrated from source library." --dry-run
npx ai-agent-skills vendor /path/to/source-library --skill <name> --area <workArea> --branch <branch> --why "Migrated from source library."
```

4. For upstream picks, use `catalog` to re-catalog from the original source:

```bash
npx ai-agent-skills catalog <owner>/<repo> --skill <name> --area <workArea> --branch <branch> --why "Migrated from source library." --dry-run
npx ai-agent-skills catalog <owner>/<repo> --skill <name> --area <workArea> --branch <branch> --why "Migrated from source library."
```

5. Rebuild docs in the target workspace.

```bash
npx ai-agent-skills build-docs
```

6. Validate the target workspace.

```bash
npx ai-agent-skills validate
```

## Gotchas

- Skill names must be unique per workspace. Check for collisions before importing.
- House copies are full folder copies — the source and target are independent after migration.
- Upstream picks re-catalog from the original upstream source, not the intermediate library.
- Dependencies (`requires` field) must also be migrated. Check `info --format json` for each skill's dependency graph.
- Collection membership does not transfer automatically. Use `curate --collection <id>` to add migrated skills to target collections.
