---
name: mini-openamer
description: "Use when the agent needs recursive reasoning, episodic memory retrieval, internet learning, or world-model prediction. Mini-OpenAmer: the 2B hybrid Mamba core with 9 tools, running 24/7 on Damir's laptop."
tags:
  - self-improvement
  - meta-learning
  - internet-learning
  - episodic-memory
  - world-model
  - prediction
  - recursive-reasoning
usage: |
  All Mini-OpenAmer capabilities live in training scripts + tool server :8081.
  The agent core can use them via:

  1. Recursive reasoning:  python scripts/training/reasoning_loop.py ask "<question>"
  2. Episodic memory:      python scripts/training/longterm_memory.py query "<text>"
  3. Internet learning:    python scripts/training/internet_learner.py --once
  4. World prediction:     read memory/world_model.jsonl (matches + predictions)
  5. Self-improvement:     python scripts/training/self_improve.py
  6. Meta-learning stats:  python scripts/training/meta_learn.py stats
  7. Swarm status:         python scripts/training/swarm_intelligence.py status
  8. Tool server health:   curl localhost:8081/health

  All scripts are E2E verified and run 24/7 via the cron fleet.
---

# Mini-OpenAmer Integration

Mini-OpenAmer is the self-learning core that runs alongside the main OpenAmer
agent. It provides capabilities the main agent can call:

## What it provides

- **Recursive Reasoning**: think → critique → improve loop
- **Episodic Memory**: 3.012+ episodes with 768d embeddings
- **Internet Learning**: 5 source types, 24/7 (news, papers, GitHub, docs, competitors)
- **World-Model**: cause→effect graph with future predictions
- **Meta-Learning**: adapts its own learning rate and strategy
- **Self-Improvement**: modifies its own code with test gates
- **Swarm Intelligence**: laptop + PC as collective (task routing, consensus)
- **Auto-Skill Creation**: internet insights become new Darwin skills

## Integration points

| Component | Location | Purpose |
|---|---|---|
| Tool Server | :8081 | 9 tools + test-time training |
| Smart Router | smart_router.py | 3-tier routing (local→cloud→GPU) |
| Frontier Server | PC :8082 | Qwen3.5-4B deep reasoning |
| Darwin | darwin_engine.py | Skill evolution, 15 min cycles |
| Self-Model | memory/self_model/identity.md | Evolving identity |
| World-Model | memory/world_model.jsonl | Cause-effect + predictions |
| Meta-State | training/meta_state.json | Learning-process self-knowledge |

## Energy

- Laptop: ~25 W (2B + all learning loops)
- PC (GPU worker): ~35-50 W (4B warm, training on demand)
- Total: ~60-75 W → target 20 W via quantization/distillation/Akida
- Running cost: 0 € (no API fees, local hardware)
