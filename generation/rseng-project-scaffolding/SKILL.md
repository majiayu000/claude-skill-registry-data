---
name: rseng-project-scaffolding
description: >-
  Covers starting research software projects from maintained templates and
  keeping them in sync: choosing a generator (Copier, cookiecutter),
  scaffolding a Python package, retrofitting template structure, pulling
  template upgrades into generated projects, and picking a pyproject build
  backend. Use when the user starts a new research software codebase, asks
  for a template or boilerplate, wants a src/ layout or pyproject.toml
  scaffold, mentions copier or cookiecutter, or chooses between setuptools,
  hatchling, poetry or PDM. For hand-rolled layout see rseng-code-quality;
  for the management side see rseng-project-kickoff.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Project scaffolding from templates

Starting from a maintained community template gives a research software
project the whole quality baseline - packaging, tests, CI, linting,
citation files, docs - in one step, encoded the way its community
actually practices it. The skill here is threefold: pick the right
generator, generate (or retrofit) honestly, and keep the project in
sync as the template evolves.

## Choosing a generator

- Copier: templates are versioned; `copier update` can replay template
  improvements into an already-generated project later. Prefer it when
  the template supports it - staying current is the hard part of
  template use, and Copier is built for it.
- cookiecutter: widest ecosystem of templates; generation is one-shot
  (no built-in update path), so treat the result as a starting point
  you own from day one.

Prefer a template maintained by a research software community over a
generic one: it will encode citation files, FAIR practices and
research-specific CI that generic templates omit.

## The NLeSC python-template (reference implementation)

The Netherlands eScience Center's Copier template
(https://github.com/NLeSC/python-template, Apache-2.0, actively
maintained) is a strong default for research Python packages:

```bash
pipx install copier
copier copy https://github.com/nlesc/python-template.git path/to/project
copier update                    # later: pull template improvements
```

- Three profiles: Minimum (essentials), Recommended (curated defaults),
  or fully custom - match the profile to the software tier (analysis
  code -> Minimum; shared tools -> Recommended).
- It can also retrofit structure onto EXISTING code: run `copier copy`
  into the existing directory and reconcile.
- What it encodes (Recommended): src/ layout, setuptools +
  setuptools-scm build backend, pytest with branch coverage, tox matrix
  following the SPEC 0 version policy (three most recent Python
  minors), ruff as single linter/formatter/import-sorter, type checking
  (Pyright default, Mypy optional), pre-commit, EditorConfig,
  CITATION.cff plus a cffconvert CI check, Zenodo DOI instructions,
  Sphinx docs with Read the Docs, SonarCloud analysis, changelog,
  community files, and a `next_steps.yml` workflow that opens onboarding
  issues for the manual setup steps (Zenodo, SonarCloud, Read the Docs).
- Expect opinionated defaults (line length 79, SonarCloud rather than
  other coverage services); accept them unless the project has a
  reason not to - fighting a template forfeits `copier update`.

## Choosing a build backend

When scaffolding by hand or answering template questions:

- setuptools + setuptools-scm: the template's default; version derived
  from git tags; battle-tested.
- hatchling: modern, minimal configuration; good default for new
  hand-rolled packages.
- poetry / PDM: bring their own dependency workflow; choose them only
  when the team wants that workflow, not just a build backend.

Whatever the choice, keep all tool configuration in pyproject.toml
sections rather than scattered dotfiles where the tools support it.

## After scaffolding

Generation is the start, not the finish:

- Work through the template's onboarding steps (the NLeSC template
  opens them as GitHub issues) instead of leaving badges broken.
- Delete generated options the project will not use rather than letting
  them rot; record the answers file (.copier-answers.yml) in git so
  `copier update` works.
- Route the per-practice follow-ups to the sibling skills: tests
  (rseng-testing), CI (rseng-ci-cd), docs (rseng-documentation), citation
  (rseng-citation-metadata), releases (rseng-publishing-releasing), FAIR
  posture (rseng-fair-software, rseng-fairguard).

## Working with this skill

This skill is source-independent: its authority is the template and
generator documentation linked below, not a bundled content source.

Learn more (verified):
  - https://github.com/NLeSC/python-template - the template
  - https://research-software-directory.org/software/nlesc-python-template -
    its Research Software Directory entry
  - https://copier.readthedocs.io/en/stable/ - Copier documentation

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-ci-cd - generated workflow files need understanding
- rseng-citation-metadata - template ships CITATION.cff and cffconvert check
- rseng-dependency-management - keeping generated tooling current
- rseng-fair-software - templates encode the FAIR baseline
- rseng-project-kickoff - management-side project start
- rseng-publishing-releasing - packaging and release setup follow-up

<!-- related-skills:end -->
