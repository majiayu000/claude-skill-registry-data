---
name: edit-manual
description: Safely hand-edit configuration files with precise change control and rollback
argument-hint: "[file]"
related:
  - deep-review-codebase
  - ask-me
  - learn
  - follow-best-practice
  - dont-over-engineer
  - use-scripts
  - update-references

---

## Goal

Safely hand-edit configuration files with precise change control, plus backup, rollback, and full validation

## Scope

Use for hand-editing configuration files such as `vite.config.ts`, `turbo.json`, `package.json`, `tsconfig.json`, `biome.jsonc`, `lefthook.yml`, `uno.config.ts`, `drizzle.config.ts`, `.github/workflows/*.yml`, and other config files

Not for creating entirely new configuration (use `/deep-review-codebase` instead)

## Execute

### 1. Pre-Edit Safety Check

> Goal: Check the environment before editing so rollback is always possible

1. Verify the git working tree is clean: run `git status --porcelain`; if there are unstaged changes → ask the user before proceeding (use `/ask-me`)
2. Record the file's hash before editing: run `git rev-parse HEAD` to keep the current commit hash for rollback
3. If the file is not yet tracked by git → create a backup copy in `$env:TEMP` before editing
4. If it is a monorepo, identify the affected workspaces

### 2. Read And Understand

> Goal: Read the config file and official docs before editing to understand the change's impact

1. Read the config file to be edited until you understand its structure and current settings
2. Run `/learn-from-web` or `/follow-best-practice` for the tool the config relates to
3. Identify which workspaces this change affects and whether cross-workspace sync is needed
4. Check version compatibility of dependencies related to the config being changed

### 3. Plan And Preview Changes

> Goal: Plan the edits and preview the diff before applying, to reduce risk

1. Identify the exact points to change and the desired new values
2. Check dependencies and constraints (e.g. version compatibility, plugin requirements, CI/CD pipeline impact)
3. Run `/dont-over-engineer` to plan the minimal necessary changes
4. Record an impact analysis: which files are affected, which CI/CD pipelines change, which workspaces need sync
5. If it is a monorepo with many workspaces to change (> 5 files) → use `/use-scripts` to create a validation script

### 4. Apply Edits

> Goal: Edit the config file precisely, changing only what is necessary

1. Use `edit` or `multi_edit` for the config file changes
2. Change only the necessary points; leave unrelated settings untouched
3. Preserve the config file's original indentation and style
4. If it exceeds 10 files → use `/use-scripts` to automate the edits and validation
5. Run `/update-references` to update the related references

### 5. Post-Edit Validation

> Goal: Verify the config's correctness across every dimension after editing

1. Run `/check-reference` to confirm there are no broken references
2. Scan for secrets: verify the edit did not embed secrets, API keys, or credentials — if the config has sensitive values, use environment variables instead
3. Run `/run-verify` to check lint, typecheck, and scans
4. Run config-specific validation per the table in Rules section `Config-Specific Validation`
5. If there are errors, run `/resolve-errors` first — if unfixable after 3 attempts → rollback and report
6. If it is `.github/workflows/*.yml` → verify the workflow syntax is correct and every secret reference is valid

### 6. Verify And Finalize

> Goal: Confirm the change actually works and breaks nothing

1. If it is a build config → test that `bun run build` passes
2. If it is a CI/CD config → verify the pipeline will not fail from the change
3. Delete the backup file in `$env:TEMP` after confirming the edit passes all validation
4. If validation fails and cannot be fixed → rollback with `git restore --source=<hash> --staged --worktree -- <file>` and report
5. Summarize the change: files edited, values changed, verified impact

## Rules

### 1. Safety And Rollback

- Always verify the git working tree is clean before editing — if not clean → ask the user first
- Always record the commit hash before editing, for rollback via `git restore --source=<hash> --staged --worktree -- <file>`
- Files not tracked by git → create a copy in `$env:TEMP` before editing
- If validation fails within 3 attempts → rollback and report (do not force a fix)
- Never edit multiple config files at once without a rollback plan

### 2. Understand Before Edit

- Always read and understand the config file before editing
- Run `/follow-best-practice` or `/learn-from-web` for unfamiliar tools
- Check that tool's official documentation before changing settings
- Never guess config values without understanding the impact — if unsure → ask the user

### 3. Minimal And Precise

- Change only what is necessary; leave unrelated settings untouched
- Always run `/dont-over-engineer`
- Never auto-format or restructure an entire config file to fix one point
- Preserve the config file's original indentation and style

### 4. Secrets And Security

- Never put secrets, API keys, passwords, or credentials directly in a config file
- Use environment variables or a secrets manager (e.g. Infisical) for sensitive values
- After editing → verify no secrets leaked into the changed files
- If the config has `env` or `secrets` fields → verify they reference environment variables, not hardcoded values
- Run `/run-audit` if the edit involves dependencies or security settings

### 5. Consistency Across Workspaces

- In a monorepo, check whether the change must be synced across workspaces
- Root config should serve as the base for workspaces
- Workspace-specific config should override only what is necessary
- Keep terminology and format consistent across all configs

### 6. Config-Specific Validation

After editing, validate according to the config file type:

| Config File | Validation Command | Pass Condition |
|-------------|-------------------|----------------|
| `vite.config*.ts` | `bun --filter website build` | Build succeeds with no errors |
| `turbo.json` | `bun run build` | Turbo runs with no config errors |
| `package.json` | `bun install --frozen-lockfile` | Install succeeds, no lockfile conflicts |
| `tsconfig.json` | `bun run typecheck` | Typecheck passes |
| `biome.jsonc` | `bunx biome lint` | Lint runs with no config errors |
| `lefthook.yml` | `bunx lefthook validate` | Validation passes |
| `uno.config.ts` | `bun --filter website build` | Build succeeds, CSS not broken |
| `drizzle.config.ts` | `bun --filter website db:generate` | Migration generation succeeds |
| `.github/workflows/*.yml` | Check syntax with a YAML parser | YAML valid, secret references correct |
| `playwright.config.ts` | `bun run test:e2e --list` | Test listing runs with no errors |

### 7. Use Scripts For Complex Edits

- If more than 5 config files need changes → use `/use-scripts` to automate the edits and validation
- Scripts must have a dry run mode to preview before real execution
- Scripts must validate the config structure after editing (e.g. JSON/YAML schema validation)
- Delete scripts from `$env:TEMP` after use

## Expected Outcome

- Configuration files edited precisely, minimally, and safely
- A clear rollback path if the edit fails validation
- Changes pass every validation type in the Config-Specific Validation table
- No broken references and no leaked secrets after the edit
- Configs stay consistent across the monorepo when cross-workspace sync is involved
- Backup files in `$env:TEMP` deleted after the edit is confirmed successful
