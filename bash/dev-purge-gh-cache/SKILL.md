---
name: dev-purge-gh-cache
description: "Purge GitHub Actions caches across every non-archived repo for one or more GitHub owners (users or orgs). Use when (1) the user says \"purge gh cache\", \"clear actions cache\", \"delete CI cache\", or invokes /dev-purge-gh-cache, (2) the user wants to free up GitHub Actions cache storage for an account/org, (3) the user names one or more GitHub owners (e.g. \"Takazudo\", \"zudolab\") and asks to wipe their Actions caches. Handles fan-out across all repos, parallel survey, bulk delete, and real-time verification."
allowed-tools: Bash
argument-hint: <owner> [owner...] [--survey-only]
---

# dev-purge-gh-cache

Wipe GitHub Actions caches across all of an owner's repos in one shot. GH Actions
caches are per-repo, so "purge for an account" means iterating every repo under
that owner. `scripts/purge-gh-cache.sh` does the whole survey → delete → verify
fan-out; this skill just drives it.

## Usage

Run the bundled script with the owner name(s) the user gave. Pass the absolute
path so the script can re-invoke itself for parallel workers:

```bash
bash $HOME/.claude/skills/dev-purge-gh-cache/scripts/purge-gh-cache.sh <owner1> [owner2 ...]
```

- Survey first without deleting anything: add `--survey-only` (or `-n`).
- Owners can be users **or** orgs; pass several to do them in one run.
- The script reports the scope (caches found, MB) before deleting, deletes via

  `gh cache delete --all`, then re-checks and prints `✅ ALL CLEAR` or the repos
  that still have caches.

If the user only named one owner, just run it for that one. If they asked to
"see what's there" rather than purge, use `--survey-only`.

## Requirements

- `gh` authenticated with `repo` + `workflow` scopes (the script preflights auth).
- `jq` available.

## Two gotchas baked into the script (don't re-learn them)

- **Verify with `gh cache list`, never the `actions/cache/usage` API.** That

  usage endpoint is GitHub's billing figure and is recomputed on a delay — it
  keeps reporting the old size/count for up to ~24h *after* caches are deleted,
  which falsely looks like the purge failed. The script verifies with the
  real-time `gh cache list` instead.

- **No `export -f` for xargs parallelism.** When the parent shell is zsh,

  exported bash functions don't survive into `xargs ... bash -c` subshells
  ("command not found"). The script parallelizes by re-invoking itself with an
  internal `__count` / `__delete` subcommand instead.

## Notes

- `gh cache delete --all` exits non-zero with "No caches to delete" on an

  empty repo — that's expected and the script ignores it.

- After a successful purge, the GitHub Storage usage figure in the UI/billing

  may still show the old size for up to ~24h; the caches themselves are gone
  (confirmed by the live verification step).
