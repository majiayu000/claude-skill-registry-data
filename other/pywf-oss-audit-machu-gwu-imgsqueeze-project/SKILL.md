---
name: pywf-oss-audit
description: "Audit a pywf open-source Python library against the template conventions (Python versions, dependencies, lint, code style, public API, test layout, docs, changelog) and report each deviation with the skill that fixes it, changing no source file. Use when the user asks to check, audit, or review a repo, or to bring an older repo up to the current template."
---

Compare one repo with the template conventions, and produce a prioritized list of deviations. The audit changes no source file: if a check regenerates a tracked file, report the diff as a finding, then restore the file.

Read ../pywf-oss-base/SKILL.md, then every file in ../pywf-oss-base/references/.

## Checks

Record each finding with the file, the rule broken (reference file and section), and the fixing skill.

1. **Python versions and dependencies.**
   - `uv tree --outdated --depth 1` (fixed by `pywf-oss-upgrade-deps`).
   - The four Python version locations agree with `04-python-versions.md` (fixed by `pywf-oss-fix-ci`).
   - Dependency constraints follow `05-uv-dependencies.md`.
2. **Lint.**
   - `mise.toml` has the `format` and `lint` tasks, and `pyproject.toml` has `[tool.ruff]` and `[tool.pytest]`.
   - `mise run lint` passes.
   - `uvx ruff format --check` on the `format` task's paths in `mise.toml` passes. Never run `mise run format` during an audit: it rewrites files.
3. **Code style** against `09-code-style.md`, sampled in about 10 source files and the recently changed areas:
   - the file header;
   - one name per import, and the five-group order;
   - no absolute self-imports inside `<package_name>/`;
   - 3.11+ type hints;
   - docstrings and `#:` comments;
   - one field per line in declarative models.
4. **Public API**, against `08-package-files.md`:
   - `api.py` exports no `_private` names;
   - every exported name has a docstring;
   - `tests/test_api.py` touches every exported name.
5. **Test layout.** Run `python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/check_test_layout.py --project_root .`.
6. **Docs and knowledge channels.**
   - No maintainer or contributor-guide pages in `docs/source/` (`18-knowledge-channels.md`); they belong in the `<maintain_prefix>` family (fixed by `pywf-oss-write-maintain-skill`).
   - If `.claude/skills/pypi-<package_name>/` exists, its version header matches the last tag (fixed by `pywf-oss-write-pypi-skill`).
   - Folder names follow `14-docfly.md`.
   - Headings use 78-character underlines.
   - `mise run build-doc` shows no warnings. It regenerates the tracked `docs/source/api/`, and may change `uv.lock`: report any `git status` diff in either, then restore them with `git checkout docs/source/api uv.lock`.
   - `python ${CLAUDE_SKILL_DIR}/../pywf-oss-base/scripts/check_doc_xrefs.py` reports 0 unresolved.
   - Notebooks have committed outputs.
7. **Changelog.** The Backlog block is present, and the latest version section matches the `pyproject.toml` version or the last tag.

## Report

Group the findings by fixing skill:

- `pywf-oss-add-module`
- `pywf-oss-write-test`
- `pywf-oss-write-doc`
- `pywf-oss-write-maintain-skill`
- `pywf-oss-write-pypi-skill`
- `pywf-oss-changelog`
- `pywf-oss-fix-ci` (Python versions and CI config)
- `pywf-oss-upgrade-deps` (outdated or unmaintained dependencies)
- "direct edit" (config and style)

Within each group, order the findings by severity:

1. breaks CI or the release;
2. breaks a convention that tools rely on;
3. style.

End with counts per group, and ask which group to fix first.
