---
name: foundations
description: |
  Claude Code basics for new users. Covers essential concepts and commands.
  Use when: user is new to Claude Code or routed here by learning-path assessment.
---

# Foundations: Claude Code Basics

Essential knowledge for getting started with Claude Code.

## Curriculum

| # | Topic | Reference |
|---|-------|-----------|
| 1 | What is Claude Code | `what-is-claude-code.md` |
| 2 | Project instructions with CLAUDE.md | `claude-md-basics.md` |
| 3 | Slash commands | `slash-commands.md` |
| 4 | Using skills | `skills-intro.md` |

## Teaching Pattern

For each topic, follow this flow:

```
1. CONCEPT   → Explain what it is (2-3 sentences)
2. EXAMPLE   → Show real usage
3. EXERCISE  → User tries it themselves
4. VERIFY    → Confirm it worked
```

### Example Flow

**Topic: Slash Commands**

```
CONCEPT:
"Slash commands are shortcuts that trigger specific actions.
Type / to see available commands."

EXAMPLE:
"Try /help — it shows all available commands."

EXERCISE:
"Type /help now and tell me what you see."

VERIFY:
"Great! You should see commands like /clear, /config, etc.
Which one looks interesting to you?"
```

## Topic Details

### 1. What is Claude Code

Key points:
- Claude Code = Claude + file system access + tools
- Can read, write, edit files directly
- Runs in your terminal, sees your project
- NOT a web chat — it's an agentic coding assistant

Reference: `what-is-claude-code.md`

### 2. CLAUDE.md Basics

Key points:
- CLAUDE.md = project instructions Claude always sees
- Put it in project root
- Include: project context, coding style, key files
- Claude reads it automatically on every conversation

Reference: `claude-md-basics.md`

### 3. Slash Commands

Key points:
- `/help` — see all commands
- `/clear` — reset conversation
- `/config` — change settings
- Custom commands from `.claude/commands/`

Reference: `slash-commands.md`

### 4. Skills Intro

Key points:
- Skills = reusable instructions Claude can invoke
- Installed via plugins or created locally
- Triggered by keywords or explicit invocation
- Example: "use the brainstorming skill"

Reference: `skills-intro.md`

## Completion Criteria

User has completed Foundations when they can:

- [ ] Explain what makes Claude Code different from chat Claude
- [ ] Create or edit a CLAUDE.md file
- [ ] Use at least 3 slash commands
- [ ] Invoke a skill by name

## Transition to Intermediate

When complete, offer:
```
"You've got the basics down! Ready for Intermediate?

Next level covers:
- Custom slash commands
- MCP servers for external tools
- Hooks for automation
- Advanced CLAUDE.md patterns

Say 'yes' or /cc:level intermediate to continue."
```
