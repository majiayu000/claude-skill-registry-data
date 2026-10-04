---
name: write-a-prd-local
description: Create a PRD through user interview, codebase exploration, and module design, stored locally in the repo. Use when user wants to write a PRD, create a product requirements document, or plan a new feature.
---

This skill will be invoked when the user wants to create a PRD. You may skip steps if you don't consider them necessary.

## Local PRD System

All PRDs and related tracking live in a `.prds/` directory at the repo root. This directory is self-contained and can be copied into any repo to bootstrap the same system.

### Directory Structure

```
.prds/
  README.md          # How the PRD system works (auto-generated on first run)
  _index.md          # Registry of all PRDs with status
  0001-short-slug/
    prd.md            # The PRD document
    tasks.md          # Breakdown of implementation tasks with checkboxes
    decisions.md      # Running log of decisions and changes post-creation
  0002-short-slug/
    prd.md
    tasks.md
    decisions.md
```

### Numbering

PRDs are numbered sequentially starting at 0001. Read `_index.md` to determine the next number. If `.prds/` doesn't exist yet, create the full structure from scratch starting at 0001.

### Index File Format

`_index.md` tracks all PRDs in a single table:

```markdown
# PRD Index

| #    | Title                  | Status      | Created    |
|------|------------------------|-------------|------------|
| 0001 | Feature short name     | draft       | 2026-03-18 |
| 0002 | Another feature        | in-progress | 2026-03-19 |
```

Valid statuses: `draft`, `ready`, `in-progress`, `done`, `abandoned`

### README.md (auto-generated on first PRD creation)

Generate a short README explaining:
- What the `.prds/` directory is
- How to read a PRD
- How statuses work
- That this directory is repo-portable

---

## PRD Creation Process

1. Ask the user for a long, detailed description of the problem they want to solve and any potential ideas for solutions.

2. Explore the repo to verify their assertions and understand the current state of the codebase.

3. Interview the user relentlessly about every aspect of this plan until you reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.

4. Sketch out the major modules you will need to build or modify to complete the implementation. Actively look for opportunities to extract deep modules that can be tested in isolation.

A deep module (as opposed to a shallow module) is one which encapsulates a lot of functionality in a simple, testable interface which rarely changes.

Check with the user that these modules match their expectations. Check with the user which modules they want tests written for.

5. Once you have a complete understanding of the problem and solution, create the PRD directory and files using the templates below.

6. Update `_index.md` with the new PRD entry.

---

## File Templates

### prd.md

```markdown
# PRD-{NUMBER}: {Title}

**Status:** draft
**Created:** {YYYY-MM-DD}
**Author:** {user or inferred from git config}

---

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

This list should be extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this PRD.

## Further Notes

Any further notes about the feature.
```

### tasks.md

```markdown
# PRD-{NUMBER}: {Title} - Tasks

Derived from [prd.md](./prd.md). Update as implementation progresses.

## Tasks

- [ ] Task description (module or area it touches)
- [ ] Task description (module or area it touches)

## Discovered During Implementation

Add tasks here that surface during the build but weren't in the original plan.

- [ ] ...
```

### decisions.md

```markdown
# PRD-{NUMBER}: {Title} - Decision Log

Running log of decisions, scope changes, and clarifications made after the PRD was created.

| Date       | Decision                            | Context / Reason         |
|------------|-------------------------------------|--------------------------|
| {date}     | Initial PRD created                 | -                        |
```

---

## Updating Existing PRDs

When the user wants to update a PRD:

1. Read the existing `prd.md` to understand current state
2. Discuss changes with the user
3. Update the relevant file (`prd.md` for scope changes, `tasks.md` for task changes, `decisions.md` for any change)
4. Always add an entry to `decisions.md` explaining what changed and why
5. Update status in both `prd.md` header and `_index.md` if status changed