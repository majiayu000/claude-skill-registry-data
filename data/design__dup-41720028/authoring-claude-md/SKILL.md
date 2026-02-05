---
name: authoring-claude-md
description: Standards for writing CLAUDE.md and modular rules files (.claude/rules/) that maximize LLM execution efficiency. Use when creating or editing project instructions, defining conventions, or optimizing agent behavior for determinism and token efficiency. Focuses on eliminating ambiguity and producing consistent agent execution.
---

# CLAUDE.md and Rules Authoring

Write CLAUDE.md and rules files optimized for LLM parsing, not human aesthetics.

## Purpose and Context

CLAUDE.md provides persistent project context loaded at conversation start. Content becomes part of the system prompt.

Rules files (.claude/rules/) organize instructions into focused modules. Support unconditional rules (apply everywhere) and path-specific rules (apply to matching files only).

Determinism and token efficiency matter because context window is shared. Every token competes with conversation history and other context. Instructions that permit multiple interpretations produce inconsistent agent behavior.

For foundational instruction authoring principles (token economics, imperative language, formatting, anti-patterns), invoke the `authoring-prompts` skill first. This skill applies those principles specifically to CLAUDE.md and rules files.

## CLAUDE.md Patterns

### Required Sections

Include when applicable:

**Project Overview** (2-3 sentences): What the project is. Technology stack. Omit if name and structure make it obvious.

**Commands**: Exact commands with all flags. One per concern (test, build, deploy, lint).

**File Boundaries**: Explicit paths for safe-to-edit and never-touch locations.

**Conventions**: Project-specific patterns only. Omit generic programming advice.

**Workflows**: Step-by-step procedures for complex operations (deployment, releases).

### Omit Entirely

Generic programming advice Claude already knows: "Write clean code", "Use meaningful names", "Add comments where necessary."

Information inferable from codebase: Framework being used (visible in imports), file organization (visible in structure).

Decorative content: Welcome messages, motivational statements, background history.

Hypothetical scenarios: "If we ever migrate to Postgres..." Address when actual, not hypothetical.

### Determinism Checklist

Before finalizing CLAUDE.md:

- [ ] All commands include exact flags and arguments
- [ ] File paths are absolute or precisely scoped with globs
- [ ] Tool versions specified when behavior varies between versions
- [ ] No "consider", "try to", "when possible", "should", "could"
- [ ] Every instruction changes agent behavior (remove if Claude would do it anyway)
- [ ] Terminology consistent throughout (pick one term, use everywhere)

### CLAUDE.md vs Rules Decision

| Put in CLAUDE.md | Put in .claude/rules/ |
|------------------|------------------------|
| Project-wide commands (test, build, deploy) | Language-specific patterns (Ruby, TypeScript, Python) |
| Global file boundaries (vendor/, node_modules/) | Framework conventions (Rails, React, FastAPI) |
| Workflow procedures (release process) | Path-specific constraints (API validation, test structure) |
| Architecture decisions (monorepo structure) | Domain-specific rules (frontend styles, backend errors) |

## Rules Files Architecture

### File Organization

**Unconditional rules**: .claude/rules/security.md, .claude/rules/testing.md - apply to all files.

**Path-specific rules**: Use YAML frontmatter with `paths` field - apply only to matching files.

```yaml
---
paths: src/api/**/*.ts
---

# API Conventions

Return `IActionResult<T>` for all endpoints.
```

**Subdirectories**: Organize by domain - .claude/rules/frontend/, .claude/rules/backend/.

**Naming**: Descriptive, singular topic per file - `api-design.md`, `error-handling.md`, not `stuff.md`.

### Path Targeting

Use glob patterns for precise scope:

| Pattern | Matches |
|---------|---------|
| `**/*.ts` | All TypeScript files anywhere |
| `src/**/*` | All files under src/ |
| `*.md` | Markdown files in project root only |
| `src/components/**/*.tsx` | React components in src/components/ |
| `{src,lib}/**/*.ts` | TypeScript in src/ or lib/ |

Multiple patterns: `paths: src/**/*.{ts,tsx}, tests/**/*.test.ts`

Test patterns before committing. Verify they match intended files only.

### When to Use Path-Specific Rules

Use path-specific rules when conventions apply to subset of files:

- API endpoints require different validation than internal functions
- Frontend components follow different patterns than backend services
- Test files have different structure than source files
- Generated code has different rules than hand-written code

Use unconditional rules for project-wide requirements that apply everywhere.

### User-Level Rules

Create personal rules in ~/.claude/rules/ that apply to all projects.

User-level rules load before project rules. Project rules take precedence on conflict.

Use for personal preferences: editor configuration, commit message style, code review approach.

## Validation Protocol

### Determinism Validation

- [ ] Two agents reading this would execute identically
- [ ] No "consider", "should", "might", "try to", "when possible"
- [ ] Every command includes all flags and arguments
- [ ] All file paths precisely specified
- [ ] Tool versions specified when behavior differs
- [ ] No instruction permits multiple reasonable interpretations
- [ ] Terminology consistent (no mixing "endpoint", "route", "URL")

### Token Efficiency Validation

- [ ] No sentence exists that doesn't change agent behavior
- [ ] No generic advice Claude already knows
- [ ] Examples preferred over verbose explanations
- [ ] No decorative or motivational content
- [ ] No information easily inferable from codebase

### Structural Validation

- [ ] Critical constraints appear first in each section
- [ ] Headings clearly define scope boundaries
- [ ] One concern per section
- [ ] White space aids parsing
- [ ] Code blocks used only for exact values

### Rules-Specific Validation

- [ ] Path glob patterns tested and match intended files only
- [ ] Rules file location matches scope (project-wide vs path-specific)
- [ ] No duplication between CLAUDE.md and rules
- [ ] More specific rules documented when they override general rules

## Templates

### Minimal CLAUDE.md

```markdown
# [Project Name]

## Commands
- `[command with all flags]`: [description]
- `[command with all flags]`: [description]

## File Boundaries
- Edit: [explicit paths]
- Never touch: [explicit paths]

## Conventions
[Only project-specific patterns Claude cannot infer]
```

### Path-Specific Rule

```yaml
---
paths: [glob pattern]
---

# [Domain] Conventions

[Imperative instruction]
[Imperative instruction]
[Imperative instruction]
```

### Comprehensive CLAUDE.md

See templates/minimal-claude.md for annotated starting point.

For path-specific rule template, see templates/path-rule.md.

For before/after optimization examples, see references/examples.md.
