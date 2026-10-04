---
name: upstream-contribution
description: Contribute from a fork to a repository you do not own without burning maintainer trust. Use when the working repo has an `upstream` remote, when the user says "open a PR against <someone else's repo>", or before the first commit in any repo the user is a guest in.
---

# Upstream contribution

**This repo is not yours.** It belongs to its maintainers, with their own queue, their own
conventions and their own history of unmerged good intentions. Act like a guest.

## Remotes

`origin` is **your fork**. `upstream` is the project, and its push URL is set to `no_push`:

```bash
git remote set-url --push upstream no_push
git remote -v          # origin = fork, upstream = project (no_push)
```

The remote you type by reflex is the one that is safe to push to. **Never commit to local
`main`** — keep it a clean mirror of upstream so rebases stay trivial:

Before replacing a fork branch, inspect `git status --porcelain --ignored` and the commits unique to it.
Stop if there are local modifications, untracked or ignored work, or unpublished commits; preserve
them outside the checkout or in a task branch first (ignored files need explicit preservation).
Never use a hard reset as an automatic cleanup shortcut. For a
clean mirror with no unique work, fetch and fast-forward:

```bash
git fetch upstream
git switch main
git merge --ff-only upstream/main
```

If that refuses, report the divergence; an intentional reset needs explicit authorization.

## Issue before code

For anything larger than a bug fix or a doc correction, **open an issue and wait for a
maintainer response before writing the implementation.** Most projects have a graveyard of
large unsolicited PRs. Volume of code is not what gets merged; agreement beforehand is.

Use the repo's issue templates. If the work is speculative, say so.

## Branch and PR scope

- Branch names: `<issue-number>-brief-description` when an issue exists, otherwise
  `<area>-brief-description`.
- **One concern per PR.** Every file in the diff traces to the declared issue. Split an
  oversized PR before requesting review, not after.
- **Never change a default silently.** The project runs inside other people's production. New
  behaviour arrives as a new parameter whose default preserves today's behaviour exactly.
- **Never bundle a refactor with a fix.** An open "make it DRY" issue is not a licence to tidy
  code you happened to be near.
- **A return-type change is a breaking change**, including swapping a third-party type for
  your own. Say so honestly in the PR; getting it wrong is how trust is lost.
- Sweeping changes (docs, type hints, lint) go one module family per PR. A fifty-file sweep is
  unreviewable and will sit.

## Before opening the PR

Run the project's own gates exactly as CI runs them; the `verification.md` rule applies with
extra force here. Fill in the PR template's sections and delete none. Use the labels the
project's release tooling reads; do not fight auto-labels.

## Where the contributing guide actually lives

`CONTRIBUTING.md` is often a stub. Treat the CI workflow file, the lint config, the PR template
and an existing module of the same kind as the in-repo sources of truth. If the real guide is
behind a site that blocks fetches, a human opens it; do not guess at its contents.

## Community

If the project has a chat or a regular contributor call, asking there is cheaper than a
rejected PR.
