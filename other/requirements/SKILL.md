---
name: requirements
description: "/requirements - Define Feature Requirements"
---

# /requirements - Define Feature Requirements

Guide through Jobs-to-be-Done discovery to define well-structured feature requirements before implementation.

## What This Skill Does

Invokes the `define-requirements` skill which:

1. **Problem Definition** - Interviews to understand the problem being solved
2. **JTBD Interview** - Maps functional jobs users need to accomplish
3. **Codebase Analysis** - Deep analysis of implementation impact
4. **Implementation Plan** - TDD-focused recommendations
5. **GitHub Issue Handoff** - Prepares everything for issue creation

---

## Workflow

When invoked, immediately activate the `define-requirements` skill.

The skill will guide through:

1. Problem definition questions (one at a time)
2. Jobs-to-be-Done mapping
3. Checkpoint to confirm understanding
4. Read CLAUDE.md for project conventions
5. Comprehensive codebase analysis
6. TDD implementation recommendations
7. Final summary checkpoint
8. Handoff to github-issue-creator skill

---

## When to Use

- Before implementing a new feature
- When planning significant enhancements
- To create well-structured GitHub issues
- When you need clarity on what to build

---

## Example

```
User: /requirements

Claude: *Invokes define-requirements skill*

"What problem are you trying to solve? Describe what's not working or what's missing today."
```
