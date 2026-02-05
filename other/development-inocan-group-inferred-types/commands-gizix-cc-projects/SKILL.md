---
description: Add an agent skill to an existing template
argument-hint: <template-name> <skill-name>
allowed-tools: Read(*), Write(*), Bash(*)
---

Add a new agent skill to an existing project template. Skills are automatically activated based on context.

## Arguments

- $1: Template directory name (e.g., "django-template", "react-template")
- $2: Skill name in lowercase-letters-numbers-hyphens (e.g., "component-generator", "api-validator")

## Process

1. **Verify Template Exists**

Check that `$1/.claude/skills/` directory exists.

2. **Gather Skill Details**

Ask the user:
- What capability does this skill provide?
- When should it automatically activate?
- What file types or scenarios trigger it?
- What patterns or templates does it implement?
- Should it be read-only or can it modify code?

3. **Create Skill Directory**

Create `$1/.claude/skills/$2/` with:
- SKILL.md (required)
- reference.md (optional - detailed docs)
- examples/ (optional - example files)
- templates/ (optional - code templates)
- scripts/ (optional - helper scripts)

4. **Create SKILL.md**

Generate with proper frontmatter and comprehensive instructions.

5. **Update Documentation**

Add the skill to `$1/README.md` in the skills section.

## Example Usage

```
/add-skill react-template component-generator
```

## Best Practices for Skills

- **Specific triggers**: Include file extensions, keywords in description
- **Focused capability**: One skill, one type of task
- **Complete examples**: Show full, working code
- **Framework-specific**: Tailor to the template's technology
- **Tool restrictions**: Limit to necessary tools
