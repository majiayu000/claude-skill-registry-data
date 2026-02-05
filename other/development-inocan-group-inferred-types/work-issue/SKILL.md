---
name: work-issue
description: Core implementation logic for working on a single GitHub issue. Used by both /work command and /work-all subagents to ensure consistent behavior.
---

# Work Issue Skill

This skill contains the implementation logic for working on a single GitHub issue. It is loaded by:
- `/work {n}` command (direct invocation)
- `/work-all` subagents (spawned for context isolation)

## Input

This skill expects an `ISSUE_NUMBER` to be provided by the caller.

## Workflow

```
1. GET ISSUE DETAILS
2. CHECK DEPENDENCIES → If blocked, report and stop
3. GET DESIGN SPECS (if UI) → Invoke designer agent
4. IMPLEMENT → Invoke developer agent
5. COORDINATE REVIEWS → Architect (required), Designer (if UI), Tester (required)
6. HANDLE CHANGE REQUESTS → Loop until all approved
7. REPORT RESULT → Success, Blocked, or Escalated
```

---

## Step 1: Get Issue Details

```bash
gh issue view {ISSUE_NUMBER}
```

Extract:
- Title
- Acceptance criteria
- Dependencies
- Labels (UI-related?)

---

## Step 2: Check Dependencies

Parse "Depends on #X" from issue body:

```bash
gh issue view {ISSUE_NUMBER} --json body --jq '.body' | grep -oE 'Depends on #[0-9]+' | grep -oE '[0-9]+'
```

For each dependency, check if closed:

```bash
gh issue view {dep_number} --json state --jq '.state'
```

**If any dependency is OPEN:**
```
Report: "BLOCKED: Issue #{ISSUE_NUMBER} is blocked on #{dep_number}"
Stop here.
```

---

## Step 3: Get Design Specs (If UI Work)

Check if issue involves UI (labels contain "ui", "frontend", or issue mentions UI work).

If UI work needed and no design specs in comments, spawn the designer agent:

```
Use the Task tool with:
  subagent_type: "general-purpose"
  model: "sonnet"
  description: "Designer specs for issue #{ISSUE_NUMBER}"
  prompt: |
    You are the Designer agent. Load your role from .claude/agents/designer/AGENT.md

    **[Designer]**

    Add UI/UX specifications to issue #{ISSUE_NUMBER}.

    1. Read the issue: gh issue view {ISSUE_NUMBER}
    2. Review requirements and acceptance criteria
    3. Add design specs as a comment following the template in your AGENT.md
```

---

## Step 4: Implement

Update issue label:
```bash
gh issue edit {ISSUE_NUMBER} --add-label "in-progress" --remove-label "ready"
```

Spawn the developer agent:

```
Use the Task tool with:
  subagent_type: "general-purpose"
  model: "sonnet"
  description: "Implement issue #{ISSUE_NUMBER}"
  prompt: |
    You are the Developer agent. Load your role from .claude/agents/developer/AGENT.md

    **[Developer]**

    Implement issue #{ISSUE_NUMBER}.

    Context:
    - Issue: {title}
    - Acceptance criteria: {from issue body}
    - Design specs: {from designer comment, if applicable}

    1. Read the issue: gh issue view {ISSUE_NUMBER}
    2. Implement the feature following acceptance criteria
    3. Write tests for your implementation
    4. Create a PR with "Closes #{ISSUE_NUMBER}" in the body
```

Wait for developer to create PR. Get PR number from output or:
```bash
gh pr list --search "head:{ISSUE_NUMBER}-" --json number --jq '.[0].number'
```

---

## Step 5: Coordinate Reviews

Update issue label:
```bash
gh issue edit {ISSUE_NUMBER} --add-label "needs-review" --remove-label "in-progress"
```

### Architect Review (Required)

