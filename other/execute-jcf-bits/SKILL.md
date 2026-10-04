---
name: execute
description: Execute a Linear issue
allowed-tools: ToolSearch, mcp__linear__list_issues, mcp__linear__get_issue, mcp__linear__update_issue, Read, Glob, Grep, Bash, Edit, Write, AskUserQuestion
---

Execute work for a Linear issue.

## Usage

- `/execute` - List open issues, select one
- `/execute BITS-17` - Execute specific issue

## Process

1. Load Linear tools via ToolSearch
2. If no argument: list Bits team issues (Todo/In Progress), present via AskUserQuestion
3. Fetch full issue details
4. Update status to "In Progress"
5. Follow execution steps:
   - Understand the requirements
   - Plan the implementation
   - Present plan for approval
   - Implement changes
   - Verify with tests
6. On completion: update status to "Done"
