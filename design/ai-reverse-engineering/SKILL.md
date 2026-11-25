---
name: ai-reverse-engineering
description: >
  Reverse-engineer an authorized application into an evidence-backed product and
  system blueprint covering modules, features, functions, UI, workflows, states,
  business rules, data, permissions, APIs, integrations, automations, exceptions,
  and user journeys. Use when asked to "reverse engineer this app", "discover an
  application's behavior", "build an application blueprint", "document an
  existing system from UI/API/code", "map features and workflows", or invokes
  /ai-reverse-engineering.
argument-hint: "[application, artifacts, or scope]"
---

# AI Reverse Engineering

Reconstruct what an application does from observable evidence. Produce a blueprint that can support documentation, testing, redesign, migration, or reimplementation.

The core loop is:

> **Observe → hypothesize → investigate → verify → document**

Never turn a plausible interpretation into a fact. Every conclusion must be **Confirmed**, **Inferred**, **Unknown**, or **Contradictory** and cite its evidence.

## Safety and Scope

Work only on applications and data the user owns or is authorized to assess.

- Confirm scope before active exploration when authorization or environment is unclear.
- Treat production as read-only unless the user explicitly approves a mutation.
- Do not submit destructive actions, trigger payments, send notifications, modify permissions, or access unrelated tenant/user data without explicit approval.
- Redact secrets, tokens, passwords, personal data, and session identifiers from outputs.
- Prefer test accounts and non-production environments.
- Record blocked areas as unknowns. Do not bypass authentication or access controls.

## Inputs

Use whatever authorized evidence is available:

- Screenshots, recordings, DOM, accessibility trees, screens, forms, dialogs, tables, and menus
- User interactions, navigation, validation, errors, and resulting state changes
- HAR files, API specifications, network requests, events, and response schemas
- Database schemas, representative redacted records, constraints, and relationships
- Frontend and backend source, configuration, tests, migrations, and infrastructure
- Product documentation, requirements, SOPs, help pages, and support material
- Roles, permissions, integrations, notifications, scheduled jobs, and automation

Do not require every input. State which evidence classes are present and what their absence prevents confirming.

## Workflow

### 1. Establish the frame

Identify:

- Application and environment
- Goal: document, reproduce, migrate, test, redesign, or compare
- Included and excluded modules
- Available roles and test accounts
- Permitted interactions and forbidden mutations
- Available artifacts
- Desired output location and format

Ask one concise question only when a missing answer blocks safe or useful work. Otherwise proceed and state assumptions.

### 2. Build an evidence inventory

Assign stable IDs to evidence as it is examined:

| ID | Type | Source | Scope | Reliability | Notes |
|---|---|---|---|---|---|
| UI-001 | UI | Customer form screenshot | Customers | Direct | Captured date if known |
| API-001 | API | `POST /customers` HAR entry | Customers | Direct | Secrets redacted |
| CODE-001 | Code | `CustomerService.create` | Customers | Direct | Commit/version |
| DOC-001 | Documentation | User guide §4 | Customers | Supporting | May be stale |

Evidence must be traceable to a file, URL, request, symbol, screen, or user-supplied statement.

### 3. Inspect by evidence class

Run independent analysis passes for the available evidence, in parallel where practical.

#### UI and behavior

Capture each screen, route, component, control, visible state, validation, role-dependent variation, action, result, and error. A visible button confirms only that the control exists—not what it does.

For active exploration, record before/action/after:

```text
Before: current screen and state
Action: exact interaction and input
After: navigation, UI change, network activity, persisted change, error, or no-op
```

#### API and events

Map endpoints, methods, authentication, parameters, request/response fields, status codes, errors, pagination, idempotency, emitted events, and callers. Redact credentials and sensitive values.

#### Source code

Trace real entry points through handlers, services, domain rules, persistence, integrations, and side effects. Prefer repository-native navigation tools. If a CodeGraph index exists, use it before grep/read loops. Use tests and migrations as evidence, not as proof that deployed behavior matches.

#### Data

Extract entities, fields, identifiers, relationships, constraints, indexes, lifecycle states, retention rules, and ownership boundaries. Distinguish schema facts from assumptions based on sample values.

#### Documentation and integrations

Map documented capabilities, external systems, inbound/outbound contracts, authentication, retries, failure handling, scheduled work, notifications, and discrepancies between docs and observed behavior.

#### Roles and permissions

Test or trace each role independently. Separate UI visibility from server-side authorization. Do not infer permission enforcement from a hidden control.

### 4. Apply the verification loop

For every candidate capability:

1. **Observe** — Record only what the evidence directly shows.
2. **Hypothesize** — State the smallest falsifiable explanation.
3. **Investigate** — Find a second evidence source or perform an authorized test.
4. **Verify** — Compare predicted and actual behavior.
5. **Document** — Add the conclusion, status, and evidence IDs.

Use these statuses:

| Status | Meaning |
|---|---|
| **Confirmed** | Direct evidence verifies the claim; cross-source confirmation is preferred |
| **Inferred** | Evidence supports the claim, but decisive verification is unavailable |
| **Unknown** | Evidence is missing or access is blocked |
| **Contradictory** | Sources disagree; preserve both claims and identify the conflict |

