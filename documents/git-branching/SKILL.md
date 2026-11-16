---
name: git-branching
description: Use when starting a branch, deciding how a change reaches the mainline, cleaning a branch's history before it lands, or choosing whether a repository needs more than one long-lived branch — in a repository of any language. Owns the one mainline releases are cut from, recording the branching and merge method and the branch-name pattern once per repository, the short-lived one-change branch, folding a fix to unlanded work into the commit it fixes, never rewriting history someone else may have built on, and when a released version earns a maintenance branch. What each commit's message says is `git-commit-message`; computing and cutting the release is `/release`. - Also when asked about GitHub Flow, GitFlow or trunk-based development, a develop or release branch, squash versus merge commit versus rebase merging, force-pushing, rebasing a branch, fixup commits, cleaning up work-in-progress commits, branch names, deleting a merged branch, or hotfixing a released version.
---

# Git — Branching

How a change travels from a branch to the mainline, and what the history looks like when it arrives.
This skill assumes no language, forge or team size, and it names no strategy as the right one: it
states what holds under every strategy, binds the lightest one below, and says what a heavier one
has to earn.

**Precondition — who runs a version other than the latest.** Most rules hold for any repository.
One depends on the answer:

| Does anything… | If no, this does not apply |
|---|---|
| run, or depend on, a released version other than the latest | rule 8 — nothing needs a fix on an old line, so every fix ships as the next number |

## When to use vs. neighbours

- What a commit's message says, its type, and where the convention has to hold under each merge
  method → `git-commit-message`. This skill picks the merge method; that one says what the choice
  obliges each message to be.
- Working out the next version from the history and cutting the release commit and tag → `/release`.
- What a version number promises, and the tag's own form → the ecosystem's versioning rules; for a
  Python distribution, for example, `python-versioning`, in the `pyhouse-universal` plugin.
- Refusing a malformed message at commit time → `/install-commit-hook`. It checks a message's shape,
  not which branch it lands on.

## Template — short-lived branches off one mainline, every commit kept

What the repository records, where contributors read — a `CONTRIBUTING` file, an agent instructions
file — writing its own default branch for `main`, its forge's word (merge request, pull request) for
"request", and the pattern its branches already share, if they share one, for `<type>/<change>`:

```markdown
## Branching

- `main` is the mainline. It always builds and passes.
- Releases are tags on `main`.
- Every change reaches `main` through a request whose checks pass.
- A request lands with a merge commit, keeping every commit, so each is cleaned up before it lands —
  fixups folded, work in progress reworded. Squash and rebase merging are off.
- A branch carries one change, starts from current `main`, and is deleted once it lands.
- A branch is named `<type>/<change>` — the commit type its change takes, then a few lowercase
  hyphenated words.
```

The releases line is written only where releases are tagged; a repository that releases no versions
leaves it out.

The forge enforces the block with three repository settings, made once (rule 2): merge commits only,
with squash and rebase merging off; the branch deleted when it lands (rule 6); and `main` protected —
no push straight to it, and no request merged until its checks pass.

## Other bindings

- **Squash merging.** The request's title becomes the one message that lands, so no branch commit
  needs curating — and the title is what has to be conventional, checked in CI or by the forge, since
  no local hook sees it. Every rule but 4 holds unchanged; rule 4's curation moves from the branch to
  the title, as `git-commit-message` rule 9 says.
- **Committing straight to the mainline** (trunk-based, no requests). Workable where one person owns
  the repository and the checks run before each push. Rule 1's gate moves from the request to the
  push; rule 5 then has no branch to protect but the mainline; rule 4 applies to the local commits
  before each push.
- **GitFlow** — a long-lived integration branch beside the mainline, plus release and hotfix branches.
  Earned when a release has to stabilise while other work continues, or several released lines are
  maintained at once; it is rule 7's exception, taken deliberately and recorded under rule 2.

## Rules

1. **One branch is the mainline, and every change that lands on it leaves it releasable.** Releases are
   cut from it and nowhere else, so a change too large for one short branch lands in steps that each
   pass, or behind a switch that keeps it inert. Where no environment stands between the mainline and
   production, the checks a change passes before landing are the only gate, and nothing skips them.
