---
name: repomix
description: Repository packaging, structure analysis, and codebase summarization for efficient AI consumption
layer: utility
category: tooling
triggers:
  - "analyze this repo"
  - "repository structure"
  - "codebase overview"
  - "pack this repo"
  - "project structure"
  - "understand this codebase"
inputs:
  - repo_path: Path to the repository root
  - scope: full | directory | files — what to analyze
  - depth: shallow | medium | deep — level of detail
  - focus: specific areas of interest (optional)
outputs:
  - structure_map: Directory tree with annotations
  - architecture_summary: High-level architecture description
  - dependency_graph: Key dependencies and their roles
  - entry_points: Main entry points and their purposes
  - tech_stack: Technologies, frameworks, and tools used
  - key_patterns: Coding patterns and conventions used
linksTo:
  - context-engineering
  - docs-seeker
  - data-modeling
linkedFrom:
  - orchestrator
  - planner
  - code-architect
preferredNextSkills:
  - context-engineering
  - docs-seeker
fallbackSkills:
  - context-engineering
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: selective
sideEffects: []
---

# Repomix

## Purpose

This skill transforms a repository into a structured, compressed representation optimized for AI comprehension. When an agent needs to understand a codebase — its architecture, patterns, dependencies, and conventions — this skill performs systematic analysis and produces context-efficient summaries that fit within token budgets.

Think of it as "repository cartography" — creating maps at different zoom levels so the agent can navigate efficiently.

## Key Concepts

### Analysis Layers

```
LAYER 0 — MANIFEST (< 500 tokens):
  Project name, type, tech stack, entry point
  "Next.js 14 SaaS app with Prisma + PostgreSQL, deployed on Vercel"

LAYER 1 — SKELETON (500-2000 tokens):
  Directory tree (depth 2-3) with annotations
  Key configuration files summarized
  Main dependencies listed

LAYER 2 — ARCHITECTURE (2000-5000 tokens):
  Module boundaries and responsibilities
  Data flow between major components
  API surface (routes/endpoints)
  Database schema overview

LAYER 3 — DETAILED (5000-15000 tokens):
  Key file contents (entry points, configs, types)
  Pattern examples from the codebase
  Test structure and coverage areas
  Build and deployment pipeline

LAYER 4 — FULL (15000+ tokens):
  All significant source files
  Complete type definitions
  Test files
  Documentation
```

### File Significance Ranking

Not all files are equally important. Rank by significance:

| Rank | File Type | Examples | Why Important |
|------|-----------|----------|---------------|
| S | Configuration | package.json, tsconfig.json, .env.example | Define project constraints |
| S | Entry points | app/layout.tsx, src/index.ts, main.py | Starting points for understanding |
| A | Type definitions | types/*.ts, interfaces/, schemas/ | Define the domain model |
| A | Route definitions | app/**/page.tsx, routes/*.ts | Define the API/page surface |
| B | Key business logic | services/, lib/, utils/ | Core functionality |
| B | Database schema | prisma/schema.prisma, migrations/ | Data model |
| C | Components | components/**/*.tsx | UI building blocks |
| C | Tests | **/*.test.*, **/*.spec.* | Behavior documentation |
| D | Static assets | public/, assets/ | Usually irrelevant to AI |
| D | Generated files | dist/, .next/, node_modules/ | Never include |

## Workflow

### Phase 1: Project Identification

```
STEP 1: Read the root directory
  → ls -la [repo_path]
  → Identify: language, framework, build system

STEP 2: Read the manifest file
  → package.json / requirements.txt / go.mod / Cargo.toml / pom.xml
  → Extract: name, version, dependencies, scripts

STEP 3: Read configuration files
  → tsconfig.json / .eslintrc / webpack.config / next.config
  → Extract: compilation target, module system, custom paths

STEP 4: Check for documentation
  → README.md, CONTRIBUTING.md, docs/
  → Extract: project purpose, setup instructions, architecture notes

OUTPUT:
  PROJECT: [name]
  TYPE: [web app / API / library / CLI / monorepo]
  LANGUAGE: [primary language + version]
  FRAMEWORK: [framework + version]
  BUILD: [build tool]
  DEPLOY: [deployment target if detectable]
```

### Phase 2: Structure Mapping

```
STEP 1: Generate directory tree
  → Use Glob to discover structure: **/* (exclude node_modules, .git, dist, etc.)
  → Build tree representation

STEP 2: Annotate directories
  src/
    ├── app/          # Next.js App Router pages and layouts
    ├── components/   # React components (organized by feature)
    │   ├── ui/       # Shared UI primitives (Button, Card, Input)
    │   ├── auth/     # Authentication components
    │   └── dashboard/# Dashboard-specific components
    ├── lib/          # Shared utilities and helpers
    ├── services/     # External service integrations
    ├── types/        # TypeScript type definitions
    └── hooks/        # Custom React hooks

STEP 3: Identify key files
  → Rank files by significance (see table above)
  → Mark entry points, configuration, and type definitions
```

### Phase 3: Architecture Analysis

