---
name: t1k:kit
description: "Maintain TheOneKit repos as a kit maintainer. Use for releasing kits, scaffolding new kits, cross-kit validation, schema migration, and E2E test runs."
keywords: [maintainer, release, scaffold, validate, audit, migrate, kit]
version: 1.0.0
argument-hint: "<subcommand> [options]"
effort: medium
origin: theonekit-core
repository: The1Studio/theonekit-core
module: null
protected: true
---

# TheOneKit Kit — Maintainer Toolkit

Unified kit maintenance skill. All subcommands are for **kit maintainers only**, not end-users.

## Subcommands

| Subcommand | Usage | Purpose |
|---|---|---|
| `validate` | `/t1k:kit validate [--cross-kit]` | Schema, activation paths, keyword conflicts, preset refs, naming |
| `release` | `/t1k:kit release [--skip-validate]` | Guided release: validate → CI gate → GitHub release → Discord |
| `sync` | `/t1k:kit sync [--pull] [--status-only]` | Pull all kits, check version compat, release-action alignment |
| `scaffold` | `/t1k:kit scaffold <name> [--org]` | Create new kit repo from template with full boilerplate |
| `audit` | `/t1k:kit audit [--all]` | Health audit: file counts, modules, keywords, CI, freshness |
| `migrate` | `/t1k:kit migrate [--dry-run]` | Schema migration (e.g., registryVersion 1→2) |
| `test` | `/t1k:kit test [--all] [--kit <name>]` | Comprehensive 15-phase E2E testing: install, modules, CLI, release infra |

## Quick Reference

```bash
/t1k:kit validate              # Validate current kit repo
/t1k:kit validate --cross-kit  # Validate across all installed kits
/t1k:kit release               # Guided release workflow
/t1k:kit sync --pull           # Pull and check all kits
/t1k:kit scaffold theonekit-x  # Scaffold new kit
/t1k:kit audit --all           # Audit all kit repos
/t1k:kit migrate --dry-run     # Preview schema migration
/t1k:kit test --all            # E2E test all kits
/t1k:kit test --kit unity      # E2E test specific kit
```

## Subcommand Details

Read the reference file for full details on each subcommand:
- `references/validate.md` — per-kit and cross-kit validation checks
- `references/release.md` — release workflow steps and gates
- `references/sync.md` — cross-kit synchronization protocol
- `references/scaffold.md` — new kit scaffolding template
- `references/audit.md` — health audit checks and scoring
- `references/migrate.md` — schema migration steps
- `references/test.md` — 12-phase E2E test plan

## Gotchas
- **Do not add origin metadata to source** — `origin`, `repository`, `module`, `protected` fields are CI/CD-injected by release action, not authored in source. See `/t1k:doctor` gotchas.
- **Modular kits use `release-modules.cjs`** (custom release script), NOT semantic-release directly. Flat kits (e.g., theonekit-rn) still use semantic-release. `release-modules.cjs` produces per-module ZIPs + `manifest.json` index.
- **`t1k-modules.json` is GENERATED** for the `modules` section — do not hand-author it. Source of truth is each `module.json`. Only `presets` in `t1k-modules.json` are hand-authored.
- **`.releaserc.json` MUST include `package.json` and `.claude/metadata.json` in `@semantic-release/git` assets** — without this, `package.json` stays at `0.0.0` forever. Every kit repo needs: `"assets": ["package.json", "CHANGELOG.md", ".claude/metadata.json"]`
- **Do not hardcode `version` or `buildDate` in source `metadata.json`** — CI generates these from `package.json`. Source should only contain manually-maintained fields (`name`, `repository`, `deletions`).

## Future: Self-Improving AI Pipeline

T1K vision: the kit should self-teach and improve using aggregated consumer data. Planned pipeline:
1. User errors collected via telemetry → D1 (already exists)
2. Scheduled AI agent (cron) queries D1 for error clusters (same fingerprint, 3+ occurrences, multiple users)
3. AI aggregates patterns → synthesizes root cause, workaround, prevention
4. Auto-generates gotcha entries for relevant skill SKILL.md files
5. Opens PR to kit repo automatically
6. Maintainer reviews and merges → next release distributes to ALL users

**Status:** Not yet implemented. See CLAUDE.md "Self-Improving AI Vision" for context.

## Auto-Activation Keywords

Triggers on: `kit validate`, `kit release`, `kit sync`, `kit scaffold`, `kit audit`, `kit migrate`, `kit test`, `kit health`, `kit status`, `cross-kit`, `maintainer`, `test kit`, `test install`, `test modules`, `e2e kit`, `validate installation`, `self-improving`, `auto-gotcha`, `gotcha generation`, `ai aggregation`, `learn from users`
