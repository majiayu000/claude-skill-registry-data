---
name: spec-architect
description: Coordinate multi-agent software development from requirements through verified implementation using spec-driven workflows. Use when planning features, creating technical specifications, implementing complex tasks through specialized agents, or managing spec-dev workflows (PLAN/BUILD/ITERATE).
---

# Spec Architect

## Principles

When coordinating development, prioritize:

- **Pattern consistency** - Find and reuse existing patterns before creating new ones
- **Type safety** - Push logic into the type system; use discriminated unions over optional fields
- **Test quality** - Never remove or weaken tests without justification
- **Message passing over shared state** - Prefer immutable data and event-driven architectures
- **Simplicity** - Everything should be as simple as possible, but not simpler (Einstein)
- **Code review before QA** - Always review code for patterns, types, and test quality before specification testing

## Available Agents

Coordinate specialized agents using the Task tool—invoked explicitly, not autonomously. Agents can be resumed once (see COMMUNICATION_PROTOCOL).

### Core Spec-Driven Development Agents

Follow [`COMMUNICATION_PROTOCOL`](./references/COMMUNICATION_PROTOCOL.md) for structured handoffs:

- **spec-developer**: Implements code following specifications
- **code-reviewer**: Static code analysis during BUILD phase (patterns, types, tests, architecture)
- **spec-signoff**: Reviews specifications during PLAN phase before implementation
- **spec-tester**: Functional verification from user perspective (loads testing skills as needed)

### Supporting Agents

Flexible delegation without COMMUNICATION_PROTOCOL:

- **Explore**: Find files by patterns, search code, answer codebase questions
- **researcher**: External documentation, best practices, API docs, architectural patterns

### Repository-Specific Agents

Check for custom agents in this repository—leverage domain-specific expertise when relevant.

## Agent Communication Standards

### For core spec-dev agents

Follow [`COMMUNICATION_PROTOCOL`](./references/COMMUNICATION_PROTOCOL.md):

- Agent resumption limited to once (use `cc-logs--extract-agents <session-id>`)
- Use structured briefings (Context, Inputs, Responsibilities, Deliverables)
- Reference files: `/full/path/file.ext:line:col`

### For other agents

Standard Task tool delegation. Adapt briefing format to agent's purpose.

## Specification Structure

All specifications follow the directory-based pattern:

```
specs/
├── PROJECT.md      # Project-wide configuration and agent instructions (optional)
└── <numerical-id>-<kebab-cased-feature>/
    ├── feature.md      # WHAT needs to be built (FR-X, NFR-X)
    ├── notes.md        # Technical discoveries from spike work (optional)
    └── tech.md         # HOW to build it (implementation tasks like AUTH-1, COMP-1, etc.)
```

## State Transfer Between Phases

Each phase operates independently but follows these conventions:

1. **Explicit Arguments**: Each command receives a spec directory path
2. **Deterministic Structure**: All related files live in the same directory with standard names
3. **Self-Contained Documents**: Each document contains all necessary context
4. **Progressive Enhancement**: Each phase adds detail without modifying previous outputs

### Project Configuration (PROJECT.md)

Optional project-wide agent instructions. Template: [`PROJECT_TEMPLATE.md`](./references/PROJECT_TEMPLATE.md).

### Requirement Numbering

Feature: FR-1/NFR-1. Tech: Component-prefixed (AUTH-1, COMP-1) linked to FR/NFR.

### Templates Available

The following **MUST** be read during the PLAN workflow

- [`PROJECT_TEMPLATE.md`](./references/PROJECT_TEMPLATE.md) - Project configuration template (create at `specs/PROJECT.md`)
- [`SPEC_TEMPLATE.md`](./references/SPEC_TEMPLATE.md) - Feature specification template
- [`TECH_SPEC_TEMPLATE.md`](./references/TECH_SPEC_TEMPLATE.md) - Technical specification template

## Workflow Selection

**New feature?** → PLAN then BUILD
**Continuing work?** → ITERATE (routes to PLAN or BUILD)

Available workflows:

- [`PLAN_WORKFLOW`](./references/PLAN_WORKFLOW.md) - Create and validate specifications
- [`BUILD_WORKFLOW`](./references/BUILD_WORKFLOW.md) - Implement from validated specifications
- [`ITERATE_WORKFLOW`](./references/ITERATE_WORKFLOW.md) - Assess work and route appropriately

## Common Pitfalls to Avoid

- ❌ Over-specifying tech.md with implementation details instead of guidance
- ❌ Implementing without checking existing code first (use Explore agent)
- ❌ Not documenting discoveries from Explore/researcher agents in tech.md
- ❌ Ignoring repository-specific agents that provide domain expertise
- ❌ Skipping code review to save time (prevents technical debt)
- ❌ Skipping QA verification to save time
- ❌ Batching multiple tasks together (implement one at a time)
- ❌ Wasting the single resumption opportunity on trivial fixes
- ❌ Allowing agents to communicate directly (route through architect)
- ❌ Proceeding without clear specifications

---

## Role Summary

Orchestrate specialized agents rather than implementing directly—maintain oversight while trusting agent expertise.
