---
name: document-elisp-extras
description: Audit, create, or refresh documentation for all Emacs extras packages in the dotfiles repo. Use when the user asks to document every extras package, fill missing extras docs, refresh outdated extras docs, check extras documentation coverage, or bring emacs/extras/doc up to date with emacs/extras sources.
---

# Document extras packages

Inventory the requested extras scope and compare each source with its Org manual.
A coverage/audit-only request authorizes a report, not manual edits, generated
Texinfo writes or commits. A request to create, fill or refresh docs authorizes
those scoped documentation changes. Do not rewrite source behavior to match prose.

Use `document-elisp-package` for documentation style and source analysis. Resolve
and read its actual catalog path for the active runtime before judging quality;
an `@path` string is not a portable automatic import. This skill coordinates the
batch, not a substitute set of documentation conventions.

## Scope and preparation

- Use `document-elisp-package` directly for one package, and `generate-readme` for
  GitHub Markdown from an existing Org manual. Do not start lint/release workflows
  merely because source or generated docs are inspected.
- Resolve the canonical dotfiles tree through `dotfiles-context`. Sources are
  top-level `emacs/extras/*.el`; manuals and tracked Texinfo live in
  `emacs/extras/doc/`. Use absolute quoted paths or establish the repository root
  before relative commands. Do not operate on an Elpaca mirror by accident.
- Respect an explicitly narrower package list or missing-only mode. Broader
  non-extras batches need a named scope, not an inferred home-directory scan.
- Inspect repository instructions, working tree and index. Preserve unrelated
  changes and check for unsaved manual/source buffers before disk edits. An
  inaccessible live editor is not proof its buffers are clean.
- Inspect the existing export policy in `emacs/extras/doc/.dir-locals.el` and its
  `org-extras-export-manual-to-texinfo` implementation. Do not enable arbitrary
  local evaluation or load all extras merely to export a manual.

## 1. Inventory and classify

Every top-level source file, including `paths.el` and names without `-extras`,
maps to `doc/BASENAME.org`. Exclude nested tests/builds from this batch, not from
some separate broader request. Build an explicit deterministic list from the
actual tree, including relevant untracked files; do not rely only on Git's index.
Use `rg --files --hidden --no-ignore` with a top-level path filter or an equivalent
filesystem enumeration. If a source is a symlink, inspect its canonical ownership
and report it explicitly rather than silently omitting or following it outside scope.

Record each package as missing, stale, current, excluded by request, or unresolved.
Presence and timestamps alone do not establish freshness. Report manuals without
a matching source separately: they may be topical documents or renamed packages,
not files to delete automatically.

For every included existing manual, compare structure, public surface and
behavior with the actual source. Missing-only requests need not rewrite current
manuals, but still account for every inventory entry.

## 2. Analyze source and documentation

Read the complete package source and existing manual before revising it. Follow
relevant callers and configuration examples only as needed to verify claims.
Do not evaluate the package just to discover its API; initialization can have
side effects or depend on the user's live configuration.

A search for `defun`, `defcustom`, `defvar` and `defconst` is only a starting
point. Include public macros, `cl-defun`, `defsubst`, modes, aliases, groups and
generated/conditional definitions where relevant. Check actual interactive forms
before classifying commands, including command aliases and generated mode commands.
Do not infer public status solely from a regular expression or name: `--`
normally marks internals, while documented compatibility aliases may remain public.
A configuration-only package may have no commands; document its actual options
and setup rather than inventing commands to fill a template.

Compare defaults, signatures, side effects, dependencies, hooks/advice, examples,
renamed/removed symbols and behavior changes. Preserve stable anchors and existing
useful explanations. Resolve misleading prose from source evidence; flag uncertain
contracts instead of inventing documentation. If source itself appears defective,
report it separately rather than silently fixing code under documentation authority.

Examples from `emacs/config.org` may depend on private paths/accounts or local
helpers. Explain required context and sanitize public examples; do not copy
credentials or personal data into tracked manuals.

## 3. Process one owned package at a time

For authorized edits, create missing manuals or refresh stale ones using
`document-elisp-package`; leave genuinely current docs alone. For audit-only mode,
record evidence and the recommended work without editing.

Use a bounded worker pool when useful, with exclusive ownership of each source/
manual pair. Every worker must read the documentation instructions and its actual
source/manual, preserve foreign edits, and return status plus evidence. The
coordinator owns shared files, reconciliation and commits unless ownership is
explicitly assigned. Do not let workers edit shared indexes or commit another
worker's partial changes.

When the user requires strict sequential processing, finish and verify one
package before starting the next; parallelism is not a reason to violate that
order. Without workers, follow the same per-package inventory and completion rules.
Re-check source revisions before accepting a worker result or committing prose.

## 4. Verify changed manuals

- Re-read each changed manual against source. Check required front matter,
  `CUSTOM_ID` anchors, index entries and the final Indices section under the
  loaded package-documentation rules. Check duplicate/broken anchors and links,
  not just the presence of marker strings.
- Inspect export-affecting includes, setup files, macros and source blocks.
  Do not execute embedded code or arbitrary local variables as a side effect.
  Keep scratch export/check outputs outside Drive; only intended tracked manual
  artifacts belong in `emacs/extras/doc/`.
- Export to an explicit reviewed `.texi` destination. The current save wrapper
  binds `org-export-preserve-breaks` to nil and `org-export-with-title` to t.
  Supply those defaults for direct exports and verify the actual output path; do not
  assume `#+export_file_name` produces the sibling file you meant to review.

For a direct export after inspecting the manual, substitute exact absolute paths:

```sh
emacs --batch -Q \
  --eval "(setq enable-local-variables nil enable-local-eval nil)" \
  --visit "/ABS/DOTFILES/emacs/extras/doc/PACKAGE.org" \
  --eval "(progn (require 'ox-texinfo) (let ((org-export-use-babel nil) (org-export-allow-bind-keywords nil)) (org-export-to-file 'texinfo \"/ABS/OUTPUT/PACKAGE.texi\" nil nil nil nil '(:preserve-breaks nil :with-title t))))"
```

Use a private outside-Drive output for diagnostic exports; for an authorized
tracked update, choose the exact sibling `.texi` path. This command does not load
the user's initialization or execute Babel blocks. It does not make arbitrary
Org export extensions safe, so inspect the input and required dependencies first.
File-level export options can override these defaults. Check conflicting
`#+OPTIONS` settings rather than assuming this command forces the final policy;
correct them only within authorized manual edits, then inspect the result.

A save in live Emacs is an alternative only when the correct buffer, hook,
unsaved state and resulting artifact are verified. No restart or signal is
authorized merely to make that path available. Export success proves format
generation, not factual accuracy; inspect the changed Texinfo, title, paragraph
breaks, node links and index entries. Use available Texinfo validation in a
disposable outside-Drive location when relevant; report missing tooling honestly.

## 5. Commit and reconcile

After each package is verified, commit its logical owned documentation change
immediately under repository policy. Use `PACKAGE: create documentation` or
`PACKAGE: update documentation`. Stage only its reviewed Org/Texinfo files, and
preserve pre-existing index entries rather than including them in a broad commit.
Do not push, release or rewrite unrelated source/configuration.

Reconcile the complete inventory: created, refreshed, already current, excluded
by the request, and unresolved. A failed export or unreadable source is not a
completed package. A second comparison should find no undocumented changes
within the completed scope; do not use cosmetic churn to manufacture activity.

## Final response

Report concise counts and material changes, relevant export/accuracy gaps,
commits and exact unresolved packages. For audit-only mode, report coverage and
recommendations without claiming manuals were created or refreshed.
