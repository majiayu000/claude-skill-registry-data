---
name: skill-exporter
description: >
  Export a specific skill from ~/.claude/skills/ into a versioned git repository.
  Use when the user says "export skill X", "move skill to repo", "back up skill",
  "save skill to repo", "version this skill", "put skill in git",
  "export to agentfiles", or wants a locally-created skill tracked in git.
  Trigger even if the user just mentions wanting a skill versioned or shared
  across machines.
---

# Skill Exporter

Copy a skill from `~/.claude/skills/` into the `skills/` directory of a git repo, then replace the local copy with a symlink. The skill keeps working in Claude Code while the source of truth moves to version control.

## Find the target repo

1. Check if CWD is inside a git repo with a `skills/` directory at its root.
2. Search: `find ~ -maxdepth 4 -type d -name skills -path "*/.git/../skills" 2>/dev/null` — confirm with user.
3. If nothing found, ask the user for the path.

## Export

The user names the skill to export (e.g. "export my codex skill"). If the name is ambiguous, list real directories (not symlinks) in `~/.claude/skills/` to disambiguate — symlinks are already exported.

Then:

1. **Copy** `~/.claude/skills/<skill-name>/` to `$REPO/skills/<skill-name>/`.
   - If it already exists in the repo, show a diff (`diff -rq`) and ask: overwrite or skip?
2. **Verify** the copy succeeded — `$REPO/skills/<skill-name>/SKILL.md` must exist.
3. **Symlink back** — replace the local directory so the skill stays discoverable but lives in git:
   ```bash
   rm -rf ~/.claude/skills/<skill-name>
   ln -s $REPO/skills/<skill-name> ~/.claude/skills/<skill-name>
   ```
4. **Verify** the symlink resolves and SKILL.md is readable through it.
5. Remind the user to commit the new skill in the repo.
