---
name: gh-cli-pr-ci
description: Use the GitHub gh CLI to inspect pull requests, status checks, and CI failures. Trigger when triaging PRs/CI, fetching workflow logs, or summarizing check results. Prefer explicit --json field lists; avoid deprecated GraphQL fields like projectCards and invalid fields like checks by using statusCheckRollup.
---

# GH CLI PR/CI Triage

## Overview

Use this skill to triage PRs and CI failures with the gh CLI while avoiding GraphQL deprecations and invalid JSON fields. The key pattern: always request explicit JSON fields and use statusCheckRollup for checks.

## Quick Start Workflow

1) Fetch PR summary + checks (explicit fields only):

```bash
gh pr view <pr-number> --repo <owner>/<repo> \
  --json title,number,state,headRefName,baseRefName,author,mergeable,commits,files,additions,deletions,labels,statusCheckRollup
```

2) List failing checks with URLs:

```bash
gh pr view <pr-number> --repo <owner>/<repo> \
  --json statusCheckRollup \
  --jq '.statusCheckRollup[] | {name,conclusion,detailsUrl,startedAt,completedAt}'
```

3) Pull job logs from the details URL:

- details URL format: `https://github.com/<owner>/<repo>/actions/runs/<run-id>/job/<job-id>`
- fetch logs:

```bash
gh run view <run-id> --repo <owner>/<repo> --job <job-id> --log
```

## Stacked PR Base Handling

- Prefer a single PR for a coherent, mergeable unit of work. Only stack when the overall effort is too large for one PR but can be split into focused, reviewable chunks that build on each other.
- If a ticket/issue is referenced (GitHub issue or external tracker), include it in the PR body and use a GitHub closing keyword when applicable (e.g., `Closes #123`) so the issue auto-closes on merge.

- For independent PRs, create against the repo trunk (`<trunk-branch>`):

```bash
gh pr create --repo <owner>/<repo> --base <trunk-branch> --head <bookmark> --title "<conventional title>" --body-file <file>
```

- For stacked PRs, set the base to the previous stack layer’s branch:

```bash
gh pr create --repo <owner>/<repo> --base <prev-layer-branch> --head <bookmark> --title "<conventional title>" --body-file <file>
```

- After merging a lower stack layer into trunk, update the next PR’s base to trunk and push the rebased bookmark:

```bash
gh pr edit <pr-number> --repo <owner>/<repo> --base <trunk-branch>
```

## Pitfalls and Avoidance

- **Do not run `gh pr view` without `--json`.** The default GraphQL selection can request deprecated `projectCards` and trigger a deprecation error.
- **Do not use `--json checks`.** The field is not supported; use `statusCheckRollup` instead.
- **Keep JSON field lists minimal.** If a field causes errors, remove it and retry with a smaller list.
- **PR body newlines:** `gh pr create/edit --body` does **not** interpret `\n` escapes. Use `--body-file` (including `--body-file -` with a heredoc) or `gh api ... --input -` with JSON to preserve newlines.
- **PR titles must be Conventional Commits.** Format: `type(scope optional)!: subject`. Allowed types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `build`, `ci`, `perf`. If the user provides a non-conforming title, propose a compliant one and confirm before creating/updating the PR.

## Useful Variations

- PR metadata without checks:

```bash
gh pr view <pr-number> --repo <owner>/<repo> \
  --json title,number,state,headRefName,baseRefName,author,mergeable,commits,files,additions,deletions,labels
```

- Filter only failed checks:

```bash
gh pr view <pr-number> --repo <owner>/<repo> \
  --json statusCheckRollup \
  --jq '.statusCheckRollup[] | select(.conclusion=="FAILURE") | {name,detailsUrl}'
```

## Decision Notes

- If you need project info, avoid classic projects fields; only add project-related fields if required and be prepared for permission or deprecation errors.
- For cross-repo PRs, always pass `--repo` to avoid querying the wrong default repository.
