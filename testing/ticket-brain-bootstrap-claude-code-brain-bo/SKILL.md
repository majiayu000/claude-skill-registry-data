---
name: ticket
description: Create a ticket/issue description with evidence-backed proof sections. Reads claude/templates.md for the template format. Saves to claude/tasks/ticket-<slug>.md.
---

# Ticket Skill

Create a well-structured ticket/issue description backed by evidence from the codebase.

## Usage

```
/ticket Bug: login fails when email has uppercase letters
/ticket Feature: add pagination to the orders list endpoint
```

## Protocol

### 1. Parse the Request
- Bug or Story?
- Which services/files are affected?
- Current vs expected behavior (for bugs)?

### 2. Research the Codebase
- Read relevant source files
- Collect evidence: file paths + line numbers
- Find root cause (for bugs) or integration points (for features)

### 3. Write the Ticket

Read `claude/templates.md` for the ticket template format.

For bugs, include:
- Steps to reproduce (exact commands or UI steps)
- Current behavior (with evidence)
- Expected behavior
- Root cause (file path + line number)
- Proposed fix (specific files to change)

For features, include:
- Problem statement / user story
- Acceptance criteria (testable, not vague)
- Technical approach (specific files/APIs to change)
- Out of scope (explicit boundaries)

### 4. Quality Rules
- Every claim must be backed by evidence (file path + line number)
- Acceptance criteria must be testable
- Proposed solution must reference exact files to change
- No vague statements like "improve performance" — be specific

### 5. Save and Report
Save to `claude/tasks/ticket-<slug>.md` where `<slug>` is a kebab-case summary.
Tell the user the exact file path.
