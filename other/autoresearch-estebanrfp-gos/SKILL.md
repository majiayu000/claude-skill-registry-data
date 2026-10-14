---
name: Autoresearch
description: "Autonomous iterative optimization. The agent modifies, executes, measures, and decides — looping in background to improve any measurable target overnight."
---

## Concept

Inspired by Karpathy's autoresearch pattern: an agent that runs experiments autonomously, keeps what works, discards what doesn't, and reports results.

The agent IS the researcher. No external framework needed — GenosOS tools (exec, write, read, memory, cron) are the infrastructure.

## How It Works

```
User: "Optimize X. Measure Y. Run overnight."

Agent:
  1. Understand the target (file, config, prompt, code)
  2. Establish baseline — run once, measure Y, save as baseline
  3. Generate hypothesis — what change might improve Y?
  4. Modify — write the change to the target
  5. Execute — run the measurement script
  6. Evaluate — compare Y against best known result
  7. Decide — keep (Y improved) or discard (revert to best)
  8. Log — save result to research log in memory
  9. Repeat from step 3 via cron
  10. Report — summarize findings when user returns
```

## Setup

No external credentials needed. Uses GenosOS built-in tools only.

**Requirements:**
- A measurable target (file, script, config, prompt)
- A metric that can be extracted from stdout (number, score, time)
- A command to execute the measurement

## Usage

Start a research session by telling the agent what to optimize:

### Prompt Optimization
```
"Optimize my system prompt for conciseness. Test with these 10 questions.
Measure average response tokens. Run every 10 minutes overnight."
```

### Code Performance
```
"Optimize server/memory.js prefetch function. Run bun test and measure
execution time. Keep changes that are faster without breaking tests."
```

### Embedding Quality
```
"Find the best similarity threshold for memory enrichment. Test values
from 0.40 to 0.70 in steps of 0.02. Measure precision against these
10 known-similar pairs. Run all variants tonight."
```

### API Response Quality
```
"Test 20 variations of temperature (0.1-1.0) and top_p (0.5-1.0) for
the summary task. Measure BLEU score against these reference summaries."
```

## Research Protocol

### Baseline (always first)
Run the target exactly as-is. Record the metric. This is the baseline that all experiments compare against.

### Experiment Strategies

**Sweep** — systematic parameter search:
```
Parameters: [threshold: 0.40-0.70, step 0.02]
Run each value once → rank by metric → report top 5
```

**Evolutionary** — agent-driven hypothesis:
```
Analyze current best → form hypothesis → modify → test → keep/discard
Each iteration informed by all previous results
```

**Ablation** — remove and measure:
```
Remove component X → measure → if equal or better, simplify
Goal: find unnecessary complexity
```

### Decision Rules

- **Keep**: metric improved (lower is better or higher is better — defined at start)
- **Discard**: metric worsened or unchanged + added complexity
- **Keep + simplify**: metric unchanged but code/config is simpler
- **Crash**: log as crash, revert, note what broke

### Logging

Each experiment logged to memory as research entry:

```
[MEMORY]
## Autoresearch: {topic}
Run: #{number} | {timestamp}
Change: {what was modified}
Metric: {value} (baseline: {baseline}, best: {best})
Status: keep | discard | crash
Insight: {what was learned}
```

## Execution Modes

### Cron Loop (overnight)
Agent creates a cron job that triggers itself with the research context:
```
cron add "autoresearch-{topic}" --schedule "every 10m"
  --message "Continue autoresearch on {topic}. Current best: {value}."
```

### Batch (immediate)
Agent generates all variants upfront, executes them sequentially, reports at the end. One LLM call to plan, mechanical execution, one LLM call to analyze.

### Interactive
User stays in the loop — agent proposes, user approves, agent executes. For sensitive targets where autonomous modification is risky.

## Token Efficiency

### Minimize LLM calls per iteration:

**Sweep mode**: Zero LLM during execution. Agent generates all parameter combinations upfront → exec loop runs mechanically → LLM analyzes results at the end. Cost: 2 LLM calls total.

**Evolutionary mode**: One LLM call per iteration (hypothesis + modification). More tokens but smarter exploration. Cost: N calls for N experiments.

**Recommended for overnight**: Sweep first (cheap, covers parameter space), then evolutionary on the best region (smart, targeted).

### Context reuse
The cron message carries the research state: topic, baseline, current best, experiment count. No memory lookup needed to resume — the context is in the message.

## Guardrails

- **Never modify prepare/measurement code** — only the target under optimization
- **Always establish baseline first** — no optimization without reference
- **Revert on crash** — restore last known-good state before next experiment
- **Cap iterations** — default max 100 experiments per session (configurable)
- **Budget awareness** — log token cost per iteration, warn if burn rate is high
- **Workspace only** — all modifications within agent workspace, never system files

## Output

When the user returns, the agent summarizes:

```
Autoresearch Report: {topic}
Duration: 8h 20m | Experiments: 84 | Kept: 12 | Discarded: 68 | Crashed: 4

Baseline: 0.997
Best: 0.891 (-10.6%)
Best config: {parameters or diff}

Top 5 experiments:
1. #47 — 0.891 — reduced attention heads from 8 to 6
2. #23 — 0.903 — increased batch size to 128
3. #61 — 0.912 — switched to cosine schedule
4. #12 — 0.934 — removed dropout (simplification win)
5. #78 — 0.940 — lower learning rate 3e-4 → 1e-4

Key insights:
- Fewer attention heads consistently outperformed (6 > 8 > 12)
- Dropout hurts at this scale — removing it is free improvement
- Batch size sweet spot is 96-128, diminishing returns above

Failed hypotheses:
- Larger model (crashes at 80M params on this GPU)
- RoPE embeddings (worse than learned positional)
```

## Scope

Covers: autonomous optimization of any measurable target within the agent workspace.
Does NOT cover: training neural networks (requires GPU + PyTorch), modifications outside workspace, tasks without measurable metrics.
