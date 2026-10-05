---
name: agents-md-screaming-architecture
description: "Create or update Codex instruction files (AGENTS.md / AGENTS.override.md and fallbacks like .agents.md) using “Screaming Architecture” style: each directory’s instructions quickly state purpose, boundaries, invariants, and exact validation commands. Use when asked to add/standardize agent instructions across a repo (root + key subdirectories), or when you need directory-scoped rules for tests/lint/docs/ownership."
---

# AGENTS.md “Screaming Architecture” Instructions

## Overview

Codex discovers instructions by walking from repo root → CWD, taking at most one file per directory (`AGENTS.override.md` first, then `AGENTS.md`, then configured fallback names like `.agents.md`). Keep instructions layered: broad rules at the root, narrow overrides close to the code they govern.

Files closer to your current directory win in practice because Codex concatenates instructions root → leaf; later directory guidance appears later in the merged prompt and overrides earlier guidance.

This skill helps you write instruction files that “scream” what each folder is for, what is safe to change, and how to validate it.

## Quick start

1. Choose the instructions filename (`AGENTS.md` vs `.agents.md`).
2. Enumerate target directories (root + “architecture boundaries”), excluding generated folders.
3. Write a root file with global guardrails + repo commands.
4. Add subdirectory files only where local context/rules differ or are easy to forget.
5. Validate: ensure files are non-empty, reasonably small, and commands are correct.

## Workflow

### 1) Choose the filename (discovery-aware)

- If the user explicitly asks for `.agents.md`, use `.agents.md`.
- If the repo already has `AGENTS.md` / `AGENTS.override.md`, prefer staying consistent.
- Otherwise, default to `AGENTS.md` (Codex reads it without extra config).
- If you choose `.agents.md`, remember: Codex only reads it if it’s listed in `project_doc_fallback_filenames` (Codex config).

### 2) Target only real architecture boundaries

- Include: repo root + key subtrees that represent a boundary (package/app/service, `scripts/`, `tests/`, `docs/`, infra, CI, etc.).
- Exclude: `.git/`, vendored deps (`node_modules/`, `.venv/`), caches (`__pycache__/`, `.pytest_cache/`), build output (`dist/`, `build/`), and other generated trees.
- Default depth: 1–2 levels. Go deeper only when a subtree has distinct rules.

Use the helper script to list candidate directories:

- `python3 scripts/list_instruction_dirs.py --root /path/to/repo`
- Add `--include-hidden` to include directories like `.github/` and `.circleci/`.

### 3) Write in “Screaming Architecture” style

For each targeted directory’s instructions file:

- **First 1–2 lines:** what this directory *is* and *why it exists*.
- **Then:** the rules that matter here (boundaries, invariants, “don’t touch” areas).
- **Then:** exact “fast check” commands (tests/lint/typecheck/build) for this directory.

Bias toward:

- Short bullets over paragraphs.
- Concrete commands over advice.
- Directory-specific deltas over repeating root guidance.

### 4) Keep layering tight (avoid duplication)

- Root file: global expectations (quality gates, dependency policy, standard commands, doc update rules).
- Subdir file: *only* what’s different/specific to that subtree.
- Use `AGENTS.override.md` only for “override, not additive” cases (temporary or truly different rules).

### 5) Validate

- Ensure files are **non-empty** (Codex ignores empty instruction files).
- Keep total instruction chain comfortably under the default size cap (32 KiB); split across nested directories if needed.
- Sanity check the commands you wrote (run the core fast check at least once when practical).

## Templates

- Root template: `references/root-template.md`
- Subdir template: `references/subdir-template.md`
- Targeting/ignore heuristics: `references/targeting.md`

## Resources

### scripts/

- `list_instruction_dirs.py`: Print a pruned, sorted list of candidate directories for instruction files.

### references/

- `root-template.md`: Fill-in template for a repo-root instructions file.
- `subdir-template.md`: Fill-in template for a directory-scoped instructions file.
- `targeting.md`: Heuristics for picking where to place instruction files (and where not to).
