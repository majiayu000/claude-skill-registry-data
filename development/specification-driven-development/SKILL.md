---
name: Specification-Driven Development
description: This skill should be used when the user asks about "spec methodology", "specification workflow", "spec-driven development", "how to write specs", "spec best practices", "specification templates", or needs guidance on creating, validating, decomposing, or executing specifications for software development.
version: 1.0.0
---

# Specification-Driven Development Methodology

A systematic approach to software development that starts with comprehensive specifications before implementation.

## Workflow Overview

The spec workflow consists of four phases:

```
/spec:create -> /spec:validate -> /spec:decompose -> /spec:execute
```

### Phase 1: Create (`/spec:create`)

Generate a comprehensive specification document using first-principles thinking:

1. **Problem Analysis**: Strip away solution assumptions, identify root cause
2. **Validation**: Confirm real user need, audit assumptions
3. **Technical Discovery**: Search codebase, identify conflicts/dependencies
4. **Specification Writing**: 17-section template covering all aspects

**When to use**: Starting any non-trivial feature or bugfix

### Phase 2: Validate (`/spec:validate`)

Analyze the specification for completeness and detect overengineering:

1. **WHY Analysis**: Intent, goals, success criteria
2. **WHAT Analysis**: Scope, requirements, deliverables
3. **HOW Analysis**: Implementation details, error handling, testing
4. **YAGNI Check**: Cut unnecessary features aggressively

**When to use**: Before decomposing, after major spec revisions

### Phase 3: Decompose (`/spec:decompose`)

Break the validated spec into actionable implementation tasks:

1. **Task Breakdown**: Single-objective tasks with clear acceptance criteria
2. **Dependency Mapping**: Identify blocking vs parallel work
3. **Content Preservation**: Copy ALL details, don't summarize
4. **Task Management**: Create in STM or TodoWrite

**When to use**: After spec passes validation

### Phase 4: Execute (`/spec:execute`)

Implement using orchestrated specialist agents:

1. **Implement**: Launch domain expert agents
2. **Test**: Write comprehensive tests
3. **Review**: Code review for completeness AND quality
4. **Fix**: Address issues before marking complete
5. **Commit**: Atomic commits per task

**When to use**: After decomposition creates tasks

## Key Principles

### First Principles Problem Analysis

Before any solution, validate the problem:

- What is the core problem separate from solutions?
- Why does this problem exist?
- What would success look like with unlimited resources?
- Could we solve this without building anything?

### YAGNI (You Aren't Gonna Need It)

Be aggressive about cutting scope:

- Unsure if needed? Cut it
- For "future flexibility"? Cut it
- Only 20% of users need it? Cut it
- Adds complexity? Question it, probably cut it

### Content Preservation

When creating tasks from specs:

- COPY implementation details verbatim
- Include complete code examples
- Never write "as specified in spec"
- Each task must be self-contained

### Quality Gates

Each phase has validation checkpoints:

- Specs require 8+/10 quality score
- Tasks require code review approval
- Implementation requires all tests passing

## Integration with Task Management

### STM (Session Task Manager)

If installed, provides persistent task tracking:

```bash
stm init                      # Initialize
stm add "Task" --details "..." # Create task
stm list --pretty             # View tasks
stm update [id] --status done # Complete task
```

### TodoWrite (Fallback)

Built-in session task tracking when STM unavailable.

## See Also

- [references/spec-template.md](references/spec-template.md) - Full 17-section specification template
- [references/overengineering-patterns.md](references/overengineering-patterns.md) - Common patterns to avoid
