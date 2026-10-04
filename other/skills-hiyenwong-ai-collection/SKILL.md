---
name: formal-verification-probabilistic-snn-quotient
description: "Formal verification toolchain for probabilistic spiking neural networks using weight-discretized quotient abstractions. CogSpike framework integrates SNN design, simulation, and PRISM-based verification. Key contributions: weight-discretized quotient model abstraction (17x state reduction per neuron), two-sided fidelity theorem bounding firing disagreement to gray zone, Asymptotic Silence theorem guaranteeing permanent silence of unforced neurons, topology-dependent exponential state space reduction. Covers probabilistic model checking of DTMC encodings, synaptic weight discretization, verification of seven canonical topologies. Activation: formal verification, probabilistic SNN, quotient abstraction, CogSpike, PRISM, DTMC, state space explosion, synaptic weight discretization, fidelity theorem"
---

# Formal Verification of Probabilistic Spiking Neural Networks Based on Quotient Abstractions

From: **"A Formal Tool for Verification of Probabilistic Spiking Neural Networks Based on Quotient Abstractions"** (arXiv: 2606.20674, June 2026) — Nikan Zandian Jazi, Elisabetta De Maria, Christopher Leturc. (Accepted at ICANN 2026)

## Core Concept

A unified framework (**CogSpike**) for **formal verification of probabilistic spiking neural networks** using **weight-discretized quotient model abstractions** that reduce the DTMC state space exponentially (~17x per neuron), enabling verification of networks that are otherwise intractable to probabilistic model checking.

## The State Space Explosion Problem

- SNNs modeled as **Discrete-Time Markov Chains (DTMC)** grow **exponentially** with neuron count
- Ion-channel noise + unreliable synaptic vesicle release → **probabilistic** computation
- Deterministic abstractions are **mathematically inadequate** for stochastic SNNs
- General-purpose quotient abstractions discard **synaptic weight information**, limiting verifiable properties

## Key Innovations

### 1. Weight-Discretized Quotient Model Abstraction

- Maps **continuous synaptic weights** to a compact **integer range** (parameter `W`)
- Preserves **relative contribution** of each synapse during abstraction
- Enables verification while maintaining weight-dependent properties

**Discretization mapping**:
```
w_continuous ∈ ℝ  →  w_discrete ∈ {0, 1, ..., W}
```

### 2. Two-Sided Fidelity Theorem

Formal correctness guarantee: any **firing disagreement** between concrete and abstract model is confined to a **bounded gray zone** around threshold.

**Formal statement**: If neuron `i` fires in concrete model but not in abstract (or vice versa), then the membrane potential difference is bounded by a function of discretization parameter `W`.

### 3. Asymptotic Silence Theorem

Exact limit guarantee: **unforced neurons** (no external input) fall **permanently silent** in the asymptotic limit.

### 4. Topology-Dependent Scaling Analysis

State space reduction compounds **exponentially** with network size:
- **~17x reduction per neuron** for discretization parameter `W = 3`
- Empirically validated across **seven canonical topologies**
- Enables verification of networks that are otherwise intractable

## CogSpike Toolchain Architecture

### Unified Isomorphic Pipeline

```
SNN Design → Simulation → Formal Verification
    ↓              ↓              ↓
  Network     Time-driven    PRISM-based
  Model       Integration    Probabilistic
                            Model Checking
```

### Integration with PRISM

- Converts SNN topology + discretized weights → **PRISM model specification**
- Verifies **probabilistic temporal logic (PCTL)** properties:
  - Reachability: "What is the probability that neuron X fires within T ms?"
  - Steady-state: "What fraction of time is neuron Y active?"
  - Safety: "Is the probability of simultaneous firing of all neurons < ε?"
  - Liveness: "Does the network eventually reach a stable firing pattern?"

### Discretization Parameter Selection

| W | State Reduction | Fidelity | Verifiable Property Scope |
|---|----------------|----------|--------------------------|
| 1 | ~5x per neuron  | Coarse   | Basic reachability only |
| 3 | ~17x per neuron | Medium   | Full PCTL suite |
| 5 | ~30x per neuron | Fine     | Weight-sensitive properties |

## Implementation Patterns

### Weight Discretization

```python
def discretize_weights(weights, W=3):
    """Map continuous synaptic weights to discrete integer range."""
    w_min, w_max = weights.min(), weights.max()
    discrete = np.floor((weights - w_min) / (w_max - w_min) * W).astype(int)
    return np.clip(discrete, 0, W)
```

### Quotient Abstraction Construction

```python
def build_quotient_abstraction(membrane_states, W):
    """Partition membrane potentials into equivalence classes."""
    n_classes = W + 1
    abstraction = {i: [] for i in range(n_classes)}
    for state in membrane_states:
        v_class = discretize_potential(state.v, W)
        abstraction[v_class].append(state)
    return abstraction
```

### PRISM Model Generation

```
// Generated PRISM module for discretized SNN
module neuron_1
    v1 : [0..W] init W/2;
    firing1 : bool init false;
    [] !(firing1) -> p_activate: (v1'=W) + (1-p_activate): (v1'=v1);
    [] v1>=W -> (v1'=0) & (firing1'=true);
    [] firing1 -> (firing1'=false);
endmodule
```

## Verification Properties

### Canonical Properties for SNNs

1. **Synchronization Probability**: `P=? [ F (firing_1 ∧ firing_2 ∧ ... ∧ firing_N) ]`
2. **Firing Rate Bounds**: `P=? [ G (firing_rate ∈ [min_rate, max_rate]) ]`
3. **Pattern Convergence**: `P=? [ F stable_pattern ]`
4. **Silence Guarantee**: `P=? [ G (no_input → F silence) ]` (Asymptotic Silence)

### Gray Zone Analysis

The fidelity theorem bounds firing disagreement to a **gray zone** around threshold:
- Neurons with membrane potential near threshold may fire differently in concrete vs. abstract
- The width of the gray zone is a **known function** of `W`
- Properties that don't depend on gray-zone neurons are **exactly preserved**

## Validation Results

- Empirically tested across **seven canonical topologies**:
  - Feedforward chains, recurrent loops, small-world, scale-free, ring, random, grid
- **State space reduction** matches theoretical predictions
- **Verification time** reduced from intractable to seconds for moderate networks

## Limitations

- **Discretization artifacts**: very fine temporal dynamics may be lost at coarse `W`
- **Probabilistic transition explosion**: still grows with network size despite quotient reduction
- **Large-scale networks**: practical verification limited to ~20-30 neurons even with reduction
- **Continuous-time SNNs**: framework is discrete-time only