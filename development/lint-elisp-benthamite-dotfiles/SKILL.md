---
name: lint-elisp
description: Fix byte-compile warnings, checkdoc notes, and other Elisp diagnostics in one or more files. Use when the user says "lint elisp", "fix warnings", "fix diagnostics", "elisp lint", "checkdoc", "byte-compile warnings", or wants to clean up Elisp compiler/linter output.
argument-hint: "[file-or-directory]"
---

# Lint Elisp

Diagnose and fix the requested Elisp diagnostics without changing intended
behavior. A completed diagnostic run is not the same as a warning-free run;
an error, skipped compiler or incomplete check must never become “clean.”

Use `elisp-conventions` for Elisp edits and verification, and `dotfiles-context`
when canonical package or paired configuration routing is needed.

## 1. Resolve scope and source

Use the actual request and reliable current-file context, not just a literal
`$ARGUMENTS` placeholder. A review, diagnosis-only or “show diagnostics” request is read-only;
a request to fix/lint the named targets authorizes scoped diagnostic fixes.

- A file request selects that exact source, including its owning repository and
  any unsaved buffer state. Do not overwrite a conflicting buffer or pick another
  file from its basename.
- A directory request defaults to immediate `.el` children unless recursive or
  exhaustive coverage was requested. Record the inventory and exclusions.
  Generated files such as `*-autoloads.el` and `*-pkg.el` normally route to their
  source/generator, not hand edits. Do not silently skip an explicitly named file.
- With no path, use an unambiguous target already established in the conversation.
  Ask one concise question only if that identity remains genuinely ambiguous;
  do not guess a “main file” from the directory name.

Resolve managed sources and required dependency locations through the actual
registry/project workflow. Do not construct a profile path from a string returned
by `emacsclient`, scan profiles for a plausible checkout, or use the package's
build as its source. An unavailable required registry/dependency context is a
reported limitation, not permission to guess. Unmanaged or self-contained Elisp
uses its own documented clean batch context; it does not require a live profile
merely to check a built-in-only file.

## 2. Collect complete diagnostics

Read [the runner contract](references/diagnostics.md) before running
[scripts/lint-file.el](scripts/lint-file.el). Use a fresh `emacs -Q --batch`
process for each exact target with literal arguments and verified source-first
dependency paths. Never interpolate a filename into an Elisp expression.

Byte compilation can execute macros, `eval-when-compile` and required libraries.
Inspect relevant code/project commands before execution; `-Q` and temporary
output are not a sandbox or authority for network, installation or live-runtime
effects. If those effects exceed the request, report the blocked check. Do not
load the target into the active Emacs session to make compilation succeed.

Record each stage's completion, diagnostics and errors, plus the target identity,
Emacs version and dependency context used. Preserve the initial findings so fixed,
remaining and newly introduced diagnostics can be distinguished. A successful
process exit alone, empty grep output or a missing callback proves nothing about
a check that did not complete. Treat `no-byte-compile` as an explicit skip, not
a clean compile; do not remove the directive merely to satisfy the checker.

## 3. Fix causes, not warning counts

Read each diagnostic in its declaration/caller context before editing. Common
cases are investigation routes, not automatic transformations:

| Diagnostic | Behavior-preserving approach |
|---|---|
| Free variable | Check spelling, lexical binding, macro expansion and the defining dependency. Use a forward `(defvar VAR)` only for an established special variable; it changes binding interpretation within its scope. Do not invent a global declaration to conceal a missing local binding. |
| Later variable definition | Check initialization, custom setters, dependency and load order before moving `defvar`, `defcustom` or `defconst`. Moving an initializer is not just formatting. Prefer an accurate declaration when it preserves the established contract. |
| Unknown function | Check the actual provider and intended optional/eager loading. Use a truthful `declare-function` or appropriate dependency fix; do not add an eager `require` solely to suppress a warning. |
| Unused binding | Preserve initializer evaluation, ordering and side effects. An ignored local name may be suitable; deleting the binding is safe only if its evaluation is unnecessary. Check keyword, public and introspected argument contracts before renaming formals. |
| Argument missing from docstring | Describe the actual argument in uppercase without inventing behavior or padding the prose. |
| Imperative or punctuation note | Apply the rule to the actual declaration type and meaning. Function-docstring guidance is not a universal rewrite of variable documentation. |
| Width note | Use the project's/checker's actual width and preserve literals, URLs, syntax and readable meaning; do not assume every diagnostic uses 80 columns. |

Preserve docstring semantics and public interfaces. Do not disable warning
classes, change algorithms, or add dummy definitions to manufacture a clean run.
If a diagnosed false positive or necessary semantic change cannot be handled by
a sound scoped edit, retain it with the reason. Keep unrelated user hunks out.

## 4. Verify and stop accurately

Re-run both stages for every changed target under the same established context.
Compare source identities and the diagnostic ledger; do not use stale results
after concurrent changes. Fix new diagnostics caused by the edit, but stop a
non-progressing cycle with an explicit unresolved result rather than rewriting
the same docstring indefinitely.

Follow the layout-specific `elisp-conventions` checks: the managed package's
source-bound batch evidence, an unmanaged project's own checks, or the owning
workflow for non-package/test-only Elisp. Add focused behavior assertions when
bindings, definitions or executable code changed. Follow its supported
post-commit live-verification path when applicable; do not substitute a bare
`emacsclient -e` call or manually reload package code. A clean lint run is
diagnostic evidence, not proof of runtime behavior.

Inspect the final diff and index, and commit only owned authorized changes under
project policy. File selection alone does not isolate foreign hunks. Do not
push, publish or restart sessions as lint bookkeeping.

## 5. Report

Briefly state the checked scope, meaningful fixes and any remaining diagnostics
or incomplete checks. Give counts only from the recorded results. Distinguish
“no diagnostics in completed checks” from “all requested checks passed,” and
never describe intentionally skipped findings as fixed.
