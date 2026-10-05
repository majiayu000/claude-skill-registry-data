---
name: demo-skill
description: A demonstration skill showing the basic structure. Use this as a template when creating new skills.
version: 1.0.0
---

# Demo Skill

This is a demonstration skill that shows the basic structure of a Newhorse skill.

## Overview

Skills are modular capabilities that can be added to agents. They define:
- Specific workflows and procedures
- Reference documentation
- Helper scripts for complex operations

## When to Use

This skill is triggered when:
- User asks about how to create skills
- User wants to see an example skill structure
- User mentions "demo skill" or "example skill"

## Skill Structure

```
demo-skill/
├── SKILL.md           # This file - skill definition
├── scripts/           # Optional: executable scripts
│   └── example.py     # Python helper script
└── references/        # Optional: reference docs
    └── guide.md       # Additional documentation
```

## Usage Example

When a user asks: "Show me how skills work"

The agent should:
1. Explain the skill structure
2. Reference this SKILL.md as an example
3. Point to the scripts/ directory for executable helpers

## Creating New Skills

To create a new skill:

1. Create a directory under `extensions/skills/`
2. Add a `SKILL.md` file with frontmatter (name, description)
3. Optionally add scripts/ for helper code
4. Optionally add references/ for documentation

### SKILL.md Template

```markdown
---
name: your-skill-name
description: Brief description of what this skill does and when to use it
version: 1.0.0
---

# Skill Name

## Overview
What this skill does...

## When to Use
Trigger conditions...

## Workflow
Step-by-step process...
```

## Tips

- Keep SKILL.md under 500 lines
- Put detailed docs in references/
- Use scripts/ for deterministic operations
- Description field is crucial for skill triggering
