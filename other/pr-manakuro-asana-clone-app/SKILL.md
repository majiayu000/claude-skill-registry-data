---
name: pr
description: Push the current branch and open a GitHub pull request whose description follows .github/PULL_REQUEST_TEMPLATE.md.
disable-model-invocation: true
argument-hint: "[notes for the PR description]"
---

# Create a pull request

Push the current branch to `origin` (the maintainer's clone or a contributor's fork) and open a PR against `main` of the upstream repository, with a description that follows `.github/PULL_REQUEST_TEMPLATE.md`.

Extra notes from the user (may be empty): $ARGUMENTS

## 1. Find the repositories

```sh
git remote -v
```

- **Head** (where the branch is pushed): the `origin` remote, `<head-owner>/<head-repo>`.
- **Base** (where the PR is opened): the `upstream` remote if there is one (a fork), otherwise `origin`. Call it `<base-owner>/<base-repo>` and use `<base>` below for that remote's name.

Read the owners and repo names from the remote URLs (`git@github.com:<owner>/<repo>.git` or `https://github.com/<owner>/<repo>.git`). Don't assume a fixed owner.

## 2. Check the branch

```sh
git branch --show-current
git status --short
git fetch <base> main --quiet
git log --oneline <base>/main..HEAD
git diff --stat <base>/main...HEAD
```

- If the current branch is `main`, stop and ask the user for a branch name. Don't push to `main`.
- If there are uncommitted changes, ask the user whether to commit them first or leave them out.
- If there are no commits ahead of `<base>/main`, stop: there is nothing to open a PR for.

## 3. Write the title and description

Read the branch name, the commit messages and the diff to understand the change.

- **Title:** Conventional Commits, like the commits in this repo (`feat(core): …`, `fix(cli): …`, `docs: …`, `build: …`, `ci: …`). For a single-commit branch, reuse the commit subject.
- **Description:** fill in every section of `.github/PULL_REQUEST_TEMPLATE.md`, keeping its headings and order:
  - **Summary**: the purpose of the change in one or two sentences, then a bullet list of the main changes
  - **Related Issues**: `Closes #<n>` for issues the branch fixes (from the branch name, commits or the user's notes), otherwise `None`
  - **Testing**: what was run (`pnpm lint`, `pnpm tsc`, `pnpm test:ci`, the playground app, …) and what was checked by hand
  - Add anything reviewers should know (breaking changes, follow-ups, generated files to skip) at the end of Summary
- Screenshots are not required.
- Don't add the `🤖 Generated with Claude Code` footer or any link to Claude at the end of the description.

## 4. Push and open the PR

```sh
git push -u origin HEAD
```

Then create the PR with the GitHub MCP server (not the `gh` CLI):

- owner / repo: `<base-owner>` / `<base-repo>`
- base: `main`
- head: the current branch, or `<head-owner>:<branch>` when the head is a fork (head owner differs from base owner)
- the title and description from step 3

If a PR for this branch already exists, update its title and description instead of opening a new one.

## 5. Report

Reply with the PR URL and its title. Mention anything left for the user, such as a missing changeset or uncommitted files that were not included.
