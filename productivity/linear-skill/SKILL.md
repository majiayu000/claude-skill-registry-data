---
name: linear
description: Manage Linear projects, issues, and tasks via the bundled Node CLI and the official Linear API. Use when you need to read, create, update, or organize Linear issues, projects, teams, milestones, comments, cycles, labels, and documents.
metadata: {"gracebot":{"always":false,"emoji":"📐","homepage":"https://github.com/MaTriXy/linear-skill","requires":{"bins":["node","npm"],"env":["LINEAR_API_KEY"]},"primaryEnv":"LINEAR_API_KEY","install":[{"id":"node-brew","kind":"brew","formula":"node","bins":["node","npm"],"label":"Install Node.js (brew)"}]},"clawdbot":{"always":false,"emoji":"📐","homepage":"https://github.com/MaTriXy/linear-skill","requires":{"bins":["node","npm"],"env":["LINEAR_API_KEY"]},"primaryEnv":"LINEAR_API_KEY","install":[{"id":"node-brew","kind":"brew","formula":"node","bins":["node","npm"],"label":"Install Node.js (brew)"}]}}
---

# Linear Workflow Management

Manage Linear issues and projects through the bundled CLI at `{baseDir}/scripts/linear-cli.js`.

## Scope and Runtime Model

- This skill runs `node {baseDir}/scripts/linear-cli.js ...`.
- The CLI uses the official `@linear/sdk`.
- Authentication is `LINEAR_API_KEY` from the local environment.
- Expected API destination is Linear GraphQL (`https://api.linear.app/graphql`) through the official SDK.

## Prerequisites

1. Node.js and npm are installed.
2. Install script dependencies once:
   - `cd {baseDir}/scripts && npm install`
3. Set your API key:
   - `export LINEAR_API_KEY="lin_api_..."`

If dependencies or `LINEAR_API_KEY` are missing, stop and complete setup before issue/project operations.

## Authentication and Credentials

- Required credential: `LINEAR_API_KEY`.
- Get it from `https://linear.app/settings/api`.
- Use least-privilege access and a dedicated token for automation.

## Required Workflow

1. Clarify intent and scope:
   - Team/project, labels, cycle, assignee, due date, priority.
2. Read current state first:
   - List/get issues, projects, statuses, labels, users, cycles.
3. Apply mutations second:
   - Create/update issues, comments, projects, milestones, labels.
4. Summarize exactly what changed:
   - Mention IDs, states, assignees, blockers, and follow-up actions.

## Command Coverage

- Teams and projects:
  `teams`, `projects`, `createProject`
- Issues:
  `issues`, `issue`, `createIssue`, `updateIssue`
- Comments:
  `createComment`
- States and labels:
  `states`, `labels`
- User:
  `user`

## Quick Examples

```bash
node {baseDir}/scripts/linear-cli.js teams
node {baseDir}/scripts/linear-cli.js projects
node {baseDir}/scripts/linear-cli.js issues
node {baseDir}/scripts/linear-cli.js issue ENG-123
node {baseDir}/scripts/linear-cli.js createIssue "Title" "Description" "team-id" '{"priority":2}'
node {baseDir}/scripts/linear-cli.js updateIssue "issue-id" '{"stateId":"state-id"}'
```

## Practical Workflows

- Triage urgent bugs:
  list high-priority open issues, assign owners, move state to `In Progress`, add triage comments.
- Sprint planning:
  review cycle scope, create missing issues, set priorities and estimates, align assignees.
- Release prep:
  verify blockers, update project status, create milestone tasks, add rollout comments.
- Documentation cleanup:
  find stale docs/issues, open follow-up tasks, link related records.

## Safety and Operational Rules

- Never invent IDs; fetch and confirm before updates.
- Prefer narrow updates over broad bulk edits.
- For bulk edits, explain grouping logic before applying changes.
- Do not include secrets in issue comments or descriptions.
- Do not send data to endpoints outside Linear API scope for this skill.

## References

- `references/API.md` for priority values and workflow patterns.
