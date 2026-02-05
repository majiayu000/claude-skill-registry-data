---
name: skill-author
description: Guide for creating new Claude Code skills following best practices. Use when the user asks to create a new skill, agent capability, or wants to extend Claude's autonomous functionality.
---

# Skill Author: Creating High-Quality Claude Code Skills

This skill guides you through creating new skills for Claude Code, following all documented best practices and requirements.

## When to Create a Skill vs Slash Command

**Create a Skill when:**

- Claude should auto-discover and use the capability based on context
- The functionality requires multiple supporting files (scripts, templates, reference docs)
- You need complex, multi-step workflows with validation
- Teams need standardized, detailed guidance for a capability

**Create a Slash Command when:**

- Users will explicitly invoke it frequently (like `/review`)
- The prompt fits in a single file
- You want explicit user control over when it runs
- It's a simple prompt template or reminder

## Skill Directory Structure

Skills must be stored in one of three locations:

1. **Personal Skills**: `~/.claude/skills/skill-name/` - Available across all your projects
2. **Project Skills**: `.claude/skills/skill-name/` - Shared with team via git
3. **Plugin Skills**: `skills/skill-name/` in plugin directory - Bundled with plugins

Each skill directory must contain:

- `SKILL.md` (required) - Main skill definition
- Supporting files (optional):
  - `reference.md` - Additional reference documentation
  - `examples.md` - Usage examples
  - `scripts/` - Helper scripts and utilities
  - `templates/` - File templates

## SKILL.md Format

Every `SKILL.md` must start with YAML frontmatter followed by Markdown content:

```yaml
---
name: skill-name
description: What it does and when Claude should use it
allowed-tools: [Read, Grep, Glob] # Optional: restrict available tools
---
# Skill Name: Clear Purpose Statement

Main instructions for Claude to follow when using this skill...
```

### Frontmatter Requirements

**name field:**

- Lowercase letters, numbers, and hyphens only
- Maximum 64 characters
- Must match the directory name
- Examples: `pdf-processor`, `code-reviewer`, `test-generator`

**description field:**

- Maximum 1024 characters
- **CRITICAL**: Must include BOTH:
  1. **What** the skill does
  2. **When** Claude should use it (trigger keywords)
- Specific descriptions enable auto-discovery
- Vague descriptions prevent Claude from finding your skill

**Examples of good descriptions:**

```yaml
description: Analyze Excel spreadsheets and generate pivot tables. Use when working with .xlsx files or when user asks about spreadsheet data analysis.

description: Review code for security vulnerabilities using OWASP guidelines. Use when user requests security audit, vulnerability scan, or mentions security review.

description: Generate comprehensive unit tests using Vitest framework. Use when user asks to write tests, add test coverage, or test a new feature.
```

**Examples of bad descriptions:**

```yaml
description: Helps with files  # Too vague, no trigger keywords

description: Code analysis tool  # Unclear when to use

description: Processes data  # Not specific enough
```

**allowed-tools field (optional):**
Restrict which tools Claude can use within the skill:

```yaml
allowed-tools: [Read, Grep, Glob]  # Read-only file access
allowed-tools: [WebFetch, WebSearch]  # Web research only
allowed-tools: [Bash, Read, Write]  # Full system access
```

## Writing Effective Skill Content

### Structure Your Instructions

1. **Start with a clear purpose**: One-line statement of what the skill does
2. **Define the scope**: What's included and what's not
3. **Provide step-by-step guidance**: Break complex workflows into numbered steps
4. **Include concrete examples**: Show don't tell
5. **Document edge cases**: Address common scenarios
6. **Add references**: Link to supporting files in the skill directory

### Best Practices

**Keep Skills Focused**

- Each skill should address ONE specific capability
- Avoid broad categories like "code-helper" or "file-processor"
- Split into specialized skills instead: `test-generator`, `code-reviewer`, `refactoring-assistant`

**Use Progressive Disclosure**

- Put essential instructions in `SKILL.md`
- Move detailed reference material to separate files
- Claude loads supporting files only when needed
- This keeps the main skill file scannable

**Include Clear Examples**
Show concrete use cases:

```markdown
## Example Usage

When user says: "Review this code for security issues"

1. Read the specified files using Read tool
2. Apply OWASP security guidelines from reference.md
3. Check for common vulnerabilities: SQL injection, XSS, etc.
4. Format findings as: File:Line - Issue - Recommendation
```

**Document Versions**
Track changes for team awareness:

```markdown
## Version History

### v1.2.0 - 2025-01-15

- Added support for TypeScript decorators
- Fixed issue with async function detection

### v1.1.0 - 2025-01-10

- Initial release
```

**Reference Supporting Files**
Guide Claude to use additional resources:

```markdown
For detailed API reference, see `reference.md` in this skill directory.
Templates are available in the `templates/` directory.
Run validation using `scripts/validate.sh`.
```

## Testing Your Skill

### Verification Process

1. **Restart Claude Code** - Changes take effect after restart
2. **Test Auto-Discovery** - Ask questions matching your description WITHOUT mentioning the skill name
3. **Verify Activation** - Claude should independently choose to use the skill
4. **Check Tool Access** - If using `allowed-tools`, verify restrictions work

### Example Test Scenarios

For a skill with description: _"Generate unit tests using Vitest. Use when user asks to write tests or add test coverage."_

**Good test prompts:**

- "Can you write tests for this function?"
- "I need test coverage for the auth module"
- "Add unit tests to this file"

**These should trigger auto-discovery** - Claude should activate the skill without you mentioning it.

### Common Issues and Solutions

**Problem: Claude doesn't use the skill**

