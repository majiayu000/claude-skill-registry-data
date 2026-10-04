---
name: elisp-conventions
description: Apply local coding and verification rules when modifying or testing Emacs Lisp, or when explicitly reviewing code against these conventions. Use for dotfiles extras, standalone Elpaca packages, and other .el files; not for non-Elisp work or read-only bug, security, or design reviews where these conventions are not material.
---

# Emacs Lisp conventions

Use this skill before changing a `.el` file and keep it active through
verification. For an explicit read-only conventions review, apply only the
relevant style rules; do not turn the review into an edit or live-Emacs task.

Apply these rules to the requested change, not as permission to restyle unrelated
code, alter public interfaces, or operate on the active session. Preserve user
edits and inspect unsaved buffers before changing a visited source file.

Use `lint-elisp` in addition when the user asks for compiler, checkdoc, or lint
diagnostics. Use `document-elisp-package` when an Org manual must be created or
refreshed.

## Coding style

- Write atomic, focused functions. Prefer a small function with a clear name to
  a comment that explains a long implementation.
- Do not insert empty lines within a function.
- Put helper functions after the function that calls them.
- Document every argument in docstrings with its uppercase name.
- Fill docstrings to 80 characters. Start with a one-sentence summary.
- In a multiline docstring, continue the first paragraph on the next line
  without an empty line. Separate later paragraphs with one empty line.
- Do not end error messages with a period.
- Add comments only when the code cannot make the reason clear.

## Choose the layout

Every edited `.el` file uses one of these paths:

1. **Dotfiles extra:** production source under
   `~/My Drive/dotfiles/emacs/extras/`. This is canonical source; the active
   Elpaca dotfiles checkout is a committed mirror. Use `dotfiles-context` for
   source routing.
2. **Standalone package:** identify the owning package from its metadata and
   project instructions. For an Elpaca-managed package, use `dotfiles-context`
   and `bin/elpaca-package-resolve` to obtain the actual registry ID, canonical
   source, repository, and evidence label; do not guess from profile-directory
   names. Unmanaged packages use their own documented checks and loading path.
   For an externally maintained package fix, also use `dotfiles-context`'s
   upstream contribution workflow, even if the user did not mention a PR.
3. **Non-package Elisp:** configuration and support files such as
   `.dir-locals.el` or `lockfile.el` use the owning project's checks. Location
   outside an Elpaca root does not by itself make a package non-package code.
   Do not force an Elpaca rebuild or package manual onto unrelated files.

Test-only files inside a package follow the package's batch and focused ERT
paths, but they do not need a rebuild, live package reload, or manual update
unless they also change production code or user documentation.

## Verification workflow

1. Edit the canonical source.
2. Establish clean batch evidence for the changed code:
   - For a dotfiles extra, run the absolute `batch-test.sh PACKAGE` command
     below. It must load the canonical extras source.
   - For managed standalone production source, run `batch-test.sh PACKAGE`
     using the resolver's evidence `.label` (the checkout label), not a guessed
     library name. The runner resolves the package ID internally. An unmanaged
     package uses its documented clean batch/compile/test workflow; do not
     register or install it just to satisfy this skill.
   - A load-only check proves loadability, not the changed behavior. Exercise
     the relevant assertion and required project checks as well.
   - For non-package Elisp, run the owning project's clean batch or compile
     check through `elisp-check-evidence file:RELATIVE-PATH -- PROJECT-CHECK`.
     `PROJECT-CHECK` must be a tracked executable in that repository. Do not
     substitute an unrelated package check.
   - A deleted production file cannot be loaded. Use the same `file:RELATIVE-PATH`
     label with a project check that proves the repository is valid without it.
3. Run focused ERT when behavior needs it. Read
   [references/testing.md](references/testing.md) for command forms and
   stale-compiled-code safeguards.
