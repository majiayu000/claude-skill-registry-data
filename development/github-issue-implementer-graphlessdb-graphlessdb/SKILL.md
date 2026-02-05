---
name: github-issue-implementer
description: You are an implementer of GitHub issues.  You are an Agent who has been assigned an issue to work on.
---

This skill guides the process to implement a GitHub issue.

## General notes

- You do NOT need to ask me to proceed at any stage, you should work with autonomy as much as possible unless explicity asked otherwise.
- You MUST carry out each implementation step in order, ensure that each step is successful before continuing to the next.
- You MUST use a git worktree to implement an issue.

## Workflow

- Ensure you have run ./utils/help.sh script to learn what scripts are available to use.
- Ensure you are on the main git branch.
- Ensure you have the pulled the latest from remote.
- Ensure the branch is in a clean state.
- Ensure you understand which issue id you should be working on, if you have not been explicitly told then stop working on this task.
- Update the GitHub issue so that its status is "In Progress" if it wasn't already.
- Add a comment onto the GitHub issue detailing what agent you are and the date / time that you have begun working on the issue.
- Create a new git worktree under the folder /tmp/claude/ for working on the issue, use a name in the format "{PROJECT_NAME}-issue-{ISSUE_ID}".
- Use the issue id to read the information such as title, description or comments from the issue to determine what your task is.
- Carry out and complete the task.
- Clean up the local git worktree.
- Carry out a review of any errors that occurred when calling scripts during this task and explain how you managed to correct your understanding usage of the script, i.e. recommend changes to the way you used it for next time. Add the review summary as a comment on the GitHub issue.
- Update the GitHub issue so that its status is "Todo", if human interaction is required because a PR needs to be merged or the issue could not be fully completed then update the GitHub issue by adding the "help wanted" label to it.
