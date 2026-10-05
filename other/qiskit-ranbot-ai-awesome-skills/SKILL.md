---
name: qiskit
description: Qiskit is the world's most popular open-source quantum computing framework with 13M+ downloads. Build quantum circuits, optimize for hardware, execute on simulators or real quantum computers, and anal
category: Creative & Media
source: antigravity
tags: [python, api, ai, workflow]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/qiskit
---


# Qiskit

## When to Use

- You are building or optimizing quantum circuits with Qiskit for simulators or real hardware.
- You need IBM Quantum-style tooling for transpilation, execution, visualization, or algorithm libraries.
- You want guidance on moving from a simple circuit prototype to backend-aware execution.

## Overview

Qiskit is the world's most popular open-source quantum computing framework with 13M+ downloads. Build quantum circuits, optimize for hardware, execute on simulators or real quantum computers, and analyze results. Supports IBM Quantum (100+ qubit systems), IonQ, Amazon Braket, and other providers.

**Key Features:**
- 83x faster transpilation than competitors
- 29% fewer two-qubit gates in optimized circuits
- Backend-agnostic execution (local simulators or cloud hardware)
- Comprehensive algorithm libraries for optimization, chemistry, and ML

## Quick Start

### Installation

```bash
uv pip install qiskit
uv pip install "qiskit[visualization]" matplotlib
```

### First Circuit

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# Create Bell state (entangled qubits)
qc = QuantumCircuit(2)
qc.h(0)           # Hadamard on qubit 0
qc.cx(0, 1)       # CNOT from qubit 0 to 1
qc.measure_all()  # Measure both qubits

# Run locally
sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.meas.get_counts()
print(counts)  # {'00': ~512, '11': ~512}
```

### Visualization

```python
from qiskit.visualization import plot_histogram

qc.draw('mpl')           # Circuit diagram
plot_histogram(counts)   # Results histogram
```

## Core Capabilities

### 1. Setup and Installation
For detailed installation, authentication, and IBM Quantum account setup:
- **See `references/setup.md`**

Topics covered:
- Installation with uv
- Python environment setup
- IBM Quantum account and API token configuration
- Local vs. cloud execution

### 2. Building Quantum Circuits
For constructing quantum circuits with gates, measurements, and composition:
- **See `references/circuits.md`**

Topics covered:
- Creating circuits with QuantumCircuit
- Single-qubit gates (H, X, Y, Z, rotations, phase gates)
- Multi-qubit gates (CNOT, SWAP, Toffoli)
- Measurements and barriers
- Circuit composition and properties
- Parameterized circuits for variational algorithms

### 3. Primitives (Sampler and Estimator)
For executing quantum circuits and computing results:
- **See `references/primitives.md`**

Topics covered:
- **Sampler**: Get bitstring measurements and probability distributions
- **Estimator**: Compute expectation values of observables
- V2 interface (StatevectorSampler, StatevectorEstimator)
- IBM Quantum Runtime primitives for hardware
- Sessions and Batch modes
- Parameter binding

### 4. Transpilation and Optimization
For optimizing circuits and preparing for hardware execution:
- **See `references/transpilation.md`**

Topics covered:
- Why transpilation is necessary
- Optimization levels (0-3)
- Six transpilation stages (init, layout, routing, translation, optimization, scheduling)
- Advanced features (virtual permutation elision, gate cancellation)
- Common parameters (initial_layout, approximation_degree, seed)
- Best practices for efficient circuits

### 5. Visualization
For displaying circuits, results, and quantum states:
- **See `references/visualization.md`**

Topics covered:
- Circuit drawings (text, matplotlib, LaTeX)
- Result histograms
- Quantum state visualization (Bloch sphere, state city, QSphere)
- Backend topology and error maps
- Customization and styling
- Saving publication-quality figures

### 6. Hardware Backends
For running on simulators and real quantum computers:
- **See `references/backends.md`**

Topics covered:
- IBM Quantum backends and authentication
- Backend properties and status
- Running on real hardware with Runtime primitives
- Job management and queuing
- Session mode (iterative algorithms)
- Batch mode (parallel jobs)
- Local simulators (StatevectorSampler, Aer)
- Third-party providers (IonQ, Amazon Braket)
- Error mitigation strategies

### 7. Qiskit Patterns Workflow
For implementing the four-step quantum computing workflow:
- **See `references/patterns.md`**

Topics covered:
- **Map**: Translate problems to quantum circuits
- **Optimize**: Transpile for hardware
- **Execute**: Run with primitives
- **Post-process**: Extract and analyze results
- Complete VQE example
- Session vs. Batch execution
- Common workflow patterns

### 8. Quantum Algorithms and Applications
For implementing specific quantum algorithms:
- **See `references/algorithms.md`**

Topics covered:
- **Optimization**: VQE, QAOA, Grover's algorithm
- **Chemistry**: Molecular ground states, excited states, Hamiltonians
- **Machine Learning**: Quantum kernels, VQC, QNN
- **Algorithm libraries**: Qiskit Nature, Qiskit ML, Qiskit Optimization
- Physics simulations and benchmarking

## Workflow Decision Guide

**If you need to:**
