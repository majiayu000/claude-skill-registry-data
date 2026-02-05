---
name: claude-code-skill-expert
description: Expert guidance for creating high-quality Claude Code skills following Anthropic's official best practices. Use when creating, improving, or auditing skill files.
---

# Claude Code Skill Expert

Guide for creating effective, well-structured Claude Code skills that follow Anthropic's official best practices.

## When to Use This Skill

- Creating a new SKILL.md file
- Improving an existing skill's structure or effectiveness
- Auditing a skill for token efficiency
- Troubleshooting why a skill isn't being triggered
- Optimizing skill context usage

---

## Core Principles

### 1. Progressive Disclosure (CRITICAL)

Structure skills as a **table of contents** where Claude loads content on-demand:

- **Metadata** (name + description) loads at startup
- **SKILL.md** loads when triggered
- **Reference files** load only as needed

**Pattern**: Keep SKILL.md under 500 lines. Move detailed content to separate reference files.

**Example**:
```markdown
## Step 1: Analyze Code

Run the analyzer: `bun run analyzer.ts`

**Output**: See [output-templates.md#analysis](references/output-templates.md#analysis) for format
```

### 2. Name and Description Quality

**The most critical fields** - Claude uses these to decide when to trigger the skill.

**Good description**:
```yaml
description: Books cinema tickets at Classic Cinemas. Use when Nathan asks to book tickets, see movies showing, or get cinema seats.
```

**Bad description**:
```yaml
description: A helpful skill for booking things
```

**Rules**:
- Include **what** the skill does
- Include **when** to use it (trigger phrases)
- Use third person ("Books tickets" not "I book tickets")
- Max 1024 characters
- Include key terms users would mention

### 3. File Organization

**One-level-deep references** from SKILL.md:

```
skill/
├── SKILL.md              # Overview, workflow steps
└── references/
    ├── templates.md      # Output formats
    ├── commands.md       # CLI reference
    └── errors.md         # Error recovery
```

**Don't do**:
```
skill/
├── SKILL.md
└── references/
    ├── advanced/
    │   └── deep-file.md  # Too deep!
```

---

## SKILL.md Structure

### Recommended Format

```markdown
---
name: my-skill
description: What it does and when to use it
allowed-tools: Bash, Read, Write
model: claude-sonnet-4-5
---

# Skill Title

Brief introduction explaining purpose.

## Workflow Overview

[Optional: Visual diagram of steps]

## Step 1: First Action

**Action**: What to do

**Command/Tool**: Specific tool or bash command

**Output**: Template reference or inline format

**Wait for**: User response or validation

---

## Step 2: Second Action

[Continue pattern...]

---

## References

- [Templates](references/templates.md) - Exact output formats
- [Commands](references/commands.md) - CLI reference
- [Errors](references/errors.md) - Recovery patterns
```

### Key Elements

1. **Workflow clarity**: Numbered steps with clear actions
2. **Template references**: Link to exact formats
3. **Validation checkpoints**: Where to wait for user confirmation
4. **Progressive disclosure**: "See X for details" instead of inline detail

---

## Output Templates Best Practice

**CRITICAL**: Create a separate `references/output-templates.md` file with **exact copy-paste formats**.

### Template File Structure

```markdown
# Output Templates

**CRITICAL**: Use these exact templates. Copy the structure precisely.

---

## Template Name

**ALWAYS use this exact format**:

\`\`\`
[Exact format with placeholders]
\`\`\`

**Rules**:
- Specific formatting requirements
- What to show/hide
- How to handle edge cases

**Mapping from data**:
\`\`\`
field_name → [PLACEHOLDER]
nested.field → [OTHER_PLACEHOLDER]
\`\`\`

**Example**:
\`\`\`
[Concrete example with real data]
\`\`\`
```

### Why This Works

- **Strictness levels**: "ALWAYS use this exact format" vs "use your best judgment"
- **Visual examples**: Claude sees the desired output structure
- **Mapping clarity**: Links data sources to placeholders
- **Progressive disclosure**: Loaded only when needed for that step

---

## Common Patterns

### 1. Conditional Workflow Pattern

```markdown
## Step 2: Choose Path

**If** creating new content → Go to Step 3
**If** editing existing → Go to Step 5
```

### 2. Validation Loop Pattern

```markdown
## Step 4: Validate

Run validator → identify errors → fix → repeat until passing

**See**: [error-handling.md#validation](references/error-handling.md#validation)
```

### 3. Tool Selection Pattern

```markdown
## Step 1: Analyze Request

**Use**:
- `kit_grep` for literal text search
- `kit_semantic` for "find where we handle X"
- `kit_symbols` for function definitions

**See**: [tool-selection.md](references/tool-selection.md) for full decision tree
```

### 4. High-Level Guide with References

```markdown
# My Skill

Keep SKILL.md as overview.

**Resources**:
- [Forms](references/forms.md) - Advanced form handling
- [API](references/api.md) - API details
- [Examples](references/examples.md) - Concrete examples
```

---

## Token Efficiency Strategies

### 1. Split Mutually Exclusive Content

If certain contexts are rarely used together, keep paths separate:

```
references/
├── create-workflow.md    # Only for creating new items
└── edit-workflow.md      # Only for editing existing
```

### 2. Use Code for Deterministic Operations

Scripts **don't load into context** - only their output does.

**Efficient**:
```bash
bun run extract-fields.ts  # Code not in context
```

**Inefficient**:
```markdown
Parse the JSON manually and extract these 20 fields...
[20 lines of parsing instructions]
```

### 3. Table of Contents for Long References

For files >100 lines:

```markdown
# Long Reference File

## Contents
- [Section 1](#section-1)
- [Section 2](#section-2)

## Section 1
...
```

---

## Troubleshooting

### Skill Not Triggering

**Likely causes**:
1. Description doesn't match user's language
2. Name is too generic or doesn't convey purpose
3. Missing key trigger phrases

**Fix**: Add trigger phrases to description: "Use when users ask about X, need to Y, or mention Z"

### Skill Over-Triggers

**Likely causes**:
1. Description too broad
2. Missing constraints

**Fix**: Narrow description with specific scenarios

### Token Bloat

**Likely causes**:
1. Everything in SKILL.md
2. Templates inline instead of referenced
3. No progressive disclosure

**Fix**: Move details to reference files, use "See X" pattern

### Inconsistent Output

**Likely causes**:
1. No explicit templates
2. Vague formatting instructions
3. Missing examples

**Fix**: Create `output-templates.md` with exact formats and examples

---

## Quality Checklist

Before considering a skill complete:

- [ ] Name is gerund form (e.g., `processing-pdfs`)
- [ ] Description includes what + when to use
- [ ] SKILL.md under 500 lines
- [ ] Templates in separate file with exact formats
- [ ] One-level-deep references
- [ ] Clear numbered workflow steps
- [ ] Validation checkpoints defined
- [ ] Error handling documented
- [ ] Examples provided
- [ ] No nested subdirectories

---

## Official Resources

- [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude 4 Prompting Guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Equipping Agents for the Real World](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

---

## Example: Well-Structured Skill

See `the-cinema-bandit` plugin's ticket-booking skill for a production example:

```
skills/ticket-booking/
├── SKILL.md (127 lines)          # Lean workflow
└── references/
    ├── output-templates.md        # Strict formats
    ├── cli-commands.md            # CLI reference
    └── error-handling.md          # Recovery patterns
```

**Key features**:
- Progressive disclosure (47% smaller than original)
- Exact output templates with examples
- Clear action → output → wait pattern
- Visual workflow diagram
- Reference files loaded on-demand
