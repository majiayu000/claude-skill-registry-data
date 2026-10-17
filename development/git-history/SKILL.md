---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: git-history
description: >
  Git archaeology: find why code changed, which commit introduced a line or bug,
  and read large diffs without truncation. Covers `git log --grep/-S/-G`,
  `git log -L` line and function history, `--follow` across renames, diff
  pagination, stale index.lock recovery, and reading the opencode session behind
  a commit via its `Session: ses_xxx` trailer. Load when debugging a regression,
  asking "why is this code like this", or reviewing a big branch diff.
---

# git-history

## Search commits

Use **all three**, passing variable names and function names as search terms:

```bash
git log --grep="search term"   # commit messages
git log -S "search term"       # commits that added or removed the string
git log -G "regex pattern"     # commits whose diff matches the regex
```

Add `--oneline` for a compact list, `-p` for diffs, `--all` to include other branches.

## Full history of a line or function

`git log -L` shows **every** commit that touched a line range. `git blame` only shows the last one. Git follows the line content through insertions, deletions, and moves above it.

```bash
git log -L 42,42:path/to/file.ts            # one line
git log -L 10,20:path/to/file.ts            # line range
git log -L :functionName:path/to/file.ts    # a function
git log -L 42,42:path/to/file.ts --oneline  # hashes and messages only
git show <hash>                             # read one commit in full
```

Use it to find the **goal** behind a change: find the commits, then read their messages and diffs.

## Full history of a file or folder

```bash
git log --oneline -- path/to/file.ts
git log --oneline --follow -- path/to/file.ts   # across renames (single file only)
git log --oneline -- src/components/
git log -p -- path/to/file.ts                   # with diffs
git log --stat -- path/to/file.ts               # with change stats
```

The `--` separator marks where paths begin, so git never confuses a filename with a branch name.

## Why a commit was made

My commits end with `Session: ses_xxx`. Read that session to get the full reasoning:

```bash
git log -1 --format=%B <hash> | rg 'Session: (ses_\w+)' -or '$1'
kimaki session read ses_xxx > ./tmp/session.md 2>/dev/null
```

## Paginating large diffs

Tools truncate long output. Page with `sed` in fixed windows with no overlap:

```bash
git diff $BASE_REF...HEAD -U20 -- ':!*.lock' | sed -n '1,500p'
git diff $BASE_REF...HEAD -U20 -- ':!*.lock' | sed -n '501,1000p'
```

Continue in 500-line steps until the output is empty. Start with `git diff --stat` to see which files matter.

## Stale index.lock

If an aborted git command leaves `.git/index.lock`:

1. Check no git or editor process is running: `pgrep -fl git`.
2. Only then remove the lock: `rm .git/index.lock`.
3. Retry non-interactively (`GIT_EDITOR=true git rebase --continue`).