- ✅ Make description more specific with trigger keywords
- ✅ Validate YAML frontmatter syntax (use a YAML validator)
- ✅ Confirm file path: `.claude/skills/skill-name/SKILL.md`
- ✅ Restart Claude Code to reload skills
- ✅ Check skill name matches directory name

**Problem: Skill fails when running**

- ✅ Run `claude --debug` to see loading errors
- ✅ Verify all referenced files exist
- ✅ Check that required dependencies are installed
- ✅ Validate `allowed-tools` doesn't block needed tools

**Problem: Skill activates at wrong times**

- ✅ Refine description to be more specific
- ✅ Add explicit "Use when..." trigger conditions
- ✅ Consider splitting into multiple focused skills

## Sharing Skills with Your Team

### Recommended: Plugin Distribution

Create a plugin containing your skills for easy team installation. See plugins documentation for details.

### Alternative: Git-Based Sharing

1. Create skill in `.claude/skills/skill-name/` (project directory)
2. Commit to git repository
3. Team members get the skill automatically after `git pull`
4. Skills are available immediately (after Claude Code restart)

## Updating and Removing Skills

**To Update:**

1. Edit `SKILL.md` or supporting files directly
2. Restart Claude Code for changes to take effect
3. For project skills, commit and push changes

**To Remove:**

1. Delete the skill directory
2. For project skills, commit the deletion
3. Restart Claude Code

## Skill Creation Checklist

When creating a new skill, verify:

- [ ] Directory created in correct location (personal/project/plugin)
- [ ] Directory name matches skill name (lowercase, hyphens only)
- [ ] `SKILL.md` exists with valid YAML frontmatter
- [ ] `name` field: lowercase, hyphens, max 64 chars
- [ ] `description` field: includes WHAT and WHEN, max 1024 chars
- [ ] Description contains trigger keywords for auto-discovery
- [ ] Content is focused on ONE specific capability
- [ ] Instructions are clear and step-by-step
- [ ] Concrete examples are included
- [ ] Supporting files are referenced if used
- [ ] `allowed-tools` specified if tool restrictions needed
- [ ] Tested with multiple prompts matching description
- [ ] Claude auto-discovers and uses skill correctly
- [ ] Team sharing method chosen (plugin or git)
- [ ] Version history documented

## Examples of Well-Designed Skills

### Example 1: Focused Test Generator

```yaml
---
name: vitest-test-generator
description: Generate unit tests using Vitest framework following TDD best practices. Use when user asks to write tests, add test coverage, create test cases, or test a function or module.
allowed-tools: [Read, Write, Grep, Glob, Bash]
---

# Vitest Test Generator

Generate comprehensive unit tests following TDD principles.

## Workflow

1. Read the code file to understand the implementation
2. Identify testable units (functions, methods, classes)
3. Generate test cases covering:
   - Happy path scenarios
   - Edge cases
   - Error conditions
   - Boundary values
4. Write tests using Vitest syntax from templates/test-template.ts
5. Run tests with `bun test` to verify they work
6. Report coverage and suggest additional test cases

## Test Structure

See templates/test-template.ts for the standard format.
Reference examples.md for common testing patterns.

## Version History
- v1.0.0 - Initial release
```

### Example 2: Documentation Reviewer

```yaml
---
name: doc-reviewer
description: Review documentation for clarity, completeness, and accuracy. Use when user asks to review docs, check documentation, or improve README files.
allowed-tools: [Read, Grep, Glob]
---

# Documentation Reviewer

Analyze documentation files for quality and completeness.

## Review Checklist

1. **Structure**: Clear sections, logical flow, table of contents
2. **Completeness**: Installation, usage, examples, API reference
3. **Clarity**: Plain language, defined terms, consistent style
4. **Accuracy**: Working code examples, correct commands, valid links
5. **Accessibility**: Code blocks labeled, alt text for images

## Process

1. Read all documentation files in the project
2. Apply checklist criteria from reference.md
3. Identify gaps and unclear sections
4. Suggest specific improvements with examples
5. Prioritize issues by impact

Reference the style guide in reference.md for writing standards.
```

## Advanced Features

### Tool Restrictions for Security

Use `allowed-tools` to create safe, read-only skills:

```yaml
---
name: code-analyzer
description: Analyze code patterns and suggest improvements
allowed-tools: [Read, Grep, Glob] # No Write, Bash, or other modification tools
---
```

This prevents the skill from making changes, ideal for analysis-only workflows.

### Multi-File Skills

Organize complex skills across multiple files:

```
.claude/skills/data-processor/
├── SKILL.md              # Main instructions
├── reference.md          # API documentation
├── examples.md           # Usage examples
├── scripts/
│   ├── validate.sh       # Validation script
│   └── transform.py      # Data transformation
└── templates/
    ├── report.md         # Report template
    └── config.json       # Config template
```

Reference files in SKILL.md:

```markdown
For API details, see reference.md
For usage examples, see examples.md
Run validation: `bash scripts/validate.sh`
Use report template from templates/report.md
```

## Summary

Creating effective skills requires:

1. **Specific descriptions** with trigger keywords for auto-discovery
2. **Focused scope** addressing one capability well
3. **Clear instructions** with examples and references
4. **Thorough testing** to verify auto-activation works
5. **Team sharing** via plugins or git

Follow this guide to create skills that Claude discovers and uses autonomously, extending capabilities seamlessly based on user needs.

---

**Sources:**

- Claude Code Skills Documentation: https://code.claude.com/docs/en/skills.md
- Slash Commands Comparison: https://code.claude.com/docs/en/slash-commands.md
- Plugin Architecture Reference: https://code.claude.com/docs/en/plugins-reference.md
