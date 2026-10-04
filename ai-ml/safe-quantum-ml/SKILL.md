---
name: safe-quantum-ml
description: "SAFE Quantum Machine Learning methodology — variational quantum classifiers with amplitude encoding, learnable classical pre-encoding, and SAFE-AI reliability metrics (Cramer-von-Mises-based accuracy/robustness/explainability evaluation). For designing safety-critical quantum ML models."
---

# SAFE Quantum Machine Learning

## Description
SAFE Quantum Machine Learning methodology combining variational quantum classifiers (VQCs) with amplitude encoding and learnable classical pre-encoding layers. Uses SAFE-AI evaluation framework (accuracy, robustness, explainability via Cramer-von-Mises divergence) for systematic reliability assessment of quantum ML models in safety-critical applications. Based on arXiv:2605.16067.

## Activation Keywords
- safe quantum ml
- quantum classifier safety
- quantum ml reliability
- variational quantum classifier
- quantum amplitude encoding
- 量子机器学习安全性
- quantum robustness evaluation
- SAFE-AI metrics
- quantum model explainability
- amplitude encoding classifier

## Tools Used
- terminal: Run quantum ML experiments (PennyLane, Qiskit, or custom VQC implementations)
- write: Create SKILL.md and supporting experiment scripts
- search_files: Find existing quantum ML code or skills

## Core Concepts

### SAFE Framework Dimensions
| Dimension | Metric | Purpose |
|-----------|--------|---------|
| **S**ecurity | Adversarial robustness | Resistance to input perturbations |
| **A**ccuracy | Predictive performance | Classification/regression quality |
| **F**airness | Bias detection | Equitable predictions across groups |
| **E**xplainability | Cramer-von-Mises divergence | Interpretable feature attribution |

### SAFE-AI Evaluation
- Uses **Cramer-von-Mises (CvM) divergence** for consistent reliability evaluation
- Measures consistency across accuracy, robustness, and explainability dimensions
- Provides balanced reliability profiles for comparing quantum vs classical models

## Usage Patterns

### Pattern 1: SAFE VQC Design
Build a variational quantum classifier with the SAFE architecture:

1. **Classical Pre-Encoding Layer**: Learnable classical layer that maps raw features to amplitude-encoded quantum states
2. **Amplitude Encoding**: Normalized input vectors → quantum state amplitudes
3. **Parameterized Quantum Circuit (PQC)**: Variational quantum circuit for classification
4. **Bounded Observables**: Quantum observables with bounded eigenvalues for stable gradients

### Pattern 2: SAFE Reliability Evaluation
Evaluate quantum ML models using the SAFE-AI framework:

1. Compute **accuracy** on test set
2. Measure **robustness** via input perturbation response
3. Assess **explainability** via CvM-based feature attribution
4. Generate **balanced SAFE score** across all dimensions

### Pattern 3: Quantum-Classical Comparison
Compare quantum models with classical baselines using SAFE metrics:

1. Train equivalent classical model with same architecture depth
2. Apply identical SAFE evaluation pipeline
3. Compare SAFE profiles (not just accuracy)
4. Identify trade-offs between quantum and classical approaches

## Instructions for Agents

### Step 1: Problem Definition
- Determine if the task is suitable for quantum ML (small-to-medium datasets, structured features)
- Define SAFE requirements: which dimensions (S/A/F/E) are most critical

### Step 2: Data Preparation
- Normalize input features to [0, 1] range for amplitude encoding
- Ensure feature dimension matches quantum register size (2^n features for n qubits)
- Split into train/validation/test sets

### Step 3: Architecture Design
- Design classical pre-encoding layer (typically MLP)
- Choose PQC architecture (hardware-efficient, alternating layers, etc.)
- Select bounded quantum observables (typically Z-basis measurements)
- Determine number of qubits and circuit depth

### Step 4: Training
- Use hybrid quantum-classical optimization (e.g., SPSA, Adam)
- Apply gradient clipping for stable training
- Monitor convergence and barren plateau indicators
- Use mini-batch training with shot-based estimation

### Step 5: SAFE Evaluation
- **Security**: Test adversarial robustness (PGD, FGSM attacks)
- **Accuracy**: Standard metrics (accuracy, F1, AUC)
- **Fairness**: Check prediction bias across demographic groups
- **Explainability**: Compute CvM divergence for feature importance

### Step 6: Comparison & Reporting
- Compare with classical baselines using SAFE profiles
- Document trade-offs and quantum advantage (if any)
- Report all four SAFE dimensions, not just accuracy

## Error Handling

### Barren Plateaus
- If gradients vanish: reduce circuit depth, use layer-wise training
- Try different initialization strategies
- Use problem-inspired ansatz instead of hardware-efficient

### Shot Noise
- If shot noise dominates: increase shots, use variance reduction
- Consider analytical gradients where possible

### Amplitude Encoding Dimensionality
- If features ≠ 2^n: pad with zeros or use PCA to reduce
- Consider angle encoding for large feature spaces

## Examples

### Example: Binary Classification with SAFE VQC
```python
# Conceptual architecture
class SafeVQC:
    def __init__(self, n_qubits=4, n_layers=2):
        self.pre_encoding = nn.Linear(n_features, 2**n_qubits)  # Classical
        self.pqc = ParameterizedQuantumCircuit(n_qubits, n_layers)
        self.observable = BoundedObservable(n_qubits)
    
    def forward(self, x):
        # Classical pre-encoding
        encoded = self.pre_encoding(x)
        # Amplitude normalization
        encoded = encoded / torch.norm(encoded, dim=1, keepdim=True)
        # Quantum circuit
        quantum_state = self.pqc(encoded)
        # Bounded measurement
        return self.observable(quantum_state)
```

## Limitations
- Currently demonstrated on small-scale problems (≤ 10 qubits)
- Requires careful hyperparameter tuning
- Shot noise limits gradient estimation precision
- Not yet proven for large-scale real-world datasets

## Resources
- arXiv:2605.16067 — "SAFE Quantum Machine Learning with Variational Quantum Classifiers"
- PennyLane: https://pennylane.ai
- Qiskit: https://qiskit.org

## Related Skills
- `quantum-ml-patterns` — General QML research patterns
- `qml-mutation-testing` — QML model testing and robustness
- `quantum-neural-architecture` — QNN architecture design
