---
name: write-skill
description: "Meta-skill that creates new Claude Code skills. Describe what you want the skill to do and this generates a complete SKILL.md with proper frontmatter, shell injection, structured instructions, and output format."
argument-hint: "[description of the skill to create]"
allowed-tools: Read, Grep, Glob, Write
disable-model-invocation: true
---

# Skill Creator

## Existing Skills (for pattern reference)
!`ls .claude/skills/ 2>/dev/null`

---

## Process

### Step 1: Gather Requirements
From the user's description, determine:
1. **Name**: lowercase-with-hyphens, becomes the `/slash-command`
2. **Purpose**: What does this skill do?
3. **Trigger**: When should someone use it?
4. **Input**: What arguments does it need?
5. **Output**: What should it produce?
6. **Tools needed**: Which Claude Code tools does it require?

### Step 2: Generate SKILL.md

Create the file following this template:

```markdown
---
name: skill-name
description: "One sentence: what it does + when to use it. Be specific enough for auto-invocation."
argument-hint: "[argument description]"
allowed-tools: Read, Grep, Glob
---

# Skill Title

## Context Detection
!`relevant shell command for auto-detecting project context`

---

## Instructions

### Step 1: [First action]
Detailed instructions for what Claude should do.

### Step 2: [Second action]
...

### Step N: [Final action]
...

## Output Format
Describe the expected structure of the output.

## Rules
- Rule 1
- Rule 2
```

### Step 3: Validate the Skill
Check the generated SKILL.md against these requirements:
- [ ] Frontmatter has `name` and `description` (required)
- [ ] Description is under 150 characters and specific
- [ ] `allowed-tools` lists only what's needed (principle of least privilege)
- [ ] Shell injection uses `!`command`` syntax correctly
- [ ] Instructions are numbered steps, not vague paragraphs
- [ ] Output format is defined
- [ ] Rules section exists with boundaries

### Step 4: Save and Test
1. Create directory: `.claude/skills/<skill-name>/`
2. Save `SKILL.md` to that directory
3. Instruct user to test: open Claude Code, type `/<skill-name>`

## Frontmatter Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Slash command name (lowercase, hyphens) |
| `description` | Yes | When to use (specific, <150 chars) |
| `argument-hint` | No | Autocomplete hint, e.g. `[filename]` |
| `allowed-tools` | No | Tools allowed without asking |
| `disable-model-invocation` | No | `true` = manual only |
| `user-invocable` | No | `false` = hidden from menu |
| `model` | No | Override model |
| `effort` | No | `low`, `medium`, `high`, `max` |
| `context` | No | `fork` for subagent isolation |

## Rules
- Follow existing skill patterns in this project
- Keep SKILL.md under 200 lines
- Use shell injection for context detection, not hardcoded assumptions
- Description must be specific enough for Claude to auto-invoke correctly
