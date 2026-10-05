---
name: researching-codebase
description: Investigates codebase before planning. Use before any non-trivial implementation task to gather context in isolation.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob
  argument-hint: [topic-or-question]
  context: fork
  agent: Explore
  stability: stable
  content-hash: sha256:6aad2323da43ca6fddaf55f24d7a6fc781a15595ff623339477b75d7376c11e6
  last-verified-cc-version: 1.0.34
---

# Codebase Research (ACE-FCA)

**Query**: $ARGUMENTS

Gathers codebase context **in isolation** before planning. Prevents search
artifacts from polluting main context.

## Core Principles

1. **Documentation-only** - Describe what exists, where, and how it works
2. **No evaluations** - Never suggest improvements or critique implementation
3. **Evidence-based** - Provide file paths, line numbers, and code references
4. **Isolation** - Research runs in fork context; return only distilled findings

## When to Use

- Before planning non-trivial implementations
- When unfamiliar with relevant codebase areas
- Before architectural decisions

## Workflow

1. **Read mentioned files first** - If specific files mentioned, read completely before exploring
2. **Decompose the question** - Break query into researchable components
3. **Explore codebase** - Investigate architecture, patterns, constraints
4. **Identify scope** - Determine relevant areas based on findings
5. **Distill** - Return structured summary using output format below

## Output Format

Follow ACE-FCA quality equation: **Correct + Complete + Minimal noise**

```markdown
---
research_query: "<original question>"
timestamp: "<ISO 8601>"
files_examined: <count>
---

## Key Files

| File | Purpose | Key Lines |
|------|---------|-----------|
| `path/to/file.ext` | Brief purpose | L42-58 |

## Patterns

- **Pattern name**: Description with file reference (`path:line`)

## Constraints

- Constraint with evidence (`path:line`)

```

## Evidence Requirements

Every claim must include:

- **File path**: Exact location (`src/auth/login.ts`)
- **Line numbers**: Specific lines (`L42-58` or `L127`)
- **Code reference**: Function/class name when relevant

**Bad**: "Authentication uses JWT tokens"
**Good**: "Authentication uses JWT tokens (`src/auth/jwt.ts:L23-45`, `verifyToken` function)"

## References

See `references/context-management.md` and `references/core-principles.md`.
