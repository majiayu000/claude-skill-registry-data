---
name: writing-skills
description: Create Agent Skills for Claude. Use when asked to write, create, or design a skill, skillsheet, or SKILL.md file. Provides skill structure, naming conventions, description patterns, and progressive disclosure strategies.
---

# Writing Agent Skills

## Workflow

1. **Clarify the skill's purpose** - What specific capability? When should it trigger?
2. **Choose complexity level** - Single file vs. multi-file based on content volume
3. **Write the description first** - This determines discoverability
4. **Draft SKILL.md body** - Keep under 500 lines
5. **Split if needed** - Extract to reference files for progressive disclosure

## Quick Reference

### Required Structure

```yaml
---
name: skill-name-here
description: What it does and when to use it. Always third person.
---

# Skill Title

[Instructions go here]
```

### Naming Rules

- Max 64 characters
- Lowercase letters, numbers, hyphens only
- No "anthropic" or "claude" in name
- Prefer gerund form: `processing-pdfs`, `analyzing-code`, `writing-tests`

### Description Rules

- Max 1024 characters
- Third person only ("Processes files", not "I process files")
- Include WHAT it does AND WHEN to use it
- Include trigger keywords users might say

## Key Principles

**Concise is key** - Context window is shared. Only add what Claude doesn't already know.

**Match freedom to fragility:**
- High freedom (text instructions) → Multiple valid approaches, context-dependent
- Medium freedom (pseudocode/templates) → Preferred pattern exists, some variation OK
- Low freedom (exact scripts) → Fragile operations, must follow precisely

**Progressive disclosure** - SKILL.md is the table of contents. Reference files for details.

## Detailed References

- **Structure & YAML requirements**: See [reference/structure.md](reference/structure.md)
- **Writing effective descriptions**: See [reference/descriptions.md](reference/descriptions.md)
- **Patterns (templates, workflows, examples)**: See [reference/patterns.md](reference/patterns.md)
- **Progressive disclosure & file organization**: See [reference/progressive-disclosure.md](reference/progressive-disclosure.md)

## Full Documentation

For comprehensive guidance, see the Anthropic docs in this project:
- [agent-skills-overview.md](../../../docs/agent-skills-overview.md) - Architecture, how skills work
- [agent-skills-best-practices.md](../../../docs/agent-skills-best-practices.md) - Complete authoring guide
- [agent-skills-in-the-sdk.md](../../../docs/agent-skills-in-the-sdk.md) - SDK integration

## Checklist Before Finalizing

- [ ] Description includes WHAT and WHEN
- [ ] Description is third person
- [ ] Name uses lowercase/numbers/hyphens only
- [ ] SKILL.md body under 500 lines
- [ ] References are one level deep (not nested)
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
