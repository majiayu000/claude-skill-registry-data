---
name: request-optimizer
version: 2.0.0
description: Intelligent request analysis and routing system. Analyzes incoming requests, calculates complexity, and routes to appropriate resources (27 agents, 27 skills, 14 MCPs). Acts as the gateway for the entire Claude Code ecosystem with future integration to LimitlessAgent.
context: fork
---

# Request Optimizer v2.0

## Purpose

Intelligent gateway that intercepts and analyzes every user request, providing strategic recommendations before execution. This skill orchestrates the entire Claude Code ecosystem by:

- Calculating task complexity (0.0 - 1.0)
- Routing to appropriate agents (27 available)
- Activating relevant skills (27 available)
- Coordinating MCPs (14 available)
- Selecting optimal model (Haiku/Sonnet/Opus)
- Preparing for future LimitlessAgent integration

## When to Use

This skill should be used automatically on every non-trivial request to:

1. **Analyze** request specificity and clarity
2. **Score** complexity using weighted factors
3. **Route** to appropriate resources
4. **Recommend** execution strategy
5. **Get approval** before heavy operations
6. **Execute** and report results

## Architecture

```
USER REQUEST
     │
     ↓
┌─────────────────────────────────────────────────────────────┐
│                  request-optimizer v2.0                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   PHASE 1: Analysis (5 Points)                              │
│   └─ references/analysis-framework.md                       │
│                                                              │
│   PHASE 2: Complexity Scoring                               │
│   └─ references/complexity-scoring.md                       │
│                                                              │
│   PHASE 3: Resource Selection                               │
│   ├─ references/agent-routing.md (27 agents)                │
│   ├─ references/skill-routing.md (27 skills)                │
│   └─ references/mcp-routing.md (14 MCPs)                    │
│                                                              │
│   PHASE 4: Execution Routing                                │
│   └─ references/decision-tree.md                            │
│                                                              │
│   PHASE 5: Integration (Future)                             │
│   └─ references/integration-interfaces.md                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
     │
     ↓
┌─────────────────────────────────────────────────────────────┐
│                   EXECUTION PATH                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Complexity < 0.3   →   Direct Execution (Haiku)           │
│   Complexity 0.3-0.7 →   Agent Execution (Sonnet)           │
│   Complexity > 0.7   →   LimitlessAgent (Opus/NZT)          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Reference Files

| File | Purpose |
|------|---------|
| `references/resource-registry.md` | Central registry of all resources |
| `references/agent-routing.md` | Logic for 27 agent selection |
| `references/skill-routing.md` | Logic for 27 skill selection |
| `references/mcp-routing.md` | Logic for 14 MCP selection |
| `references/complexity-scoring.md` | Complexity calculation algorithm |
| `references/decision-tree.md` | Decision rules and routing |
| `references/analysis-framework.md` | 5-point analysis framework |
| `references/integration-interfaces.md` | Future LimitlessAgent interfaces |
| `references/execution-example.md` | Practical example |
| `references/configuration-guide.md` | Customization guide |

## How It Works

### Phase 1: Analysis (5 Points)

When a request is received, analyze using `references/analysis-framework.md`:

1. **Specificity Assessment** - How specific/vague is the request?
2. **Exploration Detection** - Does this need codebase exploration?
3. **Subtask Identification** - Should this be decomposed?
4. **Tool Coordination** - What resources are needed?
5. **Model Recommendation** - Which model is optimal?

### Phase 2: Complexity Scoring

Calculate complexity using `references/complexity-scoring.md`:

```
complexity_score = (
    scope_factor * 0.25 +
    depth_factor * 0.25 +
    ambiguity_factor * 0.20 +
    tooling_factor * 0.15 +
    duration_factor * 0.15
)
```

Result: `0.0` (trivial) to `1.0` (maximum complexity)

### Phase 3: Resource Selection

Based on complexity and request type, consult:

- `references/agent-routing.md` - Select from 27 specialized agents
- `references/skill-routing.md` - Select from 27 available skills
- `references/mcp-routing.md` - Select from 14 MCP integrations

### Phase 4: Recommendation

Present structured recommendation:

```markdown
## Analysis Results

| Factor | Assessment |
|--------|------------|
| **Specificity** | [HIGH/MEDIUM/LOW] |
| **Complexity Score** | [0.0 - 1.0] |
| **Exploration Needed** | [Yes/No] |
| **Subtasks Identified** | [Count] |

## Resource Recommendation

| Type | Resource | Reason |
|------|----------|--------|
| Model | [Haiku/Sonnet/Opus] | [Why] |
| Agent | [name or none] | [Why] |
| Skills | [list or none] | [Why] |
| MCPs | [list or none] | [Why] |

## Execution Path

[Direct | Agent | LimitlessAgent]

## Approval Required

[List of items needing approval]

Ready to execute? (Yes / No / Adjust)
```

### Phase 5: Execution

After approval:
1. Execute recommended strategy
2. Track metrics
3. Report results
4. Ask if additional steps needed

## Approval Gates

### Always Require Approval

- Invoking Explore Agent
- Invoking any specialized Agent
- Using Opus model
- Escalating to LimitlessAgent
- MCP write operations
- Multi-step workflows (5+ tasks)

### Safe Without Approval

- Analyzing request
- Recommending strategy
- Reading files
- Simple edits (1 file, clear scope)
- MCP read operations

## External Catalogs

This skill references but does not duplicate:

| Catalog | Location |
|---------|----------|
| Agents | `Automation/agents/AGENTS-CATALOG.md` |
| MCPs | `Automation/mcps/MCP-CATALOG.md` |
| LLM Routing | `Projects/LimitlessAgent/docs/diagrams/llm-routing.md` |

## Future Integration

### LimitlessAgent

When complexity > 0.7 and task is multi-step, this skill will:
1. Create `IExecutionPlan` (see `references/integration-interfaces.md`)
2. Handoff to LimitlessAgent
3. Monitor execution via NZT Protocol
4. Report results

### State Persistence

Future versions will persist:
- Execution history
- Metrics
- Learning patterns

Via Supabase (see `references/integration-interfaces.md`)

## Constraints

1. Always get approval before heavy operations
2. Start with analysis, not execution
3. Be concise in reporting
4. Recommend `/clear` when context is bloated
5. Default to Haiku for simple tasks
6. Respect rate limits and cost budgets

## Changelog

See `CHANGELOG.md` for version history.
