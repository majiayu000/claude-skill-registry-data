---
name: nxs-gh-create-task
description: Create GitHub issues from TASK-???.md files. Use when you need to bulk-create GitHub issues from task markdown files with frontmatter containing title, label, parent, and project attributes. Automatically extracts frontmatter, creates issues via gh CLI, links parent issues, and adds to specified projects.
---

# NXS GitHub Create Task

Create GitHub issues from TASK-???.md files in a target folder.

## Usage

```bash
python ./scripts/create_gh_issues.py <target_folder> [--dry-run] [--no-project]
```

**Arguments:**

-   `target_folder` - Directory containing TASK-???.md files
-   `--dry-run` - Preview what would be created without making API calls
-   `--no-project` - Skip adding issues to any project

## Task File Format

Each TASK-???.md file should have YAML frontmatter:

```markdown
---
title: Implement user authentication
labels: [enhancement, backend]
parent: #42
project: "acme-corp/backend-roadmap"
---

## Description

Task body content goes here. This becomes the issue body.
```

**Frontmatter fields:**

| Field     | Required | Description                                                                                                                                                                          |
| --------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `title`   | Yes      | Issue title                                                                                                                                                                          |
| `labels`  | No       | Array of GitHub labels: `[label1, label2, ...]`                                                                                                                                      |
| `parent`  | No       | Parent issue reference (`#42` or full URL)                                                                                                                                           |
| `project` | No       | GitHub project to add the issue to. Supports: `owner/number` (e.g., `my-org/1`), `number` (uses current repo's owner), or project title. If omitted, auto-discovers from repository. |

## Workflow

1. Script finds all `TASK-???.md` files matching the pattern
2. For each file:
    - Parses YAML frontmatter to extract title, labels, parent, project
    - Creates temp file with body content (frontmatter stripped)
    - Runs `gh issue create --title <title> --label <label1> --label <label2> ... --body-file <temp>`
    - Adds issue to the specified project (or auto-discovered project from repo)
    - If parent specified, creates sub-issue relationship via `gh api`
    - Deletes temp file

## Project Resolution

The script determines which project to use in this order:

1. **Frontmatter `project` attribute** - If specified in the task file, use this project
2. **Repository project** - If no `project` attribute, auto-discover from the repository's linked projects
3. **No project** - If neither is found (or `--no-project` flag is set), skip project assignment

## Prerequisites

-   `gh` CLI installed and authenticated
-   For project integration: `gh auth login --scopes 'project'`
-   Repository context (run from within a git repo or use `gh repo set-default`)

## Examples

```bash
# Preview what will be created
python ./scripts/create_gh_issues.py ./tasks --dry-run

# Create the issues (uses project from frontmatter or auto-discovers)
python ./scripts/create_gh_issues.py ./tasks

# Create issues without adding to any project
python ./scripts/create_gh_issues.py ./tasks --no-project
```
