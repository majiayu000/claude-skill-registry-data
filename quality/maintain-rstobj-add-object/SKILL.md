---
name: maintain-rstobj-add-object
description: "Add a new markup or directive class to rstobj: the dataclass, its jinja2 template, the api.py export, the rendering cases and snapshots, and its place in the docs Rendering Gallery. Use when the user asks rstobj to support a new reStructuredText directive, role, or markup, or a new language code block."
---

Add one new renderable class to rstobj, tested and shown in the docs.

Read ../maintain-rstobj-base/SKILL.md, then:
- ../maintain-rstobj-base/references/01-architecture.md
- ../maintain-rstobj-base/references/03-templates.md
- ../maintain-rstobj-base/references/04-cases-snapshots-gallery.md
- ../maintain-rstobj-base/references/05-compatibility-and-traps.md

For the module and test file conventions, load `pywf-oss-base` and read its Special Files in the Package, Code Style, and Test Layout references; the `pywf-oss-add-module` skill does the generic part.

## Step 1: Pin down the target

- Name the reStructuredText construct and link its spec (docutils or Sphinx). List its argument and every option you will support, with real option names.
- Choose the module: a directive goes in `rstobj/directives/`, markup in `rstobj/markup/`. Reuse an existing module when the construct belongs to its family (a new language goes in `codeblock.py`); otherwise create one, with its test file, following the `pywf-oss-base` Test Layout reference.
- Tell the user the plan, including the release it implies: a new public class is a minor release (`05-compatibility-and-traps.md` section 1). Wait for the user's yes.

## Step 2: Write the class

- `@dataclass(kw_only=True)`, subclassing `Directive` for a directive (set `meta_directive_keyword`, define `arg`; set `meta_supports_name = False` if the directive has no `:name:`) or `RstObj` for markup.
- A new code block language only needs a `CodeBlockBase` subclass with `meta_lang` and the shared docstring, as the existing ones do.
- Docstring with an `Example::` and `Output::` block, like its siblings. Validate enumerated fields in `__post_init__` only if the old output would have been invalid anyway.

## Step 3: Write the template

Create `rstobj/templates/<module>.<ClassName>.rst` (skip for a code block language: it shares `CodeBlockBase.rst`). Follow every rule in `03-templates.md`.

## Step 4: Export it

Add one `from .module_name import ClassName` line to `rstobj/directives/api.py` or `rstobj/markup/api.py`, and one `_ = api.ClassName` line to the matching `tests/<subpackage>/test_<subpackage>_api.py`.

## Step 5: Add cases and snapshots

- In `rstobj/tests/cases.py`, add a section for the module (a `M_<NAME>` constant) and cases: one basic, one with every option, plus `gallery=False` cases for edge values (empty, `False`, `0`). Set `live=False` if rendering it would change the docs page's own structure.
- A new module also needs an entry in `GROUP_TITLES` in `rstobj/docs/__init__.py`, and a test file that parametrizes `cases_for(MODULE)` and checks orphan snapshots, as the existing ones do.
- Create and review the snapshots (`04-cases-snapshots-gallery.md` section 3).

## Step 6: Verify

`mise run cov` (100%, no warnings), `mise run lint`, and `mise run build-doc` (fails on any warning) all pass. Then look at the new gallery entries: preview `docs/build/html` with the `docs-html` configuration in `.claude/launch.json`.

## Report

The new class and its options, the files added or changed, the case ids, and the release type it needs. Suggest `pywf-oss-changelog` for the release note and, after the release, `pywf-oss-write-pypi-skill` to add the class to the API skill.
