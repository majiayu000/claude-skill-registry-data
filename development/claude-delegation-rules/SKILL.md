---
name: claude-delegation-rules
description: Rules and patterns for Claude Code agent delegation, including when to delegate, how to hand off context, and how to coordinate between agents. Use when designing agent systems or delegation workflows.
---

# Claude Delegation Rules

This skill provides patterns and rules for effective agent delegation in Claude Code.

## Core Delegation Principles

### 1. Single Responsibility

Each agent should have a clear, focused purpose:

```yaml
# ✅ Good - Clear, focused responsibility
name: code-reviewer
description: Expert code review with comprehensive quality analysis

# ❌ Bad - Too broad
name: developer
description: Does development tasks
```

### 2. Explicit Activation

Agents should know exactly when they should activate:

```yaml
# ✅ Good - Clear activation triggers
description: Senior engineer for implementation tasks. Use PROACTIVELY 
for fix, implement, build, create, add, refactor, optimize keywords.

# ❌ Bad - Vague activation
description: Helps with coding
```

### 3. Clear Boundaries

Define what an agent does and doesn't do:

```markdown
## When to Use
- Implementing new features
- Fixing bugs
- Refactoring code

## When NOT to Use
- High-level architecture decisions (use technical-architecture-advisor)
- UI/UX design (use designer agent)
- Database schema design (use data-architect)
```

## Delegation Patterns

### One-Way Handoff

Agent completes work and hands off to next agent:

```markdown
Senior Engineer
  1. Completes implementation
  2. Documents approach
  3. Hands off to Code Reviewer
     ↓
Code Reviewer
  1. Receives implementation
  2. Performs review
  3. Provides feedback
```

**When to use**: Sequential workflow, clear completion criteria

**Example**:
```markdown
## Delegation Protocol in senior-engineer.md

After implementation:
1. Document changes made
2. Run tests and verify success
3. Create summary for code-reviewer
4. Delegate to code-reviewer with context
5. DO NOT return to implementation unless requested
```

### Consultation Pattern

Agent delegates for advice, then continues work:

```markdown
Senior Engineer
  1. Encounters architectural decision
  2. Delegates to technical-architecture-advisor
  3. Receives architectural guidance
  4. Continues implementation with guidance
```

**When to use**: Specialized knowledge needed, agent continues after consultation

**Example**:
```markdown
## Delegation Protocol in senior-engineer.md

When architectural guidance needed:
1. Identify architectural question
2. Prepare context and specific questions
3. Delegate to technical-architecture-advisor
4. Receive recommendations
5. Incorporate into implementation plan
6. Continue implementation
```

### Parallel Execution

Multiple agents work simultaneously:

```markdown
Orchestrator
  ├─→ Backend Developer (API implementation)
  ├─→ Frontend Developer (UI implementation)
  └─→ Documentation Writer (docs update)
     ↓
  Integration Phase
```

**When to use**: Independent tasks, can run concurrently

**Example**:
```markdown
## Orchestrator Delegation

For feature development:
1. Break down into independent components
2. Delegate backend to senior-engineer-backend
3. Delegate frontend to senior-engineer-frontend
4. Delegate docs to documentation-writer
5. Monitor progress from all agents
6. Coordinate integration when complete
```

### Iterative Refinement

Agent delegates, receives feedback, iterates:

```markdown
Developer
  ↓
Code Reviewer → Feedback
  ↓
Developer (iteration)
  ↓
Code Reviewer → Approval
```

**When to use**: Quality refinement, iterative improvement

## Context Handoff

### What to Pass

**Always include**:
- Purpose of delegation
- Current state/progress
- Specific questions or tasks
- Success criteria
- Relevant files or code
- Constraints or requirements

**Example handoff message**:
```markdown
@technical-architecture-advisor

I need architectural guidance for implementing a caching layer.

**Context**:
- Current system: REST API with PostgreSQL
- Performance issue: N+1 queries on user dashboard
- Load: 10k requests/hour, growing 20% monthly

**Specific Questions**:
1. Should we use Redis or in-memory caching?
2. What caching strategy (write-through, write-back)?
3. How to handle cache invalidation?

**Constraints**:
- Must support horizontal scaling
- Budget: Can add $200/month infrastructure
- Timeline: 2 weeks

**Files**:
- src/api/users.js (current implementation)
- src/database/queries.js (problematic queries)

**Success Criteria**:
- Dashboard load time < 500ms
- Cache hit rate > 80%
- Zero data inconsistencies
```

