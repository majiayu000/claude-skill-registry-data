---
name: library-research
description: >-
  This skill should be used when the user asks to "evaluate a library", "research a framework",
  "check if X supports Y", "how does this library work", "implement using X", "add library X
  to the project", "what can X do", "compare libraries", or needs to go from documentation
  research to implementation for any library, framework, or plugin. Covers the full lifecycle:
  research, evaluation, and implementation.
---

# Library Research & Implementation

Research, evaluate, and implement libraries, frameworks, and plugins. Covers the full lifecycle
from documentation discovery to production code.

For detailed evaluation criteria and implementation checklists, see [references/evaluation-guide.md](references/evaluation-guide.md).

## Workflow

### Phase 1: Research

#### Step 1 - Resolve the Library

Use `resolve-library-id` (Context7 MCP) to find the exact library ID:

```
resolve-library-id(libraryName: "library-name", query: "what the user wants to accomplish")
```

If multiple matches exist, present the top candidates with their documentation coverage and benchmark scores. Let the user choose.

#### Step 2 - Query Documentation

Use `query-docs` (Context7 MCP) with specific, targeted queries:

```
query-docs(libraryId: "/org/project", query: "specific question about capability or pattern")
```

Run multiple queries to cover:
1. **Core concepts** - "Getting started and core API overview"
2. **Specific capability** - The exact feature the user asked about
3. **Configuration and setup** - "Installation, configuration, and requirements"

Limit to 3 calls per question. If information is insufficient, supplement with `WebSearch` and `WebFetch` for the official docs site.

#### Step 3 - Build the Assessment

Compile findings into a structured assessment:

- **What it does** - Core purpose and capabilities
- **What it supports** - Features, integrations, platforms
- **What it doesn't support** - Known limitations, missing features
- **API surface** - Key APIs, hooks, components, or functions
- **Dependencies** - Required peer dependencies, bundle size impact
- **Maturity** - Version stability, release frequency, community size

Present this to the user before moving to implementation. Stop here if the user only asked for research.

### Phase 2: Evaluation (when comparing alternatives)

When the user needs to choose between libraries, research each candidate using Phase 1, then compare using these criteria:

| Criteria | What to check |
|---|---|
| Feature coverage | Does it solve the specific problem? |
| API ergonomics | How clean is the integration? |
| Bundle size | Impact on client-side builds |
| Maintenance | Last release, open issues ratio, bus factor |
| Ecosystem fit | Works with existing stack (check peer deps) |
| TypeScript | First-class types or @types package |
| Documentation | Quality, examples, up-to-date |

Present a comparison table. Recommend the best fit with rationale.

### Phase 3: Implementation

Only proceed when the user explicitly asks to implement.

#### Step 1 - Check Project Conventions

Before writing code, discover existing patterns:

```
Glob: **/package.json                    # Existing dependencies
Grep: "import.*from" for similar libs    # Import patterns
Glob: **/*.config.{js,ts,mjs,cjs}       # Configuration patterns
```

Read the project's CLAUDE.md or architecture docs for conventions.

#### Step 2 - Query Implementation Patterns

Use Context7 for implementation-specific docs:

```
query-docs(libraryId, "how to integrate with [project's framework]")
query-docs(libraryId, "TypeScript setup and configuration")
query-docs(libraryId, "best practices and common patterns")
```

#### Step 3 - Implement

Follow this order:
1. **Install** - Add dependency with the project's package manager
2. **Configure** - Setup files, env vars, initialization
3. **Integrate** - Write the actual integration code following project conventions
4. **Validate** - Verify types, linting, and tests pass

#### Step 4 - Verify

Run the project's quality gates:
- TypeScript compilation passes
- Linter passes
- Existing tests still pass
- New integration works as expected

## Key Principles

1. **Docs over assumptions.** Always query actual documentation. Never assume an API exists based on naming conventions alone.
2. **Research before code.** Complete Phase 1 before writing any implementation code. Present findings and get user confirmation.
3. **Project conventions first.** Match the existing project's patterns for imports, configuration, file structure, and coding style.
4. **Minimal integration.** Only add what the user asked for. Avoid wrapping libraries in unnecessary abstractions.
5. **Version awareness.** Context7 returns current documentation. Flag if the project uses a different version than what's documented.
