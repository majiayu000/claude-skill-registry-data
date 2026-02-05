---
name: write-rules
description: Create Claude Code rule files for .claude/rules/. Writes conventions and shared guidelines that auto-inject into context. Use for path-specific coding conventions or shared project guidelines. NOT for constitution/laws (use <law> in CLAUDE.md instead).
---

# Rule Creator

Create modular rule files for conventions and shared guidelines.

## Core Principles

1. **Rules = Conventions** - Shared guidelines, lower priority than `<law>`
2. **< 50 lines** - Auto-injected = token expensive
3. **Use `paths:`** - Scope rules to relevant files only
4. **No procedures** - How-to belongs in skills
5. **NOT for laws** - Constitution uses `<law>` in CLAUDE.md

## Rule Structure

```
.claude/rules/
├── code-style.md         # Style conventions (global)
├── api/
│   └── conventions.md    # paths: src/api/**
└── testing/
    └── guidelines.md     # paths: **/*.test.ts
```

## File Format

### Global Rule (no paths:)

```yaml
---
# No paths field = applies to ALL contexts
---

# Rule Title

- Constraint 1
- Constraint 2
```

### Path-Scoped Rule

```yaml
---
paths: src/api/**/*.ts
---

# API Rules

- All endpoints MUST validate input
- MUST use standard error format
```

## Glob Patterns

| Pattern | Matches |
|---------|---------|
| `**/*.ts` | All TypeScript files |
| `src/api/**` | All under src/api/ |
| `*.md` | Markdown in root only |
| `{src,lib}/**/*.ts` | Multiple directories |
| `**/*.{ts,tsx}` | Multiple extensions |

## Example: Code Style Convention

```markdown
# .claude/rules/code-style.md
---
# Global - no paths
---

# Code Style

- Prefer const over let
- Use descriptive variable names
- Keep functions under 50 lines
```

## Example: Path-Scoped Convention

```markdown
# .claude/rules/api/conventions.md
---
paths: src/api/**/*.ts
---

# API Conventions

- Use async/await, not callbacks
- Return consistent response shapes
- Log errors with context
```

## Validation Checklist

Before creating a rule:

- [ ] Is this a convention/guideline, NOT a law? (laws use `<law>` in CLAUDE.md)
- [ ] < 50 lines?
- [ ] Does it need `paths:` scoping?
- [ ] Not duplicating existing rules?
- [ ] Written in imperative form?

## References

- [paths-patterns.md](references/paths-patterns.md) - Advanced glob patterns
- [examples.md](references/examples.md) - Rule examples by domain
