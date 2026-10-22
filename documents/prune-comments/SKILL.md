---
name: prune-comments
description: Prune redundant, over-long or coupled comments, docstrings, and prose docs down to the minimal load-bearing why — including comments that rot when something elsewhere changes (file/line references, caller lists, inventories, keep-in-sync markers, change narration). Run after generating code to clean up comment/doc bloat. Optional scope arg — diff (default), touched, branch, repo, or a path.
argument-hint: "[diff|touched|branch|repo|<path>]"
arguments: scope
---

Reduce comment, docstring, and documentation bloat to the minimum a reader can't cheaply recover from the code. Reduction only — never add or expand; rewriting a comment into an equally short or shorter one is fine.

A comment fails in one of two ways. It is **verbose**: it says what the code already says. Or it is **coupled**: it talks about some other place — a file, a caller, a list kept elsewhere, the diff that produced it — so it must be edited whenever that place changes, and nobody remembers to. A short comment that names another file can be worse than a long one that only describes its own line.

## Scope

`$scope` selects what's in range (default `diff` when empty):

- `diff` (default) — only comments/docstrings/doc lines added or changed in the uncommitted diff, staged and unstaged (`git diff HEAD`). Comments you didn't just touch are off-limits.
- `touched` — every comment in any file the diff touches.
- `branch` — everything changed on this branch vs the default branch.
- `repo` — the whole repository.
- a path — that file or directory only.

Gather the set with git (`git diff HEAD` for `diff`, `git diff --name-only <base>...HEAD` for `branch`). For diff/branch, edit only added/changed hunks; touched/repo/path cover whole files. Skip generated and vendored files; the generator or upstream rewrites their comments.

## The bar each comment must clear

Keep a comment only if it works at a different level than the code: the load-bearing _why_ (intent, a gotcha, a non-obvious tradeoff or constraint), a one-line intuition over a dense multi-line block, or precision the code doesn't state (units, bounds, invariants). Otherwise:

- Same-level restatement — narrating the line it sits on → delete. A one-line summary over a block sits higher and may stay.
- Multi-line where one line suffices → compress to that line.
- Recoverable at the cost of one lookup (a stdlib call's semantics, a flag's meaning) → drop. Compressed domain knowledge that would cost a textbook or RFC dive stays.
- Coupled to something outside itself → see "Coupled comments".
- Docstrings → keep the contract; cut signature restatement. Where the repo's linter or pervasive convention requires public-API docstrings, the floor is a one-line contract — compress to it, never delete.
- Markdown/prose → cut on density and redundancy only. Leave tone/phrasing to the avoid-ai-tropes skill; don't duplicate its job.

Measure against a reader who has only the source tree — no plan doc, no PR description, no chat transcript.

Default to one line. When a comment is genuinely load-bearing, keep it compressed rather than lose it.

## Coupled comments

Each pattern lists its tells, what to do, and when it stays.

### Positional references

- **Tell**: `path/to/file.ext:123`, `line 88`, `L42` meaning a source line; `github.com/…/blob/(main|master|HEAD)/…#L40`; `see above`, `the function below`; `# handled in src/auth/session.ts`; links to Slack threads, Google Docs or localhost with no summary of the point. A path token that fails `test -e` is already stale.
- **Do**: delete when the code reads fine without it. Otherwise point by **name**, which grep, LSP and rename tooling resolve: `see parse_header`, or the language's checked link syntax (`{@link Foo}`, rustdoc ``[`Foo`]``, Sphinx `:func:`). An unavoidable URL gets pinned to a SHA or tag, with the point summarized inline so the comment survives the link dying. A stale path: fix it if the target is obvious, else delete.
- **Keep**: SHA-pinned permalinks; external specs by section (`RFC 9110 §15.5`); upstream issue links; one pointer to an existing doc that holds the explanation (`see docs/secrets.md`). Not a finding: `L1` cache, `layer 2`, `line 1 of the header` in protocol code.

```text
# see utils/headers.py:142 for the format       → # format: see parse_header
// fix from github.com/x/y/blob/main/a.go#L40   → // workaround for x/y#812 (keepalive drops first frame)
```

### Callers and consumers

- **Tell**: `(used|called|consumed|imported) (by|from|in) …` naming specific callers; `the admin dashboard and billing worker use this`; `See also:` / `@see` lists of more than two; a docstring mostly about who else exists.
- **Do**: grep the named caller; if it's a plain call site, delete. If a caller imposes a real constraint, state the constraint, not the caller.
- **Keep**: callers grep can't find — reflection or string dispatch, framework hooks, cron/queue/webhook entry points, config or template invocations, another repo. Not a finding: preconditions the caller establishes (`caller holds mu`); that's contract.

```text
# Used by checkout and the mobile API.   → # Payload shape is frozen: mobile v2 clients parse it.
```

### Keep-in-sync markers

- **Tell**: `mirrors`, `same as`, `keep in sync with`, `must match`, `also update`, `if you change this, change …`, followed by another file, symbol or system.
- **Do**: the marker is the only thing flagging a duplication, so deleting it alone makes things worse. Keep it, name the other site by symbol (a path only when the other side has none, e.g. SQL or YAML), and **report** the duplication — removing it is a design call outside this skill.

### Inventories and counts of another source of truth

