---
description: Create new Claude Code skill with guided workflow
argument-hint: [skill name]
---

# Task

Create a new Claude Code skill following official Anthropic guidelines with strict validation and a guided Socratic workflow.

# Instructions

## Phase 1: Gather Requirements (Socratic Method)

Ask clarifying questions to fully understand the skill before creating it. Use the AskUserQuestion tool to gather information:

1. **Purpose and Scope:**
   - What task or workflow should this skill help with?
   - When should this skill be triggered or used?
   - What problem does it solve?

2. **Core Steps and Process:**
   - What are the key steps in this workflow?
   - Are there specific commands or tools that should be used?
   - What order should steps be executed in?

3. **Guidelines and Best Practices:**
   - What are common mistakes or pitfalls to avoid?
   - Are there specific rules or constraints to follow?
   - What makes a good vs. bad implementation?

4. **Examples and Templates:**
   - Should the skill include code examples?
   - Are there template structures to follow?
   - What would a successful outcome look like?

5. **Validation and Verification:**
   - How can you verify the skill was applied correctly?
   - Are there checks or tests that should be run?
   - What indicates success or failure?

## Phase 2: Fetch Official Guidelines

Before drafting the skill, fetch and review official Anthropic skill documentation:

1. **Search for guidelines:**
   - Use WebSearch to find: "Anthropic Claude Code skills documentation guidelines 2025"
   - Look for: github.com/anthropics/skills, official blog posts, support articles
   - Focus on skill structure, format requirements, and best practices

2. **Extract key requirements:**
   - Required YAML frontmatter fields
   - Markdown formatting guidelines
   - Instruction writing best practices
   - Common patterns and anti-patterns

3. **Review existing skills:**
   - First, determine the config directory: `echo "${XDG_CONFIG_HOME:-$HOME/.config}"`
   - Read skills from `<config-dir>/nix/home-manager/modules/coding-agents/claude/skills/` for reference
   - Check superpowers plugin skills if available
   - Identify patterns and styles that work well

## Phase 3: Draft Skill Content

Create the skill markdown file with proper structure:

### Required Structure:

```markdown
---
description: [Clear, concise description of what the skill does]
---

# [Skill Name]

[Brief introduction explaining when and why to use this skill]

## Instructions

[Step-by-step instructions in clear, imperative language]

1. **[Step Category]:**
   - [Specific action]
   - [Specific action]
   - [Important consideration]

2. **[Next Step Category]:**
   - [Specific action]
   - [Expected outcome]

## [Optional: Examples Section]

[Code blocks, command examples, or templates if relevant]

## [Optional: Validation/Testing Section]

[How to verify the skill was applied correctly]

## [Optional: Notes/Warnings Section]

[Important caveats, edge cases, or gotchas]

Arguments: $ARGUMENTS [if the skill accepts arguments]
```

### Content Guidelines:

1. **Description (YAML frontmatter):**
   - Must be present and concise (1-2 sentences)
   - Should clearly state what the skill does
   - Example: "Create comprehensive test suites following TDD principles"

2. **Instructions:**
   - Use imperative mood (Do X, Check Y, Verify Z)
   - Break into logical phases or categories
   - Be specific and actionable
   - Include expected outcomes
   - Mention tools to use (Read, Edit, Bash, etc.)

