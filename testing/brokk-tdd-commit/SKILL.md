---
name: brokk-tdd-commit
description: Record one reviewed batch of a test-driven plan as one commit — verify the gating reviews passed, verify or create the plan's branch, stage exactly the reviewed paths by name, re-run the full suite on the combined tree, and commit with the plan's type and subject; never deciding, never fixing, never rewriting.
---

# TDD Commit

## Purpose

Record one reviewed batch of the TDD plan as exactly one commit. The transformation is mechanical and fully specified: **the plan row fixes *what*** — the packages, the type, the subject, the branch; **the reviews fix *the content*** — the union of the `Files changed` of every evidence block they cover; **the suite fixes *when*** — a green tree, or one carrying only the plan's recorded baseline failures.

**You decide nothing.** A mismatch between any two of those three is a report item, never something you reconcile by staging more, staging less, editing a file, or rewording a subject. The tree is the fact, the plan is a claim; when they disagree you stop.

**Self-contained by design.** Message grammar, branch prefixes, staging mechanics, and the git prohibitions are all below; nothing here is imported, and a gap is a report item rather than licence to improvise. **Git discipline, in force throughout:** run one git command per invocation — never chained with `&&`, `||`, `;`, a pipe, or a redirection — and read its output before the next; never rewrite history (`amend`, `rebase`, `reset`, `filter-branch`, or a force update of any ref); never perform a remote or history-moving operation (`push`, `fetch`, `pull`, `merge`, `cherry-pick`, `revert`); never commit a secret, a scratch file, or a build artifact.

## When to Use

- Dispatched as the commit step of the TDD workflow, in a **fresh session**, after every review the batch's `Gate` names has passed.
- The brief supplies the plan Workfile path and the batch number, the paths of the gating review Workfiles, and the pinned pre-commit `HEAD`.
- **Not for** implementing, refactoring, formatting, or "tidying" anything — you add no change of your own to the diff you record.
- **Not** while a parallel wave is in flight: the batch is the whole wave plus its integration, or the wave is not done.
- **Not on your own initiative.** An uncommitted green tree is not an instruction to commit.

## Commit Types

**Normative here and nowhere else**; the planning step echoes this mapping and says so. Every commit is a reviewed green state, so the red, green, and refactor phases never produce separate commits.

| Package kind | Type | Notes |
| --- | --- | --- |
| feature | `feat:` | new behavior, tests observed failing first |
| fix | `fix:` | reproduction test plus the fix |
| refactor | `refactor:` | behavior-preserving, with characterization tests |
| test | `test:` | tests only, green — characterization or coverage; never a failing test |
| scaffold | `feat:`, or `test:` when it adds only fixtures and declarations | |
| mixed batch | the kind of the package that delivers behavior, in the order `feat:` > `fix:` > `refactor:` > `test:` | |

**Subject grammar:** `<type>: <imperative, lowercase subject, ≤ ~50 characters, no trailing period>`, describing what the diff does. A body — blank line, wrapped at ~72 characters — only when the plan row supplies one.

## Branch Rule

Commit only on a branch whose name carries one of the three prefixes `feature/`, `fix/`, or `refactor/`; this set is fixed here and you add none. The plan row says `current` and the branch conforms → proceed. It says `create <name>` → `git switch -c <name>` before staging, and the uncommitted work rides along. It says `current` while the branch does not conform, or names a branch that already exists → stop and report. **Never commit to `main`, `master`, `develop`, or any unprefixed branch, whatever the brief says.**

## The Commit Record

Returned in the report; this session writes no Workfile.

```text
Commit: batch=<n>, branch=<name>, created=<yes/no>, hash=<sha>, parent=<sha>, type=<…>, subject="<…>"
Gate:   <review path> → <verdict line>          (one line per gating review)
Staged: <paths> — equals reviewed union: <yes>
Suite:  <command> → <verbatim tail> — green | baseline failures unchanged: <names>
Left uncommitted: none | <paths> — baseline-dirty per plan
Type check: consistent | <mismatch>
```

Capture run output verbatim, trimmed to the informative tail, never summarized into prose.

## Workflow

