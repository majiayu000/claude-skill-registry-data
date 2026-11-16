---
name: rohitg00--ai-engineering-from-scratch
description: "Curriculum AI engineering từ toán học lên production — 503 bài học, 20 phase, 320 giờ. MIT license. Build từ first principles: backprop, transformer, LLM, agent, swarm."
allowed-tools: Bash, Read, Write
user-invocable: true
---

AI Engineering from Scratch: curriculum toàn diện dạy AI từ đầu — không phải dùng API, mà tự build từ toán học. 503 lesson → 503 artifact (skills, agents, MCP servers).

## 20 Phase Overview

```
Phase 0-3   — Foundations
  0: Dev environment + tooling
  1: Linear algebra, calculus, probability, optimization
  2: Classical ML (regression, decision trees, clustering)
  3: Deep learning, backprop, PyTorch, JAX

Phase 4-6   — Specialized Domains
  4: Computer Vision (CNN, detection, segmentation, GAN, diffusion)
  5: NLP (tokenization, embeddings, transformers, evaluation)
  6: Speech & Audio (ASR, TTS, voice cloning)

Phase 7-12  — Advanced AI
  7: Transformers deep dive (attention, BERT, GPT, scaling)
  8: Generative AI (VAE, diffusion, video, 3D)
  9: Reinforcement Learning (Q-learning, PPO, RLHF)
  10: LLMs from scratch (tokenizer → pre-train → instruction tune → DPO → quantization)
  11: LLM Engineering (prompting, RAG, fine-tune, production)
  12: Multimodal AI (VLM, video, embodied agents)

Phase 13-17 — Systems & Production
  13: Tools & Protocols (function calling, MCP, API design)
  14: Agent Engineering (loops, memory, planning, LangGraph)
  15: Autonomous Systems (long-horizon, self-improvement, safety)
  16: Multi-agent (coordination, swarms, negotiation)
  17: Infrastructure (serving, quantization, observability, compliance)

Phase 18-19 — Responsible Dev + Capstone
  18: Ethics, safety, alignment, red-teaming
  19: 17 end-to-end products + 9 deep-build tracks
```

## Entry Points

| Background | Start | Time |
|---|---|---|
| Beginner | Phase 0 | ~306h |
| Python fluent | Phase 1 | ~270h |
| ML experienced | Phase 3 | ~200h |
| DL expert → LLMs | Phase 10 | ~100h |
| Senior → agents only | Phase 14 | ~60h |

## Install Skills

```bash
npx skills add rohitg00/ai-engineering-from-scratch  # tất cả skills
# Hoặc offline:
python3 scripts/install_skills.py <target>
```

## Lesson Format (mỗi bài)

```
1. Motto — big idea
2. Problem — what we're solving
3. Concept — theory + math
4. Build it — from raw math, no framework
5. Use it — with PyTorch/HuggingFace/etc
6. Ship it — reusable artifact
```

## Key Topics để Reference

- Backpropagation + automatic differentiation
- Attention mechanism + transformer architecture
- Fine-tuning, RLHF, DPO, Constitutional AI
- RAG + semantic search
- Quantization + inference optimization
- Multi-agent orchestration + swarm coordination
- Production deployment + observability

## Source

https://github.com/rohitg00/ai-engineering-from-scratch · MIT
