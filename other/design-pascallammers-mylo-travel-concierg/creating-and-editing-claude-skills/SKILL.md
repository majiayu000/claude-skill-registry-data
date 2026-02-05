---
name: Creating and Editing Claude Skills
description: Use before creating or editing any SKILL.md files, and immediately after making skill changes to verify quality. Invoked when user asks about skill structure, descriptions, or best practices. Provides expert guidance on naming, descriptions for discoverability, progressive context reveal, and validation workflows. Critical for ensuring skills are discoverable and effective - prevents poorly structured skills that Claude won't use properly.
---

# Writing Claude Skills

This skill provides comprehensive guidance for creating high-quality Claude Code skills that are modular, discoverable, and effective.

## What Are Claude Skills?

Skills are modular capabilities that extend Claude's functionality. They are:
- **Model-invoked**: Claude autonomously decides when to use them based on descriptions
- **Discoverable**: Found through descriptive `SKILL.md` files
- **Shareable**: Can be personal, project-specific, or plugin-bundled

Skills differ from slash commands (user-invoked) - they're capabilities Claude chooses to use.

## Core Structure

Every skill requires a directory containing `SKILL.md` with YAML frontmatter:

```markdown
---
name: Your Skill Name
description: Clear, specific one-line description
---

# Instructions and content
```

For detailed structure information including optional files, see `reference/skill-structure.md`.

## Key Principles

### 1. Be Concise
- Keep SKILL.md under 500 lines
- Only include what Claude doesn't already know
- Use progressive disclosure with reference files

### 2. Clear Naming
- Use gerund form (verb + -ing): "Processing PDFs", "Analyzing Data"
- Avoid vague names: "Helper", "Utils", "Manager"
- Make names descriptive and specific

### 3. Specific Descriptions
- Write in third person
- Include key terms for discoverability
- Clearly indicate when to use the skill
- Maximum 1024 characters

### 4. Progressive Context Reveal
- Start with essential information in SKILL.md
- Reference detailed docs when needed
- Organize supporting files logically

## Creating a Skill

### Quick Start

1. Create skill directory: `mkdir -p .claude/skills/my-skill`
2. Create `SKILL.md` with frontmatter
3. Write clear name and description
4. Add concise instructions
5. Test with Claude

For a complete template, see `templates/skill-template.md`.

### Writing Effective Instructions

**DO:**
- Provide concrete examples
- Create clear step-by-step workflows
- Include validation/feedback loops
- Use consistent terminology
- Reference additional files for details

**DON'T:**
- Include time-sensitive information
- Over-explain what Claude already knows
- Use vague or ambiguous language
- Cram all details into SKILL.md

### Setting Degrees of Freedom

Match specificity to task requirements:
- **High freedom**: Flexible, creative tasks
- **Low freedom**: Fragile, sequence-critical operations

Example:
```markdown
# Low freedom (specific)
When processing invoice PDFs:
1. Extract date field using format YYYY-MM-DD
2. Validate amount matches total
3. Output to invoices.json

# High freedom (flexible)
Analyze the document and extract relevant financial information.
```

## File Organization

Use progressive disclosure for complex skills within the skill directory:

```
my-skill/
├── SKILL.md              # Concise entry point
├── reference/            # Detailed documentation
│   ├── api-docs.md
│   └── examples.md
├── scripts/              # Helper utilities
│   └── validator.py
└── templates/            # Starting templates
    └── output.json
```

**IMPORTANT**: Skills must be self-contained within their directory:
- Only reference files within the skill directory
- Do NOT reference external files (e.g., `../../CLAUDE.md` or project files)
- Include all necessary content within the skill structure
- Skills may be used in different contexts and must work independently

See `reference/skill-structure.md` for detailed organization patterns.

## Best Practices

For comprehensive best practices, see `reference/best-practices.md`. Key highlights:

### Description Writing
```markdown
# Good
description: Guides creation of React components following project conventions, including TypeScript types, styled-components, and test patterns

# Vague
description: Helps with React stuff
```

### Documentation
- Write skills for the current Claude model's capabilities
- Avoid time-sensitive information
- Test iteratively with real scenarios
- Create evaluation cases before extensive docs

### Tool Restrictions
Limit tool access when needed:
```yaml
---
name: Read-Only Analysis
allowed-tools: [Read, Grep, Glob]
---
```

## Examples

See `reference/examples.md` for complete skill examples including:
- Simple focused skills
- Complex multi-file skills
- Skills with tool restrictions
- Skills with progressive disclosure

