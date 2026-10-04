---
name: github-scaffold
description: "Seeds the ALDC project setup that apm install does not deploy (Copilot entrypoint, aldc.yaml, plans/memory.md, tools/). Use when initializing a new Business Central project with ALDC, right after apm install, on any OS including Claude Code."
---

# Skill: ALDC Project Scaffold

`apm install` deploys the ALDC **primitives** (agents, skills, prompts,
instructions). It does **not** deploy the non-primitive setup pieces that the
legacy npm/VS Code installer used to seed — APM has no automatic post-install
hook. This skill carries those pieces and a cross-platform installer so you get
a project layout equivalent to the npm install.

## What it seeds

Run from the consumer project root **after `apm install`**. Existing files are
skipped (pass `--force` to overwrite):

| Target | Purpose |
|--------|---------|
| `.github/copilot-instructions.md` | Copilot routing entrypoint (routes to the 4 public agents) |
| `aldc.yaml` | APM-aware BCQuality / toolkit configuration (project root) — carries a `distribution.roots` block resolving the split `.github`/`.agents` Copilot layout, and pins a `copilotEntrypointHash` instead of the canonical byte-diff mode (see below) |
| `aldc.code-workspace` | Multi-root workspace, **generated** (not copied) from the detected project layout — root `app.json` vs `App/`+`Test/` split — plus the BCQuality root |
| `.github/plans/memory.md` | Session-continuity memory file |
| `tools/bcquality`, `tools/aldc-validate`, `tools/bc-agents` | Helper tooling; `aldc-validate` resolves each primitive category through `aldc.yaml`'s `distribution.roots` |

The 14 SDD document templates are **not** seeded here — they ship as assets of
the `skill-sdd-contracts` skill (single source of truth) and resolve there.

### Copilot entrypoint coherence caveat

The canonical validator's default "trimmed" mode byte/size-diffs the deployed
entrypoint against its full source (`instructions/copilot-instructions.md`).
That source is never deployed to an APM consumer (only `*.instructions.md`
files deploy), so the seeded `aldc.yaml` instead pins a SHA-256
(`copilotEntrypointMode: "hash"` + `copilotEntrypointHash`) computed from the
entrypoint at scaffold-seed time. This detects **local drift** (someone
hand-edited the deployed entrypoint after scaffolding) but cannot detect the
upstream source evolving without a fresh `apm install` + re-scaffold.

## Usage

Cross-platform (recommended — Windows, macOS, Linux, Claude Code):

```bash
# Copilot / Cursor / Codex (skills land in .agents/skills/)
node .agents/skills/github-scaffold/scripts/Install-Scaffold.mjs

# Claude Code (skills land in .claude/skills/)
node .claude/skills/github-scaffold/scripts/Install-Scaffold.mjs
```

Windows PowerShell wrapper:

```powershell
powershell -ExecutionPolicy Bypass -File .agents/skills/github-scaffold/scripts/Install-Scaffold.ps1
```

Add `--force` (or `-Force`) to overwrite files that already exist.

## Behavior

- Idempotent: re-running skips files that already exist.
- The seed content lives in `scripts/seed/` and is kept in sync with the
  canonical ALDC repo by `scripts/build-apm.mjs`.
- `aldc.code-workspace` is layout-aware: detects `App/app.json` + `Test/app.json`
  (AL-Go split) vs a root `app.json` (simple project) and generates the
  `folders` array accordingly, reading the BCQuality `home` path from the
  already-seeded (or pre-existing) `aldc.yaml`. Like every other target, it is
  skipped if it already exists unless `--force` is passed.
