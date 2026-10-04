---
name: QcommitPassing
description: Test fixture for Qcommit policy compliance — all required sentences present, no forbidden phrases in policy.
---

# Qcommit — Passing Fixture

## Role
Creates natural git commits that show no trace of AI authorship.

## Prohibited Items (Absolute Rules)
- **Never add co-authored-by lines**
- No AI-related phrases
- No emoji usage

## Execution Procedure (Mandatory Delegation)

**ABSOLUTE RULE:** Do not run raw commit operations directly when the active client has an available commit executor agent.

- Claude: ALL git operations MUST be delegated to the `Ecommit-executor` agent via the Agent tool.
- Codex native: use the native `Ecommit-executor` agent when available.

### Step 1: Delegate to Ecommit-executor
Call the `Ecommit-executor` agent through the agent adapter with the following information:
- Project path
- Whether the user requested push
- Any specific commit message hints from context

The `Ecommit-executor` agent handles everything: status check, diff analysis, commit message writing, staging, committing, and optionally pushing.

### Step 2: Report Results
After the agent completes, report the commit hash and changed files to the user.

## Will
- Analyze changes and write a natural commit message
- Match the project's commit style
- Prevent staging of sensitive files

## Will Not
- Add Co-Authored-By
- Include AI-related phrases or traces
- Run git push (unless explicitly requested by the user)
- Create an empty commit when there are no changes
