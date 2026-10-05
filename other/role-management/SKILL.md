---
name: role-management
description: |
  Create and maintain Role entities — named sets of responsibilities that actors can fill. Use when defining a new role in the project (developer, reviewer, tech-lead, release-manager) or updating an existing role's responsibilities.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-role-management
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: processkit
    layer: 1
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
      - skill: index-management
        purpose: Query existing entities and keep the SQLite index fresh after writes.
      - skill: id-management
        purpose: Allocate unique entity identifiers via central ID generation.
    provides:
      primitives: [Role]
      mcp_tools:
        - create_role
        - get_role
        - update_role
        - list_roles
        - link_role_to_actor
      templates: [role]
---

# Role Management

## Intro

A Role is a named set of responsibilities that an Actor can fill. Roles
describe what — not who. "Alice is a developer" is a Binding between Actor
`ACTOR-alice` and Role `ROLE-developer`; this skill manages the Role side of
that relationship.

**Important:** Roles in processkit have no enforcement semantics. They are
descriptive, not restrictive. RBAC enforcement is out of scope
(see DISC-002 / DEC-017).

> **MCP server.** This skill ships a self-contained MCP server at
> `mcp/server.py` (PEP 723 script — requires `uv` and Python ≥ 3.10 on
> PATH). Agent harnesses reach its tools by reading a single MCP config
> file at startup, so the contents of `mcp/mcp-config.json` must be merged
> into the harness's MCP config and placed at the harness-specific path
> before this skill is usable. If processkit was installed by an installer,
> that wiring is the installer's responsibility; if processkit was
> installed manually, the project owner must do it by hand.

## Overview

### When to create a Role

Create a Role when:
- A responsibility recurs across multiple work items or processes.
- You need to refer to "the person who X" without naming a specific actor.
- A process template references the role ("the reviewer must …").

### Shape

```yaml
---
apiVersion: processkit.projectious.work/v2
kind: Role
metadata:
  id: ROLE-reviewer
  created: 2026-04-06T00:00:00Z
spec:
  name: reviewer
  description: "Reviews code and documentation changes before merge."
  responsibilities:
    - "Read PRs within 48 hours of request"
    - "Approve or request changes with actionable feedback"
    - "Block merges on security or correctness concerns"
  skills_required: [code-review, debugging]
  default_scope: project      # project | sprint | permanent
---

Optional body: elaboration, examples, anti-patterns.
```

### Workflow

1. Pick an ID: `ROLE-<name>` where name is kebab-case and unique.
2. Write a one-sentence `description` — the role's purpose.
3. List concrete `responsibilities` as imperative bullet points.
4. Optionally list `skills_required` — links to skill IDs that describe the
   capabilities this role depends on.
5. Save to `context/roles/`.
6. Log `role.created`.

### Assigning actors to roles

**Do not list actor IDs in the Role file.** Assignments go in Binding entities
so they can be scoped, time-bounded, and changed without editing the Role.

```yaml
kind: Binding
spec:
  type: role-assignment
  subject: ACTOR-alice
  target: ROLE-reviewer
  scope: SCOPE-project-x    # optional
```

See `skills/binding-management`.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Confusing Role with Actor.** A Role is a named set of
  responsibilities ("tech-lead", "release-manager"). An Actor is a
  person or agent who can FILL a role. "Alice is the tech lead" is
  a Binding from `ACTOR-alice` to `ROLE-tech-lead`, not an update
  to either entity.
- **Creating a Role for one specific person.** "Alice's
  responsibilities" is not a Role; it's just Alice. Roles capture
  responsibilities that can be transferred between people. If only
  one person could ever fill it, it's a job title, not a Role.
- **Treating Role membership as RBAC enforcement.** Roles are
  descriptive, not restrictive. processkit does not check whether
  an actor is "allowed" to do something based on their Role.
  Authorization is out of scope — Roles document who SHOULD do
  what, not who is permitted to.
- **Renaming a Role instead of creating a new one.** Renaming
  silently rewrites history — every old Binding now points at a
  Role with a different meaning. If the responsibilities have
  genuinely changed, create a new Role and end the old Bindings;
  don't overwrite.
- **Putting tasks in `responsibilities` instead of WorkItems.** The
  `responsibilities` field describes ongoing duties ("review PRs",
  "approve releases"), not specific to-dos. If you find yourself
  writing "implement feature X" in responsibilities, that's a
  WorkItem.
- **Vague responsibility lists.** "Ensures quality" is not a
  responsibility; "Reviews every PR before merge to main" is. Each
  bullet should be concrete enough that you could ask a holder
  "did you do this last week" and get a yes/no answer.
- **Forgetting to log `role.created` / `role.updated`.** The audit
  trail tracks role evolution. Skipping the log makes "when did we
  add the security-reviewer role" unanswerable.

## Full reference

### Fields

| Field              | Type          | Notes                                                    |
|--------------------|---------------|----------------------------------------------------------|
| `name`             | string        | Kebab-case. Matches the suffix of `metadata.id`.         |
| `description`      | string        | One sentence. Shown in role listings.                    |
| `responsibilities` | list[string]  | Imperative bullet points. Concrete, not vague.           |
| `skills_required`  | list[string]  | Skill IDs or names. Advisory, not enforced.              |
| `default_scope`    | enum          | `project` / `sprint` / `permanent`. Default assumption for Bindings. |
| `supersedes`       | string        | Role ID this one replaces (for role renames/reorg).      |

### Roles vs Categories vs Gates

Beginners sometimes conflate three related concepts:

- **Role** — who does a thing (reviewer, developer, release-manager).
- **Category** — how a thing is classified (bug, feature, tech-debt).
- **Gate** — a checkpoint that validates a thing (code-review-passed).

A Role can be assigned via Binding; a Category is a label; a Gate is
something a process has to pass. Don't model one as another.

### No enforcement

processkit does not check that an actor filling a role has the right
`skills_required`, or that actions restricted to a role are only performed
by bound actors. Roles are descriptive. If you need RBAC, that's a
governance platform concern (DEC-017).

### Well-known roles

processkit does not ship a canonical list of roles — they vary too much per
project. But these are common enough to be mentioned here for naming
consistency: `developer`, `reviewer`, `tech-lead`, `release-manager`,
`incident-commander`, `product-owner`, `designer`, `security-reviewer`.
Projects are free to use these names or invent their own.
