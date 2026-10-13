---
name: omc-gh-project
description: "Manage GitHub Projects (v2) boards: list items, move status, manage iterations, and add issues/PRs to a project. Not for issue triage (omc-gh-triage) or PR review. ADO sprints → omc-ado-sprint."
---

# OMC GitHub Project

Manage GitHub Projects (v2) boards for the current repository. Lists project items, updates card statuses, manages iterations, and adds issues or PRs to projects.

**When this skill is invoked, immediately execute the workflow below. Do not only restate or summarize these instructions back to the user.**

## Trigger Patterns

- "gh project"
- "github project"
- "project board"
- "manage board"
- "project status"
- "omc-gh-project"

---

## Step 1: Load Configuration

Read `.omg/config.json`:

```bash
node -e "const f=require('fs');try{process.stdout.write(f.readFileSync('.omg/config.json','utf8'))}catch{console.log('NOT_FOUND')}"
```

Extract from the `github` key:
- `owner` — GitHub owner (org or user)
- `repo` — repository name

If config is NOT_FOUND or missing the `github` key: tell the user to run `/oh-my-copilot:omc-gh-setup` first and stop.

---

## Step 2: Discover Projects

List all projects accessible to the owner.

```bash
gh project list --owner {owner} --format json --limit 10 2>&1
```

Present the projects:

```
### GitHub Projects ({N})
| # | Title | Items | Status |
|---|-------|-------|--------|
| 1 | Sprint Board | 24 | Open |
| 2 | Roadmap | 12 | Open |
```

If no projects are found, report "No projects found for {owner}. Create one at https://github.com/orgs/{owner}/projects or https://github.com/users/{owner}/projects."

---

## Step 3: List Project Items

Prompt the user to select a project, or accept a project number directly.

```bash
gh project item-list {projectNumber} --owner {owner} --format json --limit 50 2>&1
```

Present the items grouped by status:

```
### Project: {projectTitle}

#### Todo ({N})
| Type | # | Title | Assignees |
|------|---|-------|-----------|
| Issue | #42 | Fix login timeout | alice |
| Draft | — | Research caching options | — |

#### In Progress ({N})
| Type | # | Title | Assignees |
|------|---|-------|-----------|
| PR | #38 | Add retry logic | bob |

#### Done ({N})
| Type | # | Title | Completed |
|------|---|-------|-----------|
| Issue | #35 | Set up CI | 2026-03-28 |
```

---

## Step 4: Update Item Status

Move an item between status columns.

### 4a. Get the project and field IDs

```bash
gh project field-list {projectNumber} --owner {owner} --format json 2>&1
```

Find the `Status` field and its available options (e.g. `Todo`, `In Progress`, `Done`).

### 4b. Update the item status

```bash
gh project item-edit --project-id {projectId} --id {itemId} --field-id {statusFieldId} --single-select-option-id {optionId} 2>&1
```

Confirm:
```
Moved #{issueNumber} "{title}" → {newStatus}
```

---

## Step 5: Assign to Iteration (Optional)

If the project uses iteration fields (sprint-like cycles):

### 5a. List available iterations

```bash
gh project field-list {projectNumber} --owner {owner} --format json 2>&1
```

Find the `Iteration` field and its available iterations.

### 5b. Assign item to iteration

```bash
gh project item-edit --project-id {projectId} --id {itemId} --field-id {iterationFieldId} --iteration-id {iterationId} 2>&1
```

Confirm:
```
Assigned #{issueNumber} "{title}" → {iterationName}
```

---

## Step 6: Add Items to Project

Add an existing issue or PR to the project.

```bash
gh project item-add {projectNumber} --owner {owner} --url "https://github.com/{owner}/{repo}/issues/{issueNumber}" 2>&1
```

Or for a PR:

```bash
gh project item-add {projectNumber} --owner {owner} --url "https://github.com/{owner}/{repo}/pull/{prNumber}" 2>&1
```

Confirm:
```
Added #{number} "{title}" to project "{projectTitle}"
```

---

## Step 7: Create Draft Item (Optional)

Create a new draft item directly in the project (no backing issue/PR).

```bash
gh project item-create {projectNumber} --owner {owner} --title "{title}" --format json 2>&1
```

Confirm:
```
Created draft item "{title}" in project "{projectTitle}"
```

---

## Limitations

GitHub Projects v2 CLI support is still evolving. Known limitations:

| Operation | CLI Support | Workaround |
|-----------|------------|------------|
| List items | Full | — |
| Update status field | Full | — |
| Update iteration field | Full | — |
| Custom field updates | Partial | Use `gh api graphql` for complex field types |
| Capacity tracking | Not available | GitHub Projects has no built-in capacity tracking |
| Velocity/burndown | Not available | Use project insights in the web UI |
| Create project | Not via `gh project` | Use web UI or `gh api graphql` |

For operations not supported by `gh project`, use the GraphQL API:

```bash
gh api graphql -f query='
  mutation {
    updateProjectV2ItemFieldValue(
      input: {
        projectId: "{projectId}"
        itemId: "{itemId}"
        fieldId: "{fieldId}"
        value: { text: "{value}" }
      }
    ) {
      projectV2Item { id }
    }
  }
' 2>&1
```

---

## Error Handling

| Error | Action |
|-------|--------|
| `.omg/config.json` missing | Tell user to run `/oh-my-copilot:omc-gh-setup` first |
| `gh auth` required | Prompt user to authenticate; stop execution |
| No projects found | Suggest creating a project in the web UI |
| Project item not found | Verify item ID; it may have been removed |
| Field update fails | May require `project` scope; suggest `gh auth refresh -s project` |
| GraphQL errors | Check query syntax; GitHub Projects v2 API is in active development |
| Rate limit / 403 | Wait 2 seconds and retry once; if still failing, note as unavailable |
