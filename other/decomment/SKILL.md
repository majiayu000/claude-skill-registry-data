---
name: decomment
description: >-
  Prune comments after nontrivial code edits and before handoff, or when asked
  to decomment, remove, clean up, or trim comments in a file, working tree,
  branch, diff, PR, or commit range. Subtractive only: delete narration and
  restatement, trim doc comments to caller contracts, preserve directives.
  Route factual drift to code-gardening and refactoring to code-simplifier.
  Skip prose, docs, and pre-existing comments outside the named scope.
---

# Decomment

Run a subtractive comment pass. The result has fewer, smaller comments and
identical non-comment code. Delete or shorten comments; add only a minimal doc
comment when a linter requires one. Keep edits unstaged for the caller to review.

## 1. Resolve scope

Choose the requested boundary before reading files:

| Invocation | Comments in scope |
| --- | --- |
| Final pass after nontrivial code edits | Comments you added or changed in this session's working tree and your commits on this branch. Run before handoff, commit, or PR. A typo or single-line fix needs no automatic pass. |
| Bare `decomment` or current branch | Added or changed comments in `git diff --name-only "$(git merge-base <base> HEAD)"`, where `<base>` is the git-spice branch base, falling back to `master`. |
| Working tree | Added or changed comments in `git diff --name-only HEAD`, plus untracked files from `git ls-files --others --exclude-standard`. |
| Commit range `A..B` | Added or changed comments in `git diff --name-only A..B`. |
| Named file(s), directory, or package | Every comment in the named scope. |
| Explicit whole-workspace request without Git history | Every comment in the requested workspace. |

Use the diff to identify authorship, including staged changes. Read every
in-scope file fully before editing: an added comment can duplicate a fact
elsewhere in its file. If the user names a diff, branch, or PR, resolve its
actual base and changed lines before selecting comments. Completion: every
candidate comment is traced to the requested boundary.

## 2. Classify and prune

Before classifying, read the [comment rules](references/comment-rules.md); they
hold the deletion rules and linter floor. Apply every rule to every in-scope
comment, including tests and plausible-sounding reasons. Ask: **What would a
reader fail to learn from the code if this were deleted?** Delete it when the
answer is nothing. Keep a comment that states a non-obvious constraint,
intent, or caller contract.

Prune aggressively. If most candidate comments survive or none is deleted,
rescan for facts repeated across sites, implementation narratives dressed as
reasons, and arithmetic or defaults evident nearby. Sunk effort does not earn
a comment its place. A long genuine reason may survive; length alone is not a
deletion test. Completion: each in-scope comment has a keep, shorten, or delete
decision supported by the rules, including the one-line floor for exported Go
types, functions, constants, and variables.

## 3. Protect the boundary

Keep these bytes intact in every mode:

- Pre-existing comments you did not author, unless the user explicitly scoped
  a full pass to their file, directory, package, or workspace; comments the
  user marked to keep.
- Generated files and markers, including `Code generated ... DO NOT EDIT`,
  `@generated`, `.pb.go`, and `.gen.` files.
- License and copyright notices.
- Shebangs and tool directives such as `//go:`, `//nolint`, `//revive:`,
  `# noqa`, `# type: ignore`, `# shellcheck`, `// eslint-disable`, and
  `# pylint:`; preserve editor and linter controls in any language.

Repo-local `AGENTS.md` or `CLAUDE.md` comment policy takes precedence. Keep
non-comment code unchanged: refactoring belongs to the `code-simplifier`
skill, and a factually wrong comment is drift for the `code-gardening` skill
to correct, so leave it in place and flag it. Use targeted edits rather than
whole-file rewrites. Completion: the diff contains only permitted comment
deletions or trims, and any required linter-floor comment.

## 4. Verify and report

Inspect the diff for code, directives, and notices; run the smallest relevant
parser, linter, or test when comment edits could affect it. Leave the work
unstaged and uncommitted. Report removed and trimmed comments by file, or say
"nothing to prune" after a completed scan. Flag code problems noticed during
the pass without fixing them. Completion: the report accounts for every changed
file, verification result, and noticed code problem.

When several skills apply, run the `code-simplifier` skill first, this comment
pass next, then the `writing-for-humans` skill for PR or commit prose. This
skill covers code comments and docstrings; prose and documentation belong to
their own writing pass.
