---
name: sflow-jira-work
description: List Jira stories assigned to the authenticated user or retrieve a specific Jira issue using Singularity Flow's direct Jira REST client. Use only on explicit request.
disable-model-invocation: true
argument-hint: "[WORK-ID] [--project KEY] [--type Story]"

---
# Jira work through Singularity Flow

<!-- sflow-output-contract: concise-relay -->
**Output contract:** Relay requested CLI fields or output faithfully; preserve warnings/errors and only the explanations required below.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

No MCP server or IDE Jira plugin is used.

- Check the connection with `/sf-jira-status`.
- List assigned work with `/sf-jira-assigned` (`singularity-flow jira assigned`; `singularity-flow jira list` remains an alias).
- Browse active and future sprint Stories without backlog with `/sf-jira-board`.
- Make a separately confirmed status, assignee, priority, sprint, or comment change with `/sf-jira-update`.
- Retrieve a specific item with `singularity-flow jira pull <WORK-ID>` (`show` remains an alias).
- Discover custom field IDs with `singularity-flow jira fields --query acceptance`, `--query story points`, or `--query sprint`.
- Start selected Jira work with `singularity-flow start <WORK-ID> --jira`.

Jira access requires `JIRA_BASE_URL`, `JIRA_EMAIL`, and `JIRA_API_TOKEN`. Never request the user's Atlassian password, display the token, or store credentials in Git.
