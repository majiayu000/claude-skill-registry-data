---
name: initiative-status-report
description: Generate structured weekly status reports covering initiatives, progress, blockers, risks, and KPIs.
---

# initiative-status-report

Generates a weekly status report for all active epics.

## When to Use

- Weekly team reporting, stakeholder updates, sprint reviews

## Steps

### 1. Load epics

```bash
bd ready --type epic
```

For each: `bd show <id>` to get tasks, AC, and due dates.

### 2. Gather git activity

```bash
git log --oneline --since="1 week ago"
gh pr list --state all --limit 20 --json number,title,state,mergedAt
```

### 3. Generate Markdown report

Sections:
- **Executive Summary** (2-3 sentences: wins, risks, health)
- **Active Initiatives** (per epic: status, progress, blockers, this/next week)
- **Key Metrics** (tasks closed, PRs merged, open bugs — this vs last week)
- **Risks & Mitigation** (likelihood, impact, action)
- **Decisions Needed** (items requiring human judgment)
