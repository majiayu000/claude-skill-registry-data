---
name: mld-quantum-decoding
description: "Maximum Likelihood Decoding methodology for CSS quantum error correction codes — reformulates MLD as partition function computation in classical spin models, enabling exact MLD via tensor network contraction and approximate MLD via belief propagation. Connects QEC threshold to statistical phase transition. Use when: designing quantum error correction decoders, analyzing CSS code thresholds, computing MLD for surface/toric codes, applying tensor networks to QEC, or studying statistical mechanics of error correction."
license: Complete terms in LICENSE.txt
metadata:
  arxiv_id: "2605.17230"
  published: "2026-05-17"
  authors: "Hanyan Cao, Ge Yan, Yuxuan Du"
  tags: [quantum, error-correction, decoding, maximum-likelihood, tensor-networks, belief-propagation, phase-transition, css-codes]
---

# Maximum Likelihood Decoding for QEC Codes

Reformulates maximum likelihood decoding (MLD) of CSS codes as partition function computation in classical spin models. Provides exact and approximate decoding algorithms with theoretical guarantees.

## Core Methodology

### MLD-Spin Model Correspondence

For a CSS code [[n, k, d]] with parity check matrices H_X and H_Z:

1. **Syndrome s** from measurement → constraint on error configuration e
2. **MLD problem**: find e maximizing P(e|s) = argmax_e P(s|e)P(e)
3. **Spin model mapping**: each error configuration e ↔ spin configuration σ
4. **Partition function**: Z(β) = Σ_e exp(-β·wt(e)) · δ(H·e, s)
   where wt(e) = Hamming weight, δ enforces syndrome constraint
5. **MLD** = finding dominant term in Z(β → 0) (maximum weight configuration)

### Exact MLD via Tensor Network Contraction

```
1. Represent CSS code as tensor network:
   - Each qubit → rank-2 tensor (error variable)
   - Each check → constraint tensor (syndrome enforcement)
2. Contract network using optimized contraction path:
   - Tree-width determines computational cost
   - For planar codes (surface/toric): O(2^{√n}) via PEPS
3. Extract most probable error from contracted network
```

Complexity: exact MLD is #P-hard in general, but efficient for specific code families.

### Approximate MLD via Belief Propagation

```
BP Algorithm for CSS decoding:
1. Initialize messages m_{i→a}(e_i) = P(e_i) for each qubit i, check a
2. Iterative updates:
   - Check→qubit: m_{a→i}(e_i) = Σ_{e_{∂a\i}} ψ_a(e_{∂a}) Π_{j≠i} m_{j→a}(e_j)
   - Qubit→check: m_{i→a}(e_i) ∝ P(e_i) Π_{b≠a} m_{b→i}(e_i)
3. Convergence: stop when marginals stabilize or max iterations reached
4. Decode: e_i^* = argmax P(e_i) = argmax Π_a m_{a→i}(e_i)
```

**Convergence guarantees**: BP converges for cycle-free Tanner graphs; for CSS codes with loops, convergence depends on code structure and noise level.

### QEC Threshold as Statistical Phase Transition

The decoding threshold p_th corresponds to a phase transition in the associated spin model:
- **Ordered phase** (p < p_th): BP converges, MLD succeeds with high probability
- **Disordered phase** (p > p_th): BP fails to converge, decoding error rate → 1/2
- **Critical point**: p_th determined by Nishimori line crossing in the phase diagram

## Usage Patterns

### Pattern 1: Exact MLD for small codes
Use tensor network contraction for codes with n ≤ 50 where exact answers are needed for benchmarking.

### Pattern 2: BP decoding for large codes
Use belief propagation for codes with n > 100 where approximate decoding is acceptable.

### Pattern 3: Threshold estimation
Scan noise parameter p, compute logical error rate vs p, identify phase transition point.

## Error Handling

### BP Non-Convergence
- Use BP with decimation: fix most confident bits, re-run on remaining
- Apply message damping: m_new = (1-λ)·m_old + λ·m_update
- Fall back to minimum-weight perfect matching (MWPM) for surface codes

### Tensor Network Contraction Cost
- For high tree-width codes, use approximate contraction (boundary MPS)
- Use hypergraph product codes to reduce contraction complexity
- Apply Monte Carlo tensor contraction for very large codes
