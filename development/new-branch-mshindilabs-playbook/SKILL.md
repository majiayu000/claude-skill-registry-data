---
name: new-branch
description: >
  Create a well-formed git branch named prefix.type.TICKET.short-description,
  where the prefix is the author's initials or whatever the project
  documents — for example
  abc.feat.FSS-373.multi-currency-invoices — dropping the ticket segment
  when no ticket or issue number exists (abc.fix.null-session-token).
  Validates the name against git ref rules and Conventional Commits types,
  branches from an up-to-date base, and protects uncommitted work. Trigger on
  "create a branch", "new branch for this", "branch off main", "start work on
  FSS-373", "make me a branch", "cut a branch for this ticket", or when
  starting work that should not land on the current branch. For deleting or
  pruning branches use clean-branch; for opening the PR afterwards use
  create-pr.
---

# new-branch

You create git branches that are consistently named, safe to push, and traceable back to their ticket. Never create a branch that leaves the user's uncommitted work stranded, and never invent a ticket number.

---

## The naming convention

```
<prefix>.<type>.<TICKET-ID>.<short-description>     # ticket known
<prefix>.<type>.<short-description>                 # no ticket — skip the segment entirely
```

Examples, with `abc` standing in for the prefix:

| Situation | Branch name |
|---|---|
| New feature, Jira FSS-373 | `abc.feat.FSS-373.multi-currency-invoices` |
| Bug fix, Linear ENG-88 | `abc.fix.ENG-88.null-session-token` |
| GitHub issue #412 | `abc.fix.GH-412.retry-webhook-delivery` |
| Dependency bump, no ticket | `abc.chore.bump-prisma-6` |
| Docs pass, no ticket | `abc.docs.api-auth-examples` |
| Urgent production fix | `abc.hotfix.OPS-19.expired-tls-cert` |

Segments are separated by `.` (dots). Do **not** substitute `/` or `-` between segments — the dot form is the convention.

### Segment rules

**`<prefix>`** — always present, always first, always lowercase. It is the author's initials or a team prefix, and it never varies within a repo. Find it in this order, stopping at the first hit:

1. The project's documented convention (its `AGENTS.md`, `CLAUDE.md` or `CONTRIBUTING.md`). When the project documents a full branch pattern, that pattern wins over this skill wherever they differ, including how a ticket or issue number is written.
2. A prefix the user stated, in this conversation or in their own agent instructions.
3. The user's own recent branches: `git for-each-ref --format='%(refname:short)' refs/heads refs/remotes/origin | grep -E '^(origin/)?[a-z]{2,4}\.(feat|fix|chore|docs|refactor|test|perf|build|ci|style|revert|hotfix)\.'`. Use a prefix only if one clearly dominates.
4. Nothing found → ask the user once which prefix to use. Never invent one.

**`<type>`** — exactly one of the Conventional Commits types, lowercase:

`feat` · `fix` · `chore` · `docs` · `refactor` · `test` · `perf` · `build` · `ci` · `style` · `revert` · `hotfix`

Pick by what the change *does*, not how large it is:
- `feat` — new user-visible capability
- `fix` — corrects broken behaviour
- `refactor` — restructures code, behaviour unchanged
- `perf` — faster or lighter, behaviour unchanged
- `chore` — deps, tooling, config, housekeeping
- `build` / `ci` — build system vs. pipeline config specifically
- `hotfix` — a `fix` that bypasses the normal release train

**`<TICKET-ID>`** — verbatim from the tracker, **uppercase project key + hyphen + number**: `FSS-373`, `ENG-88`. For a bare GitHub issue number, prefix `GH-`: issue 412 → `GH-412`. If there is no ticket, **omit this segment and its dot** — never write `none`, `noticket`, `n-a`, or a placeholder.

**`<short-description>`** — 2–5 words, lowercase `kebab-case`, describing the change:
- Say what changes, not what you'll do: `multi-currency-invoices`, not `add-multi-currency-invoices` (the type already says "add").
- No repetition of the type or ticket: not `abc.fix.FSS-373.fix-373-bug`.
- No filler: drop `the`, `a`, `some`, `stuff`, `update`, `changes`, `wip`, `misc`, `test123`.
- Specific over generic: `retry-webhook-delivery` beats `webhook-fixes`.

### Hard constraints

Verify every one before creating:
- Total length **≤ 70 characters**; aim for under 50.
- Only `a-z`, `0-9`, `-`, `.`, and uppercase letters inside the ticket ID. No spaces, no underscores, no `~ ^ : ? * [ \ @{`.
- No `..` anywhere, no leading or trailing `.` or `-`, no `.lock` ending.
- Must not already exist locally or on the remote.

