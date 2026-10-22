---
name: prune-hard
description: Strip comments from code you own down to the traps — delete by default, keep only what stops a future edit from silently breaking something. The harsh sibling of prune-comments, for private or solo codebases. Optional scope arg — diff (default), touched, branch, repo, or a path.
argument-hint: "[diff|touched|branch|repo|<path>]"
arguments: scope
---

Under `prune-comments` a comment survives if it carries a load-bearing why. Here it survives only if losing it would cost a bug or real rediscovery time. **Deletion is the default outcome, not compression.**

Use this on code you own and maintain — a private config, a solo project, a personal tool — where the readers are you, a coding agent, and git history. For a library, a shared service, or anything with readers who aren't you, use `prune-comments` instead.

## Scope

`$scope` selects what's in range (default `diff` when empty):

- `diff` (default) — only comments added or changed in the uncommitted diff (`git diff HEAD`).
- `touched` — every comment in any file the diff touches.
- `branch` — everything changed on this branch vs the default branch.
- `repo` — the whole repository.
- a path — that file or directory only.

For diff/branch, edit only added/changed hunks; comments outside the range stay, however verbose they look.

## The bar

One question per comment: **if this line vanished, would I or a coding agent plausibly break something, or burn real time rediscovering it?** If no, delete it. If unsure, delete it.

### Delete

- Header prose: what this file is, what the module does, why it exists. The filename and the code say it.
- Architecture narration — "this file only holds X, the rest lives in Y", "same pattern as Z", "extracted during the Q3 refactor".
- Any restatement of language, framework, or upstream semantics — anything one lookup or one grep away.
- Enumerations of what lives in another source of truth: which keys an env file holds, what a directory contains, which fields a schema defines.
- Rationale for ordinary choices — why this port, this library, this pool size — unless guessing wrong breaks something.
- Narration of the adjacent line.
- Cross-references to other files in the same repo. Grep exists.
- Change-relative notes: plan or phase references, "replaces the old client", "newly added".

```text
# increment the retry counter            → the line below says this
// useEffect runs after render           → framework semantics, one lookup away
# we use Postgres because it's solid     → rationale for an ordinary choice
// replaces the old v1 client            → git history holds this
# .env holds DB_HOST, DB_USER, DB_PASS   → the env file is its own source of truth
```

### Keep, cut to one line

- **Traps.** Code that looks wrong, redundant, or removable but is load-bearing, and constraints that break silently when someone tidies up. This is the main category — most survivors are traps.
- **Manual setup not derivable from the tree**: a secret to set by hand, a DNS record, a click in someone's console. A terse checklist, one line per step.
- **A value whose source is unguessable**: a limit belonging to the upstream API rather than your config, a cutoff date with a reason behind it.

```text
# lock order: accounts before ledger, or the nightly job deadlocks
// keep the .toList() — the lazy view escapes the transaction scope
# minor units; the ledger stores cents, so never divide here
// retry 409 only; the SDK already backs off on 429
-- partial index (status='active'); an unfiltered lookup won't use it
# 4 MiB is SQS's hard cap, not a tunable
// double-fires on macOS, so this handler must stay idempotent
```

Each one stops a plausible future edit from breaking something quietly. Most files should end with 2–5 comments of this shape.

### A worked pass

Before — nine comment lines, none of which survive contact with the question:

```python
# ------------------------------------------------------------
# Payment reconciliation
#
# Reconciles charges against our ledger. Extracted from
# billing.py during the Q3 refactor. See also ledger/models.py.
# ------------------------------------------------------------


def reconcile(charges, *, window):
    # Sort the charges by creation time
    charges = sorted(charges, key=lambda c: c.created)

    # Stripe returns amounts in minor units
    total = sum(c.amount for c in charges)

    # Loop over the charges and match each to a ledger entry
    for charge in charges:
        # Skip refunds, they are handled elsewhere
        if charge.refunded:
            continue
```

After — one line, because it is the only one whose loss would cause a bug:

```python
def reconcile(charges, *, window):
    charges = sorted(charges, key=lambda c: c.created)

    # minor units — the ledger stores cents, so never divide here
    total = sum(c.amount for c in charges)

    for charge in charges:
        if charge.refunded:
            continue
```

## Lines that look like comments but aren't

- **Help text** is program output: `argparse` `help=`, a `click` docstring that becomes `--help`, a cobra `Short`/`Long`, a `##` Makefile target, a justfile `[doc(...)]`.
- **Published docstrings** are interface: anything a doc generator renders (Sphinx, godoc, rustdoc, JSDoc on a public API). Prune those under `prune-comments` rules, never under this one.
- **Prose and instruction documents** — a README step, a runbook, an agent prompt file. An executable instruction is content, not commentary, even when it reads redundantly.
- **Directives and pragmas**: shebangs, build tags, `# noqa`, `# type:`, `@ts-expect-error`, `eslint-disable`, license headers, encoding lines.
- **Comments inside string literals** ship as part of the artifact — an embedded config, a generated script. Still prunable, but you are editing a deployed file, not a source comment.

## Style

One line per survivor; a sentence fragment beats a sentence. Never exceed the file's existing comment width — match the neighbours, typically 80–100 characters. Collapsing three wrapped lines into one 150-character line is not a win.

## Procedure

1. Resolve scope and list the files.
2. **One subagent per file**, run concurrently — files are independent. Per-file focus is what keeps the bar harsh; an agent holding ten files drifts back toward compressing instead of deleting. Give each the bar above and nothing else to do.
3. Each agent edits in place and returns one verdict line per comment: `path:line  <verdict>`.
4. **Prove the edits are comment-only.** Best: parse each file before and after and compare — a parser drops comments, so an identical parse means identical code (`python -m ast`, `nix-instantiate --parse`, or the language's equivalent). Where no such tool exists, or where the file's comments live inside string literals and so legitimately change the parse, fall back to checking that every changed line, `+` and `-`, is a comment.
5. Run the formatter, then the project's fastest whole-tree check — build, typecheck, or test.
6. Print the verdicts and end with `review: git diff`.

Never stage and never commit; leave everything as working-tree changes. Say this to the subagents explicitly — they reach for `git add` on their own.
