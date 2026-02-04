---
name: sdd-development
description: "Specification-Driven Development (SDD) methodology for building software where specifications are executable and drive code generation. Use when users want to: (1) Create feature specifications with /speckit.specify, (2) Generate implementation plans with /speckit.plan, (3) Create executable tasks with /speckit.tasks, (4) Follow test-first, library-first development, or (5) Implement constitutional architecture principles. Essential for structured AI-assisted development workflows."
---

# Specification-Driven Development (SDD)

## Overview

SDD reverses traditional development: specifications become the source of truth, and code becomes their generated expression. This skill provides the workflow, templates, and validation tools for specification-driven development.

## Core Workflow

### 1. Create Feature Specification (`/speckit.specify`)

Generate a complete, structured feature specification:

```bash
/speckit.specify [feature description]
```

This command:
- Scans existing specs to determine next feature number (001, 002, etc.)
- Creates a semantic branch name from the description
- Generates spec from template at `specs/[branch-name]/spec.md`
- Creates proper directory structure
- Marks ambiguities with [NEEDS CLARIFICATION] tags

**Template location:** Use `assets/spec-template.md` as the base structure.

**Key principles:**
- Focus on WHAT and WHY, not HOW
- Include user stories with acceptance criteria
- Mark all ambiguities explicitly
- No technical implementation details at this stage

### 2. Generate Implementation Plan (`/speckit.plan`)

Create a comprehensive technical plan from the specification:

```bash
/speckit.plan [technical approach notes]
```

This command:
- Reads the feature specification
- Applies constitutional principles (see `references/constitution.md`)
- Generates technical architecture and implementation details
- Creates supporting documents (data-model.md, contracts/, research.md)
- Includes quickstart validation scenarios

**Template location:** Use `assets/plan-template.md` as the base structure.

**Constitutional gates enforced:**
- Library-First Principle (Article I)
- CLI Interface Mandate (Article II)
- Test-First Imperative (Article III)
- Simplicity Gates (Article VII)
- Anti-Abstraction Gates (Article VIII)
- Integration-First Testing (Article IX)

### 3. Generate Executable Tasks (`/speckit.tasks`)

Derive actionable tasks from the implementation plan:

```bash
/speckit.tasks
```

This command:
- Reads plan.md and supporting documents
- Converts contracts, entities, and scenarios into tasks
- Marks parallelizable tasks with [P]
- Outputs tasks.md ready for execution

**Input files analyzed:**
- plan.md (required)
- data-model.md (if exists)
- contracts/ (if exists)
- research.md (if exists)

## File Structure

A complete SDD feature creates:

```
specs/
└── [branch-name]/
    ├── spec.md           # Feature specification (WHAT/WHY)
    ├── plan.md           # Implementation plan (HOW)
    ├── data-model.md     # Entity schemas
    ├── contracts/        # API contracts, WebSocket events
    ├── research.md       # Technical research and comparisons
    ├── quickstart.md     # Key validation scenarios
    └── tasks.md          # Executable task list
```

## Constitutional Principles

The SDD workflow enforces nine architectural principles. Before generating any implementation plan, read `references/constitution.md` to understand:

1. **Article I: Library-First Principle** - Every feature starts as a standalone library
2. **Article II: CLI Interface Mandate** - All functionality must be CLI-accessible
3. **Article III: Test-First Imperative** - No code without approved tests
4. **Article VII: Simplicity** - Maximize simplicity, ≤3 projects initially
5. **Article VIII: Anti-Abstraction** - Trust frameworks, avoid premature abstraction
6. **Article IX: Integration-First** - Test with real services, not mocks

## Validation

Before code generation, validate specifications using:

```bash
python scripts/validate_spec.py specs/[branch-name]/
```

This checks for:
- Remaining [NEEDS CLARIFICATION] tags
- Missing required sections
- Testability of acceptance criteria
- Constitutional compliance in plans

## Templates and Assets

- `assets/spec-template.md` - Feature specification template
- `assets/plan-template.md` - Implementation plan template
- `references/constitution.md` - Full constitutional articles with examples

## Best Practices

**Specification Phase:**
- Start with user intent, not technical solutions
- Mark every ambiguity explicitly
- Include measurable acceptance criteria
- Avoid implementation details

**Planning Phase:**
- Reference constitution gates before generating plans
- Document technical choices with rationale
- Create contracts before implementation
- Define test scenarios from acceptance criteria

**Task Generation:**
- Ensure tasks map to specific contracts or entities
- Mark truly parallelizable work
- Include both implementation and test tasks
- Sequence dependencies clearly

## Example: Real-Time Chat Feature

```bash
# Step 1: Create specification
/speckit.specify Real-time chat system with message history and user online status

# Creates: specs/003-chat-system/spec.md
# Includes: User stories, acceptance criteria, non-functional requirements

# Step 2: Generate plan
/speckit.plan Using WebSocket for real-time messaging, PostgreSQL for history, Redis for presence

# Creates: specs/003-chat-system/plan.md, data-model.md, contracts/, research.md, quickstart.md

# Step 3: Generate tasks
/speckit.tasks

# Creates: specs/003-chat-system/tasks.md with concrete, executable tasks
```

## Progressive Disclosure

For detailed examples and patterns, see:
- `references/constitution.md` - Complete constitutional framework
- `assets/spec-template.md` - Full specification structure
- `assets/plan-template.md` - Full implementation plan structure

Read these files as needed during the workflow to ensure compliance and quality.
