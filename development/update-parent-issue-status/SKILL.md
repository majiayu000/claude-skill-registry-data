---
name: update-parent-issue-status
description: Update the status of all parent issues (tracked in issues) when a child issue status changes. (project)
---

# Update Parent Issue Status

## Overview
This skill updates both the child issue status (Todo → In Progress) and automatically updates parent issue statuses based on the aggregate status of all their child issues.

## Workflow
1. Update the child issue status from Todo to In Progress
2. Automatically find and update all parent issues that track this child issue
3. Parent status is determined by aggregating all child issue statuses

## Instructions
Provide clear, step-by-step guidance for Claude.

**Important**: All GitHub CLI commands used in this skill are defined in `.claude/skills/gh-commands.md`. Refer to that file for command syntax and usage examples.

1. **Extract Information from URL**: Given a GitHub Issue URL (e.g., `https://github.com/Tasup/Tasup/issues/33`), extract the owner, repository name, and issue number.

2. **Update Child Issue Status (Todo → In Progress)**:
   - Get the child issue's current project information using the "Get project information" command from `.claude/skills/gh-commands.md`
   - Get the project item ID and current status for the child issue
   - Get field information to find the "Status" field and "In Progress" option ID
   - If the current status is already "In Progress", skip this step
   - If the current status is "Todo", update it to "In Progress" using the "Update issue status" command
   - Verify the update was successful
   - If the update fails, stop here and report the error

3. **Get Parent Issue**:
   - Refer to `.claude/skills/gh-commands.md` for the "Get parent issue (REST API - Recommended)" command.
   - Execute the REST API call to retrieve the parent issue that tracks the current issue.
   - Extract the parent issue number from the response (`number` field).
   - If there is no parent issue (404 error or empty response), complete the workflow with message: "Child issue updated successfully. No parent issue found to update."

4. **Update Parent Issue Status**:
   For the parent issue found in step 3, perform the following steps:

   a. **Get Project Information**: Refer to `.claude/skills/gh-commands.md` for the "Get project information" command. Execute it to retrieve the list of projects and extract the first project's ID and number from the JSON output.

   b. **Get Project Item ID and Current Status**:
      - Refer to `.claude/skills/gh-commands.md` for the "Get project item ID" command.
      - Find the item that matches the parent issue number and extract its ID.
      - Parse the item's `fieldValues` to find the current status value.
      - If the parent issue is not found in the project items, log a warning: "Parent issue #X is not linked to any project. Skipping." and continue to the next parent issue.

   c. **Get Field Information**: Refer to `.claude/skills/gh-commands.md` for the "Get field information" command. Find the "Status" field and extract:
      - Field ID
      - All status option IDs and their names (Todo, In Progress, Done)
      - If the Status field doesn't exist, log a warning: "Status field not found in project for parent issue #X. Skipping." and continue to the next parent issue.

   d. **Check All Child Issues Status**:
      - Refer to `.claude/skills/gh-commands.md` for the "Get child issues (REST API - Recommended)" command.
      - Execute `gh api /repos/OWNER/REPO/issues/PARENT_ISSUE_NUMBER/sub_issues` to get all child issues tracked by the parent issue.
      - For each child issue, get its current status from all projects where it exists.
      - Determine the appropriate parent status based on child statuses:
        - If ALL child issues are "Done" in ALL projects, parent should be "Done"
        - If ANY child issue is "In Progress" or "In progress" in ANY project, parent should be "In Progress" (or "In progress" depending on project naming)
        - If ALL child issues are "Todo" or "TODO" in ALL projects, parent should be "Todo" (or "TODO" depending on project naming)
        - Otherwise, parent should be "In Progress" (mixed statuses)

   e. **Update Parent Issue Status**:
      - Compare the determined status with the current parent status.
      - If they are the same, skip the update and log: "Parent issue #X is already in the correct status. No update needed."
      - If they are different, refer to `.claude/skills/gh-commands.md` for the "Update issue status" command.
      - Execute it with the values obtained in previous steps to update the parent status.

   f. **Verify Update**: Refer to `.claude/skills/gh-commands.md` for the "Verify update" command. After successfully updating the status, verify the update.

5. **Handle Errors**: Ensure to handle potential errors for each parent issue, such as:
   - Invalid URLs
   - Non-existent issues
   - Issues not linked to a project
   - Missing Status field in project
   - Missing authentication scopes (project permissions)
   - Network issues
   - GraphQL API errors
   Provide clear error messages for each scenario and continue processing other parent issues if one fails.

6. **Confirm Success**: After processing all issues (child and parents), provide a summary message that includes:
   - Child issue status update result (old status → new status)
   - Total number of parent issues found
   - Number of parent issues successfully updated
   - Number of parent issues skipped (with reasons)
   - List of updated parent issues with their previous and new statuses
   - Example: "Child issue #33 updated from 'Todo' to 'In Progress'. Successfully updated 1 parent issue: #4 from 'Todo' to 'In Progress'."

## Notes

- Ensure that the user has the necessary permissions and authentication scopes to perform these actions.
- This skill performs a **two-phase update**:
  1. First, updates the child issue status from Todo to In Progress
  2. Then, updates all parent issues that track the child issue
- This skill processes **the parent issue** that tracks the current issue (GitHub supports single-level parent-child relationships).
- Parent status is determined by aggregating the status of all child issues:
  - All Done → Parent Done
  - Any In Progress → Parent In Progress
  - All Todo → Parent Todo
  - Mixed → Parent In Progress
- Parent issues already in the correct status will not be modified to avoid unnecessary API calls.
- The skill handles multiple levels of hierarchy (grandparent issues are not automatically updated, only direct parents).
- If a parent issue is not linked to any project, it will be skipped with a warning.
- If the child issue update fails, the parent issue updates will not be attempted.
