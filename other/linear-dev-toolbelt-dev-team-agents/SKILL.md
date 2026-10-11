---
name: linear
description: Linear — issue ops, status transitions, cycle management.
---

## Detection

Activate this skill when any of the following are present:
- `LINEAR_API_KEY` environment variable is set
- User mentions a Linear issue key (e.g., `ENG-123`, `INFRA-456`)
- User says "create a Linear issue", "update the Linear ticket", or similar

---

## Status Flow

```
Backlog → Todo → In Progress → In Review → Done
                                         → Cancelled (if abandoned)
```

- Move to **In Progress** when work begins on the branch
- Move to **In Review** when a PR is opened
- Move to **Done** only after the PR is merged and deployed (or as agreed with the team)
- Do not skip statuses — Linear's cycle metrics depend on accurate transitions

---

## Operations

### Before creating an issue — fetch team context first

```graphql
# Get teams, projects, and cycles
query {
  teams {
    nodes {
      id
      name
      states { nodes { id name type } }
      labels { nodes { id name } }
      activeCycle { id number startsAt endsAt }
    }
  }
}
```

Use the returned `state.id`, `label.id`, and `cycle.id` when creating issues — never hardcode IDs.

### Create issue

```graphql
mutation CreateIssue($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue { id identifier title url }
  }
}
```

Required fields: `teamId`, `title`
Recommended fields: `description`, `priority`, `labelIds`, `assigneeId`, `cycleId`

**Priority values:** `0` = No priority, `1` = Urgent, `2` = High, `3` = Medium, `4` = Low

### Update status

```graphql
mutation UpdateIssue($id: String!, $stateId: String!) {
  issueUpdate(id: $id, input: { stateId: $stateId }) {
    success
    issue { id identifier state { name } }
  }
}
```

### Add comment

```graphql
mutation AddComment($issueId: String!, $body: String!) {
  commentCreate(input: { issueId: $issueId, body: $body }) {
    success
    comment { id }
  }
}
```

---

## Branch Naming

When creating a branch for a Linear issue, use:

```
feat/ENG-123-short-description
fix/ENG-456-bug-description
chore/ENG-789-task-description
```

- Use the Linear issue key as the prefix after the type
- Keep the description slug short (3–5 words, kebab-case)
- Linear auto-links branches that contain the issue identifier

---

## Comment Format

When adding a progress comment to a Linear issue, use this structure:

```markdown
**Done:** [what was implemented or changed]

**Decisions:** [key choices made and why — omit if none]

**Blockers:** [anything blocking next steps — omit if none]

**Next:** [remaining work or recommended next action]
```

---

## Cycle Management

- Always assign issues to the **active cycle** when starting work, not when creating
- Use `activeCycle.id` from the team query — do not ask the user for the cycle ID
- If there is no active cycle, assign to the next upcoming cycle or leave unassigned and note it
- Do not create new cycles — that is a team lead responsibility

---

## Checklist

- [ ] Team context fetched before creating any issue (to get valid IDs)
- [ ] Issue assigned to active cycle when work begins
- [ ] Branch name includes the issue identifier (`ENG-123`)
- [ ] Status updated to In Review when PR is opened
- [ ] Comment added to the issue summarizing what was done
