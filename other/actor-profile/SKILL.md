---
name: actor-profile
description: |
  Create and maintain Actor entities — humans and AI agents that participate in the project. Use when adding a new collaborator (human or agent) to the project, updating their preferences/expertise, or querying who does what.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-actor-profile
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
      primitives: [Actor]
      mcp_tools:
        - create_actor
        - get_actor
        - update_actor
        - deactivate_actor
        - list_actors
      templates: [actor-human, actor-agent]
---

# Actor Profile Management

## Intro

Actors are the entities that do things in the project — humans, AI agents, and
services. This skill creates and maintains their profiles: name, type, contact,
expertise, preferences, working style.

> **MCP server.** This skill ships a self-contained MCP server at
> `mcp/server.py` (PEP 723 script — requires `uv` and Python ≥ 3.10 on
> PATH). Agent harnesses reach its tools by reading a single MCP config
> file at startup, so the contents of `mcp/mcp-config.json` must be merged
> into the harness's MCP config and placed at the harness-specific path
> before this skill is usable. If processkit was installed by an installer,
> that wiring is the installer's responsibility; if processkit was
> installed manually, the project owner must do it by hand.

## Actor ID classes

Two accepted ID shapes for Actor entities (see `context/schemas/actor.yaml`
`spec.role_actor_ids` and `DEC-20260421_2036-SoundIvy-two-class-actor-ids`):

**Role actor** — `ACTOR-<kebab-slug>`

Stable identifier for a durable team role filled by successive agents or
people (e.g. `ACTOR-product-manager`, `ACTOR-sr-architect`). Current
allowlist (from `spec.role_actor_ids` in `actor.yaml`): `assistant`,
`developer`, `jr-architect`, `jr-developer`, `jr-researcher`,
`product-manager`,
`sr-architect`, `sr-researcher`. Use when the actor represents a role, not
an individual.

**Identity actor** — `ACTOR-<YYYYMMDD_HHMM>-<WordPair>-<slug>`

Canonical id-management format. Use for a specific individual, session, or
historical figure (owner, legacy backfill, session-specific agent). Example:
`ACTOR-20260421_0144-ThriftyOtter-owner`.

**Adding a role to the allowlist**

Requires amending `spec.role_actor_ids` in `context/schemas/actor.yaml`
(and its `src/` mirror). This is a cross-cutting schema change — record a
DecisionRecord explaining why the new role is needed before making the
change. pk-doctor will ERROR on any `ACTOR-<slug>` ID whose slug is not in
the allowlist.

## Overview

### When to create an Actor

Create an Actor entity the first time a person or agent participates in a
way the project needs to remember:
- Someone gets assigned a WorkItem → create their Actor if missing.
- An agent starts making decisions → create its Actor.
- A service account performs automated actions → create its Actor.

Do **not** promote every mention of a person into an Actor. Actors are for
collaborators with ongoing involvement, not for every name that appears in a
commit message.

### Actor types

| type         | Example                                     |
|--------------|---------------------------------------------|
| `human`      | Project members, reviewers, stakeholders    |
| `ai-agent`   | Claude, Copilot, Aider, Cursor, custom MCP  |
| `service`    | GitHub Actions, CI bots, deploy pipelines   |

### Shape

```yaml
---
apiVersion: processkit.projectious.work/v2
kind: Actor
metadata:
  id: ACTOR-alice
  created: 2026-04-06T00:00:00Z
spec:
  type: human
  name: "Alice Chen"
  email: alice@example.com
  expertise: [backend, databases, rust]
  preferences:
    commit_style: conventional
    timezone: Europe/Berlin
  active: true
---

Optional Markdown body — bio, context, working-style notes.
```

### Workflow

1. Pick an ID: `ACTOR-<short-name>` where short-name is memorable and unique.
2. Set `type` (human / ai-agent / service).
3. Fill in `name` + contact (email for humans; nothing for agents; service
   account identifier for services).
