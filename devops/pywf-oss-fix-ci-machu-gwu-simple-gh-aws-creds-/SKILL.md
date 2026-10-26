---
name: pywf-oss-fix-ci
description: "Diagnose and fix a red GitHub Actions run, a failed Codecov upload, or a failed Read the Docs build of a pywf open-source Python library, or add or drop a supported Python version. Use when the user says CI, the tests on GitHub, Codecov, the docs build, or Read the Docs fails or shows warnings, or asks to add or drop a Python version."
---

Find from the logs why a hosted service is red, fix the cause in the repo, and confirm it is green again. Also add or drop a Python version.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/04-python-versions.md
- ../pywf-oss-base/references/19-github-actions.md
- ../pywf-oss-base/references/20-codecov.md
- ../pywf-oss-base/references/21-readthedocs.md
- ../pywf-oss-base/references/25-python-release-cycle.md (only for adding or dropping a Python version)

## Steps

1. **Find the red service and its log** with the commands in `19-github-actions.md`, `20-codecov.md`, or `21-readthedocs.md`. Quote the decisive log lines to the user.
2. **Reproduce locally** where possible: `mise run cov` for tests, `mise run build-doc` for docs. If it passes locally, compare OS and Python version, the installed extras (`uv sync --extra test` in CI, `--all-extras` locally), and the working directory.
3. **Fix the cause, not the symptom.**
   - Never skip, xfail, or delete a failing test to turn CI green without the user's yes.
   - Never narrow the matrix permanently to hide a failure.
4. **Verify.** Rerun locally. Then, after the user's yes, push the fix, or for an infrastructure flake run `gh run rerun <run_id> --failed`. Check the new run with `gh run view`.

## Boundaries

- Reading logs and runs needs no approval. Pushing, rerunning, deleting caches, and rerunning setup tasks each need the user's yes.

Next step: `pywf-oss-upgrade-deps` when the cause is a dependency, or when a Python version change lifts or adds dependency caps; `pywf-oss-changelog` to record a Python version change.
