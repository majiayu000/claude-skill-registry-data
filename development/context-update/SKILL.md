---
name: context-update
description: Scan repository and update context file
---

# Context Update

You are updating the repository context file. This file serves as a knowledge base about the codebase for AI agents to reference.

## Your Task

Scan the current repository from the working directory downward and create/update `.opencode/context/repo-structure.md` with current repository information.

## Step 1: Read Existing Context (If Exists)

First, check if `.opencode/context/repo-structure.md` already exists. If it does, read it to understand the previous state. This will help you:
- Detect what changed
- Preserve the structure
- Show a meaningful diff to the user

## Step 2: Scan Repository

Scan the repository comprehensively. Use deep scanning (up to 5 levels) to discover:

### A. Tech Stack
- Read `package.json`, `requirements.txt`, `Gemfile`, `go.mod`, etc.
- Identify framework, language version, build tools
- List key dependencies with brief purpose

### B. Directory Structure
- Map out the high-level folder organization
- Identify the purpose of each major directory
- Note common patterns (src/, lib/, components/, etc.)

### C. Reusable Components
- Scan for React/Vue/Svelte components (`.tsx`, `.jsx`, `.vue`, `.svelte`)
- Common locations: `src/components/`, `components/`, `app/components/`
- For each component, extract:
  - Name and file path
  - Description from JSDoc comments, or first comment in file, or inferred from filename
  - Example: "WeatherCard (src/components/WeatherCard.tsx) - Displays weather data with icon and temperature"

### D. Custom Hooks (React/Vue)
- Look for files matching `use*.ts`, `use*.js` patterns
- Common locations: `src/hooks/`, `hooks/`, `composables/`
- Extract name, path, and purpose

### E. API Services
- Look for API integration code
- Common locations: `src/services/`, `src/api/`, `lib/api/`, `api/`
- Identify what external services/APIs are being called
- Example: "weatherApi (src/services/weatherApi.ts) - Open-Meteo API integration"

### F. Utilities
- Common locations: `src/utils/`, `utils/`, `lib/`
- List utility modules and their purpose

### G. Type Definitions
- TypeScript: `src/types/`, `types/`, `*.d.ts` files
- Document key types/interfaces

### H. Conventions & Patterns
Detect patterns by analyzing code:
- Export style (named vs default)
- Naming conventions (camelCase, PascalCase, kebab-case)
- Import patterns (relative vs absolute)
- File organization (co-location, separation)
- Error handling approaches

### I. Testing Patterns (If Tests Exist)
- Test framework (Jest, Vitest, Pytest, etc.)
- Test file patterns (`*.test.js`, `*.spec.ts`, `_test.go`)
- Test location (co-located, separate `/tests` directory)

### J. Environment Variables
- Read `.env.example`, `.env.template`, or scan code for `process.env`, `os.Getenv`, etc.
- List required environment variables and their purpose
- DO NOT read actual `.env` files (may contain secrets)

### K. Build & Scripts
- From `package.json`, `Makefile`, etc.
- Document key commands: dev server, build, test, deploy

## Step 3: Smart Discovery (Don't Hardcode Paths)

Don't assume standard paths. Instead:

1. **Look for package manifests first** to understand the tech stack
2. **Scan all directories** to find actual structure (not just `src/`)
3. **Follow import statements** to discover what's actually used
4. **Use glob patterns** to find files:
   - Components: `**/*.{tsx,jsx,vue,svelte}`
   - Hooks: `**/use*.{ts,js,tsx,jsx}`
   - Services: `**/services/**/*.{ts,js}`, `**/api/**/*.{ts,js}`
   - Types: `**/types/**/*.{ts,d.ts}`, `**/*.d.ts`

## Step 4: Generate Context File

Create `.opencode/context/repo-structure.md` with this structure:

