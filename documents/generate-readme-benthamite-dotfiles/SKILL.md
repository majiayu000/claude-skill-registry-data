---
name: generate-readme
description: Generate or update a GitHub-facing README.md for an Emacs Lisp package from its Org manual. Use when the user says "generate readme", "create readme", "update readme", "readme from manual", or wants a concise Markdown README for an Elisp package. Do not use for general project README writing or for packages without an Org manual; use document-elisp-package first when the manual is missing.
---

# Generate README.md from org manual

Create or update a `README.md` for an Emacs Lisp package. The README is a lightweight GitHub-facing introduction, distinct from the org manual which is the comprehensive reference.

## Workflow

1. Distinguish a file update from a draft, review, or recommendation. Read-only requests do not edit, rename, export, or commit project files. Verify the package and manual prerequisites before writing `README.md`.
2. Read the org manual, the main `.el` file, and any existing `README.md` thoroughly enough to distinguish canonical manual content from README-specific material.
3. Generate or update `README.md` using the structure below, preserving accurate repo-specific content from an existing README.
4. Verify the resulting README and the exact owned diff before reporting completion or committing. README generation does not authorize manual reorganization, package installation, a release, or publication.

Read applicable project instructions and inspect the working tree/index and any unsaved source/document buffers before edits. Preserve foreign changes. Use `dotfiles-context` for extras or Elpaca-managed package routing. Read source/manual text without loading the package, evaluating Org Babel or honoring file-local evaluation/export directives.

## Prerequisites

Before doing anything, verify both conditions. If either fails, stop and explain why.

### 1. Elisp package

Resolve the intended package and canonical source files from package headers, packaging metadata, documentation and provided features. A valid package header includes a `;;; filename.el --- description` line, but a test or vendored library is not the target merely because it has one. Distinguish checkout/repository name, package ID and main library/feature; do not choose by directory basename or the first `.el` file. Resolve genuine multi-package ambiguity before writing.

### 2. Org manual

Use the maintained Org manual, normally `README.org`, honoring an explicit target or established layout such as `doc/manual.org`. This follows `document-elisp-package`, which preserves existing manual paths.

Preserve a case-variant rather than renaming it as a prerequisite. Inspect exact Git spelling, symlinks and destination collisions before creating `README.md`. A requested rename needs collision/inbound-link/build-reference checks and, where necessary, a safe two-step case-only Git move.

If no Org manual exists, stop README generation and identify that prerequisite. Use `document-elisp-package` only when creating the manual is authorized; do not invent one or implicitly add a second writing task.

## Existing README.md

If a `README.md` already exists and the user explicitly asked to create, update, regenerate, or refresh it, proceed without another confirmation. Exploratory requests do not replace it; ask only when a genuine unresolved choice prevents the requested work.

Before editing an existing README, inspect it for README-specific material: badges, screenshots, CI status, contribution links, license notes, project caveats, installation variants, or historical context. Preserve accurate, useful material and project-owned/generated regions. Absence from the manual or one current source file is not evidence of staleness. Reconcile discrepancies against supported versions; preserve or flag uncertain historical guidance rather than silently deleting it.

