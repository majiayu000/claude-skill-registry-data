---
name: github-user
description: You are a user of GitHub.  You interact with GitHub repositories, issues, projects and prs.
---

This skill guides interaction with GitHub apis.

## Overview

- You should use the GitHub cli to work with github rather than using an MCP. The usage of this cli is shown next.

## GitHub CLI Usage

```
USAGE
  gh <command> <subcommand> [flags]

CORE COMMANDS
  auth:          Authenticate gh and git with GitHub
  browse:        Open repositories, issues, pull requests, and more in the browser
  codespace:     Connect to and manage codespaces
  gist:          Manage gists
  issue:         Manage issues
  org:           Manage organizations
  pr:            Manage pull requests
  project:       Work with GitHub Projects.
  release:       Manage releases
  repo:          Manage repositories

FLAGS
  --help      Show help for command
  --version   Show gh version

EXAMPLES
  $ gh issue create
  $ gh repo clone cli/cli
  $ gh pr checkout 321
```

## Context

You should run the following cli commands to get a understanding of the current GitHub repository, project, etc:

```
gh repo view --json id,name,owner
gh project list --owner <OWNER>
gh project item-edit --help
gh project item-add --help
gh project field-list --help
```

## Update issue status

- If asked to update the status of a GitHub sub-issue then this refers to the GitHub project system way of handling status.
- You will need to use "gh project item-edit" to update the field with name "Status", this requires an owner and a project number which can be found using the "gh project list" command and the "gh project field-list" command.

## Creating a sub-issue

- If asked to create a GitHub sub-issue then this refers to the GitHub project system way of handling sub-issues.
- Given an existing parent issue you should start by creating the sub-issue as you would a regular issue. Then you must associate it with the parent by using the GitHub "addSubIssue" graphql mutation.

## Creating a PR

- Use "gh pr create" with appropriate params.
- You must execute this from within the worktree directory.
- When creating the PR ensure that the branch can be merged back to main without conflicts by pulling latest from remote.
