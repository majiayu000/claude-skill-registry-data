---
name: auto-update-jira-status
description: Automatically update Jira Issue status to the next stage (TODO→進行中→完了). (jira)
---

# Auto Update Jira Issue Status to Next Stage

## Instructions
Provide clear, step-by-step guidance for Claude.

**Important**: This skill uses Atlassian MCP tools to interact with Jira.

1. **Extract Information from URL**: Given a Jira Issue URL (e.g., `https://yourcompany.atlassian.net/browse/PROJ-123`), extract the cloud ID (site URL) and issue key.

2. **Get Current Issue Information**: Use `mcp__atlassian__getJiraIssue` to retrieve the current issue information:
   - cloudId: The site URL (e.g., "yourcompany.atlassian.net")
   - issueIdOrKey: The issue key (e.g., "PROJ-123")
   - Extract current status from the response

3. **Determine Next Status**:
   - Common Jira status mappings:
     * If current status name is "TODO" or "Todo" or "未着手" or "To Do" → next is "進行中" or "In Progress"
     * If current status name is "進行中" or "In Progress" or "In progress" → next is "完了" or "Done"
     * If current status name is "完了" or "Done" → skip update, return message: "Issue is already in Done status. No update needed."
   - If current status is not one of the expected values:
     * Inform the user that the current status is not part of the automatic flow
     * List the available transitions using `mcp__atlassian__getTransitionsForJiraIssue`
     * Ask the user which transition they want to execute using AskUserQuestion tool

4. **Get Available Transitions**: Use `mcp__atlassian__getTransitionsForJiraIssue` to get all available transitions for the issue:
   - cloudId: The site URL
   - issueIdOrKey: The issue key
   - Extract the list of available transitions with their IDs and target status names

5. **Find Matching Transition**: From the available transitions, find the one that matches the target next status determined in step 3:
   - Match by status name (case-insensitive comparison)
   - If exact match is not found, try partial matching (e.g., "進行中" in "進行中 (In Progress)")
   - If no matching transition is found, inform the user and list all available transitions

6. **Execute Transition**: Use `mcp__atlassian__transitionJiraIssue` to update the status:
   - cloudId: The site URL
   - issueIdOrKey: The issue key
   - transition: Object with the transition ID obtained in step 5

7. **Handle Errors**: Ensure to handle potential errors, such as:
   - Invalid URLs
   - Non-existent issues
   - Missing authentication (MCP server not configured)
   - Permission errors
   - No matching transition found
   - Network issues
   Provide clear error messages for each scenario.

8. **Confirm Success**: After successfully updating the status, verify the update using `mcp__atlassian__getJiraIssue` and confirm with a success message that includes:
   - The issue key
   - The previous status
   - The new status
   - Example: "Successfully updated issue PROJ-123: 'TODO' → '進行中'"

## Notes

- Ensure that the Atlassian MCP server is configured and authenticated.
- This skill uses the Atlassian MCP tools which are already auto-approved in settings.
- The status transition flow is flexible based on available transitions in Jira.
- Status names may vary by project configuration (Japanese vs English).
- Issues already in "Done" or "完了" status will not be modified.
- If the current status doesn't fit the automatic flow, the skill will prompt the user for manual selection.
- Jira uses workflow transitions, which may have different names than the target status.
