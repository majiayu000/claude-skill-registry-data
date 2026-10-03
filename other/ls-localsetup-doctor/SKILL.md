---
name: ls-localsetup-doctor
description: "Use for LocalSetup doctor repair workflows: dry-run review, decision handling, conservative apply, backup evidence, and post-repair verification."
metadata:
  version: "1.0"
---

# LocalSetup Doctor Repair

Use this skill when a repo has legacy, partial, or suspicious LocalSetup install state and the user wants a conservative repair path.

## Workflow

1. Run a dry report first:

```bash
localsetup doctor repair --target-directory <repo>
```

2. Inspect the JSON before applying:

- `decisions[]`: unresolved human choices. Do not apply while this list is non-empty.
- `actions[]`: paths that would be backed up, removed, installed, or verified.
- `detected_shape`: lockfiles, adapter paths, stale `ls/`, protected source-root status, legacy global roots, and partial adapters.
- `inferred`: platforms, attach mode, repo packages, and global package root.
- `blockers[]` and `warnings[]`: hard stops and caution notes.

3. Apply only when there are no unresolved decisions:

```bash
localsetup doctor repair --target-directory <repo> --yes
```

4. Verify after apply:

```bash
localsetup verify --target-directory <repo> --level filesystem
localsetup doctor --target-directory <repo>
```

## Decision Rules

- Preserve repo-owned content. If an adapter directory contains unknown files, stop and ask the user where that content belongs.
- Treat regular files at adapter destinations and unsupported filesystem nodes as manual decisions.
- Do not delete `ls/` unless it looks like copied LocalSetup framework source and the active source root is elsewhere.
- Treat LocalSetup maintainer/source checkouts as protected. If the target root contains source-root markers such as `ls/config/pack.yaml`, `ls/core/`, `VERSION`, and `pyproject.toml` or `install`, do not repair it as a consumer repo.
- Treat the registered LocalSetup shell source checkout as protected, regardless of where the user installed it. The default `~/.local/share/localsetup/source` location is only one possible managed source path.
- Do not remove, replace, or convert any protected source checkout's `ls/` tree through doctor repair.
- Prefer current scoped adapters such as `.codex/skills` over historical pre-Codex adapter roots.
- Preserve portable mode only when the current lock proves a portable deployment; otherwise use scoped symlink adapters.

## Reporting

In the final report, include:

- whether the run was dry-run or applied
- unresolved decisions, if any
- touched paths from `actions[]`
- backup/report path from `.localsetup/backups/repair-*`
- `verify.ok` and any verification issues

Do not claim repair completion unless the apply report and follow-up verification both pass.
