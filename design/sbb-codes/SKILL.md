---
name: sbb-codes
description: "Subsystem Bivariate Bicycle (SBB) codes methodology for quantum error correction. Reduces high-rate BB code stabilizer checks from weight-6+ to local weight-4 gauge measurements via CSS subsystem construction. Use when: (1) designing qLDPC codes with low-weight syndrome extraction, (2) implementing BB codes on hardware with limited connectivity, (3) analyzing topological properties of subsystem codes, (4) constructing finite-depth Clifford circuits for gauge qubit decoupling. Activation: sbb codes, subsystem bicycle codes, weight-4 qec, bb code syndrome, gauge measurement qec, low-overhead quantum memory."
---

# Subsystem Bivariate Bicycle (SBB) Codes

## Overview

Subsystem Bivariate Bicycle (SBB) codes are a translation-invariant CSS subsystem construction that realizes bivariate bicycle (BB) code logical structure using **local weight-4 gauge measurements** instead of the typical weight-6+ stabilizer checks. This makes high-rate qLDPC codes practically implementable on hardware with limited connectivity.

**Source**: arXiv:2605.04151 - "Topological subsystem bivariate bicycle codes with four-qubit check operators" by Zijian Liang, Yu-An Chen (May 2026).

## Core Methodology

### Key Insight

BB codes achieve high encoding rates but have stabilizer checks of weight ≥ 6, making syndrome extraction challenging. SBB codes decompose these into:
1. **Weight-4 gauge operators** that are locally measurable
2. **Stabilizer syndromes** inferred by multiplying corresponding gauge outcomes

### Construction Steps

1. **Define the BB code** on a toric lattice using bivariate polynomials
2. **Decompose high-weight stabilizers** into weight-4 gauge operators via CSS subsystem construction
3. **Verify translation invariance** — gauge operators must respect the lattice symmetry
4. **Check for nonlocal stabilizers** using the determinantal-ideal criterion (see references/determinantal-criterion.md)
5. **Construct finite-depth Clifford circuit** to decouple gauge qubits and identify protected subsystem

### Determinantal-Ideal Criterion

For translation-invariant CSS subsystem codes, nonlocal stabilizers are detected using a criterion based on the gauge-operator commutation matrix:
- Compute the commutation matrix of gauge operators
- Apply the determinantal-ideal test
- If criterion excludes nonlocal stabilizers → finite-depth Clifford circuit exists

### Topology Condition

An SBB code is **topological** (no nontrivial local logical operators) **if and only if** the corresponding BB code is topological.

## Known Code Examples

| Code | Parameters | Notes |
|------|-----------|-------|
| SBB-1 | [[27,6,3]] | Low-overhead example |
| SBB-2 | [[75,10,5]] | Moderate distance |
| SBB-3 | [[108,12,6]] | 6× more logical qubits than subsystem surface code at same block length and distance |

## Advantages over Standard BB Codes

1. **Weight-4 measurements** — compatible with superconducting qubit architectures
2. **Higher encoding rate** — [[108,12,6]] vs surface code [[108,2,6]]
3. **Subsystem structure** — gauge degrees of freedom enable flexible decoding
4. **Topological protection** — inherits topological properties from parent BB code

## Implementation Considerations

### Syndrome Extraction

```
Stabilizer S_i = g_a × g_b × ... × g_k  (product of gauge outcomes)
```

- Measure all weight-4 gauge operators in parallel
- Multiply outcomes to obtain stabilizer syndromes
- Use standard BP+OSD or MWPM decoding on inferred syndromes

### Gauge Qubit Management

- Finite-depth Clifford circuit decouples gauge qubits
- Protected subsystem identified with corresponding BB stabilizer code
- Gauge qubits can be initialized to |0⟩ or measured and discarded

### Hardware Mapping

- Requires local connectivity (nearest-neighbor or near-nearest-neighbor)
- Compatible with superconducting qubit and trapped-ion architectures
- Measurement scheduling must respect gauge operator commutation relations

## Activation Keywords

- sbb codes
- subsystem bicycle codes
- weight-4 qec
- bb code syndrome extraction
- gauge measurement quantum error correction
- low-overhead quantum memory
- subsystem qldpc codes
- determinantal ideal criterion

## Related Skills

- quantum-error-correction-methods: General QEC patterns
- distributed-quantum-error-correction: Distributed QEC architectures
- quantum-fault-tolerance-benchmark: QEC code evaluation

## References

- arXiv:2605.04151 — Original paper with full mathematical derivation
- references/determinantal-criterion.md — Determinantal-ideal criterion details
