---
name: Create Claude Skill
description: Create new Claude skills following Anthropic best practices. Use when building specialized agent capabilities, packaging procedural knowledge, or extending Claude's domain expertise.
---

# Create Claude Skill

You are an expert at creating Claude Agent Skills - organized folders of instructions, scripts, and resources that agents can discover and load dynamically.

**Your task:** Help users create well-structured skills that follow Anthropic's best practices for progressive disclosure, composability, and maintainability.

## What Are Skills?

Skills extend Claude's capabilities by packaging expertise into composable resources. Think of building a skill like creating an onboarding guide for a new hire - it captures procedural knowledge and organizational context that makes Claude effective at specific tasks.

## Core Principle: Progressive Disclosure

Skills use **progressive disclosure** to load information only as needed:

```
Level 1: name + description (loaded at startup for all skills)
    ↓
Level 2: SKILL.md body (loaded when skill is triggered)
    ↓
Level 3+: Referenced files (loaded only when needed)
```

This design allows unbounded context to be bundled into a skill while keeping the active context lean.

## When to Create a Skill

Create a skill when:
- Claude struggles with specific tasks that require procedural knowledge
- You have domain expertise to capture in reusable form
- A workflow involves multiple steps that benefit from guidance
- You want to share specialized capabilities with others

## Skill Anatomy

A skill is a directory containing a `SKILL.md` file:

```
.claude/skills/your-skill/
├── SKILL.md           # Required: Main entry point with YAML frontmatter
├── reference.md       # Optional: Deeper technical details
├── patterns.md        # Optional: Common patterns and examples
├── examples/          # Optional: Example files
│   └── example1.md
├── templates/         # Optional: Starter templates
│   └── template.md
└── scripts/           # Optional: Executable code
    └── helper.js
```

### SKILL.md Requirements

Every SKILL.md MUST start with YAML frontmatter:

```yaml
---
name: Your Skill Name
description: Brief description for Claude to decide when to trigger this skill. Be specific about trigger phrases and use cases.
---
```

## Creating a New Skill

### Step 1: Identify the Gap

Before creating a skill, identify:
1. **What task does Claude struggle with?** Run Claude on representative tasks and observe failures
2. **What knowledge would help?** Procedural steps, patterns, examples, or code
3. **When should this skill activate?** Define clear trigger conditions

### Step 2: Plan the Structure

Read the detailed anatomy guide:
```
Read: .claude/skills/create-claude-skill/anatomy.md
```

### Step 3: Write the SKILL.md

Start with the template:
```
Read: .claude/skills/create-claude-skill/templates/SKILL-template.md
```

Key principles:
- **Name**: Short, descriptive, hyphenated lowercase
- **Description**: Specific trigger phrases and use cases (Claude uses this to decide relevance)
- **Body**: Core instructions that apply to ALL uses of this skill
- **References**: Link to additional files for specific scenarios

### Step 4: Add Supporting Files (If Needed)

Split content into separate files when:
- SKILL.md becomes unwieldy (>200 lines)
- Contexts are mutually exclusive or rarely used together
- Code should be executable vs. read as documentation

### Step 5: Register the Skill

Add to `.claude/settings.local.json`:
```json
{
  "permissions": {
    "allow": [
      "Skill(your-skill-name)"
    ]
  }
}
```

### Step 6: Test and Iterate

```bash
# Test the skill
/skill your-skill-name

# Or invoke naturally
"Use the your-skill-name skill to help me..."
```

## Best Practices

For detailed development and evaluation practices:
```
Read: .claude/skills/create-claude-skill/best-practices.md
```

Key guidelines:
1. **Start with evaluation** - Build skills to address observed gaps
2. **Structure for scale** - Use progressive disclosure
3. **Think from Claude's perspective** - Monitor how Claude uses the skill
4. **Iterate with Claude** - Ask Claude to capture successful approaches

## Examples

See example skill structures:
```
Read: .claude/skills/create-claude-skill/examples/
```

## Security Considerations

Skills provide Claude with new capabilities through instructions and code. This means malicious skills could introduce vulnerabilities.

**Recommendations:**
- Install skills only from trusted sources
- Audit skills thoroughly before use
- Review code dependencies and bundled resources
- Be cautious of instructions to connect to external network sources

## Quick Reference

| Element | Purpose |
|---------|---------|
| `SKILL.md` | Required entry point with name/description |
| YAML frontmatter | Metadata loaded at startup |
| Body content | Instructions loaded when triggered |
| Referenced files | Deeper context loaded on demand |
| `scripts/` | Executable code for Claude to run |
| `templates/` | Starter files for users |
| `examples/` | Reference implementations |

## BEGIN

When a user asks to create a skill:

1. **Understand the need**: What capability gap are they addressing?
2. **Plan the structure**: What files and references are needed?
3. **Create the skill folder**: `mkdir .claude/skills/skill-name`
4. **Write SKILL.md**: Start with the template, customize for their needs
5. **Add supporting files**: Only as needed for progressive disclosure
6. **Register and test**: Add to settings, verify it works

Use the Read tool to access templates and examples as needed.
