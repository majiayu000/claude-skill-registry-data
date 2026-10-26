---
name: pywf-oss-upgrade-deps
description: "Upgrade, hold, or replace the dependencies of a pywf open-source Python library: find outdated and unmaintained packages, research changelogs and compatibility, update the constraints and lock file, and prove the result with tests, lint, and a docs build. Use when the user asks to upgrade or update dependencies, whether a new version of a package is worth it, or to replace an unmaintained package."
---

Bring the dependencies up to date, with every change justified and verified.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/04-python-versions.md
- ../pywf-oss-base/references/05-uv-dependencies.md
- ../pywf-oss-base/references/13-sphinx.md (section 2.2 and section 4: the cross-reference check and the visual check)
- ../pywf-oss-base/references/15-furo.md (only for a theme upgrade)
- ../pywf-oss-base/references/24-dependency-upgrades.md

## Steps

1. **Inventory.** Run `uv tree --outdated --depth 1`, check each direct dependency's last release date, and show a table: package, extra, locked version, latest version, last release date.
2. **Research.** Judge each candidate as in `24-dependency-upgrades.md` section 2 (including when to delegate to a subagent). Present each verdict (upgrade / hold / replace) with the exact constraint string.
3. **Decide.** The user picks which verdicts to apply. On "just upgrade everything", apply every upgrade verdict, and still report the holds and replacements.
4. **Apply,** as in `24-dependency-upgrades.md` section 3.
5. **Prove it.** Run every regression check in `24-dependency-upgrades.md` section 4, and report each as pass or fail. A failure sends that package back to step 2: hold it, or fix the code.
6. **Commit** after the user's yes, so the changelog sees the upgrade in git history.

## Boundaries

- Upgrade the coupled packages listed in `24-dependency-upgrades.md` section 2 together.
- Never raise `requires-python` as a side effect of an upgrade. It is the user's decision; ask it as a separate question.

Next step: `pywf-oss-changelog`, then `pywf-oss-release`.
