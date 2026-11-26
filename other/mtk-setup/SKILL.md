---
name: mtk-setup
description: One-stop setup entry point that bootstraps a repo or re-runs architecture audit
type: skill
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
argument-hint: "[--audit|--audit-only] [--merge] [--preview] [--non-interactive] [--no-verify-commands] [--update-guidelines] [--refresh [--dry-run]] [--check]"
user-invocable: true
---

# MTK Setup — Unified Entry Point for Bootstrap and Audit

You dispatch to the right setup workflow skill based on the argument and the repo's state.

## Overview

- **Bootstrap** (no flags): detect the stack, pull the pinned coding guidelines, audit once, generate `AGENTS.md` (plus the `CLAUDE.md` shim), `.claude/tech-stack` and `architecture-principles.md`.
- **Audit** (`--audit`): regenerate `architecture-principles.md` and `conventions.md` after architectural change.
- **Merge** (`--merge`): unify per-repo audits in `.claude/references/audits/` into one team-wide doc.
- **Refresh** (`--refresh`): drift-scoped refresh of every generated artifact, proposing diffs for engineer-edited files.
- **Check** (`--check`): read-only — the staleness plan as a CI gate, plus a graded report of principles whose evidence anchors no longer resolve.
- **Update guidelines** (`--update-guidelines`): bump the coding-guidelines pin to the remote HEAD SHA.

## When To Use

- First time onboarding a repo → `/mtk-setup`.
- Architecture drifted → `/mtk-setup --audit`.
- Several repos' audits to unify → `/mtk-setup --merge`.
- Generated docs drifted → `/mtk-setup --refresh` (`--dry-run` first to preview).
- CI, or "are the docs still accurate, and where has the code left the agreed principles?" → `/mtk-setup --check`.

## Workflow

### STEP 0: Parse Arguments

| Flag | Meaning |
|---|---|
| `--audit` / `--audit-only` | Audit only (no stack detection, no AGENTS.md generation) |
| `--merge` | Multi-repo unification (implies audit) |
| `--preview` | Bootstrap only: show proposed changes, ask before writing |
| `--non-interactive` | Bootstrap/refresh: skip the interview; engineer-edited files defer to Needs review |
| `--no-verify-commands` | Bootstrap only: skip STEP 3.5a command execution |
| `--update-guidelines` | Bump the coding-guidelines pin. Does not re-run bootstrap. |
| `--refresh` | Delegate to `setup-refresh` |
| `--dry-run` | Only with `--refresh`: print the plan, write nothing |
| `--check` | Delegate to `setup-refresh` Check mode. Writes nothing outside `.claude/.mtk-cache/`. |

Combination rules — reject with a clear message:
- `--update-guidelines` combines with nothing.
- `--merge` excludes `--non-interactive`.
- `--refresh` and `--check` exclude each other, `--audit`, `--merge` and `--update-guidelines`.
- `--dry-run` requires `--refresh`.
- `--no-verify-commands` is bootstrap-only.
- `--converge` was retired into `--check`: say so and run `--check`.

### STEP 1: Decide the Target

| Argument | Target |
|---|---|
| `--update-guidelines` | `bash scripts/update-guidelines.sh --bump` (below) |
| `--check` | `.claude/skills/setup-refresh/SKILL.md`, `## Check Mode` |
| `--refresh` | `.claude/skills/setup-refresh/SKILL.md` (pass `--dry-run`, `--non-interactive`) |
| `--merge` | `.claude/skills/setup-audit/SKILL.md` with `--merge` |
| `--audit` / `--audit-only` | `.claude/skills/setup-audit/SKILL.md` |
| none of the above | `.claude/skills/setup-bootstrap/SKILL.md` (pass `--preview`, `--non-interactive`, `--no-verify-commands`) |

**`--update-guidelines`:** run `bash scripts/update-guidelines.sh --bump` and print its output verbatim. The script resolves the remote HEAD to a 40-char SHA, fetches every pinned file at that SHA, hashes all of them before writing, and writes nothing on any failure. It never writes into the plugin cache: a pin read from `$CLAUDE_PLUGIN_ROOT` lands in the repo-local `.claude/mtk-version.json`. Exit 1 is a failed fetch or unreachable remote: report it, and the pin is unchanged. Then tell the engineer: "Guidelines pin updated in `<file the script named>`. Run `/mtk-setup --audit` or `/mtk-setup` to apply them." Never auto-invoke bootstrap.

**Un-bootstrapped repo** (no `.claude/tech-stack`):
- `--audit`: warn via `AskUserQuestion` — "No tech stack detected — this looks like a first-time setup. Audit alone won't generate AGENTS.md. Run `/mtk-setup` with no flags for a full bootstrap. Proceed with audit only? [y/N]"
- `--refresh` / `--check`: do not offer to proceed. Say: "This repo has not been bootstrapped — run `/mtk-setup` with no flags first."

### STEP 2: Follow the Target Skill

Read the target SKILL.md and follow every step inline, including its Verification section.

### STEP 3: Report

```
✅ MTK Setup: [bootstrap|audit|merge|refresh|check|update-guidelines] complete in [duration]. See [output file(s)].
```

## MTK File Resolution

Resolve MTK skill/reference/script paths per `.claude/references/mtk-file-resolution.md` unless the router already stated `MTK_ROOT=<path>` this session; `CLAUDE.md`, `.claude/tech-stack`, `.claude/rules/`, `tasks/`, `docs/`, `.mtk/` stay project-relative.

## Verification

- [ ] Target chosen from the flags; invalid combinations rejected
- [ ] Target skill's Verification section executed
- [ ] Bootstrap: `AGENTS.md`, the `CLAUDE.md` shim, `.claude/tech-stack` and `architecture-principles.md` exist
- [ ] Merge: source audits in `.claude/references/audits/` untouched
- [ ] Check: nothing written outside `.claude/.mtk-cache/`; plan exit code propagated
- [ ] Update guidelines: the script's exit code reported; pin file named
