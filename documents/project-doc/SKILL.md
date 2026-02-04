---
name: project-doc
description: Organize, create, and maintain documentation for projects. Use when the user asks to set up docs structure, write documentation, update existing docs, create READMEs, ADRs, guides, or any project documentation. Triggers include "organize my docs", "set up documentation", "write docs for this", "update the README", "document this", or when working on a project that needs documentation.
---

# Project Docs

Manage documentation for projects with consistent structure and quality.

## Standard Structure

Use this structure for all projects unless the user specifies otherwise:

```
docs/
├── README.md           # Project overview, quick start, links to other docs
├── decisions/          # Architecture Decision Records (ADRs)
│   └── 001-initial-setup.md
├── guides/             # How-to guides for specific tasks
└── reference/          # API docs, config options, schemas
```

## When to Create Docs

**Always create/update docs when:**

- Setting up a new project → Create README.md + initial ADR
- Making architectural decisions → Create ADR in `decisions/`
- Adding configuration or APIs → Update `reference/`

**Ask before creating:**

- If user hasn't mentioned docs but the task would benefit from documentation
- If unsure which doc type fits best

## Doc Types and Templates

### README.md

```markdown
# [Project Name]

[One sentence: what this does and why it exists]

## Quick Start

[Minimal steps to get running - 3-5 commands max]

## Configuration

[Key environment variables or config files]

## Documentation

- [Decisions](docs/decisions/) - Why things are built this way
- [Guides](docs/guides/) - How to do specific tasks
```

### ADR (Architecture Decision Record)

Place in `docs/decisions/NNN-short-title.md`. Number sequentially (001, 002...).

```markdown
# [Number]. [Title]

Date: [YYYY-MM-DD]
Status: [proposed | accepted | deprecated | superseded by [NNN]]

## Context

[What situation or problem prompted this decision? 2-4 sentences.]

## Decision

[What we decided. Be specific.]

## Consequences

[What this enables and what tradeoffs we accept. Both positive and negative.]
```

### Guide

Place in `docs/guides/[topic].md`.

```markdown
# How to [Task]

[Brief intro - when and why you'd do this]

## Steps

[Detailed walkthrough with code examples where relevant]

## Tips

[Optional: gotchas, best practices, shortcuts]
```

## Writing Style

- **Be concise**: If a sentence doesn't add value, delete it
- **Use examples**: Show don't tell, especially for technical docs
- **Present tense**: "Run `npm start`" not "You should run..."
- **No fluff**: Skip "In this document we will..." intros

## Organizing Existing Docs

When asked to organize existing docs:

1. **Audit first**: List what exists and categorize by type (decision, guide, runbook, reference)
2. **Propose structure**: Show the user the target structure with their docs mapped
3. **Wait for approval**: Don't move/rename without confirmation
4. **Execute**: Move files, update any internal links

## Updating Docs

When code changes affect documentation:

1. Identify which docs are impacted
2. Update in-place using minimal edits
3. If a decision is superseded, update its status and link to the new ADR

## Creating Docs for Existing Projects

If the project has no docs folder:

1. Create `docs/` with README.md
2. Ask: "Want me to add an initial ADR documenting [key architectural choice]?"
3. Create additional docs as work reveals the need
