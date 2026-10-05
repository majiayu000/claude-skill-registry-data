---
name: domain-template
description: Apply when documenting project-specific knowledge. Template for ADRs, naming conventions, business rules, and tech-stack quirks.
license: MIT
version: 1.0.0
tokens_target: 1000
triggers:
  - project-specific knowledge
  - business rules
loads_after: []
supersedes: []
---

# Sub-Skill: Domain Knowledge Template
<!-- target: ~850 tokens (empty template — grows when filled in for your project) -->

**Purpose:** Structured template for capturing company- or project-specific knowledge
that no public model can know — architecture decisions, naming conventions, business rules.

---

## Instructions: Fill Out This Template

Copy this file to `skills/<project-name>/SKILL.md` and fill in all sections.
Delete empty sections. Concrete > comprehensive.

---

## Project Overview

```
Project name:    [e.g. "OrderFlow"]
Technology:      [e.g. "Node.js 20, PostgreSQL 15, React 18"]
Deployment:      [e.g. "AWS ECS, GitHub Actions CI/CD"]
Team size:       [e.g. "4 backend, 2 frontend"]
Main repo:       [e.g. "github.com/acme/orderflow"]
```

---

## Architecture Decision Records (ADRs)

### ADR-001: [Title]
- **Date:** YYYY-MM-DD
- **Status:** Accepted / Deprecated / Superseded by ADR-XXX
- **Context:** Why did a decision need to be made?
- **Decision:** What was decided?
- **Consequences:** What changes as a result?

---

## Naming Conventions

| Context | Convention | Example |
|---------|-----------|---------|
| Database tables | snake_case, plural | `order_items` |
| API endpoints | kebab-case, plural | `/api/order-items` |
| TypeScript interfaces | PascalCase, no `I` prefix | `OrderItem` |
| Environment variables | SCREAMING_SNAKE_CASE | `DATABASE_URL` |
| React components | PascalCase | `OrderItemList` |

---

## Business Rules

> These rules are not documented in the code — only here.

1. **[Rule name]:** [Description]. Example: `Orders under $10 have no shipping costs.`
2. **[Rule name]:** [Description].

---

## Known Pitfalls

1. **[Pitfall]:** [What happens and why]. Example: `The users table has two ID fields: id (internal) and external_id (customer number). Never confuse them.`
2. **[Pitfall]:** [What happens and why].

---

## External Systems & Integrations

| System | Purpose | Auth Method | Contact for Issues |
|--------|---------|-------------|-------------------|
| Stripe | Payments | API key in `STRIPE_SECRET_KEY` | payments@acme.com |
| SendGrid | Emails | API key in `SENDGRID_API_KEY` | devops@acme.com |

---

## Glossary

| Term | Meaning |
|------|---------|
| `Order` | A confirmed order (status >= CONFIRMED) |
| `Cart` | An unconfirmed order (status = DRAFT) |

---

## Agent Directives

> Specific instructions for how the agent should work in this project.

1. **[Directive]:** [Description]. Example: `Never delete files without explicit user confirmation.`
2. **[Directive]:** [Description]. Example: `Always output the full file path with every change.`
3. **[Directive]:** [Description]. Example: `Always use English in commit messages.`

---

## Tech Stack Quirks

> Stack-specific gotchas not found in the documentation — only learned through experience.

1. **[Quirk name]:** [What happens and why]. Example: `Prisma Client must be regenerated with npx prisma generate after schema changes — a simple npm install is not enough.`
2. **[Quirk name]:** [What happens and why]. Example: `The Redis connection pool in production has max 10 connections — with more than 10 parallel requests, requests get dropped.`

---

## Why This Sub-Skill Earns Stars

Without domain knowledge, the agent makes plausible but wrong assumptions about naming, business rules, and architecture.
With this template filled out once → the agent knows the project like a team member.