```
Use the Task tool with:
  subagent_type: "general-purpose"
  model: "sonnet"
  description: "Architect review PR #{pr_number}"
  prompt: |
    You are the Architect agent. Load your role from .claude/agents/architect/AGENT.md

    **[Architect]**

    Review PR #{pr_number} for technical quality.

    1. Read the PR: gh pr view {pr_number}
    2. Review the code changes for architecture, patterns, and quality
    3. Post a standardized review comment:
       - ✅ APPROVED - Architect (if acceptable)
       - ❌ CHANGES REQUESTED - Architect (if issues found)
```

### Designer Review (If UI Changes)

```
Use the Task tool with:
  subagent_type: "general-purpose"
  model: "sonnet"
  description: "Designer review PR #{pr_number}"
  prompt: |
    You are the Designer agent. Load your role from .claude/agents/designer/AGENT.md

    **[Designer]**

    Review PR #{pr_number} for UI/UX quality.

    1. Read the PR: gh pr view {pr_number}
    2. Check if there are UI changes
    3. If no UI changes: Post "**[Designer]** N/A - No UI changes in this PR."
    4. Otherwise post standardized review comment:
       - ✅ APPROVED - Designer
       - ❌ CHANGES REQUESTED - Designer
```

### Tester Review (Required)

```
Use the Task tool with:
  subagent_type: "general-purpose"
  model: "sonnet"
  description: "Tester verify PR #{pr_number}"
  prompt: |
    You are the Tester agent. Load your role from .claude/agents/tester/AGENT.md

    **[Tester]**

    Verify PR #{pr_number}.

    1. Read the PR: gh pr view {pr_number}
    2. Run the test suite
    3. Perform manual verification if needed
    4. Post a standardized review comment:
       - ✅ APPROVED - Tester
       - ❌ CHANGES REQUESTED - Tester
```

---

## Step 6: Handle Change Requests

Check PR comments for review status:
```bash
gh pr view {pr_number} --comments
```

**If any `❌ CHANGES REQUESTED`:**

```
Use the Task tool with:
  subagent_type: "general-purpose"
  model: "sonnet"
  description: "Address feedback PR #{pr_number}"
  prompt: |
    You are the Developer agent. Load your role from .claude/agents/developer/AGENT.md

    **[Developer]**

    Address review feedback on PR #{pr_number}.

    Feedback to address:
    {summary of requested changes}

    1. Read the PR and feedback: gh pr view {pr_number} --comments
    2. Make the requested changes
    3. Push the fixes
    4. Comment that changes have been addressed
```

After developer pushes fixes, re-request the relevant review(s).

Repeat until all required approvals are present.

---

## Step 7: Report Result

### Check for All Approvals

Required approvals (check PR comments):
- `✅ APPROVED - Architect` (always)
- `✅ APPROVED - Tester` (always)
- `✅ APPROVED - Designer` (if UI changes)

No outstanding `❌ CHANGES REQUESTED`.

### Success

If all approvals present:

```
Report: "SUCCESS: PR #{pr_number} is ready for merge"

Include:
- PR number
- Issue number
- Summary of what was implemented
```

### Blocked

If dependencies not met (from Step 2):

```
Report: "BLOCKED: Issue #{ISSUE_NUMBER} is blocked on #{dep_number}"
```

### Escalated

If developer escalated to architect, and architect also stuck:

```
Report: "ESCALATED: Issue #{ISSUE_NUMBER} requires human intervention"

Include:
- What was tried
- Where it got stuck
- Error details
```

---

## Exit States

The caller (either /work command or /work-all orchestrator) will parse the output for these indicators:

| State | Output Contains | Meaning |
|-------|-----------------|---------|
| SUCCESS | "PR #X is ready for merge" | All reviews approved, ready to merge |
| BLOCKED | "blocked on #" | Dependencies not met |
| ESCALATED | "requires human intervention" or "Escalating" | Stuck, needs human |

---

## Commands Reference

```bash
# Issue operations
gh issue view {n}
gh issue edit {n} --add-label "X" --remove-label "Y"

# PR operations
gh pr list --search "head:{issue}-"
gh pr view {n} --comments
gh pr comment {n} --body "..."

# Dependency check
gh issue view {n} --json body --jq '.body' | grep -oE 'Depends on #[0-9]+'
gh issue view {n} --json state --jq '.state'
```
