---
name: auto-update-issue-status-from-todo-to-in-progress
description: Automatically update GitHub Issue status to the next stage (Todo→In Progress→Done) in all linked projects.
---

# Auto Update Issue Status to Next Stage

## Instructions
Provide clear, step-by-step guidance for Claude.

**Important**: All GitHub CLI commands used in this skill are defined in `.claude/skills/gh-commands.md`. Refer to that file for command syntax and usage examples.

1. **Extract Information from URL**: Given a GitHub Issue URL (e.g., `https://github.com/Tasup/Tasup/issues/5`), extract the owner, repository name, and issue number.

2. **Get Project Information**: Refer to `.claude/skills/gh-commands.md` for the "Get project information" command. Execute it to retrieve the list of all projects. Extract each project's ID and number from the JSON output for processing in subsequent steps.

3. **Get Project Item ID and Current Status for All Projects**:
   - For each project obtained in step 2, refer to `.claude/skills/gh-commands.md` for the "Get project item ID" command.
   - For each project, find the item that matches the issue number and extract its ID.
   - Parse each item's `fieldValues` to find the current status value.
   - Collect all projects where the issue is found. If the issue is not found in any project, return an error: "Issue is not linked to any project."

4. **Get Field Information for All Projects**: For each project where the issue was found in step 3, refer to `.claude/skills/gh-commands.md` for the "Get field information" command. For each project, find the "Status" field and extract:
   - Field ID
   - All status option IDs and their names (Todo, In Progress, Done)
   - If the Status field doesn't exist in any project, return an error: "Status field not found in project [PROJECT_NAME]."

5. **Determine Next Status**:
   - If current status is "Todo", next status is "In Progress"
   - If current status is "In Progress", next status is "Done"
   - If current status is "Done", skip the update and return a message: "Issue is already in Done status. No update needed."
   - If current status is not one of the expected values (Todo/In Progress/Done):
     * Inform the user that the current status "[STATUS_NAME]" is not part of the automatic Todo→In Progress→Done flow
     * Automatically invoke the `update-issue-status` skill by using the Skill tool: `Skill(update-issue-status-from-todo-to-in-progress)`
     * The update-issue-status skill will present all available statuses to the user for interactive selection
     * Do NOT return an error - instead, gracefully transition to the interactive skill

6. **Update Issue Status in All Projects**: For each project where the issue was found, refer to `.claude/skills/gh-commands.md` for the "Update issue status" command. Execute it with the values obtained in previous steps to update the status to the next stage in all linked projects. Track which projects were successfully updated and which failed (if any).

7. **Handle Errors**: Ensure to handle potential errors, such as:
   - Invalid URLs
   - Non-existent issues
   - Issues not linked to a project
   - Missing Status field in project
   - Missing authentication scopes (project permissions)
   - Network issues
   Provide clear error messages for each scenario.

   Note: Statuses outside the Todo→In Progress→Done flow are handled in step 5 with a suggestion to use the alternative skill, not as errors.

8. **Confirm Success**: Refer to `.claude/skills/gh-commands.md` for the "Verify update" command. After successfully updating the status in all projects, verify the updates and confirm with a success message that includes:
   - The number of projects updated
   - The previous status and new status for each project
   - The project names
   - Example: "Successfully updated issue #5 in 2 projects:
     - Project 'Tasup Project': 'Todo' → 'In Progress'
     - Project 'Tasup Experiment': 'TODO' → 'In progress'"
   - If some projects failed to update, list both successful and failed projects with reasons for failures.

9. **Update Parent Issue Status**:
   After successfully updating the child issue status, check and update the parent issue if applicable.

   a. **Get Parent Issue**:
      - Refer to `.claude/skills/gh-commands.md` for the "Get parent issue (REST API - Recommended)" command.
      - Execute `gh api /repos/OWNER/REPO/issues/ISSUE_NUMBER/parent` to retrieve the parent issue.
      - Extract the parent issue number from the response (`number` field).
      - If there is no parent issue (404 error or empty response), skip to step 10 with message: "No parent issue found to update."

   b. **Get All Projects for Parent Issue**:
      - For the parent issue, get project information for all linked projects (same as steps 2-4 for the child issue).
      - Retrieve project item IDs, current statuses, and field information for all projects.

   c. **Check All Child Issues Status**:
      - Refer to `.claude/skills/gh-commands.md` for the "Get child issues (REST API - Recommended)" command.
      - Execute `gh api /repos/OWNER/REPO/issues/PARENT_ISSUE_NUMBER/sub_issues` to get all child issues tracked by the parent issue.
      - For each child issue, get its current status from all projects where it exists by using the same project item retrieval logic as in steps 2-4.
      - Determine the appropriate parent status based on child statuses:
        - If ALL child issues are "Done" in ALL projects, parent should be "Done"
        - If ANY child issue is "In Progress" or "In progress" in ANY project, parent should be "In Progress" (or "In progress" depending on project naming)
        - If ALL child issues are "Todo" or "TODO" in ALL projects, parent should be "Todo" (or "TODO" depending on project naming)
        - Otherwise, parent should be "In Progress" (mixed statuses)

   d. **Update Parent Issue Status in All Projects**:
      - For each project where the parent issue exists, compare the determined status with the current parent status.
      - If they are the same, skip the update for that project.
      - If they are different, update the parent status to the determined status.
      - Track which projects were successfully updated and which failed (if any).

   e. **Verify Parent Updates**: Verify the parent issue updates using the "Verify update" command.

10. **Final Confirmation**: Provide a comprehensive summary that includes:
    - Child issue status update (old status → new status for each project)
    - Number of projects updated for the child issue
    - Parent issue information (if found):
      - Parent issue number and title
      - Number of projects updated for the parent issue
      - Old status → new status for each project
      - Any projects where parent status was already correct (no update needed)
    - Any warnings or errors encountered
    - Example: "Successfully updated issue #42 'SubIssue3333' from 'Todo' to 'In Progress' in 2 projects. Parent issue #4 'Ready' updated from 'Todo' to 'In Progress' in 2 projects."

## Notes

- Ensure that the user has the necessary permissions and authentication scopes to perform these actions.
- This skill targets **all projects** linked to the issue.
- The status transition flow is strictly: **Todo → In Progress → Done**
- Issues already in "Done" status in all projects will not be modified.
- Status names are case-sensitive. Common variations include:
  - "Todo" or "TODO"
  - "In Progress" or "In progress"
  - "Done"
- **For issues with statuses outside this flow** (e.g., "In review", "Backlog", "Ready"), this skill will suggest using the `update-issue-status` skill instead, which supports manual selection of any available status.
- If an issue is linked to multiple projects, the skill will update the status in all of them.
- If the issue has different statuses across projects (e.g., "Todo" in one, "In Progress" in another), each project will be advanced to its respective next status.
- Partial failures are handled gracefully: if some projects update successfully while others fail, the success message will list both outcomes.
