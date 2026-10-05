---
name: task-router
description: Model routing and subagent delegation patterns. Teaches when to work inline vs spawn subagents, and which model tier + agent type to use.
triggers:
  - delegate
  - spawn
  - agent
  - route
  - subagent
  - task type
---

## Role

Route tasks to the appropriate model tier and execution mode. Most work should happen inline in the main conversation. Spawn subagents only when there's a clear benefit.

## When to Spawn a Subagent

Spawn a subagent via the Task tool ONLY when:
1. **Context isolation** — verbose output that would pollute main context (large codegen, deep search)
2. **Different model tier** — task needs opus reasoning or haiku speed
3. **Parallel work** — multiple independent tasks can run simultaneously
4. **Tool restrictions** — read-only exploration that shouldn't accidentally edit files

For everything else, work inline. Inline is faster (no startup overhead) and cheaper (~4x fewer tokens than a subagent).

## Routing Table

| Task Class | Model | Agent Type | Key Skills to Reference |
|---|---|---|---|
| Quick triage, simple Q&A | haiku | Explore | -- |
| Codebase exploration | haiku | Explore | -- |
| Standard planning, task breakdown | sonnet | general-purpose | planning, arch-core |
| Architecture design, deep research | opus | general-purpose | architecture-design, go-arch, go-api |
| Code implementation | sonnet | general-purpose | go-code |
| Write/fix tests | sonnet | general-purpose | go-test |
| Standard debugging | sonnet | general-purpose | debug-core, go-test |
| Complex debugging (concurrency, perf) | opus | general-purpose | debug-core, go-perf, go-concurrency |
| Code review | opus | Explore | go-review, security-core |
| Acceptance validation | opus | Explore | acceptance |
| API/endpoint testing | sonnet | general-purpose | qa-api |
| Browser E2E testing | sonnet | general-purpose | qa-browser |
| Flutter/mobile testing | sonnet | general-purpose | qa-flutter |
| Performance/load testing | sonnet | general-purpose | qa-performance |
| Visual regression, a11y | sonnet | general-purpose | qa-visual |

## Slim Agents (OpenCode / Named Agents)

For platforms like OpenCode where agent name determines model+tools, use named slim agents instead of ad-hoc routing:

| Agent | Model Tier | Role | Use For |
|---|---|---|---|
| `scout` | fast | research | File search, quick lookup, simple Q&A |
| `coder` | main | execution | Writing, editing, refactoring code |
| `planner` | main | planning | Task breakdown, implementation plans |
| `researcher` | heavy | research | Architecture design, deep codebase analysis |
| `reviewer` | heavy | review | Code review, security audit, quality check |

In OpenCode, reference agents by name: the agent definition in `pkg/agents/meta/` binds the correct model and skills automatically.

## Task Tool Invocation Patterns

### Quick exploration (read-only, fast)
```
Task(model: "haiku", subagent_type: "Explore", prompt: "Find all usages of UserRepository interface in the codebase")
```

### Implementation (needs editing tools)
```
Task(model: "sonnet", subagent_type: "general-purpose", prompt: "Implement the CreateUser use case following Clean Architecture. Domain entity in internal/domain/entity/user.go, repository contract in internal/domain/contract/user.go, use case in internal/usecase/user/create.go")
```

### Deep analysis (needs best reasoning)
```
Task(model: "opus", subagent_type: "general-purpose", prompt: "Design the authentication system architecture. Create design.md with component diagram, layer decisions, data flow, and database schema")
```

### Review (read-only, best reasoning)
```
Task(model: "opus", subagent_type: "Explore", prompt: "Review the changes in internal/usecase/order/ for bugs, security issues, and adherence to Clean Architecture. Only report findings with confidence >= 80%")
```

## Complexity Assessment Signals

**Use haiku (fast)** when:
- Simple lookup, file search, or pattern matching
- Task has a clear, single-step answer
- No reasoning or judgment needed

**Use sonnet (standard)** when:
- Standard implementation following established patterns
- Multi-step but well-defined tasks
- Test writing, standard debugging, planning

**Use opus (heavy)** when:
- Architecture decisions with trade-offs
- Complex debugging (concurrency, performance, multi-component)
- Code review requiring deep reasoning
- Ambiguous requirements needing interpretation

## Decision Flow

```
Is this a quick lookup or search?
  YES → inline (or haiku Explore if large)
  NO ↓

Does this need editing tools?
  YES → sonnet general-purpose (or opus for complex)
  NO → Explore agent type

Is this complex/ambiguous?
  YES → opus
  NO → sonnet (or haiku for trivial)

Can multiple tasks run in parallel?
  YES → spawn separate Task calls
  NO → work sequentially
```
