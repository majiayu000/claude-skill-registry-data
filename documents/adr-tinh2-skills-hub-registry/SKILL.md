---
name: adr
description: "Create and manage Architecture Decision Records using the Michael Nygard format. Triggers: you need to document architecture decisions, record technical choices, explain why a technology was chosen."
version: "2.0.1"
category: docs
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Create or manage Architecture
Decision Records for this project.

INPUT:
$ARGUMENTS

Accepted arguments:
- A decision description (e.g., "Use PostgreSQL over MongoDB for primary datastore")
  Creates a new ADR for this decision.
- `retrospective` or `retro`: Analyze the codebase and generate ADRs for decisions
  already made but not documented.
- `index`: Regenerate the ADR index file.
- `supersede <N> <new decision>`: Create a new ADR that supersedes ADR-N.
- `deprecate <N>`: Mark ADR-N as deprecated.
- `list`: List all existing ADRs with their statuses.

If no arguments provided, run in retrospective mode.

============================================================
PHASE 1: DIRECTORY SETUP
============================================================

Step 1.1 -- Initialize ADR Directory

Check if `docs/adr/` exists. If not, create it.

Check for ADRs in alternative locations:
- `adr/`
- `docs/decisions/`
- `decisions/`
- `doc/adr/`

If found in an alternative location, use that location instead of creating a new one.

Step 1.2 -- Determine Next ADR Number

Scan existing ADR files matching the pattern `NNNN-*.md` (e.g., `0001-use-postgresql.md`).
Find the highest number and increment by 1 for the next ADR.
If no ADRs exist, start at 0001.

Step 1.3 -- Read Existing ADRs

Read all existing ADR files to understand:
- What decisions have already been documented
- Current statuses (proposed, accepted, deprecated, superseded)
- Cross-references between ADRs

============================================================
PHASE 2: NEW ADR CREATION
============================================================

When creating a new ADR from a decision description:

Step 2.1 -- Research the Decision

Analyze the codebase to gather context for the decision:
- Read config files related to the technology choice
- Look for alternatives that were considered (comments, TODOs, removed code)
- Identify what the decision affects (which files, modules, services)
- Check git history for when the decision was implemented

Step 2.2 -- Write ADR

Use the Michael Nygard format:

```markdown
# [ADR-NNNN] [Title: Short Decision Statement]

**Date:** YYYY-MM-DD

**Status:** [proposed | accepted | deprecated | superseded by [ADR-XXXX](XXXX-title.md)]

## Context

[What is the issue that we're seeing that is motivating this decision or change?
Describe the forces at play: technical, political, social, project-specific.
These forces are likely in tension and should be called out as such.
State facts, not opinions. 2-4 paragraphs.]

## Decision

[What is the change that we're proposing and/or doing?
State the decision clearly and unambiguously.
Use active voice: "We will use X" not "X should be used."
1-2 paragraphs.]

## Consequences

[What becomes easier or more difficult to do because of this change?
Include both positive and negative consequences.
Be honest about trade-offs.

**Positive:**
- [consequence]
- [consequence]

**Negative:**
- [consequence]
- [consequence]

**Neutral:**
- [consequence]
]
```

Step 2.3 -- File Naming

Name the file: `NNNN-kebab-case-title.md`
- NNNN is zero-padded to 4 digits
- Title is derived from the decision, converted to kebab-case
- Keep filename under 60 characters
- Example: `0003-use-postgresql-for-primary-datastore.md`

============================================================
PHASE 3: RETROSPECTIVE MODE
============================================================

When running in retrospective mode, analyze the codebase to infer
architectural decisions that were made but never documented:

Step 3.1 -- Detect Decisions

Scan for these categories of decisions:

| Category | What to Look For |
|----------|-----------------|
| Language/Runtime | Primary language, runtime version constraints |
| Framework | Web framework, UI framework, CLI framework choice |
| Database | Database type, ORM/query builder choice |
| Auth | Authentication strategy, provider choice |
| State Management | State management library/pattern |
| API Style | REST vs GraphQL vs gRPC, API versioning strategy |
| Infrastructure | Docker, K8s, serverless, cloud provider |
| CI/CD | Pipeline tool, deployment strategy |
| Testing | Test framework, testing strategy (unit/integration/e2e) |
| Monorepo vs Polyrepo | Repository structure decision |
| Dependency Management | Package manager, lockfile strategy |
| Code Style | Linter, formatter, style guide |
| Error Handling | Error handling strategy, logging approach |
| Caching | Caching strategy, cache provider |

Step 3.2 -- Generate ADRs

For each detected decision:
1. Determine if an ADR already exists for this decision
2. If not, create one with status "accepted" and today's date
3. In the Context section, note that this is a retrospective ADR:
   "This ADR was created retrospectively to document a decision already in effect."
4. Infer context from the codebase (why this choice likely was made)
5. Document consequences based on how the choice has played out

Step 3.3 -- Prioritize

Generate retrospective ADRs in priority order:
1. Framework and language choices (highest architectural impact)
2. Database and data layer decisions
3. Authentication and security patterns
4. Infrastructure and deployment choices
5. Testing and code quality decisions

============================================================
PHASE 4: INDEX GENERATION
============================================================

Generate or update `docs/adr/README.md` (or `docs/adr/index.md`):

```markdown
# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for [Project Name].

## What is an ADR?

An ADR is a short document that captures an important architectural decision
made along with its context and consequences.

## ADR Index

| # | Title | Status | Date |
|---|-------|--------|------|
| [0001](0001-title.md) | Title | Accepted | YYYY-MM-DD |
| [0002](0002-title.md) | Title | Superseded by [0003](0003-title.md) | YYYY-MM-DD |
| ... | ... | ... | ... |

## Statuses

- **Proposed** -- Under discussion, not yet decided
- **Accepted** -- Decision has been made and is in effect
- **Deprecated** -- Decision is no longer relevant
- **Superseded** -- Replaced by a newer decision (linked)
```


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing documentation, validate completeness:

1. Verify all required sections are present and non-empty.
2. Verify internal cross-references and links resolve correctly.
3. Verify no placeholder text remains ("{TODO}", "[TBD]", "...", "etc.").
4. Verify code examples are syntactically valid.

IF VALIDATION FAILS:
- Identify which sections are incomplete or contain placeholders
- Re-generate only the deficient sections
- Repeat up to 2 iterations

============================================================
OUTPUT
============================================================

## ADR Report

### Action Taken
- **Mode:** [New ADR / Retrospective / Index / Supersede / Deprecate]
- **ADRs Created:** N
- **ADRs Updated:** N
- **Total ADRs:** N

### ADR Summary

| # | Title | Status | Date |
|---|-------|--------|------|
| NNNN | Title | Status | Date |
| ... | ... | ... | ... |

### Files Written
- `docs/adr/NNNN-title.md` -- [description]
- `docs/adr/README.md` -- Updated index


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /adr — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT fabricate technical context. Only document decisions that are
  evident from the codebase.
- Do NOT create ADRs for trivial decisions (e.g., "use prettier for formatting"
  is too small; "adopt Prettier + ESLint with specific rule overrides" is worth documenting).
- Do NOT create duplicate ADRs for decisions already documented.
- Do NOT change the status of existing ADRs unless explicitly asked.
- Do NOT use ADR numbers that are already taken.
- Do NOT include opinions in the Context section -- state facts and forces.

NEXT STEPS:

After creating ADRs:
- "Run `/document` to check overall documentation health."
- "Run `/diagram` to generate architecture diagrams that complement these ADRs."
- "Run `/arch-review` to review the architecture decisions for consistency."