```markdown
# Repository Context

Last updated: [current timestamp]

## Tech Stack
- **Framework**: [name and version]
- **Language**: [language and version]
- **Build Tool**: [tool and version]
- **Styling**: [CSS framework if any]
- **Package Manager**: [npm, yarn, pnpm, etc.]
- **Other Key Dependencies**:
  - [dependency]: [brief purpose]

## Directory Structure
\`\`\`
[tree-like structure with inline comments explaining each directory]
\`\`\`

## Reusable Components

### [ComponentName] ([path])
[Description from JSDoc, comments, or inferred]

[Repeat for each component]

## Custom Hooks

### [hookName] ([path])
[Purpose]

[Repeat for each hook]

## API Services

### [serviceName] ([path])
[What API/backend it connects to]

[Repeat for each service]

## Utilities

### [utilName] ([path])
[Purpose]

[Repeat for each utility]

## Type Definitions

### [TypeName] ([path])
[What it defines]

[Repeat for key types]

## Conventions & Patterns

- **Exports**: [pattern observed]
- **Naming**: [conventions used]
- **File Organization**: [pattern]
- **Error Handling**: [approach]
- **[Other patterns]**: [description]

## Testing

- **Framework**: [test framework]
- **Location**: [where tests live]
- **Patterns**: [file naming, structure]

## Environment Variables

- `[VAR_NAME]` - [purpose and default if any]

[Repeat for each variable]

## Build & Scripts

- `[command]` - [what it does]

[Repeat for common commands]
```

## Step 5: Detect Changes

If an existing context file was read in Step 1, compare old vs new and identify:
- **Added**: New components, hooks, services, dependencies, etc.
- **Removed**: Items that no longer exist
- **Modified**: Changes to existing sections (e.g., dependency version updates)

## Step 6: Write File and Report

Write the updated context file to `.opencode/context/repo-structure.md`.

Then, report to the user in this format:

```
Updated .opencode/context/repo-structure.md

Changes:
+ Added component: WeatherSummary (src/components/WeatherSummary.tsx)
+ Added component: LoadingSpinner (src/components/LoadingSpinner.tsx)
+ Added hook: useSummary (src/hooks/useSummary.ts)
+ Added service: ollamaApi (src/services/ollamaApi.ts)
~ Updated Tech Stack: added @types/node v24.10.1
~ Updated Directory Structure: added src/hooks/ directory
- Removed component: OldComponent (no longer exists)

Summary: Detected 3 new components, 1 new hook, 1 new service since last scan.

Context file is now synced with current repository state.
```

If this is the first time (no existing file):

```
Created .opencode/context/repo-structure.md

Summary:
- Scanned from: [current directory]
- Found: X components, Y hooks, Z services
- Tech stack: [Framework]

Context file created. AI agents can now reference this for repository knowledge.
```

## Important Notes

- **Scope**: Scan from current working directory downward
- **Depth limit**: Maximum 5 directory levels to prevent runaway scanning
- **Performance**: For very large repos, focus on most important items first
- **Accuracy**: Infer descriptions when not explicitly documented (better than nothing)
- **Security**: Never read actual `.env` files, only `.env.example` or template files
- **File size**: Include everything found, organized well - don't artificially limit
- **Idempotent**: Running multiple times should produce consistent results

## Edge Cases

1. **No package.json**: Still scan - might be Go, Python, Rust, etc.
2. **Multiple frameworks**: Document all (e.g., monorepo with React + Node backend)
3. **Nested node_modules**: Ignore them when scanning
4. **Build artifacts**: Ignore `dist/`, `build/`, `.next/`, etc.
5. **Hidden files**: Scan `.env.example` but respect `.gitignore` patterns

## Example Workflow

```bash
# User runs from repo root
/project-root$ /context-update

# Agent scans entire repo
# Creates /project-root/.opencode/context/repo-structure.md

# Later, user runs from subdirectory
/project-root/packages/frontend$ /context-update

# Agent scans only frontend package
# Creates /project-root/packages/frontend/.opencode/context/repo-structure.md
```

Each location has its own context file, scoped to that directory tree.
