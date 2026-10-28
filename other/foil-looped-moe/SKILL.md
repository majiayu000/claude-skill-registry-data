---
name: foil-looped-moe
version: v1.0.0
last_updated: 2026-09-30
description: "Foil methodology for looped sparse MoE — flatten experts (halve layers, double experts/layer, double passes) and untie attention (per-pass attention params, shared experts/routers). Use when: (1) combining layer looping with MoE, (2) MoE routing confidence is low or load imbalanced, (3) extracting more capability at fixed params+compute. Keywords: looped MoE, expert flattening, attention untying, routing confidence, parameter efficiency."
arxiv_id: "2609.35751"
authors: "Shouren Wang, Chuang Ma, Mohsen Hariri et al. (9 authors)"
tags: [moe, looped-transformer, routing, architecture-design, efficiency]
---

# Foil: How to Loop MoE — Flatten the Experts, Untie the Attention

From arXiv:2609.35751 (2026-09-28). Code: https://github.com/SR-A-W/how-to-loop-moe

## Two Ideas, One Combination

**Looped transformers** reuse one layer block multiple passes (fixed size, more compute). **Sparse MoE** activates few experts per token (many params, low compute). **Looped MoE** bridges them — but naive looping of an MoE underperforms. **Foil** is the correct way to loop an MoE, at fixed expert parameters and fixed expert compute per token:

### 1. Flatten the experts
- Halve the number of expert layers, **double the experts per layer**, **double the passes**.
- Effect: every routing decision draws from a **larger pool** (2× choices per routing), while total expert params and FLOPs stay constant.
- The returns of looping and of wider expert pools **amplify each other** — this is the key interaction.

### 2. Untie the attention
- Give **each pass its own attention parameters**; experts and routers stay shared across passes.
- Effect: more balanced, more confident routing at equal model shape.

## Why It Works (ablation-derived design guidance)

1. Loss improves **monotonically with flattening degree** at 100B tokens (best: −0.012 nat vs baseline at equal params+compute).
2. **Routing confidence tracks healthy expert use better than load balance** — use confidence, not balance losses, as the health signal.
3. A sparse looped MoE should therefore use **more experts per layer and more passes** than intuition suggests.

## Implementation Sketch

```python
# baseline MoE: L expert layers, E experts/layer, 1 pass
# Foil(k):  L/2 expert layers, 2E experts/layer, 2 passes,
#           per-pass attention params (unshared), shared experts+routers
for p in range(passes):            # 2 passes for Foil
    h = attn_p[h]                  # per-pass attention: NOT shared
    h = moe_router_topk(h, k)      # router shared across passes,
                                   # now selects from 2E experts
```

## When to Use

- Designing a looped MoE from scratch or converting a looped dense model.
- MoE routing is under-confident / load-balance losses dominate without helping loss.
- Parameter-compute tradeoff sweet spot: same params, same compute, better loss — the win is architectural, not budgetary.

## Key Results (20B→100B token pretraining)

| Metric | Result |
|---|---|
| Pretraining loss @ 20B tokens | every Foil variant < unflattened looped baseline |
| Loss @ 100B tokens | monotonic in flattening; best −0.012 nat @ equal params+compute |
| Downstream accuracy | on par or better |
| Routing | untying attention → more balanced + more confident |
