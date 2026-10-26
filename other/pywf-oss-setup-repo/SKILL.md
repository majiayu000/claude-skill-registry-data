---
name: pywf-oss-setup-repo
description: "Take a freshly generated pywf open-source Python library repo live: verify it locally, create and push the GitHub repo, set its metadata, connect Codecov and Read the Docs, enable CI, and confirm all are green, with the user's yes before each external step. Use when the user has a new repo from the template and wants it on GitHub with CI, coverage, and hosted docs."
---

Turn a local repo generated from the template into a live project, with GitHub, CI, Codecov, and Read the Docs all green. Each external step waits for the user's yes; one yes covers one step.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/01-secrets.md
- ../pywf-oss-base/references/03-mise.md
- ../pywf-oss-base/references/19-github-actions.md
- ../pywf-oss-base/references/20-codecov.md
- ../pywf-oss-base/references/21-readthedocs.md

## Steps

1. **Preflight.**
   - Run the token True/False check. If any token is `False`, stop and hand off to `pywf-oss-setup-machine`.
   - Read `[project].name` from `pyproject.toml`, and run `git remote -v`.
   - No `origin` yet: propose the GitHub owner and the repo name `<package_name>-project`, and wait for the user to confirm. Step 3 creates the repo and remote.
   - `origin` exists: show the GitHub repo URL, the Read the Docs slug, and the docs URL the tasks will use (`.mise/tasks/utils.py` derives them from `origin` and the project name), and ask the user to confirm.
2. **Local green.** `mise run inst`, `mise run cov`, `mise run lint`, and `mise run build-doc` pass; template-fresh code should. Fix any failure before going online.
3. **GitHub repo.** If none exists, propose `gh repo create <owner>/<repo> --public --source . --remote origin --push`, and run it after the user's yes. Then show the URL, slug, and docs URL derived from the new `origin`.
4. **GitHub metadata.** `mise run update-github-metadata`, after the user's yes.
5. **Codecov.** `mise run setup-codecov`, after the user's yes. Confirm the secret with `gh secret list` (names only).
6. **Read the Docs.** `mise run setup-readthedocs`, after the user's yes.
7. **CI.** Show the change that enables the `push` and `pull_request` triggers in `.github/workflows/main.yml`, commit and push it after the user's yes, and watch the run with `gh run list` and `gh run view`.
8. **Confirm.** Report the CI run, the Codecov project, and the docs build as green or red. Diagnose anything red with `19-github-actions.md`, `20-codecov.md`, or `21-readthedocs.md`, or hand off to `pywf-oss-fix-ci`.

## Boundaries

- Never change repo visibility, branch protection, or any repo setting not listed in these steps.

Next steps: `pywf-oss-add-module` to start coding, `pywf-oss-release` for the first version, and `pywf-oss-write-maintain-skill` once there is something to say about maintaining it.
