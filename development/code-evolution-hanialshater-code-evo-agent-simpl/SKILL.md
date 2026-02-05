---
name: code-evolution
description: Autonomous multi-agent code evolution system for optimization problems. Use when solving complex optimization problems (packing, geometry, scheduling, search) through evolutionary approaches with multiple independent AI agents. Multi-start hybrid heuristic+SLSQP methods significantly outperform single approaches. Triggers include genetic algorithms, evolutionary optimization, multi-agent problem solving, parameter tuning at scale, AlphaEvolve-style research, or evolving code solutions across generations.
---

# Code Evolution

## Architecture

```
orchestrator (you)
├── spawn agents (Task tool, subagent_type='general-purpose')
├── evaluate solutions (run evaluate.py)
├── manage archive (best solutions per generation)
└── plan next generation
```

## Critical Principle: Agent Autonomy

**NEVER write solution code yourself.** You (the orchestrator) ONLY:
- Create the fixed evaluation harness (read-only for agents)
- Spawn autonomous subagents via Task tool
- Evaluate results using the harness
- Plan next generation based on results

Agents have **full autonomy** to implement their assigned approach. You don't guide their code - you guide their problem-solving strategy.

## Workflow

### Phase 0: Setup (Orchestrator Only)
Create the **immutable harness** - agents can ONLY use, never alter:
1. `problems/<name>/problem.md` - problem definition (READ-ONLY for agents)
2. `problems/<name>/evaluation/evaluate.py` - evaluation function (FROZEN, not modifiable by agents)
3. `problems/<name>/config.json` - benchmark, constraints, metadata

Agents receive paths to these files but cannot modify them.

### Phase 1: Generation Loop (3-7 generations)

1. **Plan Strategies**: Design 2-4 different approaches for agents to explore
2. **Spawn Agents**: Use Task tool with `subagent_type='general-purpose'` (15s timeout per agent)
   - Each agent gets problem description, their specific approach, and path to evaluator
   - Agents write solutions to `generations/gen{N}/agent_{id}.py`
   - Agents run themselves: `subprocess.run([sys.executable, agent_file])`
   - Output: JSON with `"score"` and `"circles"`
3. **Evaluate**: You run evaluator on agent outputs (agents cannot run this)
4. **Cross-Inspiration**: Share winning ideas with next generation agents for inspiration
5. **Prune**: Keep only the best 1-2 approaches from previous generation
6. **Archive**: Store best solution to `generations/archive/`

### Phase 2: Cross-Inspiration & Pruning

Between generations:
- **Reference winners**: Show agents the best previous solution's strategy
- **Prune dead approaches**: Stop testing approaches that underperform
- **Mix winning ideas**: Combine best techniques from multiple agents
- **Diversify within winners**: Vary parameters (seeds, iteration counts, thresholds)

## File Structure

```
problems/<name>/
├── problem.md
├── config.json
├── evaluation/evaluate.py
└── generations/
    ├── gen1/agent_*.py
    └── archive/best_solution.py
```

## Core Design Principles

### Separation of Concerns
- **Orchestrator role**: Strategy planning, harness building, result evaluation, pruning
- **Agent role**: Implementation autonomy within their assigned strategy
- **Harness**: Frozen, read-only, immutable contract between them

### Evolution Mechanics
1. **Diverse exploration** (Gen 1-3): Different approaches find different optima
2. **Cross-inspiration** (Gen 2+): Winning ideas inspire next generation
3. **Pruning** (Gen 3+): Kill weak approaches, double down on winners
4. **Multi-start within winners**: Vary parameters of proven strategies (+2-5% improvement)
5. **Validation first**: Invalid solutions score 0 - harness is source of truth

## Evolution Strategy

| Phase | Generations | Orchestrator Action |
|-------|-------------|-----|
| Explore | 1-3 | Spawn 3-4 agents with diverse strategies. Find winners. |
| Prune | After Gen 2-3 | Kill underperforming approaches. Keep 1-2 best. |
| Cross-Inspire | Before Gen 4+ | Share winning solution code/strategy with next agents. |
| Exploit | 4-5 | Spawn agents that refine/combine winning approaches. Vary seeds/params. |
| Polish | 6-7 | Multi-start within best approach. Push toward benchmark. |

## Orchestrator Responsibilities

### What YOU Do (Never Delegate)
- Create immutable evaluation harness (problem definition, evaluator, config)
- Spawn agents with Task tool
- Analyze results and plan next generation
- **Prune**: Decide which approaches to continue, which to kill
- **Cross-inspire**: Extract winning ideas and share with next agents
- Archive best solutions

### What Agents Do (Full Autonomy)
- Implement their assigned strategy
- Write solution code
- Self-validate before output
- Run themselves and produce JSON output

## Cross-Inspiration Strategy

After each generation, **extract and communicate**:

```markdown
## What Worked
- Agent X achieved Y% with [strategy description]
- Key insight: [what made it work]
- Code reference: [location or snippet]

## What Failed
- Agent Z's [strategy] only achieved W%
- Likely issue: [root cause analysis]
- Don't repeat: [specific thing to avoid]

## Recommended Evolution
- Agents should build on: [winning strategy]
- Vary these parameters: [list of what to try]
- Combine techniques: [which ideas from multiple winners]
```

Agents use this to:
- Understand what works (cross-inspiration)
- Avoid dead ends (prune knowledge)
- Focus effort on proven directions

## References

- **Agent spawning**: See [references/agent-prompts.md](references/agent-prompts.md)
- **Evaluator template**: See [references/evaluator-template.md](references/evaluator-template.md)

## Adding New Problems

1. Create `problems/<name>/problem.md` (objective, constraints, benchmark, format)
2. Create `problems/<name>/config.json` (benchmark value, metadata)
3. Create `problems/<name>/evaluation/evaluate.py` (validate, score, evaluate functions)
