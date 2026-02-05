---
description: Create a new Agent Skill with conversational guidance through the skill-builder skill
argument-hint: "<skill-name> [--personal|--project] [context] - e.g., 'pdf-analyzer --personal for processing research papers'"
---

# Create New Agent Skill

You are being asked to create a new Agent Skill named: **$1**

Scope: ${2:---personal}
Context: $ARGUMENTS

## What Happens Next

This command activates the **skill-builder** skill, which will have an interactive conversation with you to understand:

1. **What the skill should do** - Its purpose and capabilities
2. **When it should activate** - Trigger keywords and scenarios
3. **Whether it needs tooling** - Scripts, templates, or just instructions
4. **Tool restrictions** - If it should be read-only or have limited capabilities
5. **Dependencies** - Any packages or external tools required

## Skill-Builder Activation

The skill-builder skill is now active. It will:
- Ask clarifying questions about your needs
- Help craft an effective description for Claude to discover the skill
- Determine if the skill should be instruction-based or script-powered
- Create the complete skill structure (SKILL.md and any supporting files)
- Support both personal (`~/.claude/skills/`) and project (`.claude/skills/`) scopes

## Key Principles

**Agent Skills are model-invoked** - Claude autonomously decides when to use them based on the description. This is different from slash commands, which you explicitly trigger.

**Skills should be focused** - Each skill addresses one capability, not broad domains.

**Description is critical** - It must include both what the skill does AND when Claude should use it.

**Tooling when needed** - Not every skill needs scripts. Some are pure instruction/knowledge.

---

Please proceed with the skill-builder conversation to create: **$1**
