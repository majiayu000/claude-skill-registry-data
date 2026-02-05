---
name: update-issue-status
description: Update the status of a GitHub Issue to any available status in all linked projects using the `gh project item-edit` command. Allows interactive status selection via CLI.
supporting_files:
  - path: .claude/skills/gh-commands.md
    description: GitHub CLI commands reference for project status updates
---

# Update Issue Status

## Required Files
This skill requires the following supporting file:
- `.claude/skills/gh-commands.md`: Contains all GitHub CLI commands needed for project status updates

## Instructions
Provide clear, step-by-step guidance for Claude.

1. **Extract Information from URL**: Given a GitHub Issue URL (e.g., `https://github.com/Tasup/Tasup/issues/5`), extract the owner, repository name, and issue number.

2. **Get Project Information**: Refer to `.claude/skills/gh-commands.md` for the command to retrieve project information. Execute it to retrieve the list of all projects. Extract each project's ID and number from the JSON output for processing in subsequent steps.

3. **Get Project Item ID and Current Status for All Projects**:
   - For each project obtained in step 2, refer to `.claude/skills/gh-commands.md` for the command to retrieve project items.
   - For each project, find the item that matches the issue number and extract its ID and current status.
   - Collect all projects where the issue is found. If the issue is not found in any project, return an error: "Issue is not linked to any project."

4. **Get Field Information for All Projects**: For each project where the issue was found in step 3, refer to `.claude/skills/gh-commands.md` for the command to retrieve project fields. For each project, find the "Status" field ID and all available status options from the JSON output. If the Status field doesn't exist in any project, return an error: "Status field not found in project [PROJECT_NAME]."

5. **Present Current Status and Let User Select New Status**:
   - Display the current status of the issue in each project to the user in a text message.
   - If different projects have different current statuses, list them all.
   - Collect all unique available status options across all projects (excluding statuses that are already current in any project).
   - Use the AskUserQuestion tool with the following approach to handle more than 4 status options:

   **If there are 4 or fewer status options (excluding current statuses):**
   - Present all available statuses in a single AskUserQuestion
   - Question: "issue #NUMBER をどのステータスに変更しますか？現在のステータス: [list current statuses for each project]"
   - Header: "ステータス選択"
   - Options: List all available statuses

   **If there are more than 4 status options (excluding current statuses):**
   - First, display all available statuses in a text message to the user
   - Then ask the user which specific status they want to change to using AskUserQuestion with the first 4 most common statuses as options
   - The "Other" option will automatically be available for any status not in the initial 4
   - Common workflow statuses to prioritize: "Todo", "In progress", "In review", "Done"

6. **Update Issue Status in All Projects**: For each project where the issue was found, refer to `.claude/skills/gh-commands.md` for the command to update the issue status. Replace the placeholders with the values obtained in previous steps and the user-selected status option ID. Track which projects were successfully updated and which failed (if any).

7. **Handle Errors**: Ensure to handle potential errors, such as:
   - Invalid URLs
   - Non-existent issues
   - Issues not linked to a project
   - Missing Status field in project
   - Missing authentication scopes (project permissions)
   - Network issues
   Provide clear error messages for each scenario.

8. **Confirm Success**: Refer to `.claude/skills/gh-commands.md` for the command to verify the update. After successfully updating the status in all projects, verify the updates and confirm with a success message that includes:
   - The number of projects updated
   - The previous status and new status for each project
   - The project names
   - Example: "Successfully updated issue #5 in 2 projects:
     - Project 'Tasup Project': 'In progress' → 'Done'
     - Project 'Tasup Experiment': 'In progress' → 'Done'"
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

## Command Reference
All required GitHub CLI commands are documented in `.claude/skills/gh-commands.md`. Refer to that file for:
- Getting project information
- Listing project items
- Retrieving field information
- Updating issue status
- Verifying updates

## Notes

- Ensure that the user has the necessary permissions and authentication scopes to perform these actions.
- This skill targets **all projects** linked to the issue.
- This skill performs a **two-phase update**:
  1. First, updates the child issue status to the user-selected status
  2. Then, automatically updates parent issues that track the child issue
- Status names are case-sensitive. Common variations include:
  - "Todo" or "TODO"
  - "In Progress" or "In progress"
  - "Done"
- If an issue is linked to multiple projects, the skill will update the status in all of them to the same user-selected status.
- If the issue has different statuses across projects, all projects will be updated to the newly selected status.
- Partial failures are handled gracefully: if some projects update successfully while others fail, the success message will list both outcomes.
- Parent status is determined by aggregating the status of all child issues:
  - All Done → Parent Done
  - Any In Progress → Parent In Progress
  - All Todo → Parent Todo
  - Mixed → Parent In Progress
- Parent issues already in the correct status will not be modified to avoid unnecessary API calls.
- If a parent issue is not linked to any project, it will be skipped with a warning.
- All command examples and usage patterns are maintained in `.claude/skills/gh-commands.md`


