---
name: opence-skill-creator
description: Learn how to create effective project skills following opence conventions.
metadata:
  short-description: Learn skill creation conventions.
---

<!-- OPENCE:START -->
# opence-skill-creator

Learn how to create effective project skills following opence conventions.

## When to Create a Skill

Create a skill during the **compound phase** when you identify:
- Repeatable workflows that can be encoded as instructions
- Recurring pitfalls or manual checks that need documentation
- Domain-specific knowledge that will be useful in future changes

Don't create a skill for one-off solutions or highly specific edge cases.

## Quick Start

Use the CLI to create skills (recommended):

```bash
# Create a new skill
opence skill add api-testing --description "Guidelines for testing API endpoints"

# List all skills
opence skill list

# Show skill details
opence skill show api-testing
```

The CLI automatically:
- Creates proper directory structure
- Generates correct frontmatter for each tool
- Validates naming conventions
- Creates references/ and scripts/ directories

## Skill Structure

```
.claude/skills/my-skill/
├── SKILL.md           # Concise entry point (< 200 lines)
├── references/        # Detailed documentation
│   └── *.md          # Extended guides, examples
└── scripts/          # Reusable code
    └── *.sh, *.py    # Helper scripts
```

**SKILL.md**: Keep concise. Include "When to use", key steps, and pointers to references/.

**references/**: Put detailed docs, long examples, API references here.

**scripts/**: Add reusable code that users can copy or execute.

## Naming Rules

- **Format**: kebab-case (e.g., `api-testing`, `deploy-prod`)
- **Reserved**: Don't use `opence-` prefix (reserved for native skills)
- **Unique**: Check with `opence skill list` to avoid duplicates

**Valid**: `api-testing`, `error-recovery`, `db-migration`
**Invalid**: `api testing` (spaces), `api_testing` (underscores), `opence-custom` (reserved)

## Next Steps

After creating a skill:
1. Edit SKILL.md to add instructions and examples
2. Add detailed docs to references/ if needed
3. Add helper scripts to scripts/ if applicable
4. Test the skill in actual usage
5. Commit to version control

See references/ for detailed guidance on:
- Directory structure and sizing
- Frontmatter formats for different tools
- Best practices and anti-patterns
<!-- OPENCE:END -->