4. Before any live Emacs check, read
   [references/live-verification.md](references/live-verification.md).
   - After the verified commit, use `elisp-live-verify PACKAGE -- EXPR` for a
     standalone package or dotfiles extra. It waits for the package rebuild,
     exercises the named live path, and records package/commit-bound evidence.
     Confirm the helper supports this package before using it. An isolated
     fixture does not establish that an existing live session has the change.
   - For a deleted package, use `elisp-live-verify deleted:PACKAGE -- EXPR`.
     The helper removes only that package's safe Elpaca build, unloads the
     feature, and requires a non-nil expression that verifies its absence.
     This destructive mode is only for an authorized whole-package removal,
     not a library/file rename within a surviving package.
   - Non-package Elisp uses its owning workflow; do not load it into the active
     session unless that workflow makes the operation safe.

```bash
~/My\ Drive/dotfiles/claude/bin/elpaca-rebuild-wait PACKAGE
~/My\ Drive/dotfiles/claude/bin/elisp-live-verify PACKAGE -- '(PACKAGE-CHECK)'
~/My\ Drive/dotfiles/claude/bin/batch-test.sh PACKAGE
~/My\ Drive/dotfiles/claude/bin/elisp-check-evidence file:RELATIVE-PATH -- PROJECT-CHECK
~/My\ Drive/dotfiles/claude/bin/elisp-ert PACKAGE TEST-FILE [TEST-NAME]
```

Test evidence counts only when it identifies the repository, package, and
source revision or equivalent content identity that was tested. A generic
session marker or a clean test for another package is not evidence for the
current change. Live evidence must also identify the committed repository and
package and establish the intended runtime, profile, source checkout, and
successful rebuild token. A true return value is not sufficient unless the
expression directly checks the requested behavior. Treat any stale-load warning
as a failed verification.

These rules are enforced on content, not on command spelling, so pipes,
chained `git add && git commit`, `git -C`, and multi-line messages all work.
Each successful runner records which Elisp files, at which contents, it
covered. In agent sessions the global Git `pre-commit` hook
(`claude/git-hooks`) rejects a commit whose Elisp contents no run covered and
prints the runner command to use. The `post-commit` hook records a live check
as owed for a production package, and the Stop hook keeps the turn from
ending until `elisp-live-verify` covers that commit or a later one. Nothing
blocks other commands in between, so a bug the live check finds can be fixed,
tested, and committed normally.

Never use `load-file`, `eval-buffer`, `eval-defun`, or manual
`byte-compile-file` to reload edited package code. Use the bounded rebuild helper
and the layout-specific sequence above.

## Documentation and commit gates

Update and stage the matching manual for changed documented behavior:

- Dotfiles extras use `emacs/extras/doc/<package>.org`.
- Standalone packages use their established manual, including a non-root Org
  manual. Use root `README.md` only when the project has no Org manual.

The current commit guard mechanically requires a selected manual for non-exempt
production `.el` changes when it finds a manual; it does not determine whether
behavior changed or whether that manual belongs to the package. Standard skill
`scripts/*.el` helpers instead require changed, selected `SKILL.md` or
`references/*.md` from each owning skill. Mixed package changes retain the
independent manual requirement.
Check the actual scoped commit paths. Never stage an unrelated manual or invent
a documentation change to appease the guard. If a truthful no-doc change is
blocked, diagnose the policy conflict; do not silently disable the guard.
When generated Texinfo/Info outputs change, validate and stage the destinations
actually declared by the manual, which need not share a basename.
Read declarations from the proposed commit's manual bytes, not unrelated
unstaged headers. For combined staging/commit syntax the guard cannot resolve,
stage the intended files separately and rerun the check without borrowing other
staged changes.

Manual updates are not required only because a commit changes a test file or a
generated/machine-owned file such as `lockfile.el`, `*-autoloads.el`, or
`*-pkg.el`. Read [references/testing.md](references/testing.md) before using the
branch-local documentation deferral for a deliberate multi-commit refactor.
