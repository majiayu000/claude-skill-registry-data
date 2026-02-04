---
name: skill-architecture
description: Comprehensive guide for creating effective Claude Code skills with security best practices, CLI-specific features, and structural patterns. Use when creating skills, needing security guidance, understanding skill architecture, or learning best practices.
---

# Skill Architecture

Comprehensive guide for creating effective Claude Code skills following Anthropic's official standards with emphasis on security, CLI-specific features, and progressive disclosure architecture.

> ⚠️ **Scope**: Claude Code CLI Agent Skills (`~/.claude/skills/`), not Claude.ai API skills

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities with specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains—transforming Claude from general-purpose to specialized agent with procedural knowledge no model fully possesses.

### What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, assets for complex/repetitive tasks

______________________________________________________________________

## Skill Creation Process (6 Steps)

### Step 1: Understanding the Skill with Concrete Examples

Clearly understand concrete examples of how the skill will be used. Ask users:
- "What functionality should this skill support?"
- "Can you give examples of how it would be used?"
- "What would trigger this skill?"

Skip only when usage patterns are already clearly understood.

### Step 2: Planning Reusable Contents

Analyze each example to identify what resources would be helpful:

**Example 1 - PDF Editor**:
- Rotating PDFs requires rewriting code each time
- → Create `scripts/rotate_pdf.py`

**Example 2 - Frontend Builder**:
- Webapps need same HTML/React boilerplate
- → Create `assets/hello-world/` template

**Example 3 - BigQuery**:
- Queries require rediscovering table schemas
- → Create `references/schema.md`

### Step 3: Initialize the Skill

Run the marketplace init script (don't copy, use from marketplace):

```bash
/Users/terryli/.claude/plugins/marketplaces/anthropic-agent-skills/skill-creator/scripts/init_skill.py <skill-name> --path ~/.claude/skills/
```

Creates: skill directory + SKILL.md template + example resource directories

### Step 4: Edit the Skill

**Writing Style**: Imperative/infinitive form (verb-first), not second person
- ✅ "To accomplish X, do Y"
- ❌ "You should do X"

**SKILL.md should answer**:
1. What is the purpose? (few sentences)
2. When should it be used?
3. How should Claude use bundled resources?

**Start with resources** (`scripts/`, `references/`, `assets/`), then update SKILL.md

### Step 5: Validate the Skill

**For local development** (validation only, no zip creation):

```bash
/Users/terryli/.claude/plugins/marketplaces/anthropic-agent-skills/skill-creator/scripts/quick_validate.py <path/to/skill-folder>
```

**For distribution** (validates AND creates zip):

```bash
/Users/terryli/.claude/plugins/marketplaces/anthropic-agent-skills/skill-creator/scripts/package_skill.py <path/to/skill-folder>
```

Validates: YAML frontmatter, naming, description, file organization

**Note**: Use `quick_validate.py` for most workflows. Only use `package_skill.py` when actually distributing the skill to others.

### Step 6: Iterate

1. Use skill on real tasks
2. Notice struggles/inefficiencies
3. Update SKILL.md or resources
4. Test again

______________________________________________________________________

## Skill Anatomy

```
skill-name/
├── SKILL.md           # Required: YAML frontmatter + instructions
├── scripts/           # Optional: Executable code (Python/Bash)
├── references/        # Optional: Documentation loaded as needed
└── assets/            # Optional: Files used in output
```

### YAML Frontmatter (Required)

```yaml
---
name: skill-name-here
description: What this does and when to use it (max 1024 chars for CLI)
allowed-tools: Read, Grep, Bash # Optional, CLI-only feature
---
```

**Field Requirements:**

| Field | Rules |
|-------|-------|
| `name` | Lowercase, hyphens, numbers. Max 64 chars. Unique. |
| `description` | WHAT it does + WHEN to use. Max 1024 chars (CLI) / 200 (API). Include triggers! |
| `allowed-tools` | **CLI-only**. Comma-separated list restricts tools. Optional. |

**Good vs Bad Descriptions:**

✅ **Good**: "Extract text and tables from PDFs, fill forms, merge documents. Use when working with PDF files or when user mentions forms, contracts, document processing."

❌ **Bad**: "Helps with documents" (too vague, no triggers)

### Progressive Disclosure (3 Levels)

Skills use progressive loading to manage context efficiently:

1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude (unlimited*)

*Scripts can execute without reading into context.

______________________________________________________________________

## Bundled Resources

Skills can include `scripts/`, `references/`, and `assets/` directories. See [Progressive Disclosure](/Users/terryli/.claude/skills/skill-architecture/references/progressive-disclosure.md) for detailed guidance on when to use each.

______________________________________________________________________

## CLI-Specific Features

CLI skills support `allowed-tools` restriction for security. See [Security Practices](/Users/terryli/.claude/skills/skill-architecture/references/security-practices.md) for details.

______________________________________________________________________

## Structural Patterns

See [Structural Patterns](/Users/terryli/.claude/skills/skill-architecture/references/structural-patterns.md) for detailed guidance on:

1. **Workflow Pattern** - Sequential multi-step procedures
2. **Task Pattern** - Specific, bounded tasks
3. **Reference Pattern** - Knowledge repository
4. **Capabilities Pattern** - Tool integrations

______________________________________________________________________

## User Conventions Integration

This skill follows Terry's conventions from [`~/.claude/CLAUDE.md`](/Users/terryli/.claude/CLAUDE.md):

- **Absolute paths**: Always use `/Users/terryli/...` (iTerm2 Cmd+click compatible)
- **Unix-only**: macOS, Linux (no Windows support)
- **Python**: `uv run script.py` with PEP 723 inline dependencies
- **Planning**: OpenAPI 3.1.1 specs in [`/Users/terryli/.claude/specifications/`](/Users/terryli/.claude/specifications/)

______________________________________________________________________

## Marketplace Scripts

See [Scripts Reference](/Users/terryli/.claude/skills/skill-architecture/references/scripts-reference.md) for marketplace script usage.

______________________________________________________________________

## Reference Documentation

For detailed information, see:

- [Structural Patterns](/Users/terryli/.claude/skills/skill-architecture/references/structural-patterns.md) - 4 skill architecture patterns
- [Progressive Disclosure](/Users/terryli/.claude/skills/skill-architecture/references/progressive-disclosure.md) - Context management patterns
- [Creation Workflow](/Users/terryli/.claude/skills/skill-architecture/references/creation-workflow.md) - Step-by-step process
- [Scripts Reference](/Users/terryli/.claude/skills/skill-architecture/references/scripts-reference.md) - Marketplace script usage
- [Security Practices](/Users/terryli/.claude/skills/skill-architecture/references/security-practices.md) - Threats and defenses (CVE references)
- [Token Efficiency](/Users/terryli/.claude/skills/skill-architecture/references/token-efficiency.md) - Context optimization
- [Advanced Topics](/Users/terryli/.claude/skills/skill-architecture/references/advanced-topics.md) - CLI vs API, composition, bugs
- [Validation Reference](/Users/terryli/.claude/skills/skill-architecture/references/validation-reference.md) - Quality checklist
- [SYNC-TRACKING](/Users/terryli/.claude/skills/skill-architecture/references/SYNC-TRACKING.md) - Marketplace version tracking