- **Tell**: a comment listing what lives elsewhere (env keys, directory contents, enum members, providers, config fields, routes, flags); counts of it (`the 3 backends`, `all 5 event types`); a value restated from a constant in another file (`# retries 3 times` when `MAX_RETRIES` lives in config); module docstrings inventorying the file (`This file contains X, Y, Z`).
- **Do**: delete the list, or point at its source by name (`see Provider enum`, `keys: .env.example`). Drop the count or say "all". Name the constant instead of its value. Module docstrings state purpose and invariants, not contents.
- **Keep**: the list _is_ the source of truth (the only spec of an exhaustive match); an external contract nothing in-repo encodes; a count the adjacent code enforces (`# exactly 3 bytes: R, G, B`). Not a finding: unit-only comments (`# seconds`).

### Change narration and plan references

- **Tell**: a change verb about this code — `added`, `updated`, `fixed`, `replaced`, `moved`, `newly added`, `NEW:`, `FIX:`; `per review`, `as discussed`, `PR #123`; plan or phase references (`Phase 2`, `per the migration plan`, `plan.md step 3`); `Revision History`, `Last updated` blocks. Not a finding: the same words as domain terms (`Fixed-point math`, `Removed entries are tombstoned`).
- **Review, don't auto-delete**: `previously`, `no longer`, `instead of`, `now uses`, `as of <date>`. Act only when the comment makes sense solely to someone who read the diff or the conversation — the same words appear in real why-nots (`use X instead of Y: Y deadlocks`) and algorithm names (`phase 1 of two-phase commit`).
- **Do**: delete the narration; git history holds it. If a lasting why is buried in it, rewrite that as a present-tense comment about the current code. TODOs survive only when self-contained — a concrete condition that stands without the plan (`remove after v2 migration ships`); rewrite to one if recoverable, else delete.
- **Keep**: deprecations with a removal target (`@deprecated since 3.2, removed in 4.0`), `versionadded`/`versionchanged` in published docs; a rejected alternative with its reason; an incident cited because it _is_ the constraint (`don't batch: double charges, INC-123`); a workaround with its removal condition (`drop once lib >= 2.4`); files whose job is recording a change (migrations).

```text
// Updated to use the new client per review; old one timed out
→ // 5s client timeout: upstream drops idle sockets at 6s
```

### Implementation in interface docs

- **Tell**: a public docstring naming private identifiers or helpers; `internally`, `under the hood`, `first it … then it …`, `uses a dict`; numbered lists of internal steps.
- **Do**: keep only the contract — behaviour, params, errors, invariants. Move a genuinely tricky step to an inline comment beside the code; drop the rest. A contract you can't state without the implementation is a design smell: **report** it.
- **Keep**: traits callers depend on (`O(n log n)`, `not thread-safe`, `blocks on network I/O`, `cached for 60s`), observable side effects and their order, references to other public API (`same as load() but async`).

### Per-file headers

- **Tell**: `File: utils.py`, `@author`, `Maintainer:`, `Copyright (c) 2019-2025` ranges bumped yearly.
- **Do**: delete `File:` lines and authorship; git log holds them. **Never edit copyright or license headers** — report them; that's the legal owner's call.
- **Keep**: legally required headers; upstream headers in vendored files; `DO NOT EDIT, generated by X` banners.

## Examples

Same-level restatement — delete:

    - // increment the counter
      counter += 1

Over-long why → minimal why (real case):

    - # aarch64 emulation so this x86_64 host can cross-build the Raspberry Pi
    - # kiosk SD image (~/dev/kiosk). Some derivations run target binaries at
    - # build time (e.g. writeShellScript's bash -n), which fails without binfmt.
    + # cross-builds the Raspberry Pi kiosk SD image
      boot.binfmt.emulatedSystems = ["aarch64-linux"];

The code already says it enables aarch64 emulation — that's the _what_. The only thing unrecoverable from the code is _why this host_ has it: the cross-build. Keep that, drop the rest.

Plan reference — delete:

    - // Phase 2 of the auth migration: new token validator, replaces legacy_check
      fn validate_token(token: &str) -> Result<Claims, AuthError>

The plan isn't in the tree and git blame already says what this replaced. Nothing here survives a rewrite to "why does this code exist", so delete rather than compress.

Docstring carrying its weight — leave it:

    def settle(txn, *, retries):
        """Finalize txn; retry transient lock errors up to `retries` times.

        Raises LockError if still locked after the last retry.
        """

## Procedure

1. Resolve scope from `$scope` (default `diff` when empty); gather the target lines.
2. Enumerate every comment/docstring in scope, then rule on each: delete, compress, rewrite, keep, or report. No comment goes unruled — a keep requires a one-line justification naming what the code can't recover. If you can't name it, it's a delete. Check coupled claims before ruling: `test -e` the paths, grep the named callers and symbols.
3. Edit the working tree in place.
4. Print the verdicts, one line per comment — `path:line  <verdict>` (e.g. `3 lines → 1`, `deleted (same-level restatement)`, `deleted (plan reference)`, `path → symbol`, `kept — lock-retry gotcha`). For `branch`/`repo`, print changes only and end with the keep count. Then a **Report** section for findings left for a human: duplications behind keep-in-sync markers, license headers, interface contracts that can't be stated without the implementation. End with `review: git diff`.

Never commit; leave edits uncommitted for review.
