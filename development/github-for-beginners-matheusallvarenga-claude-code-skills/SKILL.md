---
name: GitHub for Beginners
description: This skill provides comprehensive guidance for learning and using GitHub, from fundamental concepts through practical workflows. Designed for complete beginners, this skill should be used when teaching GitHub concepts, explaining git workflows, debugging git/GitHub issues, or guiding through practical GitHub tasks like creating branches, commits, pull requests, and merging code.
---

# GitHub for Beginners - Complete Learning Skill

## Purpose

This skill transforms GitHub novices into self-sufficient users by providing clear explanations, practical commands, and solutions to common problems. It covers everything from foundational concepts through advanced workflows, evolving with the user's skill level.

## When to Use This Skill

Use this skill when:

- **Teaching Concepts**: Explaining Git, GitHub, branches, commits, PRs, or other core concepts
- **Guiding Workflows**: Helping users execute practical tasks (creating PRs, merging branches, etc.)
- **Debugging Problems**: Troubleshooting merge conflicts, undoing changes, or other errors
- **Answering Questions**: Clarifying what something means or why it works that way
- **Best Practices**: Advising on conventional workflows and standards

## How to Use This Skill

All procedural knowledge is organized in reference files for easy lookup and context management:

### Core References

**`references/git-basics.md`** - Foundational concepts and mental models
- Understanding Git vs GitHub distinction
- Key concepts: repositories, commits, branches, remotes
- Mental models and analogies for abstract ideas
- Philosophy and why these patterns exist

**`references/commands-reference.md`** - Complete command dictionary
- Organized by workflow and frequency of use
- Every command includes: what it does, common variations, when to use it
- Covers setup, daily work, branching, merging, undoing changes
- Examples for each command

**`references/workflows.md`** - Step-by-step procedures for common tasks
- Complete workflows for: making your first commit, creating a PR, merging code, etc.
- Multi-step processes broken down with explanations
- Integration with Claude Code workflow (since the user has this setup)
- Collaboration patterns and team workflows

**`references/troubleshooting.md`** - Common problems and solutions
- Organized by problem category (merge conflicts, undo operations, permission issues, etc.)
- Diagnostic questions to identify the problem
- Step-by-step solutions with explanations
- Prevention tips for future

**`references/claude-code-integration.md`** - GitHub + Claude Code
- How Claude Code works with GitHub (the user's current setup)
- Using @claude in issues and PRs
- Workflow for collaborative development with Claude Code
- Best practices for the GitHub App integration

### Using These References

When responding to a user question:

1. **Assess the question** - Determine which reference(s) contain relevant information
2. **Load references** - Read the appropriate sections from the reference files
3. **Apply knowledge** - Use the structured information to answer clearly
4. **Provide examples** - Give practical examples from commands-reference when relevant
5. **Connect concepts** - Link back to foundational understanding from git-basics

## Progressive Learning Path

The skill is designed for progression:

### Level 1: Novice (Current)
- Understanding core concepts
- Making first commit
- Creating branches
- Opening first PR
- Basic troubleshooting

### Level 2: Intermediate (Next)
- Advanced merge strategies
- Rebasing workflows
- Stashing and cleaning
- Complex troubleshooting
- Collaborating with teams

### Level 3: Advanced (Future)
- Advanced git workflows (gitflow, trunk-based)
- Performance optimization
- Custom git hooks
- Repository maintenance
- Mentoring others

## Key Principles

**Clarity Over Completeness**: Explain concepts clearly rather than covering every edge case upfront.

**Practical First**: Lead with practical examples and real commands before diving into theory.

**Progressive Disclosure**: Build knowledge layer by layer, not overwhelming with information.

**Student-Centered**: Acknowledge the user's current level and guide them appropriately.

**References as Sources of Truth**: Maintain detailed information in references for future expansion and reference.
