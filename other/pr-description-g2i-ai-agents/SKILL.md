---
name: pr-description
description: Generate a PR description for the current branch against your base branch.
---

# PR Description

## Invocation

This skill defaults to running in the `Developer` persona. If you are not already running as `Developer` (for example, the user invoked `/pr-description` directly or you are the parent agent), delegate execution to a `Developer` subagent and stop. If you are already running as `Developer`, continue with the steps below.

## Objective

Generate a copyable PR description for the current branch relative to your base branch.

## Instructions

1. Analyze the branch diff with `git diff <base-branch>...HEAD`.
2. Read recent commits with `git log <base-branch>...HEAD --oneline`.
3. If there are no branch changes relative to your base branch, stop and report that clearly.
4. Read `templates/pr-description-template.md`.
5. Fill the template with a concise title, summary, change list, testing notes, and related specs or briefs when present.
6. Output the final description inside a single fenced `markdown` block for easy copy-paste.
7. Suggest `/draft-pr` as the next step.
