---
name: rseng-code-quality
description: >-
  Covers writing readable research code and structuring software projects:
  naming, formatting, style guides, linters and formatters, pre-commit hooks,
  modular design, and a conventional directory layout with top-level metadata
  files. Use when the user asks how to make code readable or clean, pick or
  enforce a style guide, set up linting/formatting or pre-commit, name
  variables and functions, organise a repo, or decide where files and data go.
  For generating a new project from a maintained template see
  rseng-project-scaffolding; for quantitative complexity and duplication
  measurement see rseng-software-metrics; for architecture-level structure see
  rseng-software-design.
license: CC-BY-4.0
metadata:
  version: 0.2.0
---

# Readable code and project structure

Use this skill when writing or reviewing research code for readability, or
when laying out a project's directories. Both goals serve the same end:
code is read far more often than it is written (a commonly cited read/write
ratio is 7:1), so anything that helps a future reader - including the
original author months later - directly improves reusability, the "R" in
the FAIR research software principles.
Favour conventions others already recognise over clever, project-specific
inventions.

## Make code readable

Apply these rules when authoring or reviewing code:

- Use descriptive names for variables, functions, classes, and modules
  that explain their purpose. Avoid single-letter names outside tight
  loops or well-known math notation.
- Format consistently: consistent indentation and spacing throughout.
  Consistency within a project or module matters more than any global
  ideal - when joining existing code, adopt the conventions already in
  place rather than imposing your own.
- Separate code into sections with blank lines (between classes,
  functions, logical blocks) so structure is visible at a glance.
- Keep lines short. Prefer many short lines over few long ones - blocks
  that are horizontally short and vertically long are easier to scan.
- Use indentation to show hierarchy and mark the beginning and end of
  control structures.
- Add type annotations (type hints) for untyped or dynamically typed
  languages such as Python or JavaScript, and validate them with a type
  checker (e.g. mypy for Python). Type checking catches faulty assumptions
  as well as faulty annotations.
- Write informative comments and docstrings that convey intent and
  context - what the code is for and why - not a restatement of the
  syntax. Comment where logic is not self-evident.

## Follow a style guide

- Adopt the community-standard style guide for the language rather than
  inventing one: PEP 8 for Python, the Google R style guide for R; Google's
  style guides cover Python, Java, R, C++, and Shell.
- A style guide is a shared set of conventions so everyone's contributions
  look similar. Consistency across the project is the point.
- When contributing to an existing project, match its existing style even
  if it differs from your preference.

## Automate style and quality checks

Do not enforce style by hand - let tools do it:

- Run an auto-formatter to apply style mechanically (e.g. Black for Python).
  This removes formatting from code review entirely.
- Run a linter - static analysis that flags inconsistencies, stylistic
  errors, suspicious constructs, and some real bugs (e.g. Pylint for
  Python).
- Lean on editor/IDE support: VS Code, PyCharm, RStudio, and Eclipse can
  check conformance as you type, warn on deviations, and often autocorrect.
- Wire formatters and linters into pre-commit hooks and CI so every change
  is checked automatically, not just when someone remembers.

## Pre-commit: the guardrail framework

The pre-commit framework runs the checks automatically at commit
time, from one versioned config - the difference between "we have a
linter" and "nothing unlinted lands":

- Anatomy: a `.pre-commit-config.yaml` at the repo root lists hook
  repositories PINNED to revisions; start from the basics (trailing
  whitespace, end-of-file, merge-conflict markers, large-file guard),
  add the ecosystem's linter/formatter (ruff for Python), a secret
  scanner (rseng-security), and project-specific `local` hooks where a
  custom check earns automation.
- Adoption on an existing repo: install the hooks, then run
  `pre-commit run --all-files` ONCE in its own commit - a dedicated
  formatting commit keeps blame readable (the same reasoning as
  avoiding repo-wide reformats in rseng-legacy-code).
- Keep hooks fast: commit-time checks have a seconds budget - slow
  checks (test suites, type-checking large trees) belong in CI, not
  in the hook, or people bypass hooks entirely and the guardrail is
  gone.
- Update deliberately: `pre-commit autoupdate` bumps pinned hook
  revisions - treat it like any dependency update, on a cadence with
  green tests (rseng-dependency-management).
- SKIP honestly: skipping a hook (SKIP=<id>) is legitimate when the
  hook itself is broken or inapplicable to the change - record why
  in the commit; skipping to silence a real finding just moves the
  failure to CI or review.
