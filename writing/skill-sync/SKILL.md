---
name: skill-sync
description: Use when installing, copying, or checking local skills across agent harnesses. Treat ~/.agents/skills as the source of truth, sync selected skill directories to the target loader, and verify SKILL.md is discoverable.
version: 1.0.0
license: MIT
metadata:
  package: local-operator-skills
  category: skill-engineering
  author: Admin
  triggers:
    - sync skills
    - install skills to claude
    - copy skills
    - skill not loading
    - propagate skill
---
# Skill Sync

## Purpose

Keep a skill in every harness that should load it, without turning global instruction files into catalogs.

Canonical root: `C:\Users\Admin\.agents\skills\<name>\`.

## Workflow

1. **Name the source and targets.** Default source is `~/.agents/skills/<name>`. Default targets come from [references/harness-map.md](references/harness-map.md). Add a harness only when that agent actually scans the destination.
   - Done when each destination path is known to exist or is created deliberately.
2. **Copy the skill directory, not a snippet.** Sync `SKILL.md` plus `references/`, `scripts/`, `templates/`, and `assets/` when present. Do not flatten or rename files.
   - Done when destination file names match the source tree.
3. **Verify byte-level identity for the synced set.** Compare `SKILL.md` and referenced files. A description-only stub is a failed sync.
   - Done when source and destination hashes match for every synced file.
4. **Confirm loader visibility.** Check that the destination is a scanned skills root for that harness. Do not edit `AGENTS.md` just to list the skill.
   - Done when a fresh session of that harness can resolve the skill by name or trigger.

## Rules

- One-way by default: agents → selected harnesses. Reverse-sync only when the operator edited the copy on purpose.
- Sync named skills, not the entire 200+ pack, unless the operator asked for a full mirror.
- Prefer updating an existing destination directory in place over creating a second spelling of the same skill.
- Leave archived or harness-specific skills untouched.

## Completion Gate

- [ ] Source `SKILL.md` exists and parses.
- [ ] Every requested target has an identical tree for the synced files.
- [ ] Broken relative links were not introduced by a partial copy.
- [ ] The reply lists source, targets, and file counts or hashes.

## Common Failure Modes

- **Index duplication:** pasting the skill name into multiple `AGENTS.md` files instead of copying the skill tree.
- **Stub sync:** copying `SKILL.md` and omitting `references/`.
- **Wrong root:** writing into a home directory the harness does not scan.
- **Bidirectional drift:** editing both copies independently.
