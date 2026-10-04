---
name: prompt
description: Develop a detailed feature plan and create a Linear issue
allowed-tools: ToolSearch, mcp__linear__create_issue, Read, Glob, Grep, AskUserQuestion
---

Develop a detailed plan for a feature or task, then capture it in Linear.

## Usage

`/prompt <brief description>`

## Process

### 1. Understand the Goal

Ask clarifying questions:

- What problem does this solve?
- Who is affected?
- What does success look like?

### 2. Explore the Codebase

Use Glob, Grep, and Read to:

- Find relevant files and modules
- Understand existing patterns
- Identify what needs to change

### 3. Define Success Criteria

Work with the user to establish:

- Specific, testable outcomes
- Edge cases to handle
- What's explicitly out of scope

### 4. Outline the Approach

Document:

- Files that need modification
- New components or modules required
- Dependencies or prerequisites
- Potential risks or complications

### 5. Present the Plan

Summarise the plan in markdown with:

- **Goal**: One sentence summary
- **Success criteria**: Bullet list
- **Files involved**: With brief notes on changes
- **Approach**: Step-by-step implementation plan
- **Open questions**: Anything still unclear

### 6. Create Linear Issue

Once the user approves the plan:

1. Load Linear tools via ToolSearch
2. Create issue with:
   - Title from the goal
   - Full plan as markdown description
   - Team: Bits
   - Priority: Medium (unless user specifies otherwise)
3. Return the issue identifier and URL

## Important

The value is in the discovery process, not just creating a ticket. Take time to understand the problem and explore the codebase before proposing a plan.
