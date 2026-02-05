---
name: dipeo-frontend-dev
description: Router skill for DiPeO frontend (React, visual editor, GraphQL integration, TypeScript types). Use when task mentions React components, diagram editor, GraphQL hooks, or type errors. For simple tasks, handle directly; for complex work, escalate to dipeo-frontend-dev agent.
allowed-tools: Read, Grep, Glob, Bash, Skill
---

# DiPeO Frontend Dev Router

**Domain**: React components, visual diagram editor (XYFlow), GraphQL integration, TypeScript types in `/apps/web/src/`.

## Quick Decision: Skill or Agent?

### ✅ Handle Directly (This Skill)
- **Simple fixes**: <20 lines, 1-2 files
- **Quick type fixes**: Single TypeScript error in one file
- **Documentation lookups**: "Where is X?", "What hooks are available?"
- **Small styling changes**: Update component layout, add simple UI element
- **Pattern reference**: GraphQL hook usage examples

### ❌ Escalate to Agent
- **TypeScript type fixing**: Multiple related errors, GraphQL schema mismatches, complex generics
- **Feature implementation**: New diagram editor features, multi-step UI workflows
- **Refactoring**: Component hierarchy changes, extracting shared logic
- **Complex debugging**: Runtime errors across components, state synchronization issues

**Agent**: `Task(dipeo-frontend-dev, "your detailed task description")`

## Documentation Sections (Load On-Demand)

Use `Skill(doc-lookup)` with these anchors when you need detailed context:

**Core Responsibilities & Tech Stack**:
- `docs/agents/frontend-development.md#your-core-responsibilities` - React, diagram editor, GraphQL, TypeScript
- `docs/agents/frontend-development.md#technical-context` - Tech stack and project structure

**Code Quality & Patterns**:
- `docs/agents/frontend-development.md#code-quality-standards` - Component patterns, GraphQL, state management
- `docs/agents/frontend-development.md#common-patterns` - Hooks, factory functions, error boundaries

**Constraints & Escalation**:
- `docs/agents/frontend-development.md#important-constraints` - What not to modify
- `docs/agents/frontend-development.md#when-to-escalate` - When to escalate to other agents

**Example doc-lookup call**:
```bash
python .claude/skills/doc-lookup/scripts/section_search.py \
  --query "graphql-usage" \
  --paths docs/agents/frontend-development.md \
  --top 1
```

## Escalation to Other Agents

**To dipeo-backend**: GraphQL schema modifications, server API changes
**To dipeo-codegen-pipeline**: TypeScript model definitions, generated type issues
**To dipeo-package-maintainer**: New node type backend handlers

## Typical Workflow

1. **Assess complexity**: Simple fix vs. complex implementation
2. **If simple**: Load relevant section via `Skill(doc-lookup)`, make change directly
3. **If complex**: Escalate with `Task(dipeo-frontend-dev, "task details")`
4. **Always verify**: Run `pnpm typecheck` before finalizing