2. **The strategy is chosen once per repository and recorded where contributors read.** How a change
   reaches the mainline, and the merge method a request lands with, are one decision — not a choice
   per request, because `git-commit-message` puts the convention's check in a different place under
   each method. Every request lands the recorded way. Enforce it in the forge's settings where the
   forge allows it. The branch-name pattern is recorded with it, so every contributor, person or agent,
   names a branch the same way. Changing either later is a recorded decision too. Where the method is
   not recorded, the forge's merge setting is the answer; failing that, the mainline's shape — merge
   commits on it mean every branch commit lands, and single-parent commits whose subjects end in a
   request number mean squashing; anything else, ask.
3. **A branch carries one logical change, starts from the current mainline, and lives until that change
   lands.** A long-lived branch drifts from what it will merge into, and its conflicts arrive all at
   once, late. Name it for the change, in the pattern the repository records (rule 2), or, where it
   records none, the one its branches share — two prefixes for one kind of change count as none; then
   name it by the template's pattern and propose recording one in a change of its own, since a pattern
   is the repository's decision, never made inside an unrelated request. Never name it for the spec or
   plan it was planned in, even where a tool created it so: a merge commit or the request records the
   name, so it names only what `git-commit-message` rule 10 lets a message name, and a branch so named
   is renamed before its request opens, which rules 5 and 6 allow while only its author has used it.
   Where changes land
   through requests, nothing is committed straight onto the mainline — except the repository's first
   commit, which creates the mainline and has nothing to branch from.
4. **Before a branch lands under a keep-every-commit method, its history is made true.** A fix to a
   change that has not landed yet is folded into the commit it fixes, never committed as a `fix` of its
   own — that records a defect no release ever carried; it is committed as a fixup of that commit and
   folded, so no `fixup!` or `squash!` commit reaches the mainline. Work-in-progress commits are folded
   or reworded. This is the curation a squash would otherwise do, done where the author still knows what
   each commit was. A fold is meant to change no line the branch's checks have seen: it keeps the point
   the branch left from, a fold that did change the tree has the checks run again, and bringing the mainline in is
   the merge's job, never the fold's.
5. **History someone else may have built on is never rewritten.** The mainline, and any branch another
   person or process has fetched, are never rebased, amended or force-pushed; a mistake on them is
   corrected by a new commit. A branch only its author has used may be, until it lands — with a force
   that refuses to overwrite commits the author has not seen (a lease), never a bare force.
6. **A branch is deleted once it has landed; until then, only by whoever created it.** A branch whose
   commits are not on the mainline is someone's unfinished work; deleting it destroys that work with no
   record it existed, so anyone else asks its owner rather than deleting it. Once it has landed nothing
   is lost, so the forge deleting it on merge is right.
7. **The mainline is the only long-lived branch until another one earns its place.** A second
   integration line, a release-stabilisation branch or a per-environment branch each doubles where a
   change has to land. One earns its place only by a need rule 1 cannot meet — a release stabilising
   while other work continues, or an old line still maintained. Without one of those it is GitFlow's
   cost without the need that pays for it.
8. **A released version is fixed on the mainline and shipped as the next number, unless something
   still runs that version and cannot take the latest.** Only then is a maintenance branch cut from
   its tag, the fix landed there and on the mainline, and the maintenance release tagged from that
   branch. Precondition: something runs or depends on a version other than the latest.

Rule 4 in git: a fix to unlanded work is committed with `git commit --fixup=<sha>` and folded before
the request lands by `git -c sequence.editor=: rebase -i --autosquash $(git merge-base origin/<mainline> HEAD)`
after `git fetch`; the no-op editor accepts the folded plan without opening one. Take
`git rev-parse HEAD` before the fold and `git diff <before> HEAD` after it: empty, the tree is the one
already checked; not empty, the fold changed the tree. Before git 2.44, `--autosquash` without `-i` is
silently ignored and the fixups land as they are.

## Hard stops

- Asked what a commit message or its type should be → stop, use `git-commit-message`.
- Asked what the next version is, or to cut a release → stop, use `/release`.
