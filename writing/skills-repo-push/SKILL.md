---
name: skills-repo-push
description: >
  Synchronizes Claude skills from the skills repo (github.com/Theycallmeholla/skills) to
  the local ~/.claude/skills directory, ensuring local skills match the repo's latest
  versions. Compares each skill to detect new or changed content, creates a tarball for
  manual Claude app upload, and preserves local-only skills that aren't in the repo. Use
  when the user says "push skills out", "sync repo to local", "update my local skills from the
  repo", "distribute skills", "my local skills are stale", "refresh skills from github",
  or after pulling updates from the skills repo. Runs in dry-run mode by default to preview
  changes before applying them with --apply.
---

# Skills Repo Push

Updates local Claude skills at `~/.claude/skills` from the skills repo
(`github.com/Theycallmeholla/skills`, local clone: `/Users/cursivemedia/skills`), treating
the repo as the source of truth.

## Direction

**Repo → Local** — opposite of `skills-repo-sync` which goes local → repo.

## What it does

1. **Scans** the repo's `skills/` directory for all skill folders.
2. **Compares** each repo skill against `~/.claude/skills`:
   - NEW: skill exists in repo but not locally
   - CHANGED: skill exists in both but content differs
   - IDENTICAL: skill matches exactly (skipped)
3. **Preserves** local-only skills — never deletes or modifies skills that exist only
   locally (e.g., adapt, polish, typeset, harden).
4. **Reports** what would change with file counts and diff sizes.
5. **Applies** changes only with `--apply` flag (dry-run by default).
6. **Packages** NEW+CHANGED skills into `/tmp/skills-push-TIMESTAMP.tar.gz` for manual
   Claude app upload.

## Usage

```bash
# Dry run — see what would change
scripts/push.sh

# Apply changes to local skills
scripts/push.sh --apply

# Limit to specific skills
scripts/push.sh --apply skill1 skill2

# Custom paths via environment
REPO_DIR=/path/to/repo LOCAL_DIR=/path/to/local scripts/push.sh
```

## Safety

- **Dry-run by default** — requires explicit `--apply` to write.
- **Never deletes** — local-only skills are left completely alone.
- **Protects local state** — some files accumulate real user data locally while the repo
  carries only a blank template. `blog-topic-interview/references/opinion-bank.md` is the live example: locally
  it holds the author's actual positions, in the repo it is placeholders. Overwriting it is
  silent data loss. Files matching `PRESERVE_GLOBS` are stashed before the update and
  restored on top of the fresh copy. Dry-run prints every file it will keep.
- **Backs up before writing** — each replaced skill folder is copied to
  `/tmp/skills-push-backup-<timestamp>/` before anything is removed.
- **Shows diffs** — see exactly what changes before applying.

Add a pattern to `PRESERVE_GLOBS` whenever a skill starts writing state into its own folder.
The default list is `references/opinion-bank.md references/*-bank.md state.json`.

## Output

Dry-run mode shows:
- Count of NEW, CHANGED, IDENTICAL skills
- Per-skill change summary with file/line counts
- Tarball path for manual app upload
- Exact command to apply changes

Apply mode additionally:
- Copies NEW skills to local
- Updates CHANGED skills in place
- Reports final sync status

## Environment

- `REPO_DIR`: Skills repo path (default: `/Users/cursivemedia/skills`)
- `LOCAL_DIR`: Local skills path (default: `~/.claude/skills`)

## Notes

- Compares only `SKILL.md` and subdirectory contents; ignores hidden files.
- Tarball includes only NEW+CHANGED skills for efficient app upload.
- Run after `git pull` in the repo to distribute updates locally.
- Claude app upload remains manual — extract tarball and upload through UI.
