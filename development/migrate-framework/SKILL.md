---
name: migrate-framework
description: "Assists with migrating between frameworks or major versions — Express to Fastify, CRA to Vite, Vue 2 to Vue 3, class components to hooks, etc. Creates a migration plan, identifies breaking changes, and provides file-by-file migration order."
argument-hint: "[source framework] to [target framework]"
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Framework Migration Assistant

## Detect Current Setup
!`ls package.json requirements.txt go.mod Cargo.toml *.csproj Gemfile composer.json 2>/dev/null`
!`cat package.json 2>/dev/null | head -30`
!`find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.go" -o -name "*.rs" \) -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | head -30`

---

## Migration Process

### Step 1: Audit Current Usage
1. Identify all imports/requires of the source framework
2. Map which features and APIs are used
3. Catalog plugins, middleware, and extensions in use
4. Count affected files and estimate scope

### Step 2: Map Source to Target
For each source feature in use, determine:
| Source API | Target Equivalent | Breaking Change? | Notes |
|-----------|-------------------|-----------------|-------|
| ... | ... | Yes/No | ... |

Flag features with NO direct equivalent — these need custom solutions.

### Step 3: Migration Plan
Create an ordered migration plan:
1. **Setup**: Install target framework alongside source (coexistence period)
2. **Configuration**: Migrate config files (build config, env, plugins)
3. **Core**: Migrate entry points and routing
4. **Components/Modules**: Migrate individual files (ordered by dependency — leaves first)
5. **Tests**: Update test setup and migrate test files
6. **Cleanup**: Remove source framework dependencies

### Step 4: File-by-File Migration Order
List every file that needs changes, ordered by:
1. No dependencies on other migrated files (migrate first)
2. Shared utilities and types
3. Core modules
4. Feature modules
5. Entry points (migrate last)

### Step 5: Execute Migration
For each file:
1. Show the current code
2. Show the migrated code
3. Explain what changed and why
4. Run tests after each file to catch regressions

## Rules
- Migrate incrementally — one file or module at a time
- Keep both frameworks running during migration if possible
- Run tests after every change
- Don't change functionality during migration — only change the framework layer
- Flag any features that cannot be migrated 1:1
