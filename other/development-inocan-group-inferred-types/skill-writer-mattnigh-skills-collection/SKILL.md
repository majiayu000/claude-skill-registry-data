---
name: skill-writer
description: Creates and validates Claude Code skills with proper format. Use when creating new skills, writing SKILL.md files, validating existing skills, or when user mentions "skill format", "create skill", "skill template", or "validate skill".
---

# Skill Writer

This skill helps Claude Code create properly formatted skills following all Claude Code conventions. It provides four main capabilities: generating new skills, validating existing skills, providing templates, and interactive skill building.

## Capabilities

1. **Generate Complete SKILL.md Files**: Create new skills from scratch with proper YAML frontmatter and structure
2. **Validate Existing Skills**: Check skills for correct format, YAML syntax, and best practices
3. **Provide Templates and Examples**: Access pre-built templates for common skill patterns
4. **Interactive Skill Builder**: Guide users through questions to build skills step-by-step

## Instructions

### When User Asks to Create a New Skill

1. **Use Interactive Approach**: Ask the user these questions:
   - What is the skill name? (lowercase, hyphens only, max 64 chars)
   - What does the skill do? (capabilities)
   - When should Claude invoke it? (trigger keywords and contexts)
   - Should it restrict tools? (optional: read-only, specific tools)
   - Does it need supporting files? (templates, examples, scripts)

2. **Generate the SKILL.md File**:
   ```yaml
   ---
   name: skill-identifier
   description: Clear description of capabilities and usage triggers
   allowed-tools: Optional, Read, Grep, Glob
   ---

   # Skill Title

   ## Instructions
   Step-by-step guidance for Claude.

   ## Examples
   Concrete usage examples.
   ```

3. **Critical Format Rules**:
   - Opening `---` MUST be on line 1
   - Use spaces for indentation, NEVER tabs
   - Name: lowercase, numbers, hyphens only
   - Description: Must include WHAT (capabilities) and WHEN (triggers)
   - Maximum description length: 1024 characters
   - Maximum name length: 64 characters

4. **Create Supporting Files If Needed**:
   - `templates/` for reusable templates
   - `examples.md` for detailed examples
   - `reference.md` for documentation
   - `scripts/` for utility scripts

### When User Asks to Validate a Skill

1. **Read the SKILL.md file** using the Read tool

2. **Check YAML Frontmatter**:
   - Verify opening `---` is on line 1
   - Verify closing `---` exists before content
   - Check for tabs (should only use spaces)
   - Validate name format: lowercase, hyphens, max 64 chars
   - Validate description exists and is clear
   - Check allowed-tools syntax if present

3. **Evaluate Description Quality**:
   - Does it explain WHAT the skill does?
   - Does it explain WHEN to invoke it?
   - Does it include specific trigger keywords?
   - Is it under 1024 characters?
   - Would Claude know when to use it?

4. **Check File Structure**:
   - Verify proper Markdown formatting
   - Check for clear sections (Instructions, Examples)
   - Validate any file references use forward slashes
   - Ensure supporting files exist if referenced

5. **Report Findings**: Provide specific issues found and suggestions for fixes

6. **Reference validation-checklist.md** for comprehensive validation steps

### When User Wants Templates

1. **Reference templates.md** which contains:
   - Minimal single-file skill template
   - Multi-file skill with supporting docs
   - Read-only skill with allowed-tools restriction
   - Advanced skill with dependencies and scripts

2. **Suggest the appropriate template** based on user's needs:
   - Simple one-off task → Minimal single-file
   - Complex workflow → Multi-file structure
   - Code review/analysis → Read-only with tool restrictions
   - External tools needed → Advanced with dependencies

3. **Customize the template** with user's specific requirements

### Interactive Skill Builder Workflow

When user says "help me build a skill" or similar:

1. **Gather Requirements**:
   ```
   - What specific task should this skill accomplish?
   - What trigger words would a user naturally use?
   - Should Claude be able to modify files or only read?
   - Do you need any scripts, templates, or examples?
   - Are there any dependencies (npm packages, Python libraries)?
   ```

2. **Propose a Structure**: Based on answers, suggest:
   - Skill name (derived from task)
   - Description draft (with triggers)
   - File structure (single vs multi-file)
   - Tool restrictions if applicable

3. **Get Feedback**: Show the proposed structure and ask for confirmation

4. **Generate the Skill**: Create all files with proper formatting

5. **Explain Usage**: Tell user how the skill will be invoked

## Best Practices

### Description Writing

**BAD**: "Helps with documents"
**GOOD**: "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."

The description is CRITICAL for skill discovery. Include:
- Specific capabilities (what it does)
- Natural trigger keywords (what users would say)
- Context clues (when it's relevant)

### Naming Conventions

- Use descriptive, action-oriented names
- Keep it concise but clear
- Examples: `commit-message-generator`, `code-reviewer`, `pdf-processor`
- NOT: `helper`, `util`, `tool`

### Focus and Scope

- Keep each skill focused on ONE primary capability
- Split broad skills into specialized ones
- Example: Instead of "document-processor", create:
  - `pdf-extractor` for extraction
  - `pdf-form-filler` for forms
  - `pdf-merger` for merging

### Tool Restrictions

Use `allowed-tools` for:
- Read-only operations (code review, analysis)
- Security-sensitive workflows
- Preventing accidental modifications

Example:
```yaml
allowed-tools: Read, Grep, Glob
```

### File Organization

```
skill-name/
├── SKILL.md (required)
├── templates.md (optional)
├── examples.md (optional)
├── reference.md (optional)
├── scripts/
│   └── helper.py
└── templates/
    └── template.txt
```

Use forward slashes in all paths: `scripts/helper.py`

## Common Skill Patterns

### 1. Code Analysis Skill
```yaml
---
name: code-analyzer
description: Analyze code for patterns, complexity, and maintainability. Use when reviewing code quality or checking for anti-patterns.
allowed-tools: Read, Grep, Glob
---
```
**Pattern**: Read-only, focuses on analysis without modifications

### 2. Generator Skill
```yaml
---
name: test-generator
description: Generate unit tests for functions and classes. Use when writing tests or when user mentions test coverage.
---
```
**Pattern**: Creates new files, needs write access

### 3. Transformation Skill
```yaml
---
name: refactorer
description: Refactor code for better structure and readability. Use when improving code organization or reducing complexity.
---
```
**Pattern**: Modifies existing files, needs edit access

### 4. Workflow Skill
```yaml
---
name: deploy-checker
description: Validate deployment readiness with checklist. Use before deployments or when user mentions release preparation.
---
```
**Pattern**: Multi-step process, may need various tools

## Examples

See [examples.md](examples.md) for complete, real-world skill examples with explanations.

See [templates.md](templates.md) for ready-to-use templates.

See [validation-checklist.md](validation-checklist.md) for comprehensive validation steps.

## Technical Validation Checklist

Before finalizing any skill, verify:

- [ ] YAML frontmatter has `---` on line 1
- [ ] Closing `---` exists before Markdown content
- [ ] No tabs in YAML (spaces only)
- [ ] Name is lowercase with hyphens only
- [ ] Name is max 64 characters
- [ ] Description includes capabilities and triggers
- [ ] Description is max 1024 characters
- [ ] File paths use forward slashes
- [ ] Supporting files exist if referenced
- [ ] Dependencies are documented if needed
- [ ] Examples are concrete and actionable

## Usage Reminder

After creating or modifying a skill:
1. Restart Claude Code to load the changes
2. Test by asking questions that match the description
3. Refine the description if Claude doesn't invoke it correctly
