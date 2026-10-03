---
name: project-cleanup-audit
description: Audit and safely clean local project repositories or workspaces with excessive generated files, old project residue, dirty Git status, stale worktrees, build caches, duplicate nested projects, confusing roots, or agent context/token waste. Use when the user asks to organize a repo, remove useless files, classify valid project files, clean untracked/deleted files, reduce disk usage, migrate from an old repo layout to a canonical project, or prepare a repository for future Codex/agent work.
---

# Project Cleanup Audit

## Operating Rules

Use this skill as an evidence-first cleanup workflow for local repositories. Prioritize preserving user work over reclaiming disk.

- Do not delete, reset, or overwrite until the target paths and rationale are explicit.
- If evidence is insufficient, provide only known facts, candidate hypotheses, validation paths, and temporary mitigations. Mark unverified conclusions clearly.
- Keep installed applications, user data directories, credentials, and system-wide caches out of scope unless the user explicitly includes them.
- Before structural cleanup, create a backup outside the workspace containing Git status, remotes, worktrees, patches, and copies of non-generated untracked files.
- Stop only development processes whose command line clearly points inside the workspace. Do not stop installed app processes just because the product name matches.
- Never run whole-repo `git clean -fdX` unless every ignored dry-run path has been classified as safe generated residue. If the dry-run includes datasets, release artifacts, local validation output, `.runtime`, `.codex`, `.codegraph`, or other agent context, delete only explicit pathspecs or resolved literal paths.
- Do not recursively print or quote sensitive local data directories while auditing. Prefer aggregate sizes, file counts, top-level names, and short non-sensitive samples.

## Quick Audit

Run the bundled read-only audit first when PowerShell is available:

```powershell
powershell -ExecutionPolicy Bypass -File "<skill>/scripts/audit_repo_cleanup.ps1" -Root . -Top 25
```

Use `-IncludeProcesses` when deletion is blocked by locked files or old dev servers:

```powershell
powershell -ExecutionPolicy Bypass -File "<skill>/scripts/audit_repo_cleanup.ps1" -Root . -Top 25 -IncludeProcesses
```

Use `-HashReleaseArtifacts` only when checking whether local release packages match already-published assets. This can be slow on GB-scale archives:

```powershell
powershell -ExecutionPolicy Bypass -File "<skill>/scripts/audit_repo_cleanup.ps1" -Root . -Top 25 -HashReleaseArtifacts
```

Read `references/classification.md` before classifying ambiguous files, local models, installers, datasets, dirty worktrees, or nested legacy projects.

When the audit reports `Review Required Ignored Paths`, treat those entries as a hard stop for whole-repo ignored cleanup. Classify them path by path before any delete.

## Workflow

1. Restate the cleanup target and boundaries.
   - Identify the intended canonical project, e.g. remote URL, default branch, active package manifest, app name, or repo root.
   - State explicitly what will not be touched, such as installed software, user profile data, or external archives.

2. Gather read-only facts.
   - Record `git rev-parse --show-toplevel`, branch, HEAD, remotes, `git status --short`, worktrees, and top-level sizes.
   - Compare the current root with the canonical upstream when relevant.
   - Use dry runs: `git clean -ndX` for ignored files and `git clean -nd` for untracked files.
   - Inspect the audit's `review_required_ignored_paths` before considering any ignored cleanup.
   - For release-heavy repositories, inspect `release_artifacts`. If available, compare package names, sizes, and SHA256 values against the release host before deleting versioned archives.
   - Inspect `local_context_paths` before deleting `.codex`, `.codegraph`, `.gstack`, `.venv`, `.pytest_cache`, or `__pycache__`.
   - Inspect `local_data_evidence_paths` by aggregate counts and extensions; do not recursively print sensitive document names or contents.
   - Inspect package/build manifests: `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `pom.xml`, `*.sln`, etc.

3. Classify paths.
   - `delete after confirmation`: ignored/rebuildable build outputs, dependency installs, logs, test browser profiles, diagnostics.
   - `backup/archive first`: untracked source, dirty worktrees, nested old projects, release packages not confirmed uploaded.
   - `keep`: source, manifests, lockfiles, CI, docs, migrations, public assets, test fixtures.
   - `needs explicit user confirmation`: local models, datasets, databases, installers, credentials, external user data.
   - For `build/`, classify tracked packaging configuration separately from ignored `build/work`, `build/runtime`, and generated metadata.

4. Back up before structural changes.
   - Save status/remotes/worktrees/logs to a backup directory outside the workspace.
   - Save `git diff --binary` patches for dirty tracked files.
   - Copy non-generated untracked files, excluding clearly rebuildable caches such as `node_modules`, `target`, `dist`, `.next`, and browser output.

5. Execute the smallest safe cleanup.
   - Prefer exact path deletion or `git clean -fdX -- <pathspec...>` for ignored generated files after reviewing `git clean -ndX`.
   - Use whole-repo `git clean -fdX` only when the ignored dry-run has no review-required paths and all entries are safe generated residue.
   - Use `git worktree remove` for registered worktrees; do not raw-delete registered worktrees first.
   - Use native shell deletion with literal paths and resolved workspace-bound checks.
   - On Windows, verify resolved absolute paths stay inside the workspace before recursive deletion.

6. Handle canonical root migration only after backup.
   - If the current directory is an old repo shell and the real product repo is another remote/branch/layout, switch or clone to the canonical root only after preserving dirty work.
   - Do not force-delete unmerged local branches unless the user explicitly accepts losing that history.
   - Prune stale remote refs and tags only after the remote is correct.

7. Verify.
   - Show final `git status`, branch/upstream, remotes, worktrees, top-level tree, and disk usage.
   - Run a minimal dependency or build dry-run when reasonable, e.g. `npm ci --dry-run --ignore-scripts`.
   - Report any remaining locked or intentionally retained residue with reason and size.

## Output Format

When reporting results, keep the distinction clear:

- Known facts
- Cleanup actions taken
- Backups created
- Remaining risks or unverified assumptions
- Recommended next action

Never present a destructive cleanup as "fixed" if only an audit was completed.
