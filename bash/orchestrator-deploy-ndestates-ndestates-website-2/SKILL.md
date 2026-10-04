---
name: orchestrator-deploy
description: >
  Deploy orchestrator .grok skills, prompts, agents, and root chains (CHAIN.md,
  chains/registry.yaml) to any target project. Tracks customized files in
  deploy-state.json; prompts overwrite, skip, or merge on conflict. Pre-deploy
  backups with --rollback. Selectable bundles include .claude and .copilot. Use with
  `.github/prompts/orchestrator-v2.prompt.md`-deploy or .github/skills/chain/SKILL.md template-deploy. Run from orchestrator repo.
argument-hint: "Target path — optional --dry-run, --selections, --rollback"
user-invocable: true
disable-model-invocation: false
---

# Orchestrator Deploy

Deploy the orchestrator template bundle from **this repo** to a selected project (e.g. lightstone, ndestates-io). Uses `scripts/deploy_grok_to_project.py` — never inline shell for deploy logic.

## What gets deployed

Bundle: `scripts/deploy-bundle.yaml` — **named selections** via `--selections`.

| Selection | Paths |
|-----------|-------|
| `grok` (default) | Grok tree: skills, prompts, agents, registry |
| `chains` (default) | `CHAIN.md`, `chains/registry.yaml` |
| `loops` (default) | `LOOP.md`, `loop-budget.md`, `patterns/` |
| `scripts` (default) | sync, audits, deploy script |
| `claude` | Claude commands + agents + `CLAUDE.md` |
| `copilot` | Copilot skills mirror |
| `github` | GitHub skills, agents, prompts |

Default (no flag): `grok,chains,loops,scripts`. Use `--selections all` or e.g. `--selections grok,claude,copilot`.

**Before deploying `claude` / `copilot` / `github`:** run sync on the **source** orchestrator repo so mirrors are current:

```bash
python3 scripts/sync_grok_to_github_claude.py
```

**Never auto-deploy:** `STATE.md`, `loop-run-log.md`, `TODO/`, `docs/codebase/`, project manifests, `.grok/deploy-backups/`.

## Rollback (mandatory safety net)

Every deploy (unless `--no-backup`) snapshots changed files to:

`<target>/.grok/deploy-backups/<timestamp>/`

| Command | Action |
|---------|--------|
| `--list-backups <target>` | List available backups |
| `--rollback <target>` | Restore latest backup |
| `--rollback <target> --backup-id 2026-06-17T143022Z` | Restore specific backup |
| `--rollback <target> --dry-run` | Preview restore actions |

Rollback restores backed-up files, removes files created during that deploy, and restores `deploy-state.json`.

## Conflict policy (mandatory)

When a target file differs from template and is **customized** or **first-seen without deploy-state**:

| Option | Action |
|--------|--------|
| **skip** (default) | Leave project file unchanged; mark customized |
| **overwrite** | Replace with template copy |
| **merge** | Write `<file>.merged` with conflict markers; human resolves |
| **diff** | Show unified diff, then choose again |

Non-interactive: `--non-interactive --default-action skip` (safe) or `--yes` (overwrite all).

## Workflow

1. **Confirm source** — run from orchestrator repo root (`ndestates`.github/prompts/orchestrator-v2.prompt.md``).

2. **List selections** (optional):

   ```bash
   python3 scripts/deploy_grok_to_project.py --list-selections
   ```

3. **Dry-run first** (recommended):

   ```bash
   python3 scripts/deploy_grok_to_project.py /path/to/target --dry-run
   python3 scripts/deploy_grok_to_project.py /path/to/target --dry-run --selections grok,claude,copilot
   ```

4. **Interactive deploy**:

   ```bash
   python3 scripts/deploy_grok_to_project.py /path/to/target
   python3 scripts/deploy_grok_to_project.py /path/to/target --selections all
   ```

5. **On target after deploy**:

   ```bash
   cd /path/to/target
   python3 scripts/sync_grok_to_github_claude.py
   python3 scripts/check_name_alignment.py
   bash scripts.github/skills/chain/SKILL.md-audit.sh
   ```

6. **Review** `.grok/deploy-state.json`, `.grok/deploy-reports/`, and backup id in report.

7. **Rollback if needed**:

   ```bash
   python3 scripts/deploy_grok_to_project.py /path/to/target --rollback
   ```

## Chain invocation

```text
.github/skills/chain/SKILL.md template-deploy
```

Steps: load-cache → orchestrator-deploy (this skill).

Or direct: ``.github/prompts/orchestrator-v2.prompt.md`-deploy /home/nickd/projects/lightstone --selections grok,claude,copilot`

## Agent / human handoff

When running as agent: list conflicts and ask user per file or batch:
- overwrite all customized
- skip all
- merge specific paths
- which selections to include (especially `claude` / `copilot`)

Do not auto-overwrite customized project scripts (e.g. `.github/skills.github/skills/project-drift-guardian/SKILL.md/scripts/drift-check.sh`).

## Anti-patterns

- Deploying without dry-run on production fork
- Deploying `claude`/`copilot` without syncing source first
- Overwriting `docs/codebase/` or manifests (excluded by design)
- Inline `cp -r` without deploy-state tracking
- Skipping `sync_grok_to_github_claude.py` on target after deploy
- Using `--no-backup` without explicit approval

## Related

- Bundle manifest: `scripts/deploy-bundle.yaml`
- Adoption guide: `docs/TEMPLATE_ADOPTION.md`
- Template docs: `docs/guides/template-deploy.md`