---
name: feature-spec
description: Generate persistent feature specification documents that serve as the source of truth across sessions. Use when specifying features, documenting requirements, or when user mentions "feature spec", "write spec", "specification", "requirements doc", "define feature", or "spec this".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Feature Spec Skill

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

You create persistent feature specification documents. Specs are the source of truth that survive across sessions — they prevent context loss, scope creep, and misaligned implementations.

## Process

### Step 1: Interview

Before writing the spec, clarify with the user:

1. **What problem does this solve?** — Not what to build, but why
2. **Who is the user?** — Which user type/persona benefits
3. **What does success look like?** — How do we know it's working
4. **What's out of scope?** — Explicit boundaries prevent creep
5. **Any constraints?** — Timeline, technology, compatibility requirements

If the user provides a complete description, extract these answers from their description rather than asking.

### Step 2: Research Existing Context

1. **Check for existing specs** — `ls {project_path}/docs/specs/`
2. **Check related features** — Are there specs this feature depends on or affects?
3. **Check the codebase** — What already exists that this feature touches?
4. **Check the data model** — What entities are involved?

### Step 3: Write the Spec

Use the template below. Every section is mandatory — if a section doesn't apply, explicitly state "N/A" with a reason.

### Step 4: Identify Ripple Effects

Check if this spec affects other existing specs:
- Does it change a shared data model?
- Does it affect an API contract?
- Does it change user flows documented elsewhere?

If yes, note which specs need updating.

## Spec Template

Save to: `{project_path}/docs/specs/{feature-name}.md`

```markdown
# Feature Spec: {Feature Name}

**Status:** Draft | Approved | In Progress | Complete | Deprecated
**Author:** {who}
**Date:** {DATE}
**Last Updated:** {DATE}
**Project:** {project name}

---

## Problem Statement

{What problem exists? Why does it matter? What's the cost of not solving it?}

## User Story

As a {user type}, I want to {action}, so that {benefit}.

## Requirements

### Must Have
1. {Requirement — specific, testable}
2. {Requirement}

### Should Have
1. {Requirement}

### Won't Have (Explicit Scope Exclusions)
1. {What this feature explicitly does NOT include, and why}

## Design

### User Flow
1. User {action}
2. System {response}
3. User sees {outcome}

### Data Model Changes
{New tables, columns, or relationships needed}

| Table | Column | Type | Notes |
|-------|--------|------|-------|
| {table} | {column} | {type} | {constraints, defaults} |

### API Changes
{New or modified endpoints}

| Method | Endpoint | Request | Response | Auth |
|--------|----------|---------|----------|------|
| POST | /api/v1/{resource} | `{ field: type }` | `{ data: ... }` | Required |

### UI Changes
{Screens or components affected — describe layout and behavior}

## Edge Cases

1. **{Edge case}** — {How it should be handled}
2. **{Edge case}** — {How it should be handled}

## Dependencies

- **Internal:** {Other features or services this depends on}
- **External:** {Third-party APIs, libraries, or services}

## Acceptance Criteria

- [ ] {Testable criterion 1}
- [ ] {Testable criterion 2}
- [ ] {Testable criterion 3}

## Open Questions

- [ ] {Question that needs answering before implementation}

---

## Changelog

| Date | Author | Change |
|------|--------|--------|
| {DATE} | {who} | Initial draft |
```

## Updating Specs

When a feature changes during implementation:
1. **Update the spec first** — Don't let the code diverge from the spec
2. **Add a changelog entry** — What changed and why
3. **Check ripple effects** — Update dependent specs
4. **Update status** — Draft → Approved → In Progress → Complete

## Output

After creating the spec:
- **File saved**: {path}
- **Status**: Draft (needs approval before implementation)
- **Ripple effects**: {list of other specs that may need updating, or "None"}
- **Open questions**: {count of questions that need answers}
- **Next step**: Review and approve, then use `/plan-generation` to create implementation plan

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
