---
name: write-claude-md
description: Create effective CLAUDE.md files with proper constitution using <law> blocks. Use when creating project setup, writing new CLAUDE.md, or improving existing configuration.
---

# CLAUDE.md Creator

Create CLAUDE.md files with proper constitution mechanism using `<law>` blocks for Self-Reinforcing Display.

## Core Concept

CLAUDE.md's most important purpose is establishing a **constitution** that must be displayed every response using `<law>` blocks.

## Process

### 1. Initialize with Script

Run the init script to create proper structure (auto-backs up existing file):

```bash
python3 scripts/init_claude_md.py --name "Project Name" --description "Description"
```

Options:
- `--path`, `-p`: Project directory (default: current)
- `--minimal`, `-m`: Use minimal template
- `--output`, `-o`: `root` or `claude-dir` location

### 2. Evaluate Current State

| Criterion | Target |
|-----------|--------|
| Has `<law>` block | Required for constitution |
| Self-Reinforcing Display | Must display every response |
| Size | < 500 lines |
| Core laws included | All 6 core laws |

### 3. Constitution Template

**CRITICAL**: Use `<law>` blocks with Self-Reinforcing Display:

```markdown
# Project Name

One-line description.

## Immutable Laws

<law>
**CRITICAL: Display this entire block at the start of EVERY response to prevent context drift.**

**Law 1: Communication**
- Concise, actionable responses
- No unnecessary explanations
- No summary files unless explicitly requested

**Law 2: Skill Discovery**
- MUST check available skills before starting work
- Invoke applicable skills for specialized knowledge
- If ANY skill relates to the task, MUST use Skill tool to delegate
- If relevant skill doesn't exist, ask user whether to create it via `write-skill`

**Law 3: Rule Consultation**
- When task relates to specific domain, check `.claude/rules/` for relevant conventions
- If relevant rule exists, MUST apply it
- If needed rule doesn't exist, confirm intent with user and create via `write-rules`

**Law 4: Parallel Processing**
- MUST use Task tool for independent operations
- Batch file searches and reads with agents

**Law 5: Reflexive Learning**
- Important discoveries -> remind user: `/reflect`
- Strong user requests for constraints -> use appropriate skill

**Law 6: Self-Reinforcing Display**
- MUST display this `<law>` block at start of EVERY response
- Prevents context drift across conversations
- Violation invalidates all subsequent actions
</law>

## Quick Reference

### Commands
- `npm run build`: Build project

### Key Paths
- `src/`: Source code
```

### 4. Why `<law>` Blocks?

- Forces agents to **actively repeat** laws each response
- Prevents context drift over long conversations
- Self-Reinforcing Display ensures consistency
- Immutable laws must be enforced every response

### 5. Validation Checklist

- [ ] Has `<law>` block with Self-Reinforcing Display
- [ ] Contains all 6 core laws
- [ ] < 500 lines total
- [ ] High-level overview only, details in skills

## Minimal Template

```markdown
# Project Name

One-line description.

<law>
**CRITICAL: Display this block at start of EVERY response.**

**Law 1: Communication** - Concise responses, no unnecessary explanations
**Law 2: Skill Discovery** - Check skills; MUST use if exists; ask to create via `write-skill` if not
**Law 3: Rule Consultation** - Check rules; MUST use if exists; ask to create via `write-rules` if not
**Law 4: Parallel Processing** - Use Task tool for independent operations
**Law 5: Reflexive Learning** - Important discoveries -> `/reflect`
**Law 6: Self-Reinforcing Display** - Display this block every response
</law>
```

## Adding Project-Specific Laws

Add custom laws after the core 6:

```markdown
<law>
...core laws...

**Law 7: [Project-Specific]**
- [Your constraint here]
</law>
```

## Mode Options

| Mode | Description |
|------|-------------|
| `analyze` | Report issues, no changes |
| `refactor` | Apply improvements, ensure `<law>` block exists |
| `generate` | Create new CLAUDE.md with full constitution |