### What NOT to Pass

- Unnecessary history
- Unrelated code
- Implementation details (unless relevant)
- Personal opinions without context
- Ambiguous requirements

## Agent Coordination

### Shared Context Files

Use shared files for multi-agent workflows:

```markdown
# .plans/feature-implementation.md

## Status: In Progress

## Architecture Review
**Owner**: technical-architecture-advisor
**Status**: ✅ Complete
**Outcome**: Use microservices pattern, see details below

## Implementation
**Owner**: senior-engineer
**Status**: 🔄 In Progress (60%)
**Next Steps**: Complete API endpoints

## Testing
**Owner**: QA agent
**Status**: ⏸️ Waiting for implementation
```

### Communication Protocol

**Starting Delegation**:
```markdown
@agent-name

**Task**: [Clear, specific task]
**Context**: [Essential background]
**Deliverables**: [What you need back]
**Timeline**: [If applicable]
```

**Completing Delegation**:
```markdown
@delegating-agent

**Status**: Complete
**Summary**: [What was done]
**Deliverables**: [Links to files, decisions]
**Next Steps**: [What should happen next]
**Blockers**: [Any issues encountered]
```

## Delegation Anti-Patterns

### ❌ Circular Delegation

```
Agent A → Agent B → Agent C → Agent A  (infinite loop)
```

**Fix**: Clear ownership and final decision maker

### ❌ Over-Delegation

```
Agent delegates every tiny decision
```

**Fix**: Delegate only when specialized expertise needed

### ❌ Under-Context

```
@agent: "Please help"  (no context provided)
```

**Fix**: Provide comprehensive context with every delegation

### ❌ Ambiguous Boundaries

```
Both Agent A and Agent B think they're responsible for task X
```

**Fix**: Document clear responsibility boundaries

## Delegation Decision Tree

```
Does task require specialized expertise?
├─ No → Handle it yourself
└─ Yes → Is the expertise in your domain?
    ├─ Yes → Handle it yourself
    └─ No → Should you learn first or delegate?
        ├─ Learn → Research then handle
        └─ Delegate → Identify appropriate agent
            ↓
        Is agent clearly defined?
        ├─ Yes → Delegate with full context
        └─ No → Create spec for new agent
```

## Agent Configuration Examples

### Proactive Agent

```yaml
---
name: senior-engineer
description: Senior engineer for all development and implementation tasks. 
Use PROACTIVELY for fix, implement, build, create, add, refactor, optimize 
keywords. Delegates to technical-architecture-advisor for architectural concerns.
---
```

### Reactive Agent

```yaml
---
name: technical-architecture-advisor
description: Architecture evaluation and design guidance. Use when requested
for architectural decisions, system design, or when senior-engineer identifies
architectural concerns requiring expert analysis.
---
```

### Coordinator Agent

```yaml
---
name: workflow-orchestrator
description: Coordinates complex multi-step workflows involving multiple agents.
Use when tasks require coordination between specialized agents, parallel work
streams, or complex dependencies.
---
```

## Testing Delegation

Verify delegation works correctly:

1. **Clear Activation**: Agent activates for intended scenarios
2. **Proper Context**: Receives necessary information
3. **Appropriate Delegation**: Delegates to correct agents
4. **No Loops**: No circular delegation patterns
5. **Clean Handoffs**: Clear completion and transitions

## Best Practices Summary

- [ ] Each agent has single, clear responsibility
- [ ] Activation criteria are explicit and testable
- [ ] Delegation triggers are well-defined
- [ ] Context handoff is comprehensive
- [ ] Boundaries between agents are clear
- [ ] Shared state is managed through files
- [ ] Error handling includes delegation paths
- [ ] No circular delegation patterns
- [ ] Performance impact is considered

## Integration Points

This skill informs:
- Agent specification creation
- AGENTS.md documentation
- Workflow design
- Plugin architecture
- Team collaboration patterns
