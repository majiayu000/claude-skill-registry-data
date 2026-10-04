---
name: diagonal-ano-qnn
description: "Diagonal Adaptive Non-local Observables (ANO) methodology for quantum neural networks — reduces observable parameter complexity from O(4^k) to O(2^k) while retaining full ANO expressivity via diagonal canonical representatives. For efficient VQA measurement design."
---

# Diagonal Adaptive Non-local Observables (ANO)

## Description
Diagonal Adaptive Non-local Observables methodology that significantly reduces the parameter burden and classical optimization cost of ANO-based Variational Quantum Algorithms by using only diagonal observables. Mathematically equivalent to full ANO modulo unitary similarity, reducing k-local observable complexity from O(4^k) to O(2^k). Based on arXiv:2605.15410.

## Activation Keywords
- diagonal ano
- adaptive non-local observables
- quantum observable design
- vqa measurement optimization
- quantum neural network observables
- observable parameter reduction
- 量子可观测量设计
- variational quantum algorithm measurement
- diagonal observable vqa

## Tools Used
- terminal: Run quantum circuit simulations (PennyLane, Qiskit)
- write: Create SKILL.md and experiment scripts
- search_files: Find existing QNN code

## Core Concepts

### The ANO Problem
Adaptive Non-local Observables (ANOs) make quantum observables **dynamic** during VQA training, enlarging the function space beyond fixed observables. However, full Hermitian ANOs have:
- **O(4^k)** parameters for k-local observables
- Steep classical optimization cost
- Hardware demands shift from circuit synthesis to measurement design

### The Diagonal ANO Solution
Key insight: **Diagonal matrices are canonical representatives of the ANO space modulo unitary similarity**.

This means:
- Diagonal ANO + arbitrary quantum circuit ≡ Full ANO + restricted circuit
- Parameter reduction: **O(4^k) → O(2^k)** for k-local observables
- Classical computation cost reduced proportionally
- Conventional VQCs become a special case (fixed diagonal observable)

### Mathematical Equivalence
For any full ANO (Hermitian H), there exists a unitary U such that:
- U†HU = D (diagonal)
- The circuit U can be absorbed into the variational ansatz
- Therefore: diagonal observable + richer circuit = full observable + simpler circuit

## Usage Patterns

### Pattern 1: Diagonal ANO VQA Design
Design a VQA using diagonal ANO instead of full ANO:

1. **Fix observable as diagonal**: O = diag(λ₁, λ₂, ..., λ_{2^n})
2. **Enrich variational circuit**: Add layers to compensate for observable restriction
3. **Optimize diagonal entries**: Only 2^n parameters instead of 4^n (full Hermitian)
4. **Measure in computational basis**: No need for complex measurement bases

### Pattern 2: Complexity Reduction
When designing ANO-based VQAs:

1. Calculate full ANO parameter count: 4^k for k-local
2. Replace with diagonal ANO: 2^k parameters
3. Add compensating circuit layers: ~O(k·n) additional gates
4. Net gain: exponential parameter reduction with linear gate overhead

### Pattern 3: Hybrid Ansatz Design
Combine diagonal ANO with specific circuit architectures:

1. **Data re-uploading circuits**: Interleave data encoding with variational layers
2. **Hardware-efficient ansatz**: Match device native gate set
3. **Problem-inspired ansatz**: Encode problem structure in circuit, keep observable simple

## Instructions for Agents

### Step 1: Problem Analysis
- Determine if the VQA problem benefits from adaptive observables
- Assess k-locality requirements (how many qubits per observable term)
- Calculate full ANO vs diagonal ANO parameter budgets

### Step 2: Observable Design
- Initialize diagonal observable with random eigenvalues
- Constrain eigenvalues if problem requires (e.g., binary classification: ±1)
- Ensure observable is measurable in computational basis

### Step 3: Circuit Design
- Design variational ansatz to compensate for diagonal observable restriction
- Use sufficient expressivity (number of layers ≥ log(4^k / 2^k) = k·log2)
- Consider hardware connectivity constraints

### Step 4: Training
- Use hybrid classical-quantum optimization
- Optimize circuit parameters AND diagonal observable eigenvalues jointly
- Monitor gradient norms for barren plateaus
- Compare convergence with full ANO baseline

### Step 5: Validation
- Verify diagonal ANO achieves comparable performance to full ANO
- Measure parameter efficiency (performance per parameter)
- Document trade-offs between circuit depth and observable complexity

## Error Handling

### Under-expressive Circuit
- If diagonal ANO underperforms full ANO: increase circuit depth/expressivity
- Add entangling layers or data re-uploading blocks
- Check that circuit can generate the unitary that diagonalizes the optimal full ANO

### Barren Plateaus
- If gradients vanish: reduce circuit depth, use layer-wise training
- Try different ansatz structures
- Consider problem-inspired initialization

### Eigenvalue Constraints
- If eigenvalues need specific values (e.g., ±1 for classification):
  - Parameterize as O = U† diag(±1) U where U is fixed
  - Optimize only the diagonal entries within constraints

## Examples

### Example: Binary Classification with Diagonal ANO
```python
# Conceptual implementation
class DiagonalANO_VQC:
    def __init__(self, n_qubits, n_layers):
        # Diagonal observable: 2^n parameters (vs 4^n for full ANO)
        self.diagonal_eigenvalues = nn.Parameter(torch.randn(2**n_qubits))
        # Variational circuit: richer to compensate
        self.circuit = VariationalCircuit(n_qubits, n_layers)
    
    def forward(self, x):
        # Encode input
        state = self.encode(x)
        # Variational circuit
        state = self.circuit(state)
        # Measure in computational basis with diagonal observable
        return self.diagonal_eigenvalues @ self.measure_probabilities(state)
```

## Limitations
- Requires sufficiently expressive variational circuit
- Diagonal ANO parameter count still exponential in qubit number (2^n)
- Best suited for problems where observable adaptivity provides significant benefit
- Classical simulation overhead for large qubit counts

## Resources
- arXiv:2605.15410 — "Diagonal Adaptive Non-local Observables on Quantum Neural Networks"
- PennyLane: https://pennylane.ai

## Related Skills
- `safe-quantum-ml` — SAFE evaluation for quantum ML models
- `quantum-neural-architecture` — QNN architecture design
- `quantum-ml-patterns` — General QML research patterns
