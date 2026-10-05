---
name: scout
description: Codebase reconnaissance and exploration -- map structure, find patterns, understand architecture
layer: hub
category: workflow
triggers:
  - "/scout"
  - "explore the codebase"
  - "what does this codebase look like"
  - "map the architecture"
  - "find where X is"
  - "how is this structured"
inputs:
  - target: What to explore -- a directory, feature, pattern, or question about the codebase
  - depth: How deep to go -- surface (structure only), standard (structure + key files), deep (full analysis)
outputs:
  - architectureMap: High-level structure and relationships between components
  - fileIndex: Relevant files categorized by purpose
  - patterns: Detected coding patterns, conventions, and architectural decisions
  - entryPoints: Key files to read for understanding a feature or subsystem
  - techStack: Detected technologies, frameworks, and tools
linksTo:
  - research
  - debug
  - code-review
linkedFrom:
  - plan
  - cook
  - team
  - ship
  - refactor
  - optimize
  - debug
preferredNextSkills:
  - plan
  - code-review
  - debug
fallbackSkills:
  - research
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: selective
sideEffects:
  - Reads many files (may be slow on very large codebases)
  - Produces architecture map in working memory
---

# Scout Skill

## Purpose

Perform systematic codebase reconnaissance to answer questions about structure, conventions, patterns, and architecture. Scout is the eyes and ears of the agent system -- it goes in first and reports back what it finds so that other skills (plan, debug, refactor, etc.) can make informed decisions.

Scout does not change code. It reads, maps, and reports.

## Workflow

### Mode 1: Full Reconnaissance (default for new codebases)

1. **Project structure scan**
   - List top-level directories and files
   - Identify project type (monorepo, single app, library, etc.)
   - Read configuration files: `package.json`, `tsconfig.json`, `Cargo.toml`, `pyproject.toml`, `.env.example`, etc.
   - Identify build tools, test frameworks, and CI/CD configuration

2. **Tech stack identification**
   - Framework(s) and version(s)
   - Language(s) and version(s)
   - Database(s) and ORM(s)
   - Key dependencies (UI libraries, state management, API clients)
   - Dev tooling (linters, formatters, type checkers)

3. **Architecture mapping**
   - Identify architectural pattern (MVC, hexagonal, feature-sliced, etc.)
   - Map directory structure to responsibilities
   - Identify shared/common code locations
   - Find the entry points (main files, route definitions, API handlers)
   - Map data flow: where does data come from, how does it transform, where does it go?

4. **Convention detection**
   - Naming conventions (files, functions, components, variables)
   - File organization patterns (co-location, separation by type, feature folders)
   - Import patterns (barrel files, direct imports, path aliases)
   - Error handling patterns
   - Testing conventions (test file location, naming, framework)

5. **Produce the reconnaissance report** using the template below.

### Mode 2: Targeted Exploration (for specific questions)

1. **Parse the question** -- What specifically is the user looking for?
   - A feature: "Where is authentication handled?"
   - A pattern: "How does this project handle errors?"
   - A file/function: "Where is the user model defined?"
   - A dependency: "How is Redis used?"

2. **Search strategy**
   - Start with file/directory name search (Glob)
   - Then content search for keywords (Grep)
   - Then read key files to trace relationships
   - Follow imports to map the dependency graph for the target

3. **Trace the feature/pattern**
   - Find the entry point
   - Follow the call chain
   - Identify all files involved
   - Map the data flow specific to this feature
   - Note any tests associated with this feature

4. **Report findings** with file paths, code snippets, and a summary of how the pieces connect.

### Mode 3: Diff Reconnaissance (for understanding changes)

1. **Analyze recent changes** -- What files have been modified recently?
2. **Map change impact** -- What other files/features might be affected?
3. **Identify test coverage gaps** -- Are the changed areas tested?
4. **Report risk areas** -- Where are changes most likely to cause breakage?

## Reconnaissance Report Template

```markdown
# Codebase Reconnaissance: [Project Name]

## Overview
- **Type**: [monorepo | app | library | ...]
- **Primary language**: [language + version]
- **Framework**: [framework + version]
- **Architecture**: [pattern name]

## Tech Stack
| Category | Technology | Version | Notes |
|----------|-----------|---------|-------|
| Runtime | Node.js | 20.x | |
| Framework | Next.js | 14.x | App Router |
| Database | PostgreSQL | 15 | Via Prisma |
| ... | ... | ... | ... |

## Directory Structure
```
project/
├── src/           # Application source
│   ├── app/       # Next.js app router pages
│   ├── components/# Shared UI components
│   ├── lib/       # Utilities and shared logic
│   └── ...
├── tests/         # Test files
└── ...
```

## Key Entry Points
| Purpose | File | Notes |
|---------|------|-------|
| App entry | `src/app/layout.tsx` | Root layout |
| API routes | `src/app/api/` | REST endpoints |
| Database | `prisma/schema.prisma` | Data model |

## Conventions
- **File naming**: kebab-case for files, PascalCase for components
- **Imports**: Path aliases via `@/` prefix
- **Testing**: Jest + React Testing Library, tests co-located with source
- **Error handling**: [pattern description]

## Architecture Notes
[Key observations about how the system is structured]

## Notable Patterns
- [pattern 1]: [where and how it is used]
- [pattern 2]: [where and how it is used]

## Potential Concerns
- [concern 1]
- [concern 2]
```

## Usage

### Full reconnaissance
```
/scout
```

### Targeted exploration
```
/scout Where is authentication handled?
/scout How does the payment flow work?
/scout Find all API endpoints
```

### Focused on a directory
```
/scout Explore src/lib/
```

### Change impact
```
/scout What would be affected if we change the User model?
```

## Examples

### Example: Feature exploration

**Input**: "/scout How does file upload work?"

**Process**:
1. Grep for "upload", "file", "multer", "formdata" across codebase
2. Find `src/app/api/upload/route.ts` -- the API endpoint
3. Find `src/components/FileUploader.tsx` -- the UI component
4. Find `src/lib/storage.ts` -- the storage abstraction
5. Trace: Component calls API endpoint, which uses storage lib to write to S3
6. Find `tests/upload.test.ts` -- tests exist

**Output**: Detailed map of the upload feature with file paths, data flow diagram, and notes about the S3 configuration.

### Example: Architecture mapping

**Input**: "/scout"

**Process**:
1. Read package.json -- Next.js 14, Prisma, Tailwind, etc.
2. Scan directory structure -- feature-sliced design with app router
3. Read tsconfig.json -- path aliases, strict mode
4. Check for .env.example -- environment variables needed
5. Read a few representative files to confirm patterns

**Output**: Full reconnaissance report with tech stack table, directory map, conventions, and notable findings.

## Guidelines

- **Read, do not write** -- Scout never modifies files. It is purely observational.
- **Start broad, go deep** -- Begin with structure, then drill into specifics as needed.
- **Be efficient with file reads** -- Use Glob and Grep before reading full files. Read selectively.
- **Report absolute paths** -- All file references must be absolute paths for downstream tools.
- **Flag what is unusual** -- Note deviations from common conventions. These are often the most important findings.
- **Do not assume** -- If a pattern is ambiguous, say so. Do not guess the intent behind code.
- **Respect scale** -- On very large codebases, focus on the relevant subsystem rather than trying to map everything.
- **Cache findings** -- Store reconnaissance results in working memory for other skills to consume without re-scanning.