3. **Formatting:**
   - Use proper markdown headings (##, ###)
   - Use bold for emphasis on key terms
   - Use code blocks for commands, code, or examples
   - Use lists for sequential steps or multiple points

4. **Tone and Style:**
   - Clear and direct
   - Professional but not overly formal
   - Focus on "what" and "why", not just "how"
   - Avoid ambiguity or vague instructions

## Phase 4: Validate Skill

Before writing the file, validate the skill content:

1. **Structure validation:**
   - ✓ Has YAML frontmatter with `description` field
   - ✓ Description is clear and concise
   - ✓ Has proper markdown headings
   - ✓ Instructions are well-organized

2. **Content validation:**
   - ✓ Instructions are specific and actionable
   - ✓ Each step has a clear purpose
   - ✓ Expected outcomes are mentioned
   - ✓ Common pitfalls are addressed
   - ✓ Examples are provided if relevant

3. **Format validation:**
   - ✓ Proper YAML frontmatter syntax
   - ✓ Consistent markdown formatting
   - ✓ Code blocks are properly fenced
   - ✓ No broken syntax or structure

4. **Quality validation:**
   - ✓ Skill is focused on one clear task
   - ✓ Instructions are comprehensive but not overwhelming
   - ✓ Language is clear and unambiguous
   - ✓ Skill adds value beyond general instructions

## Phase 5: Create Skill File

1. **Determine filename:**
   - Use kebab-case: `my-skill-name.md`
   - Should clearly indicate the skill's purpose
   - Check that file doesn't already exist

2. **Write to Home Manager skills directory:**
   - Determine config directory: `echo "${XDG_CONFIG_HOME:-$HOME/.config}"`
   - Path: `<config-dir>/nix/home-manager/modules/coding-agents/claude/skills/[skill-name].md`
   - Use Write tool to create the file
   - This will be managed by Home Manager and symlinked to `~/.claude/skills/`

3. **Apply with Home Manager:**
   - Run `hm switch` to symlink the new skill to `~/.claude/skills/`
   - Wait for the command to complete successfully
   - Check for any errors or warnings in the output

4. **Verify creation:**
   - Read the file back to confirm it was written correctly
   - Check symlink exists: `ls -l ~/.claude/skills/[skill-name].md`

## Phase 6: Document and Explain

1. **Confirm creation:**
   - Show the skill name and location
   - Summarize what the skill does
   - Explain when to use it

2. **Usage instructions:**
   - How to invoke the skill (if applicable)
   - What arguments it accepts (if any)
   - Expected behavior when used

3. **Next steps:**
   - Skill is available after `hm switch` completes
   - Test it with a relevant scenario if appropriate
   - Can be modified later by editing the file and running `hm switch`

# Validation Checklist

Before creating the skill file, ensure ALL of these are true:

- [ ] Description field exists in YAML frontmatter
- [ ] Description clearly states the skill's purpose
- [ ] Instructions are broken into logical phases/steps
- [ ] Each step is specific and actionable
- [ ] Instructions use imperative mood
- [ ] Expected outcomes are mentioned
- [ ] Common pitfalls or mistakes are addressed
- [ ] Markdown formatting is correct and consistent
- [ ] Code examples use proper fenced blocks
- [ ] Skill name is clear and descriptive
- [ ] File name uses kebab-case
- [ ] Content follows official Anthropic guidelines
- [ ] Skill is focused on a single, clear purpose
- [ ] Language is clear and unambiguous

# Example Skills to Reference

Look at existing skills in `<config-dir>/nix/home-manager/modules/coding-agents/claude/skills/` for format examples (where `<config-dir>` is `${XDG_CONFIG_HOME:-$HOME/.config}`):
- `debug-error.md` - Systematic debugging workflow
- `code-review.md` - Comprehensive code review checklist
- `code.md` - Simple utility skill

These are symlinked to `~/.claude/skills/` at runtime by Home Manager.

# Notes

- Skills are managed declaratively through Home Manager
- After creating a skill, run `hm switch` to apply changes
- Skills are symlinked from the source directory to `~/.claude/skills/`
- Skills can include executable scripts or additional resources
- Skills should be self-contained and comprehensive
- Don't create skills for trivial tasks (use slash commands instead)
- Skills are best for complex, multi-step workflows that need guidance
- Update skills by editing the source file and running `hm switch`

# Error Handling

If skill creation fails:
1. Check that `<config-dir>/nix/home-manager/modules/coding-agents/claude/skills/` directory exists (where `<config-dir>` is `${XDG_CONFIG_HOME:-$HOME/.config}`)
2. Verify the skill name doesn't conflict with existing skills
3. Ensure markdown syntax is valid
4. Confirm YAML frontmatter is properly formatted
5. If `hm switch` fails, check the Nix error message and fix syntax issues

Arguments: $ARGUMENTS (optional: skill name or topic)
