---
name: doc-operationnelle
description: >
  Skill based on "Documentation opérationnelle : structurer pour retrouver"
  (blog.stephane-robert.info). Use this skill when the user wants to structure,
  create, or improve operational documentation: choosing the right family
  (mapping, architecture, procedures, reference, history), applying the one-doc/one-family
  rule, setting up a RACI, avoiding anti-patterns, or using minimum viable / maturity
  checklists. Also triggers on: "how to document my infra", "runbook vs ADR",
  "who owns this doc", "docs-as-code", "CODEOWNERS", "team documentation",
  "operational documentation".
---

# Operational Documentation — Structure to Find

> Source: https://blog.stephane-robert.info/docs/documenter/concevoir/documentation-operationnelle/

## Why It's Essential

**Tacit knowledge vs documentation**
Tacit knowledge lives in experts' heads. When they leave, it disappears.
Documentation is what remains when they're not around.

**5 concrete benefits**

| Benefit | Without docs | With docs |
|---|---|---|
| Diagnosis time | 20 min figuring out "what is this server?" | Open the service page, follow the runbook |
| Onboarding | 3 weeks pestering colleagues | 3 days reading, then targeted questions |
| On-call | Call the expert at 3am | Follow the runbook, solve 80% alone |
| Expert departure | Panic, critical knowledge lost | Smooth transition |
| Security audit | "Uh… I think it's configured like that…" | "Here's our access documentation" |

---

## The 5 Documentation Families

**Golden rule: one document = one family.**
Different update cycles, different audiences, different needs.

| Family | Question | When to consult | Typical format |
|---|---|---|---|
| Mapping | What exists? | Understanding the landscape | Inventories, tables |
| Architecture | How does it work? | Diagnosis, onboarding | Diagrams, schemas |
| Procedures | How to act? | Incident, operation | Runbooks, checklists |
| Reference | Who? What access? What rules? | Organisation, rights | Directories, conventions |
| History | Why this choice? | Understanding the past | ADRs, postmortems |

### Family 1 — Mapping
**Question: What exists?**

Inventories everything that makes up the system: servers, services, databases, APIs, connections.

Contents: server inventory (name, role, IP, env), service list (name, function, owner, criticality),
database registry, API catalogue, dependency matrix.

Recommended format — structured table:
```markdown
| Service         | Owner          | Criticality | Dependencies      | SLA    |
|-----------------|----------------|-------------|-------------------|--------|
| auth-api        | @team-identity | Tier 1      | PostgreSQL, Redis  | 99.9%  |
| payment-service | @team-payment  | Tier 1      | auth-api, Stripe   | 99.95% |
```

Update cycle: on every change (new service, migration, decommission).
Tip: ideal candidate for automation via CMDB or discovery scripts.

### Family 2 — Architecture
**Question: How does it work?**

Explains how components interact, data flows, and protocols used.

Contents: component diagrams (boxes and arrows), data flows (user → API → DB),
network diagrams (VLAN, firewalls, load balancers), deployment schemas (Kubernetes, VMs, cloud).

Recommended format: text-based diagrams (Mermaid, PlantUML) + explanatory text.
Detail levels (C4 model):

| Level | Audience | Detail |
|---|---|---|
| Context | Everyone | The system and its external interactions |
| Containers | Developers | Services, databases, queues |
| Components | Technical team | Internal modules of a service |
| Code | Contributors | Classes, functions (rarely documented) |

⚠️ An outdated diagram is worse than no diagram: it misleads. Prefer simple,
maintainable diagrams over masterpieces no one dares to touch.

Update cycle: on structural changes. Annual review minimum.

### Family 3 — Procedures
**Question: How to act?**

What you consult at 3am. Describes actions to take for routine operations or incidents.

| Type | Usage | Example |
|---|---|---|
| Runbooks | Incidents, technical operations | Restart the auth service |
| Checklists | Don't forget anything | Production deployment checklist |
| Playbooks | Complex multi-actor scenarios | Major incident management |
| Troubleshooting | Step-by-step diagnosis | "500 error on /api/users" |

