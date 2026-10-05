---
name: task-coordinator
description: "Coordinate complex multi-step tasks by breaking them down into manageable subtasks with dependency tracking. Covers multi-agent architectural patterns (supervisor, swarm, hierarchical), token economics, and handoff protocols. Use when implementing large features, coordinating parallel work streams, designing multi-agent systems, or managing complex workflows. Turkish triggers: karmaşık işi koordine et, bağımlılık ve durum takibi, çok adımlı teslimatı yönet."
---

# Task Coordinator

Specialized expertise in breaking down complex development tasks into manageable subtasks, coordinating parallel execution, managing dependencies, and ensuring comprehensive completion of multi-step implementations.

## When to Use This Skill

Use this skill for:

- Implementing features that span multiple files/components
- Coordinating work that has sequential dependencies
- Managing parallel development streams
- Breaking down ambiguous or large requirements
- Tracking progress across complex implementations
- Ensuring no steps are missed in multi-phase work

**Trigger phrases**: "coordinate tasks", "multi-step workflow", "complex implementation", "break down", "task dependencies", "parallel work", "large feature", "comprehensive implementation", "multi-agent", "agent handoff", "agent coordination", "orchestrator pattern", "swarm pattern"

## What This Skill Does

Provides structured task management including:

- **Task Decomposition**: Breaking complex work into atomic tasks
- **Dependency Analysis**: Identifying task relationships and ordering
- **Parallel Identification**: Finding tasks that can run concurrently
- **Progress Tracking**: Monitoring completion status
- **Risk Mitigation**: Identifying blockers and alternatives
- **Quality Gates**: Ensuring completion criteria are met

## Instructions

### Step 1: Analyze the Overall Task

Before breaking down work, understand the full scope:

**Discovery Questions**:
1. What is the end goal/deliverable?
2. What systems/components are affected?
3. What are the hard dependencies?
4. What can be parallelized?
5. What are the quality criteria?
6. What could block progress?

**Task Classification**:

| Type | Characteristics | Approach |
|------|-----------------|----------|
| **Feature** | New functionality | Design → Implement → Test → Document |
| **Refactor** | Restructuring | Analyze → Plan → Incremental changes → Verify |
| **Bug Fix** | Defect correction | Reproduce → Root cause → Fix → Regression test |
| **Migration** | System transition | Inventory → Plan → Execute → Validate → Cleanup |

### Step 2: Create Task Breakdown Structure

**Template for Task Decomposition**:

```markdown
## Task: [Main Task Name]

### Phase 1: Foundation
- [ ] Task 1.1: [Description]
  - Dependencies: None
  - Estimated effort: [S/M/L]
  - Files: [list affected files]

- [ ] Task 1.2: [Description]
  - Dependencies: Task 1.1
  - Estimated effort: [S/M/L]
  - Files: [list affected files]

### Phase 2: Core Implementation
- [ ] Task 2.1: [Description] (can run parallel with 2.2)
- [ ] Task 2.2: [Description] (can run parallel with 2.1)
- [ ] Task 2.3: [Description]
  - Dependencies: Tasks 2.1, 2.2

### Phase 3: Integration & Testing
- [ ] Task 3.1: [Description]
- [ ] Task 3.2: [Description]

### Phase 4: Documentation & Cleanup
- [ ] Task 4.1: [Description]
- [ ] Task 4.2: [Description]

### Completion Criteria
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] No regressions
```

### Step 3: Identify Dependencies and Parallelization

**Dependency Types**:

| Type | Description | Example |
|------|-------------|---------|
| **Hard** | Must complete first | DB schema before queries |
| **Soft** | Preferred order | Tests before refactor |
| **Resource** | Shared resource | Same file modifications |
| **External** | Outside control | API availability |

**Dependency Graph Example**:

```
┌─────────┐
│ Task A  │ (Foundation)
└────┬────┘
     │
     ├─────────────────┐
     │                 │
┌────▼────┐      ┌────▼────┐
│ Task B  │      │ Task C  │  (Parallel)
└────┬────┘      └────┬────┘
     │                 │
     └────────┬────────┘
              │
         ┌────▼────┐
         │ Task D  │ (Depends on B and C)
         └────┬────┘
              │
         ┌────▼────┐
         │ Task E  │ (Final)
         └─────────┘
```

**Parallelization Opportunities**:

```markdown
## Parallel Streams

### Stream A: Backend
- [ ] API endpoint implementation
- [ ] Database queries
- [ ] Business logic

### Stream B: Frontend (parallel with Stream A)
- [ ] UI components
- [ ] State management
- [ ] API integration (waits for Stream A)

### Stream C: Testing (parallel with A and B)
- [ ] Test scaffolding
- [ ] Mock data preparation
- [ ] Test implementation (waits for A and B)
```

