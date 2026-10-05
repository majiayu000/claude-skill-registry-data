---
name: cursor-rules
description: Create and manage Cursor IDE rules for AI-assisted coding. Use when asked to create .cursorrules, .mdc rule files, or configure Cursor AI behavior for a project.
---

# Cursor Rules

## Repository Pattern

Store rules in `rules/` directory, symlink to activate:

```
rules/
├── python.mdc
├── typescript.mdc
└── project-standards.mdc

# Activate in target project:
ln -s /path/to/rules/python.mdc .cursor/rules/python.mdc
```

## MDC File Structure

```yaml
---
description: When to apply this rule (for Agent Requested)
globs: ["*.py", "src/**/*.js"]  # For Auto Attached rules
alwaysApply: false
---

# Rule Content

Your instructions here...
```

## Rule Types

| Type | Trigger | Use Case |
|------|---------|----------|
| Always | `alwaysApply: true` | Core project standards |
| Auto Attached | `globs: [...]` | File-type specific rules |
| Agent Requested | `description` only | Situational guidance |
| Manual | No frontmatter | Explicitly referenced |

## Workflow

1. Create rule in `rules/<name>.mdc`
2. Symlink to project's `.cursor/rules/` to activate
3. Remove symlink to deactivate (rule remains in repo)

Keep rules concise—AI is smart, add only project-specific context.