- Mirror in CI: run the same hooks in the pipeline
  (`pre-commit run --all-files` as a CI step or pre-commit.ci) so a
  locally bypassed hook (--no-verify) cannot land unchecked
  (rseng-ci-cd) - local hooks are convenience; CI is enforcement.

## Write modular, reusable code

- Split code into small functions that each achieve a single, clear
  purpose - easier to read, test, and reuse.
- Group related functions into reusable libraries and packages.
- Reach for established design patterns for common, well-defined problems
  instead of reinventing a solution; this saves time and raises quality.
- Prefer existing, well-tested libraries for common tasks (e.g. reading and
  writing standard data formats) over bespoke, error-prone code.

## Structure the project directory

A clear, conventional layout lets people (and you) locate things fast, keep
code, config, and data separate, isolate issues quickly, and reproduce
results - especially valuable for long-term or collaborative work. There is no single official standard,
but the following is widely understood.

Put everything for the project in a single, meaningfully named directory.

Keep auxiliary information and metadata at the top level so others can tell
what the project does and how to reuse it:

- `README` - what the project is, how to install and run it, how to
  reproduce results.
- `LICENSE` - the reuse terms.
- `CITATION.cff` - how to cite the project (Citation File Format).
- `codemeta.json` or a similar metadata standard - machine-readable
  software metadata.

Organise the rest into sub-directories labelled by content type:

- `src/` (or `code`, `scripts`) - source code.
- `data/` - data, with raw kept separate and never modified: e.g.
  `data/raw`, `data/clean`, `data/processed`. This prevents overwriting or
  losing the original.
- `results/` - analysis outputs, tables, summary statistics.
- `figures/` (or `fig`) - generated plots and figures (or fold these into
  `results/`).
- `doc/` - documentation and guides.
- `papers/`, `presentations/`, or `references/` - literature; consider
  keeping these in a separate project so papers do not mix with a reusable
  software package.
- Add a nested `README` or `LICENSE` inside a sub-directory when its terms
  differ (for example, code and data licensed differently).

## Name files and directories consistently

- Use standard, self-explanatory directory names (as above).
- Avoid spaces and special characters - they break tools; use underscores
  or hyphens and stay consistent.
- Name files to reflect their contents; let version control track versions
  rather than encoding `_v2`, `_final` in filenames.

## Version-control the project

- Put the whole project under version control in its own repository; at
  minimum version-control code and data sub-directories, plus anything
  written by hand (docs, manuscripts) rather than generated.
- Untrack files too large or too sensitive to expose (use `.gitignore` in
  Git); never version-control passwords or secrets.
- Use tags/releases to mark specific versions (a journal submission, a
  dissertation version) instead of proliferating dated filenames.

## Scaffold new projects with tooling

- For Python, a src-layout with `src/your_package/`, `tests/`,
  `pyproject.toml`, `README`, and `.gitignore` is the common modern shape.
- Poetry manages dependencies, virtual environments, versioning, and
  publishing from a single `pyproject.toml`, and scaffolds a new project
  directory; it works well with the recommended src layout.
- Project templates/skeletons enforce a standardised layout and modern
  tooling, cutting setup time and keeping teams consistent.

A concrete reference stack (as encoded by the NLeSC python-template;
see rseng-project-scaffolding): ruff as the single linter, formatter and
import sorter; EditorConfig for cross-editor consistency; SonarCloud
for hosted static analysis; and first-class type checking with Pyright
(or Mypy) - treat type checks as part of linting, not an optional
extra.

## Working with this skill

The generated references.md beside this file lists the source
material and pointers:

- references.md - verified Learn more pointers


Learn more (verified):
  - https://peps.python.org/pep-0008/ - PEP 8 style guide for Python code
  - https://google.github.io/styleguide/ - Google style guides for
    many languages
  - https://docs.astral.sh/ruff/ - Ruff Python linter and formatter
  - https://pre-commit.com - pre-commit hook framework
  - https://editorconfig.org - consistent editor settings across tools


<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-documentation - docstrings and README quality
- rseng-fair-software - readability serves reusability
- rseng-language-guides - per-language style and tool choice
- rseng-legacy-code - repo-wide reformat cautions
- rseng-project-scaffolding - templates encode this tooling baseline
- rseng-software-metrics - quantifying complexity and duplication

<!-- related-skills:end -->
