---
name: sop-builder
version: 1.0.0
category: Operations & Systems
domain: standard-operating-procedures
author: Matt Warren
license: MIT
status: production
updated: 2026-02-07
activation_triggers:
  - "create an SOP"
  - "standard operating procedure"
  - "document this process"
  - "write a process doc"
  - "how to guide"
  - "runbook"
  - "process documentation"
  - "step by step guide"
  - "onboarding doc"
tools: []
---

# SOP Builder

Create clear, repeatable standard operating procedures for any business process. Turn tribal knowledge into documentation anyone can follow.

## Purpose

SOPs are the foundation of a scalable business. If a process lives in one person's head, it's a liability. This skill extracts, structures, and documents any business process into a format that a new hire could follow on day one.

## Workflow

### Step 1: Identify the Process

Ask the user:
- What process do you want to document?
- Who currently does this? (role, not person)
- How often does it happen? (daily, weekly, per-event)
- What triggers it? (customer request, scheduled, event-based)
- What does "done" look like?

### Step 2: Extract the Steps

Walk through the process step by step:
- Ask "What happens first?"
- For each step: "Then what?" and "What could go wrong here?"
- Identify decision points: "If X, do Y. If not, do Z."
- Note tools, logins, or systems used at each step
- Capture time estimates per step

### Step 3: Structure the SOP

```markdown
# [Process Name] — Standard Operating Procedure

**Owner:** [Role]
**Frequency:** [How often]
**Trigger:** [What starts this process]
**Estimated Time:** [X minutes/hours]
**Last Updated:** [Date]

## Prerequisites
- [ ] [Access/tool/permission needed]
- [ ] [Information needed before starting]

## Steps

### 1. [Step Name]
**Action:** [What to do]
**Tool:** [System/app used]
**Notes:** [Tips, common mistakes, edge cases]

### 2. [Step Name]
...

## Decision Points

### If [condition]:
→ Do [action A]

### If [other condition]:
→ Do [action B]

## Quality Checklist
- [ ] [Verification step 1]
- [ ] [Verification step 2]
- [ ] [Verification step 3]

## Troubleshooting
| Problem | Cause | Solution |
|---------|-------|----------|
| [Issue] | [Why] | [Fix]    |

## Escalation
If [condition], contact [role/person] via [channel].
```

### Step 4: Add Context

For each step, include:
- **Why** this step matters (not just what to do)
- **Screenshots or examples** (suggest where the user should add them)
- **Common mistakes** to avoid
- **Time estimate** for that step

### Step 5: Review and Refine

Ask the user:
- Does this match how you actually do it?
- Are there edge cases I'm missing?
- Who should own this SOP?
- How should updates be tracked?

## Output Format

Complete SOP document in markdown, ready to paste into Notion, Google Docs, or a wiki.

## Constraints

- Every step must be specific enough for someone unfamiliar with the process
- Never assume the reader knows jargon — define terms or link to glossary
- Include the "why" for non-obvious steps
- Flag steps that require specific permissions or access
- Keep steps atomic — one action per step, not compound instructions
- SOPs should be living documents — include a "Last Updated" field and review schedule
