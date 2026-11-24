---
name: retrofit-from-public
description: 'Find changes made directly in the public repository (Senzing/bootcamp) since the last promotion and file them as GitHub issues in this development repository: a typo fixed in a pull request there, a page edited by hand, a dependency bump. Use when the maintainer wants to bring public-repository edits back to development, or before promoting when the plan shows a change this repository did not make. It writes nothing into either repository''s files. Maintainer tool — not part of the bootcamper experience.'
argument-hint: "[path to the public clone] (omit for ~/github.com/senzing/bootcamp) [--draft <run-dir> | --file <run-dir>]"
---

# Retrofit from the public repository

This is a **maintainer** tool, and the inverse of `/propagate-to-public`. Everything a
bootcamper installs is generated here, so an edit made directly in the public repository is
lost at the next promotion unless it is made here too. This skill finds those edits and files
each as an issue. It ⛔ **copies nothing**: the fix is implemented here, in `source/`, `hosts/`
or `site/`, so that it reaches every assistant and survives the next build.

## The public clone

With no argument, use the default checkout, `~/github.com/senzing/bootcamp`. An argument is the
path to the public repository's working tree: use it as `<public clone>` in every command below.

**Don't guess the source.** If the public repository isn't at the default path and none was
given, or the source does not exist, is not a git repo, or its `origin` is not
`Senzing/bootcamp`, ask rather than retrofitting from somewhere uncertain. The promotion plan
refuses each of these, and a guessed source files issues about an unrelated tree's content.

## How to find what changed

1. Read the version the public repository holds, from any package manifest in it, for example
   `plugins/claude/senzing-bootcamp/.claude-plugin/plugin.json`.
2. In a scratch worktree of this repository, check out the tag of that version:
   `git worktree add <scratch> <version>`.
3. From that worktree, plan a promotion against the public clone. It writes nothing:

   ```console
   python3 -m tools.bootcamp_build promote --to <public clone> --show 1000
   ```

4. Read the plan. The public repository was last written from exactly this tag, so:
   - **`change`** is a managed file edited in the public repository.
   - **`add`** is a managed file deleted there.
   - **`remove`** is a file added there inside a managed directory.
   - An empty plan means nothing was edited in the managed paths.
5. Remove the scratch worktree: `git worktree remove <scratch>`.

Files outside the managed paths (workflows, license, contribution files) belong to the public
repository and are not this skill's business.

## What to do with each change

⛔ **(INV-312) The output of this skill is GitHub issues, not a modified working tree.** It
compares and reports, and writes nothing into this repository's files.

1. **Read what changed and why.** For each change, read the public repository's history for
   the file (`git -C <public clone> log -p -- <path>`). Then decide where the same fix belongs
   here:

   | The edit is in | The fix belongs in |
   | --- | --- |
   | `plugins/<assistant>/senzing-bootcamp/skills/`, `scripts/`, `docs/` | `source/`, unless it is truly about one assistant |
   | A manifest, a catalog or a hook configuration | `hosts/<assistant>/host.json`, or the build |
   | `docs/` | `site/`, or `hosts/<assistant>/fragments/site-*.html` for an install page |
   | `README.md`, `assets/` | `public/` |

   ⛔ **An edit made to one assistant's package is checked against every assistant.** If the
   same defect exists in the others, say so in the issue: it was fixed for one assistant only
   because the public repository holds one copy per assistant.
2. **Group the changes into coherent issues**, one per thing a maintainer would decide about
   (a dependency bump, a prose correction, a page edited by hand), not one per file.
3. ⛔ **Search the tracker before filing each one.**

   ```bash
   gh issue list --state all --search "<the public commit subject or SHA>"
   ```

   A change already made here, or already filed, must not get a second issue. The tracker is
   the record; this skill keeps no ledger of its own, because a second list of the same fact
   is how two records come to disagree.
4. **(INV-314) Show the maintainer each title and body and get a yes**, or
   one yes for the whole list shown in one message (INV-314, 2026-10-13 note), under the
   conditions in `.claude/skills/feedback-to-issues/drafts.py` → "The batch yes", then file:

   ```bash
   gh issue create --title "<what diverged, not the symptom>" --body-file <file>
   ```

   ⛔ **Filing is outward-facing and immediate.** An issue can be edited or closed afterwards
   but never un-filed.

   ⛔ **(INV-318) Never apply the `unattended-ok` label to an issue this run files.** A
   divergence report that labels its own issues lets `/unattended-issue-loop` *(user level)*
   bring public-repository changes in with nobody deciding to. Choosing what runs unattended
   is the maintainer's decision alone.

   ⛔ **(INV-368) With `--draft <run-dir>`, this run files nothing, fixes nothing and sends
   nothing, and writes nothing outside `<run-dir>`.** Each issue becomes a
   [`drafts.py`](../feedback-to-issues/drafts.py) `add` record instead, and the run ends with
   `drafts.py list`. `--draft` is the release cycle's interface (#573), and the caller records
   unresolved drafts (INV-317). **With `--file <run-dir>`**, repeat step 3's search for each
   approved record, since the tracker may have changed, then file what `drafts.py file-plan`
   prints, after a yes for each record or one yes for the whole list shown in one message
   (INV-314, 2026-10-13 note), under the conditions in
   `.claude/skills/feedback-to-issues/drafts.py` → "The batch yes". Both stages, the manifest
   and its statuses are stated once in `drafts.py` (INV-300).
5. ⛔ **(INV-312) File in this repository only.** This skill never files anywhere but this
   repository's tracker, and never in the public repository.
6. Each issue body carries the **public commit** (subject and SHA), the paths affected there,
   and where the fix belongs here.
