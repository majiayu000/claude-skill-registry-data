---
description: Onboard to a new codebase - architecture scan, key decisions, first tasks
argument-hint: "[project directory or repo URL]"
allowed-tools:
  - Read
  - Agent
  - Glob
  - Grep
  - Bash(git log:*, find:*, wc:*, ls:*)
---

New project onboarding. Scans a codebase and generates a comprehensive orientation: architecture, key decisions, dependency map, environment setup, and first tasks.

## Steps

### Step 1: Locate the project

If the user specified a directory, use that. Otherwise, use the current working directory.

Verify it's a real project (has package.json, Cargo.toml, pyproject.toml, go.mod, or equivalent).

### Step 2: Structural scan (parallel)

**Scan 1 — Project identity:**
- Read README, CONTRIBUTING, CHANGELOG if they exist
- Read package.json / Cargo.toml / pyproject.toml for metadata
- Identify: language, framework, build tool, test framework
- Count: total files, lines of code, number of dependencies

**Scan 2 — Architecture:**
- Map the directory structure (top 3 levels)
- Identify architectural pattern (MVC, hexagonal, monolith, microservices, serverless)
- Find entry points (main files, route definitions, handlers)
- Locate config files (env, yaml, json configs)

**Scan 3 — Key files:**
- Find the 10 most-changed files (`git log --format='' --name-only | sort | uniq -c | sort -rn | head -20`)
- Find the largest files (likely important or problematic)
- Locate test directories and test patterns

### Step 3: Dependency analysis

- List direct dependencies with versions
- Flag any outdated or deprecated packages (check for major version gaps)
- Identify critical dependencies (the ones the project can't function without)
- Note any unusual or niche dependencies worth understanding

### Step 4: Code patterns

Read 3-5 representative files to identify:
- Naming conventions (camelCase, snake_case, etc.)
- Error handling patterns
- Logging approach
- State management (if frontend)
- Database access patterns (if backend)
- Authentication / authorisation approach

### Step 5: Git archaeology

```bash
git log --oneline -20
```

From recent history:
- What's being actively worked on?
- Who are the main contributors?
- What's the commit style? (conventional commits, free-form, etc.)
- Any long-running branches?

### Step 6: Generate the onboarding guide

Save to `ONBOARDING.md` (or output directly):

```markdown
# Onboarding Guide — [Project Name]

## Quick Facts
- **Language:** [lang] / **Framework:** [framework]
- **Architecture:** [pattern]
- **Lines of code:** [count]
- **Dependencies:** [count direct]
- **Test framework:** [framework]
- **Build tool:** [tool]

## Project Structure
```
[directory tree, top 3 levels, annotated]
```

## Key Files to Read First
1. **[file]** — [why it matters]
2. **[file]** — [why it matters]
3. **[file]** — [why it matters]
4. **[file]** — [why it matters]
5. **[file]** — [why it matters]

## Architecture Overview
[2-3 paragraphs explaining how the system works]

## Code Patterns
- **Naming:** [convention]
- **Error handling:** [pattern]
- **State:** [approach]
- **Auth:** [approach]

## Environment Setup
1. [Step to get running locally]
2. [Step]
3. [Step]

## First Tasks to Tackle
These are good starter tasks to build familiarity:
1. [Specific, small task with file reference]
2. [Specific, small task with file reference]
3. [Specific, small task with file reference]

## Watch Out For
- [Gotcha or non-obvious pattern]
- [Gotcha or non-obvious pattern]

---
Generated: [date]
```

Output a brief summary and highlight the most important thing to understand about this codebase.
