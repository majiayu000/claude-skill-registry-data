---
name: github-project-release
description: Use when preparing or publishing a local project as a clean GitHub repository. Covers new repositories, private staging releases, public README cleanup, updates to existing remotes, and research-code packaging without datasets, checkpoints, papers, or generated artifacts.
license: MIT
---

# GitHub Project Release

Turn a local project into a clean GitHub repository that is safe to make public later. Default to
research-code release behavior: clean copy first, private GitHub repo first, audit before push.

## Workflow

1. Inspect the source project before copying.
   - Identify the runnable entrypoints, key configs, curated figures/tables, license, citation files,
     and upstream dependencies.
   - Treat the codebase as source of truth. Do not preserve stale upstream README language as the
     release front page.

2. Check credentials.
   - Run `scripts/github_project_release.py auth-check`.
   - Use the active `gh` account as the default owner.
   - Never ask the user to paste a GitHub token into chat. If auth is missing, ask them to run
     `gh auth login` or provide credentials through a secure non-chat channel.

3. Prepare a clean release copy.
   - Run `scripts/github_project_release.py prepare --source <project> --dest <release-dir>`.
   - Keep only what a new user needs to understand and run the project.
   - Exclude datasets, checkpoints, logs, generated outputs, raw experiment dumps, paper PDFs, local
     submission material, and exploratory files unless the user explicitly overrides the default.

4. Write or rewrite the README.
   - Read `references/readme_playbook.md` before drafting README content.
   - Use English by default.
   - Write for external readers, not for the project owner.
   - For research code, cover Context + Run + Cite: what it is, what problem it solves, what is
     included, how to install/run the minimal path, and how to cite current and upstream work.

5. Audit before publishing.
   - Run `scripts/github_project_release.py audit --path <release-dir>`.
   - Treat reported high-risk items as blockers unless the user explicitly accepts them.
   - If a paper link is not public, use `Paper link: coming soon.` and do not upload PDFs.

6. Publish privately.
   - Run `scripts/github_project_release.py publish --release-dir <release-dir>`.
   - If the repo does not exist, create a private repo.
   - If it exists, push only safe non-rewriting updates.
   - Do not force-push, delete, overwrite, or make the repo public unless explicitly requested.

7. Report the result.
   - Include repo URL, branch, commit SHA, visibility, and audit status.
   - If any sensitive artifact was accidentally pushed earlier, explain that branch-history cleanup
     may not immediately remove exact-SHA access on GitHub; for strict removal, recreate a clean repo.

## Script Quick Reference

Resolve `<skill-dir>` to the directory containing this `SKILL.md`; do not
assume a particular global skills installation root.

```bash
python "<skill-dir>/scripts/github_project_release.py" auth-check

python "<skill-dir>/scripts/github_project_release.py" prepare \
  --source /path/to/project \
  --dest /path/to/project-github

python "<skill-dir>/scripts/github_project_release.py" audit \
  --path /path/to/project-github

python "<skill-dir>/scripts/github_project_release.py" publish \
  --release-dir /path/to/project-github
```

Use `--dry-run` on `prepare` or `publish` to inspect intended actions without copying or pushing.

## Defaults

- Visibility: private.
- Owner: active `gh` account.
- Repo name: sanitized release directory name, unless `--repo`, `--owner`, or `--name` is provided.
- Existing repo policy: safe update only.
- README language: English.
- Results policy: paper-confirmed figures/tables/results only; never infer metrics from logs.
- Asset policy: curated explanatory figures/tables only; never bulk-upload raw visualization outputs.

## When To Ask

Ask the user only when the answer cannot be derived from the project:

- Target GitHub owner differs from the active `gh` account.
- Repo name should differ from the project/release directory.
- A normally blocked file type must be included.
- The user wants public release, force-push, repo deletion, or history rewrite.
- The current project has no clear runnable path and the README would otherwise invent commands.
