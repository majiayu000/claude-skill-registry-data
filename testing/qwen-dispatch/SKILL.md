---
name: qwen-dispatch
description: Bidirectional Qwen↔Claude task routing with Claude-style thinking — offload worker tasks, escalate complex tasks, unified model routing
trigger: /qwen-dispatch — When a task is L5-L6 worker tier, or when adding Claude-style thinking to Qwen tasks
globs: ["**/*"]
---

# Qwen Dispatch Skill — Bidirectional Claude↔Qwen Integration

Route tasks to the optimal engine. Claude Code handles strategic work (L0-L2).
Qwen Code handles worker tasks (L5-L6) with optional Claude-style thinking.

## Task Types (11)

| Type | Mode | Description |
|------|------|-------------|
| `review` | Worker | Code review and analysis |
| `test-gen` | Worker | Generate tests |
| `docs` | Worker | Generate documentation |
| `explore` | Worker | Codebase exploration |
| `fix` | Worker | Simple bug fixes |
| `scaffold` | Worker | Generate boilerplate |
| `refactor` | Worker | Clean up code |
| `think` | Thinking | Claude-style reasoning only (no execution) |
| `plan` | Thinking | Think + plan (no execution) |
| `auto` | Pipeline | Think + plan + execute (full pipeline) |
| `raw` | Direct | Pass prompt directly |

## How to Dispatch

### Worker Tasks (saves Claude tokens)
```bash
qwen-dispatch review "Review src/auth.py for security issues" --cwd /path/to/project
qwen-dispatch test-gen "Generate pytest tests for src/utils.py" --cwd /path/to/project
qwen-dispatch docs "Generate docstrings for src/core/pipeline.py" --cwd /path/to/project
qwen-dispatch explore "Find all API endpoints in this project" --cwd /path/to/project
qwen-dispatch fix "Fix the off-by-one error in pagination logic" --cwd /path/to/project
qwen-dispatch scaffold "Create a new FastAPI router for /api/v2/users" --cwd /path/to/project
qwen-dispatch refactor "Simplify the nested conditionals in src/auth.py" --cwd /path/to/project
```

### Thinking Tasks (NEW — Claude-style reasoning in Qwen)
```bash
# Thinking only — structured analysis without execution
qwen-dispatch think "Analyze the auth flow design" --cwd /path/to/project

# Think + Plan — analysis + execution DAG
qwen-dispatch plan "Implement user pagination" --cwd /path/to/project

# Full auto-activation — think + plan + execute
qwen-dispatch auto "Build REST API with JWT auth" --cwd /path/to/project
```

### --think Flag (NEW — add thinking to ANY task type)
```bash
# Review WITH structured reasoning first
qwen-dispatch review "Review src/auth.py" --think --cwd /path/to/project

# Fix WITH root cause analysis first
qwen-dispatch fix "Fix the TypeError in src/utils.py:42" --think --cwd /path/to/project
```

### Escalation — Qwen → Claude (NEW)
```bash
# When Qwen detects a task beyond its tier
qwen-escalate "Design the new microservice architecture" --cwd /path/to/project

# With prior thinking context
qwen-escalate "Deploy to production" --context ~/.qwen/thinking/think_abc123.json
```

## Model Selection

| Model | Type | Best For |
|-------|------|----------|
| coder-model (--qwen-oauth) | Cloud | Best quality coding (1K free/day) |
| qwen3.5:cloud | Cloud (default) | Most capable reasoning |
| qwen3:8b | Local (5.2GB) | Fast, free, worker tasks |
| kimi-k2.5:cloud | Cloud | Strong coding |
| minimax-m2.5:cloud | Cloud | Creative tasks |

## Backend Selection

| Flag | Backend | Limit |
|------|---------|-------|
| `--qwen-oauth` | Qwen3-Coder cloud | 1K free req/day |
| `--ollama` | Ollama local/cloud | Unlimited |
| (default) | Uses ~/.qwen/settings.json | Depends on auth |

## Routing Decision Matrix

| Signal | Route to Qwen | Route to Claude |
|--------|--------------|-----------------|
| Authority | L5-L6 worker | L0-L2 strategic |
| Risk | T0-T1 safe/local | T2-T3 shared/critical |
| MCP needs | filesystem, github, memory, context7, brave-search, tavily, sequential | aster, playwright, stripe, k8s, terraform, slack, postgres, docker |
| Scope | Single file, clear goal | Multi-file, coordination needed |
| Nature | Review, test, docs, explore, scaffold | Architecture, security, design |

## Artifact Locations

| Artifact | Path |
|----------|------|
| Thinking | `~/.qwen/thinking/*.json` |
| Plans | `~/.qwen/plans/*.json` |
| Execution logs | `~/.qwen/logs/*.json` |
| Metrics | `~/.qwen/metrics/*.jsonl` |

## Token Budget

- Each Qwen dispatch = 0 Claude tokens
- Qwen OAuth: 1,000 requests/day free
- Ollama: unlimited
- Auto-dispatch in /plan routes L5-L6 tasks automatically

## Auto-Dispatch in /plan

The plan command auto-routes L5-L6 worker tasks to Qwen Code.
Claude Code focuses on L0-L2 strategic decisions and orchestration.
The `--think` flag is automatically added for tasks that benefit from structured reasoning.