4. Record `expertise` as a tag list — used by assignment skills.
5. Write the Actor file to `context/actors/`.
6. Log a `LogEntry` with `event_type: actor.created`.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Creating an Actor for every name mentioned in a commit or
  comment.** Actors are for collaborators with ongoing involvement,
  not for every string that looks like a name. If the person doesn't
  have at least one upcoming WorkItem, decision, or Binding pointing
  at them, don't create the Actor yet.
- **Putting personal or sensitive information in a public Actor file.**
  Personal context (relationship dynamics, private preferences,
  personal contact info) belongs in `context/owner/private/...` with
  `privacy: user-private`, not in the Actor entity which defaults to
  project-visible. Check the privacy field on the entity before
  writing sensitive content.
- **Setting `type` wrong.** `human` / `ai-agent` / `service` aren't
  cosmetic — other skills filter on type (e.g., to send a Slack ping
  only to humans, or to auto-promote service-account actions). Wrong
  type causes silent miscategorization downstream.
- **Updating an Actor when the relationship is what changed.** If
  Alice's role on the project changed, that's a new Binding (or
  ending the old one), NOT an update to her Actor. The Actor is
  who she IS; the Binding is what she's DOING.
- **Reusing a name as an ID for two distinct people.** Two
  collaborators named "Alice" need distinct Actor IDs
  (`ACTOR-alice-pm` vs `ACTOR-alice-eng`). The ID is forever; the
  display name is mutable. Disambiguate at creation time, not later.
- **Hallucinating Actor IDs when other skills reference them.** If
  workitem-management is asked to assign a workitem to "Bob", look
  up `ACTOR-bob` (or all `ACTOR-bob-*`) via `index-management` first.
  Inventing an ID like `ACTOR-bob` without verifying creates a
  dangling reference that breaks at the next index validation.
- **Forgetting to log `actor.created`.** Use `event-log` after every
  Actor creation. The audit trail tracks "who joined when", and
  skipping the log makes "when did Alice start working on this?"
  unanswerable.

## Full reference

### Fields

| Field           | Type              | Notes                                                     |
|-----------------|-------------------|-----------------------------------------------------------|
| `type`          | enum              | `human` / `ai-agent` / `service`                          |
| `name`          | string            | Display name. For agents: model name + version.           |
| `email`         | string            | Optional. Human actors only.                              |
| `handle`        | string            | Optional. GitHub handle, Slack user, etc.                 |
| `expertise`     | list[string]      | Tags used by assignment suggestions.                      |
| `roles`         | list[string]      | Role IDs. For scoped roles prefer a Binding over this.    |
| `preferences`   | map               | Free-form. See conventional keys below.                   |
| `active`        | bool              | `false` = profile preserved but no new work assigned.     |
| `joined_at`     | datetime          | When they became part of the project.                     |
| `left_at`       | datetime          | When they stopped (sets `active: false`).                  |

### Conventional preference keys

- `commit_style`: `conventional` / `freeform`
- `timezone`: IANA name
- `review_style`: `strict` / `pragmatic` / `light`
- `communication`: `async` / `sync` / `mixed`
- `languages`: human languages for communication

These are conventions, not enforced. Projects may add any preferences they like.

### Scoped roles: use a Binding, not the `roles` field

`spec.roles` is a shortcut for "Alice is a developer" when that's true
everywhere in the project. If "Alice is the tech lead for Project X but a
regular developer everywhere else", use a Binding entity instead:

```yaml
kind: Binding
spec:
  type: role-assignment
  subject: ACTOR-alice
  target: ROLE-tech-lead
  scope: SCOPE-project-x
```

See `skills/binding-management` for details.

### Deactivation, not deletion

When an actor leaves the project, set `active: false` and `left_at`. Do not
delete the file — historical LogEntries and Bindings reference it. Queries
for "current team" should filter by `active: true`.

### Privacy considerations

Actor files are checked into git and visible to everyone with repo access.
Do not put sensitive contact info (phone, home address) in Actor files.
Keep email optional — agents and services do not need one.