1. **Collect the inputs.** Read the plan header — `Branch:`, `Tree at planning:`, `Test command:`, `Baseline:` — and the batch row. Read the **first line** of every gating review Workfile: each reads `PASS` or `PASS-WITH-NOTES`, or you stop with `gate not met — <path>: <verdict>`. Collect the `Files changed` of every evidence block those reviews cover; their union is the **reviewed union**.
2. **Verify `HEAD`.** `git rev-parse HEAD` equals the brief's pinned reference, or you stop: something committed in between, and the reviews no longer describe the diff.
3. **Resolve the branch** per § Branch Rule.
4. **Verify the tree.** `git status --porcelain`. The modified and untracked set, minus the plan's recorded baseline-dirty paths, must equal the reviewed union exactly. A path in the tree but not in the union is unreviewed work → stop with `unreviewed change — <paths>`. A union path absent from the tree is a missing reviewed change → stop. Never stage a `.yggdrasil-workspace/` path; when the workspace is not ignored, say so in the record and **do not** add the ignore entry — that is a change nobody reviewed.
5. **Stage by explicit name**, one path per invocation: `git add <path>`, `git rm <path>` for a deletion, `git mv <old> <new>` for a rename. Never `git add .`, never `git add -A`, never a directory wholesale. Then re-read `git diff --cached --stat` and confirm the staged path set equals the union.
6. **Check the type** per § Commit Types: the plan row's type must be consistent with the staged diff's shape. A `feat:` row over a tests-only diff, or a `refactor:` row over a diff adding tests for new behavior, is reported — never re-typed.
7. **Run the full suite** — the plan's command — on the tree, and capture the tail verbatim. Green, or red on exactly the plan's baseline failures and no others → proceed. Anything else → commit nothing, **leave the index staged exactly as it stands** — undoing the staging is not yours to do, and the staged set is the evidence the next session inspects — and report `red at commit — <failing tests>`, adding `index left staged for inspection; no commit made`.
8. **Commit.** `git commit -m "<type>: <subject>"`, adding the plan row's body when it has one.
9. **Verify the result.** `git show --stat --name-status HEAD` lists exactly the staged set; the parent equals the pinned reference; `git status --porcelain` shows only the baseline-dirty paths.
10. **Report the commit record.**

**Failure handling.** Every stop condition above commits **nothing** and reports its named string, so the requesting agent has a stable token to route on. Also stop when: the plan row references a package with no gating review in the brief; a review file's first line is not a verdict line (`malformed gate — <path>`); branch creation fails because the name exists; or the suite command cannot execute at all — report its verbatim error, which is not a red suite. A missing `.yggdrasil-workspace/` ignore entry is noted, never fixed. A request to "just commit" past a stop is declined, restating the stop.

## Quality Criteria

- Exactly one commit exists, and its parent is the pinned `HEAD`.
- Committed path set = staged path set = reviewed union, with no workspace, scratch, or unreviewed path among them.
- The type is one of the four and is consistent with the diff; the subject is the plan row's, verbatim.
- The suite was run on the tree **after** staging, captured verbatim, and was green or red only on unchanged baseline failures.
- The branch carries a `feature/`, `fix/`, or `refactor/` prefix, and a created branch is recorded as created.
- Every git command was run alone, and no history was rewritten and no remote touched.
- The working tree afterwards holds only the plan's baseline-dirty paths.
- The commit record is complete and in the given schema.

## Anti-Patterns

- **Committing on a promise** — "the review is coming", "the verdict was verbal". The gate is a verdict line you read.
- **Staging the tree** because it "is all the reviewed work": `git add .` records whatever else happens to be there.
- **Fixing a red suite before committing**, or editing any file at all. A red tree at this step ends the session.
- **Rewording the subject to fit the diff**, or **re-typing the commit** when the row and the diff disagree. Both are reports.
- **Adding the `.gitignore` entry** you noticed was missing — an unreviewed project change.
- **Committing a subset of a wave**, or splitting a batch, because part of it is ready.
- **Committing to `main` "just this once."**
- **Amending or resetting to repair a mistake.** The fix is a new commit and a report; history is never rewritten.
- **Treating a PASS-WITH-NOTES note as a to-do** to address inside the commit.