```
STEP 1: Map the data flow
  USER REQUEST
    → Route handler (app/api/**/route.ts)
      → Service layer (services/*.ts)
        → Database (prisma/schema.prisma)
      → Response

STEP 2: Identify module boundaries
  MODULE: auth
    ENTRY: lib/auth.ts
    COMPONENTS: components/auth/*
    ROUTES: app/(auth)/*
    SERVICES: services/auth-service.ts
    TYPES: types/auth.ts

STEP 3: Map external dependencies
  RUNTIME:
    next@14.2.0 — Framework
    prisma@5.x — ORM
    zod@3.x — Validation
    next-auth@5.x — Authentication
  DEV:
    typescript@5.x — Type system
    tailwindcss@3.x — Styling
    vitest@1.x — Testing

STEP 4: Identify patterns and conventions
  NAMING: kebab-case files, PascalCase components, camelCase functions
  STATE: Server components by default, 'use client' for interactive
  FETCHING: Server-side with async components, no client-side fetching
  STYLING: Tailwind utility classes, cn() helper for merging
  VALIDATION: Zod schemas for all external input
  ERROR: Error boundaries + try/catch in server actions
```

### Phase 4: Summary Generation

Produce summaries at the requested depth level:

```
MANIFEST SUMMARY:
  "Next.js 14 SaaS application with App Router. Uses Prisma ORM with PostgreSQL,
  NextAuth for authentication, and Tailwind CSS for styling. Monorepo-like
  structure with feature-based component organization. 47 routes, 23 API
  endpoints, 156 components."

ARCHITECTURE SUMMARY:
  "Three-layer architecture: presentation (React components with server/client
  split), business logic (service layer with Zod validation), data access
  (Prisma ORM). Authentication via NextAuth with role-based middleware.
  Background jobs via Inngest. Deployed on Vercel with edge middleware
  for geo-routing."
```

## Analysis Patterns

### Pattern: Dependency Audit

```
1. Read package.json dependencies and devDependencies
2. Categorize each dependency:
   - Framework: next, react, express
   - Data: prisma, drizzle, mongoose
   - Auth: next-auth, clerk, lucia
   - Validation: zod, yup, joi
   - Styling: tailwindcss, styled-components
   - Testing: vitest, jest, playwright
   - Utilities: lodash, date-fns, nanoid
3. Flag potential issues:
   - Duplicate functionality (e.g., both moment and date-fns)
   - Outdated major versions
   - Deprecated packages
   - Security advisories (check with npm audit)
```

### Pattern: Route Surface Analysis

```
For Next.js App Router:
  1. Glob: app/**/page.tsx — all pages
  2. Glob: app/**/layout.tsx — all layouts
  3. Glob: app/**/route.ts — all API routes
  4. Glob: app/**/loading.tsx — loading states
  5. Glob: app/**/error.tsx — error boundaries

  MAP:
    / → app/page.tsx (public)
    /dashboard → app/dashboard/page.tsx (authenticated)
    /api/users → app/api/users/route.ts (GET, POST)
    ...
```

### Pattern: Type System Overview

```
1. Glob: **/types/**/*.ts, **/*.d.ts, **/interfaces/**
2. Read each type file
3. Extract:
   - Domain entities (User, Order, Product)
   - API contracts (request/response types)
   - Component props (key component interfaces)
   - Shared enums and constants
4. Produce domain model summary
```

### Pattern: Convention Detection

```
ANALYZE: 10 representative files of each type

FILE NAMING:
  - Components: PascalCase.tsx vs kebab-case.tsx
  - Utils: camelCase.ts vs kebab-case.ts
  - Tests: *.test.ts vs *.spec.ts

CODE PATTERNS:
  - Error handling: try/catch vs Result type vs error boundaries
  - Async: async/await vs .then() vs callbacks
  - State: useState vs useReducer vs external store
  - Exports: named vs default vs barrel files

FORMATTING:
  - Indentation: tabs vs spaces (and how many)
  - Quotes: single vs double
  - Semicolons: yes vs no
  - Trailing commas: yes vs no

DERIVE: .editorconfig, .prettierrc, or eslintrc if they exist
```

## Output Templates

### Compact Repository Card

```
## [Project Name]
**Stack**: [Language] + [Framework] + [Database]
**Structure**: [Monorepo/Single] — [# files] files, [# dirs] directories
**Entry**: [main entry point]
**Key Modules**: [list top 5 modules with one-line descriptions]
**Patterns**: [3-5 key patterns/conventions]
**Dependencies**: [top 5 runtime deps]
```

### Architecture Document

```
## Architecture Overview

### System Type
[Web app / API / Library / CLI / Monorepo]

### Layer Diagram
[Text-based layer diagram]

### Module Map
[Module → responsibility → key files]

### Data Flow
[Request lifecycle from entry to response]

### External Integrations
[Third-party services and how they're used]

### Key Decisions
[Architectural decisions evident from the code]
```

## Anti-Patterns

1. **Including generated files**: Never include node_modules, dist, .next, __pycache__, or other generated directories. They waste tokens and provide no architectural insight.
2. **Flat file listing**: Listing every file without structure or annotation. Always organize hierarchically with purpose annotations.
3. **Ignoring configuration**: Configuration files are among the most information-dense files in a repository. They reveal constraints, targets, and conventions.
4. **Over-reading**: Reading every source file for a high-level overview. Use the layered approach — read more files only when deeper understanding is needed.
5. **Missing the "why"**: A structure map without explanation is just a directory listing. Always annotate with purpose and relationships.

## Integration Notes

- Feed output to **context-engineering** for token budget optimization.
- Use **docs-seeker** to find and incorporate project documentation.
- Hand off database schema findings to **data-modeling** for schema analysis.
- When the analysis reveals API endpoints, hand off to **api-designer** for API review.
