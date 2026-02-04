---
name: julien-dev-claude-md-documenter
version: 1.0.0
description: "Guide for creating CLAUDE.md files. Use when: user asks to create CLAUDE.md, document project, add project instructions, or mentions CLAUDE.md."
category: development
license: Apache-2.0
triggers:
  - "CLAUDE.md"
  - "claude.md"
  - "create CLAUDE.md file"
  - "créer un CLAUDE.md"
  - "document project"
  - "project documentation"
  - "project context"
  - "project instructions"
  - "documenter projet"
  - "documentation projet"
  - "contexte projet"
  - "instructions projet"
  - "create claude"
  - "créer claude"
  - "setup project documentation"
  - "fichier claude.md"
  - "add project context"
---

# CLAUDE.md Documenter

Create effective CLAUDE.md files that give Claude project context without over-documenting.

## What is CLAUDE.md?

A markdown file that Claude automatically loads at the start of every conversation. It provides project context so you don't have to repeat yourself.

**Location:** `./CLAUDE.md` (project root) or `~/.claude/CLAUDE.md` (global)

## Core Principles

### 1. Keep It Short
- **Target:** 50-200 lines
- **Maximum:** 500 lines
- **Why:** Content is prepended to EVERY message (costs tokens)

### 2. Link, Don't Duplicate
```markdown
❌ Don't:
## API Endpoints
POST /api/users - Creates user...
[50 more endpoints]

✅ Do:
## API
See: docs/api.md or visit /api-docs when running
```

### 3. Project-Specific Only
**Include:**
- Unique workflows
- Critical gotchas
- Common commands
- File structure

**Don't include:**
- Code style (use linters)
- General programming knowledge
- Complete API docs (link to them)

## Minimal Template

```markdown
# [Project Name]

[2 sentences: What is this? What problem does it solve?]

## Tech Stack
- [Primary language/framework]
- [3-5 key dependencies]

Full deps: package.json

## Structure
```
app/        # Routes
components/ # UI
lib/        # Utils
```

## Commands
```bash
npm run dev    # Start dev server
npm test       # Run tests
```

All: Run `npm run` or see package.json

## Important
- [Project-specific gotcha #1]
- [Project-specific gotcha #2]

## References
- Architecture: [link]
- Contributing: CONTRIBUTING.md
- Style: .eslintrc
```

## Best Practices

**Source:** [Anthropic Engineering - Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

1. **~150-200 instructions max** - LLMs can follow ~150 instructions reliably
2. **Avoid code style rules** - "Never send an LLM to do a linter's job"
3. **Iterate over time** - Start minimal, add only what Claude misses
4. **Be specific** - "Run `npm test` before commit" > "Test your code"
5. **Provide motivation** - Explain WHY, not just WHAT

## File Locations

```
~/.claude/CLAUDE.md              # Global (lowest priority)
/project/CLAUDE.md                # Project root
/project/packages/api/CLAUDE.md   # Subdirectory (highest priority)
```

Closer to working directory = higher priority.

## Common Mistakes

❌ **Too long** - 1000+ lines nobody reads
❌ **Duplicates docs** - Repeats README, API specs
❌ **Code style rules** - That's what linters are for
❌ **General knowledge** - Claude already knows React basics

## Quick Start

1. Create `CLAUDE.md` in project root
2. Start with the minimal template above
3. Fill in only unique project details
4. Link to existing docs (don't duplicate)
5. Keep under 200 lines

## External Resources

**Official:**
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Using CLAUDE.MD Files](https://www.claude.com/blog/using-claude-md-files)
- [Prompting Best Practices](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)

**Community:**
- [Writing a Good CLAUDE.md - HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [Complete Guide - Sid Bharath](https://www.siddharthbharath.com/claude-code-the-complete-guide/)

**More:** See [references/external-resources.md](references/external-resources.md)

## Usage

When user asks to create/improve a CLAUDE.md:

1. Ask about their project (tech stack, structure, key workflows)
2. Use the minimal template above
3. Fill in only project-specific details
4. Point to existing docs (README, CONTRIBUTING, etc.)
5. Keep it under 200 lines
6. Remind: iterate based on usage

## Skill Chaining

### Skills Required Before
- None (entry point skill)

### Input Expected
- User request to create/improve CLAUDE.md
- Project context (tech stack, structure, workflows)
- Optional: existing CLAUDE.md to improve

### Output Produced
- **Format**: CLAUDE.md file in project root
- **Side effects**: Creates or modifies CLAUDE.md
- **Duration**: 5-10 minutes

### Compatible Skills After
**Recommandés:**
- **julien-dev-tools-skill-creator-pro**: If creating project-specific skills
- Git workflow: Commit the new CLAUDE.md

### Called By
- Direct user invocation: "Create a CLAUDE.md", "Improve my CLAUDE.md"
- New project setup workflows

### Tools Used
- `Read` (usage: read existing CLAUDE.md, README, package.json)
- `Write` (usage: create/update CLAUDE.md)
- `Glob` (usage: discover project structure)

### Visual Workflow

```
User: "Create CLAUDE.md for this project"
    ↓
[THIS SKILL]
    ├─► Ask about project (tech, structure)
    ├─► Use minimal template
    ├─► Fill project-specific details
    ├─► Link to existing docs
    └─► Keep under 200 lines
    ↓
CLAUDE.md created
    ↓
[Optional] Git commit
```

### Usage Example

**Scenario**: Create CLAUDE.md for a React project

**Command**: "Create a CLAUDE.md for this project"

**Result**:
- CLAUDE.md created with ~100 lines
- Tech stack, structure, commands documented
- Links to README, CONTRIBUTING for details

---

**Remember:** The best CLAUDE.md is concise, specific, and links to details instead of duplicating them.
