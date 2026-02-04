---
name: reasoner
description: >
  Advanced reasoning with search strategies (beam search, MCTS).
  WHEN: Complex problem-solving requiring exploration of multiple solution paths, optimization problems, decision trees, when you need scored/ranked reasoning paths.
  WHEN NOT: Simple linear reasoning (use sequential_thinking), trivial problems, when branching isn't needed.
version: 0.1.0
---

# Reasoner - Advanced Multi-Strategy Reasoning

## Core Concept

`mcp__plugin_kg_kodegen__reasoner` provides sophisticated reasoning with multiple search strategies. Unlike sequential_thinking (simple linear tracking), reasoner uses algorithms like Beam Search and Monte Carlo Tree Search (MCTS) to explore and score multiple solution paths, finding optimal reasoning chains.

## Strategies

| Strategy | Best For | Description |
|----------|----------|-------------|
| `beam_search` | General problems | Maintains top N paths simultaneously |
| `mcts` | Decision trees | UCB1/PUCT exploration-exploitation |
| `mcts_002_alpha` | Creative solutions | 10% higher exploration bonus |
| `mcts_002alt_alpha` | Detailed analysis | Rewards longer reasoning paths |

## Key Parameters

**Required:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `thought` | string | Current reasoning step |
| `thought_number` | number | Current step (1-based) |
| `total_thoughts` | number | Estimated total needed |
| `next_thought_needed` | boolean | Whether more steps needed |

**Optional:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `strategy_type` | string | beam_search (default), mcts, mcts_002_alpha, mcts_002alt_alpha |
| `beam_width` | number | Paths to maintain (1-10, default: 3) |
| `num_simulations` | number | MCTS rollouts (1-150, default: 50) |
| `parent_id` | string | Parent node for branching |

## Usage Examples

### Beam Search (Default)
```json
{
  "thought": "Analyzing possible caching strategies for the API",
  "thought_number": 1,
  "total_thoughts": 4,
  "next_thought_needed": true,
  "strategy_type": "beam_search",
  "beam_width": 3
}
```

### MCTS for Decision Making
```json
{
  "thought": "Evaluating database migration approaches",
  "thought_number": 1,
  "total_thoughts": 3,
  "next_thought_needed": true,
  "strategy_type": "mcts",
  "num_simulations": 100
}
```

### Creative Problem Solving
```json
{
  "thought": "Exploring novel approaches to distributed consensus",
  "thought_number": 1,
  "total_thoughts": 5,
  "next_thought_needed": true,
  "strategy_type": "mcts_002_alpha",
  "num_simulations": 75
}
```

### Detailed Analysis
```json
{
  "thought": "Deep comparison of microservices vs monolithic architecture",
  "thought_number": 1,
  "total_thoughts": 6,
  "next_thought_needed": true,
  "strategy_type": "mcts_002alt_alpha",
  "num_simulations": 50
}
```

### Branching from Parent
```json
{
  "thought": "Alternative approach using event sourcing",
  "thought_number": 3,
  "total_thoughts": 5,
  "next_thought_needed": true,
  "parent_id": "previous-node-uuid"
}
```

## Output Format

```json
{
  "session_id": "uuid-v4",
  "thought": "echoed input",
  "score": 0.85,
  "depth": 2,
  "is_complete": false,
  "next_thought_needed": true,
  "branches": 3,
  "best_path_score": 0.92,
  "strategy": "beam_search",
  "history_length": 5
}
```

## When to Use What

| Problem Type | Tool | Why |
|--------------|------|-----|
| Simple step-by-step | sequential_thinking | No scoring needed |
| Optimization | reasoner (mcts) | Finds optimal path |
| Multiple alternatives | reasoner (beam_search) | Tracks top N paths |
| Creative exploration | reasoner (mcts_002_alpha) | Higher exploration |
| Detailed analysis | reasoner (mcts_002alt_alpha) | Rewards depth |

## Reasoner vs Sequential Thinking

| Feature | Sequential Thinking | Reasoner |
|---------|-------------------|----------|
| Path scoring | No | Yes (0.0-1.0) |
| Strategy selection | No | beam_search, MCTS variants |
| Semantic analysis | No | Yes (Stella 400M embeddings) |
| Best path tracking | No | Yes (best_path_score) |
| Complexity | Lower | Higher |
| Use case | Linear reasoning | Optimization/exploration |

## Remember

- **Choose strategy wisely** - beam_search for general, MCTS for optimization
- **Adjust beam_width** - higher = more paths but slower
- **num_simulations** - more = better MCTS results but slower
- **Check scores** - output includes quality scores (0.0-1.0)
- **Use for complex problems** - overkill for simple reasoning
- **Prefer sequential_thinking** for straightforward step-by-step
