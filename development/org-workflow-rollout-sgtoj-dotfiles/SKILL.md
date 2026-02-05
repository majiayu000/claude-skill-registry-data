---
name: org-workflow-rollout
description: Roll out or update a GitHub Actions workflow file across multiple org repositories with signed commits and PRs
---

## Purpose

Automate the process of adding or updating GitHub Actions workflow files across
multiple repositories in an organization, with proper signed commits and pull
requests.

## Required Inputs

| Input               | Required | Description                                          |
|---------------------|----------|------------------------------------------------------|
| `repositories`      | Yes      | List of repo names (assumes single org or org/repo)  |
| `org`               | No       | GitHub organization (if not in repo names)           |
| `workflow_name`     | Yes      | Workflow filename, e.g., `ai.yaml`                   |
| `workflow_content`  | Yes      | Full YAML content of the workflow                    |
| `branch_name`       | Yes      | Branch to create, e.g., `add-ai-workflow`            |
| `commit_message`    | Yes      | Commit message, e.g., `feat: add ai workflow`        |
| `pr_title`          | Yes      | Default PR title (can be overridden per-repo)        |
| `pr_body`           | Yes      | PR description body                                  |
| `pr_title_overrides`| No       | Map of repo -> custom PR title                       |
| `mode`              | No       | `create`, `update`, or `upsert` (default: `upsert`)  |
| `dry_run`           | No       | If true, only report what would be done              |

## Modes

- **create**: Only create workflow if it doesn't exist (fail if exists)
- **update**: Only update existing workflow (fail if missing)
- **upsert**: Create if missing, update if exists (default)

## Execution Steps

### 1. Pre-flight Checks

- Verify `gh` CLI is authenticated
- Verify git signing is configured (`git config --global commit.gpgsign`)
- For each repository:
  - Verify repository exists and is accessible
  - Check if workflow file already exists on main
  - Check if branch already exists
  - Determine action based on mode

### 2. Dry Run Output (if `dry_run: true`)

Report a table showing what would happen:

| Repository   | Workflow Exists | Branch Exists | Action                   |
|--------------|-----------------|---------------|--------------------------|
| repo-name    | Yes/No          | Yes/No        | Create/Update/Skip/Error |

Stop execution after displaying this table.

### 3. Execution (if `dry_run: false`)

For each repository:

1. Clone shallow (`--depth 1`) to temp directory under `/tmp/`
2. Create and checkout new branch from main
3. Create or update `.github/workflows/<workflow_name>`
4. Stage changes and commit with GPG signature (`git commit -S`)
5. Push branch with upstream tracking (`git push -u origin <branch>`)
6. Create PR via `gh pr create` with appropriate title (check overrides)
7. Verify commit signature is valid via GitHub API

### 4. Summary Report

Output a results table:

| Repository   | Status  | PR URL                                    |
|--------------|---------|-------------------------------------------|
| repo-name    | Success | https://github.com/org/repo/pull/123      |
| other-repo   | Failed  | Error: branch already exists              |

### 5. Cleanup

Remove all temporary clone directories from `/tmp/`.

## Error Handling

- If a repository fails, log the error and continue with remaining repos
- Report all failures in the summary table
- Do not attempt rollback (user can manually close PRs and delete branches)

## Example Invocation

```
Roll out the AI workflow to these repositories:
- acme-dashboards
- acme-backend
- acme-frontend (PR title override: "feat: UNTRACKED: add ai workflow")

Workflow name: ai.yaml
Branch: add-ai-workflow
Commit message: feat: add ai workflow
PR title: feat: add ai workflow
PR body: |
  This PR adds the ai workflow that triggers on PR comments.

  Example: https://github.com/org/repo/pull/123#issuecomment-456
Mode: upsert
Dry run: true
```

## Implementation Notes

- All commits MUST be GPG signed (`git commit -S`)
- Use `gh` CLI for all GitHub API interactions
- Clone repos to `/tmp/<unique-dir>/` for execution
- Parallelize independent operations (cloning, pushing) where possible
- Respect GitHub API rate limits when creating multiple PRs
