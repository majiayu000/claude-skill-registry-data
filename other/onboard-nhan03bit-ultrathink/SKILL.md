---
name: onboard
description: Codebase onboarding orchestrator that scans, documents, summarizes, and teaches a codebase to new developers or to the AI agent itself.
layer: orchestrator
category: orchestration
triggers:
  - "/onboard"
  - "onboard me to this codebase"
  - "explain this codebase"
  - "walk me through this project"
  - "learn this codebase"
  - "what does this project do"
inputs:
  - Codebase path or repository
  - Optional focus area (specific module, feature, or layer)
  - Optional audience level (junior, senior, architect)
  - Optional output format (interactive walkthrough, written guide, diagram-heavy)
outputs:
  - Project overview and architecture summary
  - Module-by-module breakdown with key files
  - Data flow and dependency diagrams
  - Key patterns and conventions guide
  - Entry points and critical paths map
  - Onboarding guide document
linksTo:
  - scout
  - research
  - sequential-thinking
  - mermaid
  - docs-writer
  - plan
  - brainstorm
linkedFrom:
  - team
  - audit
preferredNextSkills:
  - cook
  - audit
  - kanban
fallbackSkills:
  - scout
  - research
riskLevel: low
memoryReadPolicy: full
memoryWritePolicy: always
sideEffects:
  - Reads all source files (read-only)
  - May generate documentation files (if requested)
  - May generate diagram files (if requested)
  - Writes comprehensive codebase knowledge to memory for future sessions
---

# Onboard

## Purpose

Onboard is the codebase learning and teaching orchestrator. It systematically explores a codebase and produces a comprehensive understanding that it can either present to a human developer or internalize for its own future use. Onboard answers the question every new team member asks: "How does this all fit together?"

Onboard goes beyond just listing files and directories. It traces data flows, identifies architectural patterns, maps dependencies, finds the critical paths, and explains the "why" behind design decisions when evidence is available. It produces both high-level summaries for quick orientation and deep-dive documentation for reference.

## Workflow

### Phase 1: Scan
1. **Invoke `scout`** -- Perform a comprehensive codebase scan:
   - Directory structure and organization pattern
   - File types and language composition
   - Entry points (main files, route files, index files)
   - Configuration files and their purposes
   - Dependency manifest (package.json, Cargo.toml, etc.)
   - Test file locations and patterns
   - Build and deployment configuration
2. **Identify the tech stack** -- Catalog all technologies:
   - Languages and versions
   - Frameworks and libraries (with versions)
   - Database and storage technologies
   - Infrastructure and deployment tools
   - Development tools (linters, formatters, test runners)
3. **Invoke `research`** (if needed) -- For unfamiliar frameworks or libraries, look up their purpose and patterns via Context7 to understand what role they play.

### Phase 2: Map Architecture
4. **Identify architectural pattern** -- Determine the overall architecture:
   - Monolith vs microservices vs monorepo
   - MVC, layered, hexagonal, event-driven, etc.
   - Client-server, serverless, edge, etc.
5. **Map module boundaries** -- Identify logical modules and their responsibilities:
   - What each top-level directory represents
   - How modules communicate (imports, APIs, events, shared state)
   - Module ownership and dependency direction
6. **Invoke `mermaid`** -- Generate architecture diagrams:
   - High-level system architecture
   - Module dependency graph
   - Data flow diagrams for key operations
   - Database entity relationship diagram (if schema is accessible)
7. **Trace critical paths** -- Identify and document the most important code paths:
   - User authentication flow
   - Primary data creation/update flow
   - Request lifecycle (from entry to response)
   - Error handling flow
   - Background job processing (if applicable)

### Phase 3: Analyze Patterns & Conventions
8. **Extract coding conventions** -- Document the patterns the codebase follows:
   - Naming conventions (files, functions, variables, components)
   - File organization patterns (co-location, feature-based, layer-based)
   - Import patterns (absolute vs relative, barrel files)
   - Component patterns (composition, render props, hooks)
   - State management approach
   - Error handling patterns
   - Logging conventions
9. **Identify key abstractions** -- Find and explain the core abstractions:
   - Base classes or shared interfaces
   - Custom hooks or utilities used everywhere
   - Middleware or decorator patterns
   - Configuration and environment handling
10. **Invoke `sequential-thinking`** -- For complex architectural decisions, reason through why they were made based on evidence in the code.

### Phase 4: Document
11. **Generate the onboarding guide** -- Structure the knowledge into a consumable format:

    **Section 1: Quick Start**
    - What this project does (one paragraph)
    - How to set it up locally
    - How to run it
    - How to run tests

    **Section 2: Architecture Overview**
    - System architecture diagram
    - Tech stack table
    - Module map with one-line descriptions

    **Section 3: Key Concepts**
    - Core domain concepts and terminology
    - Key abstractions and where they live
    - Patterns and conventions to follow

    **Section 4: Code Map**
    - Directory-by-directory breakdown
    - Key files and what they do
    - Entry points for each major feature

    **Section 5: Data Flow**
    - How data moves through the system
    - Critical path walkthroughs
    - Database schema overview

    **Section 6: Development Guide**
    - How to add a new feature (where to put what)
    - How to add a new test
    - How to deploy
    - Common gotchas and tribal knowledge

