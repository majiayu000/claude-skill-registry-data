---
name: agent-compat-sync
description: Keep repository-level Claude and Codex agent instructions compatible by creating safe symlinks between CLAUDE.md and AGENTS.md, and between .claude/skills/* and .agents/skills/*. Use when a repository should work with both Claude and Codex, when one agent instruction file exists but the other is missing, when migrating agent skills between .claude and .agents directories, or when asked to improve Claude/Codex compatibility for a repo.
---

# Agent Compat Sync

Make a repository usable by both Claude and Codex without duplicating instruction files or skill folders. Prefer symlinks so one canonical source stays authoritative.

## Workflow

1. Inspect the repository root for `CLAUDE.md`, `AGENTS.md`, `.claude/skills`, and `.agents/skills`.
2. Choose the canonical side:
   - If `CLAUDE.md` exists and `AGENTS.md` is missing, treat Claude as canonical.
   - If `AGENTS.md` exists and `CLAUDE.md` is missing, treat Codex as canonical.
   - If one instruction file is already a symlink to the other, treat the real target side as canonical.
   - If both instruction files exist as independent real files, stop and ask the user which file should become canonical.
3. Create the missing instruction-file symlink:
   - Claude canonical: `AGENTS.md -> CLAUDE.md`
   - Codex canonical: `CLAUDE.md -> AGENTS.md`
4. Mirror skill entries with per-entry symlinks:
   - Claude canonical: create `.agents/skills/<name> -> ../../.claude/skills/<name>` for each item in `.claude/skills`.
   - Codex canonical: create `.claude/skills/<name> -> ../../.agents/skills/<name>` for each item in `.agents/skills`.
5. Treat an existing path as acceptable when it already resolves to the same real target, even if the symlink is on a parent directory or points in the reverse direction.
6. Never overwrite existing real files or directories without explicit user approval. Report conflicts with exact paths.

## Scripted Sync

Use the bundled script for normal execution:

```bash
python3 scripts/sync_compat.py --repo /path/to/repo
```

From the target repository root, this is also valid:

```bash
python3 /path/to/agent-compat-sync/scripts/sync_compat.py
```

Useful options:

- `--dry-run`: show planned changes without writing.
- `--repo PATH`: run against a repository other than the current working directory.

The script is intentionally conservative. It creates missing symlinks and directories, leaves correct or equivalent symlinks alone, and exits non-zero when it finds ambiguous or conflicting existing paths.

## Manual Fallback

If the script cannot be used, apply the same rules manually with relative symlinks.

Claude canonical:

```bash
ln -s CLAUDE.md AGENTS.md
mkdir -p .agents/skills
ln -s ../../.claude/skills/<skill-name> .agents/skills/<skill-name>
```

Codex canonical:

```bash
ln -s AGENTS.md CLAUDE.md
mkdir -p .claude/skills
ln -s ../../.agents/skills/<skill-name> .claude/skills/<skill-name>
```

Before creating any symlink manually, check whether the destination already exists. If it exists and is not already the expected symlink, stop and ask the user.
