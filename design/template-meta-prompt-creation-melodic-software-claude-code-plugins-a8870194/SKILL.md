---
name: template-meta-prompt-creation
description: Create Level 6 template meta-prompts that generate other prompts. Use when building prompt generators, designing high-leverage meta-prompts, or creating templates that scaffold other prompts.
allowed-tools: Read, Grep, Glob
---

# Template Meta-Prompt Creation Skill

Create Level 6 template meta-prompts - the highest leverage prompts that generate other prompts.

## Purpose

Build prompts that create other prompts in a specific format. This is the highest leverage prompt engineering pattern.

## When to Use

- Building prompt libraries
- Standardizing team prompt format
- Scaffolding new workflows
- Creating prompt generators

## The Meta-Prompt Pattern

```text
High-Level Description -> [Meta-Prompt] -> New Prompt in Specified Format
```

## Key Components

### 1. Documentation Section

Fetch current documentation for accuracy:

```markdown
## Documentation

Slash Commands: https://docs.anthropic.com/en/docs/claude-code/slash-commands
Settings: https://docs.anthropic.com/en/docs/claude-code/settings
```

**Why:** Ensures generated prompts follow current best practices.

### 2. Template Section (Critical)

The exact format generated prompts should follow:

<!-- markdownlint-disable MD033 MD025 MD003 MD040 -->

```markdown
## Specified Format

```

---

allowed-tools: <tools comma separated>
description: <description for discovery>
argument-hint: [<arguments>]
model: opus
---

# <name_of_prompt>

<prompt purpose - high level description>

## Variables

<NAME_OF_DYNAMIC_VARIABLE>: $1
<NAME_OF_STATIC_VARIABLE>: <STATIC_VALUE>

## Workflow

<numbered list of tasks>

## Report

<output format specification>
```

<!-- markdownlint-enable MD033 MD025 MD003 MD040 -->

**Why:** Consistency across all generated prompts.

### 3. Workflow Section

How to generate the prompt:

```text
## Workflow

- We're building a new prompt to satisfy the HIGH_LEVEL_PROMPT
- Ultra Think - operating a prompt that builds a prompt
- Fetch documentation in parallel with Task tool
- Think through static vs dynamic variables
- Save to .claude/commands/<name>.md
```

## Creation Process

### Step 1: Define Target Format

What should generated prompts look like?

- Which sections are required?
- What frontmatter options?
- What naming conventions?
- Where should prompts be saved?

### Step 2: Create Specified Format Template

Design the exact structure:

```text
## Specified Format

```md
[Your template here with placeholders]
```

Use `<placeholder>` for values the meta-prompt fills in.

### Step 3: Add Documentation Sources

Include relevant documentation URLs:

```markdown
## Documentation

- Source 1: [URL]
- Source 2: [URL]
```

Consider using Task tool for parallel fetching.

### Step 4: Design Meta-Workflow

How does the meta-prompt generate prompts?

```markdown
## Workflow

1. Parse HIGH_LEVEL_PROMPT for requirements
2. Fetch documentation (in parallel if multiple)
3. Design prompt structure
4. Determine variables (dynamic vs static)
5. Create workflow steps
6. Output in Specified Format
7. Save to appropriate location
```

### Step 5: Add Validation

Ensure generated prompts are valid:

```markdown
## Validation

Before outputting:
- [ ] Frontmatter is valid YAML
- [ ] Title is action-oriented
- [ ] Variables use SCREAMING_SNAKE_CASE
- [ ] Workflow has numbered steps
- [ ] Saved to correct location
```

## Complete Example

```markdown
---
allowed-tools: Write, Edit, WebFetch, Task
description: Create a new prompt in specified format
argument-hint: [high level prompt description]
model: opus
---

# MetaPrompt

Based on the HIGH_LEVEL_PROMPT, follow the Workflow to create a new prompt in the Specified Format.

## Variables

HIGH_LEVEL_PROMPT: $ARGUMENTS

## Documentation

Slash Commands: https://docs.anthropic.com/en/docs/claude-code/slash-commands
Settings: https://docs.anthropic.com/en/docs/claude-code/settings

## Workflow

1. Parse HIGH_LEVEL_PROMPT to understand requirements
2. Fetch documentation using Task tool in parallel
3. Design prompt structure based on requirements
4. Determine variables:
   - What inputs from user? (dynamic)
   - What fixed values? (static)
5. Create workflow steps (numbered, sequential)
6. Design output format (Report section)
7. Validate against Specified Format
8. Save to .claude/commands/<kebab-case-name>.md

## Specified Format

<!-- markdownlint-disable MD033 MD025 MD003 MD040 MD024 -->

```text
---

allowed-tools: <tools needed>
description: <clear description>
argument-hint: [<expected args>]
model: opus
---

# <Action-Oriented Title>

<Purpose: 1-2 sentences>

## Variables

<DYNAMIC_VAR>: $1
<STATIC_VAR>: <value>

## Workflow

1. <First step>
2. <Second step>
3. <Third step>

## Report

<Output format>

## Report

Prompt created: .claude/commands/<name>.md
Purpose: <brief description>
Variables: <count> dynamic, <count> static
```

<!-- markdownlint-enable MD033 MD025 MD003 MD040 MD024 -->

## Variations

### Domain-Specific Meta-Prompt

Add domain knowledge to the template:

```markdown
## Domain Context

This meta-prompt creates prompts for [domain]:
- Common patterns: [patterns]
- Required tools: [tools]
- Standard variables: [variables]
```

### Multi-Template Meta-Prompt

Support multiple output formats:

```markdown
## Templates

### Slash Command Template
[template 1]

### Agent Template
[template 2]

## Workflow
1. Determine which template fits
2. Generate using appropriate template
```

## Output Format

When creating a meta-prompt:

```markdown
## Meta-Prompt Design

**Purpose:** Generate [type] prompts

**Target Format:**
- Sections: [list]
- Frontmatter: [fields]
- Output location: [path]

**Documentation Sources:**
- [source 1]
- [source 2]

**Generated:**
[meta-prompt content]
```

## Key Quotes

> "Level six, the template meta prompt, is the most powerful prompt you can write. It's the prompt that creates your other prompts."
>
> "Highest leverage - prompts creating prompts."

## Cross-References

- @seven-levels.md - Level 6 description
- @prompt-sections-reference.md - Template section details
- @prompt-section-design skill - Designing sections

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
