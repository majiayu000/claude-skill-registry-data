---
name: pywf-oss-release
description: "Release a new version of a pywf open-source Python library: bump the version, make sure the changelog, tests, and docs are ready, then publish to PyPI and create the GitHub release, asking for the user's yes before each public step. Use when the user asks to release, publish, ship, or cut a new version."
---

Take the repo from "the change is done" to "the version is on PyPI and tagged on GitHub". Stop for the user's yes before every step that cannot be undone.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/01-secrets.md
- ../pywf-oss-base/references/03-mise.md
- ../pywf-oss-base/references/22-versioning-and-changelog.md
- ../pywf-oss-base/references/23-release.md

## Steps

1. **Version.**
   - Show the last tag and the current `pyproject.toml` version.
   - If they are equal, propose a bump (PATCH, MINOR, or MAJOR) with a one-line reason from the `api.py` diff, and apply it after the user's yes.
2. **Changelog.** If `release-history.rst` has no section for the target version, or a stale one, run the `pywf-oss-changelog` steps first.
3. **Checks.**
   - `mise run cov`, `mise run lint`, and `mise run build-doc` pass.
   - `git status` is clean, apart from the version bump (`pyproject.toml`, `uv.lock`) and the changelog edit.
   - On any failure, report it and stop.
4. **Commit and push.** Show the commit message; commit and push to `main` after the user's yes.
5. **Publish.** Ask: "Publish `<package_name>` `<version>` to PyPI?" After the user's yes, run `mise run publish`.
6. **GitHub release.** Ask, and run `mise run release` after the user's yes.
7. **Report.** Give the PyPI URL (printed by `publish`) and the release URL.

Next step (optional): `pywf-oss-write-pypi-skill`.