Let git be the final judge:

```bash
git check-ref-format --branch "<name>"
```

If that exits non-zero, the name is invalid — fix it, do not force it through.

---

## Step 1 — Gather what you need

Work out the **type**, **ticket**, and **description** from what the user gave you plus the repo state.

Find the ticket in this order, stopping at the first hit:
1. An ID the user typed (`FSS-373`, `#412`, "ticket 373 in FSS").
2. An ID in the conversation already — a pasted ticket, an issue body, an error report.
3. Nothing → **skip the ticket segment.** Ask for a ticket number only if the user's own words imply one exists but they haven't said which ("the branch for that Jira ticket").

Never derive a ticket ID from a branch name, a guess, or a number that appears in unrelated context.

If the description is unclear from the request, ask one short question rather than inventing a vague slug.

## Step 2 — Check the repo is ready

```bash
git rev-parse --is-inside-work-tree
git status --short --branch
git branch --show-current
```

Then handle what you find:

- **Not a git repo** → say so and stop. Offer `git init` only if the user asks.
- **Uncommitted changes** → these matter. Present them and ask which the user wants:
  - carry them onto the new branch (default — `git switch -c` brings them along cleanly when the base is the current HEAD),
  - stash them (`git stash push -u -m "pre-<branch>"`, and tell the user the exact `git stash pop` to get them back),
  - commit them on the current branch first (hand off to `commit-changes`).

  Never discard, never `checkout -f`, never `reset --hard`.
- **Detached HEAD** → tell the user, and confirm the intended base explicitly.

## Step 3 — Pick and refresh the base

Detect the repository's default branch rather than assuming `main`:

```bash
git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@'
```

If that is empty, fall back to whichever of `main`, `master`, `develop` exists on the remote, and say which you chose.

Branch from the default branch unless the user names a different base, or the work clearly belongs on a release/`develop` line — in which case confirm the base before proceeding.

Refresh so the branch does not start behind:

```bash
git fetch origin --prune
```

Create from the **remote** ref, not a possibly-stale local one:

```bash
git switch -c <branch-name> origin/<base>
```

For a `hotfix`, base on the production line (the release branch or tag the user names), not on `develop`.

## Step 4 — Respect an existing repo convention

Before creating, look at what the repo already does:

```bash
git branch -r --sort=-committerdate --format='%(refname:short)' | head -20
```

If the recent branches overwhelmingly use a different shape (`feature/FSS-373-thing`, `release/*`) — especially if CI branch filters or branch protection rules key off a prefix — **flag the conflict and ask** before creating. A branch named outside the pattern CI matches on will silently skip its pipeline. Default to this skill's convention when there is no conflict.

## Step 5 — Verify the name is free

```bash
git rev-parse --verify --quiet "refs/heads/<name>"
git ls-remote --exit-code --heads origin "<name>"
```

If either exists, do not clobber it. Offer to switch to the existing branch, or append a distinguishing word to the description (never a bare `-2` or `-v2`).

## Step 6 — Create, confirm, and report

Create the branch, then confirm the result:

```bash
git switch -c <branch-name> origin/<base>
git status --short --branch
```

Report back plainly:
- the branch name and what each segment came from,
- the base it was cut from and that base's freshness,
- what happened to any uncommitted work (carried, stashed with the exact pop command, or committed),
- whether it has been pushed.

**Do not push automatically.** Only push when the user asks, or when they clearly want the branch on the remote immediately:

```bash
git push -u origin <branch-name>
```

Pushing publishes the branch name and its commits — treat it as an outward-facing action and confirm first.

If a guard or a git hook blocks the push, fix the cause and never bypass it (no `--no-verify`). See "If a guard or a git hook blocks you" in the `commit-changes` skill.

---

## Judgment calls

- **Several unrelated changes in flight** → one branch per logical change. Say so and suggest which to cut first, rather than creating a catch-all branch.
- **User gives a full branch name already** → validate it against the constraints above. If it is valid and intentional, use it verbatim; if it breaks a hard constraint, show the corrected form and why.
- **User is already on a branch in this convention and asks for a new one** → clarify whether the new branch stacks on the current work (base it on the current branch) or is independent (base it on the default branch). Do not assume.
- **Only a type and ticket, no description** → ask. `abc.feat.FSS-373` alone tells a reviewer nothing six weeks later.