Do not invent confidence percentages. The status and cited evidence communicate confidence more honestly.

### 5. Normalize the application model

Organize findings into this hierarchy:

```text
Application
├── Product purpose and users
├── Modules
│   └── Features
│       ├── Functions
│       ├── UI
│       ├── Workflows and journeys
│       ├── States and transitions
│       ├── Business rules and validations
│       ├── Data
│       ├── Permissions
│       ├── APIs and events
│       ├── Integrations and automation
│       └── Exceptions and dependencies
├── Cross-module data model
├── Role/permission model
├── Integration map
└── Evidence gaps and contradictions
```

Keep one canonical record for each concept. Link concepts with plain relationships before proposing a graph database:

```text
Sales Representative --can execute--> Create Customer
Create Customer --appears on--> Customer Creation Screen
Create Customer --calls--> POST /customers
Create Customer --creates--> Customer
Create Customer --requires--> customer:create
Create Customer --triggers--> CustomerCreated
```

### 6. Resolve high-value gaps

Prioritize unknowns that affect:

1. Security or permissions
2. Money, destructive changes, or external side effects
3. Core workflows and business rules
4. State transitions and persistence
5. Edge cases and operational behavior
6. Cosmetic UI details

For each unresolved gap, name the cheapest decisive evidence: role test, network capture, schema access, source symbol, representative record, or stakeholder answer.

### 7. Produce the blueprint

Write to the user's requested destination. If none is given, create `AI_REVERSE_ENGINEERING_BLUEPRINT.md` in the current directory. Produce JSON only when requested; Markdown is the default.

## Blueprint Structure

```markdown
# Application Blueprint: <name>

## 1. Executive Overview
- Purpose
- Target users
- Business objectives
- Major capabilities
- Scope and evidence limitations

## 2. Evidence Inventory

## 3. Application Map
- Modules, submodules, features, and dependencies

## 4. Feature Catalog

## 5. Workflow and User-Journey Catalog
- Happy, alternate, failure, and edge paths
- State transitions

## 6. Data Model
- Entities, fields, relationships, constraints, ownership, lifecycle

## 7. Roles and Permission Matrix

## 8. API and Event Catalog

## 9. Integration, Notification, and Automation Map

## 10. Business Rules and Validations

## 11. Exceptions and Operational Behavior

## 12. Evidence Gaps, Contradictions, and Verification Plan

## 13. Reproduction or Migration Notes
- Include only when relevant to the user's goal
```

Use tables for catalogs and matrices. Use Mermaid only when diagrams improve comprehension and the target supports it.

### Feature record

Use this template for every material feature:

```markdown
### <Feature name>

| Field | Value |
|---|---|
| Module | |
| Purpose | |
| Actors | |
| Preconditions | |
| Trigger | |
| Inputs | |
| Outputs | |
| UI | |
| Functions | |
| Business rules | |
| Permissions | |
| APIs/events | |
| Data | |
| Notifications/automation | |
| Exceptions | |
| Dependencies | |
| Status | Confirmed / Inferred / Unknown / Contradictory |
| Evidence | UI-001, API-001, ... |
```

### Workflow record

For each workflow, document:

- Trigger and actor
- Preconditions
- Ordered steps
- Decisions and branches
- State changes
- External side effects
- Happy path
- Alternate and failure paths
- Final states
- Evidence per step

### Business-rule record

```markdown
| Rule | Scope | Enforcement point | Failure behavior | Status | Evidence |
|---|---|---|---|---|---|
```

### Permission matrix

```markdown
| Function | Role A | Role B | Role C | Enforcement evidence |
|---|---:|---:|---:|---|
```

Use **Confirmed**, **Denied**, and **Unknown** in role cells rather than checkmarks when evidence quality matters.

## Quality Gate

Before finishing, verify:

- [ ] Every material claim has an evidence ID or is labeled Unknown.
- [ ] UI presence is not presented as backend behavior without verification.
- [ ] Hidden controls are not treated as proof of server-side authorization.
- [ ] Happy paths, failures, alternate paths, and edge cases are separated.
- [ ] State changes and external side effects are explicit.
- [ ] Conflicting evidence remains visible.
- [ ] Secrets and personal data are redacted.
- [ ] The report states scope, environment, version/date, and evidence limitations.
- [ ] The blueprint distinguishes deployed behavior from docs, tests, and code intent.

## Completion Summary

Report:

- Output path
- Modules, features, workflows, and rules cataloged
- Confirmed vs. inferred vs. unknown counts
- Highest-risk gaps
- Next verification action with the best information gain

## Anti-Patterns

- One giant unstructured summary
- Treating labels, buttons, or docs as proof of behavior
- Filling gaps with generic product assumptions
- Hiding contradictions to make the blueprint look complete
- Creating a knowledge-graph platform when a relationship table is enough
- Using multiple analysis passes without reconciling duplicate concepts
- Claiming completeness when roles, failure paths, or integrations were not examined
