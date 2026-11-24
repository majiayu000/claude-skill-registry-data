---
name: superpowers
title: Superpowers - AI-Assisted Development Workflows
description: Comprehensive skill framework from obra/superpowers for AI-assisted development workflows, covering planning, implementation, debugging, code review, and more
tags: workflow, ai-agent, development, planning, debugging, code-review, tdd
source: https://github.com/obra/superpowers
---

# Superpowers

A comprehensive skill framework for AI-assisted development workflows, integrated from [obra/superpowers](https://github.com/obra/superpowers).

## Overview

Superpowers provides a complete set of skills that guide AI agents through the entire software development lifecycle. These skills are designed to work together as an integrated workflow, from initial design exploration to final code review and completion.

## Skills Included

### Planning & Design
- [brainstorming](brainstorming/SKILL.md) - Design exploration before implementation
- [writing-plans](writing-plans/SKILL.md) - Implementation plan creation with bite-sized tasks

### Implementation
- [executing-plans](executing-plans/SKILL.md) - Execute implementation plans with review checkpoints
- [subagent-driven-development](subagent-driven-development/SKILL.md) - Subagent-based development workflow
- [test-driven-development](test-driven-development/SKILL.md) - TDD methodology and practices

### Collaboration
- [dispatching-parallel-agents](dispatching-parallel-agents/SKILL.md) - Parallel task execution for independent work
- [receiving-code-review](receiving-code-review/SKILL.md) - Handling code review feedback with technical rigor
- [requesting-code-review](requesting-code-review/SKILL.md) - Requesting and managing code reviews

### Quality Assurance
- [systematic-debugging](systematic-debugging/SKILL.md) - Systematic approach to debugging
- [verification-before-completion](verification-before-completion/SKILL.md) - Pre-completion verification requirements

### Workflow Management
- [finishing-a-development-branch](finishing-a-development-branch/SKILL.md) - Branch completion and integration
- [using-git-worktrees](using-git-worktrees/SKILL.md) - Git worktree management for isolation

### Skill Management
- [using-superpowers](using-superpowers/SKILL.md) - Skill discovery and usage patterns
- [writing-skills](writing-skills/SKILL.md) - Creating and editing skills

## Recommended Workflow

1. **Start**: Use `using-superpowers` to understand skill discovery
2. **Explore**: Use `brainstorming` for design exploration
3. **Plan**: Create implementation plans with `writing-plans`
4. **Execute**: Implement using `executing-plans` or `subagent-driven-development`
5. **Test**: Follow `test-driven-development` practices
6. **Debug**: Use `systematic-debugging` when issues arise
7. **Review**: Request and receive code reviews
8. **Complete**: Verify with `verification-before-completion` and finish with `finishing-a-development-branch`

## Integration Notes

These skills are stored as a collection in the `superpowers/` directory. They are designed for direct reference and integration into AI agent workflows, providing structured guidance for complex development tasks.

Each skill includes detailed instructions, checklists, and examples to ensure consistent and high-quality development practices.
