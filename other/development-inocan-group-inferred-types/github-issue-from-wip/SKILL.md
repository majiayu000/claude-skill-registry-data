---
name: github-issue-from-wip
description: Create a GitHub issue from work-in-progress by analyzing changes against the base branch
---

# GitHub Issue from Work-in-Progress Skill

Creates a GitHub issue describing work that has already been done (or is in progress) as if it hadn't been done yet. Useful for retroactively creating issues for tracking purposes.

## Workflow

### 1. Get Branch Info

Run `gbinfo` to get branch information as JSON:
```bash
gbinfo
```

Returns:
```json
{
  "current_branch": "feature-branch",
  "default_branch": "main",
  "ancestor_branch": "develop"  // optional, may not exist
}
```

### 2. Determine Base Branch

Choose the base branch for comparison:
- If `ancestor_branch` exists in the gbinfo output: use `ancestor_branch`
- If `ancestor_branch` does not exist: use `default_branch`

Store this as `{base}` for the following steps.

### 3. Gather Work Context

Run this git command to understand the work that has been done:

```bash
git diff {base_branch}
```

### 4. Analyze and Synthesize

Review all gathered context and create a summary that:
- Identifies the purpose/intent of the changes
- Lists the key modifications made
- Frames everything in **future tense** as work to be done

**Important:** Write the issue to describe the **problem or need**, not the solution. Issues should focus on what's wrong or what's needed, while PRs describe the fix. Transform completed work into problem statements:
- "Added feature X" → "Need feature X" or "Support for X"
- "Fixed bug where Y crashed" → "Y crashes when..." or "Bug: Y fails under..."
- "Refactored Z for performance" → "Z is slow" or "Performance issue in Z"

### 5. Hand Off to GitHub Issue Skill

After gathering and analyzing the context, invoke the `github-issue` skill using the Skill tool.

Provide this context to the skill:
- A description of what needs to be done (framed in future tense)
- Key technical details from the diff that inform the implementation
- Any relevant file paths that will be affected

The `github-issue` skill will handle:
- Template discovery
- Creating diagrams if needed
- Drafting and reviewing the issue with the user
- Creating the issue on GitHub