Recommended format — numbered steps with validations:
```markdown
## Restart the auth service
### Prerequisites
- SSH access to auth-prod-01
- sudo rights

### Steps
1. Check current state
   ```bash
   systemctl status auth-service
   ```
   **Expected**: "active (running)" or "failed"

2. Restart the service
   ```bash
   sudo systemctl restart auth-service
   ```

3. Verify restart
   ```bash
   systemctl status auth-service
   ```
   **Expected**: "active (running)" for less than 1 minute

### If it doesn't work
- Logs: `journalctl -u auth-service -n 100`
- Escalate: @oncall-platform
```

Update cycle: after every incident where the procedure failed or was incomplete.

### Family 4 — Reference
**Question: Who to contact? What access? What rules?**

Centralises organisational information: contacts, access, conventions, policies.

| Type | Content | Example |
|---|---|---|
| Team directory | Who does what, oncall, escalation | "The Platform team manages Kubernetes" |
| Access matrix | Who has access to what | "Only SREs have prod access" |
| Conventions | Naming standards, formats | "Services: {domain}-{function}" |
| Policies | Company rules | "All prod changes require a PR" |
| Glossary | Business term definitions | "A 'tenant' is a B2B customer" |

Recommended format — tables and structured lists:
```markdown
| Team     | Responsibilities            | Slack          | Oncall           |
|----------|-----------------------------|----------------|------------------|
| Platform | Kubernetes, CI/CD, Obs.     | #team-platform | @oncall-platform |
| Identity | Auth, SSO, Permissions      | #team-identity | @oncall-identity |

| Resource | Format               | Example            |
|----------|----------------------|--------------------|
| Server   | {env}-{role}-{num}   | prod-web-01        |
| Service  | {domain}-{function}  | payment-api        |
| Database | {svc}-{type}-{env}   | auth-postgres-prod |
```

Update cycle: directory on every join/departure, access quarterly review, conventions rarely.

### Family 5 — History
**Question: Why this choice? What happened?**

Preserves the memory of decisions and events to avoid repeating mistakes.

| Type | Usage | Example |
|---|---|---|
| ADR | Document a technical decision | "Why PostgreSQL over MySQL" |
| Postmortems | Analyse an incident | "Outage on 15 March 2024" |
| Changelog | History of changes | "v2.3.0: added Redis cache" |
| Migration log | Track migrations | "Oracle → PostgreSQL migration" |

Recommended format — ADR template:
```markdown
# ADR-003: Adopt PostgreSQL for sessions
**Date**: 2024-01-15 | **Status**: Accepted | **Deciders**: @alice, @bob

## Context
Store user sessions with high availability and ACID transactions.

## Options considered
| Option     | Advantages         | Drawbacks        |
|------------|--------------------|------------------|
| Redis      | Fast, simple       | Not ACID         |
| PostgreSQL | ACID, native SQL   | Slightly slower  |
| DynamoDB   | Serverless         | Vendor lock-in   |

## Decision
PostgreSQL — ACID mandatory, team already familiar.

## Consequences
- [+] Data consistency guaranteed
- [-] Slightly higher latency
- [Action] Set up PgBouncer
```

Update cycle: ADRs are immutable (new decision = new ADR), postmortems within 5 days of incident.

---

## Golden Rule: One Document = One Family

| ❌ Anti-pattern | ✅ Good practice |
|---|---|
| Service Overview with embedded runbooks | Service Overview + links to separate runbooks |
| ADR with migration procedure | ADR (decision) + Runbook (procedure) |
| Directory with network architecture | Teams page + Network architecture page |
| Postmortem with embedded checklist | Postmortem + action item "create checklist" |

Why: different update cycles, different audiences, easier to search.

---

## Implementation (Step by Step)

1. **Inventory what exists** — where is the current doc? What's missing?
   Exercise: list every time you had to "ask someone" in recent weeks.
   Each recurring question → candidate to document.

2. **Choose a central tool** — criteria: effective search, versioning, collaboration,
   accessible during an incident.
   Options: Wiki (Confluence, Notion), Docs-as-code (MkDocs, Docusaurus), Git README.

