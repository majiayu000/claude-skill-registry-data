---
name: unified-router
description: Intelligent task routing across Claude Code + Qwen Code — picks the right engine, model, and thinking depth for every task
trigger: Always active — CoreMind evaluates routing for every task in STAGE 4 (PLAN) and STAGE 7 (EXECUTE)
globs: ["**/*"]
---

# Unified Router — Claude↔Qwen Intelligent Task Routing

Route every task to the optimal engine (Claude Code or Qwen Code), model, and thinking depth.
This skill replaces ad-hoc routing decisions with a systematic framework.

## Routing Decision Matrix

### Engine Selection

| Signal | Route to Claude Code | Route to Qwen Code |
|--------|---------------------|---------------------|
| Authority level | L0-L2 (strategic) | L5-L6 (worker) |
| Risk tier | T2-T3 (shared/critical) | T0-T1 (safe/local) |
| MCP servers needed | aster, playwright, stripe, k8s, terraform, slack, postgres, docker | filesystem, github, memory, context7, brave-search, tavily, sequential |
| Multi-agent orchestration | Yes | No |
| File coordination | Multiple tasks touch same files | Single-file focus |
| Thinking depth | Architecture, security, design | Review, test, docs, explore |
| Cost sensitivity | Budget available | Token-saving priority |

### Model Selection (within each engine)

**Claude Code models:**
| Complexity | Model | When |
|-----------|-------|------|
| Enterprise | opus | Architecture, security audit, multi-service design |
| Complex | sonnet | Multi-file implementation, debugging, integration |
| Simple | haiku | Quick lookups, simple edits, status checks |

**Qwen Code models:**
| Complexity | Model | When |
|-----------|-------|------|
| Deep | qwen3.5:cloud | Complex code review, large refactors |
| Standard | qwen3:8b | Test gen, docs, simple fixes |
| Quick | qwen3:8b | Exploration, search, scaffolding |
| Creative | minimax-m2.5:cloud | Creative writing, brainstorming |
| Coding | kimi-k2.5:cloud | Strong coding tasks |
| Cloud (free) | coder-model (--qwen-oauth) | Best quality, 1K free/day |

### Thinking Depth Selection

| Task Type | Thinking Budget | Model | Engine |
|-----------|----------------|-------|--------|
| Architecture, design, security | 8000 tokens | qwen3.5:cloud or Claude opus | Either (prefer Claude) |
| Implementation, bug fix, integration | 4000 tokens | qwen3:8b or Claude sonnet | Either |
| Review, test, docs, explore, scaffold | 1000 tokens | qwen3:8b or Claude haiku | Prefer Qwen (saves tokens) |

## Dispatch Commands

### Claude → Qwen (offload worker tasks)
```bash
# Standard dispatch (existing)
qwen-dispatch review "Review src/auth.py" --cwd ~/project

# With thinking (NEW)
qwen-dispatch review "Review src/auth.py" --think --cwd ~/project

# Thinking-only mode (NEW)
qwen-dispatch think "Analyze the auth flow design" --cwd ~/project

# Full auto-activation (NEW)
qwen-dispatch auto "Implement user pagination" --cwd ~/project
```

### Qwen → Claude (escalation)
```bash
# When Qwen detects T2+ risk
qwen-escalate "Design the new microservice architecture" --cwd ~/project

# With prior thinking context
qwen-escalate "Deploy to production" --context ~/.qwen/thinking/think_abc123.json
```

## Routing Algorithm

```
1. Parse task → extract domain, complexity, risk signals
2. Check MCP requirements → if needs servers Qwen lacks → Claude
3. Check risk tier → T2+ → Claude
4. Check authority level → L0-L2 → Claude, L5-L6 → Qwen
5. Check file coordination → multi-task same-file → Claude (needs orchestration)
6. Default → Qwen with --think flag (saves tokens, adds reasoning)
```

## Integration Points

- **CoreMind STAGE 4 (PLAN)**: Router evaluates each plan step
- **CoreMind STAGE 7 (EXECUTE)**: Router dispatches to the selected engine
- **qwen-dispatch**: Updated with `think`, `plan`, `auto` task types + `--think` flag
- **qwen-escalate**: New bidirectional bridge for Qwen→Claude handoff
- **auto-activate.py**: Qwen's thinking engine (invoked by all new task types)

## Artifact Flow

```
Claude thinking  →  ~/.claude/projects/*/memory/  (Claude's memory)
Qwen thinking    →  ~/.qwen/thinking/*.json       (structured artifacts)
Qwen plans       →  ~/.qwen/plans/*.json          (execution DAGs)
Qwen logs        →  ~/.qwen/logs/*.json           (execution results)
Qwen metrics     →  ~/.qwen/metrics/*.jsonl       (performance tracking)
```

Both engines can read each other's artifacts for context continuity.
