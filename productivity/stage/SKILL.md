---
name: stage
description: Use when committing work from the current session to stage ONLY hunks the session touched, not the entire file. Prevents accidentally staging unrelated uncommitted changes from other work.
metadata:
  website: "https://photostructure.com/coding/clean-commits/#stage"
---

# Stage Session Changes

> More on these workflows: [photostructure.com/coding](https://photostructure.com/coding/) (no dedicated `stage` article yet)

Stage ONLY the changes that belong to the current body of work and compose a Conventional Commit message.

## User direction

User instructions take precedence over this skill's workflow defaults. A direct
instruction such as "commit", "approved, commit", or "commit these changes"
authorizes the commit for the understood scope. Use the supplied message or
compose one; the user need not approve its exact wording separately.

Unless the user also requests a review first, verify the staged scope and commit
without starting or resuming a review, requiring a reviewer verdict, or asking
for approval again. Loading this skill does not reopen settled decisions about
scope, grouping, or review. Preserve unrelated changes and follow the
repository's Git history safeguards. Ask for clarification only when the commit
scope cannot be determined from the conversation and repository state.

When project instructions require review before every commit, a commit
instruction for changes that review has not finished on since they last
changed runs the review first, and only an explicit instruction to skip review
skips it.

If, after checking the current git status, you find that all of your changes have been committed already, tell the user that: this skill is done.

**NEVER `git add` an entire modified file unless every hunk in its diff belongs to this work.**

Interactive staging may be unavailable. This skill includes
[`scripts/stage_hunks.py`](./scripts/stage_hunks.py) for deterministic,
non-interactive partial staging on Windows and POSIX hosts.

## One concern per commit

When preparing a commit proposal, propose **separate commits** for distinct
concerns unless the user has already specified or approved their grouping.

Signs the session's work should be split:

- Changes span unrelated features, bugs, or subsystems (e.g. a CSS tweak + an unrelated backend fix)
- You'd need "and" in the commit subject to describe it (`fix X and refactor Y`)
- The commit message would exceed 10 lines to explain everything
- Some changes are refactors/cleanup while others are behavior changes
- Tests for feature A are mixed with implementation of feature B

When splitting, run the procedure below **once per commit**: inventory just that concern's files, stage them, compose a focused message, and commit if authorized — then move on to the next concern. Approval covering several commits applies to all of them; do not ask again per commit. Do NOT stage everything at once and try to describe it in a single message.

These grouping rules guide proposals before approval. Honor a grouping the user
has already specified or approved; do not reopen it after a commit instruction.

## Gather live context

Run these commands at invocation time; never rely on embedded or previously
captured output:

```text
git status --short
git diff --cached --stat
git log -5 --format='%h %B'
```

## Procedure

### 1. Inventory Changes to Stage

Review the conversation and operation history. Collect:

- each changed file and the exact before/after content attributable to this
  body of work;
- new files created for this work;
- files deleted for this work.

Files you only inspected are not session changes. Do not stage them.

If the session is working from a plan or task document, its scope may extend beyond this conversation — prior work may have left related uncommitted changes. In that case, read the plan, and for each uncommitted file in `git status` decide whether it belongs to the same body of work; **ask the user** when unsure. Stage the plan/task file itself if it was updated this session.

### 2. Classify Each File

For each file you changed, run `git diff -- <file>` and compare every hunk with
the recorded changes from this body of work.

| Situation                                 | Action                 |
| ----------------------------------------- | ---------------------- |
| **New file** (`??` in status)             | `git add <file>` only if the whole file belongs to this work |
| **Deleted file**                          | `git rm <file>`        |
| **ALL hunks are yours**                   | `git add <file>`       |
| **SOME hunks are yours** (mixed)          | Partial-stage (step 3) |
| **NO hunks are yours**                    | Do not stage           |

### 3. Partial-stage mixed files

Resolve the bundled helper relative to this skill directory and use the host's
Python 3 launcher. It reads one tracked file's unstaged diff, numbers its hunks,
and passes only explicitly selected hunks to `git apply --cached`; it does not
create a fixed-path temporary file or modify the working tree.

First list the hunks:

```text
python3 scripts/stage_hunks.py path/to/file --list
```

Map each numbered hunk back to the recorded changes for this work. Then stage
only the matching hunk numbers:

```text
python3 scripts/stage_hunks.py path/to/file --include 1,3
```

On Windows, `py -3` is a common equivalent; otherwise use the host's documented
Python 3 launcher. Review the helper's displayed hunk summaries before
applying.

The helper refuses broadened path selections and file-level mode, rename,
copy, creation, or deletion metadata. Attribute and stage those changes
separately before selecting content hunks.

The helper generates its own canonical diff and ignores the repository's diff
configuration (color, prefixes, relative paths, textconv, context, and
inter-hunk context). Always number hunks from `--list` rather than from a plain
`git diff`: a repository that sets `diff.interHunkContext` will merge adjacent
hunks in `git diff` output, so the two numberings can disagree.

If one Git hunk mixes related and unrelated lines, **do not stage that hunk or
the whole file**. Stop and ask the user how to split or attribute the entangled
change. Preserving unrelated work is more important than forcing a commit.

### 4. Verify

```bash
git diff --cached --stat
git diff --cached
```

Every newly staged line must trace to this body of work. Also compare against
the staged diff that existed before this workflow so pre-existing staged work is
not mistaken for yours. If anything is uncertain, stop before committing and
ask the user; never clear or replace someone else's staged changes wholesale.

### 5. Compose Commit Message

Draft a [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) message from the staged diff.

#### Format

```
<type>[(<scope>)][!]: <description>

[problem and rationale; omit only if clear from subject]

[optional footer(s)]
```

#### Spec summary

- **Type** (REQUIRED): a noun prefix. `feat` = new feature, `fix` = bug fix. Other common types: `refactor`, `perf`, `test`, `docs`, `style`, `build`, `ci`, `chore`.
- **Scope** (optional): a noun in parentheses after the type describing the section of the codebase, e.g. `fix(parser):`. Use the most significantly changed filename (no extension/path).
- **`!`** (optional): append immediately before `:` to flag a breaking change, e.g. `feat!:` or `feat(api)!:`.
- **Description** (REQUIRED): a concrete, imperative subject. Avoid task-status summaries such as "finish cleanup".
- **Body**: for nontrivial changes, explain the problem and why this fix in a short paragraph. Omit only when the subject conveys the rationale.
- **Footer(s)** (optional): one blank line after body. Format: `token: value` or `token #value`. A `BREAKING CHANGE:` footer (uppercase) is synonymous with `!` in the type prefix.

#### Trailers (attribution + references)

Add git trailers whenever the conversation provides the data, so credit and links aren't lost:

- `Reported-by: <name>` — a third party reported it: a user, customer, forum poster, or issue filer
- `Link: <url>` — a thread, issue, or message that gives context (no auto-close)
- `Refs: <#NNN | url>` — related issue you do **not** want to auto-close
- `Closes: #NNN` / `Fixes: #NNN` — a GitHub issue to auto-close on merge
- `Fixes: <12-char-sha> ("subject")` — the bug-introducing commit (Linux-kernel form)

`Reported-by` credits someone **outside** the work. Never name the repo owner, the person you are working with, or yourself — a maintainer finding a bug in their own project is not a bug report, and the commit's authorship already records who wrote the fix. When nobody outside reported it, omit the trailer.

Repeat a trailer for multiple values (one per line) — never `Reported-by: a, b`. Prefer `git commit --trailer "Reported-by=name" --trailer "Link=https://..."` (git ≥2.32) so formatting stays canonical.

#### Constraints

- Keep the message under 10 lines (subject + blank + body + footers) unless the
  user supplies or approves a longer message.
- If a draft needs more space, shorten it or propose splitting by topic before
  approval. Do not reopen approved scope or grouping to meet the line limit.
- Match the style of the recent commits gathered above. Check that the complete proposal explains why.

**NEVER include**: Co-Authored-By trailers, AI attribution, line-by-line enumeration.

### 6. Commit When Authorized

If the user has already instructed you to commit or approved the proposed
commit, proceed without another approval request. If the user only asked to
stage changes or prepare a proposal, show the staged diff summary and proposed
message, then wait for commit authorization.

Pass the message to `git commit` using the host's normal non-interactive argument
or message-file mechanism; do not use shell substitution.

After verifying the staged diff contains exactly the intended commit, use plain
`git commit`. Do not use `git commit --only -- <paths>` after partial staging:
`--only` commits the named paths' working-tree content instead of their staged
content, so filtered-out hunks return under a message that does not describe
them.

`--only` is still right for what it was meant for: committing one whole file's
working-tree content without disturbing a shared index you never filtered. It
is wrong the moment you have partial-staged anything.

Confirm what you are about to commit, not what you staged some minutes ago:

```bash
git diff --cached --stat        # scope
git log -1 --format='%h %s'     # still your commit at the tip?
```

The second matters before any `--amend`: if another session committed while you
were composing, `--amend` rewrites *their* commit. Then the fix is a follow-up
commit or a revert, never an amend.

## STOP — Red Flags

- About to `git add .` or `git add -A` or `git add --all` — **STOP**
- About to `git add <file>` on a file with mixed changes — **STOP**, partial-stage
- Staged diff has lines you cannot trace to this work — **STOP** and preserve
  the user's existing index state
- About to `git commit --only` after partial-staging — **STOP**, it commits the
  working tree and discards everything you staged
- About to `git commit --amend` — **STOP** and check `git log -1` first; if the
  tip is no longer your commit you would rewrite someone else's
- About to commit without user authorization — **STOP**; a direct commit
  instruction already supplies that authorization

## Scratch files

Any copy this workflow makes — of the repo, of a build-output directory, of a
file you replay edits onto — belongs in the operating system's temporary
directory, in a fresh directory named for the project and the purpose. Never
inside the checkout, and never under a home directory.

Delete it before you finish. A repo or build-output copy runs to gigabytes,
nothing reaps a home directory, and the out-of-disk failure that eventually
follows surfaces somewhere unrelated — a test suite that hangs, a build that
dies mid-link — costing far more to diagnose than the copy ever saved.
