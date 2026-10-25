---
name: ami-detect-pr-conflicts
description: Must be triggered before creating or proposing any Pull Request. Identifies overlapping changes and merge conflicts with other open PRs.
allowed-tools: Bash, Read, Grep
---

# Skill: PR Conflict Detector

When invoked, act as a Repository Coordinator to identify potential conflicts with parallel work streams.

## Workflow

1. **Fetch Open PRs:**
   - Run `git fetch` to ensure remote tracking branches and tags are updated locally.
   - Use GitHub CLI (e.g., `gh pr list --state open`) or git commands to identify other open Pull Requests.

2. **Analyze File Overlaps & Stack Dependencies:**
   - For each open PR, use `gh pr view <PR_NUMBER> --json files,baseRefName,headRefName` or similar git commands to see which files they modify and their branch topology.
   - Compare the list of files modified in the other open PRs with the files modified in the current local PR.
   - **Stacked PR Awareness:** Check branch relationships. If the current PR's base branch (`baseRefName`) matches another open PR's head branch (`headRefName`), or vice-versa, recognize this as a **Stacked PR hierarchy** (parent-child dependent branches).

3. **Determine Conflicts:**
   - If there is no overlap in files, or no other open PRs exist, let the user know and terminate the skill.
   - If there is an overlap in files between two branches that form a parent-child relationship in a Stacked PR hierarchy, categorize the overlap as an **Expected Stack Dependency** rather than a parallel git merge conflict. Inform the user without triggering a conflict warning or blocking workflow.
   - If there is an overlap between independent parallel branches, alert the user and analyze whether the overlapping modifications will cause a direct git merge conflict or a logical conflict.

4. **Reporting:**
   - Provide a clear warning listing the parallel PRs (PR number, Title, Author and Date) that touch the same files.
   - Analyze the degree of conflict for each PR and file (high, medium, low).

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