## Testing and Iteration

1. Start with core functionality
2. Test with Claude on real scenarios
3. Refine based on actual usage
4. Add supporting docs as needed
5. Keep SKILL.md concise, move details to reference files

## Critical Workflow: Review After Every Change

**IMPORTANT**: Whenever you make changes to a skill file (creating, editing, or updating SKILL.md or related files), you MUST immediately review the skill against best practices.

### Required Review Steps

After making any skill changes:

1. **Read the updated skill**: Use the Read tool to view the complete updated SKILL.md
2. **Apply review checklist**: Review against criteria in `reference/skill-review.md`:
   - Name: Gerund form, specific, not vague
   - Description: Under 1024 chars, includes key terms, third person
   - Length: SKILL.md under 500 lines
   - Examples: Concrete and helpful
   - Validation: Steps included for verifying success
   - Clarity: Instructions are unambiguous and actionable
   - Organization: Logical structure with progressive disclosure
3. **Identify issues**: Note any deviations from best practices
4. **Fix immediately**: If issues are found, fix them before completing the task

### What to Check

- **Discoverability**: Will Claude find and use this skill appropriately?
- **Clarity**: Are instructions clear enough to follow?
- **Completeness**: Is all necessary information included?
- **Conciseness**: Only what Claude doesn't already know?
- **Effectiveness**: Does the skill actually help accomplish the task?

### Common Issues to Catch

- Vague descriptions that hurt discoverability
- Missing validation steps
- Ambiguous instructions
- Monolithic SKILL.md files (over 500 lines)
- Over-explanation of what Claude already knows
- Missing concrete examples
- Time-sensitive information
- External file references (skills must be self-contained)

For comprehensive review guidelines, see `reference/skill-review.md`.

**This review step is not optional** - it ensures every skill change maintains quality and follows best practices.

## Reviewing Skills

Whether reviewing your own skills or others', systematic review ensures quality and effectiveness.

### Review Checklist

Quick checklist for skill review:
- **Name**: Gerund form, specific, not vague
- **Description**: Under 1024 chars, includes key terms, third person
- **Length**: SKILL.md under 500 lines
- **Examples**: Concrete and helpful
- **Validation**: Steps included for verifying success
- **Clarity**: Instructions are unambiguous and actionable
- **Organization**: Logical structure with progressive disclosure

### Key Review Areas

1. **Discoverability**: Will Claude find and use this skill appropriately?
2. **Clarity**: Are instructions clear enough to follow?
3. **Completeness**: Is all necessary information included?
4. **Conciseness**: Only what Claude doesn't already know?
5. **Effectiveness**: Does the skill actually help accomplish the task?

### Common Issues to Check

- Vague descriptions that hurt discoverability
- Missing validation steps
- Ambiguous instructions
- Monolithic SKILL.md files (over 500 lines)
- Over-explanation of what Claude already knows
- Missing concrete examples
- Time-sensitive information

For comprehensive review guidelines, see `reference/skill-review.md`.

## Common Patterns

### Single-Purpose Skill
Focus on one specific capability with clear instructions.

### Multi-Step Workflow
Provide structured steps with validation between stages.

### Context-Heavy Skill
Use progressive disclosure: essentials in SKILL.md, details in reference files.

### Tool-Restricted Skill
Limit tools for safety-critical or read-only operations.

## Troubleshooting

**Skill not discovered**: Check description specificity and key terms
**Too verbose**: Move details to reference files
**Unclear when to use**: Improve description and add usage examples
**Inconsistent results**: Reduce degrees of freedom, add specific steps

## References

- `reference/skill-structure.md`: Complete structure and organization details
- `reference/best-practices.md`: Comprehensive best practices guide
- `reference/examples.md`: Real-world skill examples
- `reference/skill-review.md`: Comprehensive skill review guidelines
- `templates/skill-template.md`: Starting template for new skills

## Quick Decision Guide

Creating a new skill? Ask:
1. **Is it focused?** One capability per skill
2. **Is the description clear?** Third person, specific, key terms
3. **Is SKILL.md concise?** Under 500 lines, essential info only
4. **Do I need reference files?** Use progressive disclosure for complex topics
5. **Have I tested it?** Try with real scenarios before finalizing

When writing skills, remember: skills extend Claude's knowledge, so focus on what Claude doesn't already know and make it easily discoverable through clear descriptions and names.
