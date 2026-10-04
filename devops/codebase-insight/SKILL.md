---
name: codebase-insight
description: When the user wants to deeply understand a codebase, map its architecture, or build a persistent mental model for future sessions. Use when the user says "explain this codebase," "map the architecture," "codebase insight," "understand this repo," "what does this project do," "how does this work," "analyze the codebase," or when starting work on an unfamiliar project. Produces a persistent insight file that survives across sessions.
metadata:
  version: 1.0.0
  inspired_by: codebase analysis and persistent context patterns
---

# Codebase Insight — Deep Analysis with Persistent Memory

You are a codebase archaeologist and cartographer. You read the entire codebase, understand how every piece connects, and produce a map that makes the system navigable for any developer — including future AI sessions.

## Why This Exists

Every time you open a codebase, you start from zero. You re-read the same files, re-discover the same patterns, re-learn the same quirks. Codebase Insight fixes that by persisting the analysis to a file that future sessions can read immediately.

## The Insight Protocol

### Step 1: Full Codebase Scan

Read everything systematically. Don't sample — survey.

```
SCAN ORDER:
═══════════
1. Root files — README, package.json/manifest, config files
   → Project name, purpose, tech stack, dependencies

2. Directory structure — full tree, note patterns
   → Architecture style, organization principle

3. Entry points — main/index files, app bootstrap
   → How the application starts, what it initializes

4. Route/API layer — endpoints, handlers
   → What the system exposes, request/response shapes

5. Data layer — schemas, models, migrations, ORM config
   → What's stored, how it relates, what constraints exist

6. Business logic — services, utils, core modules
   → Where the real work happens, key algorithms

7. Infrastructure — CI/CD, Docker, deployment configs
   → How it's built, tested, deployed

8. Tests — test files, coverage config
   → What's tested, what's not, test patterns used

9. Git history — last 30 commits, active branches
   → Recent momentum, who's working on what
```

### Step 2: Pattern Recognition

Identify the recurring patterns in the codebase:

```
PATTERN ANALYSIS:
═════════════════
Architecture Pattern: [Monolith / Microservices / Modular Monolith / Serverless / etc.]
Organization: [Feature-based / Layer-based / Domain-driven / Mixed]

Code Patterns:
- Error handling: [how errors flow — throws/returns/callbacks]
- Data fetching: [REST/GraphQL/tRPC, client-side/server-side]
- State management: [what holds state, how it flows]
- Authentication: [strategy, where checks happen]
- Validation: [where and how input is validated]
- Logging: [what's logged, what framework]

Naming Conventions:
- Files: [camelCase / kebab-case / PascalCase / snake_case]
- Functions: [pattern]
- Types: [prefix/suffix conventions]
- Database: [singular/plural, naming style]

Testing Patterns:
- Framework: [Jest/Vitest/Playwright/etc.]
- Style: [unit-heavy / integration-heavy / E2E-heavy]
- Mocking: [how external deps are mocked]
- Coverage: [approximate coverage level]
```

### Step 3: Dependency Map

Map how components depend on each other:

```
DEPENDENCY MAP:
═══════════════
[Component A]
  ├── depends on: [Component B, Component C]
  ├── depended on by: [Component D]
  └── external deps: [API X, Database Y]

[Component B]
  ├── depends on: [nothing]
  ├── depended on by: [Component A, Component E]
  └── external deps: [none]

Circular dependencies: [list any]
Highly coupled components: [list any with 5+ dependencies]
Isolated components: [list any with 0 dependents]
```

### Step 4: Critical Path Analysis

Identify the most important flows:

```
CRITICAL PATHS:
═══════════════
1. [Primary user flow — e.g., "User signs up"]
   Entry: [file:line] → [file:line] → [file:line] → Response
   Touches: [list of modules]
   Risk: [what could break this flow]

2. [Secondary flow — e.g., "User creates resource"]
   ...

3. [Background flow — e.g., "Cron job syncs data"]
   ...
```

### Step 5: Quirks & Gotchas

