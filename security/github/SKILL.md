---
name: github
description: Work with GitHub — pull requests, issues, Actions, code review, project boards, releases.
category: development
aliases:
- pr
- pull-request
- issue
- gh
- github-actions
triggers:
- open a PR
- create an issue
- github actions
- help with GitHub
- review a PR
keywords:
- github
- pr
- pull-request
- issue
- action
- workflow
- release
dependencies:
- git
- gh-cli-optional
risk: medium
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- development
- github
- issue
- pull-request
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# GitHub

## Purpose

Operate on GitHub: pull requests, issues, Actions workflows, releases, project boards, and
code review etiquette.

## When to Use

- User wants to open / merge / review a PR
- User wants to file or triage an issue
- User wants to set up GitHub Actions
- User wants to publish a release

## When NOT to Use

- Pure git questions (route to `git`)
- Pure code review feedback (route to `code-review`)

## Capabilities

- Draft PR descriptions
- Issue templates and triage
- GitHub Actions YAML
- Branch protection rules
- Releases and tags
- CODEOWNERS, labels, projects

## Inputs

- Repo context (visibility, branch protection)
- Goal (open PR, fix workflow, etc.)

## Safety

- Don't write secrets into workflow files
- Pin Actions to SHA, not tag, for security
- Warn about `pull_request_target` and other trigger risks

## Source

Custom skill, written for this library.

## Notes

Pairs with:
- `git`
- `code-review`
- `secure-coding` (Actions security)

## Workflow

1. Confirm the goal, scope, and constraints.
2. Inspect the available context before acting.
3. Apply the skill-specific guidance in this document.
4. Verify the result and report limitations or next steps.

## Tools

- No mandatory tool unless declared in frontmatter.
- Use only project-approved tools and documented optional dependencies.

## Examples

Requests that should activate this skill include: "open a PR"; "create an issue"; "github actions".