3. **Define a clear structure**:
   ```
   Services/
     payment-service/
       overview.md
       architecture.md
       runbooks/
   Infrastructure/
     network.md
     servers.md
   Cross-cutting-procedures/
     incident-management.md
     deployment.md
   Decisions-ADR/
     001-postgresql-choice.md
   Contacts-and-access/
     team.md
     access.md
   ```

4. **Create essential pages** — per critical service, in priority order:
   overview → architecture → dependencies → runbooks → contacts.

5. **Keep it up to date**:
   - Rule 1: on every change, update the doc (not "later")
   - Rule 2: quarterly review of key pages
   - Rule 3: every page has an owner
   - Docs-as-code: no merge without updated docs

---

## RACI Governance

| Letter | Role | Meaning |
|---|---|---|
| R | Responsible | Does the work (writes, updates) |
| A | Accountable | Validates and owns the final result |
| C | Consulted | Consulted before finalising |
| I | Informed | Notified after (doesn't participate) |

**Golden rule**: there can only be **one Accountable** per document.
"Everyone is responsible" = no one is.

**CODEOWNERS** (automate RACI with docs-as-code):
```
# PR cannot be merged without reviewer approval
/docs/infrastructure/    @ops-team
/docs/api/               @backend-team
/docs/security/          @security-team
```

Conflict resolution:

| Situation | Solution |
|---|---|
| Two teams want to modify the same doc | The Owner decides |
| Technical content disagreement | Escalate to architect → document decision (ADR) |
| Duplicate documentation | Merge, assign single owner, delete duplicate |
| Nobody wants to maintain a doc | Explicitly assign an owner, or archive |

---

## Classic Anti-patterns

| Anti-pattern | What happens | How to avoid |
|---|---|---|
| Ghost documentation | Exists but nobody knows where | Single tool, clear structure |
| Stale documentation | 2019 diagram, infra changed 3 times | Updates integrated into workflow |
| Too much detail | 50 pages nobody reads | Focus on what's essential |
| Not enough detail | "Ask Jean-Pierre" | If it's critical, it's documented |
| Documentation silos | Each team has its own wiki | One common tool or cross-links |
| No owner | "Everyone's doc = nobody's doc" | Explicit owner per section |
| Fuzzy ownership | "Teams X and Y are responsible" | One Accountable only |
| Endless validation | 5 approvers, 3 weeks for a typo | Simplify the workflow |

---

## Checklists

### Minimum viable (starting from scratch)
- [ ] Documentation tool chosen and accessible to everyone
- [ ] Service mapping (list with criticality)
- [ ] Network diagram (how machines are connected)
- [ ] Runbooks for the most common incidents
- [ ] Directory (who to call in case of a problem)
- [ ] Full-text search working
- [ ] Every critical service has at least one page
- [ ] Owners identified for each section

### Maturity (once the basics are in place)
- [ ] ADRs for important technical decisions
- [ ] Versioning (git or wiki history)
- [ ] Quarterly reviews scheduled
- [ ] Templates for creating new pages
- [ ] Feedback loop (report a stale doc)
- [ ] Incident access (doc accessible if infra is down)
- [ ] Docs CI/CD (automated build and deploy)
- [ ] RACI matrix documented
- [ ] CODEOWNERS configured (if docs-as-code)
- [ ] Contributor onboarding documented

### Before creating a document
- [ ] Which family? (Mapping / Architecture / Procedures / Reference / History)
- [ ] Where to file it? (corresponding folder)
- [ ] Does it already exist? (avoid duplicates)
- [ ] Who will maintain it? (owner defined)
- [ ] What is the update cycle?

---

## Key Takeaways

- **Undocumented information doesn't exist** — if it's only in someone's head, it disappears with them.
- **5 distinct families** — Mapping, Architecture, Procedures, Reference, History. Don't mix them.
- **One document = one family** — different update cycles, different audiences.
- **One Accountable per document** — "everyone responsible" = no one is.
- **Updates integrated into the workflow** — no merge without updated docs.
- **Start small** — critical services + common incident runbooks + directory. The rest will follow.