Document the non-obvious things that waste time:

```
QUIRKS & GOTCHAS:
═════════════════
- [Quirk]: [explanation + where it manifests]
  Example: "The auth middleware silently fails on expired tokens instead of
  returning 401 — it just sets req.user to null. Check auth/middleware.ts:45"

- [Technical debt]: [what it is + why it exists if apparent]
  Example: "Two separate user tables (users and legacy_users) because
  the migration from the old system was never completed"

- [Hidden dependency]: [something not obvious from the code]
  Example: "The PDF generator requires LibreOffice installed on the host —
  not documented anywhere, discovered from Dockerfile"
```

### Step 6: Health Assessment

Score the codebase health:

```
CODEBASE HEALTH:
════════════════
| Dimension | Score (1-10) | Notes |
|-----------|-------------|-------|
| Code Organization | [N] | [brief note] |
| Test Coverage | [N] | [brief note] |
| Documentation | [N] | [brief note] |
| Dependency Health | [N] | [brief note] |
| Error Handling | [N] | [brief note] |
| Security Posture | [N] | [brief note] |
| Build/Deploy | [N] | [brief note] |

Overall: [N]/70

Top 3 improvement areas:
1. [Area] — [specific action]
2. [Area] — [specific action]
3. [Area] — [specific action]
```

### Step 7: Persist the Insight

**This is the critical step.** Save the full analysis to a persistent file:

```
Output file: .codebase-insight.md (in project root)
```

The file should contain ALL of the above in a structured markdown document with a generation timestamp and a table of contents.

```markdown
# Codebase Insight — [Project Name]
> Generated: [YYYY-MM-DD HH:MM]
> Source: [commit hash at time of generation]

## Table of Contents
- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Directory Map](#directory-map)
- [Patterns](#patterns)
- [Dependency Map](#dependency-map)
- [Critical Paths](#critical-paths)
- [Data Model](#data-model)
- [API Surface](#api-surface)
- [Quirks & Gotchas](#quirks--gotchas)
- [Health Assessment](#health-assessment)

[... full content ...]
```

### Step 8: Announce the File

After saving:

```
Codebase insight saved to .codebase-insight.md
[N] components mapped, [N] patterns identified, [N] critical paths traced.
Health score: [N]/70

This file will be available to future sessions for instant context loading.
To refresh: run /codebase-insight again.
```

## Insight Modes

### Quick Insight
Scan Steps 1-2 only. Produces a high-level overview without deep dependency or path analysis. Saves a shorter `.codebase-insight.md`.

### Standard Insight
All 8 steps. The default.

### Deep Insight
All 8 steps plus:
- Dispatch subagents to analyze different subsystems in parallel
- Include code quality metrics (function length distribution, cyclomatic complexity patterns)
- Map all environment variables and their usage
- Trace all external API integrations
- Analyze git history for hotspot files (most frequently changed)

### Delta Insight
When `.codebase-insight.md` already exists:
- Compare current codebase state to the saved insight
- Identify what's changed (new files, removed files, modified patterns)
- Update only the changed sections
- Append a changelog entry to the insight file

```markdown
## Insight Changelog
| Date | Changes |
|------|---------|
| [YYYY-MM-DD] | [what changed since last insight] |
```

## Multi-Project Support

In monorepos or multi-project directories:
- Ask which project to analyze (or do all)
- Save per-project: `.codebase-insight-[project-name].md`
- Include cross-project dependency map in each file

## Rules

- **Read before writing.** Scan the full codebase before producing any analysis.
- **Facts only.** Every claim must reference a specific file. No speculation.
- **Always persist.** The insight file is the product. Without it, the analysis evaporates.
- **Include the commit hash.** So future sessions know if the insight is stale.
- **Timestamp everything.** The insight file must show when it was generated.
- **Acknowledge gaps.** If parts of the codebase are unclear, say so. Don't fill gaps with guesses.
- **Keep it scannable.** Use tables and structured formats. Nobody reads walls of prose about architecture.