### Step 4: Execute with Progress Tracking

**Progress Update Template**:

```markdown
## Progress Report: [Task Name]
**Status**: In Progress | Blocked | Complete
**Last Updated**: [Date/Time]

### Completed
- [x] Task 1.1: Foundation setup
- [x] Task 1.2: Database schema

### In Progress
- [ ] Task 2.1: API endpoints (70% complete)
  - Completed: GET, POST endpoints
  - Remaining: PUT, DELETE endpoints

### Blocked
- [ ] Task 2.3: Integration tests
  - Blocker: Waiting for Task 2.1 completion
  - Mitigation: Can prepare test scaffolding

### Not Started
- [ ] Task 3.1: Documentation
- [ ] Task 3.2: Cleanup

### Issues & Risks
1. [Issue description]
   - Impact: [High/Medium/Low]
   - Mitigation: [Action]

### Next Steps
1. Complete Task 2.1 (API endpoints)
2. Unblock Task 2.3 (integration tests)
3. Begin Task 3.1 (documentation)
```

### Step 5: Handle Blockers and Adapt

**Blocker Resolution Framework**:

```markdown
## Blocker Analysis

### Blocker: [Description]

**Type**: Technical | External | Resource | Knowledge

**Impact Assessment**:
- Affected tasks: [List]
- Schedule impact: [Description]
- Risk level: High | Medium | Low

**Resolution Options**:

1. **Option A**: [Description]
   - Pros: [List]
   - Cons: [List]
   - Effort: [S/M/L]

2. **Option B**: [Description]
   - Pros: [List]
   - Cons: [List]
   - Effort: [S/M/L]

**Recommended**: Option [X] because [reasoning]

**Workaround** (if applicable):
- Temporary solution: [Description]
- Tasks that can proceed: [List]
- Cleanup needed later: [Description]
```

### Step 6: Verify Completion

**Completion Checklist**:

```markdown
## Completion Verification

### Functional Requirements
- [ ] All acceptance criteria met
- [ ] Edge cases handled
- [ ] Error handling implemented
- [ ] Performance acceptable

### Code Quality
- [ ] Code follows project standards
- [ ] No linting errors
- [ ] No TypeScript/type errors
- [ ] No console warnings

### Testing
- [ ] Unit tests written and passing
- [ ] Integration tests written and passing
- [ ] Manual testing completed
- [ ] No regressions in existing tests

### Documentation
- [ ] Code comments where needed
- [ ] README updated (if applicable)
- [ ] API documentation updated
- [ ] Architecture decisions documented

### Cleanup
- [ ] No debug code remaining
- [ ] No TODO comments left (or documented)
- [ ] No unused imports/variables
- [ ] Feature flags documented (if used)

### Review
- [ ] Self-review completed
- [ ] Peer review requested
- [ ] Review feedback addressed
```

## Best Practices

- **Start with the end** - Define completion criteria first
- **Small tasks** - Each task should be completable in one session
- **Clear dependencies** - Explicitly document what blocks what
- **Track actively** - Update progress frequently
- **Communicate blockers** - Surface issues early
- **Verify incrementally** - Test after each major task
- **Document decisions** - Record why choices were made
- **Plan for failure** - Have contingency approaches

## Common Patterns

### Pattern 1: Feature Implementation Workflow

```markdown
## Feature: [Name]

### Phase 1: Design (1-2 tasks)
- [ ] Define data models
- [ ] Design API contracts

### Phase 2: Backend (3-5 tasks)
- [ ] Database migrations
- [ ] Repository layer
- [ ] Service layer
- [ ] API endpoints
- [ ] Backend tests

### Phase 3: Frontend (3-5 tasks)
- [ ] UI components
- [ ] State management
- [ ] API integration
- [ ] Frontend tests

### Phase 4: Integration (2-3 tasks)
- [ ] E2E tests
- [ ] Performance testing
- [ ] Security review

### Phase 5: Release (2-3 tasks)
- [ ] Documentation
- [ ] Deployment
- [ ] Monitoring setup
```

### Pattern 2: Refactoring Workflow

```markdown
## Refactor: [Target]

### Phase 1: Preparation
- [ ] Add comprehensive tests for current behavior
- [ ] Document current implementation
- [ ] Identify all usages

### Phase 2: Incremental Changes
- [ ] Change 1: [Small, safe change]
- [ ] Verify: Run tests
- [ ] Change 2: [Next small change]
- [ ] Verify: Run tests
(repeat)

### Phase 3: Cleanup
- [ ] Remove old code
- [ ] Update documentation
- [ ] Final verification
```

### Pattern 3: Bug Fix Workflow

