---
name: gated-qkan-fwp
description: "Quantum-inspired sequence learning using Gated QKAN-FWP (Quantum Fast Weight Programmers with variational quantum Kolmogorov-Arnold Networks). Use this skill for designing quantum-inspired sequence models, temporal encoding for quantum ML, fast weight programming patterns, and Kolmogorov-Arnold Network architectures for sequential data. Also triggered by: quantum sequence learning, QKAN, fast weight programmer, quantum-inspired RNN, temporal encoding quantum, 量子序列学习."
---

# Gated QKAN-FWP: Quantum-Inspired Sequence Learning

Based on "Gated QKAN-FWP: Scalable Quantum-inspired Sequence Learning" (arXiv: 2605.06734).

## When to Use

- Designing quantum-inspired sequence models for time-series or NLP
- Replacing traditional RNN/LSTM with quantum-inspired fast weight architectures
- Implementing temporal encoding for quantum machine learning
- Building Kolmogorov-Arnold Network variants for sequential data
- Seeking scalable alternatives to full quantum circuits for sequence tasks

## Core Concepts

### Quantum Fast Weight Programmers (QFWP)

Fast Weight Programmers generate weight matrices dynamically from input. In the quantum-inspired variant:

```python
# Classical FWP pattern
def fast_weight(input_seq, base_weights):
    """Generate dynamic weights from input sequence."""
    # Input-dependent weight generation
    for x in input_seq:
        delta_w = generate_delta(x)  # quantum-inspired transformation
        base_weights += delta_w
    return base_weights
```

### Variational Quantum Kolmogorov-Arnold Networks (QKAN)

Kolmogorov-Arnold Networks parameterize functions as sums of 1D functions:
```
f(x) = Σ φ_q(Σ ψ_{q,p}(x_p))
```

QKAN replaces classical 1D functions with parameterized quantum circuits:
```
f(x) = Σ_q ⟨0| U_q(x)† O_q U_q(x) |0⟩
```

### Quantum-Inspired Temporal Encoding

Key insight: quantum circuits naturally encode temporal information through gate sequencing. The temporal encoding pattern:

1. **Time-aware initialization**: Map temporal position to phase angles
2. **Sequential gate application**: Each timestep applies a rotation conditioned on previous state
3. **Interference-based memory**: Constructive/destructive interference captures long-range dependencies

## Implementation Pattern

### Step 1: Define the QKAN Layer

```python
import numpy as np
from pennylane import numpy as pnp

def qkan_layer(x, params, n_qubits):
    """Single QKAN layer with variational quantum circuit."""
    # Initialize quantum state
    # Apply data encoding
    # Apply variational ansatz
    # Measure expectation value
    pass

def qkan_forward(x_seq, qkan_params, n_qubits):
    """Process sequence through QKAN."""
    outputs = []
    for x in x_seq:
        out = qkan_layer(x, qkan_params, n_qubits)
        outputs.append(out)
    return np.array(outputs)
```

### Step 2: Fast Weight Generation

```python
def gated_qkan_fwp(x_seq, base_weights, gate_params):
    """Gated QKAN-FWP for sequence learning.
    
    Args:
        x_seq: Input sequence (T, d_input)
        base_weights: Base weight matrix (d_model, d_model)
        gate_params: Parameters for quantum-inspired gates
    
    Returns:
        outputs: Processed sequence (T, d_model)
    """
    # Generate fast weights from input
    fast_weights = generate_fast_weights(x_seq, gate_params)
    
    # Apply gated mechanism (sigmoid gate controls information flow)
    gate = sigmoid(linear(x_seq, gate_params))
    
    # Combine base and fast weights
    effective_weights = base_weights + gate * fast_weights
    
    # Apply to sequence
    outputs = einsum('td,dm->tm', x_seq, effective_weights)
    return outputs
```

### Step 3: Training Loop

```python
def train_gated_qkan_fwp(data, labels, n_qubits, lr=0.001, epochs=100):
    """Train Gated QKAN-FWP model."""
    # Initialize parameters
    qkan_params = init_qkan_params(n_qubits)
    gate_params = init_gate_params()
    
    for epoch in range(epochs):
        # Forward pass
        outputs = gated_qkan_fwp(data, qkan_params, gate_params)
        loss = compute_loss(outputs, labels)
        
        # Compute gradients (parameter-shift rule or finite differences)
        qkan_grad = compute_gradients(loss, qkan_params)
        gate_grad = compute_gradients(loss, gate_params)
        
        # Update parameters
        qkan_params -= lr * qkan_grad
        gate_params -= lr * gate_grad
        
    return qkan_params, gate_params
```

## Key Patterns

### Pattern 1: Temporal Encoding via Quantum Gates

Map temporal sequence to quantum circuit:

```
t=0 → R_z(θ_0) R_x(ϕ_0)
t=1 → R_z(θ_1) R_x(ϕ_1)  
t=2 → R_z(θ_2) R_x(ϕ_2)
```

Where θ_t, ϕ_t are functions of input at time t.

### Pattern 2: Fast Weight Decomposition

Decompose fast weight generation into:
- **Key extraction**: `k_t = W_k x_t`
- **Value generation**: `v_t = W_v x_t`  
- **Fast weight**: `ΔW_t = k_t ⊗ v_t` (outer product)

### Pattern 3: Gated Information Flow

Use sigmoid gates to control how much fast weight contributes:
```
g_t = σ(W_g [x_t; h_{t-1}])
W_fast = g_t ⊙ ΔW_t
```

## Design Guidelines

1. **Qubit count**: Start with 4-8 qubits for sequence modeling
2. **Circuit depth**: Keep shallow (2-4 layers) to avoid barren plateaus
3. **Encoding**: Use amplitude encoding for dense data, angle encoding for sparse
4. **Measurement**: Expectation value of Pauli-Z for classification tasks
5. **Training**: Use parameter-shift rule for gradient computation

## When NOT to Use

- Very long sequences (>1000 steps) — consider classical alternatives
- Real-time inference on edge devices — quantum-inspired overhead
- Tasks requiring exact reproducibility — quantum stochasticity

## Related Papers

- QuanForge (arXiv: 2604.20706) — Mutation testing for QNNs
- SPATE (arXiv: 2604.11022) — Spiking-phase temporal encoding for QML
- Quantum-Inspired Optimization (arXiv: 2605.07947) — QIEO for non-convex ML
