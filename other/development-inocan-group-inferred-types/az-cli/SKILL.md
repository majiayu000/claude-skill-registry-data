---
name: az-cli
description: This skill should be used when working with Azure DevOps from the command line. Trigger when user mentions az devops, az repos, az pipelines, az boards, or asks about managing PRs, work items, pipelines, or repositories in Azure DevOps. Also trigger for questions about Azure DevOps CLI setup, authentication, or querying work items.
---

# Azure DevOps CLI

## Overview

Manage Azure DevOps resources using the `az` CLI with the `azure-devops` extension. Covers repositories, pull requests, pipelines, boards, and work items.

## Prerequisites

```bash
# Install azure-devops extension (requires az cli 2.30+)
az extension add --name azure-devops

# Authenticate
az login

# Set defaults (recommended)
az devops configure --defaults organization=https://dev.azure.com/YOUR_ORG project=YOUR_PROJECT
```

## Most-Used Commands

### My Pull Requests

```bash
# List PRs I created
az repos pr list --creator "$(az account show --query user.name -o tsv)"

# List PRs assigned to me for review
az repos pr list --reviewer "$(az account show --query user.name -o tsv)"

# Show PR details
az repos pr show --id <pr-id>

# Checkout PR locally
az repos pr checkout --id <pr-id>
```

### My Work Items

```bash
# List work items assigned to me
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.AssignedTo] = @Me AND [System.State] <> 'Closed' ORDER BY [System.ChangedDate] DESC"

# Show work item details
az boards work-item show --id <work-item-id>

# Create work item
az boards work-item create --title "Task title" --type "Task"

# Update work item state
az boards work-item update --id <id> --state "In Progress"
```

### Pipelines

```bash
# List pipelines
az pipelines list

# List recent runs
az pipelines runs list --top 10

# Run a pipeline
az pipelines run --name "pipeline-name"

# Run with parameters
az pipelines run --name "pipeline-name" --parameters "env=prod version=1.0"

# Show run details
az pipelines runs show --id <run-id>
```

### Repositories

```bash
# List repositories
az repos list

# Show repo details
az repos show --repository <repo-name>

# Create repository
az repos create --name "new-repo"
```

### Pull Request Workflow

```bash
# Create PR
az repos pr create --source-branch feature/my-branch --target-branch main --title "PR Title" --description "Description"

# Add reviewers
az repos pr update --id <pr-id> --reviewers user@email.com

# Set vote (approve: 10, approve with suggestions: 5, wait: -5, reject: -10)
az repos pr set-vote --id <pr-id> --vote 10

# Complete/merge PR
az repos pr update --id <pr-id> --status completed
```

## References

Detailed command references available:

- **`references/repos.md`** - Repository management, PRs, policies, refs
- **`references/pipelines.md`** - Pipeline CRUD, runs, variables, releases
- **`references/boards.md`** - Work items, queries, areas, iterations
- **`references/devops.md`** - Organization, projects, teams, wikis, auth

## Common Flags

Most commands support:

| Flag                | Description                                         |
| ------------------- | --------------------------------------------------- |
| `--org`             | Organization URL (or set via `az devops configure`) |
| `--project`         | Project name (or set via `az devops configure`)     |
| `--detect`          | Auto-detect org/project from git remote             |
| `-o json/table/tsv` | Output format                                       |

## Troubleshooting

```bash
# Check current config
az devops configure --list

# Verify authentication
az account show

# Check extension version
az extension show --name azure-devops
```
