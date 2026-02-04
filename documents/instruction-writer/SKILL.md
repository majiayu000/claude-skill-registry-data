---
name: instruction-writer
description: Write and optimize instructions for Claude Code (skills, slash commands, memory files, CLAUDE.md). **ALWAYS use before creating or modifying any CLAUDE.md file, SKILL.md file, command file, or instruction documentation.** Triggers when writing skill descriptions, optimizing prompts for clarity/token efficiency, or when user mentions "write a skill", "create a command", "optimize instructions", or "improve this prompt".
---

# Instruction Writer Skill

Expertise in writing effective instructions for Claude Code using latest prompt engineering best practices.

## When to Use This Skill

**MANDATORY** - Automatically invoked when:

- Creating or modifying ANY CLAUDE.md file (project, global, or package-level)
- Creating or modifying SKILL.md files
- Creating or modifying slash command files
- Creating or modifying any instruction/documentation files meant for Claude
- Optimizing prompts for clarity or token efficiency
- User mentions "write instructions", "create a skill/command", or "optimize this prompt"

## Core Principles

Apply all principles from @best-practices.md when writing or optimizing instructions. Key focus areas: clarity & specificity, token efficiency, canonical examples, and actionable steps.

## Workflow

### For New Instructions

1. Understand the purpose and trigger conditions
2. Draft clear, specific description (if skill) or title/purpose (if command)
3. Structure content with headers/XML tags
4. Add canonical examples
5. Review for token efficiency

### For Optimization

1. Read target file first to identify all linked files (@ references)
2. Read all linked files from target
3. Read @best-practices.md for comparison
4. Identify issues: verbosity, unclear structure, weak examples, cross-file redundancy
5. Report findings with before/after examples
6. Wait for approval before applying changes
7. Apply optimizations preserving all salient information

## Supporting Files

- @best-practices.md: Comprehensive prompt engineering guidelines for Claude 4.x
