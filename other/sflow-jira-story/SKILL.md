---
name: sflow-jira-story
description: Pull one Jira user story by key through Singularity Flow's direct Jira REST client and present its normalized details without changing Jira or Git.
disable-model-invocation: true
argument-hint: "<JIRA-ID> [--json]"

---
# Pull a Jira user story

<!-- sflow-output-contract: concise-relay -->
**Output contract:** Relay requested CLI fields or output faithfully; preserve warnings/errors and only the explanations required below.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

1. Require an explicit Jira key; do not invent or guess one.
2. Run `singularity-flow jira pull <JIRA-ID>` with supplied arguments.
3. Report the exact summary, type, project, status, priority, assignee, reporter, parent, story points, sprint, dates, labels, components, description, acceptance criteria, subtasks, linked issues, and attachment metadata that were returned.
4. Clearly label fields that are absent. Do not infer missing acceptance criteria or requirements.
5. Do not create a branch, write repository files, modify Jira, or expose credentials.
6. When the user explicitly asks to begin work on the story, use `/sf-start <JIRA-ID> --jira`; that operation persists `source.json` and `USER-STORY.md` on the exact Jira-ID branch.

Jira access requires `JIRA_BASE_URL`, `JIRA_EMAIL`, and `JIRA_API_TOKEN`. Optional custom-field IDs can be configured with `SINGULARITY_FLOW_JIRA_ACCEPTANCE_FIELD`, `SINGULARITY_FLOW_JIRA_STORY_POINTS_FIELD`, and `SINGULARITY_FLOW_JIRA_SPRINT_FIELD`.
