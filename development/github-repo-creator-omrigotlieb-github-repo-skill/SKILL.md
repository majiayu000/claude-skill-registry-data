---
name: github-repo-creator
description: Creates GitHub repositories with proper setup. Use when the user wants to create a new GitHub repo, initialize a repository, or set up a new project on GitHub.
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# GitHub Repository Creator

Creates new GitHub repositories with professional setup using the `gh` CLI.

## Prerequisites

- GitHub CLI (`gh`) must be installed and authenticated
- Run `gh auth status` to verify authentication

## Instructions

When creating a GitHub repository:

### 1. Gather Information

Ask the user for:
- **Repository name** (required)
- **Description** (optional but recommended)
- **Visibility**: public or private (default: private)
- **Initialize with**: README, .gitignore, license

### 2. Create the Repository

```bash
# For a new repo (not from existing folder)
gh repo create <repo-name> --public/--private --description "description" --clone

# For existing local project
gh repo create <repo-name> --source=. --public/--private --push
```

### 3. Common Options

| Flag | Description |
|------|-------------|
| `--public` | Make repository public |
| `--private` | Make repository private |
| `--description "text"` | Add description |
| `--clone` | Clone the new repo locally |
| `--source=.` | Use current directory as source |
| `--push` | Push local commits to new repo |
| `--gitignore <template>` | Add .gitignore (e.g., Node, Python) |
| `--license <license>` | Add license (e.g., MIT, Apache-2.0) |

### 4. Post-Creation Setup

After creating the repo:
1. Confirm the repo was created successfully
2. Provide the repository URL to the user
3. Suggest next steps (add collaborators, set up CI/CD, etc.)

## Examples

**Create a new public repo and clone it:**
```bash
gh repo create my-awesome-project --public --description "A cool project" --clone
```

**Create repo from existing local project:**
```bash
gh repo create my-project --source=. --private --push
```

**Create with README and MIT license:**
```bash
gh repo create my-project --public --add-readme --license MIT
```

## Future Enhancements

- [ ] Auto-generate repository banner/social image
- [ ] Template selection for common project types
- [ ] Automatic branch protection rules setup