```markdown
## Bug Fix: [Issue]

### Phase 1: Investigation
- [ ] Reproduce the bug
- [ ] Identify root cause
- [ ] Document findings

### Phase 2: Fix
- [ ] Write failing test
- [ ] Implement fix
- [ ] Verify test passes

### Phase 3: Validation
- [ ] Check for similar issues
- [ ] Run regression tests
- [ ] Test edge cases

### Phase 4: Prevention
- [ ] Add monitoring/alerting
- [ ] Document learnings
- [ ] Consider systemic improvements
```

## Multi-Agent Coordination Patterns

When a task is too large or complex for a single agent context window, distribute work across multiple agents. The primary benefit of multi-agent systems is **context isolation**, not role specialization.

### Architectural Patterns

#### Pattern A: Supervisor/Orchestrator

A central agent decomposes tasks and routes them to specialized sub-agents.

```
                ┌──────────────┐
                │  Supervisor  │  (Decomposes, routes, aggregates)
                └──────┬───────┘
           ┌───────────┼───────────┐
     ┌─────▼─────┐ ┌───▼───┐ ┌────▼─────┐
     │  Agent A  │ │ Agent B│ │ Agent C  │
     │ (Research)│ │ (Code) │ │ (Review) │
     └───────────┘ └───────┘ └──────────┘
```

**When to use**: Tasks with clear decomposition, well-defined sub-task boundaries, and a need for centralized quality control.

**Trade-offs**: Strict control and consistent output; but the supervisor becomes a bottleneck and introduces the "telephone game problem" (summaries compound errors across handoffs).

#### Pattern B: Peer-to-Peer / Swarm

Agents communicate directly without a central controller.

**When to use**: Exploratory tasks, parallel research, tasks where each agent can independently contribute results that are later merged.

**Trade-offs**: No single point of failure and high parallelism; but coordination is complex, consensus is harder, and results may be inconsistent.

#### Pattern C: Hierarchical

Layered agents at different abstraction levels: strategy > planning > execution.

**When to use**: Large-scale implementations where high-level decisions guide mid-level planning, which in turn drives low-level execution. Each layer has its own context budget.

**Trade-offs**: Clean separation of concerns and scalable; but increased token cost and latency across layers.

### Token Economics of Multi-Agent Systems

| Configuration | Token Multiplier | When Justified |
|---------------|-----------------|----------------|
| Single-agent chat | 1x baseline | Simple tasks, short sessions |
| Single-agent + tools | 3-5x | Tasks requiring file reads, searches |
| Multi-agent (2-3 agents) | 5-10x | Tasks needing context isolation |
| Multi-agent (5+ agents) | 10-15x | Complex pipelines with specialized agents |

**Rule of thumb**: Only use multi-agent when the context isolation benefit outweighs the token cost. If a single agent can hold all relevant context, prefer that.

### Agent Handoff Protocol

When passing work between agents, use this structured handoff format:

```markdown
## Agent Handoff: [From Agent] → [To Agent]

### Task Summary
[One-sentence description of what the receiving agent should do]

### Context Provided
- Key findings: [Concise list]
- Files modified: [Paths]
- Decisions made: [With rationale]

### Constraints
- Must not modify: [Protected files/systems]
- Must follow: [Patterns, conventions]

### Expected Output
- Deliverable: [What the receiving agent should produce]
- Format: [How to structure the output]

### State
- Completed: [What is done]
- Remaining: [What is left]
```

**Critical guidelines**:
- Pass **structured state**, not raw conversation history
- Each agent should be able to operate with only the handoff document (no implicit context)
- Use file-based handoffs for large state (write findings to a shared file, reference the path)
- Set time-to-live limits to prevent infinite loops between agents

## Integration with Other Skills

When coordinating tasks, invoke related skills at appropriate phases:

| Phase | Related Skills |
|-------|---------------|
| Planning | `plan-before-code`, `context-analysis` |
| Implementation | `code-quality`, language-specific skills |
| Testing | `unit-tests`, `test-cases`, `performance-testing` |
| Security | `security-review`, `dependency-security-audit` |
| Documentation | `technical-documentation`, `api-documentation` |
| Deployment | `cicd-architect`, `kubernetes-expert` |

## Quality Checklist

- [ ] Task breakdown covers all requirements
- [ ] Dependencies explicitly documented
- [ ] Parallel opportunities identified
- [ ] Completion criteria defined
- [ ] Progress tracking mechanism in place
- [ ] Blocker handling planned
- [ ] Integration points identified
- [ ] Testing strategy defined

## Related Skills

- `plan-before-code` - Initial planning methodology
- `context-manager` - Managing information across tasks
- `workflow-orchestrator` - End-to-end workflow management
- `code-quality` - Quality standards for implementations

---

**Version**: 1.1.0
**Last Updated**: February 2026
**Based on**: awesome-claude-code-subagents patterns, project management best practices
**Attribution**: Multi-agent patterns adapted from [Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) (MIT License)


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
