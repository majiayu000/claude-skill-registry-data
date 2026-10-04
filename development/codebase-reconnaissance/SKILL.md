---
name: codebase-reconnaissance
description: >
  Systematically understand an unfamiliar or partially-known codebase
  before making changes. Produces a Codebase Profile that informs all
  subsequent skills. Use before any modification to a codebase you
  haven't reconnoitered in the current session.
version: 1.0.0
permissions:
  - fs.read
  - shell.exec
triggers:
  - context: "unfamiliar codebase"
  - context: "first time working in a project"
  - context: "task-decomposition-engine requests reconnaissance"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
  gemini:
    enforcement_style: "structured-checklist"
  gpt:
    enforcement_style: "directive-imperative"
author: codehands-core
signed: true
tier: 0
---

## Overview

You can't modify what you don't understand. Codebase reconnaissance is the systematic process of understanding a project's structure, patterns, tools, and conventions BEFORE proposing or implementing changes. The output is a Codebase Profile that informs all downstream skills.

## When to Use

- When `codehands:task-decomposition-engine` flags uncertainty
- When working in a project for the first time in a session
- When the project has changed significantly since last session
- NOT when you've already profiled this codebase in the current session

## Process

### 1. Project Identity

```bash
# What is this project?
cat README.md | head -50        # Project description
cat package.json | head -20     # Or Cargo.toml, go.mod, pyproject.toml
ls -la                          # Root structure
```

Record: Project name, purpose, primary language, framework.

### 2. Architecture Scan

```bash
# Directory structure (depth 2)
find . -type f -name "*.ts" -o -name "*.py" -o -name "*.go" -o -name "*.rs" | \
  head -50 | sed 's|/[^/]*$||' | sort -u

# Entry points
ls src/index.* src/main.* src/app.* app/layout.* 2>/dev/null
```

Record: Module organization pattern (feature-based, layer-based, hybrid). Key entry points.

### 3. Test Infrastructure

```bash
# Test framework detection
ls jest.config* vitest.config* pytest.ini pyproject.toml .mocharc* 2>/dev/null

# Test files
find . -name "*.test.*" -o -name "*.spec.*" -o -name "*_test.*" | head -20

# Test commands
grep -A5 '"test"' package.json 2>/dev/null   # npm
grep -A5 '\[tool.pytest' pyproject.toml 2>/dev/null  # pytest
```

Record: Test framework, test file location pattern, test command, approximate test count.

### 4. Build & Run

```bash
# Build commands
grep -E '"(build|dev|start|lint)"' package.json 2>/dev/null
cat Makefile 2>/dev/null | grep -E "^[a-z]+:" | head -10

# CI pipeline
ls .github/workflows/*.yml .gitlab-ci.yml Jenkinsfile 2>/dev/null
```

Record: Build command, dev command, lint command, CI presence.

### 5. Coding Patterns

Read 2-3 representative source files and identify:
- **Naming:** camelCase? snake_case? PascalCase for what?
- **Imports:** Grouped? Sorted? Relative vs absolute?
- **Error handling:** try/catch? Result types? Error callbacks? Custom error classes?
- **Async style:** async/await? Promises? Callbacks?
- **State management:** (if frontend) Redux? Zustand? Context? Signals?
- **Logging:** console.log? Structured logger? Log levels?

### 6. Dependencies & Security

```bash
# Dependency audit
npm audit 2>/dev/null || pip audit 2>/dev/null || cargo audit 2>/dev/null

# Dependency count
cat package-lock.json 2>/dev/null | grep -c '"resolved"' || echo "N/A"
```

Record: Package manager, dependency count, known vulnerabilities.

### 7. Produce Codebase Profile

Save to `.codehands/session-state.md` (or append if it exists):

```markdown
## Codebase Profile — [Project Name]
Reconnoitered: YYYY-MM-DD HH:MM

### Identity
- Language: [e.g., TypeScript 5.3]
- Framework: [e.g., Next.js 14 App Router]
- Purpose: [one sentence]

### Architecture
- Pattern: [feature-based | layer-based | hybrid]
- Key dirs: [src/components, src/services, src/models]
- Entry: [src/app/layout.tsx]

### Testing
- Framework: [Jest + RTL]
- Pattern: [*.test.ts alongside source]
- Command: `npm test`
- Count: ~[N] test files

### Build & Run
- Build: `npm run build`
- Dev: `npm run dev`
- Lint: `npm run lint`
- CI: [GitHub Actions]

### Patterns
- Naming: [camelCase vars, PascalCase components]
- Errors: [Custom AppError, try/catch at boundaries]
- Async: [async/await throughout]
- Imports: [absolute paths via @/ alias]

### Dependencies
- Manager: [npm]
- Count: [~150 production]
- Vulnerabilities: [0 critical, 1 high, 3 moderate]

### Observations
- [Any notable patterns, tech debt, or concerns]
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I can tell what this project is from the file names" | File names tell structure, not patterns. You need to read code to understand error handling, naming conventions, and testing style. 5 minutes of reconnaissance saves 30 minutes of pattern-breaking code. |
| "I've worked with this framework before" | This project's conventions may differ from the framework defaults. Every team customizes. Read THIS project's code. |
| "Reconnaissance is slow, the user wants code" | Reconnaissance takes 2-5 minutes. Writing code that conflicts with existing patterns, then debugging it, takes 30+ minutes. |

## Red Flags

- Modifying code without knowing the project's test command
- Writing code in a different style than the existing codebase
- Not knowing the error handling pattern before writing error handling code
- No Codebase Profile produced

## Verification

- [ ] Project language, framework, and purpose identified
- [ ] Architecture pattern and key directories known
- [ ] Test framework, pattern, and command identified
- [ ] Build, dev, and lint commands known
- [ ] Coding patterns observed (naming, errors, async, imports)
- [ ] Codebase Profile saved to session state
- [ ] Dependencies audited for known vulnerabilities

## See Also

- `codehands:task-decomposition-engine` — Invokes this skill when uncertainty is high
- `codehands:source-driven-development` — Uses the profile during implementation
- `codehands:security-and-hardening` — Uses dependency audit results
