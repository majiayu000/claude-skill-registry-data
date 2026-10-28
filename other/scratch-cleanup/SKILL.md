---
name: scratch-cleanup
description: "Sweep a dusty .scratch/: file research into docs/, remove finished efforts, and report the work still open."
disable-model-invocation: true
argument-hint: "Days of inactivity before open work counts as stale (default 30)"
---

# Scratch Cleanup

`.scratch/` is an inbox, not an archive. Everything in it ends one of three ways: **filed** (research that belongs in `docs/`), **removed** (an effort whose work is all done), or **kept** (work still open, listed in the report). Nothing changes on disk until the user approves the plan.

The stale threshold is `$ARGUMENTS` days; 30 when empty.

## 1. Inventory

Read the tracker layout from `.agents/issue-tracker.md` (fallback `docs/agents/issue-tracker.md`, then `setup/issue-tracker.md` in this collection) and the status vocabulary from the matching `triage-labels.md`. Then walk `.scratch/` and put every file in exactly one bucket:

- **Effort**: a `.scratch/<slug>/` directory holding a map, spec, decisions, tickets, or triage request files. Older efforts may use an `issues/` folder instead of `tickets/`; treat it as tickets.
- **Research**: findings files, by default under `.scratch/research/`, or any file whose body is a cited findings report ending in **What this unblocks**.
- **Unclassified**: everything else (wizards, loose notes, questionnaires outside an effort). `.DS_Store` files are junk: they go in the plan as deletions with no question.

For every file, record whether git tracks it (`git ls-files --error-unmatch <path>`) and its last change date (`git log -1 --format=%cs -- <path>`, or the file mtime when untracked).

Done when every file under `.scratch/` has a bucket, a tracked/untracked flag, and a date.

## 2. Judge each effort

Read each file's status in either dialect: the YAML frontmatter `status:` field, or a legacy `**Status:**` / `Status:` line near the top of the body. A file is **done** when its status is `closed` or the wontfix role string. An effort is **done** only when all three hold:

1. Every file in it is done: the map, every decision ticket, the spec, every build ticket, every triage file.
2. Every commit a ticket cites (a 7–40 character hex SHA in its status line, `## Resolution`, or `## Comments`) exists on the default branch: `git merge-base --is-ancestor <sha> <default-branch>`. The default branch is `git symbolic-ref --short refs/remotes/origin/HEAD` without the remote prefix, else `main`. A cited commit that is not an ancestor still counts as on the default branch when the work arrived by squash-merge or rebase, so check equivalence before calling it missing: a merged PR contains it (`gh api repos/{owner}/{repo}/commits/<sha>/pulls --jq '.[] | select(.merged_at) | .number'`), `git cherry <default-branch> <sha> <sha>~1` prints it with `-` (an equivalent patch is on the branch), or a commit on the default branch has the same subject (`git log <default-branch> --fixed-strings --grep="$(git log -1 --format=%s <sha>)" -1`). A SHA git cannot resolve at all is checked by the PR route only. Only a commit that fails every check is missing.
3. Nothing in the effort contradicts itself: for example, a spec still `ready-for-agent` while every ticket is closed, or a closed ticket whose commit is missing.

An effort that fails rule 3, or has a file with no readable status, is **mismatched**: it goes in the plan as a question, never a removal. An effort with any open file is **open**. An open effort is also **stale** when its newest file is older than the threshold; clear any `claimed-by` in a stale effort (the claim's session is gone) and leave its status alone.

Done when every effort is labelled done, mismatched, or open (with stale marked).

## 3. Plan

Build the plan for every bucket:

- **Research**: pick a destination under `docs/`. Match an existing topic folder (`docs/<topic>/`) when one fits the subject; otherwise use `docs/research/<same-filename>`. When two folders fit, or none fits and the subject clearly belongs to a topic that does not exist yet, list the choice as a question. Find every inbound link (`rg -n --fixed-strings '<old path>'` across the repo, `.scratch/` included) so the move can rewrite each one.
- **Done effort**: read its spec, map, and closed decision tickets for **lasting decisions**: choices that are hard to reverse, still true in the code today, and whose reasons live nowhere else. List each as a one-line ADR candidate. Then list the effort for removal.
- **Mismatched effort**: state the contradiction in one line and what would settle it.
- **Unclassified**: one line per file saying what it looks like and a proposed fate (file, remove, or keep).

Show the plan in one message, with these sections in order: **File** (research moves and link rewrites), **ADR candidates** (numbered, so the user can pick by number), **Remove** (committed paths), **Remove: cannot recover** (untracked paths, with a note that git holds no copy), **Questions** (mismatched efforts, unclear destinations, unclassified files), and **Keep** (the report table from step 5). Ask for approval with `AskUserQuestion` where available, otherwise in chat. The untracked removals need their own explicit yes, separate from the rest of the plan.

Done when the user has approved, trimmed, or rejected each section, and has answered every question.

## 4. Apply

Apply only what the user approved, in this order:

1. **ADRs first**, while the source files still exist: write each picked candidate as an ADR through the `domain-modeling` skill's format and location (`docs/adr/` in a single-context repo).
2. **File research**: `git mv` for tracked files, `mv` for untracked ones, creating `docs/` folders as needed. Rewrite every inbound link found in step 3 to the new path.
3. **Remove**: `git rm -r -- <path>` for committed efforts and files; `rm` for approved untracked ones and `.DS_Store`.
4. **Release stale claims** found in step 2.
5. **Stage** every changed path by explicit path (`git add -- <path> …`); leave the commit to the user.

Done when `rg -n --fixed-strings` finds no reference to any moved or removed path, and `git status --short` shows only the approved changes.

## 5. Report

End with the table of everything that stayed in `.scratch/`, one row per effort or kept file:

| Effort | Open work | Blocked by | Last change | Stale | Next |
|---|---|---|---|---|---|
| `.scratch/<slug>/` | open ticket or decision files, by number | open blockers, or the question the user left open | date | yes/no | the skill that moves it forward (`/implement <ticket>`, `/wayfinder <map>`, `/to-tickets <spec>`) |

Under the table, give one line each for: files filed (old → new path), ADRs written, paths removed, claims released. Then suggest `/commit` for the staged changes.
