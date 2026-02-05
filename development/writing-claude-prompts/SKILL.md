---
name: writing-claude-prompts
description: Best practices for writing Claude Code skills, CLAUDE.md files, and prompts optimized for Opus 4.5. Use when creating or reviewing skills, writing agent instructions, or optimizing prompts for Claude 4.x models.
---

# Claude Prompting Best Practices

## Opus 4.5 Behavioral Characteristics

Opus 4.5 has specific behavioral characteristics that affect prompt design:

- **Highly responsive to system prompts** - Emphatic language causes overtriggering
- **Stricter instruction adherence** - Won't infer implied requests; needs explicit direction
- **Sensitive to "think" word** - When extended thinking is disabled, triggers unintended behavior
- **Tendency to over-engineer** - May create extra files, unnecessary abstractions, or unrequested features
- **May skip code exploration** - Can propose solutions without reading relevant files

## Core Principles

### Use Positive Framing

Describe what to do rather than what to avoid. Negative prompting can backfire.

### Soften Emphatic Language

Opus 4.5 overtriggers on emphatic language.

| Avoid                                       | Prefer                               |
| ------------------------------------------- | ------------------------------------ |
| "CRITICAL: You MUST use this tool when..."  | "Use this tool when..."              |
| "ALWAYS call the search function before..." | "Call the search function before..." |
| "You are REQUIRED to..."                    | "You should..."                      |
| "NEVER skip this step"                      | "Don't skip this step"               |
| "**NO** custom test attributes"             | "Don't use custom test attributes"   |

**Exception:** Emphatic language is appropriate for code exploration directives where skipping leads to incorrect solutions based on unread code:

- "Read and understand relevant files before proposing code edits"

### Replace "Think" Variants

When extended thinking is disabled, Opus 4.5 is sensitive to "think."

| Avoid           | Prefer                   |
| --------------- | ------------------------ |
| think about     | consider                 |
| think through   | evaluate                 |
| thinking        | reasoning or considering |
| think carefully | consider carefully       |

### Be Explicit and Specific

Opus 4.5 requires explicit direction. Vague instructions underperform.

```markdown
# Vague (less effective)

- Prioritize simplicity and well-structured code
- Use good architecture patterns

# Explicit (more effective)

- Implement exactly what was requested, nothing more
- Place domain logic in models, external API calls in service objects
- Use Capybara's click_on, fill_in methods with visible text labels
```

### Provide Context and Motivation

Explain _why_ behavior matters to help Claude understand goals:

```markdown
# Without context

- Let code fail loudly on invalid assumptions

# With context (more effective)

- Let code fail loudly on invalid assumptions - this reveals programming
  errors early rather than masking bugs with defensive checks
```

## Skill Structure

### File Naming and Layout

```
skill-name/
├── SKILL.md              # Required - uppercase, contains frontmatter + content
└── references/           # Optional - supporting reference material
    └── reference.md      # Claude reads these only when needed
```

### YAML Frontmatter

```yaml
---
name: skill-name # lowercase, hyphens, max 64 chars
description: What the skill does. Use when [trigger conditions]. Covers [scope].
---
```

**Description requirements:**

- Maximum 1024 characters
- Include BOTH what it does AND when to use it (trigger terms)
- Be specific, not generic

```yaml
# Effective description
description: Guide for writing Ruby and Rails code in this codebase. Use when
implementing features, fixing bugs, refactoring, or reviewing code. Covers
code style, architecture patterns, testing, and Rails conventions.
```

### Skill Naming

- Lowercase letters, numbers, and hyphens only
- Maximum 64 characters
- Specific and descriptive
- Match domain terminology users would search for

### Scope: One Capability Per Skill

A skill should address one focused problem domain. If you need "and/or" or long lists of unrelated capabilities, consider splitting.

Examples of appropriately focused skills:

- "pdf-form-filling"
- "rails-hotwire"
- "customer-support-debugging"

## Content Best Practices

### Use Concrete Examples

Provide working code examples like `StripeService.create_subscription(team, plan)` rather than abstract descriptions like "Use service objects for external API calls."

### Structure with Tables for Reference

Tables make lookup information scannable. Use them for tool references, command options, and comparison matrices.

### Use Step-by-Step Workflows

Explicit numbered steps give clear actions. List the specific sequence of operations to perform.

### Move Reference Content to Separate Files

Keep SKILL.md focused on workflows. Move large reference tables and lookup data to `references/` subdirectory.

## Context Management

### Keep Content Focused

Every token in a skill enters the context window when activated, affecting both cost and performance. Optimize for signal by removing redundant examples, avoiding repetition of standard conventions Claude already knows, and moving lookup tables to reference files.

### Match Prompt Style to Output Style

Formatting in prompts influences response formatting. Use prose paragraphs unless bullet lists are necessary, as this reduces markdown artifacts in responses.

## Anti-Patterns to Avoid

| Anti-Pattern                        | Problem                                | Fix                              |
| ----------------------------------- | -------------------------------------- | -------------------------------- |
| Excessive negative framing          | May cause reverse behavior             | Reframe as positive instructions |
| Emphatic caps (MUST, NEVER, ALWAYS) | Causes overtriggering in Opus 4.5      | Use normal prompting             |
| "Think" and variants                | Triggers extended thinking sensitivity | Use "consider", "evaluate"       |
| Vague philosophical statements      | No actionable guidance                 | Replace with specific patterns   |
| Very broad skill scope              | Unclear when to activate               | Split into focused skills        |
| Lowercase `skill.md`                | May not be discovered                  | Use `SKILL.md` (uppercase)       |
