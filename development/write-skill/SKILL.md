---
name: write-skill
description: Create effective Claude Code SKILL.md files following Anthropic's official patterns. Use when writing new skills, improving existing skills, or learning skill best practices.
---

# Skill Creator

Create skills that extend Claude's capabilities with specialized knowledge and workflows.

## Core Principles

1. **Concise is key** - Context window is shared; only add what Claude doesn't know
2. **< 200 lines** - Split to `references/` if approaching limit
3. **Description triggers** - Include "Use when..." in YAML description, not body
4. **Scripts for precision** - Create `.py` scripts for tasks requiring exact format or validation; for templates, prefer Python scripts over raw markdown to ensure stable formatting

## Skill Structure

```
.claude/
└── skills/
    └── skill-name/
        ├── SKILL.md           # Required: instructions (<200 lines)
        ├── scripts/           # Optional: executable code
        ├── references/        # Optional: docs loaded on-demand
        └── assets/            # Optional: templates, images
```

## Creation Process

### 1. Initialize

Run the init script to create proper structure:

```bash
python3 scripts/init_skill.py <skill-name>
```

Options:
- `--path`, `-p`: Output directory (default: `.claude/skills`)

### 2. Write SKILL.md

**Frontmatter** (required):
```yaml
---
name: my-skill
description: [What it does]. Use when [specific triggers].
---
```

**Body**: Instructions only. Keep lean—move details to `references/`.

### 3. Validate

```bash
python3 scripts/validate_skill.py <path/to/skill>
```

### 4. Test

Restart Claude Code, trigger naturally (don't mention skill name).

## Degrees of Freedom

| Level | When | Format |
|-------|------|--------|
| High | Multiple valid approaches | Text guidance |
| Medium | Preferred pattern exists | Pseudocode |
| Low | Fragile/critical operations | Specific scripts |

## Progressive Disclosure

Split content when SKILL.md grows:

```markdown
## Quick start
[Essential usage]

## Advanced
- **Forms**: See [forms.md](references/forms.md)
- **API**: See [api.md](references/api.md)
```

Claude loads references only when needed.

## What NOT to Include

- README.md, CHANGELOG.md, INSTALLATION_GUIDE.md
- Explanations Claude already knows
- "When to use" sections in body (put in description)
- **Shared conventions** - if multiple skills use the same convention, extract to `.claude/rules/`

## Relationship with Rules

**Rules = conventions shared across skills.**

If you find yourself repeating the same guideline in multiple skills:
1. Extract to `.claude/rules/` using `write-rules` skill
2. Skills automatically inherit rules (auto-injected)
3. Keep skill-specific details in the skill

## References

- [spec.md](references/spec.md) - YAML frontmatter specification
- [patterns.md](references/patterns.md) - Common skill patterns
- [examples.md](references/examples.md) - Before/after examples
