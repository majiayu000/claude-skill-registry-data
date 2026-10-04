---
name: qml-model-testing
description: >
  Quantum Machine Learning model testing and robustness analysis methodology.
  Covers mutation testing for QNN circuits, accuracy/robustness evaluation of
  Variational Quantum Circuits (VQCs), and practical considerations for deploying
  QML models on NISQ-era quantum hardware. Use when: (1) testing quantum neural
  network implementations for correctness, (2) evaluating QML model robustness
  against circuit faults and noise, (3) designing test suites for parametrized
  quantum circuits, (4) analyzing VQC accuracy under hardware constraints,
  (5) preparing QML models for deployment on real quantum hardware.
---

# QML Model Testing & Robustness

## Overview

Quantum Machine Learning models (especially QNNs built on VQCs) require specialized
testing approaches due to their hybrid quantum-classical nature, parameterized gates,
and sensitivity to noise. This skill provides systematic methodologies for testing,
evaluating, and hardening QML models.

## Core Testing Methodologies

### 1. Mutation Testing for QML

Based on arxiv:2605.00107. Mutation testing injects faults into quantum circuits to
verify test suite adequacy.

**Mutation Operations for Quantum Circuits:**
- Gate insertion: Add random single/two-qubit gates
- Gate deletion: Remove gates from the circuit
- Gate replacement: Swap gate types (e.g., RX → RY)
- Parameter perturbation: Modify rotation angles by small ε
- Wire swap: Exchange qubit connections

**Workflow:**
1. Define original QNN circuit architecture
2. Generate mutant circuits via mutation operations
3. Run test suite against each mutant
4. Calculate mutation score = (killed mutants) / (total non-equivalent mutants)
5. Augment test suite to kill surviving mutants

**Equivalence Detection:**
Two circuits are equivalent if they produce identical output distributions for all
inputs. Use symbolic simplification or randomized benchmarking to detect equivalences.

### 2. Accuracy & Robustness Analysis of QNNs

Based on arxiv:2604.26110. Systematic evaluation of VQC-based QNNs.

**Evaluation Dimensions:**
- **Accuracy**: Classification/regression performance on benchmark datasets
- **Robustness to noise**: Performance degradation under depolarizing, amplitude
  damping, and phase damping noise models
- **Parameter sensitivity**: Gradient magnitude analysis and barren plateau detection
- **Expressibility**: Circuit's ability to explore Hilbert space (use KL divergence
  from Haar-random distribution)
- **Entangling capability**: Multi-qubit correlation strength

**Testing Protocol:**
```
1. Train QNN on clean data → record baseline accuracy
2. Inject noise at varying levels (0.001 → 0.1 error rates)
3. Measure accuracy degradation curve
4. Test parameter initialization sensitivity (random vs structured)
5. Evaluate gradient vanishing across circuit depth
6. Report: accuracy at target noise level, max tolerable depth
```

### 3. Hardware Readiness for NISQ Devices

Based on arxiv:2604.24886. Preparing QNNs for real quantum hardware.

**Key Constraints:**
- Limited qubit count (current: ~100-1000 physical qubits)
- Gate fidelity (typically 99%+ for single-qubit, 95-99% for two-qubit)
- Coherence time limits circuit depth (~100-500 gates)
- Connectivity constraints (coupling maps)

**Pre-Deployment Checklist:**
1. Map circuit to target hardware topology (minimize SWAP gates)
2. Transpile to native gate set
3. Estimate circuit depth vs coherence time budget
4. Simulate with realistic noise model
5. Apply error mitigation (zero-noise extrapolation, readout correction)
6. Validate on simulator before hardware execution

## Practical Guidelines

### When to Use Each Approach

| Scenario | Method |
|----------|--------|
| New QNN implementation | Mutation testing + accuracy baseline |
| Production QML pipeline | Full robustness analysis + noise simulation |
| Hardware deployment | Hardware readiness checklist + error mitigation |
| Model comparison | Expressibility + entangling capability metrics |

### Common Pitfalls

- **Barren plateaus**: Deep VQCs with random initialization suffer from vanishing
  gradients. Use layer-wise training or problem-inspired ansatz.
- **Over-parameterization**: Too many parameters relative to training data causes
  overfitting. Monitor train/test gap.
- **Noise amplification**: Error mitigation can amplify statistical noise. Balance
  shot count with mitigation overhead.
- **Equivalent mutants**: Many circuit mutations are functionally equivalent. Filter
  before computing mutation scores.

## Resources

- arxiv:2605.00107 - Mutation Testing of QML Models
- arxiv:2604.26110 - Accuracy & Robustness in QNNs
- arxiv:2604.24886 - Large-scale QNNs for Quantum Hardware
