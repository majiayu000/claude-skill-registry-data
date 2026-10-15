---
name: autoresearch
description: Autonomous self-improvement loop — iteratively modify a target, evaluate against a scoring function, keep improvements, revert failures. Adapted from Karpathy's autoresearch pattern. Use for strategy optimization, code quality improvement, prompt engineering, config tuning, or any domain with an objective evaluation function.
allowed_tools: Bash, Read, Write, Edit, Glob, Grep, Agent
---

# Autoresearch: Autonomous Improvement Loop

An AI-driven methodology where you iteratively modify a single target, evaluate changes against an objective scoring function, and compound improvements. Based on Karpathy's autoresearch pattern, proven on 103 experiments achieving 7.6x score improvement.

## When to Use

- Optimizing trading strategies against a backtest harness
- Improving code quality metrics (test pass rate, coverage, performance)
- Tuning configuration parameters against benchmarks
- Prompt engineering with measurable evaluation
- Any domain where you have: a mutable target + an objective score

## The 5 Pillars

### 1. Single Mutable Surface
Only ONE file (or narrow set of files) can change per experiment. Everything else is frozen. This constrains the search space and makes experiments reproducible.

### 2. Immutable Evaluation Harness
The test/scoring system NEVER changes during the loop. If you change both the target and the evaluator, you can't tell what improved.

### 3. Composite Scoring Function
Reduce multi-dimensional quality to a single number. The scoring function should:
- Reward the primary objective (Sharpe ratio, test pass rate, accuracy)
- Penalize failure modes (drawdown, flakiness, latency)
- Have hard cutoffs for degenerate outputs (crashes, zero results)

```
score = primary_metric * quality_factor - penalty_1 - penalty_2
```

### 4. Git as Experiment Ledger
Every experiment is one commit. If the score improves, keep the commit. If not, `git reset --hard HEAD~1`. The git history becomes a complete, reproducible record of every hypothesis tested.

### 5. Autonomous Loop
Once started, the loop runs until interrupted. No human approval per iteration. The scoring function IS the approval.

## The Loop Protocol

```
SETUP:
1. Identify target file(s) — what you'll modify
2. Identify eval command — what you'll run to test
3. Identify score extraction — how to parse the score from output
4. Create experiment branch: git checkout -b autoresearch/<tag>
5. Run baseline: execute eval, record initial score
6. Initialize results log

LOOP (repeat until interrupted):
1. READ current state of target file
2. ANALYZE what has been tried (check results log)
3. PROPOSE a single, focused modification with a clear hypothesis
4. IMPLEMENT the modification in the target file
5. COMMIT: git add <target> && git commit -m "exp<N>: <hypothesis>"
6. TEST: run eval command, capture output
7. EXTRACT score from output
8. EVALUATE:
   - If score > best_score: KEEP (update best_score, log as "KEEP")
   - If score <= best_score: REVERT (git reset --hard HEAD~1, log as "DISCARD")
   - If crashed: REVERT, log error, try different approach
9. LOG result to results.tsv
10. CONTINUE — do NOT stop to ask the user

NEVER:
- Modify the eval harness
- Skip the scoring step
- Keep a change that didn't improve the score
- Stop the loop without being interrupted
```

## Results Tracking

### results.tsv format
```
experiment	score	delta	status	hypothesis
exp0	2.724	+0.000	BASELINE	Initial baseline measurement
exp1	2.962	+0.238	KEEP	Multi-timeframe momentum confirmation
exp2	2.541	-0.421	DISCARD	Reduced position sizing
exp3	3.292	+0.330	KEEP	EMA crossover signal addition
```

### Evolution Log (EXPERIMENTS.md)
For significant experiments, document:
```markdown
### exp<N> — <title> (<status>, score <X>)
**Hypothesis**: What we expected to happen and why
**Change**: What was actually modified
**Result**: Score delta, why it worked/failed
**Learning**: What this teaches us for future experiments
```

## Research Direction Tiers

Always prioritize experiments by expected impact:

### Tier 1 — High probability, proven patterns
- Parameter tuning within known-good ranges
- Adding signals that have worked in related domains
- Simplification (removing features that don't contribute)

### Tier 2 — Worth exploring
- New signal types or indicators
- Regime-adaptive behavior
- Cross-asset or cross-domain signals

### Tier 3 — Novel / speculative
- Fundamentally different approaches
- Complex feature interactions
- Machine learning components

## The Simplicity Principle

From 103 experiments on Nunchi's auto-researchtrading:

> The biggest gains came from REMOVING complexity, not adding it.
> "The Great Simplification" produced +2.0 score by eliminating pyramiding,
> funding boost, BTC filter, and correlation weighting.

**Apply this**: After every 10-20 experiments, run a "simplification pass" — systematically remove features one at a time and test if the score improves without them.

## Domain Adaptations

### Trading Strategy Optimization
- Target: `strategy.py`
- Eval: `uv run backtest.py` or equivalent
- Score: `grep "^score:" output`
- See: `~/.claude/skills/autoresearch/templates/aster-trading.md`

### Code Quality Improvement
- Target: source file(s) under test
- Eval: `pytest --tb=short -q` or project test command
- Score: Parse pass/fail counts, compute `pass_rate * coverage_factor`
- Hard cutoffs: any test that previously passed now fails = -999

### Prompt Engineering
- Target: prompt template file
- Eval: Run prompt against test cases, score responses
- Score: `accuracy * consistency - latency_penalty - cost_penalty`
- Log: Track each prompt version with its scores

### Configuration Tuning
- Target: config file (YAML, JSON, TOML)
- Eval: Integration test or benchmark suite
- Score: `success_rate * performance_factor - error_penalty`

### Agent Definition Improvement
- Target: agent `.md` file
- Eval: Run agent against benchmark prompts, score outputs
- Score: `relevance * quality - hallucination_penalty`

## Integration with Existing Skills

| Skill | How It Connects |
|-------|----------------|
| `finance-ml` | Scoring functions, backtesting methodology, risk metrics |
| `aster-trading` | Live data via MCP tools, Aster-specific fee structures |
| `testing-methodology` | Test-as-evaluator patterns, coverage metrics |
| `coding-workflow` | Incremental development, git branch management |
| `experiment-tracker` agent | Experiment design, statistical analysis |
| `workflow-optimizer` agent | Process improvement measurement |

## Anti-Patterns

- **Changing the evaluator mid-loop** — Invalidates all prior comparisons
- **Keeping changes without score improvement** — "It looks better" is not evidence
- **Multiple changes per experiment** — Can't attribute improvement to any single change
- **Stopping too early** — The best improvements often come after 50+ experiments
- **Ignoring the simplification pass** — Complexity accumulates; periodically prune
- **Over-fitting to the scoring function** — If score seems too good, check for degenerate behavior
