---
name: document-elisp-package
description: Create or update an Org manual for an Emacs Lisp package in the Denote manual style. Use for documenting Elisp packages or emacs/extras; use generate-readme for Markdown README generation alone.
---

# Document an Elisp package

Create or update an Org manual with the usage context and reference detail of
[Protesilaos Stavrou's Denote manual](https://protesilaos.com/emacs/denote).
The organization and metadata below are local conventions inspired by that
manual, not a claim that Denote requires this exact template.

**Dotfiles monorepo override:** In `~/My Drive/dotfiles/`, documentation for `emacs/extras/<package>.el` goes in `emacs/extras/doc/<package>.org` (one file per package), NOT `README.org`. When invoked for a package under `emacs/extras/`, use that path instead of the standalone-repo convention below.

For standalone packages, prefer an established manual path and the user's explicit target; use root `README.org` for a new manual when no convention exists. Do not force a rename, case-only move or consolidation of an existing multi-manual layout as an incidental documentation change. If a rename is actually requested, inspect collisions and inbound/build references, preserve history and use a safe two-step case-only move when the filesystem requires it. Cover the package's supported source files thematically, not vendored dependencies, unrelated libraries or tests.

If several existing manuals could be authoritative, inspect project references
and export configuration to resolve the target. If that evidence cannot settle
it, ask for the missing path choice rather than rewriting every candidate.

## Scope boundary

Use this skill for Org manuals that explain an Emacs Lisp package's user-facing behavior, customization surface, and extension points. It applies both to standalone package repositories and to dotfiles extras packages under `emacs/extras/`.

Do not use this skill when the user only wants a Markdown `README.md`; use `generate-readme` after an Org manual already exists. Do not use it to document every extras package in one pass; use `document-elisp-extras`. Do not use it for compiler/checkdoc cleanup without a documentation request; use `lint-elisp`.

## Workflow

1. Resolve the canonical repository, relevant source files and actual manual/build layout. Use `dotfiles-context` for extras or Elpaca-managed package routing. Read applicable instructions and inspect working tree/index plus unsaved source/manual buffers before disk edits. Preserve foreign changes. A review-only request ends with evidence and recommendations, not edits, renames or exports into the repository.
2. Read the complete supported source surface before writing. Inventory options, faces, variables/keymaps, commands, public functions/macros, modes and compatibility aliases, including conditional or generated definitions. Verify actual public/interactive status; a name regex alone is not authority. Do not load/evaluate the package to enumerate it: initialization and macros can have effects.
3. Compare with the existing manual and supported versions. Record added, renamed, retired and behavior-changed symbols and concrete prose gaps. Keep supported compatibility/migration explanations; absence from one current source file is not sufficient reason to erase historical guidance.
4. For authorized documentation updates, edit in place, preserve accurate prose and stable anchors, and fix concrete gaps. Do not expand concise sufficient sections just to meet a length target. Recheck source changes before accepting worker output or committing. Report source defects separately instead of changing code to fit the manual.
5. Handle Texinfo export setup only where this skill says it applies. Avoid creating broad repository-level hooks in the dotfiles monorepo.
6. Verify the manual against the source and report the changed files, verification performed, and any definitions intentionally left undocumented. Commit changes only when the user requested commits or the local repository conventions require them.

## Analyzing the source

Extract all public definitions from the package's `.el` source file(s):

- `defcustom` (user options)
- `defface` (customizable faces)
- `defvar`, `defconst`, `defvar-keymap` and groups (public variables/keymaps and customization organization)
- Interactive `defun`, `cl-defun`, and mode forms such as `define-minor-mode` or `define-derived-mode` (commands)
- Public non-interactive `defun`, `cl-defun`, `defsubst`, `defmacro` and `cl-defmacro`
- Public aliases, obsolete aliases and generated/conditional interfaces still supported by the package

In the usual naming convention, `package--helper` is internal: the marker is the double hyphen after the package name, not a literal prefix at the start of the symbol. Treat naming as evidence alongside callers, docstrings and supported contracts. Exclude test helpers and private internals from required reference coverage, but retain necessary implementation context or documented extension points explicitly.

If documentation already exists, perform a structural diff: identify definitions that are added, removed, or renamed relative to what the `.org` file documents. Also check whether existing descriptions still accurately reflect the current docstrings and behavior, and whether the documentation meets the quality standard below.

When updating existing docs:

- Add documentation for new items in the appropriate section.
- Remove obsolete current-API claims while preserving useful supported-version and migration information.
- Update descriptions for items whose behavior has changed.
- Rewrite terse sections to meet the quality standard.
- Ensure the Overview accurately reflects the package's current feature set.
- Preserve any existing content that is accurate and well-written.

## Documentation format

### Front matter

Preserve established author, license, attribution and publication metadata. The
following defaults are for a new manual owned/authored by Pablo; do not assign
his identity to a third party's manual automatically. For prose he will publish
as his own, use `personalize` while respecting this technical documentation style.
Do not copy private account details, credentials or machine-specific configuration
into public examples. Placeholders must be clearly marked and explained.

```org
#+title: PACKAGE-NAME: Short description
#+author: Pablo Stafforini
#+email: pablo@stafforini.com
#+language: en
#+options: ':t toc:t author:t email:t num:t
#+startup: content
#+export_file_name: PACKAGE-NAME.info
#+texinfo_filename: PACKAGE-NAME.info
#+texinfo_dir_category: Emacs misc features
#+texinfo_dir_title: Display Name: (PACKAGE-NAME)
#+texinfo_dir_desc: Short description
```

Follow the front matter with a one-line introduction:

```
This manual describes the features and customization options for =PACKAGE-NAME=.
```

### Section structure

Every doc file must include these sections in this order. Omit a section only if the package has no items of that type.

1. `* Overview`
2. `* User options` — for `defcustom` variables
3. `* Faces` — for public `defface` definitions
4. `* Variables and keymaps` — for public non-option state/keymaps users can use
5. `* Commands` — for interactive functions and modes
6. `* Functions` — for public non-interactive functions and macros worth documenting
7. Integration-specific sections — if the package integrates with other packages in notable ways (e.g., `* Embark integration`, `* Transient menus`)
8. `* Indices` — always last

Preserve an established equivalent organization when rearranging it would break
useful navigation. A configuration-only package need not invent commands. Group
metadata belongs with its relevant options rather than an artificial reference entry.

For a new Indices section, use the following function and variable index layout.
Preserve established stable IDs and equivalent index organization in existing
manuals; do not break incoming links just to copy these default IDs.

```org
* Indices
:PROPERTIES:
:CUSTOM_ID: h:indices
:END:

** Function index
:PROPERTIES:
:INDEX: fn
:CUSTOM_ID: h:function-index
:END:

** Variable index
:PROPERTIES:
:INDEX: vr
:CUSTOM_ID: h:variable-index
:END:
```

### Subsection organization

Group related items under thematic subsections (`**`, `***`). Choose headings that describe the *purpose* or *workflow*, not the symbol name:

- GOOD: `** File handling and attachment`
- GOOD: `** Searching for entries on external websites`
- BAD: `** ebib-extras-open-file-dwim`
- BAD: `** Miscellaneous`

Individual items (a single command or option) get their own heading only when they need substantial documentation (multiple paragraphs, examples, etc.). Otherwise, group several related items under one subsection.

### PROPERTIES drawers

Every heading at every level must have a `:PROPERTIES:` drawer with `:CUSTOM_ID:`:

```org
* Commands
:PROPERTIES:
:CUSTOM_ID: h:commands
:END:

** File handling
:PROPERTIES:
:CUSTOM_ID: h:file-handling
:END:
```

Preserve existing stable IDs even when headings are renamed. New IDs must be
unique within the manual; check every internal link after adding or moving them.

Convention for new CUSTOM_ID values:

- Top-level sections: `h:overview`, `h:user-options`, `h:faces`, `h:commands`, `h:functions`, `h:indices`
- Thematic subsections: `h:DESCRIPTIVE-SLUG` (e.g., `h:file-handling`, `h:entry-processing`)
- Individual symbols (when they have their own heading): `h:SYMBOL-NAME` (e.g., `h:ebib-extras-download-use-vpn`)

### Texinfo index entries

Place these directives immediately after the `:END:` of the PROPERTIES drawer, before the prose:

- `#+findex: FUNCTION-NAME` for every documented function, macro, mode command and command alias.
- `#+vindex: VARIABLE-NAME` for every documented variable, user option, and face.

When multiple functions are documented under one subsection, place all their `#+findex:` entries together at the top of that subsection.

### Cross-references

Link liberally within the same doc file using Org internal links:

```org
This function uses ~ebib-extras-get-file~ internally ([[#h:file-handling][File handling]]).
```

Add a cross-reference when it helps navigation, especially at the first meaningful mention or between related workflows. Avoid repeated links that add no information. Every target must exist and identify the intended section; a formatting example is not evidence that a target exists in the real manual.

For references to other packages, use verbatim markup: `=PACKAGE-NAME.el=`.

### Markup conventions

- `~tildes~` for Lisp symbols: function names, variable names, package names, keywords, nil, t.
- `=equals=` for literal values: file paths, key sequences, format strings, literal strings.
- `*bold*` sparingly, for emphasis in important notes.
- `/italic/` rarely, only for introducing technical terms.

## Quality standard

The documentation must match the rigor of Protesilaos Stavrou's Denote manual. The key attributes are:

### Overview

Do not merely list features. The overview should:

- Explain the *purpose* of the package: what problem it solves and why it exists as a separate file.
- Describe its relationship to the underlying Emacs package it extends (e.g., "=ebib-extras.el= extends =ebib=, the Emacs BibTeX database manager").
- Mention key external dependencies.
- Provide a thematic map of capabilities organized by workflow, not just a flat bullet list.

### User options

Each `defcustom` must include:

- Its source-defined default, including a default expression when environment-dependent. Distinguish that from a current user's customized value; do not evaluate private configuration just to print it.
- The type of value it accepts (boolean, string, integer, list, choice, etc.).
- A clear explanation of what the option controls.
- *When* and *why* a user would want to change it from the default.
- How it interacts with other options or commands, if relevant.

### Commands

Each interactive command must include:

- A contextual explanation of *when* and *why* a user would invoke the command.
- The context in which it operates (e.g., "while in the Ebib index buffer", "with point on an Org heading").
- Its arguments, prefix argument behavior, and DWIM branches.
- What source evidence establishes about edge cases, errors, cancellation and side effects. For asynchronous work, distinguish starting a request from completion and state relevant callback/buffer assumptions; do not invent successful outcomes.
- Cross-references to related commands, options, and functions.

Do not merely paraphrase the docstring. Explain usage context and relationships
that the source, tests or maintained examples support. Sparse evidence is not
permission to invent a workflow, guarantee or edge-case outcome.

### Functions

Document public non-interactive functions and macros when they are:

- Useful for customization or hooks.
- Part of workflows that users might want to extend.
- Called by documented commands (helps the reader understand the architecture).

Private `package--helper` symbols do not require public reference entries. Mention internals only where needed to explain a supported contract, clearly labeled as implementation details; do not promote them to stable APIs.

For public macros, explain argument evaluation and binding/expansion semantics
where material; do not describe them as ordinary function calls. For public hooks
or mode interfaces, document arguments, locality and enable/disable effects from
the actual implementation.

### Prose style

- Write in a direct, informative, second-person tone. The Denote manual says things like "The user option ~denote-directory~ specifies..." — do the same.
- Explain *why* before *how*. Provide context before reference details.
- Use complete sentences. No telegram-style fragments.
- Prefer short paragraphs; use the space the explanation needs rather than padding every entry to a fixed count.
- Use Elisp code blocks (`#+begin_src emacs-lisp ... #+end_src`) when an example clarifies usage.
- Refer to Emacs commands in the standard way when mentioning interactive invocation: =M-x command-name=.
- When a command has a noteworthy implementation detail (e.g., uses `el-patch`, calls an external process, depends on a specific mode), mention it briefly — the reader should know what's happening under the hood without reading the source.

## Texinfo export and automation

Reuse the established export/build policy. A documentation request is not by
itself permission to install a repository-wide after-save evaluator. Do not add
or replace `.dir-locals.el` automatically. If export automation is explicitly
requested or required by repository policy, inspect existing settings, merge
without duplicate/shadowed alist entries, restrict it to the intended manuals
and owned outputs, and verify the actual save path before calling it active.
Do not install a lambda that blindly exports every Org file in the repository.

For dotfiles extras, keep the manual at `emacs/extras/doc/<package>.org` and use
the existing reviewed export path. The current save wrapper supplies title=t and
preserve-breaks=nil defaults; file-level options can override them. The paired
agent after-edit hooks generate owned sibling outputs without local/Babel
evaluation and explicitly refuse unsupported evaluation/include/raw-export forms.
A refusal is an export gap to investigate, not permission to bypass protections.

Before direct export, inspect includes, setup files, macros, file options and
destination directives. Disable file/directory-local evaluation before visiting
and Babel before export. Use an explicit reviewed output path. Do not follow
external data references, enable evaluation or install missing dependencies as
an implicit verification step. Keep scratch exports and Info validation outputs
outside Drive; only intentional tracked generated manuals belong in the repository.

After replacing placeholders with exact paths, a clean direct export is:

```sh
emacs --batch -Q \
  --eval "(setq enable-local-variables nil enable-local-eval nil enable-dir-local-variables nil)" \
  --visit "/ABS/SOURCE/MANUAL.org" \
  --eval "(progn (require 'ox-texinfo) (let ((org-export-use-babel nil) (org-export-allow-bind-keywords nil)) (org-export-to-file 'texinfo \"/ABS/OUTPUT/MANUAL.texi\" nil nil nil nil '(:preserve-breaks nil :with-title t))))"
```

This is for inspected input, not a sandbox for arbitrary Org export extensions.
Per-file options may override defaults; check the actual title, paragraph breaks,
node links and indexes. For an authorized tracked update, use the repository's
exact output naming convention; do not silently replace a configured package
Info basename with a README basename. The automatic hooks preserve validated
literal sibling basenames: `EXPORT_FILE_NAME` selects the Texinfo stem and
`TEXINFO_FILENAME` independently selects the Info name. Paths, ambiguous
declarations and unsupported names are refused explicitly; inspect that result.

## Verification

Reconcile each public inventory entry with the manual or a reasoned omission.
Check factual behavior, signatures/defaults, setup, examples, supported versions
and dependency requirements against source and authoritative APIs. Distinguish
read-through examples from safely executed examples. Do not call a shell/network/
editor example verified unless that exact authorized behavior was exercised.

Check unique/stable anchors, all internal links, index directives and the final
Indices section. Export changed manuals when tooling permits, then inspect the
actual generated content and use available Texinfo validation in a disposable
location. Export success establishes format generation, not prose correctness.
No active Emacs restart, global setting change or source execution is authorized
merely to obtain an export.

If verification is incomplete, state the exact gap. Do not assume an Org manual
requires loading its package: investigate the actual exporter dependency first.
Review the source/manual/generated diff and confirm no stale or unexpected output
was staged. Commit logical owned documentation changes according to the user's
request and repository policy, preserving unrelated index entries. Commit any
separately authorized automation change as its own verified logical change.

End with concise changed files, relevant verification, commits and unresolved
documentation gaps. For review-only work, distinguish recommendations from edits.

## Illustrative examples

These symbols and values are fictional examples of format and depth, not claims
about installed packages. Derive real names, defaults and behavior from the
package being documented. Cross-reference targets shown here belong in the
complete manual before these fragments are used.

```org
** Revisiting recent entries
:PROPERTIES:
:CUSTOM_ID: h:revisiting-entries
:END:

#+findex: sample-open-recent-entry
Use =M-x sample-open-recent-entry= to choose an entry from the recent-entry
list while working in a sample buffer. The command displays the chosen
entry without modifying its contents. With a prefix argument, it opens
the entry in another window.

The list is limited by ~sample-recent-entry-limit~
([[#h:recent-entry-limit][Recent-entry limit]]). If the list is empty,
the command reports that no recent entry is available.
```

```org
** Recent-entry limit
:PROPERTIES:
:CUSTOM_ID: h:recent-entry-limit
:END:

#+vindex: sample-recent-entry-limit
The user option ~sample-recent-entry-limit~ controls how many recent entries
are retained for ~sample-open-recent-entry~
([[#h:revisiting-entries][Revisiting recent entries]]).

The default is =20=. The value must be a positive integer. Increase it if
you regularly revisit older entries; a smaller value keeps the selection
list shorter.
```
