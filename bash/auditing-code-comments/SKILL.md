---
name: auditing-code-comments
description: Audits comments in functions changed on a branch and agrees edits with the user. Use for comment review or the comment nudge.
argument-hint: "[base-ref, default: nearest parent branch, else configured upstream]"
allowed-tools: Bash(git config --get *), Bash(git symbolic-ref *), Bash(git rev-parse *), Bash(git diff *), Bash(git log *), Bash(git -c core.attributesFile=* diff *), Bash(git merge-base *), Bash(git for-each-ref *), Bash(git rev-list *), Bash(~/.claude/skills/auditing-code-comments/scripts/*)
---

# Auditing Code Comments

Configured upstream: !`git config --get --default unset auditing-code-comments.upstream`

## Setup — first use in a clone

Run this when the configured upstream above is `unset`.

1. Ask the user which branch their PRs usually merge into. Offer
   `git symbolic-ref --short refs/remotes/origin/HEAD` as the default.
2. Record it in the clone's local config (shared by all its worktrees):
   `git config auditing-code-comments.upstream <ref>`
3. Install the pre-commit nudge. `comment-nudge.sh` prints the comment lines
   added in the staged diff to stderr and never blocks. `--git-path` honors
   `core.hooksPath` and worktrees:

   ```bash
   H="$(git rev-parse --git-path hooks)/pre-commit"
   ```

   - No `$H`: `ln -s ~/.claude/skills/auditing-code-comments/scripts/comment-nudge.sh "$H"`
   - `$H` already resolves to `comment-nudge.sh`: nothing to do.
   - Some other hook: show it to the user and ask before appending a line that
     runs `~/.claude/skills/auditing-code-comments/scripts/comment-nudge.sh`.

## Step 1 — Find the fork point

```bash
SK=~/.claude/skills/auditing-code-comments
BASE=$($SK/scripts/branch-base.sh)        # or branch-base.sh <upstream>; skip if the user passed a base ref
git log --oneline $BASE..HEAD
```

`branch-base.sh` picks the nearest local branch below HEAD that isn't on the
configured upstream yet (the parent of a stacked PR), else the merge-base with
the upstream, and says which on stderr. If the log lists commits that aren't
this branch's work, ask the user for the base.

## Step 2 — Collect the functions and comments

Diff against the working tree (`git diff $BASE`, no `HEAD`) so uncommitted work counts.

```bash
git diff --stat $BASE
git diff -U0 $BASE | $SK/scripts/added-comments.py          # every added comment line, path:line
git -c core.attributesFile=$SK/assets/funcname.gitattributes diff -W $BASE -- <file>
```

`-W` prints each touched function whole, and the attributes file makes hunk
headers name the enclosing Python/C++ function. Read it file by file. Skip
generated files, goldens, lockfiles, and docs.

## Step 3 — Judge each touched function

If the repo has `.claude/rules/code_style.md`, read its Comments section; it
overrides this summary:

- Default to no comment.
- Keep contracts the signature can't show: units, ownership, thread-safety,
  error modes, side effects.
- Keep a non-obvious *why*: a constraint, a workaround, the bug a line prevents.
- Keep outward pointers: the spec implemented, the source of copied logic, the
  issue a fix closes, why deliberately unidiomatic code is right.
- Hypotheses, history, and broader rationale go in the PR description.
- No narration of straightforward code; a 1–2 line outline only when a readable
  body doesn't make the structure clear.
- A comment that needs a paragraph usually means naming or structure should change.
- Delete obvious header comments in touched code; no commented-out code.

Some comments signal that the code should change instead of the comment text:

| Comment | Fix in code |
|---|---|
| "keep in sync with X", "must match the order in Y" | encode the rule in data (`fold-knowledge-into-data`) |
| "X-specific" label on a block inside a generic loop | lifecycle hook (`lifecycle-hooks`) |
| shape/type contract, e.g. `# -> B,N,hidden` | assert or type it (`construct-or-inject`) |
| explains what an obscure name means | rename |
| a unit, e.g. `# in ms` | `_ms` suffix on the name |

Give every comment in a touched function — added or pre-existing — one verdict:
**keep**, **delete**, **rewrite**, **to PR description**, or **replace with code**.
Also flag the opposite gap: a touched function whose contract isn't visible from
its signature and has no comment gets a proposed **add**. Untouched functions
are out of scope.

## Step 4 — Discuss, then edit

Present one compact table per file, deletions and rewrites first:

| function | `file:line` | verdict | proposed text, or a one-clause reason |
|---|---|---|---|

Wait for the user's decisions; they will often reword. Apply only the agreed
changes with Edit. List anything moved out of the code under "For the PR
description" at the end, so cut rationale isn't lost.
