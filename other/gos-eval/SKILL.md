---
name: gos-eval
description: Evaluates whether dependency-aware structural retrieval of agent skills improves task completion performance and computational efficiency compared to flat library access and semantic-only retrieval. It probes an agent's ability to assemble functionally complete, prerequisite-aware skill bundles for long-horizon technical and embodied sequential decision-making tasks. Use when the user wants to benchmark on SkillsBench, ALFWorld, or asks about evaluating this task. Reports average reward.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.05333
  bibtex_key: li2026graphofskills
  confidence: high
---

# gos-eval

> Graph of Skills: Dependency-Aware Structural Retrieval for Massive Agent Skills — Li et al. (2026) (arXiv:2604.05333, 2026)

## What this evaluates

Evaluates whether dependency-aware structural retrieval of agent skills improves task completion performance and computational efficiency compared to flat library access and semantic-only retrieval. It probes an agent's ability to assemble functionally complete, prerequisite-aware skill bundles for long-horizon technical and embodied sequential decision-making tasks.

## Datasets

- **SkillsBench** — total ?; splits: full (-1)
- **ALFWorld** — total 140; splits: test (140)

## Metrics

- `average reward` **(primary)** — range: percent
  - Mean of per-task reward scores across all evaluated tasks. For ALFWorld, reward is binary (0/1), making average reward equivalent to success rate.
- `total token usage` — range: other
  - Sum of input and output tokens consumed by the LLM agent during task execution.
- `agent runtime` — range: other
  - Wall-clock time from agent start to agent finish, excluding environment setup.

## Input / output format

**Input**: Task instructions or textual room descriptions paired with a skill library (or retrieved skill bundles). The agent receives the raw task query without optional query rewriting.

**Output**: A sequence of executable commands, code, or tool calls to accomplish the task goal, followed by a final output formatted according to the task's expected structure.

## Scoring recipe

```python
def compute_metrics(predictions, gold, tasks):
    rewards, tokens_list, runtime_list = [], [], []
    for task in tasks:
        # Apply retry policy: max 2 infrastructure rebuilds
        reward, tokens, runtime = run_agent(task, predictions)
        if reward is not None:  # Exclude unresolved infrastructure failures
            rewards.append(reward)
            tokens_list.append(tokens)
            runtime_list.append(runtime)
    avg_reward = sum(rewards) / len(rewards)
    avg_tokens = sum(tokens_list) / len(tokens_list)
    avg_runtime = sum(runtime_list) / len(runtime_list)
    return {"average_reward": avg_reward, "avg_tokens": avg_tokens, "avg_runtime": avg_runtime}
```

## Common pitfalls

- Infrastructure failures vs. model failures: Tasks that fail environment construction are rebuilt up to two times; only truly unresolved infrastructure failures are excluded, not counted as model failures.
- Timeout handling: Timeouts after meaningful execution count as 0 reward and are kept in aggregates; early startup timeouts trigger a rerun.
- Semantic vs. structural retrieval: Vector Skills often misses prerequisite utilities needed for long-horizon tasks, leading to incomplete skill sets and artificially low rewards compared to graph-aware methods.

## Evidence (verbatim from paper)

> We report average reward across tasks as the primary evaluation metric. For ALFWorld, rewards are binary, so average reward is equivalent to success rate. We additionally report average total token usage and agent-only runtime; runtime is measured from agent start to agent finish and excludes environment setup.

## Citation

```bibtex
@misc{li2026graphofskills,
  title={Graph of Skills: Dependency-Aware Structural Retrieval for Massive Agent Skills},
  author={Li et al. (2026)},
  year={2026},
  note={arXiv:2604.05333}
}
```

- arXiv: 2604.05333