Check competing README locations before claiming the landing page will change: GitHub prioritizes `.github`, then the repository root, then `docs`. Creating root `README.md` alone is not proof of its selection. Preserve the manual and link to its actual path. See [GitHub's README and relative-link rules](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes).

## Generating the README

Read the org manual, the main `.el` file, and the existing README if present. Then produce a `README.md` with the following structure.

### Structure

#### 1. Title and tagline

```markdown
# `package-name`: One-sentence description from the package header
```

#### 2. Overview

A concise summary, sized to the package rather than a paragraph quota, explaining:

- What the package does and what problem it solves.
- Who it is for (target audience, assumed context).
- Key capabilities, organized thematically — not an exhaustive list of every command, but enough to convey scope.

Draw from the manual's Overview section but rewrite for a reader who is deciding whether to install the package. Be concrete: mention specific workflows, not just abstract features.

#### 3. Screenshots or demos

Inspect screenshots/GIFs in relevant directories and existing README/manual references. Include useful, intended-publication assets with descriptive alt text; do not publish private screenshots or fetch/generate new assets implicitly:

```markdown
## Screenshots

![Description](screenshots/example.png)
```

If none are appropriate, omit the section. Rebase paths from the manual directory to the README directory, and convert Org links/anchors to valid Markdown rather than copying `file:`, `id:` or Org search suffixes literally.

#### 4. Installation

```markdown
## Installation
```

Present supported installation methods as alternatives, not steps to combine. Prefer documented recipes. These templates assume the package and provided feature agree and the repository has a conventional layout:

- **use-package `:vc`** (built into Emacs 30+; `package-vc-install` itself is available in Emacs 29):

  ```emacs-lisp
  (use-package PACKAGE
    :vc (:url "https://github.com/OWNER/PACKAGE"))
  ```

- **Elpaca**, with the manager installed and `elpaca-use-package-mode` enabled:

  ```emacs-lisp
  (use-package PACKAGE
    :ensure (:host github :repo "OWNER/PACKAGE"))
  ```

- **straight.el**, with its `use-package` integration loaded:

  ```emacs-lisp
  (use-package PACKAGE
    :straight (:host github :repo "OWNER/PACKAGE"))
  ```

Bind the publication/install repository using existing canonical links, package metadata and remotes together. A fork named `origin` is not automatically the intended source. Inspect remote identity without disclosing credential-bearing URLs; never copy credentials, SSH aliases or private local paths into public snippets or infer public accessibility from a remote alone. If uncertain, retain a verified existing recipe or state the missing identity instead of inventing a public URL.

Adapt manager-specific package name, main file, subdirectory/file selection, build requirements and revision when feature/package/repository identities differ. Do not advertise generic monorepo recipes without verifying the layout. Match quick-start APIs to the version the recipe installs: `use-package :vc` can default to the last release rather than current HEAD. Prefer a supported release; select another revision explicitly only when justified. Consult primary docs for unfamiliar syntax: [use-package](https://www.gnu.org/software/emacs/manual/html_node/use-package/Installing-packages.html), [Elpaca](https://github.com/progfolio/elpaca/blob/master/doc/manual.md), [straight.el](https://github.com/radian-software/straight.el#integration-with-use-package).

List versioned `Package-Requires` dependencies plus evidenced runtime tools/data and optional feature requirements. A missing or conflicting header is an evidence gap, not permission to invent requirements.

Also mention the minimum Emacs version from the `Package-Requires` header. If the minimum is older than Emacs 30, present the `:vc` example as the Emacs 30+ built-in option rather than implying every supported Emacs version has it.

#### 5. Quick start

```markdown
## Quick start
```

Give the smallest complete configuration and actual first command or library call. Verify feature names, options, arguments, autoload/require behavior and prerequisites. Respect Elpaca's asynchronous activation (use the documented activation/configuration point rather than immediate top-level calls). Do not omit essential tools/data/account setup to fit 5–10 lines or promise completion in under a minute. Never include real secrets.

#### 6. Documentation

```markdown
## Documentation

For detailed usage and reference documentation, see the [manual](README.org).
```

Replace the example link with the actual manual path and describe its verified coverage; preserve stable section targets.

#### 7. Roadmap (if applicable)

Preserve accurate existing README roadmap content. If the manual owns a roadmap, link to it or summarize without deleting the source. Checklist form may be useful; preserve substance, nested details and status:

```markdown
## Roadmap

- [ ] Planned feature one
- [ ] Planned feature two
- [x] Completed feature (keep if recently completed and informative)
```

If neither source has roadmap content, omit this section.

Move the roadmap into the README as its sole home only when that migration is explicitly requested. Inspect the exact authorized section, inbound links, stable anchors and generated-document requirements before removal; do not remove every heading matching a generic roadmap name.

#### 8. Contributing and license (if applicable)

Use existing project evidence, including nonstandard files such as `CONTRIBUTING.org` or `COPYING` and documented license statements. Preserve accurate existing links; do not invent licensing or erase supported information merely because a filename differs.

### Style guidelines

- Render package names in backticks in ordinary prose and titles; preserve URL/image/other markup.
- Write in a direct, informative tone. Second person ("you") is fine.
- Prefer short paragraphs and bullet lists over walls of text.
- Use fenced code blocks with `emacs-lisp` language tag for Elisp.
- Do not duplicate the full manual content — the README is an entry point, not a mirror.
- Do not include badges unless the repo already has CI or other badge-worthy infrastructure.
- Do not add a table of contents — GitHub renders one automatically for markdown files.
- Apply `humanize` to final public-facing prose, or `personalize` when the user is personally authoring it. Neither may change technical meaning.

## Verification and closeout

Before finishing:

- Re-read the generated README and any separately authorized manual edits at their actual paths.
- Check local links/images with exact Git spelling, relative base and anchors. Targets must exist in the intended publishable tree, not merely as ignored/untracked files, outside-repository symlink targets or private local paths. Check intended new assets are included.
- Corroborate code examples against actual symbols, recipes, versions and prerequisites. Reader-only syntax checks must disable reader evaluation. Do not evaluate or byte-compile installer forms: even compilation can install packages. Any installation, cloning, network or user-state acceptance needs appropriate authority/isolation; syntax checks alone do not prove runtime success.
- Inspect Markdown rendering or a suitable preview for changed images, tables, lists and fences. Local preview does not prove GitHub's actual landing-page selection.
- Check that the README has no placeholder owner, package, screenshot, or command names.
- Unless separately authorized, verify the manual is unchanged. For requested migrations, verify only the approved section moved and follow the manual workflow for stable links/generated artifacts. A repeated generation should not churn valid content.
- Run `git diff --check`.
- Inspect `git status --short`, the exact diff and current index; stage only owned hunks. Do not sweep in pre-existing README/manual edits or unrelated staged files.

Commit requested durable file changes using the repository's conventions; do not push or publish. Draft/review requests end without project mutations or commits. Report the artifact and only material verification gaps, distinguishing checks actually run from unexecuted installation/runtime claims.
