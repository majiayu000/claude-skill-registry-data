---
name: documentation
description: Write effective technical documentation — READMEs, runbooks, Architecture Decision Records, and API docs. Apply the Divio documentation system (tutorials, how-to guides, reference, explanation) to create documentation that engineers actually read and maintain.
triggers:
  - "write documentation"
  - "document this"
  - "write a README"
  - "write a runbook"
  - "document the API"
  - "add docs"
  - "explain this codebase"
audience:
  - engineer
---

# Documentation

Write documentation that gets read, maintained, and actually helps.

---

## The Divio Documentation System

Documentation serves four distinct purposes. Mixing them is why most docs are hard to use.

| Type | Purpose | Answers | Example |
|---|---|---|---|
| **Tutorial** | Learning-oriented | "Help me get started" | Getting Started guide |
| **How-to Guide** | Task-oriented | "How do I do X?" | "How to deploy to production" |
| **Reference** | Information-oriented | "What is X?" | API reference, config options |
| **Explanation** | Understanding-oriented | "Why does X work this way?" | Architecture overview, ADR |

**Rule**: When writing a doc, decide which type it is first. Don't mix types in one document.

---

## README Template

A README is a tutorial/how-to hybrid. It answers: "What is this, and how do I use it?"

```markdown
# [Project Name]

[One sentence: what does this do, for whom]

## Quick Start

```bash
# Minimum viable example to get running
git clone ...
npm install
npm start
```

## What It Does

[2-3 paragraphs explaining the problem it solves and how]

## Requirements

- [Runtime/language version]
- [Key dependency]
- [Environment variables needed]

## Usage

[Most common use case with working code example]

## Configuration

| Variable | Default | Description |
|---|---|---|
| `PORT` | 3000 | HTTP port |
| `DATABASE_URL` | — | Required. PostgreSQL connection string |

## Development

```bash
npm test
npm run lint
```

## Architecture

[Link to ADR or architecture doc, or 1-paragraph overview]

## Contributing

[Link to CONTRIBUTING.md or brief instructions]

## License

[License name and link]
```

---

## Runbook Template

A runbook is a how-to guide for on-call engineers. It answers operational questions under pressure.

```markdown
# Runbook: [Service Name]

**Owner**: [team]  
**On-call rotation**: [link to PagerDuty/OpsGenie]  
**Dashboard**: [link]  
**Logs**: [link]  
**Repo**: [link]

---

## Service Overview

[2 sentences: what this service does and why it matters]

**Dependencies**:
- Calls: [services this depends on]
- Called by: [services that depend on this]

---

## Common Alerts

### Alert: [AlertName]

**Meaning**: [What this alert means in plain English]  
**Impact**: [What breaks for users]

**Investigation**:
1. Check [dashboard link] for [metric]
2. `kubectl logs -n [ns] deployment/[name] | grep ERROR`
3. Check [dependency service] status

**Resolution**:
- If [condition A]: [action]
- If [condition B]: [action]
- If unknown: escalate to [team/person]

**Post-incident**: Link to incident retrospective skill

---

## Deployment

```bash
# Deploy to production
git tag v[x.y.z] && git push origin v[x.y.z]
# Observe: [dashboard link] for 10 min post-deploy
```

**Rollback**:
```bash
kubectl rollout undo deployment/[name] -n [namespace]
```

---

## Scaling

[When and how to scale this service manually if needed]

---

## Known Issues

| Issue | Workaround | Ticket |
|---|---|---|
| [description] | [workaround] | [link] |
```

---

## API Documentation

For every public API endpoint, document:

```markdown
### POST /orders

Create a new order.

**Auth**: Bearer token required (scope: `orders:write`)

**Request**
```json
{
  "customerId": "string (required)",
  "items": [
    { "productId": "string", "quantity": 1 }
  ]
}
```

**Response 201**
```json
{
  "orderId": "uuid",
  "status": "pending",
  "createdAt": "ISO8601"
}
```

**Errors**
| Code | Reason |
|---|---|
| 400 | Missing required fields |
| 401 | Invalid or missing auth token |
| 422 | `quantity` must be > 0 |
```

---

## Documentation Debt Signals

Your docs need work if:
- New engineers spend > 30 min getting their first PR running
- On-call engineers can't resolve P2 incidents without calling someone
- You have to explain the same thing in Slack more than twice
- Comments in the code are doing the job README or architecture docs should do

---

## AI-Assisted Documentation

### Generate a README draft
```
Here is the code for [project/module]. 
Generate a README following the standard template.
Focus on: what problem it solves, how to run it locally, key configuration.
Keep it accurate — if you're unsure about something, flag it with [VERIFY].
```

### Generate a runbook
```
Here is the deployment config and alerting rules for [service].
Generate a runbook covering: service overview, common alerts with investigation steps,
deployment and rollback commands.
Flag anything that needs a real URL or verification with [TODO].
```

### Improve existing docs
```
This documentation hasn't been updated in [N months].
Review it against the current code/config and:
1. Flag anything that's inaccurate
2. Identify gaps (what's commonly asked but not documented?)
3. Suggest the top 3 improvements
```

---

## What Not to Document

- **How the code works** — that's what code comments and clear naming are for
- **Every function's parameters** — that's what type signatures and IDE tooling are for
- **Process that changes every sprint** — keep that in the ticket system, not static docs

**Rule**: Document decisions, not mechanics. Document "why we do it this way," not "here is a list of all the things."

---

## References
- [Divio Documentation System](https://documentation.divio.com/)
- Martin Fowler: [Sacrificial Architecture](https://martinfowler.com/bliki/SacrificialArchitecture.html) (on the value of documenting decisions)
- [Write the Docs](https://www.writethedocs.org/guide/)
- LeadDev: [Making documentation a team habit](https://leaddev.com/documentation)

## MCP Integration

**Search Confluence for existing documentation to update:**
```
confluence_search(query: "<component or feature name> documentation", space_key: "ENG", limit: 5)
```

**Read an existing page before updating:**
```
confluence_get_page(page_id: "<page_id>")
```

**Create a new documentation page:**
```
confluence_create_page(space_key: "ENG", title: "<Component> — <Doc Type>", content: "<structured documentation content>", parent_page_id: "<docs_section_page_id>")
```

**Update an existing page (tutorials, how-tos, references):**
```
confluence_update_page(page_id: "<page_id>", title: "<same or updated title>", content: "<updated content with version note>")
```

**Graceful fallback:** Output documentation as Markdown with a recommended Confluence page title and parent page path. Include `> 📄 Paste into Confluence > <Space> > <Parent Page>` at the top.
