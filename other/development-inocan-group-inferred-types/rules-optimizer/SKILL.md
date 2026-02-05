---
name: rules-optimizer
description: Optimize and create Claude Rules (.claude/rules/*.md) following best practices.
---

# Rules Optimizer

Create and optimize `.claude/rules/*.md` files for effective AI guidance.

## Best Practices

### File Structure

```
.claude/rules/
├── typescript.md        # Language-specific
├── python.md
├── frontend/
│   ├── react.md         # Framework-specific
│   ├── tailwind.md
│   └── component-structure.md
└── backend/
    └── api.md
```

### Rule File Format

```markdown
---
paths: "**/*.{ts,tsx}" # Glob pattern (quoted)
---

# [Topic] Rules

## [Category]

[Rule statement]

\`\`\`typescript
// ❌ BAD
[anti-pattern]

// ✅ GOOD
[correct pattern]
\`\`\`
```

### Content Guidelines

1. **One topic per file** — keep focused
2. **150-200 lines ideal** — enough for examples, not overwhelming
3. **Include examples** — 1 BAD/GOOD pair per rule that needs clarity
4. **Skip obvious rules** — focus on what AI gets wrong
5. **No "why" explanations** — just the rule and example
6. **Use tables** for mappings (e.g., v3→v4 migrations)

### Path Patterns

| Pattern               | Matches         |
| --------------------- | --------------- |
| `**/*.ts`             | All TS files    |
| `**/*.{ts,tsx}`       | TS and TSX      |
| `src/**/*`            | All under src/  |
| `components/**/*.tsx` | Components only |

### What to Include

- ❌ Anti-patterns AI commonly generates
- ✅ Correct patterns with minimal example
- Migration mappings (old → new)
- Framework-specific conventions

### What to Exclude

- Self-evident rules (use semicolons, etc.)
- Long explanations of "why"
- Multiple examples for same rule
- Style preferences (let linters handle)

## Workflow

1. Read existing rule file
2. Identify: redundancy, missing examples, excessive length
3. Compress to essentials with 1 example per rule
4. Ensure paths pattern is appropriate
5. Output optimized version
