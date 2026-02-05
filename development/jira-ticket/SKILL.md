---
name: jira-ticket
description: Read Jira tickets, extract requirements, summarize in developer-friendly format, optionally search codebase for related files, and update ticket status with transitions
allowed-tools: [mcp__atlassian__*, Grep, Glob, Read, TodoWrite]
---

# Skill: Jira Ticket Management

## Purpose
Intelligently read Jira tickets, understand requirements, and optionally update ticket status with context-aware automation. This skill bridges Jira project management with your codebase, enabling seamless requirement tracking and status synchronization.

## Prerequisites
- Atlassian MCP server configured in `.mcp.json.atlassian`
- Jira API authentication set up (API token and site URL)
- Valid Jira ticket ID in format: `PROJ-123`
- MCP permissions enabled in `.claude/settings.local.json`

## Workflow

### Objective
Read Jira ticket details, extract key requirements, summarize in developer-friendly format, optionally search related codebase files, and update ticket status if requested.

### Input
- **Required**: Jira ticket ID (e.g., `PROJ-456`, `WORK-123`)
- **Optional**:
  - Search codebase for related files (boolean)
  - Update status with transition (e.g., "In Progress", "Ready for Review", "Done")

### Steps

#### 1. Fetch Ticket Details
Use MCP Atlassian tools to retrieve:
- Ticket summary (title)
- Description (full requirement details)
- Acceptance criteria (if present in description or custom field)
- Current status (e.g., "To Do", "In Progress", "Done")
- Assignee (who's responsible)
- Priority and labels
- Comments (recent context)

#### 2. Extract Key Requirements
Parse the ticket content to identify:
- **Problem Statement**: What needs to be solved?
- **Technical Specifications**: Specific implementation details
- **Acceptance Criteria**: Clear definition of done
- **Dependencies**: Related tickets or systems
- **Edge Cases**: Mentioned constraints or special scenarios

#### 3. Generate Developer Summary
Create a structured summary:

```markdown
## Ticket: [TICKET-ID] - [Summary]

### Problem
[Concise description of the issue or feature request]

### Requirements
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

### Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

### Current Status
**Status**: [Current Status]
**Assignee**: [Assignee Name]
**Priority**: [Priority Level]

### Technical Notes
[Any technical specifications or implementation hints from the ticket]
```

#### 4. Search Codebase (Optional)
If requested, search for related files/components:
- Use ticket keywords to search codebase
- Identify potentially affected files
- List related components or modules
- Provide file paths and brief context

Output format:
```markdown
### Related Codebase Files
- `src/components/Button.tsx` - Button component mentioned in requirements
- `src/services/api.ts` - API service for data fetching
- `tests/integration/workflow.test.ts` - Integration tests to update
```

#### 5. Update Ticket Status (Optional)
If status update requested:
- Validate the transition is allowed (e.g., can't go from "To Do" to "Done" directly)
- Use MCP Atlassian tools to transition ticket
- Optionally add a comment with update context
- Confirm successful transition

Output:
```markdown
### Status Update
✅ Ticket transitioned from "[Old Status]" to "[New Status]"
Comment added: "[Optional context about the update]"
```

### Output
Structured ticket summary with:
1. Problem statement
2. Requirements list
3. Acceptance criteria checklist
4. Current status and metadata
5. Technical notes
6. Optional: Related codebase files
7. Optional: Status update confirmation

## Error Handling

### Ticket Not Found (404)
- Verify ticket ID format (should be `PROJECT-NUMBER`)
- Check Jira project permissions
- Confirm MCP Atlassian server is connected

### Authentication Issues
- Validate `JIRA_API_TOKEN` environment variable is set
- Confirm `JIRA_SITE_URL` is correct (e.g., `https://yourcompany.atlassian.net`)
- Check API token hasn't expired

### Invalid Transition
- List available transitions for current ticket status
- Suggest valid next states
- Explain workflow restrictions

### Connection Timeout
- Check network connectivity
- Verify MCP SSE endpoint is accessible: `https://mcp.atlassian.com/v1/sse`
- Retry with exponential backoff

## Usage Examples

### Example 1: Basic Ticket Read
```bash
/skill jira-ticket PROJ-456
```
Output: Structured summary of ticket PROJ-456 with problem, requirements, and acceptance criteria.

### Example 2: Read Ticket and Search Codebase
```bash
/skill jira-ticket WORK-789 --search-codebase
```
Output: Ticket summary + list of related files in the codebase.

### Example 3: Read and Update Status
```bash
/skill jira-ticket PROJ-123 --status "In Progress"
```
Output: Ticket summary + confirmation of status update to "In Progress".

### Example 4: Full Workflow
```bash
/skill jira-ticket WORK-456 --search-codebase --status "Ready for Review"
```
Output: Complete ticket summary + related files + status update confirmation.

## Best Practices

1. **Read Before Implementation**: Always fetch ticket details before starting work
2. **Validate Acceptance Criteria**: Ensure you understand all criteria before marking complete
3. **Update Status Promptly**: Keep ticket status in sync with actual progress
4. **Add Context to Comments**: When updating status, add meaningful comments about what was done
5. **Link Code to Tickets**: Reference ticket IDs in commit messages and PR descriptions

## Troubleshooting

### Problem: "MCP server not found"
**Solution**: Ensure `.mcp.json.atlassian` exists and contains valid Atlassian MCP configuration.

### Problem: "Authentication failed"
**Solution**: Set environment variables:
```bash
export JIRA_API_TOKEN="your_api_token_here"
export JIRA_SITE_URL="https://yourcompany.atlassian.net"
```

### Problem: "Ticket not accessible"
**Solution**: Verify you have read permissions for the Jira project. Check with your Jira admin.

### Problem: "Transition not allowed"
**Solution**: Check your Jira workflow. Some transitions require specific conditions (e.g., assignee must be set, subtasks must be complete).

## Integration Tips

- **With Git Commits**: Reference ticket IDs in commit messages: `git commit -m "PROJ-123: Implement user authentication"`
- **With PRs**: Link Jira tickets in PR descriptions for traceability
- **With CI/CD**: Use ticket status to gate deployments (e.g., only deploy when ticket is "Ready for Release")
- **With Design QA**: Combine with `design-qa` skill to ensure Figma designs match ticket requirements
