---
name: azure-cli
description: When users share links (such as visualstudio.com or dev.azure.com) and/or mention Azure DevOps, use the Azure DevOps CLI to interact with work items, pull requests (PRs), repositories, and more.
---

# Azure DevOps CLI

You have access to an already signed in version of the Azure CLI with devops access. When users share Azure DevOps links or mention Azure DevOps resources, infer the appropriate action from context before running commands.

## Parsing Azure DevOps URLs

Extract parameters from common URL patterns:

- `https://dev.azure.com/{org}/{project}/_git/{repo}/pullrequest/{prId}`
- `https://{org}.visualstudio.com/{project}/_git/{repo}/pullrequest/{prId}`
- `https://dev.azure.com/{org}/{project}/_workitems/edit/{workItemId}`

## Pull Requests

Infer user intent from context when they share a PR link:

| Context                          | Likely Action                             |
| -------------------------------- | ----------------------------------------- |
| "review", "comments", "feedback" | Get comment threads                       |
| "what's this PR", "show me"      | Show PR details                           |
| "check out", "work on this"      | Checkout PR branch                        |
| "approve", "complete", "merge"   | Update PR status                          |
| No clear intent                  | Show PR summary first, ask what they need |

### Show PR Details

```shell
az repos pr show --id {prId} --org {orgUrl}
```

### Checkout PR Branch

```shell
az repos pr checkout --id {prId}
```

### Get PR Comment Threads

The CLI lacks a first-class command for threads; use `az devops invoke`:

```shell
az devops invoke --area git --resource pullRequestThreads --route-parameters project={project} repositoryId={repository} pullRequestId={prId} --org {orgUrl} --api-version 7.1
```

Filter to active/unresolved threads:

```shell
... | jq '.value[] | select(.status == "active")'
```

### Vote on a PR

```shell
# approve, approve-with-suggestions, wait-for-author, reject, reset
az repos pr set-vote --id {prId} --vote approve --org {orgUrl}
```

### Update PR Status

```shell
az repos pr update --id {prId} --status completed --org {orgUrl}  # or: abandoned
```

### List Linked Work Items

```shell
az repos pr work-item list --id {prId} --org {orgUrl}
```

### Manage Reviewers

```shell
az repos pr reviewer add --id {prId} --reviewers {email} --org {orgUrl}
az repos pr reviewer list --id {prId} --org {orgUrl}
```

## Work Items

### Show Work Item Details

```shell
az boards work-item show --id {workItemId} --org {orgUrl}
```

### Update Work Item

```shell
az boards work-item update --id {workItemId} --state "Active" --org {orgUrl}
az boards work-item update --id {workItemId} --assigned-to {email} --org {orgUrl}
```

### Create Work Item

```shell
az boards work-item create --title "Title" --type "Task" --project {project} --org {orgUrl}
```

### Query Work Items (WIQL)

```shell
az boards query --wiql "SELECT [System.Id] FROM workitems WHERE [System.AssignedTo] = @Me" --org {orgUrl}
```

### Manage Work Item Relations

```shell
az boards work-item relation add --id {workItemId} --relation-type "Parent" --target-id {targetId} --org {orgUrl}
```

## Using `az devops invoke` for REST APIs

When the CLI lacks a first-class command, use `invoke` to call any Azure DevOps REST API:

```shell
az devops invoke --area {area} --resource {resource} --route-parameters {key}={value} --org {orgUrl} --api-version 7.1
```

Common areas: `git`, `wit` (work item tracking), `core`
