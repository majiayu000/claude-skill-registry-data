---
name: sync-migration
description: User-invoked as /sync-migration. Compares the date in .github/copilot/Migration-report.md with the latest git history touching .claude/, then syncs changed Claude files into the Copilot layout when Claude is ahead.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
invocation: /sync-migration
---

# Sync Migration

Keep the Copilot migration current with the latest Claude-side changes.

This skill treats `.github/copilot/Migration-report.md` as the sync boundary:

- Read `**Date**: YYYY-MM-DD` from `.github/copilot/Migration-report.md`
- Fetch the latest git date touching `.claude/`
- If `.claude` is newer, migrate the changed files

## Helper

Use the helper script first:

```bash
python scripts/sync_copilot_migration.py --json
```

It reports:

- `migration_date`
- `last_claude_date`
- `claude_ahead`
- `direct_copy[]` — safe 1:1 sync candidates
- `manual_port[]` — transformed surfaces that need a real Copilot-aware port

## Workflow

1. **Check whether Claude is ahead**
   - Run `python scripts/sync_copilot_migration.py --json`.
   - If `claude_ahead` is `false`, stop and report that the migration is current.

2. **Apply safe direct ports**
   - Run:
     ```bash
     python scripts/sync_copilot_migration.py --apply
     ```
   - This copies changed files from:
     - `.claude/agents/**` → `.github/copilot/agents/**`
     - `.claude/skills/**` → `.github/copilot/skills/**`
   - This includes `references/` and `examples/` assets, not just `SKILL.md`.

3. **Manually port transformed surfaces**
   - Review every `manual_port[]` item from the helper output.
   - Apply the change to the Copilot-native target instead of copying blindly.

   Manual-port rules:

   - `.claude/hooks/*.py` → `.github/hooks/*.py`
     - Preserve Copilot JSON output behavior (`permissionDecision`,
       `additionalContext`, `decision` for `Stop`).
     - Do **not** overwrite native Copilot hook protocol handling with raw Claude code.

   - `.claude/settings.json` → `.github/hooks/aegis-hooks.json`
     - Sync new hook matchers, new hook scripts, or policy intent.
     - Preserve Copilot event names and repository-level hook layout.

   - `.claude/loops/*.md` → `.github/copilot/loops-emulated/**/SKILL.md`
     - Preserve the Copilot iterative-skill adaptation.
     - Do not reintroduce `ScheduleWakeup` assumptions.

   - `.claude/CLAUDE.md`
     - Propagate durable policy changes into relevant Copilot agents, skills,
       hooks, and `Migration-report.md`.

4. **Refresh the migration boundary**
   - After all changed Claude files are migrated, update:
     - `**Date**:` in `.github/copilot/Migration-report.md`
   - Set it to the `last_claude_date` reported by the helper script.

5. **Summarize what changed**
   - In `.github/copilot/Migration-report.md`, update any sections that are now stale:
     - structure
     - hook map
     - remaining gaps
   - Mention newly migrated files or behavior changes if they affect how Copilot works.

## Output

Report:

- migration date
- last Claude git date
- whether Claude was ahead
- direct-copy files synced
- manual-port files updated
- final date written back to `.github/copilot/Migration-report.md`

## Completion checklist

- [ ] `python scripts/sync_copilot_migration.py --json` run
- [ ] If `claude_ahead = true`, direct-copy files applied with `--apply`
- [ ] Every `manual_port` item reviewed and ported to the Copilot-native target
- [ ] `.github/hooks/*.py` changes preserve Copilot hook JSON protocol
- [ ] `.github/hooks/aegis-hooks.json` updated if `.claude/settings.json` changed
- [ ] `.github/copilot/Migration-report.md` date set to `last_claude_date`
- [ ] Final migration summary reflects the newly synced state
