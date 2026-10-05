---
name: sync-claude
description: Sync the live ~/.claude global config (settings.json, CLAUDE.md, statusline.ts, own skills, skills.sh lock file) into this git backup repo, then commit. Allowlist-based so credentials, history, and project transcripts are never copied. Use when the user says "sync my claude config", "back up .claude", "update the .claude repo", or runs "/sync-claude".
---

# Sync Claude config to git

Backs up the user's live global Claude Code config (`~/.claude`) into this repo.
This is a project skill of the backup repo, it is not installed globally.

## What it touches

Only these paths are ever read (the allowlist lives in `sync.ts`):

- `~/.claude/settings.json`, `CLAUDE.md`, `statusline.ts`
- `~/.claude/skills/*` that are NOT listed in the skills.sh lock file. These are
  the user's own skills and are mirrored into `skills/<name>/`.
- `~/.agents/.skill-lock.json`, the manifest the skills.sh CLI keeps for skills
  it installed into `~/.agents/skills` and symlinked into `~/.claude/skills`.
  Copied to `.agents/.skill-lock.json`. Those skills are never vendored here;
  `install-skills.ts` reinstalls them from the lock on a new machine.

Everything else in `~/.claude` (`.credentials.json`, `history.jsonl`, `projects/`,
`sessions/`, `todos/`, `tasks/`, ...) is never read. That allowlist is the primary
defense against leaking secrets. A value-shaped secret scan on the copied content
is a second safety net: if a key or token ever appears inside an allowlisted file,
that file (or that whole skill) is skipped.

## Steps

1. From the repo root, show what would change (copies nothing):

   ```
   bun .claude/skills/sync-claude/sync.ts
   ```

   `orphan` lines are skill folders in the repo that are not live own skills.
   A skill "managed by skills.sh" got vendored by mistake: delete it from
   `skills/`. A skill "not in ~/.claude/skills" was removed live: delete it, or
   copy it back to `~/.claude/skills/` if the removal was an accident.

2. Apply the copy:

   ```
   bun .claude/skills/sync-claude/sync.ts --apply
   ```

   If it exits non-zero, a possible secret was detected. Stop, show the user the
   flagged line, and do not commit.

3. Review and commit on `main` (this repo commits directly to main, no PR):

   ```
   git status
   git diff
   git add -A settings.json CLAUDE.md statusline.ts skills .agents
   git commit -m "chore: sync live .claude config"
   ```

   Do not push unless the user asks.

## Restoring skills.sh skills

```
bun .claude/skills/sync-claude/install-skills.ts --list   # print the commands
bun .claude/skills/sync-claude/install-skills.ts          # run them
```

One `bunx skills add <source> -g -y -a claude-code -s <names>` per source repo.

## Notes

- Line endings are normalized to LF on copy, so CRLF/LF differences never show up
  as spurious changes.
- `statusline.ts` is the source. The live status line runs the compiled
  `statusline` binary, which is large and not tracked.
- To add another top-level file to the backup, add its name to `FILES` in
  `sync.ts` (and make sure it never contains secrets).
