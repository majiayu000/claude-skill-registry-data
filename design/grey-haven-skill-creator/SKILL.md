---
name: grey-haven-skill-creator
description: "Guide for creating effective skills that extend Claude's capabilities. Use when users want to create a new skill, update an existing skill, or need guidance on skill structure and best practices. Triggers: 'create skill', 'new skill', 'skill template', 'build skill', 'skill structure', 'skill design'."
skills:
  - grey-haven-prompt-engineering
allowed-tools:
  - Read
  - Write
  - MultiEdit
  - Bash
  - Grep
  - Glob
  - TodoWrite
---

# Skill Creator

Guide for creating effective skills that extend Claude's capabilities.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains—they transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge.

### What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, and assets for complex tasks

## Core Principles

### Concise is Key

The context window is a public good. Skills share context with system prompts, conversation history, other skills, and user requests.

**Default assumption: Claude is already very smart.** Only add context Claude doesn't already have. Challenge each piece: "Does Claude really need this?" and "Does this justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match specificity to task fragility:

| Freedom Level | When to Use | Format |
|---------------|-------------|--------|
| High | Multiple approaches valid, context-dependent | Text-based instructions |
| Medium | Preferred pattern exists, some variation OK | Pseudocode or parameterized scripts |
| Low | Operations fragile, consistency critical | Specific scripts, few parameters |

Think of Claude exploring a path: narrow bridge needs guardrails (low freedom), open field allows many routes (high freedom).

### Grey Haven Skill Anatomy

Every Grey Haven skill follows this structure:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (required)
│   │   ├── name: grey-haven-{skill-name}
│   │   ├── description: (comprehensive, includes triggers)
│   │   ├── skills: (optional, v2.0.43)
│   │   └── allowed-tools: (optional, v2.0.74)
│   └── Markdown body (required)
└── Bundled Resources (optional)
    ├── scripts/      - Executable code
    ├── references/   - Documentation for context
    ├── examples/     - Usage examples
    ├── templates/    - Reusable templates
    └── checklists/   - Validation checklists
```

#### SKILL.md Frontmatter

```yaml
---
name: grey-haven-your-skill
description: "What the skill does. When to use it. Trigger phrases."
# v2.0.43: Auto-load these skills when this skill activates
skills:
  - grey-haven-code-style
  - grey-haven-testing-strategy
# v2.0.74: Restrict available tools when skill is active
allowed-tools:
  - Read
  - Write
  - Bash
  - TodoWrite
---
```

**Description is critical**: This is the primary trigger mechanism. Include:
- What the skill does
- When to use it
- Specific trigger phrases

#### Bundled Resources

| Directory | Purpose | When to Include |
|-----------|---------|-----------------|
| `scripts/` | Executable code | Repeated code, deterministic operations |
| `references/` | Documentation | Detailed guides, schemas, API docs |
| `examples/` | Usage examples | Complex patterns, before/after |
| `templates/` | Reusable formats | Boilerplate, standard structures |
| `checklists/` | Validation | Quality gates, pre-flight checks |

### Progressive Disclosure

Skills use a three-level loading system:

1. **Metadata** (~100 words) - Always in context
2. **SKILL.md body** (<5K words) - When skill triggers
3. **Bundled resources** - As needed by Claude

**Keep SKILL.md under 500 lines.** Split into reference files when approaching this limit. Always reference split files from SKILL.md with clear "when to read" guidance.

## Skill Creation Process

### Step 1: Understand with Concrete Examples

Before creating, understand concrete usage:

- "What functionality should this skill support?"
- "Give examples of how this skill would be used."
- "What would a user say that should trigger this skill?"

Conclude when you clearly understand the functionality needed.

### Step 2: Plan Reusable Contents

Analyze each example:

1. How would you execute this from scratch?
2. What scripts, references, assets would help when doing this repeatedly?

Example analyses:

| Skill Goal | Analysis | Resource Needed |
|------------|----------|-----------------|
| Rotate PDFs | Same code every time | `scripts/rotate_pdf.py` |
| Build webapps | Same boilerplate each time | `templates/react-starter/` |
| Query BigQuery | Rediscover schemas each time | `references/schema.md` |

### Step 3: Initialize the Skill

Run the initialization script:

```bash
python scripts/init_skill.py my-skill --path grey-haven-plugins/core/skills
```

This creates:
- SKILL.md template with TODO placeholders
- Example resource directories
- Proper structure for Grey Haven

### Step 4: Edit the Skill

**Writing Guidelines:**
- Use imperative/infinitive form
- Challenge every paragraph's token cost
- Prefer examples over explanations

**Frontmatter:**
- `name`: Use `grey-haven-` prefix
- `description`: Include what + when + triggers
- `skills`: Optional dependent skills
- `allowed-tools`: Optional tool restrictions

**Body:**
- Start with clear overview
- Include practical examples
- Reference bundled resources with "when to read" guidance

**Design Patterns** (see `references/`):
- Multi-step processes: See `references/workflows.md`
- Output formats: See `references/output-patterns.md`

### Step 5: Test and Iterate

After creating:

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Update SKILL.md or resources
4. Test again

## What NOT to Include

Skills should only contain essential files. Do NOT create:

- README.md (SKILL.md is the readme)
- INSTALLATION_GUIDE.md
- CHANGELOG.md
- User-facing documentation
- Process documentation

The skill is for Claude, not humans. Include only what helps Claude do the job.

## Grey Haven Conventions

### Naming

- Skill name: `grey-haven-{domain}-{function}`
- Directory: `skills/{skill-name}/`
- Examples: `grey-haven-tdd-python`, `grey-haven-api-design-standards`

### Description Format

```yaml
description: "{What it does}. {When to use it}. Triggers: '{trigger1}', '{trigger2}', '{trigger3}'."
```

### File Organization

```
skill-name/
├── SKILL.md
├── examples/
│   └── practical-example.md
├── references/
│   └── detailed-guide.md
├── templates/
│   └── reusable-template.md
└── checklists/
    └── validation-checklist.md
```

## Quick Start

```bash
# Initialize new skill
python scripts/init_skill.py my-new-skill --path grey-haven-plugins/core/skills

# Edit the generated SKILL.md
# Add resources as needed
# Test with real usage
```

---

**Skill Version**: 1.0
**Based on**: Anthropic skill-creator (Dec 2025)
**Last Updated**: 2025-01-15
