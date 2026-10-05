---
name: issues
description: Interact with GitHub issues - create, list, and view issues. 
category: Document Processing
source: antigravity
tags: [ai, workflow, document, rag]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/issues
---


Interact with GitHub issues - create, list, and view issues.

## When to Use
- The user wants to create, list, inspect, or otherwise work with GitHub issues.
- The task involves issue intake or repository issue management through the GitHub CLI workflow.
- You need a guided issue flow that gathers titles, descriptions, and action selection before running commands.

## Instructions

This command helps you work with GitHub issues using the `gh` CLI.

### Step 1: Determine Action

Use AskUserQuestion to ask what the user wants to do:

**Question:**
- question: "What would you like to do with GitHub issues?"
- header: "Action"
- multiSelect: false
- options:
  - label: "Create new issue"
    description: "Open a new issue with title, body, and optional labels"
  - label: "List issues"
    description: "View open issues in the current repository"
  - label: "View issue"
    description: "See details of a specific issue by number"

---

## If "Create new issue" selected:

### Step 2a: Get Issue Title

Use AskUserQuestion to get the issue title:

**Question:**
- question: "What's a short, scannable title for this issue? Keep it brief (5-10 words max) - details go in the body. (Use 'Other' to type your title)"
- header: "Title"
- multiSelect: false
- options:
  - label: "I'll type a title"
    description: "Enter a concise title like 'Login button unresponsive' or 'Add dark mode support'"

**Title guidelines:**
- Keep titles SHORT and scannable (5-10 words max)
- Good: "Fix broken password reset flow"
- Bad: "When I try to reset my password and click the button nothing happens and I get an error"
- The description/body is where details belong, not the title

If the user provides a long title, help them shorten it and move the details to the body.

### Step 3a: Get Issue Body

Use AskUserQuestion to gather the issue body content:

**Question 1 - Issue type context:**
- question: "What type of issue is this?"
- header: "Type"
- multiSelect: false
- options:
  - label: "Bug"
    description: "Something broken that needs fixing"
  - label: "Enhancement"
    description: "Improvement to existing functionality"
  - label: "New feature"
    description: "Brand new functionality"
  - label: "Task"
    description: "General work item or chore"

**Question 2 - Description:**
- question: "Now provide the full details. This is where you explain context, background, and specifics that didn't fit in the title. (Use 'Other' to type your description)"
- header: "Description"
- multiSelect: false
- options:
  - label: "I'll describe it in detail"
    description: "Provide context, steps, examples, and any relevant information"

The user will select "Other" here to provide their full description.

**Description guidelines:**
- This is where ALL the detail goes - be thorough
- Include context: what were you doing, what's the background?
- Include specifics: error messages, URLs, versions, etc.
- The more detail here, the better - unlike the title which should be brief

**Question 3 - For bugs, ask about reproduction:**
If issue type is "Bug", use AskUserQuestion:

- question: "Can you provide steps to reproduce this bug? (Use 'Other' to type steps)"
- header: "Repro steps"
- multiSelect: false
- options:
  - label: "Provide steps"
    description: "I'll describe how to reproduce the issue"
  - label: "Not reproducible"
    description: "The bug is intermittent or hard to reproduce"

**Question 4 - Expected vs actual behavior (for bugs):**
If issue type is "Bug", use AskUserQuestion:

- question: "What did you expect to happen vs what actually happened? (Use 'Other' to describe)"
- header: "Behavior"
- multiSelect: false
- options:
  - label: "Describe behavior"
    description: "I'll explain expected vs actual behavior"

### Step 4a: Get Labels (Optional)

Use AskUserQuestion to select labels:

- question: "Which labels should we add? (if any)"
- header: "Labels"
- multiSelect: true
- options:
  - label: "bug"
    description: "Something isn't working"
  - label: "enhancement"
    description: "New feature or request"
  - label: "documentation"
    description: "Improvements to docs"
  - label: "good first issue"
    description: "Good for newcomers"

### Step 5a: Create the Issue

Construct the issue body based on the type:

**For Bug reports:**
```
## Description
[User's description]

## Steps to Reproduce
[User's reproduction steps or "Not easily reproducible"]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]
```

**For Feature requests/Enhancements:**
```
## Description
[User's description]

## Use Case
[Why this would be useful]
```

**For Tasks/Other:**
```
## Description
[User's description]
```

Run the gh command to create the issue:
```bash
gh issue create --title "[title]" --body "[constructed body]" --label "[labels]"
```

Report the issue URL back to the user.

---

## If "List issues" selected:

### Step 2b: Filter Options

Use AskUserQuestion to determine filtering:

- question: "