12. **Invoke `docs-writer`** (if writing to file) -- Format and write the onboarding guide as a document.

### Phase 5: Teach
13. **Present the summary** -- Deliver the onboarding to the user in the requested format:
    - **Interactive**: Walk through the codebase conversationally, answering questions as they arise
    - **Written guide**: Deliver the full document
    - **Diagram-heavy**: Lead with visual architecture diagrams, supplement with text
14. **Answer questions** -- Be prepared to go deeper on any area the user asks about.
15. **Write to memory** -- Store the codebase knowledge for future sessions so subsequent interactions don't need a full re-scan.

## Output Formats

### Quick Summary (for experienced developers)
```
Project: [name] - [one-line description]
Stack: [language] + [framework] + [database] + [deployment]
Architecture: [pattern] with [key characteristic]
Entry: [main entry file] -> [routing] -> [handlers] -> [data layer]
Tests: [test runner] in [test directory], run with [command]
Key dirs: [dir1] (purpose), [dir2] (purpose), [dir3] (purpose)
```

### Full Onboarding (for new team members)
Complete multi-section document as described in Phase 4.

### Architecture Deep Dive (for architects)
Focused on architectural decisions, trade-offs, and technical debt with supporting diagrams.

## Decision Points

| Condition | Action |
|-----------|--------|
| Small project (< 50 files) | Quick summary format, skip deep architecture |
| Large project (> 500 files) | Full onboarding with all sections |
| Monorepo | Document each package/app separately, then integration |
| User asks about specific area | Focus onboard on that area, brief overview of rest |
| Unfamiliar technology detected | Invoke `research` via Context7 before documenting |
| Complex architecture | Invoke `sequential-thinking` to explain design rationale |
| Codebase already scanned in memory | Skip Phase 1, update only changed areas |

## Usage

Use Onboard when encountering a new codebase for the first time, when a new team member joins, or when you need to refresh understanding of a project you haven't worked on recently.

**Best for:**
- First encounter with a new codebase
- Onboarding new team members
- Documenting an undocumented project
- Refreshing context after time away from a project
- Understanding a project before an audit
- Preparing to contribute to an open-source project

**Not ideal for:**
- Building features (use `cook` after onboarding)
- Code review (use `code-review`)
- Auditing for issues (use `audit`)

## Examples

### Example 1: Full codebase onboarding
```
User: /onboard Walk me through this codebase

Onboard workflow:
1. scout -> Scan: Next.js app, 234 files, TypeScript, Prisma, Tailwind
2. Architecture -> App Router pattern, API routes, Prisma data layer
3. mermaid -> System diagram, module deps, auth flow, data creation flow
4. Patterns -> Feature-based directories, custom hooks pattern, Zod validation
5. Document -> Full 6-section onboarding guide
6. Present -> Deliver guide, offer to deep-dive on any section
```

### Example 2: Focused module onboarding
```
User: /onboard Explain the payment system in this codebase

Onboard workflow:
1. scout -> Focus scan on payment-related files and dependencies
2. Architecture -> Payment module boundaries, Stripe integration points
3. mermaid -> Payment flow diagram (checkout -> webhook -> fulfillment)
4. Patterns -> Payment-specific error handling, retry logic, idempotency
5. Document -> Payment system deep-dive document
6. Present -> Walkthrough of the payment flow with key files
```

### Example 3: Self-onboarding (AI learning)
```
User: /onboard Learn this codebase so you can help me effectively

Onboard workflow:
1. scout -> Full codebase scan
2. Architecture -> Map all modules and patterns
3. Key abstractions -> Identify core utilities, shared types, conventions
4. Memory write -> Store complete codebase map, conventions, and patterns
5. Present -> Brief summary to user, deep knowledge stored for future use
6. Ready -> "I've learned the codebase. Here's a quick overview..."
```

### Example 4: Open-source contribution prep
```
User: /onboard I want to contribute to this open-source project, help me understand it

Onboard workflow:
1. scout -> Scan codebase + look for CONTRIBUTING.md, CODE_OF_CONDUCT.md
2. Architecture -> Map the project structure and key modules
3. research -> Check project docs, issue tracker patterns, PR conventions
4. Document -> Contributor-focused guide: where to add code, test patterns,
              PR expectations, coding style
5. Present -> "Here's how this project works and how to contribute..."
```

## Guardrails

- **Read-only.** Onboard never modifies source code. It only reads and analyzes.
- **Start broad, go deep.** Always provide the high-level overview before diving into details.
- **Show, don't just tell.** Use diagrams for architecture, code snippets for patterns, examples for conventions.
- **Admit uncertainty.** If the "why" behind a design decision is unclear, say so rather than guessing.
- **Respect scope.** If asked about one module, don't dump the entire codebase analysis.
- **Update, don't rebuild.** If the codebase was previously onboarded and stored in memory, only re-scan changed areas.
- **Tailor to the audience.** Junior developers need more explanation; architects need more diagrams and trade-off analysis.
- **Always include "how to get started."** The most important outcome is that the reader can set up and run the project.
