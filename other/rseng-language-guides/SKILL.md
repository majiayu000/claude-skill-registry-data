---
name: rseng-language-guides
description: >-
  Covers language-specific research software practice: per-language
  conventions for Python, R, JavaScript/TypeScript, C/C++, Fortran, Rust and
  Bash - setup, development environments, style standards, packaging, testing,
  quality assurance, optimization, logging, documentation and dependency
  management. Use when the user asks which tools or conventions to use FOR A
  SPECIFIC LANGUAGE in research software (e.g. Python packaging, R style, C++
  QA, Fortran tooling, Rust starting points, shell scripting practice), or
  wants a language-by-language comparison.
license: CC-BY-4.0
metadata:
  version: 0.2.0
---

# Language-specific research software practice

The process skills in this pack are language-agnostic; this skill answers
language-SPECIFIC questions with per-language guidance. Each language
guide follows the same template -
introduction, information sources, setup, development environments,
style standards, packaging, testing, quality assurance, optimization,
logging, documentation, dependencies, starting points - so comparable
answers exist for every covered language.

## Current-tool quick reference per language

The strongest current stack per ecosystem (the pack-wide rule: best
current option, runner-up named, reason given - and these move, so
verify against the ecosystem when in doubt):

- Python: uv for environments/packaging (runner-up: pip+venv - uv is
  faster and lockfile-native), ruff as the single linter+formatter
  (replaces flake8/isort/black), pytest for tests, mypy for types,
  pyproject.toml as the one config home. Python 2 relics (2to3, six)
  and legacy tool chains belong to migration work, not new projects.
- R: usethis/devtools for package workflow, testthat for tests,
  lintr + styler for quality, roxygen2 for docs, renv for
  reproducible libraries; rOpenSci's guide is the community bar.
- C/C++: CMake as the build lingua franca, Catch2 or GoogleTest for
  tests, clang-tidy + clang-format for quality, sanitizers
  (ASan/UBSan) in CI, a package manager (vcpkg/Conan) over vendored
  sources.
- Fortran: fpm (Fortran Package Manager) for new projects, gfortran
  in CI, pFUnit for tests; modern-Fortran style over F77 habits, and
  interop via iso_c_binding when Python needs to call it.
- Julia: built-in Pkg with Project.toml/Manifest.toml, Test stdlib,
  JuliaFormatter; register in General only once the API settles.
- JavaScript/TypeScript: TypeScript by default for anything shared,
  vitest for tests, Biome as linter+formatter (runner-up:
  eslint+prettier - Biome is one fast tool), npm lockfiles committed.
- Bash: shellcheck non-negotiable, bats-core for tests when a script
  earns them - and past ~100 lines, prefer a real language
  (rseng-software-design's honesty about scripts).

These map the pack's practices INTO each ecosystem; the process
itself (testing discipline, packaging, CI shape) stays in the
process skills.

## How to use the guides

- Identify the language, open the matching page from references.md, and
  answer from its sections rather than from generic memory - the guides
  encode current, community-reviewed tool choices (for example the
  Python guide's Ruff-first style tooling, pytest, mypy/Pydantic typing
  and Sphinx/MkDocs documentation stack).
- For multi-language projects, apply each language's guide to its part
  and keep shared concerns (CI, licensing, citation) with the process
  skills.
- Where a language guide and a general skill overlap (testing,
  packaging, documentation), the general skill gives the WHY and the
  language guide gives the concrete WHAT for that ecosystem.
- The covered languages: Python, R, JavaScript/TypeScript, C/C++,
  Fortran, Rust, Bash - plus a technology overview page for adjacent
  topics.

## Choosing a language

For "which language should this project use", combine the guides'
starting-point sections with rseng-management-planning (technology
choice): weigh ecosystem fit for the research domain, team experience,
and long-term maintainability over micro-benchmarks.

## Working with this skill

The generated references.md beside this file lists the source material
and pointers:

- references.md - verified Learn more pointers


Learn more (verified):
  - https://peps.python.org/pep-0008/ - PEP 8 style guide for Python code
  - https://style.tidyverse.org - Tidyverse style guide for R
  - https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines -
    C++ Core Guidelines
  - https://doc.rust-lang.org/book/ - The Rust Programming Language book
  - https://fortran-lang.org/learn/ - Fortran-lang community
    learning resources

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-code-quality - linter and formatter per ecosystem
- rseng-dependency-management - verifying current ecosystem tooling
- rseng-management-planning - language choice for new projects
- rseng-notebooks - Python/Julia notebook practice
- rseng-project-scaffolding - language templates at kickoff
- rseng-testing - per-language test framework choice

<!-- related-skills:end -->
