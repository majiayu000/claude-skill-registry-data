---
name: linear
description: "Manage Linear issues, projects, cycles, and labels through GraphQL and webhook-driven workflows."
category: productivity
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["linear", "graphql", "issues", "cycles", "product-ops", "webhooks", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Linear Product Issue Tracking AI Skill Guide (Claude)

## Overview & Engine Architecture
Linear is a high-speed issue tracker for product/engineering teams with **Issues**, **Projects**, **Cycles**, **Initiatives**, and **Workflow states**. Automation uses the **Linear GraphQL API**, personal API keys / OAuth, and **webhooks**. Claude operates as a Principal Product Operations Engineer, specializing in **issue triage mutations**, **project roadmap queries**, **label taxonomies**, and **idempotent webhook handlers**.

### Linear Domain & API Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Linear Architecture                         │
│                                                             │
│  Product Objects                                            │
│  ├── Teams / Members / Workflow States                      │
│  ├── Issues / Labels / Comments / Attachments               │
│  └── Projects / Cycles / Initiatives                        │
│                                                             │
│  API                                                        │
│  ├── GraphQL endpoint https://api.linear.app/graphql        │
│  ├── API Key (Authorization: <key>)                         │
│  └── Webhooks (issue create/update, comments, ...)          │
│                                                             │
│  Client Surfaces                                            │
│  ├── Desktop / Web / Mobile                                 │
│  ├── Slack / GitHub integrations                            │
│  └── @linear/sdk                                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Team-Scoped Writes**: Always resolve `teamId` before `issueCreate`.
2. **State by Type**: Prefer state IDs/types (`started`, `completed`) over hard-coded names when possible.
3. **Idempotent Imports**: Key off external IDs in description/attachments or custom fields patterns.
4. **Rate Limits**: Batch thoughtfully; prefer GraphQL selection sets that fetch only needed fields.
5. **Webhook Verification**: Validate signatures when Linear provides signing secrets.

---

## Production TypeScript: Create Issue + Query Cycle Load

```typescript
// ==============================================================================
// Linear GraphQL: create issue and list active cycle issues
// npm i @linear/sdk
// ==============================================================================
import { LinearClient } from "@linear/sdk";

const linear = new LinearClient({ apiKey: process.env.LINEAR_API_KEY });

async function createBug(title: string, description: string, teamKey: string) {
  const teams = await linear.teams({ filter: { key: { eq: teamKey } } });
  const team = teams.nodes[0];
  if (!team) throw new Error(`Team not found: ${teamKey}`);

  const payload = await linear.createIssue({
    teamId: team.id,
    title,
    description,
    priority: 2, // High
  });

  const issue = await payload.issue;
  if (!issue) throw new Error("Issue creation failed");
  return issue.identifier; // e.g. ENG-123
}

async function activeCycleSummary(teamKey: string) {
  const teams = await linear.teams({ filter: { key: { eq: teamKey } } });
  const team = teams.nodes[0];
  if (!team) throw new Error(`Team not found: ${teamKey}`);

  const cycles = await team.cycles({ filter: { isActive: { eq: true } } });
  const cycle = cycles.nodes[0];
  if (!cycle) return { cycle: null, issues: [] as string[] };

  const issues = await cycle.issues();
  return {
    cycle: cycle.name,
    issues: issues.nodes.map((i) => `${i.identifier} ${i.title}`),
  };
}

createBug("Checkout 500 on promo codes", "Repro steps...", "ENG").then(console.log);
```

Raw GraphQL alternative:

```graphql
mutation IssueCreate($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue { id identifier url }
  }
}
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Unauthorized** | Bad/revoked API key. | Regenerate key; check header format. |
| **Team not found** | Wrong key / private team. | List teams via API; confirm membership. |
| **State transition rejected** | Illegal workflow move. | Query team states; move via allowed edges. |
| **Webhook duplicates** | At-least-once delivery. | Dedupe on `action` + issue id + updatedAt. |

---

## Best Practices

1. Encode triage rules as labels + templates, not tribal knowledge.
2. Link PRs via Linear<>GitHub integration rather than pasting only URLs.
3. Keep priority taxonomy small and consistent (Urgent/High/Medium/Low).

### Essential References
- GraphQL: `https://api.linear.app/graphql`
- SDK: `@linear/sdk`
- Auth header: `Authorization: <LINEAR_API_KEY>`

---

## Agent Operational Directive
> **MANDATORY**: Resolve team IDs before creating issues. Prefer SDK/GraphQL typed inputs over scraping the UI. Make webhook consumers idempotent.
