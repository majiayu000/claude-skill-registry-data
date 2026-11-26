---
name: tidying
description: >-
  Finds junk files (backups, temp, stray notes) and removes them reversibly after your ok. Use when the user asks to clean up the project, remove leftovers, or says the repo is messy. Not for refactoring code.
license: Apache-2.0
metadata:
  level: "setup"
  uses: ""
  agents: ""
  tokens: "783"
---

Finds unneeded files, shows a manifest, and removes only what the user approves, in a way that can be undone. Report first, nothing changes before the ok.

## Steps
1. Read the CLAUDE.md contract (`## Where things live`: Docs, Plans, Scratch, Trash). Not a git repo: say so and stop (nothing is recoverable). `$ARGUMENTS` only narrows the path.
2. Detect without reading file contents: `git status --short -uall`, `git ls-files --others --exclude-standard`, `git ls-files --others --ignored --exclude-standard --directory`, `find` for zero-byte files and empty dirs (skip `.git`, `node_modules`, venvs, build output).
3. Sort every candidate into a tier. **T1** safe to remove: OS junk, backup and merge leftovers, Claude temp, zero-byte strays, empty dirs. **T2** needs a look: untracked scratch or debug scripts, `.md` outside the docs home, logs, screenshots, large untracked files, finished plans (archived, never deleted). **T3** never touched: `.env*`, keys, data, assets, untracked source that matches no T1 pattern, `.git`, nested repos.
4. A T2 item is only listed when it has a second signal: no `grep -r` reference to its name and not modified for 30 days (`find <path> -mtime +30`). A detector (knip, vulture, cargo-machete) counts as one signal only if the project already has it; never install one.
5. Show the manifest, grouped by tier and by kind: path, size, tracked or untracked, why. Show T3 as a count only. Compact: more than 30 items per group → counts plus the first 10 and the path of the full list in `.scratch/tidy.md`.
6. Ask per group (T1 groups first; T2 one item at a time unless the user takes the group). Remove only approved groups.
   - Tracked: `git rm` (history keeps it).
   - Untracked: `mv` into `.trash/<YYYYMMDD-HHMMSS>/` keeping the relative path, and append `path<TAB>git HEAD sha` to `.trash/<stamp>/MANIFEST`.
   - Finished plans: move to `docs/plans/archive/`.
7. Verify: re-run the detection for removed paths, confirm each is gone and each trashed file is in `.trash/`; if the project has a test command, run it once. Report what was undone-able how.
8. Prevention: a junk kind seen twice, or a missing `.gitignore` entry for `.trash/` and `.scratch/`: propose the pattern; edit `.gitignore` only after its own ok. Bigger rules go to `/foma-skills:learning`.

## Rules
- Never `rm -rf`, `git clean`, `find -delete` or any delete that git or `.trash/` cannot restore.
- Never touch T3, a path outside the project, or anything you were not shown and approved.
- A file is not junk because its name looks odd: unclear means T2, never T1.
- Empty `.trash/` only when the user asks, and name what it holds first.
- Not a decision of yours: tracked source, tests and docs. Unused code is a finding for `/foma-skills:refactoring`, not a removal here.

If you sort candidates into tiers (step 3), read `references/tiers.md` for the patterns.

## Report
- Per group: found, removed, left (and why); trash folder.
- Undo: `mv` back from `.trash/<stamp>/` (MANIFEST has the paths), `git restore` for tracked.
- Not checked: <...>

Next: `/foma-skills:learning` if a junk kind keeps coming back.
